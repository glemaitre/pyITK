"""Base classes for the registration methods."""


class BaseRegistrator(object):

    def get_params(self):
        # it will allow to get the parameters of the different modules of the
        # registration pipeline.
        pass

    def set_params(self):
        # it will allow to set the parameters of the different modules of the
        # registration pipeline.
        pass


class RegistratorrMixin(object):

    def fit_transform(self, fixed_image, moving_image):
        return (self.fit(fixed_image, moving_image)
                    .transform(fixed_image, moving_image))
