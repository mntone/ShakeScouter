# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from utils.images.filters.filter import Filter

class InRange(Filter):
	__lower: np.ndarray
	__upper: np.ndarray

	def __init__(
		self,
		lower: np.ndarray,
		upper: np.ndarray,
	) -> None:
		self.__lower = lower
		self.__upper = upper

	def apply(self, image: np.ndarray) -> np.ndarray:
		# Make mask
		mask = cv.inRange(image, self.__lower, self.__upper)

		return mask
