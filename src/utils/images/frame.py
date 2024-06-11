# Copyright (C) 2024 mntone
# Licensed under the GPLv3 license.

import cv2 as cv
import numpy as np

from functools import reduce
from math import ceil, floor
from numpy.typing import NDArray

from utils.images.model import PartInfo, RectF
from utils.images.filters.filter import Filter

class Frame:
	__image: NDArray[np.uint8]

	def __init__(self, **kwargs) -> None:
		if 'raw' in kwargs:
			self.__image = kwargs['raw']
		elif 'filepath' in kwargs:
			image = cv.imread(kwargs['filepath'], cv.IMREAD_ANYCOLOR)
			if image is None:
				raise TypeError(f'Image is not found: {kwargs['filepath']}')
			if image.dtype != np.uint8:
				raise TypeError(f'Image type is not np.uint8')
			self.__image = image.astype(np.uint8)
		else:
			raise TypeError('At least the "raw" or "filepath" is required')

	@property
	def native(self) -> NDArray[np.uint8]:
		return self.__image

	def apply(self, partInfo: PartInfo) -> NDArray[np.uint8]:
		subimage = self.__subimage(partInfo['area'])
		filtered = Frame.__filter(subimage, partInfo['filters'])
		return filtered

	def filter(self, filters: list[Filter]) -> NDArray[np.uint8]:
		image = Frame.__filter(self.__image, filters)
		return image

	def subimage(self, rect: RectF) -> 'Frame':
		subimage = self.__subimage(rect)
		newFrame = Frame(raw=subimage)
		return newFrame

	def __subimage(self, rect: RectF) -> NDArray[np.uint8]:
		if rect['left'] < 0 or rect['left'] > 1:
			raise ValueError('"rect[\'left\']" must be between 0 and 1')
		if rect['top'] < 0 or rect['top'] > 1:
			raise ValueError('"rect[\'top\']" must be between 0 and 1')
		if rect['right'] < 0 or rect['right'] > 1:
			raise ValueError('"rect[\'right\']" must be between 0 and 1')
		if rect['bottom'] < 0 or rect['bottom'] > 1:
			raise ValueError('"rect[\'bottom\']" must be between 0 and 1')

		image = self.__image
		height, width = image.shape[:2]
		top = floor(rect['top'] * height)
		bottom = ceil(rect['bottom'] * height)
		left = floor(rect['left'] * width)
		right = ceil(rect['right'] * width)

		subimage = image[top:bottom, left:right]
		return subimage

	def update(self, raw: NDArray[np.uint8]):
		self.__image = raw

	@staticmethod
	def __filter(src: NDArray[np.uint8], filters: list[Filter]) -> NDArray[np.uint8]:
		dst = reduce(lambda i, f: f.apply(i), filters, src)
		return dst
