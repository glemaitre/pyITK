"""Gradient-based optimizer"""

import itk


class RegularStepGradientDescentOptimizer(object):

    def __init__(self, learning_rate=4.0, min_step_length=0.001,
                 relaxation_factor=0.5, max_iter=200):
        self.learning_rate = learning_rate
        self.min_step_length = min_step_length
        self.relaxation_factor = relaxation_factor
        self.max_iter = max_iter

    def __call__(self):
        self.optimizer_ = itk.RegularStepGradientDescentOptimizerv4[
            itk.D].New()
        self.optimizer_.SetLearningRate(self.learning_rate)
        self.optimizer_.SetMinimumStepLength(self.min_step_length)
        self.optimizer_.SetRelaxationFactor(self.relaxation_factor)
        self.optimizer_.SetNumberOfIterations(self.max_iter)
        return self.optimizer_
