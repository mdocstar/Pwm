####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, modulation_index):
        self.modulation_index = modulation_index

        self.time = np.linspace(0, 0.02, 10000)  # 50 Hz fundamental frequency
        self.angle = self.time * 2 * np.pi * 50  # Phase angle over time
        self.degree = self.angle * 180 / np.pi   
        self.start_anlge = 0 # Starting phase angle
        self.Va = []
        self.Vb = []
        self.Vc = []
        self.Vzmax = []
        self.Vzmin = []
        self.Vzs_SV = []
        self.Vzs_ZCD = np.zeros_like(self.time)
        
        self.VPOD_max = np.zeros_like(self.time)
        self.VPOD_min = np.zeros_like(self.time)
        self.VPD_max1 = np.zeros_like(self.time)
        self.VPD_min1 = np.zeros_like(self.time)
        self.VPD_max2 = np.zeros_like(self.time)
        self.VPD_min2 = np.zeros_like(self.time)
        self.Ymax = 1.3
        self.Ymin = -self.Ymax
        
    def calculate_voltages(self):
        self.Va = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + self.start_anlge)
        self.Vb = self.modulation_index * np.sin(2 * np.pi * 50 * self.time - 2 * np.pi / 3 + self.start_anlge)
        self.Vc = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + 2 * np.pi / 3 + self.start_anlge)
        Vmax = np.maximum(self.Va, np.maximum(self.Vb, self.Vc))
        Vmin = np.minimum(self.Va, np.minimum(self.Vb, self.Vc))
        Vmid = self.Va + self.Vb + self.Vc - Vmax - Vmin
        self.Vzmax = np.minimum(1 - Vmax, -Vmin)
        self.Vzmin = np.maximum(-1 - Vmin, -Vmax)
        self.Vzs_SV = -0.5 * (Vmax + Vmin)
        self.VPOD_max = np.minimum(self.Vzmax,0.5 * Vmax)
        self.VPOD_min = np.maximum(self.Vzmin,0.5 * Vmin)
        
        for i in range(len(self.Va)):
            if (1 + Vmin[i]) <= Vmid[i]:
                self.VPD_max1[i] = self.Vzmax[i]
                self.VPD_min1[i] = np.maximum(self.Vzmin[i],-Vmid[i])
            else:
                self.VPD_max1[i] = np.nan
                self.VPD_min1[i] = np.nan
                
        for i in range(len(self.Va)):
            if (1 + Vmid[i]) <= Vmax[i]:
                self.VPD_max2[i] = np.minimum(self.Vzmax[i],-Vmid[i])
                self.VPD_min2[i] = self.Vzmin[i]
            else:
                self.VPD_max2[i] = np.nan
                self.VPD_min2[i] = np.nan


        for i in range(len(self.Va)):
            # 取出当前点的三相电压
            va = self.Va[i]
            vb = self.Vb[i]
            vc = self.Vc[i]
            
            Vmax = max(va, vb, vc)
            Vmin = min(va, vb, vc)
            Vmid = va + vb + vc - Vmax - Vmin  # middle voltage
            Vmid = -Vmid

            # 判断符号（核心逻辑和你原来完全一致）
            if np.sign(va) == np.sign(vb):
                self.Vzs_ZCD[i] = np.sign(vc) - vc
            elif np.sign(va) == np.sign(vc):
                self.Vzs_ZCD[i] = np.sign(vb) - vb
            else:
                self.Vzs_ZCD[i] = np.sign(va) - va
            
            if abs(self.Vzs_ZCD[i]) <= abs(Vmid):
                self.Vzs_ZCD[i] = self.Vzs_ZCD[i]
            else:
                self.Vzs_ZCD[i] = Vmid

    def fig_plot(self,Picsize=(7, 4.2)):
        plt.rcParams["font.family"] = "Times New Roman"  # set global font to Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # solve the problem of negative sign display as a square
        plt.rcParams['mathtext.fontset'] = 'stix'  # set math font to match Times style
        
        fig,ax = plt.subplots(figsize=Picsize, layout='constrained')
        
        ax.plot(self.angle, self.Vzmax, color='#FFE699',linewidth=2)
        ax.plot(self.angle, self.Vzmin, color='#D3ECB9',linewidth=2)
        ax.plot(self.angle, self.Vzs_SV, color='#FF9999',linewidth=2)
        ax.plot(self.angle, self.Vzs_ZCD, color="#A099FF",linewidth=2)

        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(8)  # fontsize
            label.set_fontweight('bold')  # font weight bold
        ax.set_xlabel('Angle (rad)',fontsize=14,fontweight='bold')
        ax.set_ylabel('zero-sequence Voltage (p.u.)',fontsize=14,fontweight='bold')
        ax.tick_params(axis='y', labelsize=14)
        ax.set_xlim(0, self.angle[-1])
        ax.grid(linestyle='--', alpha=0.3)

        xticks = [0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]
        xtick_labels = [r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$',r'$2\pi$']
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=14, fontweight='bold')
        
        ax.fill_between(
            self.angle,  # X轴范围
            self.VPOD_max,          # 下方边界（X轴，y=0）
            self.VPOD_min,          # 上方边界（曲线y=sin(x)）
            where=None,  # 指定填充范围：x在2到6之间
            color="#96EBFE",          # 填充颜色
            alpha=0.3,                  # 透明度（避免遮挡曲线）
            label=None             # 图例标签
        )
        
        ax.fill_between(
            self.angle,  # X轴范围
            self.VPD_max1,          # 下方边界（X轴，y=0）
            self.VPD_min1,          # 上方边界（曲线y=sin(x)）
            where=None,  # 指定填充范围：x在2到6之间
            color="#666666",          # 填充颜色
            alpha=0.3,                  # 透明度（避免遮挡曲线）
            label=None             # 图例标签
        )
        
        ax.fill_between(
            self.angle,  # X轴范围
            self.VPD_max2,          # 下方边界（X轴，y=0）
            self.VPD_min2,          # 上方边界（曲线y=sin(x)）
            where=None,  # 指定填充范围：x在2到6之间
            color="#666666",          # 填充颜色
            alpha=0.3,                  # 透明度（避免遮挡曲线）
            label=None             # 图例标签
        )
                
        plt.show()
        
if __name__ == "__main__":
    modulation_index = 0.90  # Example modulation index
    ClassThreePhaseVoltage = ThreePhaseVoltage(modulation_index)
    ClassThreePhaseVoltage.calculate_voltages()
    ClassThreePhaseVoltage.fig_plot()
