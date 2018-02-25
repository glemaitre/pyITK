"""Define correspondences between numpy and itk dtype"""

import itk
import numpy as np


NPY_ITK_DYTPES = {np.dtype(np.float64): itk.D,
                  np.dtype(np.float32): itk.F,
                  np.dtype(np.float128): itk.LD,
                  np.dtype(np.uint8): itk.UC,
                  np.dtype(np.uint16): itk.US,
                  np.dtype(np.uint32): itk.UI,
                  np.dtype(np.uint64): itk.UL,
                  np.dtype(np.int8): itk.SC,
                  np.dtype(np.int16): itk.SS,
                  np.dtype(np.int32): itk.SI,
                  np.dtype(np.int64): itk.SL,
                  np.dtype(bool): itk.B}
