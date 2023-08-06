#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Web app skeleton
"""
import os
import logging
import re
from urllib.parse import urlparse
import hashlib

from flask import Flask, request, make_response, abort
from flask import send_from_directory
from coshed_flask.tools import wolfication
import requests

from coshed_ebusd.defaults import USER_AGENT
from coshed_ebusd.defaults import CONFIGURATION_SOURCE_URL
from coshed_ebusd.defaults import CONFIGURATION_SOURCE_LOCAL
from coshed_ebusd.defaults import CFG_LOCAL_EXTENSIONS
from coshed_ebusd.defaults import CFG_LOCAL_ENABLED

APP_NAME = "ebusd_updates"

#: flask application instance
app = wolfication(Flask(__name__), app_name=APP_NAME)


PATTERN_LIST_FILES = r"^(broadcast|memory|_templates|scan|general)\.csv$"
REGEX_LIST_FILES = re.compile(PATTERN_LIST_FILES)


def _local_dispatch(folder=None):
    parsed = urlparse(request.url)
    local_path = os.path.join(CONFIGURATION_SOURCE_LOCAL, parsed.path[1:])
    content_type = "text/comma-separated-values;charset=UTF-8"
    content_type = "text/csv;charset=utf-8"
    content_type = "text/plain;charset=utf-8"
    existing, existing_folder = False, False
    local_items = set()

    try:
        existing = os.path.exists(local_path)
    except Exception:
        pass

    try:
        existing_folder = os.path.isdir(local_path)
    except Exception:
        pass

    if not request.args:
        if existing and not existing_folder:
            _, ext = os.path.splitext(local_path)

            if not ext.lower() in CFG_LOCAL_EXTENSIONS:
                abort(404)

            app.logger.info(f"SERVE LOCAL {local_path}")

            return send_from_directory(
                CONFIGURATION_SOURCE_LOCAL,
                parsed.path[1:],
                mimetype=content_type,
            )

        if existing_folder:
            local_items = set(
                list(get_file_list(local_path, REGEX_LIST_FILES))
            )

    else:
        regex = None

        if request.args.get("a"):
            prefix = request.args.get("a")

            if prefix == "-":
                regex = REGEX_LIST_FILES
            else:
                regex = re.compile(
                    r"^" + re.escape(prefix) + r"\." + r".*?.csv$"
                )

        if existing and not existing_folder:
            abort(404)

        local_items = set(list(get_file_list(local_path, regex)))

    if local_items:
        app.logger.info("RESPONDING WITH")

        for item in sorted(local_items):
            app.logger.info(f" * {item}")

        output = make_response("\n".encode("utf-8").join(local_items))
        output.headers["Content-type"] = content_type

        return output

    raise KeyError()


@app.route("/", methods=["GET"])
@app.route("/<path:folder>", methods=["GET"])
def root_handler_proxy(folder=None):
    if CFG_LOCAL_ENABLED:
        try:
            return _local_dispatch(folder=folder)
        except KeyError:
            pass

    request_headers = {"user-agent": USER_AGENT}
    response_headers = dict()
    content_hash_cookie = hashlib.sha1()
    parsed = urlparse(request.url)

    the_url = f"{CONFIGURATION_SOURCE_URL}{parsed.path}"
    if parsed.query:
        the_url += f"?{parsed.query}"

    app.logger.debug(f"URL={request.url}")
    app.logger.debug(f" -> {the_url}")
    app.logger.debug(f" PATH: {parsed.path}")

    if parsed.query:
        app.logger.info(f" QUERY: {parsed.query}")

    local_path = os.path.join(CONFIGURATION_SOURCE_LOCAL, parsed.path[1:])

    try:
        response = requests.get(the_url, headers=request_headers)
    except Exception as exc:
        app.logger.error(f"Could not fetch {the_url}: {exc}")
        abort(504)

    content_hash_cookie.update(response.text.encode("utf-8"))
    output = make_response(response.text)

    response_headers["X-SHA1"] = content_hash_cookie.hexdigest()
    if not parsed.query:
        response_headers["X-LOCAL-PATH"] = local_path

        if os.path.exists(local_path):
            local_content_hash_cookie = hashlib.sha1()
            with open(local_path, "r") as src:
                local_content_hash_cookie.update(src.read().encode("utf-8"))
            response_headers[
                "X-LOCAL-SHA1"
            ] = local_content_hash_cookie.hexdigest()
            same_same = (
                local_content_hash_cookie.hexdigest()
                == content_hash_cookie.hexdigest()
            )
            app.logger.info(f" ==> {local_path} SAME={same_same}")
    else:
        parsed_contents = response.text.encode("utf-8").split(
            "\n".encode("utf-8")
        )
        response_items = set([x for x in parsed_contents if x])

        for item in sorted(response_items):
            app.logger.info(f" + {item}")

        regex = None

        if request.args.get("a"):
            prefix = request.args.get("a")
            if prefix == "-":
                regex = REGEX_LIST_FILES
            else:
                regex = re.compile(
                    r"^" + re.escape(prefix) + r"\." + r".*?.csv$"
                )

        local_items = set(list(get_file_list(local_path, regex)))

        for item in sorted(local_items):
            app.logger.info(f" * {item}")

        app.logger.info(
            " SIMILAR?! {!r}".format(response_items == local_items)
        )

    output.headers = response_headers

    return output


def get_file_list(path, regex=None):
    if os.path.isdir(path):
        for item in os.listdir(path):
            abs_path = os.path.join(path, item)

            if os.path.isdir(abs_path):
                continue

            if not item.startswith("_") and regex:
                matcher = regex.match(item)
                if not matcher:
                    continue

            yield item.encode("utf-8")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    #: logger instance
    LOG = logging.getLogger(APP_NAME)

    DEBUG_FLAG = True

    port = int("31329")
    bind_address = "0.0.0.0"

    LOG.info(f"CFG_LOCAL_ENABLED={CFG_LOCAL_ENABLED}")
    LOG.info(f"CONFIGURATION_SOURCE_LOCAL={CONFIGURATION_SOURCE_LOCAL}")
    app.run(host=bind_address, port=port, debug=DEBUG_FLAG)
