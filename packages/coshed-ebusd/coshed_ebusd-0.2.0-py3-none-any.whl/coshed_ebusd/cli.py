#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

import click

from coshed_ebusd.defaults import CONFIGURATION_SOURCE_LOCAL_ROOT
from coshed_ebusd.defaults import CONFIGURATION_SOURCE_LOCAL
from coshed_ebusd.defaults import CFG_LOCAL_ENABLED
from coshed_ebusd.defaults import EK
from coshed_ebusd.click_glue import simple_verbosity_option
from coshed_ebusd.analysis import perform_analysis, csv_analysis_header

log = logging.getLogger(__name__)


@click.group()
@click.pass_context
@simple_verbosity_option(log)
def analysis_cli(ctx, **kwargs):
    pass


@analysis_cli.command(help="CSV header analysis")
@click.argument(
    "path",
    default=os.path.join(CONFIGURATION_SOURCE_LOCAL_ROOT, "ebusd-2.1.x/de"),
)
@click.option("-v", "--verbose", count=True)
def csv(**kwargs):
    perform_analysis(
        kwargs["path"],
        extensions=(".csv", ".inc"),
        func=csv_analysis_header,
        verbose=kwargs["verbose"],
        use_log=log,
    )


@click.command()
@simple_verbosity_option(log)
@click.option("-p", "port", default=31329, type=int, show_default=True)
@click.option("-a", "bind_address", default="0.0.0.0", show_default=True)
@click.option("--debug/--no-debug", "debug_flag", default=False)
def configuration_server_cli(**kwargs):
    from coshed_ebusd.configuration_files import app

    for item in sorted(EK.values(), key=lambda x: x["key"]):
        key = item["key"]

        log.info(
            "{:40}: {!r}".format(key, os.environ.get(key, item["default"]))
        )

        if not os.environ.get(key) and item.get("description"):
            log.info(
                " By defining the environment variable '{key}' you can define '{description}'".format(
                    **item
                )
            )

    if CFG_LOCAL_ENABLED:
        log.info(
            f"Configuration files will be served from {CONFIGURATION_SOURCE_LOCAL!r}"
        )

    try:
        app.run(
            host=kwargs["bind_address"],
            port=kwargs["port"],
            debug=kwargs["debug_flag"],
        )
    except Exception as exc:
        log.error(exc)
