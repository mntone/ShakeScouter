# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

from .console import *
from .json import *
from .websocket import *

OUTPUT_PLUGINS_KEYLIST = {
	'console': 'ConsoleOutput',
	'json': 'JsonOutput',
	'websocket': 'WebSocketOutput',
}
