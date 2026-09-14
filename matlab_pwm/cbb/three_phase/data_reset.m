function self = data_reset(self, mi, frequency, start_angle, time)
% DATA_RESET  Reset the three-phase voltage parameters.
%   Equivalent to Python `ThreePhaseVoltage.data_reset` (tp_voltage.py).

if nargin < 2 || isempty(mi),          mi          = 0.90; end
if nargin < 3 || isempty(frequency),   frequency   = 50;   end
if nargin < 4 || isempty(start_angle), start_angle = 0;    end
if nargin < 5 || isempty(time),        time        = 0.02; end

% Clamp modulation index to [0, 2/sqrt(3)]  (np: mi = max(0, min(2/sqrt(3), mi)))
mi = max(0, mi);
mi = min(2 / sqrt(3), mi);
self.modulation_index = mi;

% Angle array: wt = linspace(0, 2*pi*frequency*time, 1000)
self.wt = linspace(0, 2 * pi * frequency * time, 1000);
self.start_angle = start_angle;

self.Va = self.modulation_index * sin(self.wt + self.start_angle);
self.Vb = self.modulation_index * sin(self.wt - 2 * pi / 3 + self.start_angle);
self.Vc = self.modulation_index * sin(self.wt + 2 * pi / 3 + self.start_angle);
self.vzs_sv  = [];
self.vzs_zcd = [];
end
