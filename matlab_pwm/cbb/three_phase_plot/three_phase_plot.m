function three_phase_plot(self, pic_size)
% THREE_PHASE_PLOT  Plot three-phase voltage waveforms (single sector).
%   Equivalent to Python `ThreePhaseClsOne.three_phase_plot`.

if nargin < 2 || isempty(pic_size), pic_size = [10, 7.0]; end

set(groot, 'defaultAxesFontName', 'Times New Roman');

figure('Units', 'inches', 'Position', [2 2 pic_size(1) pic_size(2)]);
ax = axes;
hold(ax, 'on');

xticks      = [0, pi/6, pi/3, pi/2, 2*pi/3];
xtick_labels = {'0', '\pi/6', '\pi/3', '\pi/2', '2\pi/3'};

% #FFE699, #D3ECB9, #FF9999, #0072BD, #D95319
plot(ax, self.wt, self.umax, 'Color', [255 230 153]/255, 'DisplayName', 'Phase Voltage Umax');
plot(ax, self.wt, self.umid, 'Color', [211 236 185]/255, 'DisplayName', 'Phase Voltage Umid');
plot(ax, self.wt, self.umin, 'Color', [255 153 153]/255, 'DisplayName', 'Phase Voltage Umin');
plot(ax, self.wt, self.vzs_max, '--', 'Color', [0 114 189]/255, 'DisplayName', 'Zero-sequence voltage maximum');
plot(ax, self.wt, self.vzs_min, '--', 'Color', [217 83 25]/255, 'DisplayName', 'Zero-sequence voltage minimum');

title(ax, sprintf('Three-Phase Voltage Waveforms (Modulation Index = %.2f)', self.modulation_index), 'FontWeight', 'bold');
xlabel(ax, 'Angle (rad)', 'FontWeight', 'bold');
ylabel(ax, 'Voltage (p.u.)', 'FontWeight', 'bold');
xlim(ax, [0, self.wt(end)]);

set(ax, 'XTick', xticks, 'XTickLabel', xtick_labels, 'FontSize', 12, 'FontWeight', 'bold');
legend(ax, 'Location', 'northeast', 'FontSize', 8);
grid(ax, 'on');
ax.GridLineStyle = '--';
ax.GridAlpha = 0.3;
ax.GridColor = [127 127 127]/255;   % #7F7F7F
end
