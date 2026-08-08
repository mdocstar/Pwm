import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import matplotlib.pyplot as plt
from python_pwm.pod_pd_pwm.pd1_cmv  import Pd1_cmv
from python_pwm.pod_pd_pwm.pd2_cmv  import Pd2_cmv
from python_pwm.pod_pd_pwm.pod1_cmv import Pod1_cmv
from python_pwm.pod_pd_pwm.pod2_cmv import Pod2_cmv

class PdPodmodu:
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
            inst.cmv_proportion_modu()
        
    def data_2d_plot(self, pic_size=(10, 6.5)):
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["axes.unicode_minus"] = False
        plt.rcParams['mathtext.fontset'] = 'stix'

        fig = plt.figure(figsize=pic_size, layout='constrained')
        axes_dict = fig.subplot_mosaic([
            ['left', 'right_top'],
            ['left', 'right_bottom']
        ])
    
        # 按需要的顺序获取axes
        axes_list = [axes_dict['left'], axes_dict['right_top'], axes_dict['right_bottom']]
        colors = {'PD-I': '#4472C4', 'PD-II': '#ED7D31', 'POD-I': '#70AD47', 'POD-II': '#A855F7'}

        ylabels = [
            'Total Low-CMV Area Proportion (%)',
            'Upper Low-CMV Area Proportion (%)',
            'Lower Low-CMV Area Proportion (%)',
        ]
        data_keys = ['cmv_in_modu', 'up_cmv_in_modu', 'down_cmv_in_modu']

        for ax, ylabel, data_key in zip(axes_list, ylabels, data_keys):
            for label, inst in self.variants.items():
                ax.plot(inst.modulation_3d, getattr(inst, data_key),
                color=colors[label], linewidth=1.2, label=label)
            
            ax.set_xlabel('Modulation Index', fontweight='bold', fontsize=11)
            ax.set_ylabel(ylabel, fontweight='bold', fontsize=11)
            ax.set_xlim(0, inst.modulation_3d[-1])
            ax.legend(loc='best', fontsize=9)
            ax.grid(linestyle='--', alpha=0.3, color='#7F7F7F')
            ax.tick_params(labelsize=10)

        fig.suptitle('Low Common-Mode Voltage Area Proportion with Modulation Index',
                 fontweight='bold', fontsize=14)
        plt.show()

if __name__ == "__main__":
    plotter = PdPodmodu()
    plotter.data_2d_plot()
