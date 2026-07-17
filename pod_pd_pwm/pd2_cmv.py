####### This file is aimed at plotting the PD-I PWM's low
####### common mode voltage area and its proportion
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from cbb import three_phase_3d as tp3d

class Pd2_cmv(tp3d.ThreePhase3D):
    def __init__(self):
        super().__init__()
        length_modu = len(self.modulation_3d)
        length_wt   = len(self.wt)
        self.vzs_up_low_cmv_max = np.zeros((length_modu, length_wt))
        self.vzs_up_low_cmv_min = np.zeros((length_modu, length_wt))
        self.vzs_down_low_cmv_max = np.zeros((length_modu, length_wt))
        self.vzs_down_low_cmv_min = np.zeros((length_modu, length_wt))

    def vzs_low_cmv_calculate(self):
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                if self.one_plus_min[i,j] <= self.v_mid[i,j] and self.vz_max_3d[i,j] >= np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j]):
                    self.vzs_low_cmv_max[i,j] = self.vz_max_3d[i,j]
                    self.vzs_low_cmv_min[i,j] = np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])
                else:
                    self.vzs_low_cmv_max[i,j] = np.nan
                    self.vzs_low_cmv_min[i,j] = np.nan

    def data_porportion_calculate(self):
        self.vzs_low_cmv_proportion = 0
        data_3d_volume = 0
        low_cmv_volume = 0
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                if not np.isnan(self.vzs_low_cmv_max[i,j]) and not np.isnan(self.vzs_low_cmv_min[i,j]):
                    low_cmv_volume += self.vzs_low_cmv_max[i,j] - self.vzs_low_cmv_min[i,j]
                data_3d_volume += self.vz_max_3d[i,j] - self.vz_min_3d[i,j]

        self.vzs_low_cmv_proportion = low_cmv_volume * 100 / data_3d_volume if data_3d_volume != 0 else 0
        return  self.vzs_low_cmv_proportion

if __name__ == "__main__":
    test_instance = Pd2_cmv()
    test_instance.data_3d_calculate()
    test_instance.vzs_low_cmv_calculate()
    #test_instance.data_3d_plot(test_instance.vzs_low_cmv_max, test_instance.vzs_low_cmv_min)
    data_3d_volume = test_instance.data_porportion_calculate()
    print(f"{data_3d_volume:.2f}%")

