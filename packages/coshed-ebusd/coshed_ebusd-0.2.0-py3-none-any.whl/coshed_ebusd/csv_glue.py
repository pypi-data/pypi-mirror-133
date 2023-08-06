#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import logging

from coshed_ebusd.defaults import DELIMITER, QUOTECHAR, DIALECT
from coshed_ebusd.defaults import ROW_KIND_DATA
from coshed_ebusd.defaults import ROW_KIND_EMPTY
from coshed_ebusd.defaults import ROW_KIND_DEFAULTS
from coshed_ebusd.defaults import ROW_KIND_HEADER
from coshed_ebusd.defaults import ROW_KIND_COMMENT
from coshed_ebusd.defaults import ROW_KIND_INCLUDE

log = logging.getLogger(__name__)


def ebusd_csv_parser(csv_path, **kwargs):
    with open(csv_path, newline="") as csvfile:
        spamreader = csv.reader(
            csvfile, delimiter=DELIMITER, quotechar=QUOTECHAR
        )

        for idx, row in enumerate(spamreader):
            if len(row) == 0:
                log.debug(f"#{idx:4d} EMPTY")
                yield idx, ROW_KIND_EMPTY, row
                continue

            if row[0].startswith("*"):
                log.debug(f"#{idx:4d} DEFAULTS {row}")
                yield idx, ROW_KIND_DEFAULTS, row
                continue

            if row[0].startswith("#"):
                row_kind = ROW_KIND_COMMENT
                if idx == 0:
                    row_kind = ROW_KIND_HEADER
                yield idx, row_kind, row
                continue

            if row[0].startswith("!include"):
                log.debug(f"#{idx:4d} INCLUDE {row[1]}")
                yield idx, ROW_KIND_INCLUDE, row
                continue

            yield idx, ROW_KIND_DATA, row


def csv_write(rows, csv_path):
    with open(csv_path, "w", newline="") as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter=DELIMITER,
            quotechar=QUOTECHAR,
            quoting=csv.QUOTE_MINIMAL,
            dialect=DIALECT,
        )

        for row in rows:
            spamwriter.writerow(row)
