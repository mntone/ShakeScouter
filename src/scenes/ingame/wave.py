# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from typing import Any

from constants import Color, screen
from recognizers.digit import DigitReader
from scenes.base import *
from scenes.base import SceneContext
from utils.anomaly import CounterAnomalyDetector
from utils.images import errorMAE, Frame

# Correlation Param
ALIVE_THRESHOLD = 0.8 * 255

class WaveScene(Scene):
	MIN_ERROR = 0.1

	def __init__(self, reader: DigitReader) -> None:
		self.__reader           = reader
		self.__waveTemplate     = Scene.loadTemplate('wave')
		self.__waveExTemplate   = Scene.loadTemplate('wave_ex')
		self.__unstableTemplate = Scene.loadTemplate('unstable')

	def setup(self) -> Any:
		data = {
			'end': -1,
			'wave': 0,
			'color': None,
			'quota': -1,
			'detector': CounterAnomalyDetector(),
		}
		return data

	def reset(self, data: Any) -> None:
		data['end']   = -1
		data['wave']  = 0
		data['color'] = None
		data['quota'] = -1
		data['detector'].reset()

	async def __detectAnomalousCount(self, context: SceneContext, data: Any, count: Optional[int]) -> None:
		if count is not None:
			if not data['detector'].isAnomalous(count, context.timestamp):
				# Calc estimated end timestamp
				data['end'] = context.timestamp + (100 - count)
			else:
				await context.sendImmediately(SceneEvent.DEV_WARN, {
					'description': f'Anomalous value detected: {count}',
				})

	def __analysisCount(self, frame: Frame) -> Optional[int]:
		# Read "count"
		timerImage = frame.apply(screen.TIMER_PART)
		timerInt = self.__reader.read(timerImage)

		return timerInt

	def __analysisPlayerStatus(self, data: Any, frame: Frame):
		# Get player subimage
		playerImage = WaveScene.__applyPlayerPostFilter(frame.apply(screen.PLAYERS_PART))

		# Get nearest hue from image
		if data['color'] is None:
			data['color'] = WaveScene.__findNearestColor(playerImage)
		color: Color = data['color']

		# Get player status
		maskFilter = screen.getPlayerFilter(color.hueA)
		playerMask = Frame(raw=playerImage).filter(maskFilter)
		playerStatus = list(map(lambda i: {
			'alive': WaveScene.__getAliveStatus(playerMask, i)
		}, range(4)))

		return playerStatus

	def __analysisUnstable(self, frame: Frame):
		# Get unstable status
		unstableImage = frame.apply(screen.UNSTABLE_PART)
		unstableError = errorMAE(unstableImage, self.__unstableTemplate)
		unstableStatus = bool(unstableError <= WaveScene.MIN_ERROR)

		return unstableStatus

	async def __analysisXtrawave(self, context: SceneContext, data: Any, frame: Frame, waveImage: Optional[NDArray[np.uint8]] = None) -> SceneStatus:
		if context.timestamp >= data['end']:
			if waveImage is None:
				waveImage = frame.apply(screen.WAVE_PART)
			waveExError = errorMAE(waveImage, self.__waveExTemplate)

			if waveExError > WaveScene.MIN_ERROR:
				return SceneStatus.FALSE
			else:
				data['wave']  = 'extra'
				data['quota'] = -1

		# Read each part
		count    = self.__analysisCount(frame)
		players  = self.__analysisPlayerStatus(data, frame)
		unstable = self.__analysisUnstable(frame)

		# Detect anomalous count
		await self.__detectAnomalousCount(context, data, count)

		# Send message
		message = {
			'color': data['color'].value.name,
			'wave': 'extra',
			'count': count,
			'players': players,
			'unstable': unstable,
		}
		await context.send(SceneEvent.GAME_UPDATE, message)

		return SceneStatus.CONTINUE

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		# In "Xtrawave"
		if data['wave'] == 'extra':
			result = await self.__analysisXtrawave(context, data, frame)
			return result

		if context.timestamp >= data['end']:
			# Detect "Wave"
			waveImage = frame.apply(screen.WAVE_PART)
			waveTextImage = screen.removeNumberAreaFromWaveImage(waveImage)
			waveError = errorMAE(waveTextImage, self.__waveTemplate)

			if waveError > WaveScene.MIN_ERROR:
				data['quota'] = -1

				# Check "Xtrawave"
				result = await self.__analysisXtrawave(context, data, frame, waveImage)
				return result

			# Read "wave"
			waveNumberImage = waveImage[:, self.__waveTemplate.shape[1]:]
			waveNumberInt = self.__reader.read(waveNumberImage)
			if waveNumberInt is not None:
				data['wave'] = waveNumberInt

			# Read "quota"
			quotaImage = frame.apply(screen.QUOTA_PART)
			quotaInt = self.__reader.read(quotaImage)
			if quotaInt is not None:
				data['quota'] = quotaInt

		# Read "amount"
		amountImage = frame.apply(screen.AMOUNT_PART)
		amountInt = self.__reader.read(amountImage)

		# Read each part
		count    = self.__analysisCount(frame)
		players  = self.__analysisPlayerStatus(data, frame)
		unstable = self.__analysisUnstable(frame)

		# Detect anomalous count
		await self.__detectAnomalousCount(context, data, count)

		# Send message if any of count or amount is not None
		if any([count, amountInt]):
			message = {
				'color': data['color'].value.name,
				'wave': data['wave'],
				'count': count,
				'amount': amountInt,
				'quota': data['quota'],
				'players': players,
				'unstable': unstable,
			}
			await context.send(SceneEvent.GAME_UPDATE, message)

		return SceneStatus.CONTINUE

	@staticmethod
	def __applyPlayerPostFilter(image: np.ndarray) -> np.ndarray:
		# Remove base background if hue > 127
		# TODO: Improve removing algorithm
		backgroundHue, _, value = image[0, 0]
		if value > 127:
			mask = cv.inRange(
				image,
				np.array([backgroundHue - 2, 127, 204]),
				np.array([backgroundHue + 2, 255, 255]),
			)
			image = cv.bitwise_and(image, image, mask=cv.bitwise_not(mask))

		return image

	@staticmethod
	def __findNearestColor(image: np.ndarray) -> Color:
		# Calc hue histgram
		hueHist = cv.calcHist([image], [0], None, [180], [0, 180])

		# Get dominant hue
		dominantHueIndex = np.argmax(hueHist)

		# Calc hue distance
		hueDistances = np.abs(Color.hues() - dominantHueIndex)

		# Get nearest color index
		nearestIndex = np.argmin(hueDistances)

		# Get nearest color
		nearestColor = Color.all()[nearestIndex]

		return nearestColor

	@staticmethod
	def __getAliveStatus(image: np.ndarray, playerIndex: int) -> bool:
		# Get each player image
		left = playerIndex * 72
		right = min(left + 78, image.shape[1])
		subimage = image[:, left:right]

		# Count color pixels
		pixelCount = cv.countNonZero(subimage)

		return pixelCount > 0
