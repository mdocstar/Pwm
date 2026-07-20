####### This file is aimed at plotting the POD-II PWM's
####### common mode voltage area and its proportion
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from pod_pd_pwm.pd_pod_cmv import PdPodCmv


class Pod2_cmv(PdPodCmv):
    def vzs_calculate(self):
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                up_limit  = self.v_max[i,j] * 0.5
                low_limit = np.minimum(-self.v_mid[i,j],-1 + self.v_max[i,j] )

                ### set low common mode voltage area when vzs > -v_mid
                if (-self.v_mid[i,j] <= up_limit and
                    np.minimum(up_limit, self.vz_max_3d[i,j]) >= np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])):
                    self.vzs_up_max[i,j] = np.minimum(up_limit, self.vz_max_3d[i,j])
                    self.vzs_up_min[i,j] = np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])
                else:
                    self.vzs_up_max[i,j] = np.nan
                    self.vzs_up_min[i,j] = np.nan

                ### set low common mode voltage area when vzs < -v_mid
                if (self.v_min[i,j] * 0.5 <= low_limit and
                    np.minimum(low_limit, self.vz_max_3d[i,j]) >= np.maximum(self.v_min[i,j] * 0.5, self.vz_min_3d[i,j])):
                    self.vzs_down_max[i,j] = np.minimum(low_limit, self.vz_max_3d[i,j])
                    self.vzs_down_min[i,j] = np.maximum(self.v_min[i,j] * 0.5, self.vz_min_3d[i,j])
                else:
                    self.vzs_down_max[i,j] = np.nan
                    self.vzs_down_min[i,j] = np.nan

if __name__ == "__main__":
    test_instance = Pod2_cmv()
    test_instance.data_3d_calculate()
    test_instance.vzs_calculate()
    #test_instance.data_3d_plot(test_instance.vzs_max, test_instance.vzs_min)
    vzs_up_proportion, vzs_down_proportion, vzs_proportion, vzs_in_up_proportion, vzs_in_down_proportion = test_instance.data_porportion_calculate()
    print(f"Low Common Mode Voltage in Total Area (Vzs > -Vmid): {vzs_up_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Total Area (Vzs < -Vmid): {vzs_down_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Total Area: {vzs_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Upper Area: {vzs_in_up_proportion:.2f}%")
    print(f"Low Common Mode Voltage in Lower Area: {vzs_in_down_proportion:.2f}%")
