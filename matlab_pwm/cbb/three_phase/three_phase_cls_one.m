function self = three_phase_cls_one(mi)
% THREE_PHASE_CLS_ONE  Initialize a single-sector three-phase voltage object.
%   Equivalent to Python `ThreePhaseClsOne.__init__` (three_phase_cls_one.py).
%
%   Note: the passed `mi` is ignored — the Python __init__ hard-codes
%   super().__init__(mi=1.15), so the modulation index is always 1.15.

if nargin < 1 || isempty(mi), mi = 1.15; end

% base init with fixed mi = 1.15 (mirrors super().__init__(mi=1.15))
self = three_phase_voltage(1.15);

% override: ClsOne only covers one sector (0 ~ 2*pi/3)
self.wt = linspace(0, 2 * pi / 3, 1000);
wt = self.wt;

% three-phase voltage according to voltage max/mid/min division
self.umax = self.modulation_index * sin(wt + pi / 6);
self.umid = zeros(size(wt));
self.umin = zeros(size(wt));

division_curve = pi / 3;
division1 = wt < division_curve;
division2 = wt >= division_curve;

self.umid(division1) = self.modulation_index * sin(wt(division1) + 5 * pi / 6);
self.umin(division1) = self.modulation_index * sin(wt(division1) - pi / 2);

self.umid(division2) = self.modulation_index * sin(wt(division2) - pi / 2);
self.umin(division2) = self.modulation_index * sin(wt(division2) + 5 * pi / 6);

% set Va/Vb/Vc from umax/umid/umin so base-class methods can operate on them
self.Va = self.umax;
self.Vb = self.umid;
self.Vc = self.umin;

% zero-sequence voltage limitation (base-class method)
[self.vzs_max, self.vzs_min] = vzs_limit_calculate(self);
end
