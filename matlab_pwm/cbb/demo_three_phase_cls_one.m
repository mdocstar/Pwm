%% DEMO: reproduce three_phase_cls_one.py __main__
clc, clear, close all

modulation_index = 0.90;   % note: ignored — ThreePhaseClsOne hard-codes mi = 1.15
self = three_phase_cls_one(modulation_index);
three_phase_plot(self);
