####### This file is aimed at plotting the PD-I PWM's low
####### common mode voltage area and its proportion
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from pod_pd_pwm.pd_pod_cmv import PdPodCmv


class Pd1_cmv(PdPodCmv):
    def vzs_calculate(self):
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                ### pd1's vzs_max is equivalent to other files' vzs_down_max
                if self.one_plus_min[i,j] <= self.v_mid[i,j] and self.vz_max_3d[i,j] >= np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j]):
                    self.vzs_down_max[i,j] = self.vz_max_3d[i,j]
                    self.vzs_down_min[i,j] = np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])
                else:
                    self.vzs_down_max[i,j] = np.nan
                    self.vzs_down_min[i,j] = np.nan

                ### up region is not used by pd1 — set to vz_max_3d so up volume = 0
                self.vzs_up_max[i,j] = self.vz_max_3d[i,j]
                self.vzs_up_min[i,j] = self.vz_max_3d[i,j]

if __name__ == "__main__":
    test_instance = Pd1_cmv()
    test_instance.data_3d_calculate()
    test_instance.vzs_calculate()
    #test_instance.data_3d_plot(test_instance.vzs_max, test_instance.vzs_min)
    vzs_up_proportion, vzs_down_proportion, vzs_proportion = test_instance.data_porportion_calculate()[:3]
    print(f"Low Common Mode Voltage in Total Area (Vzs > -Vmid): {vzs_up_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Total Area (Vzs < -Vmid): {vzs_down_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Total Area: {vzs_proportion:.2f}%")
