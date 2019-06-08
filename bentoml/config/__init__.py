# Copyright 2019 Atalaya Tech, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import logging

from bentoml.utils import Path
from bentoml.exceptions import BentoMLConfigException
from bentoml.config.configparser import BentoConfigParser

logger = logging.getLogger(__name__)


def expand_env_var(env_var):
    """Expands potentially nested env var by repeatedly applying `expandvars` and
    `expanduser` until interpolation stops having any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        else:
            env_var = interpolated


BENTOML_HOME = expand_env_var(os.environ.get("BENTOML_HOME", "~/bentoml"))
try:
    Path(BENTOML_HOME).mkdir(exist_ok=True)
except OSError as err:
    raise BentoMLConfigException(
        "Error creating bentoml home dir '{}': {}".format(BENTOML_HOME, err.strerror)
    )

# Default bentoml config comes with the library bentoml/config/default_bentoml.cfg
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "default_bentoml.cfg")
with open(DEFAULT_CONFIG_FILE, "rb") as f:
    DEFAULT_CONFIG = f.read().decode("utf-8")

if "BENTML_CONFIG" in os.environ:
    # User local config file for customizing bentoml
    BENTOML_CONFIG_FILE = expand_env_var(os.environ.get("BENTML_CONFIG"))
else:
    BENTOML_CONFIG_FILE = os.path.join(BENTOML_HOME, "bentoml.cfg")
    if not os.path.isfile(BENTOML_CONFIG_FILE):
        logger.info("Creating new Bentoml config file: %s", BENTOML_CONFIG_FILE)
        with open(BENTOML_CONFIG_FILE, "w") as f:
            f.write(DEFAULT_CONFIG)

config = BentoConfigParser(default_config=DEFAULT_CONFIG)
config.read(BENTOML_CONFIG_FILE)