"""Rigid transformation"""

import itk

import numpy as np

from ..utils.types import NPY_ITK_DYTPES


class TranslationTransform(object):

    def __init__(self, image_ndim, params_dtype, init=None):
        self.image_ndim = image_ndim
        self.params_dtype = np.dtype(params_dtype)
        self.init = init

    def __call__(self):
        self.transform_ = itk.TranslationTransform[
            NPY_ITK_DYTPES[self.params_dtype], self.image_ndim].New()
        if self.init is None:
            self.transform_.SetIdentity()
        else:
            self.transform_.SetParameters(self.init)
        return self.transform_

    def get_params(self):
        return self.__call__().GetParameters()

    def set_params(self, params):
        self.init = params
