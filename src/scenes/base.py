# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from abc import abstractmethod
from enum import Enum
from typing import Any, Optional

from constants import env
from utils.images import Frame

class SceneEvent(Enum):
	MATCHMAKING = 'matchmaking'
	GAME_STAGE  = 'game_stage'
	GAME_KING   = 'game_king'
	GAME_UPDATE = 'game_update'
	GAME_RESULT = 'game_result'
	GAME_ERROR  = 'game_error'

class SceneStatus(Enum):
	FALSE = 0
	DONE = 1
	CONTINUE = 2

class SceneContext:
	@abstractmethod
	async def sendImmediately(self, event: SceneEvent, message: Optional[dict[str, Any]] = None) -> None:
		raise NotImplementedError()

	@abstractmethod
	async def send(self, event: SceneEvent, message: dict[str, Any]) -> None:
		raise NotImplementedError()

class Scene:
	def setup(self) -> Any:
		return None

	def reset(self, data: Any):
		pass

	@abstractmethod
	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		raise NotImplementedError()

	@staticmethod
	def loadTemplate(templateName: str) -> np.ndarray:
		tmpPath = env.TEMPLATE_PATH.format(templateName)
		tmpImage = cv.imread(tmpPath, cv.IMREAD_GRAYSCALE)
		return tmpImage
