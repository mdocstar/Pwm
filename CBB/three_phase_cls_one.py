import numpy as np
import matplotlib.pyplot as plt
from CBB import tp_voltage as tpv

class ThreePhaseClsOne(tpv.ThreePhaseVoltage):
    def __init__(self, mi):
        super().__init__(mi=mi)

        ##### override: ClsOne only covers one sector (0 ~ 2*pi/3)
        self.wt = np.linspace(0, 2 * np.pi / 3, 10000)

        ##### calculate three-phase voltage according to voltage max/mid/min division
        self.umax = self.modulation_index * np.sin(self.wt + np.pi / 6)
        self.umid = np.zeros_like(self.wt)
        self.umin = np.zeros_like(self.wt)

        division_curve = np.pi / 3
        division1 = self.wt < division_curve
        self.umid[division1] = self.modulation_index * np.sin(self.wt[division1] + 5 * np.pi / 6)
        self.umin[division1] = self.modulation_index * np.sin(self.wt[division1] - np.pi / 2)

        division2 = self.wt >= division_curve
        self.umid[division2] = self.modulation_index * np.sin(self.wt[division2] - np.pi / 2)
        self.umin[division2] = self.modulation_index * np.sin(self.wt[division2] + 5 * np.pi / 6)

        ##### set Va/Vb/Vc from umax/umid/umin so base class methods can operate on them
        self.Va = self.umax
        self.Vb = self.umid
        self.Vc = self.umin

        ##### calculate zero-sequence voltage limitation using base class method
        self.vzs_max, self.vzs_min = self.vzs_limit_calculate()

    def three_phase_plot(self, pic_size=(10, 7.0)):
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # solve negative sign display issue
        plt.rcParams['mathtext.fontset'] = 'stix'        # match math font to Times style

        fig, ax = plt.subplots(figsize=pic_size, layout='constrained')
        xticks = [0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3]
        xtick_labels = [r'$0$', r'$\pi/6$', r'$\pi/3$', r'$\pi/2$', r'$2\pi/3$']

        #### three-phase voltage plot
        ax.plot(self.wt, self.umax, label='Phase Voltage Umax', color='#FFE699')
        ax.plot(self.wt, self.umid, label='Phase Voltage Umid', color='#D3ECB9')
        ax.plot(self.wt, self.umin, label='Phase Voltage Umin', color='#FF9999')
        ax.plot(self.wt, self.vzs_max, label='Zero-sequence voltage maximum', color='#0072BD', linestyle='--')
        ax.plot(self.wt, self.vzs_min, label='Zero-sequence voltage minimum', color='#D95319', linestyle='--')
        ax.set_title(f'Three-Phase Voltage Waveforms (Modulation Index = {self.modulation_index})', fontweight='bold')
        ax.set_xlabel('Angle (rad)', fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)', fontweight='bold')
        ax.set_xlim(0, self.wt[-1])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(linestyle='--', alpha=0.3)

        plt.show()

if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    three_phase_voltage = ThreePhaseClsOne(modulation_index)
    three_phase_voltage.three_phase_plot()
