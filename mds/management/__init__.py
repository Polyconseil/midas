# Copyright (c) Polyconseil SAS. All rights reserved.
import contextlib
import logging
import sys
import time

from django.core.management import base


#: Mask those keyword arguments when logging data.
MASKED_ARGUMENT_NAMES = ("password", "secret", "token")


def safe_repr(value):
    res = repr(value)
    if isinstance(res, bytes):
        res = str(res, "utf-8", errors="ignore")
    return res


def fmt_kwarg(key, value):
    """Format a (key, value) pair from kwargs."""
    if any(name in key for name in MASKED_ARGUMENT_NAMES):
        return "%s=<HIDDEN>" % key
    return "%s=%s" % (key, safe_repr(value))


def fmt_params(*args, **kwargs):
    """Format a list of parameters."""
    all_items = [safe_repr(arg) for arg in args]
    all_items.extend(fmt_kwarg(k, v) for k, v in sorted(kwargs.items()))
    return ", ".join(all_items)


@contextlib.contextmanager
def command_duration_logger(command):
    start = time.time()
    try:
        yield
    except Exception:
        command.logger.exception(
            "command=%s failed, duration=%0.2f s",
            command.__module__,
            time.time() - start,
        )
        raise
    command.logger.info(
        "command=%s succeeded, duration=%0.2f s",
        command.__module__,
        time.time() - start,
    )


class EnhancedCommandMixin:
    """Mixin to enhance a Command.

    Provides:
    - self.logger is an already setup logger
    - Any exception apart from CommandError raised during handle() will be logged
    - Command execution time is logged
    - Extra verbose mode will display logs on the console
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__class__.__module__)

    def execute(self, *args, **options):
        if options["verbosity"] > 1:
            # Ease debug by printing logs from all modules to console
            # not just this command's logger
            root_logger = logging.getLogger()
            root_logger.setLevel(
                logging.INFO if options["verbosity"] == 2 else logging.DEBUG
            )
            # It could be self.stdout but it adds an extra carriage return
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)
            stdout_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            stdout_handler.setFormatter(stdout_formatter)
            root_logger.addHandler(stdout_handler)

        with command_duration_logger(self):
            try:
                return super().execute(*args, **options)
            except base.CommandError:  # pylint: disable=try-except-raise
                raise
            except Exception:
                self.logger.exception(
                    "Error when executing %s(%s)",
                    self.__module__,
                    fmt_params(*args, **options),
                )
                raise


class BaseCommand(EnhancedCommandMixin, base.BaseCommand):
    """Enhanced BaseCommand."""

    def handle(self, *args, **options):
        raise NotImplementedError


class AppCommand(EnhancedCommandMixin, base.AppCommand):
    """Enhanced AppCommand."""

    def handle_app_config(self, app_config, **options):
        """
        Perform the command's actions for app_config, an AppConfig instance
        corresponding to an application label given on the command line.
        """
        raise NotImplementedError


class LabelCommand(EnhancedCommandMixin, base.LabelCommand):
    """Enhanced LabelCommand."""

    def handle_label(self, label, **options):
        raise NotImplementedError
