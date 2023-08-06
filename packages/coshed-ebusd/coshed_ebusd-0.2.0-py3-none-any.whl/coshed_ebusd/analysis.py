#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import logging
import zlib
import re
import sys
import traceback

from coshed_ebusd.defaults import MESSAGE_COLUMNS, FIELD_COLUMNS
from coshed_ebusd.defaults import ROW_KIND_DATA
from coshed_ebusd.defaults import ROW_KIND_DEFAULTS
from coshed_ebusd.defaults import ROW_KIND_HEADER
from coshed_ebusd.csv_glue import ebusd_csv_parser


EXTENSIONS = (".csv",)


PATTERN_MESSAGE_DEFAULT = r"^\*(r|w|wi|ws)?$"
REGEX_MESSAGE_DEFAULT = re.compile(PATTERN_MESSAGE_DEFAULT)


def log_traceback(message, exception, uselog=None):
    """
    Use *uselog* Logger to log a Traceback of exception *exception*.

    Args:
        message(str): message to be logged before trace log items
        exception(Exception): exception to be logged
        uselog(logging.Logger, optional): logger instance override

    """
    if uselog is None:
        uselog = logging.getLogger(__name__)
    e_type, e_value, e_traceback = sys.exc_info()

    uselog.warning(message)
    uselog.error(exception)

    for line in traceback.format_exception(e_type, e_value, e_traceback):
        for part in line.strip().split("\n"):
            if part != "":
                uselog.warning(part)


def data_crc32(row):
    source_columns = ["TYPE", "CIRCUIT", "NAME", "QQ", "ZZ", "PBSB", "ID"]
    values = []

    for sc in source_columns:
        idx = MESSAGE_COLUMNS.index(sc)
        values.append(row[idx].encode("utf-8"))

    return "{:08X}".format(zlib.crc32("".encode("utf-8").join(values)))


def csv_analysis_header(csv_path, **kwargs):
    verbose = kwargs.get("verbose", 0)
    log = kwargs.get("use_log", logging.getLogger(__name__))

    if kwargs.get("top_path"):
        top_path = kwargs.get("top_path")
        prefix = f"{os.path.relpath(csv_path, top_path):50}"
    else:
        prefix = f"{csv_path:50}"
    expected_rows_len = None

    for idx, row_kind, row in ebusd_csv_parser(csv_path):
        if row_kind == ROW_KIND_HEADER:
            expected_rows_len = len(row)
            field_definitions = 0
            flaky = False
            additional_columns = row[len(MESSAGE_COLUMNS) :]

            if len(row) != len(MESSAGE_COLUMNS):
                if len(row) < len(MESSAGE_COLUMNS):
                    missing = len(MESSAGE_COLUMNS) - len(row)
                    log.warning(
                        f"{prefix} not enough header columns: {missing:3} missing!"
                    )
                    flaky = True
                else:
                    field_definitions = len(additional_columns) // len(
                        FIELD_COLUMNS
                    )
                    remainder = len(additional_columns) % len(FIELD_COLUMNS)

                    if remainder == 0:
                        log_meth = log.debug

                        if field_definitions != 1:
                            log_meth = log.info

                        if kwargs.get("verbose"):
                            log_meth = log.info

                        log_meth(
                            f"{prefix} {field_definitions:2} field definition(s). {expected_rows_len:3} column(s)."
                        )
                    else:
                        flaky = True
                        offset = field_definitions * len(FIELD_COLUMNS)
                        dangling_columns = additional_columns[offset:]
                        flaky_indicator = ""

                        if set(dangling_columns) == {""}:
                            flaky_indicator = " [All empty]"

                        log.warning(
                            f"{prefix} {field_definitions:2} field definition(s) + {remainder:3} addtional column(s){flaky_indicator}. {expected_rows_len:3} column(s)."
                        )

                if flaky or field_definitions != 1 or verbose > 2:
                    log.debug(f"{row}")
            else:
                log.info(f"{csv_path} valid header line.")

        if row_kind == ROW_KIND_DATA:
            if expected_rows_len is None:
                raise ValueError("No header line known?!")

            diff = abs(expected_rows_len - len(row))

            if len(row) < expected_rows_len:
                log.warning(
                    f"{prefix} line {idx+1:4} has only {len(row):3} column(s): {diff:2} missing!"
                )
            elif len(row) > expected_rows_len:
                log.warning(
                    f"{prefix} line {idx+1:4} has {len(row):3} column(s): {diff:2} too many!"
                )

    if verbose:
        log.info("")


