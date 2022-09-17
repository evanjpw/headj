from __future__ import annotations
from dataclasses import dataclass
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from rich import console, theme
from typing import AnyStr, Optional, Union
from typing_extensions import Self

_H_ERROR_THEME = theme.Theme(
    {
        "critical": "bold red underline on white",
        "error": "red",
        "warning": "yellow",
        "info": "green",
        "debug": "cyan",
        "trace": "magenta",
    }
)


@dataclass
class HErrorLevel:
    """HErrorLevel"""

    error_level: int
    color: str


class HErrorLevels:

    CRITICAL = HErrorLevel(CRITICAL, "critical")
    ERROR = HErrorLevel(ERROR, "error")
    WARNING = HErrorLevel(WARNING, "warning")
    INFO = HErrorLevel(INFO, "info")
    DEBUG = HErrorLevel(DEBUG, "debug")
    TRACE = HErrorLevel(5, "trace")

    @staticmethod
    def from_logging(level) -> Optional[Self]:
        if level == CRITICAL:
            return Self.CRITICAL
        elif level == ERROR:
            return Self.ERROR
        elif level == WARNING:
            return Self.WARNING
        elif level == INFO:
            return Self.INFO
        elif level == DEBUG:
            return Self.DEBUG
        elif level == 5:
            return Self.TRACE
        else:
            return None


@dataclass
class HErrorConfig:
    quiet: bool = False
    debug: bool = False
    show_stack_trace = False


class HError:
    _CONFIG = HErrorConfig()

    @classmethod
    def _format(
        cls, e: Union[AnyStr, Exception], error_level: Optional[HErrorLevel] = None
    ) -> (int, str):
        """"""
        is_exception = isinstance(e, Exception)

        if (not cls._CONFIG.debug) and error_level in (
            HErrorLevels.DEBUG,
            HErrorLevels.TRACE,
        ):
            return None, None

        if error_level is None:
            if is_exception:
                error_level = HErrorLevels.ERROR
            else:
                error_level = HErrorLevels.WARNING
        error_text = str(e)
        print("error_level = %r" % error_level)
        text_color = error_level.color
        return error_text, text_color

    @classmethod
    def init_config(
        cls, quiet: bool = False, debug: bool = False, show_stack_trace: bool = False
    ):
        cls._CONFIG.quiet = quiet
        cls._CONFIG.debug = debug
        cls._CONFIG.show_stack_trace = show_stack_trace

    def __init__(
        self, use_stderr: bool = True, color_theme: theme.Theme = _H_ERROR_THEME
    ):
        self.console = console.Console(stderr=use_stderr, theme=color_theme)

    def print(
        self, e: Union[AnyStr, Exception], error_level: Optional[HErrorLevel] = None
    ):
        (error_text, text_color) = self._format(e, error_level)
        if error_text is not None or text_color is not None:
            self.console.print(error_text, style=text_color)
        if isinstance(e, Exception) and self._CONFIG.show_stack_trace:
            self.console.print_exception(show_locals=True)

    def log(
        self, e: Union[AnyStr, Exception], error_level: Optional[HErrorLevel] = None
    ):
        (error_text, text_color) = self._format(e, error_level)
        if error_text is None and text_color is None:
            return
        self.console.log(error_text, style=text_color)

    def debug(self, message: str, *args):
        self.print(message % args, error_level=HErrorLevels.DEBUG)

    def log_debug(self, message: str, *args):
        self.log(message % args, error_level=HErrorLevels.DEBUG)

    def error(self, message: str, *args):
        self.print(message % args, error_level=HErrorLevels.ERROR)

    def warning(self, message: str, *args):
        self.print(message % args, error_level=HErrorLevels.WARNING)


h_error = HError()
