function figure_plot(self, pic_size)
% FIGURE_PLOT  Plot the CMV zero-sequence voltages with VPOD/VPD bands.
%   Equivalent to Python `ThreePhaseVoltageCMV.figure_plot`.

if nargin < 2 || isempty(pic_size), pic_size = [7, 4.2]; end

set(groot, 'defaultAxesFontName', 'Times New Roman');

figure('Units', 'inches', 'Position', [2 2 pic_size(1) pic_size(2)]);
ax = axes;
hold(ax, 'on');

% #FFE699, #D3ECB9, #FF9999, #A099FF
plot(ax, self.angle, self.vz_max,  'Color', [255 230 153]/255, 'LineWidth', 2);
plot(ax, self.angle, self.vz_min,  'Color', [211 236 185]/255, 'LineWidth', 2);
plot(ax, self.angle, self.vzs_sv,  'Color', [255 153 153]/255, 'LineWidth', 2);
plot(ax, self.angle, self.vzs_zcd, 'Color', [160 153 255]/255, 'LineWidth', 2);

set(ax, 'FontSize', 8, 'FontWeight', 'bold');
xlabel(ax, 'Angle (rad)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel(ax, 'zero-sequence Voltage (p.u.)', 'FontSize', 14, 'FontWeight', 'bold');
xlim(ax, [0, self.angle(end)]);
grid(ax, 'on');
ax.GridLineStyle = '--';
ax.GridAlpha = 0.3;
ax.GridColor = [127 127 127]/255;   % #7F7F7F

xticks      = [0, pi/2, pi, 3*pi/2, 2*pi];
xtick_labels = {'0', '\pi/2', '\pi', '3\pi/2', '2\pi'};
set(ax, 'XTick', xticks, 'XTickLabel', xtick_labels, 'FontSize', 14, 'FontWeight', 'bold');

% VPOD band (#96EBFE)
fill_between(ax, self.angle, self.vpod_max, self.vpod_min, [150 235 254]/255, 0.3);
% VPD bands (#666666) — NaN gaps handled by fill_between
fill_between(ax, self.angle, self.vpd_max1, self.vpd_min1, [102 102 102]/255, 0.3);
fill_between(ax, self.angle, self.vpd_max2, self.vpd_min2, [102 102 102]/255, 0.3);
end
