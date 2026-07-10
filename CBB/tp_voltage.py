####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, mi=0.90, fre=50, start_angle=0, time=0.02):
        ##### initialize all instance attributes
        self.modulation_index = None
        self.wt = None
        self.start_anlge = None
        self.Va = None
        self.Vb = None
        self.Vc = None
        ##### use data_reset to initialize the three-phase voltage parameters
        self.data_reset(mi, fre, start_angle, time)

    def data_reset(self, mi=0.90, fre=50, start_angle=0, time=0.02):
        ##### set modulation index limitation 0~2/sqrt(3)
        mi = max(0, mi)
        mi = min(2 / np.sqrt(3), mi)
        self.modulation_index = mi

        ##### set three-phase voltage parameters
        self.wt = np.linspace(0, 2*np.pi*fre*time, 1000)  # 50 Hz fundamental frequency
        self.start_anlge = start_angle  # Starting phase angle
        self.Va = self.modulation_index * np.sin(self.wt + self.start_anlge)
        self.Vb = self.modulation_index * np.sin(self.wt - 2 * np.pi / 3 + self.start_anlge)
        self.Vc = self.modulation_index * np.sin(self.wt + 2 * np.pi / 3 + self.start_anlge)

    def vzslimit_cal(self):
        ##### calculate zero-sequence voltage limitation
        umax = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        umin = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))

        vzs_max = np.minimum(1 - umax, -umin)
        vzs_min = np.maximum(-1 - umin, -umax)
        return vzs_max, vzs_min

    def data_plot(self, *parameters, picsize=(7, 4.3)):
        ##### plot three-phase voltage waveforms
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False      # fix negative sign display issue
        plt.rcParams['mathtext.fontset'] = 'stix'
        fig, ax = plt.subplots(figsize=picsize)

        ##### plot the data waveforms
        for paramter in parameters:
            ax.plot(self.wt, paramter,linewidth=2.0)
              
        ##### set grid label font size and weight
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)  
            label.set_fontweight('bold')
        
        ##### set axis labels, limits, and grid    
        ax.set_xlabel(r'$\theta$ (rad)', fontsize=14,fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)', fontsize=14,fontweight='bold')
        ax.set_xlim(0,self.wt[-1])
        ax.grid(linestyle='--', alpha=0.3)
        plt.show()
    
if __name__ == "__main__":
    mod_idx = 0.90  # Example modulation index
    class_three_phase_voltage = ThreePhaseVoltage(mod_idx)
    result_max, result_min = class_three_phase_voltage.vzslimit_cal()
    class_three_phase_voltage.data_plot(class_three_phase_voltage.Va, class_three_phase_voltage.Vb, class_three_phase_voltage.Vc, result_max, result_min)
