# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from typing import Any

from constants import Color, screen
from recognizers.digit import DigitReader
from scenes.base import *
from utils.images import calcSimilarity, Frame

# Correlation Param
WAVE_THRESHOLD     = 0.9
UNSTABLE_THRESHOLD = 0.9

ALIVE_THRESHOLD = 0.8 * 255

class WaveScene(Scene):
	def __init__(self, reader: DigitReader) -> None:
		self.__reader           = reader
		self.__waveTemplate     = Scene.loadTemplate('wave')
		self.__waveExTemplate   = Scene.loadTemplate('wave_ex')
		self.__unstableTemplate = Scene.loadTemplate('unstable')

	def setup(self) -> Any:
		data = {
			'color':  None,
			'wave':   -1,
			'count':  100,
			'amount': -1,
			'quota':  -1,
			'players': [
				dict(alive=True),
				dict(alive=True),
				dict(alive=True),
				dict(alive=True),
			],
			'unstable': False,
		}
		return data

	async def analysis(self, context: SceneContext, data: Any, frame: Frame) -> SceneStatus:
		# Detect "Wave"
		waveImage = frame.apply(screen.WAVE_PART)
		waveSim = calcSimilarity(waveImage, self.__waveTemplate)

		if waveSim < WAVE_THRESHOLD:
			waveExSim = calcSimilarity(waveImage, self.__waveExTemplate)

			if waveExSim < WAVE_THRESHOLD:
				data['wave'] = -1
				data['quota'] = -1
				return SceneStatus.FALSE

			else:
				if data['wave'] != 'extra':
					# Set "extra" wave
					data['wave'] = 'extra'
					data['amount'] = -1
					data['quota'] = -1

		else:
			# Read "wave"
			waveNumberImage = waveImage[:, self.__waveTemplate.shape[1]:]
			waveNumberInt = self.__reader.read(waveNumberImage)
			if waveNumberInt is not None:
				data['wave'] = waveNumberInt

		# Read "count"
		timerImage = frame.apply(screen.TIMER_PART)
		timerInt = self.__reader.read(timerImage)
		if timerInt is not None:
			data['count'] = timerInt

		if data['wave'] != 'extra':
			# Read "amount"
			amountImage = frame.apply(screen.AMOUNT_PART)
			amountInt = self.__reader.read(amountImage)
			if amountInt is not None:
				data['amount'] = amountInt

			if data['quota'] == -1:
				# Read "quota"
				quotaImage = frame.apply(screen.QUOTA_PART)
				quotaInt = self.__reader.read(quotaImage)
				if quotaInt is not None:
					data['quota'] = quotaInt

		# Get player subimage
		playerImage = WaveScene.__applyPlayerPostFilter(frame.apply(screen.PLAYERS_PART))

		# Get nearest hue from image
		if data['color'] is None:
			data['color'] = WaveScene.__findNearestColor(playerImage)
		color: Color = data['color']

		# Get player status
		maskFilter = screen.getPlayerFilter(color.hueA)
		playerMask = Frame(raw=playerImage).filter(maskFilter)
		for i in range(4):
			data['players'][i]['alive'] = WaveScene.__getAliveStatus(playerMask, i)

		# Get unstable status
		unstableImage = frame.apply(screen.UNSTABLE_PART)
		unstableSim = calcSimilarity(unstableImage, self.__unstableTemplate)
		data['unstable'] = bool(unstableSim >= UNSTABLE_THRESHOLD)

		# Send message
		transformedData = WaveScene.__transformData(data)
		await context.send(SceneEvent.GAME_UPDATE, transformedData)

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

	@staticmethod
	def __transformData(data: Any) -> dict[str, Any]:
		ret = {}
		for key, value in data.items():
			if key == 'color':
				ret[key] = value.value.name
			else:
				ret[key] = value
		return ret
