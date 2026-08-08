####### This file is aimed at plotting the PD-I PWM's low
####### common mode voltage area and its proportion
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from python_pwm.pod_pd_pwm.pd_pod_cmv import PdPodCmv
class Pd1_cmv(PdPodCmv):
    def vzs_calculate(self):
        for i in range(len(self.modulation_3d)):
            for j in range(len(self.wt)):
                ### pd1's vzs_max is equivalent to other files' vzs_down_max
                if self.one_plus_min[i,j] <= self.v_mid[i,j] and self.vz_max_3d[i,j] >= np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j]):
                    self.vzs_up_max[i,j] = self.vz_max_3d[i,j]
                    self.vzs_up_min[i,j] = np.maximum(-self.v_mid[i,j], self.vz_min_3d[i,j])
                else:
                    self.vzs_up_max[i,j] = np.nan
                    self.vzs_up_min[i,j] = np.nan

                ### up region is not used by pd1 — set to vz_max_3d so up volume = 0
                self.vzs_down_max[i,j] = self.vz_max_3d[i,j]
                self.vzs_down_min[i,j] = self.vz_max_3d[i,j]

    def data_2d_fill_plot(self, pic_size=(16, 9)):
        """Plot low-CMV filled area slices at 6 modulation indices for PD-I only."""
        import matplotlib.pyplot as plt

        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams['mathtext.fontset'] = 'stix'

        fig, axes = plt.subplots(2, 3, figsize=pic_size, layout='constrained')
        axes = axes.flatten()

        modu_ratios = np.array([1/6, 1/3, 1/2, 2/3, 5/6, 1.0])
        modu_values = 2 / np.sqrt(3) * modu_ratios
        color = '#4472C4'
        label = 'PD-I'

        for idx, (ax, modu_val, ratio) in enumerate(
            zip(axes, modu_values, modu_ratios)
        ):
            modu_idx = np.argmin(np.abs(self.modulation_3d - modu_val))
            actual_modu = self.modulation_3d[modu_idx]

            # ---- upper region (vzs > -v_mid) ----
            ax.fill_between(
                self.wt,
                self.vzs_up_min[modu_idx, :],
                self.vzs_up_max[modu_idx, :],
                color=color, alpha=0.60, edgecolor='none', linewidth=0,
            )

            # ---- lower region (vzs < -v_mid) ----
            ax.fill_between(
                self.wt,
                self.vzs_down_min[modu_idx, :],
                self.vzs_down_max[modu_idx, :],
                color=color, alpha=0.60, edgecolor='none', linewidth=0,
            )

            # ---- VZS boundary lines ----
            ax.plot(self.wt, self.vz_max_3d[modu_idx, :],
                    color='#DC143C', linewidth=1.5, alpha=0.85)
            ax.plot(self.wt, self.vz_min_3d[modu_idx, :],
                    color='#2E86AB', linewidth=1.5, alpha=0.85)

            # ---- reference line: -v_mid ----
            ax.plot(self.wt, -self.v_mid[modu_idx, :], 'k--',
                    linewidth=1.5, alpha=0.55)

            # ---- axis / title settings ----
            ax.set_title(
                r'$m = \frac{2}{\sqrt{3}} \times $'
                + f'{ratio:.3f}  (actual: {actual_modu:.4f})',
                fontweight='bold', fontsize=12,
            )
            ax.set_xlabel('Angle (rad)', fontweight='bold', fontsize=12)
            ax.set_ylabel('Zero-sequence Voltage (p.u.)', fontweight='bold', fontsize=12)
            ax.set_xlim(0, self.wt[-1])
            ax.grid(linestyle='--', alpha=0.3, color='#7F7F7F')

            xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
            xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$']
            ax.set_xticks(xticks)
            ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')

            ax.tick_params(axis='y', labelsize=12)
            plt.setp(ax.get_yticklabels(), fontweight='bold')

        # ---- legend ----
        from matplotlib.lines import Line2D
        legend_handles = [
            plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.55),
            Line2D([0], [0], color='#DC143C', linewidth=1.5, alpha=0.85),
            Line2D([0], [0], color='#2E86AB', linewidth=1.5, alpha=0.85),
            Line2D([0], [0], color='black', linestyle='--', linewidth=1.5, alpha=0.55),
        ]
        legend_labels = [
            f'{label} Low-CMV Area',
            r'$v_{z,max}$',
            r'$v_{z,min}$',
            r'$-v_{mid}$',
        ]
        fig.legend(legend_handles, legend_labels, loc='right',
                   ncol=1, fontsize=10, frameon=True)

        fig.suptitle(
            f'{label} Low Common-Mode Voltage Filled Area at Different Modulation Indices',
            fontweight='bold', fontsize=14,
        )
        plt.show()


if __name__ == "__main__":
    test_instance = Pd1_cmv()
    test_instance.data_3d_calculate()
    test_instance.vzs_calculate()
    test_instance.data_2d_fill_plot()
