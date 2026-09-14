function self = three_phase_voltage_plot(mi)
% THREE_PHASE_VOLTAGE_PLOT  Initialize the plot-specific object.
%   Equivalent to Python `ThreePhaseVoltagePlot.__init__` (three_phase_voltage_plot.py).

if nargin < 1 || isempty(mi), mi = 0.85; end

self = three_phase_voltage(mi);   % super().__init__(mi=mi)

% plot-specific display / time settings
self.xy_labels           = {'Time (s)', 'Voltage (p.u.)'};
self.xy_labels_fontsize  = 14;
self.grid_labels_fontsize = 12;
self.legend_fontsize     = 14;

self.time  = linspace(0, 0.04, 10000);   % 50 Hz fundamental frequency
self.angle = self.time * 2 * pi * 50;    % phase angle over time
self.degree = self.angle * 180 / pi;
self.start_angle = pi / 6;               % starting phase angle

% recalculate Va/Vb/Vc with plot-specific time base and start angle
self.Va = self.modulation_index * sin(2 * pi * 50 * self.time + self.start_angle);
self.Vb = self.modulation_index * sin(2 * pi * 50 * self.time - 2 * pi / 3 + self.start_angle);
self.Vc = self.modulation_index * sin(2 * pi * 50 * self.time + 2 * pi / 3 + self.start_angle);

self.y_max = 1.3;
self.y_min = -self.y_max;
end
