####### This file is aimed at plotting the PD-I PWM's
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
                up_limit  = self.v_max[i,j] * 0.5
                low_limit = np.minimum(-self.v_mid[i,j],-1 + self.v_max[i,j] )
                
                ### set low common mode voltage area when vzs > -v_mid 
                if (-self.v_mid[i,j] <= up_limit and 
                    np.minimum(up_limit, self.vz_max_3d[i,j]) >= np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])):
                    self.vzs_up_low_cmv_max[i,j] = np.minimum(up_limit, self.vz_max_3d[i,j])
                    self.vzs_up_low_cmv_min[i,j] = np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])
                else:
                    self.vzs_up_low_cmv_max[i,j] = np.nan
                    self.vzs_up_low_cmv_min[i,j] = np.nan
                    
                ### set low common mode voltage area when vzs < -v_mid 
                if (self.v_min[i,j] * 0.5 <= low_limit and 
                    np.minimum(low_limit, self.vz_max_3d[i,j]) >= np.maximum(self.v_min[i,j] * 0.5, self.vz_min_3d[i,j])):
                    self.vzs_down_low_cmv_max[i,j] = np.minimum(low_limit, self.vz_max_3d[i,j])
                    self.vzs_down_low_cmv_min[i,j] = np.maximum(self.v_min[i,j] * 0.5, self.vz_min_3d[i,j])
                else:
                    self.vzs_down_low_cmv_max[i,j] = np.nan
                    self.vzs_down_low_cmv_min[i,j] = np.nan

    def data_porportion_calculate(self):
        data_3d_volume = 0
        up_low_cmv_volume = 0
        down_low_cmv_volume = 0
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                if not np.isnan(self.vzs_up_low_cmv_max[i,j]) and not np.isnan(self.vzs_up_low_cmv_min[i,j]):
                    up_low_cmv_volume += self.vzs_up_low_cmv_max[i,j] - self.vzs_up_low_cmv_min[i,j]
                if not np.isnan(self.vzs_down_low_cmv_max[i,j]) and not np.isnan(self.vzs_down_low_cmv_min[i,j]):
                    down_low_cmv_volume += self.vzs_down_low_cmv_max[i,j] - self.vzs_down_low_cmv_min[i,j]
                # calculate the total volume of 3D data    
                data_3d_volume += self.vz_max_3d[i,j] - self.vz_min_3d[i,j]

        vzs_up_low_cmv_proportion   = (up_low_cmv_volume ) * 100 / data_3d_volume if data_3d_volume != 0 else 0
        vzs_down_low_cmv_proportion = (down_low_cmv_volume) * 100 / data_3d_volume if data_3d_volume != 0 else 0
        vzs_low_cmv_proportion      = (up_low_cmv_volume + down_low_cmv_volume) * 100 / data_3d_volume if data_3d_volume != 0 else 0
        return  vzs_up_low_cmv_proportion, vzs_down_low_cmv_proportion, vzs_low_cmv_proportion

if __name__ == "__main__":
    test_instance = Pd2_cmv()
    test_instance.data_3d_calculate()
    test_instance.vzs_low_cmv_calculate()
    #test_instance.data_3d_plot(test_instance.vzs_low_cmv_max, test_instance.vzs_low_cmv_min)
    vzs_up_low_cmv_proportion, vzs_down_low_cmv_proportion, vzs_low_cmv_proportion = test_instance.data_porportion_calculate()
    print(f"{vzs_up_low_cmv_proportion:.2f}%")
    print(f"{vzs_down_low_cmv_proportion:.2f}%")
    print(f"{vzs_low_cmv_proportion:.2f}%")
