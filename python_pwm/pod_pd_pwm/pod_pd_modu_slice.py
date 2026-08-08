####### This file is aimed at plotting the PD-POD PWM's low
####### common mode voltage area at specific modulation index slices
####### (2/sqrt(3) × [1/6, 1/3, 1/2, 2/3, 5/6, 1.0])
####### with fill-between regions for all four modulation variants

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import matplotlib.pyplot as plt
from python_pwm.pod_pd_pwm.pd1_cmv  import Pd1_cmv
from python_pwm.pod_pd_pwm.pd2_cmv  import Pd2_cmv
from python_pwm.pod_pd_pwm.pod1_cmv import Pod1_cmv
from python_pwm.pod_pd_pwm.pod2_cmv import Pod2_cmv


class PodPdModuSlice:
    def __init__(self):
        self.variants = {
            'PD-I':   Pd1_cmv(),
            'PD-II':  Pd2_cmv(),
            'POD-I':  Pod1_cmv(),
            'POD-II': Pod2_cmv(),
        }
        for inst in self.variants.values():
            inst.data_3d_calculate()
            inst.vzs_calculate()

        # modulation ratios to slice at
        self.modu_ratios = np.array([1/6, 1/3, 1/2, 2/3, 5/6, 1.0])
        self.modu_values = 2 / np.sqrt(3) * self.modu_ratios

    def data_2d_fill_plot(self, pic_size=(16, 9)):
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams['mathtext.fontset'] = 'stix'

        fig, axes = plt.subplots(2, 3, figsize=pic_size, layout='constrained')
        axes = axes.flatten()

        colors = {
            'PD-I':   '#4472C4',
            'PD-II':  '#ED7D31',
            'POD-I':  '#70AD47',
            'POD-II': '#A855F7',
        }

        # get wt array from any variant (all share the same wt)
        wt = list(self.variants.values())[0].wt

        for idx, (ax, modu_val, ratio) in enumerate(
            zip(axes, self.modu_values, self.modu_ratios)
        ):
            # find the closest modulation index in modulation_3d
            modu_idx = np.argmin(
                np.abs(
                    list(self.variants.values())[0].modulation_3d - modu_val
                )
            )
            actual_modu = list(self.variants.values())[0].modulation_3d[modu_idx]

            for label, inst in self.variants.items():
                # ---- upper region (vzs > -v_mid) ----
                ax.fill_between(
                    wt,
                    inst.vzs_up_min[modu_idx, :],
                    inst.vzs_up_max[modu_idx, :],
                    color=colors[label],
                    alpha=0.60,
                    edgecolor='none',
                    linewidth=0,
                )

                # ---- lower region (vzs < -v_mid) ----
                ax.fill_between(
                    wt,
                    inst.vzs_down_min[modu_idx, :],
                    inst.vzs_down_max[modu_idx, :],
                    color=colors[label],
                    alpha=0.60,
                    edgecolor='none',
                    linewidth=0,
                )

            # ---- VZS boundary lines: vz_max_3d and vz_min_3d ----
            first_inst = list(self.variants.values())[0]
            ax.plot(wt, first_inst.vz_max_3d[modu_idx, :],
                    color='#DC143C', linewidth=1.5, alpha=0.85,
                    label=r'$v_{z,max}$')
            ax.plot(wt, first_inst.vz_min_3d[modu_idx, :],
                    color='#2E86AB', linewidth=1.5, alpha=0.85,
                    label=r'$v_{z,min}$')

            # ---- reference line: -v_mid ----
            v_mid = list(self.variants.values())[0].v_mid[modu_idx, :]
            ax.plot(wt, -v_mid, 'k--', linewidth=1.5, alpha=0.55)

            # ---- axis / title settings ----
            ax.set_title(
                r'$m = \frac{2}{\sqrt{3}} \times $'
                + f'{ratio:.3f}'
                + f'  (actual: {actual_modu:.4f})',
                fontweight='bold',
                fontsize=12,
            )
            ax.set_xlabel('Angle (rad)', fontweight='bold', fontsize=12)
            ax.set_ylabel('Zero-sequence Voltage (p.u.)', fontweight='bold', fontsize=12)
            ax.set_xlim(0, wt[-1])
            ax.grid(linestyle='--', alpha=0.3, color='#7F7F7F')

            # x-axis ticks at 0, π/2, π, 3π/2, 2π
            xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
            xtick_labels = [
                r'$0$', r'$\pi/2$', r'$\pi$',
                r'$3\pi/2$', r'$2\pi$',
            ]
            ax.set_xticks(xticks)
            ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')

            # y-axis tick labels: enlarge + bold
            ax.tick_params(axis='y', labelsize=12)
            plt.setp(ax.get_yticklabels(), fontweight='bold')

        # ---- unified legend (variant colours + boundary lines) ----
        legend_handles = [
            plt.Rectangle((0, 0), 1, 1, color=colors[label], alpha=0.55)
            for label in self.variants.keys()
        ]
        legend_labels = list(self.variants.keys())

        # add VZS boundary lines to legend
        from matplotlib.lines import Line2D
        legend_handles.append(
            Line2D([0], [0], color='#DC143C', linewidth=1.5, alpha=0.85)
        )
        legend_labels.append(r'$v_{z,max}$')
        legend_handles.append(
            Line2D([0], [0], color='#2E86AB', linewidth=1.5, alpha=0.85)
        )
        legend_labels.append(r'$v_{z,min}$')

        # add -v_mid reference line
        legend_handles.append(
            Line2D([0], [0], color='black', linestyle='--', linewidth=0.8, alpha=0.55)
        )
        legend_labels.append(r'$-v_{mid}$')

        fig.legend(
            legend_handles,
            legend_labels,
            loc='right',
            ncol=7,
            fontsize=10,
            frameon=True,
        )

        fig.suptitle(
            'Low Common-Mode Voltage Filled Area at Different Modulation Indices',
            fontweight='bold',
            fontsize=14,
        )
        plt.show()


if __name__ == "__main__":
    plotter = PodPdModuSlice()
    plotter.data_2d_fill_plot()
