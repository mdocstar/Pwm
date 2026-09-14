%% DEMO: reproduce three_phase_3d.py __main__
clc, clear, close all

self = three_phase_3d();
self = data_3d_calculate(self);
data_3d_plot(self);
