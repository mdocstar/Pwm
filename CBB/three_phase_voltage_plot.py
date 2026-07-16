####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt
from CBB import tp_voltage as tpv

class ThreePhaseVoltagePlot(tpv.ThreePhaseVoltage):
    def __init__(self, mi):
        super().__init__(mi=mi)

        ##### override with plot-specific display / time settings
        self.xy_labels = ['Time (s)', 'Voltage (p.u.)']
        self.xy_labels_fontsize = 14
        self.grid_labels_fontsize = 12
        self.legend_fontsize = 14

        self.time = np.linspace(0, 0.04, 10000)  # 50 Hz fundamental frequency
        self.angle = self.time * 2 * np.pi * 50  # Phase angle over time
        self.degree = self.angle * 180 / np.pi
        self.start_angle = np.pi / 6  # Starting phase angle

        ##### recalculate Va/Vb/Vc with plot-specific time base and start angle
        self.Va = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + self.start_angle)
        self.Vb = self.modulation_index * np.sin(2 * np.pi * 50 * self.time - 2 * np.pi / 3 + self.start_angle)
        self.Vc = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + 2 * np.pi / 3 + self.start_angle)

        self.y_max = 1.3
        self.y_min = -self.y_max

    def fill_sector(self, ax, x_start, x_end, **parameters):
        if 'color' in parameters:
            func_color = parameters['color']
        else:
            func_color = 'lightblue'

        if 'label' in parameters:
            func_label = parameters['label']
        else:
            func_label = None

        ax.fill_between(
            np.linspace(x_start, x_end, 1000),
            self.y_min,
            self.y_max,
            where=None,
            color=func_color,
            alpha=0.3,
            label=func_label
        )

        ax.text(
            0.5 * (x_start + x_end),
            -1.10,
            func_label,
            fontsize=12,
            fontweight='bold',
            ha='center',
            va='center',
            color='#000000',
        )

    def three_voltage_plot(self, pic_size=(7, 4.3)):
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False        # fix negative sign display issue
        fig, ax = plt.subplots(figsize=pic_size, layout='constrained')

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(self.grid_labels_fontsize)
            label.set_fontweight('bold')

        ax.plot(self.angle, self.Va, label='Phase A Voltage', color='r')
        ax.plot(self.angle, self.Vb, label='Phase B Voltage', color='g')
        ax.plot(self.angle, self.Vc, label='Phase C Voltage', color='b')
        ax.set_title(f'Three-Phase Voltage Waveforms (Modulation Index = {self.modulation_index})', fontweight='bold')
        ax.set_xlabel('Angle (rad)', fontsize=self.xy_labels_fontsize, fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)', fontsize=self.xy_labels_fontsize, fontweight='bold')
        ax.set_xlim(0, self.angle[-1])
        ax.set_ylim(self.y_min, self.y_max)

        ax.legend(loc='upper right', fontsize=self.legend_fontsize)
        ax.grid(linestyle='--', alpha=0.3)

        ##### fill sectors with different colors
        sector_list = np.linspace(0, 4 * np.pi, 7)
        sector_color = ["#FEBF96", '#D3ECB9', '#D3FFFE']
        sector_labels = ['Sector I', 'Sector II', 'Sector III']
        for i in range(len(sector_list) - 1):
            x_start = sector_list[i]
            x_end = sector_list[i + 1]
            self.fill_sector(ax, x_start, x_end,
                             color=sector_color[i % len(sector_color)],
                             label=sector_labels[i % len(sector_labels)])

        plt.show()

if __name__ == "__main__":
    modulation_index = 0.85  # Example modulation index
    three_phase_voltage = ThreePhaseVoltagePlot(modulation_index)
    three_phase_voltage.three_voltage_plot()
