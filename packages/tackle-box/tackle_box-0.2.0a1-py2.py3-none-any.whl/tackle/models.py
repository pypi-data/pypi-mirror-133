"""Models for the project."""
import os
from pathlib import Path
from pydantic import BaseModel, SecretStr, Field, Extra, validator
from typing import Any, Union, Optional

from tackle.utils.paths import work_in
from tackle.providers import ProviderList
from tackle.render import wrap_jinja_braces


class Context(BaseModel):
    """The main object that is being modified by parsing."""

    # Mode
    no_input: bool = False
    verbose: bool = False

    # Source
    password: SecretStr = None
    directory: str = None

    # Inputs
    input_string: str = None
    input_dir: Path = None
    input_file: str = None
    version: str = Field(
        None,
        description="For inputs referencing remote repos, this refers to "
        "a branch or tag.",
    )
    existing_context: dict = {}
    overwrite_inputs: Union[dict, str] = None

    input_dict: dict = {}
    output_dict: dict = {}
    keys_to_remove: list = []

    # Internal
    key_path: list = []
    providers: ProviderList = None
    calling_directory: str = os.path.abspath(os.path.curdir)
    env: Any = None

    global_args: list = None
    global_kwargs: dict = None
    global_flags: list = None

    # post_exec_handlers: list = []

    def __init__(self, **data: Any):
        super().__init__(**data)
        # Allows for passing the providers between tackle runtimes
        if self.providers is None:
            # Native and settings.extra_providers initialized
            self.providers = ProviderList()


class BaseHook(BaseModel):
    """
    Base hook class from which all other hooks inherit from to be discovered. There are
    a number of reserved keys that are used for logic such as `if` and `for` that are
    aliased to `if_` and `for_` to not collide with python reserved key words. We also
    append underscores to

    """

    hook_type: str = Field(..., description="Name of the hook.")

    # TODO: Serialize the access modifier earlier in parsing - Could store the arrow in
    #  key_path as boolean. Would have big changes to tackle.utils.dicts
    # access_modifier: Literal['public', 'private'] = None

    if_: Union[str, bool] = Field(None, render_by_default=True)
    else_: Union[str, bool] = Field(None, render_by_default=True)
    for_: Union[str, list] = Field(None, render_by_default=True)
    reverse: Union[str, bool] = Field(None, render_by_default=True)

    while_: Union[str, bool] = None  # TODO
    match_: Any = None  # TODO
    case_: list = None  # TODO

    callback: str = None
    chdir: Optional[str] = Field(None, description="Name of the hook.")
    merge: Union[bool, str] = None
    confirm: Optional[Any] = None

    # context: Context
    input_dict: Union[dict, list] = None
    output_dict: Union[dict, list] = {}
    existing_context: dict = None
    no_input: bool = None
    calling_directory: Path = None

    providers_: ProviderList = None  # TODO: RM? - Not really needed
    key_path_: list = None

    # Placeholder until help can be fully worked out
    help: str = None

    _args: list = []
    _kwargs: dict = {}
    _flags: list = []
    # Fields that should not be rendered by default
    _render_exclude_default: set = {'input_dict', 'output_dict', 'hook_type'}
    _render_exclude: set = {}
    _render_by_default: list = []

    @validator('if_', 'else_', 'reverse', 'for_', 'merge')
    def wrap_bool_if_string(cls, v):
        return wrap_jinja_braces(v)

    # Per https://github.com/samuelcolvin/pydantic/issues/1577
    # See below
    def __setattr__(self, key, val):
        """Override method to alias input fields."""
        if key in self.__config__.alias_to_fields:
            key = self.__config__.alias_to_fields[key]
        super().__setattr__(key, val)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.forbid
        validate_assignment = True
        fields = {
            'if_': 'if',
            'else_': 'else',
            'match_': 'match',
            'case_': 'case',
            'for_': 'for',
            'while_': 'while',
            'enumerate_': 'enumerate',
        }
        # Per https://github.com/samuelcolvin/pydantic/issues/1577
        # This is an issue until pydantic 1.9 is released and items can be set with
        # properties which will override the internal __setattr__ method that
        # disregards aliased fields
        alias_to_fields = {v: k for k, v in fields.items()}

    def __init__(self, **data: Any):
        super().__init__(**data)

    def execute(self) -> Any:
        raise NotImplementedError("Every hook needs an execute method.")

    def call(self) -> Any:
        """
        Call main entrypoint to calling hook.

        Handles `chdir` method.
        """
        if self.chdir:
            path = os.path.abspath(os.path.expanduser(self.chdir))
            if os.path.isdir(path):
                # Use contextlib to switch dirs
                with work_in(os.path.abspath(os.path.expanduser(self.chdir))):
                    return self.execute()
            else:
                raise NotADirectoryError(
                    f"The specified path='{path}' to change to was not found."
                )
        else:
            return self.execute()
