####### This file is aimed at plotting the three-phase voltage waveforms
####### for a given modulation index and phase angle from 0~2 pi.
import numpy as np
import matplotlib.pyplot as plt

class ThreePhaseVoltage:
    def __init__(self, mi):
        self.modulation_index = mi
        self.XYlabels = ['Time (s)', 'Voltage (p.u.)']
        self.XYlabels_fontsize = 14
        self.Gridlabels_fontsize = 12
        self.legend_fontsize = 14

        self.time = np.linspace(0, 0.04, 10000)  # 50 Hz fundamental frequency
        self.angle = self.time * 2 * np.pi * 50  # Phase angle over time
        self.degree = self.angle * 180 / np.pi   
        self.start_anlge = np.pi / 6 # Starting phase angle
        self.Va = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + self.start_anlge)
        self.Vb = self.modulation_index * np.sin(2 * np.pi * 50 * self.time - 2 * np.pi / 3 + self.start_anlge)
        self.Vc = self.modulation_index * np.sin(2 * np.pi * 50 * self.time + 2 * np.pi / 3 + self.start_anlge)
        self.Ymax = 1.3
        self.Ymin = -self.Ymax

    def fill_sector(self,ax, x_start, x_end, **parameters):
        if 'color' in parameters:
            func_color = parameters['color']
        else:
            func_color = 'lightblue'
            
        if 'label' in parameters:
            func_label = parameters['label']
        else:
            func_label = None
        
        ax.fill_between(
            np.linspace(x_start, x_end, 1000),  # X轴范围
            self.Ymin,          # 下方边界（X轴，y=0）
            self.Ymax,          # 上方边界（曲线y=sin(x)）
            where=None,  # 指定填充范围：x在2到6之间
            color=func_color,          # 填充颜色
            alpha=0.3,                  # 透明度（避免遮挡曲线）
            label=func_label             # 图例标签
        )
        
        ax.text(
            0.5 * (x_start + x_end),     # 填充区域中心X坐标
            -1.10,                        # 填充区域中心坐标
            func_label,                # 文字内容
            fontsize=12,                 # 文字大小
            fontweight='bold',           # 加粗
            ha='center',                 # 水平居中
            va='center',                 # 垂直居中
            color='#000000',            # 文字颜色（与曲线呼应，提升美观度）
            # 可选：添加白色背景框，避免文字被填充色遮挡
            # bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none')
        )
        
    def three_voltage_plot(self, picsize=(7, 4.3)):
        plt.rcParams["font.family"] = "Times New Roman"  # 设置全局西文字体为 Times New Roman
        plt.rcParams["axes.unicode_minus"] = False        # 解决负号显示为方块的问题
        fig, ax = plt.subplots(figsize=picsize, layout='constrained')
        
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontsize(self.Gridlabels_fontsize)  # 10号字体
            label.set_fontweight('bold')  # 字体加粗
            
        ax.plot(self.angle, self.Va, label='Phase A Voltage', color='r')
        ax.plot(self.angle, self.Vb, label='Phase B Voltage', color='g')
        ax.plot(self.angle, self.Vc, label='Phase C Voltage', color='b')
        ax.set_title(f'Three-Phase Voltage Waveforms (Modulation Index = {self.modulation_index})', fontweight='bold')
        ax.set_xlabel('Angle (rad)',fontsize = self.XYlabels_fontsize,fontweight='bold')
        ax.set_ylabel('Voltage (p.u.)',fontsize = self.XYlabels_fontsize,fontweight='bold')
        ax.set_xlim(0, self.angle[-1])
        ax.set_ylim(self.Ymin, self.Ymax)
    
        ax.legend(loc = 'upper right',fontsize=self.legend_fontsize)
        ax.grid(linestyle='--', alpha=0.3)
        
        '''
        # Fill sectors with different colors
        '''
        sector_list = np.linspace(0, 4 * np.pi, 7)
        sector_color = ["#FEBF96", '#D3ECB9', '#D3FFFE']
        sector_labels = ['Sector I', 'Sector II', 'Sector III']
        for i in range(len(sector_list)-1):
            x_start = sector_list[i]
            x_end = sector_list[i+1]
            self.fill_sector(ax, x_start, x_end, color=sector_color[i % len(sector_color)],label=sector_labels[i % len(sector_labels)])
        
        plt.show()
            
if __name__ == "__main__":
    mod_idx = 0.85  # Example modulation index
    class_three_phase_voltage = ThreePhaseVoltage(mod_idx)
    class_three_phase_voltage.three_voltage_plot()