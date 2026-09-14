function vzs_sv = vzs_sv_calculate(self)
% VZS_SV_CALCULATE  Zero-sequence voltage via the space-vector (SV) method.
%   vzs_sv = -0.5 * (Vmax + Vmin), the common-mode voltage injected in
%   standard space-vector PWM.
%   Equivalent to Python `ThreePhaseVoltage.vzs_sv_calculate` (tp_voltage.py).

Va = self.Va; Vb = self.Vb; Vc = self.Vc;

vmax_arr = max(Va, max(Vb, Vc));
vmin_arr = min(Va, min(Vb, Vc));

vzs_sv = -0.5 * (vmax_arr + vmin_arr);
end
