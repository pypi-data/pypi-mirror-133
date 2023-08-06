#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

EK = {
    "CONFIGURATION_SOURCE_URL": dict(
        key="EBUSD_CONFIGURATION_URL",
        description="Upstream configuration files source URL",
        default="https://cfg.ebusd.eu:443",
    ),
    "CONFIGURATION_SOURCE_LOCAL_ROOT": dict(
        key="EBUSD_CONFIGURATION_ROOT",
        description="Local configuration files repository root path",
        default="/var/ebusd-configuration",
    ),
}

USER_AGENT = "ebusd/21.3"


CONFIGURATION_SOURCE_URL = os.environ.get(
    EK["CONFIGURATION_SOURCE_URL"]["key"],
    EK["CONFIGURATION_SOURCE_URL"]["default"],
)

DELIMITER = ","

QUOTECHAR = '"'

DIALECT = "unix"

CFG_LOCAL_VER = "latest"

CFG_LOCAL_LANGUAGE_DEFAULT = "de"

CFG_LOCAL_LANGUAGES = {"de", "en"}

CFG_LOCAL_EXTENSIONS = (".csv", ".inc")


CONFIGURATION_SOURCE_LOCAL_ROOT = os.environ.get(
    EK["CONFIGURATION_SOURCE_LOCAL_ROOT"]["key"],
    EK["CONFIGURATION_SOURCE_LOCAL_ROOT"]["default"],
)

CONFIGURATION_SOURCE_LOCAL = os.path.join(
    CONFIGURATION_SOURCE_LOCAL_ROOT, CFG_LOCAL_VER, CFG_LOCAL_LANGUAGE_DEFAULT
)

CFG_LOCAL_ENABLED = os.path.isdir(CONFIGURATION_SOURCE_LOCAL)


MESSAGE_COLUMNS = [
    "TYPE",
    "CIRCUIT",
    "NAME",
    "COMMENT",
    "QQ",
    "ZZ",
    "PBSB",
    "ID",
]

FIELD_COLUMNS = [
    "FIELD",
    "PART",
    "DATATYPE",
    "DIVIDER/VALUES",
    "UNIT",
    "COMMENT",
]

ROW_KIND_DATA = "DATA"

ROW_KIND_EMPTY = "EMPTY"

ROW_KIND_DEFAULTS = "DEFAULTS"

ROW_KIND_HEADER = "HEADER"

ROW_KIND_COMMENT = "COMMENT"

ROW_KIND_INCLUDE = "INCLUDE"
