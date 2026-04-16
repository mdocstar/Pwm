import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import tp_voltage as tpv

class threephase3D(tpv.ThreePhaseVoltage):
    def __init__(self):
        super().__init__(modulation_index = 0.90)
        self.Modu3D = np.linspace(0, 2 / np.sqrt(3), int(1e3))
        self.X = np.zeros((len(self.Modu3D), len(self.wt)))
        self.Y = np.zeros((len(self.Modu3D), len(self.wt)))
        self.vzmax3D = np.zeros((len(self.Modu3D), len(self.wt)))
        self.vzmin3D = np.zeros((len(self.Modu3D), len(self.wt)))
    
    def data3D_Cal(self):
        for i in range(self.X.shape[0]):
            self.data_reset(modulation_index = self.Modu3D[i])
            self.vzmax3D[i,:],self.vzmin3D[i,:] = self.Vzslimit_cal()
            for j in range(self.X.shape[1]):
                self.X[i,j] = self.wt[j]
                self.Y[i,j] = self.Modu3D[i]

    def data3D_plot(self):
        plt.rcParams["font.family"] = "Times New Roman"  # 设置全局西文字体为 Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # 解决负号显示为方块的问题
        plt.rcParams['mathtext.fontset'] = 'stix'  # 让数学符号也匹配 Times 风格
        
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
        grid_color = "#C0C0C0"
        ax.xaxis._axinfo['grid']['color'] = grid_color
        ax.yaxis._axinfo['grid']['color'] = grid_color
        ax.zaxis._axinfo['grid']['color'] = grid_color
        # set the axis lines to a darker gray for better contrast
        ax.xaxis.line.set_color('#666666')
        ax.yaxis.line.set_color('#666666')
        ax.zaxis.line.set_color('#666666')
        
        ##### set view angle for better visibility of the 3D structure
        ax.view_init(elev=30, azim=45, roll=0)
        
        # ===================== colorbar settigns =====================
        cmap = cm.viridis  # 你可以换成 cm.plasma / cm.inferno / cm.Blues
        combined_data = np.concatenate([self.vzmax3D.ravel(), self.vzmin3D.ravel()])
        vmin, vmax = combined_data.min(), combined_data.max()
        
        # ===================== plot two surfaces =====================
        surf2 = ax.plot_surface(
            self.X, self.Y, self.vzmin3D,
            cmap=cmap, alpha=1.0, vmin=vmin, vmax=vmax,
            rstride=2, cstride=5,   # 根据数据密度调整
            antialiased=True, edgecolor='none'
            )
                
        surf1 = ax.plot_surface(
            self.X, self.Y, self.vzmax3D,
            cmap=cmap, alpha=1.0, vmin=vmin, vmax=vmax,
            rstride=2, cstride=5,   # 根据数据密度调整
            antialiased=True, edgecolor='none'
            )
        cbar = fig.colorbar(surf1, ax=ax, shrink=0.7, pad=0.05)

        # ===================== label fonts =====================
        ax.set_xlabel('Angle (rad)', fontweight='bold')
        ax.set_ylabel('Modulation Index', fontweight='bold')
        ax.set_zlabel('Zero-sequence Voltage (p.u.)', fontweight='bold')
        ax.set_box_aspect(None, zoom=0.95)

        # ===================== X axis label =====================
        xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$',r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')
        
        plt.show()

if __name__ == "__main__":
    ClassTest = threephase3D()
    ClassTest.data3D_Cal()
    ClassTest.data3D_plot()