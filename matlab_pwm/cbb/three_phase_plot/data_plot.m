function data_plot(self, varargin)
% DATA_PLOT  Plot three-phase voltage waveforms against self.wt.
%   Equivalent to Python `ThreePhaseVoltage.data_plot` (tp_voltage.py).
%   Each extra input is plotted as a curve over self.wt.
%
%   Example: data_plot(self, self.Va, self.Vb, self.Vc, vzs_max, vzs_min)

pic_size = [7, 4.3];

% global font settings (mirrors plt.rcParams in the Python source)
set(groot, 'defaultAxesFontName', 'Times New Roman');

figure('Units', 'inches', 'Position', [2 2 pic_size(1) pic_size(2)]);
ax = axes;
hold(ax, 'on');

% plot every passed curve
for k = 1:numel(varargin)
    plot(ax, self.wt, varargin{k}, 'LineWidth', 2.0);
end

% tick label font size / weight
set(ax, 'FontSize', 12, 'FontWeight', 'bold');

xlabel(ax, '\theta (rad)', 'FontSize', 14, 'FontWeight', 'bold');
ylabel(ax, 'Voltage (p.u.)', 'FontSize', 14, 'FontWeight', 'bold');
xlim(ax, [0, self.wt(end)]);
grid(ax, 'on');
ax.GridLineStyle = '--';
ax.GridAlpha = 0.3;
end
