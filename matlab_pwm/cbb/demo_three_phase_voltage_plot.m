%% DEMO: reproduce three_phase_voltage_plot.py __main__
clc, clear, close all

modulation_index = 0.85;

self = three_phase_voltage_plot(modulation_index);
three_voltage_plot(self);
