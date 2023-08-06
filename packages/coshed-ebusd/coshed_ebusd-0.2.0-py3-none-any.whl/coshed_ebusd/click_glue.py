#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import click


def simple_verbosity_option(logger=None, *names, **kwargs):
    """A decorator that adds a `--verbosity, -v` option to the decorated
    command.

    Name can be configured through ``*names``. Keyword arguments are passed to
    the underlying ``click.option`` decorator.

    stolen from click-log
    """

    if not names:
        names = ["--log-level", "-l"]

    kwargs.setdefault("default", "INFO")
    kwargs.setdefault("show_default", True)
    kwargs.setdefault("metavar", "LVL")
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("help", "Either CRITICAL, ERROR, WARNING, INFO or DEBUG")
    kwargs.setdefault("is_eager", True)

    def decorator(f):
        def _set_level(ctx, param, value):
            x = getattr(logging, value.upper(), None)
            if x is None:
                raise click.BadParameter(
                    "Must be CRITICAL, ERROR, WARNING, INFO or DEBUG, not {}"
                )
            logger.setLevel(x)

        return click.option(*names, callback=_set_level, **kwargs)(f)

    return decorator
