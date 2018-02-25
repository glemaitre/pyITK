"""Similarity metrics"""

import itk

import numpy as np

from ..interpolation import LinearInterpolate
from ..utils.types import NPY_ITK_DYTPES


class MeanSquaresMetric(object):

    def __init__(self, image_dtype, image_ndim, interpolator=None):
        self.image_dtype = np.dtype(image_dtype)
        self.image_ndim = image_ndim
        self.interpolator = interpolator

    def __call__(self):
        image_type = itk.Image[NPY_ITK_DYTPES[self.image_dtype],
                               self.image_ndim]
        if self.interpolator is None:
            fixed_interpolator = LinearInterpolate(self.image_dtype,
                                                   self.image_ndim,
                                                   np.float64)
            moving_interpolator = LinearInterpolate(self.image_dtype,
                                                    self.image_ndim,
                                                    np.float64)
        self.metric_ = itk.MeanSquaresImageToImageMetricv4[image_type,
                                                           image_type].New()
        self.metric_.SetFixedInterpolator(fixed_interpolator())
        self.metric_.SetMovingInterpolator(moving_interpolator())
        return self.metric_
