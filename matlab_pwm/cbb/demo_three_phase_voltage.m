%% DEMO: reproduce tp_voltage.py __main__
clc, clear, close all

modulation_index = 0.90;

self = three_phase_voltage(modulation_index);
[vzs_max, vzs_min] = vzs_limit_calculate(self);
data_plot(self, self.Va, self.Vb, self.Vc, vzs_max, vzs_min);
