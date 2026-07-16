import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from CBB import tp_voltage as tpv

class ThreePhase3D(tpv.ThreePhaseVoltage):
    def __init__(self):
        super().__init__(mi=0.90)
        self.modulation_3d = np.linspace(0, 2 / np.sqrt(3), int(1e3))
        self.X = np.zeros((len(self.modulation_3d), len(self.wt)))
        self.Y = np.zeros((len(self.modulation_3d), len(self.wt)))
        self.vz_max_3d = np.zeros((len(self.modulation_3d), len(self.wt)))
        self.vz_min_3d = np.zeros((len(self.modulation_3d), len(self.wt)))

    def data_3d_calculate(self):
        for i in range(self.X.shape[0]):
            self.data_reset(mi=self.modulation_3d[i])
            self.vz_max_3d[i, :], self.vz_min_3d[i, :] = self.vzs_limit_calculate()
            for j in range(self.X.shape[1]):
                self.X[i, j] = self.wt[j]
                self.Y[i, j] = self.modulation_3d[i]

    def data_3d_plot(self):
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # fix negative sign display issue
        plt.rcParams['mathtext.fontset'] = 'stix'  # match math font to Times style

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        plt.subplots_adjust(left=0.05, right=0.95, top=0.98, bottom=0.02)  # cut some white space around the plot

        # ===================== axis settings =====================
        ##### set the projection type to orthographic for a more technical look
        ax.set_proj_type('ortho')

        ##### set facecolor to white for a cleaner background
        ax.set_facecolor('white')
        # close the panes to make the plot cleaner
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        # set grid lines to a light gray for better visibility without overpowering the data
        ax.grid(color='#C0C0C0')
        # set the axis lines to a darker gray for better contrast
        ax.xaxis.line.set_color('#666666')
        ax.yaxis.line.set_color('#666666')
        ax.zaxis.line.set_color('#666666')

        ##### set view angle for better visibility of the 3D structure
        ax.view_init(elev=30, azim=45, roll=0)

        # ===================== colorbar settings =====================
        cmap = cm.viridis
        combined_data = np.concatenate([self.vz_max_3d.ravel(), self.vz_min_3d.ravel()])
        vmin, vmax = combined_data.min(), combined_data.max()

        # ===================== plot two surfaces =====================
        ax.plot_surface(
            self.X, self.Y, self.vz_min_3d,
            cmap=cmap, alpha=1.0, vmin=vmin, vmax=vmax,
            rstride=2, cstride=5,
            antialiased=True, edgecolor='none'
        )

        surface = ax.plot_surface(
            self.X, self.Y, self.vz_max_3d,
            cmap=cmap, alpha=1.0, vmin=vmin, vmax=vmax,
            rstride=2, cstride=5,
            antialiased=True, edgecolor='none'
            )
        cbar = fig.colorbar(surface, ax=ax, shrink=0.7, pad=0.05)

        # ===================== label fonts =====================
        ax.set_xlabel('Angle (rad)', fontweight='bold')
        ax.set_ylabel('Modulation Index', fontweight='bold')
        ax.set_zlabel('Zero-sequence Voltage (p.u.)', fontweight='bold')
        ax.set_box_aspect(None, zoom=0.95)

        # ===================== X axis label =====================
        xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')

        plt.show()

if __name__ == "__main__":
    test_instance = ThreePhase3D()
    test_instance.data_3d_calculate()
    test_instance.data_3d_plot()
