function self = three_phase_voltage(mi, frequency, start_angle, time)
%   THREE_PHASE_VOLTAGE  Initialize a three-phase voltage "object" (struct).
%   Equivalent to Python `ThreePhaseVoltage.__init__` (tp_voltage.py).
%
%   self = three_phase_voltage(mi, frequency, start_angle, time)
%
%   Defaults: mi = 0.90, frequency = 50, start_angle = 0, time = 0.02

if nargin < 1 || isempty(mi),          mi          = 0.90; end
if nargin < 2 || isempty(frequency),   frequency   = 50;   end
if nargin < 3 || isempty(start_angle), start_angle = 0;    end
if nargin < 4 || isempty(time),        time        = 0.02; end

% Initialize all fields (mirrors the Python __init__ attribute list)
self.modulation_index = [];
self.wt           = [];
self.start_angle  = [];
self.Va           = [];
self.Vb           = [];
self.Vc           = [];
self.vzs_sv       = [];
self.vzs_zcd      = [];

% Delegate to data_reset (mirrors the Python __init__ -> data_reset call)
self = data_reset(self, mi, frequency, start_angle, time);
end
