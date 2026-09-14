%% DEMO: reproduce three_phase_voltage_cmv.py __main__
clc, clear, close all

modulation_index = 0.90;

self = three_phase_voltage_cmv(modulation_index);
self = calculate_voltages(self);
figure_plot(self);
