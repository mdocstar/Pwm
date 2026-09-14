function three_voltage_plot(self, pic_size)
% THREE_VOLTAGE_PLOT  Plot three-phase voltages with sector fills.
%   Equivalent to Python `ThreePhaseVoltagePlot.three_voltage_plot`.

if nargin < 2 || isempty(pic_size), pic_size = [7, 4.3]; end

set(groot, 'defaultAxesFontName', 'Times New Roman');

figure('Units', 'inches', 'Position', [2 2 pic_size(1) pic_size(2)]);
ax = axes;
hold(ax, 'on');

% tick label font size / weight
set(ax, 'FontSize', self.grid_labels_fontsize, 'FontWeight', 'bold');

plot(ax, self.angle, self.Va, 'r', 'DisplayName', 'Phase A Voltage');
plot(ax, self.angle, self.Vb, 'g', 'DisplayName', 'Phase B Voltage');
plot(ax, self.angle, self.Vc, 'b', 'DisplayName', 'Phase C Voltage');

title(ax, sprintf('Three-Phase Voltage Waveforms (Modulation Index = %.2f)', self.modulation_index), 'FontWeight', 'bold');
xlabel(ax, 'Angle (rad)', 'FontSize', self.xy_labels_fontsize, 'FontWeight', 'bold');
ylabel(ax, 'Voltage (p.u.)', 'FontSize', self.xy_labels_fontsize, 'FontWeight', 'bold');
xlim(ax, [0, self.angle(end)]);
ylim(ax, [self.y_min, self.y_max]);

legend(ax, 'Location', 'northeast', 'FontSize', self.legend_fontsize);
grid(ax, 'on');
ax.GridLineStyle = '--';
ax.GridAlpha = 0.3;

% fill sectors with different colors
sector_list   = linspace(0, 4 * pi, 7);
sector_color  = {[254 191 150]/255, [211 236 185]/255, [211 255 254]/255};  % #FEBF96, #D3ECB9, #D3FFFE
sector_labels = {'Sector I', 'Sector II', 'Sector III'};
for i = 1:numel(sector_list) - 1
    x_start = sector_list(i);
    x_end   = sector_list(i + 1);
    fill_sector(self, ax, x_start, x_end, ...
        sector_color{mod(i - 1, numel(sector_color)) + 1}, ...
        sector_labels{mod(i - 1, numel(sector_labels)) + 1});
end
end
