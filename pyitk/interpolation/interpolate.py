"""Interpolate methods"""

import itk

import numpy as np

from ..utils.types import NPY_ITK_DYTPES


class LinearInterpolate(object):

    def __init__(self, image_dtype, image_ndim, coord_dtype):
        self.image_dtype = np.dtype(image_dtype)
        self.image_ndim = image_ndim
        self.coord_dtype = np.dtype(coord_dtype)

    def __call__(self):
        image_type = itk.Image[NPY_ITK_DYTPES[self.image_dtype],
                               self.image_ndim]
        self.interpolator_ = itk.LinearInterpolateImageFunction[
            image_type, NPY_ITK_DYTPES[self.coord_dtype]].New()
        return self.interpolator_
