function [vmax, vmin, vmid] = v_max_min_calculate(self)
% V_MAX_MIN_CALCULATE  Maximum / minimum / middle of the three-phase voltages.
%   Equivalent to Python `ThreePhaseVoltage.v_max_min_calculate` (tp_voltage.py).

Va = self.Va; Vb = self.Vb; Vc = self.Vc;

vmax = max(Va, max(Vb, Vc));
vmin = min(Va, min(Vb, Vc));
vmid = Va + Vb + Vc - vmax - vmin;
end