def perform_analysis(top_path, extensions=None, func=None, **kwargs):
    log = kwargs.get("use_log", logging.getLogger(__name__))

    if extensions is None:
        extensions = EXTENSIONS

    if func is None:
        func = csv_analysis_header

    stats = dict(
        path=top_path,
        extensions=extensions,
        files=0,
        files_w_comments=0,
        files_ignored=0,
    )

    if not os.path.isdir(top_path):
        log.error(f"{top_path!r} does not appear to be a directory! Abort.")

        return stats

    log.info(f"Scanning {top_path} ...")
    for root, _, files in os.walk(top_path):
        for file_path in files:
            stats["files"] += 1
            abs_path = os.path.join(root, file_path)
            trunk, ext = os.path.splitext(file_path)
            mangled, comments = [], None

            if ext.lower() not in extensions:
                stats["files_ignored"] += 1
                continue

            if trunk.startswith("_"):
                stats["files_ignored"] += 1
                continue

            if trunk in ("broadcast", "memory", "general", "scan"):
                stats["files_ignored"] += 1
                continue

            if os.path.islink(abs_path):
                stats["files_ignored"] += 1
                continue

            rv = None
            try:
                rv = func(abs_path, top_path=top_path, **kwargs)
            except Exception as exc:
                log_traceback(f"Reading/parsing {abs_path}", exc, log)

            if rv is not None:
                mangled, comments, _ = rv

            if comments:
                stats["files_w_comments"] += 1
            #    csv_write(mangled, abs_path)

    return stats


def perform_i18n_analysis(top_path, extensions=None, func=None, **kwargs):
    log = kwargs.get("use_log", logging.getLogger(__name__))

    if extensions is None:
        extensions = EXTENSIONS

    names = dict()
    comments = dict()

    idx_NAME = MESSAGE_COLUMNS.index("NAME")
    comment_indices = set()

    for root, _, files in os.walk(top_path):
        for file_path in files:
            abs_path = os.path.join(root, file_path)
            trunk, ext = os.path.splitext(file_path)

            if ext.lower() not in extensions:
                continue

            if trunk.startswith("_"):
                continue

            if trunk in ("broadcast", "memory", "general", "scan"):
                continue

            if os.path.islink(abs_path):
                continue

            try:
                for idx, row_kind, row in ebusd_csv_parser(abs_path):
                    if row_kind == ROW_KIND_HEADER:
                        for column_idx, column in enumerate(row):
                            if "comment" in column.lower():
                                comment_indices.add(column_idx)

                    if row_kind == ROW_KIND_DATA:
                        name = row[idx_NAME]

                        try:
                            names[name] += 1
                        except KeyError:
                            names[name] = 1

                        for comment_idx in comment_indices:
                            try:
                                comment = row[comment_idx]
                                if comment:
                                    try:
                                        comments[name].add(comment)
                                    except KeyError:
                                        comments[name] = {comment}
                            except IndexError:
                                pass
            except Exception as exc:
                log_traceback(f"Reading/parsing {abs_path}", exc, log)

    for key, value in sorted(names.items(), key=lambda x: x[0].lower()):
        if value < 3:
            continue

        print(f"{key:40}: {value:4d}")
        key_comments = sorted(comments.get(key, []))
        if value > 1 and len(key_comments) > 1:
            print(f" comments: {key_comments}")
            print("")


def subfolders_analysis(extensions=None, func=None):
    stats_all = []

    for item in os.listdir():
        if item.startswith("."):
            continue

        if os.path.isdir(item) and not os.path.islink(item):
            stats_all.append(
                perform_analysis(item, extensions=extensions, func=func)
            )

    for stat in sorted(stats_all, key=lambda x: x["path"]):
        print(stat)
