"""Implements a family of rigid registration"""

import itk
import SimpleITK as sitk

import numpy as np

from pydicom import dcmread

from .base import BaseRegistrator
from .base import RegistratorrMixin

from ..optimization import RegularStepGradientDescentOptimizer
from ..metric import MeanSquaresMetric
from ..transformation import TranslationTransform

from ..utils.types import NPY_ITK_DYTPES


class RigidRegistrator(BaseRegistrator, RegistratorrMixin):

    def __init__(self, interpolator=None, loss=None, transformer=None,
                 solver=None, n_levels_resolution=1, smooth_sigma_levels=[0],
                 shrink_factors_levels=[1]):
        self.interpolator = interpolator
        self.loss = loss
        self.transform = transformer
        self.solver = solver
        self.n_levels_resolution = n_levels_resolution
        self.smooth_sigma_levels = smooth_sigma_levels
        self.shrink_factors_levels = shrink_factors_levels

    def check_inputs(self, fixed_image, moving_image):
        if fixed_image.dtype != moving_image.dtype:
            raise ValueError("The data type of the input images are different."
                             "Got fixed_image: {} - moving_image: {}".format(
                                 fixed_image.dtype, moving_image.dtype))
        else:
            self.image_dtype_ = fixed_image.dtype

        if fixed_image.ndim != moving_image.ndim:
            # FIXME: better error message
            raise ValueError("Not the same number of dimensions.")
        else:
            self.image_ndim_ = fixed_image.ndim

    def fit(self, fixed_image_filename, moving_image_filename):

        # Trick to make it works for now
        fixed_image = dcmread(fixed_image_filename).pixel_array.astype(np.float32)
        moving_image = dcmread(moving_image_filename).pixel_array.astype(np.float32)
        self.check_inputs(fixed_image, moving_image)

        FixedImageType = itk.Image[NPY_ITK_DYTPES[np.dtype(self.image_dtype_)],
                                   self.image_ndim_]
        fixedImageReader = itk.ImageFileReader[FixedImageType].New()
        fixedImageReader.SetFileName(fixed_image_filename)

        MovingImageType = itk.Image[NPY_ITK_DYTPES[np.dtype(self.image_dtype_)],
                                    self.image_ndim_]
        movingImageReader = itk.ImageFileReader[MovingImageType].New()
        movingImageReader.SetFileName(moving_image_filename)

        if self.loss is None:
            self.loss = MeanSquaresMetric(self.image_dtype_,
                                          self.image_ndim_,
                                          self.interpolator)
        if self.transform is None:
            self.transform = TranslationTransform(self.image_ndim_,
                                                  np.float64)
            self.moving_transform = TranslationTransform(self.image_ndim_,
                                                         np.float64)
            self.fixed_transform = TranslationTransform(self.image_ndim_,
                                                        np.float64)
        if self.solver is None:
            self.solver = RegularStepGradientDescentOptimizer()

        image_type = itk.Image[NPY_ITK_DYTPES[self.image_dtype_],
                               self.image_ndim_]
        self.registration = itk.ImageRegistrationMethodv4[
            image_type, image_type].New()

        img1 = sitk.GetImageFromArray(fixed_image)
        img2 = sitk.GetImageFromArray(moving_image)
        self.registration.SetFixedImage(img1.GetITKBase().Update())
        self.registration.SetMovingImage(img2.GetITKBase().Update())

        self.registration.SetMetric(self.loss())
        self.registration.SetOptimizer(self.solver())
        self.registration.SetInitialTransform(self.transform())

        init_params_moving = self.moving_transform.get_params()
        for idx in range(len(init_params_moving)):
            init_params_moving[idx] = 0
        self.fixed_transform.set_params(init_params_moving)
        self.registration.SetMovingInitialTransform(self.moving_transform())
        self.registration.SetFixedInitialTransform(self.fixed_transform())

        self.registration.SetNumberOfLevels(self.n_levels_resolution)
        self.registration.SetSmoothingSigmasPerLevel(self.smooth_sigma_levels)
        self.registration.SetShrinkFactorsPerLevel(self.shrink_factors_levels)

        self.registration.Update()

        transform = self.registration.GetTransform()

        finalParameters = transform.GetParameters()
        TranslationAlongX = finalParameters.GetElement(0)
        TranslationAlongY = finalParameters.GetElement(1)

        numberOfIterations = self.solver.optimizer_.GetCurrentIteration()

        bestValue = self.solver.optimizer_.GetValue()

        print("Result = ")
        print(" Translation X = " + str(TranslationAlongX))
        print(" Translation Y = " + str(TranslationAlongY))
        print(" Iterations    = " + str(numberOfIterations))
        print(" Metric value  = " + str(bestValue))

        return self

    def transform(self, fixed_image, moving_image):
        pass
        # return [param for param in transform.GetParameters()]
