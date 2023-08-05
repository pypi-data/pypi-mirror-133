# Copyright (c) cdr4eelz.
# Distributed under the terms of the Modified BSD License.

import json
from pathlib import Path

from .backend import SerialHubWidget, SerialIO
from .nbextension import _jupyter_nbextension_paths

from ._version import __version__

HERE = Path(__file__).parent.resolve()

with (HERE / "labextension" / "package.json").open() as fid:
    data = json.load(fid)

def _jupyter_labextension_paths():
    return [{
        "src": "labextension",
        "dest": data["name"]
    }]
