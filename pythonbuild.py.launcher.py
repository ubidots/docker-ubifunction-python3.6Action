#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function
from main__ import main as main
from sys import stdin
from sys import stdout
from sys import stderr
from os import fdopen
import sys
import os
import json
import traceback
import warnings
import requests
import random
import requests
import time
import datetime
import math

from threading import Thread
import sentry_sdk
import queue

q = queue.Queue()


def parse_to_json(value):
    if isinstance(value, dict):
        return value
    try:
        return json.loads(value)
    except (SyntaxError, json.JSONDecodeError, TypeError):
        return {}


def worker():
    while True:
        __report_url, __sentry_url, __action_id, execution_time, timestamp = q.get()
        try:
            requests.post(
                __report_url,
                json={
                    "timestamp": timestamp,
                    "execution-time": execution_time,
                    "id": __action_id,
                },
            )
        except Exception as e:
            if __sentry_url is not None:
                sentry_sdk.init(dsn=__sentry_url)
                sentry_sdk.captureMessage(
                    "*UbiFunction Container Node:* \n{}".format(e)
                )
        finally:
            q.task_done()


t = Thread(target=worker)
t.daemon = True
t.start()

try:
    # if the directory 'virtualenv' is extracted out of a zip file
    path_to_virtualenv = os.path.abspath("./virtualenv")
    if os.path.isdir(path_to_virtualenv):
        # activate the virtualenv using activate_this.py contained in the virtualenv
        activate_this_file = path_to_virtualenv + "/bin/activate_this.py"
        if os.path.exists(activate_this_file):
            with open(activate_this_file) as f:
                code = compile(f.read(), activate_this_file, "exec")
                exec(code, dict(__file__=activate_this_file))
        else:
            sys.stderr.write(
                "Invalid virtualenv. Zip file does not include /virtualenv/bin/"
                + os.path.basename(activate_this_file)
                + "\n"
            )
            sys.exit(1)
except Exception:
    traceback.print_exc(file=sys.stderr, limit=0)
    sys.exit(1)

# now import the action as process input/output
warnings.filterwarnings("ignore")
warnings.resetwarnings()

# if there are some arguments exit immediately
if len(sys.argv) > 1:
    sys.stderr.flush()
    sys.stdout.flush()
    sys.exit(0)

env = os.environ
out = fdopen(3, "wb")

while True:
    line = stdin.readline()
    if not line:
        q.join()
        break
    args = json.loads(line)
    payload = {}
    for key in args:
        if key == "value":
            payload = args["value"]
        elif key.upper() in ["TRANSACTION_ID", "ACTIVATION_ID", "ACTION_NAME"]:
            env["__OW_%s" % key.upper()] = args[key]

    res = {}
    try:
        if payload.get("_ping") == "true":
            raise RuntimeError("Ping function")
        __action_id = os.getenv("__OW_ACTION_NAME", "").split("adapter-")[-1]
        __report_url = payload.pop("reportUrl", None)
        __sentry_url = payload.pop("sentryUrl", None)
        __environment = payload.pop("_environment", None)
        __auth_credentials = payload.pop("_auth_credentials", {})
        __parameters = payload.pop("_parameters", None)

        # Parse environment data and create each key as an environment variable
        parsed_data = parse_to_json(__environment)
        for key, value in parsed_data.items():
            env["__{key}".format(key=key)] = value

        # Create each key on auth_credentials as an environment variable
        parsed_data = parse_to_json(__auth_credentials)
        for key, value in parsed_data.items():
            env["AUTH_CREDENTIALS_{key}".format(key=key.upper())] = value

        # Parse _parameters data and sent to script as an extra key inside args
        parsed_data = parse_to_json(__parameters)
        if parsed_data:
            payload.update({"_parameters": parsed_data})

        init_time = time.time()
        res = main(payload)
    except RuntimeError:
        res = {"result": "pong"}
    except Exception as ex:
        print(traceback.format_exc(), file=stderr)
        res = {"error": str(ex)}

    # Reporter: Action name expected '/Ubidots_parsers/adapter-id'
    execution_time = math.ceil((time.time() - init_time) * 1000)
    timestamp = int(datetime.datetime.utcnow().timestamp() * 1000)
    q.put((__report_url, __sentry_url, __action_id, execution_time, timestamp))

    out.write(json.dumps(res, ensure_ascii=False).encode("utf-8"))
    out.write(b"\n")

    stdout.flush()
    stderr.flush()
    out.flush()
