####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt
import tp_voltage as tpv

class ThreePhaseVoltageCMV(tpv.ThreePhaseVoltage):
    def __init__(self, mi):
        super().__init__(mi=mi)

        ##### override with CMV-specific time/angle arrays (higher resolution)
        self.time = np.linspace(0, 0.02, 10000)  # 50 Hz fundamental frequency
        self.angle = self.time * 2 * np.pi * 50  # Phase angle over time
        self.degree = self.angle * 180 / np.pi
        self.start_anlge = 0  # Starting phase angle

        ##### CMV-specific voltage arrays for VPOD / VPD
        self.Vzmax = []
        self.Vzmin = []
        self.VPOD_max = np.zeros_like(self.time)
        self.VPOD_min = np.zeros_like(self.time)
        self.VPD_max1 = np.zeros_like(self.time)
        self.VPD_min1 = np.zeros_like(self.time)
        self.VPD_max2 = np.zeros_like(self.time)
        self.VPD_min2 = np.zeros_like(self.time)
        self.Ymax = 1.3
        self.Ymin = -self.Ymax

    def calculate_voltages(self):
        ##### calculate three-phase voltages using CMV-specific time base
        self.Va = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + self.start_anlge)
        self.Vb = self.modulation_index * np.sin(2 * np.pi * 50 * self.time - 2 * np.pi / 3 + self.start_anlge)
        self.Vc = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + 2 * np.pi / 3 + self.start_anlge)

        vmax_arr = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        vmin_arr = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))
        vmid_arr = self.Va + self.Vb + self.Vc - vmax_arr - vmin_arr

        ##### use base class method for zero-sequence voltage limitation (Vzmax / Vzmin)
        self.Vzmax, self.Vzmin = self.vzslimit_cal()

        ##### use base class method for space-vector zero-sequence voltage (Vzs_SV)
        self.vzs_sv_cal()

        ##### use base class method for zero-crossing detection zero-sequence voltage (Vzs_ZCD)
        self.vzs_zcd_cal()

        ##### CMV-specific: VPOD (Phase Opposition Disposition) limits
        self.VPOD_max = np.minimum(self.Vzmax, 0.5 * vmax_arr)
        self.VPOD_min = np.maximum(self.Vzmin, 0.5 * vmin_arr)

        ##### CMV-specific: VPD (Phase Disposition) limits, case 1
        for i in range(len(self.Va)):
            if (1 + vmin_arr[i]) <= vmid_arr[i]:
                self.VPD_max1[i] = self.Vzmax[i]
                self.VPD_min1[i] = np.maximum(self.Vzmin[i], -vmid_arr[i])
            else:
                self.VPD_max1[i] = np.nan
                self.VPD_min1[i] = np.nan

        ##### CMV-specific: VPD (Phase Disposition) limits, case 2
        for i in range(len(self.Va)):
            if (1 + vmid_arr[i]) <= vmax_arr[i]:
                self.VPD_max2[i] = np.minimum(self.Vzmax[i], -vmid_arr[i])
                self.VPD_min2[i] = self.Vzmin[i]
            else:
                self.VPD_max2[i] = np.nan
                self.VPD_min2[i] = np.nan

    def fig_plot(self, picsize=(7, 4.2)):
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # solve the problem of negative sign display as a square
        plt.rcParams['mathtext.fontset'] = 'stix'  # set math font to match Times style

        fig, ax = plt.subplots(figsize=picsize, layout='constrained')

        ax.plot(self.angle, self.Vzmax, color='#FFE699', linewidth=2)
        ax.plot(self.angle, self.Vzmin, color='#D3ECB9', linewidth=2)
        ax.plot(self.angle, self.Vzs_SV, color='#FF9999', linewidth=2)
        ax.plot(self.angle, self.Vzs_ZCD, color="#A099FF", linewidth=2)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(8)  # fontsize
            label.set_fontweight('bold')  # font weight bold
        ax.set_xlabel('Angle (rad)', fontsize=14, fontweight='bold')
        ax.set_ylabel('zero-sequence Voltage (p.u.)', fontsize=14, fontweight='bold')
        ax.tick_params(axis='y', labelsize=14)
        ax.set_xlim(0, self.angle[-1])
        ax.grid(linestyle='--', alpha=0.3)

        xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=14, fontweight='bold')

        ax.fill_between(
            self.angle,
            self.VPOD_max,
            self.VPOD_min,
            where=None,
            color="#96EBFE",
            alpha=0.3,
            label=None
        )

        ax.fill_between(
            self.angle,
            self.VPD_max1,
            self.VPD_min1,
            where=None,
            color="#666666",
            alpha=0.3,
            label=None
        )

        ax.fill_between(
            self.angle,
            self.VPD_max2,
            self.VPD_min2,
            where=None,
            color="#666666",
            alpha=0.3,
            label=None
        )

        plt.show()

if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    ClassThreePhaseVoltage = ThreePhaseVoltageCMV(modulation_index)
    ClassThreePhaseVoltage.calculate_voltages()
    ClassThreePhaseVoltage.fig_plot()
