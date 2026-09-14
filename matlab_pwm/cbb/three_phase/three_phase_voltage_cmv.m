function self = three_phase_voltage_cmv(mi)
% THREE_PHASE_VOLTAGE_CMV  Initialize the CMV-specific object.
%   Equivalent to Python `ThreePhaseVoltageCMV.__init__` (three_phase_voltage_cmv.py).

if nargin < 1 || isempty(mi), mi = 0.90; end

self = three_phase_voltage(mi);   % super().__init__(mi=mi)

% CMV-specific time / angle arrays (higher resolution)
self.time  = linspace(0, 0.02, 10000);   % 50 Hz fundamental frequency
self.angle = self.time * 2 * pi * 50;    % phase angle over time
self.degree = self.angle * 180 / pi;
self.start_angle = 0;

% CMV-specific voltage arrays for VPOD / VPD
self.vz_max    = [];
self.vz_min    = [];
self.vpod_max  = zeros(size(self.time));
self.vpod_min  = zeros(size(self.time));
self.vpd_max1  = zeros(size(self.time));
self.vpd_min1  = zeros(size(self.time));
self.vpd_max2  = zeros(size(self.time));
self.vpd_min2  = zeros(size(self.time));
self.y_max = 1.3;
self.y_min = -self.y_max;
end
