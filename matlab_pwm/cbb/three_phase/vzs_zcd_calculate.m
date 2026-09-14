function vzs_zcd = vzs_zcd_calculate(self)
% VZS_ZCD_CALCULATE  Zero-sequence voltage via zero-crossing detection (ZCD).
%   Equivalent to Python `ThreePhaseVoltage.vzs_zcd_calculate` (tp_voltage.py).

Va = self.Va; Vb = self.Vb; Vc = self.Vc;
n = numel(Va);
vzs_zcd = zeros(size(Va));

for i = 1:n
    va = Va(i); vb = Vb(i); vc = Vc(i);

    vmax = max([va vb vc]);
    vmin = min([va vb vc]);
    vmid = va + vb + vc - vmax - vmin;
    vmid = -vmid;

    if sign(va) == sign(vb)
        vzs_zcd(i) = sign(vc) - vc;
    elseif sign(va) == sign(vc)
        vzs_zcd(i) = sign(vb) - vb;
    else
        vzs_zcd(i) = sign(va) - va;
    end

    if abs(vzs_zcd(i)) > abs(vmid)
        vzs_zcd(i) = vmid;
    end
end
end
