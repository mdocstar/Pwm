function self = data_3d_calculate(self)
% DATA_3D_CALCULATE  Build the 3D data grids over wt x modulation index.
%   Equivalent to Python `ThreePhase3D.data_3d_calculate`.

len_wt = numel(self.wt);

for i = 1:size(self.X, 1)
    self = data_reset(self, self.modulation_3d(i));   % update Va/Vb/Vc
    [self.vz_max_3d(i, :), self.vz_min_3d(i, :)] = vzs_limit_calculate(self);
    [self.v_max(i, :), self.v_min(i, :), self.v_mid(i, :)] = v_max_min_calculate(self);
    self.one_plus_min(i, :)  = 1 + self.v_min(i, :);
    self.one_minus_max(i, :) = 1 - self.v_max(i, :);

    for j = 1:len_wt
        self.X(i, j) = self.wt(j);
        self.Y(i, j) = self.modulation_3d(i);

        if -self.v_mid(i, j) >= self.vz_min_3d(i, j) && -self.v_mid(i, j) <= self.vz_max_3d(i, j)
            self.vzs_division(i, j) = -self.v_mid(i, j);
        elseif self.vz_max_3d(i, j) < -self.v_mid(i, j)
            self.vzs_division(i, j) = self.vz_max_3d(i, j);
        else
            self.vzs_division(i, j) = self.vz_min_3d(i, j);
        end
    end
end
end
