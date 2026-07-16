####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, mi=0.90, frequency=50, start_angle=0, time=0.02):
        ##### initialize all instance attributes
        self.modulation_index = None
        self.wt = None
        self.start_angle = None
        self.Va = None
        self.Vb = None
        self.Vc = None
        self.vzs_sv = None
        self.vzs_zcd = None
        ##### use data_reset to initialize the three-phase voltage parameters
        self.data_reset(mi, frequency, start_angle, time)

    def data_reset(self, mi=0.90, frequency=50, start_angle=0, time=0.02):
        ##### set modulation index limitation 0~2/sqrt(3)
        mi = max(0, mi)
        mi = min(2 / np.sqrt(3), mi)
        self.modulation_index = mi

        ##### set three-phase voltage parameters
        self.wt = np.linspace(0, 2*np.pi*frequency*time, 1000)  # 50 Hz fundamental frequency
        self.start_angle = start_angle  # Starting phase angle
        self.Va = self.modulation_index * np.sin(self.wt + self.start_angle)
        self.Vb = self.modulation_index * np.sin(self.wt - 2 * np.pi / 3 + self.start_angle)
        self.Vc = self.modulation_index * np.sin(self.wt + 2 * np.pi / 3 + self.start_angle)
        self.vzs_sv = None
        self.vzs_zcd = None

    def vzs_limit_calculate(self):
        ##### calculate zero-sequence voltage limitation
        umax = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        umin = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))

        vzs_max = np.minimum(1 - umax, -umin)
        vzs_min = np.maximum(-1 - umin, -umax)
        return vzs_max, vzs_min
    
    def v_max_min_calculate(self):
        ##### calculate the maximum and minimum of the three-phase voltages
        vmax = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        vmin = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))
        return vmax, vmin

    def vzs_sv_calculate(self):
        ##### calculate zero-sequence voltage using space vector (SV) method
        ##### vzs_sv = -0.5 * (Vmax + Vmin), representing the common-mode
        ##### voltage injected in standard space-vector PWM
        vmax_arr = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        vmin_arr = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))
        self.vzs_sv = -0.5 * (vmax_arr + vmin_arr)
        return self.vzs_sv

    def vzs_zcd_calculate(self):
        ##### calculate zero-sequence voltage using zero-crossing detection (ZCD) method
        ##### the method determines which two phases share the same sign,
        ##### then computes the ZCD voltage from the third (odd-one-out) phase
        ##### and clamps the result to the negated middle voltage (-vmid)
        n = len(self.Va)
        self.vzs_zcd = np.zeros(n)

        for i in range(n):
            va = self.Va[i]
            vb = self.Vb[i]
            vc = self.Vc[i]

            vmax = max(va, vb, vc)
            vmin = min(va, vb, vc)
            vmid = va + vb + vc - vmax - vmin
            vmid = -vmid

            if np.sign(va) == np.sign(vb):
                self.vzs_zcd[i] = np.sign(vc) - vc
            elif np.sign(va) == np.sign(vc):
                self.vzs_zcd[i] = np.sign(vb) - vb
            else:
                self.vzs_zcd[i] = np.sign(va) - va

            if abs(self.vzs_zcd[i]) > abs(vmid):
                self.vzs_zcd[i] = vmid

        return self.vzs_zcd

    def data_plot(self, *parameters, pic_size=(7, 4.3)):
        ##### plot three-phase voltage waveforms
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False      # fix negative sign display issue
        plt.rcParams['mathtext.fontset'] = 'stix'
        fig, ax = plt.subplots(figsize=pic_size)

        ##### plot the data waveforms
        for parameter in parameters:
            ax.plot(self.wt, parameter, linewidth=2.0)

        ##### set grid label font size and weight
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(12)
            label.set_fontweight('bold')

        ##### set axis labels, limits, and grid
        ax.set_xlabel(r'$\theta$ (rad)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)', fontsize=14, fontweight='bold')
        ax.set_xlim(0, self.wt[-1])
        ax.grid(linestyle='--', alpha=0.3)
        plt.show()

if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    three_phase_voltage = ThreePhaseVoltage(modulation_index)
    result_max, result_min = three_phase_voltage.vzs_limit_calculate()
    three_phase_voltage.data_plot(three_phase_voltage.Va, three_phase_voltage.Vb, three_phase_voltage.Vc, result_max, result_min)
