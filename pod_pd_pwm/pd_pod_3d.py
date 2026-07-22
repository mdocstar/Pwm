####### Summary plot of PD-I, PD-II, POD-I, POD-II low common-mode
####### voltage areas in a 2×2 3D subplot layout.
####### Envelope: vz_max_3d / vz_min_3d drawn as dashed wireframe lines.
####### Filled regions: up (vzs_up_max → vzs_up_min) and down
####### (vzs_down_max → vzs_down_min) with distinct colours.
####### vzs_division is overlaid to separate the upper/lower zones.

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from pod_pd_pwm.pd1_cmv  import Pd1_cmv
from pod_pd_pwm.pd2_cmv  import Pd2_cmv
from pod_pd_pwm.pod1_cmv import Pod1_cmv
from pod_pd_pwm.pod2_cmv import Pod2_cmv


class PdPod3D:
    """Hold the four PWM variants and produce the summary 2×2 plot."""

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

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _plot_envelope(ax, X, Y, Z_max, Z_min, n_lines=18):
        """Draw vz_max_3d and vz_min_3d as dashed envelope curves.

        Samples *n_lines* equally-spaced modulation indices and plots each
        slice vs. angle as a dashed black line.  This gives a lightweight
        wireframe-style envelope without resorting to a full surface or
        colorbar.
        """
        n_modu = Z_max.shape[0]
        idx = np.linspace(0, n_modu - 1, n_lines, dtype=int)
        for i in idx:
            ax.plot(X[i, :], Y[i, :], Z_max[i, :],
                    color='#333333', linestyle='--', linewidth=0.5, alpha=0.6)
            ax.plot(X[i, :], Y[i, :], Z_min[i, :],
                    color='#333333', linestyle='--', linewidth=0.5, alpha=0.6)

    @staticmethod
    def _plot_filled_region(ax, X, Y, Z_max, Z_min, face_color,
                            rstride=4, cstride=4, stem_stride=25):
        """Fill the band between *Z_max* and *Z_min*.

        Two complementary techniques are used:

        1. **Surface pair** — both bounding surfaces are drawn with the same
           face colour so the band reads as a contiguous slab.
        2. **Vertical stems** — sparse vertical lines connect *Z_min* to
           *Z_max* so the "filled" character is obvious even when the two
           surfaces are close together.

        NaN cells are naturally skipped, leaving holes where the low-CMV
        condition is not met.
        """
        # --- surface backdrop ------------------------------------------
        kw_surf = dict(rstride=rstride, cstride=cstride,
                       antialiased=True, edgecolor='none',
                       alpha=0.55, shade=True)
        ax.plot_surface(X, Y, Z_max, color=face_color, **kw_surf)
        ax.plot_surface(X, Y, Z_min, color=face_color, **kw_surf)

        # --- vertical stems for explicit fill --------------------------
        n_modu, n_wt = Z_max.shape
        segments = []
        for i in range(0, n_modu, stem_stride):
            for j in range(0, n_wt, stem_stride):
                z_hi = Z_max[i, j]
                z_lo = Z_min[i, j]
                if (not np.isnan(z_hi) and not np.isnan(z_lo)
                        and z_hi - z_lo > 1e-10):
                    x = X[i, j]
                    y = Y[i, j]
                    segments.append([[x, y, z_lo], [x, y, z_hi]])
        if segments:
            lc = Line3DCollection(segments, colors=face_color,
                                  linewidths=0.4, alpha=0.55)
            ax.add_collection3d(lc)

    @staticmethod
    def _plot_division(ax, X, Y, Z_div, rstride=6, cstride=6):
        """Draw the vzs_division surface as a semi-transparent wireframe
        that separates the upper and lower low-CMV regions."""
        ax.plot_wireframe(X, Y, Z_div,
                          color='#228B22', rstride=rstride, cstride=cstride,
                          linewidth=0.5, alpha=0.5)

    @staticmethod
    def _style_3d_ax(ax, title):
        """Apply consistent cosmetics to one 3D Axes3D subplot."""
        ax.set_proj_type('ortho')
        ax.set_facecolor('white')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(color='#C0C0C0', linewidth=0.4)
        for spine in (ax.xaxis.line, ax.yaxis.line, ax.zaxis.line):
            spine.set_color('#666666')

        ax.view_init(elev=30, azim=45, roll=0)

        ax.set_xlabel('Angle (rad)', fontweight='bold', fontsize=8)
        ax.set_ylabel('Modulation Index', fontweight='bold', fontsize=8)
        ax.set_zlabel('Zero-sequence Voltage (p.u.)',
                      fontweight='bold', fontsize=8)
        ax.set_title(title, fontweight='bold', fontsize=11, pad=2)

        xticks = [0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi]
        xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$',
                        r'$3\pi/2$', r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=7, fontweight='bold')
        ax.set_box_aspect(None, zoom=0.88)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def plot_2x2(self, up_color='#4472C4', down_color='#ED7D31'):
        """Draw the 2×2 summary figure.

        Parameters
        ----------
        up_color : str
            Face colour for the upper low-CMV band (vzs > -v_mid).
        down_color : str
            Face colour for the lower low-CMV band (vzs < -v_mid).
        """
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams['mathtext.fontset'] = 'stix'

        fig, axes = plt.subplots(
            2, 2,
            subplot_kw={"projection": "3d"},
            figsize=(14, 11),
        )
        plt.subplots_adjust(left=0.02, right=0.98,
                            top=0.94, bottom=0.04,
                            wspace=0.12, hspace=0.18)

        titles = ['PD-I', 'PD-II', 'POD-I', 'POD-II']

        for title, ax in zip(titles, axes.flat):
            inst = self.variants[title]

            # 1. Dashed envelope — vz_max_3d & vz_min_3d
            self._plot_envelope(ax, inst.X, inst.Y,
                                inst.vz_max_3d, inst.vz_min_3d)

            # 2. Upper low-CMV band (vzs > -v_mid)
            self._plot_filled_region(ax, inst.X, inst.Y,
                                     inst.vzs_up_max, inst.vzs_up_min,
                                     up_color)

            # 3. Lower low-CMV band (vzs < -v_mid)
            self._plot_filled_region(ax, inst.X, inst.Y,
                                     inst.vzs_down_max, inst.vzs_down_min,
                                     down_color)

            # 4. Division surface — separates upper / lower regions
            # self._plot_division(ax, inst.X, inst.Y, inst.vzs_division)

            self._style_3d_ax(ax, title)

        plt.show()


# ------------------------------------------------------------------
# Standalone test
# ------------------------------------------------------------------
if __name__ == "__main__":
    plotter = PdPod3D()
    plotter.plot_2x2()
