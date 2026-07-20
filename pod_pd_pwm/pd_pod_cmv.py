####### Base class for PD-POD PWM low common mode voltage area
####### calculation. Other files only need to override vzs_calculate.
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from cbb import three_phase_3d as tp3d

class PdPodCmv(tp3d.ThreePhase3D):
    def __init__(self):
        super().__init__()
        length_modu = len(self.modulation_3d)
        length_wt   = len(self.wt)
        self.vzs_up_max   = np.zeros((length_modu, length_wt))
        self.vzs_up_min   = np.zeros((length_modu, length_wt))
        self.vzs_down_max = np.zeros((length_modu, length_wt))
        self.vzs_down_min = np.zeros((length_modu, length_wt))

    def vzs_calculate(self):
        """Override this method in subclasses to implement specific logic."""
        raise NotImplementedError(
            "Subclasses must implement vzs_calculate"
        )

    def data_porportion_calculate(self):
        data_3d_volume      = 0
        data_3d_up_volume   = 0
        data_3d_down_volume = 0
        up_volume   = 0
        down_volume = 0
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                if not np.isnan(self.vzs_up_max[i,j]) and not np.isnan(self.vzs_up_min[i,j]):
                    up_volume += self.vzs_up_max[i,j] - self.vzs_up_min[i,j]
                if not np.isnan(self.vzs_down_max[i,j]) and not np.isnan(self.vzs_down_min[i,j]):
                    down_volume += self.vzs_down_max[i,j] - self.vzs_down_min[i,j]
                data_3d_volume      += self.vz_max_3d[i,j] - self.vz_min_3d[i,j]
                data_3d_up_volume   += self.vz_max_3d[i,j] - self.vzs_division[i,j]
                data_3d_down_volume += self.vzs_division[i,j] - self.vz_min_3d[i,j]

        vzs_up_proportion       = (up_volume)          * 100 / data_3d_volume       if data_3d_volume       != 0 else 0
        vzs_down_proportion     = (down_volume)        * 100 / data_3d_volume       if data_3d_volume       != 0 else 0
        vzs_proportion          = (up_volume + down_volume) * 100 / data_3d_volume if data_3d_volume != 0 else 0
        vzs_in_up_proportion    = (up_volume)          * 100 / data_3d_up_volume    if data_3d_up_volume    != 0 else 0
        vzs_in_down_proportion  = (down_volume)        * 100 / data_3d_down_volume  if data_3d_down_volume  != 0 else 0
        return (vzs_up_proportion, vzs_down_proportion,
                vzs_proportion, vzs_in_up_proportion,
                vzs_in_down_proportion)

if __name__ == "__main__":
    print("This is a base class. Use a concrete subclass (e.g. pd2_cmv.Pd2_cmv) for testing.")
