import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseDOne:
    def __init__(self, mi):
        ##### set modulation index limitation 0~2/sqrt(3)
        mi = max(0, mi)
        mi = min(2 / np.sqrt(3), mi)
        self.modulation_index = mi

        ##### calculate three-phase voltage according to voltage max/mid/min division
        self.wt = np.linspace(0, 2 * np.pi / 3, 10000)
        self.umax = self.modulation_index * np.sin(self.wt + np.pi / 6)
        self.umid = np.zeros_like(self.wt)
        self.umin = np.zeros_like(self.wt)

        division_cave = np.pi / 3
        division1 = self.wt < division_cave
        self.umid[division1] = self.modulation_index * np.sin(self.wt[division1] + 5 * np.pi / 6)
        self.umin[division1] = self.modulation_index * np.sin(self.wt[division1] - np.pi / 2)

        division2 = self.wt >= division_cave
        self.umid[division2] = self.modulation_index * np.sin(self.wt[division2] - np.pi / 2)
        self.umin[division2] = self.modulation_index * np.sin(self.wt[division2] + 5 * np.pi / 6)
        
        ##### calculate zero-sequence voltage limitation
        self.Vzs_max = np.minimum(1 - self.umax,-self.umin)
        self.Vzs_min = np.maximum(-1 - self.umin,-self.umax)
        
    def three_phase_plt(self, picsize=(7, 4.2)):
        plt.rcParams["font.family"] = "Times New Roman"  # 设置全局西文字体为 Times New Roman
        plt.rcParams["axes.unicode_minus"] = False       # 解决负号显示为方块的问题
        plt.rcParams['mathtext.fontset'] = 'stix'  # 让数学符号也匹配 Times 风格

        fig, ax = plt.subplots(figsize=picsize, layout='constrained')
        xticks = [0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3]
        xtick_labels = [r'$0$', r'$\pi/6$', r'$\pi/3$', r'$\pi/2$',r'$2\pi/3$']

        #### three-phase voltage plot
        ax.plot(self.wt, self.umax, label='Phase Voltage Umax', color='#FFE699')
        ax.plot(self.wt, self.umid, label='Phase Voltage Umid', color='#D3ECB9')
        ax.plot(self.wt, self.umin, label='Phase Voltage Umin', color='#FF9999')
        ax.plot(self.wt, self.Vzs_max, label='Zero-sequence voltage maximum', color='#0072BD',linestyle='--')
        ax.plot(self.wt, self.Vzs_min, label='Zero-sequence voltage minimum', color='#D95319',linestyle='--')
        ax.set_title(f'Three-Phase Voltage Waveforms (Modulation Index = {self.modulation_index})',fontweight='bold')
        ax.set_xlabel('Angle (rad)',fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)',fontweight='bold')
        ax.set_xlim(0, self.wt[-1])
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels, fontsize=12, fontweight='bold')
        ax.legend(loc = 'upper right',fontsize=8)
        ax.grid(linestyle='--', alpha=0.3)
        
        plt.show()

if __name__ == "__main__":
    mod_idx = 0.90  # Example modulation index
    class_three_phase_voltage = ThreePhaseDOne(mod_idx)
    class_three_phase_voltage.three_phase_plt()