function self = calculate_voltages(self)
% CALCULATE_VOLTAGES  Compute all CMV-specific voltage arrays.
%   Equivalent to Python `ThreePhaseVoltageCMV.calculate_voltages`.

% three-phase voltages using the CMV-specific time base
self.Va = self.modulation_index * sin(2 * pi * 50 * self.time + self.start_angle);
self.Vb = self.modulation_index * sin(2 * pi * 50 * self.time - 2 * pi / 3 + self.start_angle);
self.Vc = self.modulation_index * sin(2 * pi * 50 * self.time + 2 * pi / 3 + self.start_angle);

vmax_arr = max(self.Va, max(self.Vb, self.Vc));
vmin_arr = min(self.Va, min(self.Vb, self.Vc));
vmid_arr = self.Va + self.Vb + self.Vc - vmax_arr - vmin_arr;

% zero-sequence voltage limitation (base-class method)
[self.vz_max, self.vz_min] = vzs_limit_calculate(self);

% space-vector and zero-crossing-detection zero-sequence voltages
self.vzs_sv  = vzs_sv_calculate(self);
self.vzs_zcd = vzs_zcd_calculate(self);

% VPOD (Phase Opposition Disposition) limits
self.vpod_max = min(self.vz_max, 0.5 * vmax_arr);
self.vpod_min = max(self.vz_min, 0.5 * vmin_arr);

% VPD (Phase Disposition) limits, case 1
for i = 1:numel(self.Va)
    if (1 + vmin_arr(i)) <= vmid_arr(i)
        self.vpd_max1(i) = self.vz_max(i);
        self.vpd_min1(i) = max(self.vz_min(i), -vmid_arr(i));
    else
        self.vpd_max1(i) = NaN;
        self.vpd_min1(i) = NaN;
    end
end

% VPD (Phase Disposition) limits, case 2
for i = 1:numel(self.Va)
    if (1 + vmid_arr(i)) <= vmax_arr(i)
        self.vpd_max2(i) = min(self.vz_max(i), -vmid_arr(i));
        self.vpd_min2(i) = self.vz_min(i);
    else
        self.vpd_max2(i) = NaN;
        self.vpd_min2(i) = NaN;
    end
end
end
