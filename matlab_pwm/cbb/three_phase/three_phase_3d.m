function self = three_phase_3d()
% THREE_PHASE_3D  Initialize the 3D surface-plot object.
%   Equivalent to Python `ThreePhase3D.__init__` (three_phase_3d.py).

self = three_phase_voltage(0.90);   % super().__init__(mi=0.90)

self.modulation_3d = linspace(0, 2 / sqrt(3), 1000);
length_modu = numel(self.modulation_3d);
length_wt   = numel(self.wt);

self.X            = zeros(length_modu, length_wt);
self.Y            = zeros(length_modu, length_wt);
self.vz_max_3d    = zeros(length_modu, length_wt);
self.vz_min_3d    = zeros(length_modu, length_wt);
self.v_mid        = zeros(length_modu, length_wt);
self.v_max        = zeros(length_modu, length_wt);
self.v_min        = zeros(length_modu, length_wt);
self.one_plus_min = zeros(length_modu, length_wt);
self.one_minus_max = zeros(length_modu, length_wt);
self.vzs_division = zeros(length_modu, length_wt);
end
