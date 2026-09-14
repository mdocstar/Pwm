function [vzs_max, vzs_min] = vzs_limit_calculate(self)
% VZS_LIMIT_CALCULATE  Zero-sequence voltage limitation.
%   Equivalent to Python `ThreePhaseVoltage.vzs_limit_calculate` (tp_voltage.py).

Va = self.Va; Vb = self.Vb; Vc = self.Vc;

umax = max(Va, max(Vb, Vc));
umin = min(Va, min(Vb, Vc));

vzs_max = min(1 - umax, -umin);
vzs_min = max(-1 - umin, -umax);
end
