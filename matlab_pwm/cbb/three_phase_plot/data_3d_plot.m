function data_3d_plot(self, data1, data2)
% DATA_3D_PLOT  Plot the two zero-sequence voltage surfaces in 3D.
%   Equivalent to Python `ThreePhase3D.data_3d_plot`.

if nargin < 2 || isempty(data1), data1 = self.vz_max_3d; end
if nargin < 3 || isempty(data2), data2 = self.vz_min_3d; end

set(groot, 'defaultAxesFontName', 'Times New Roman');

figure;
ax = axes;
view(ax, [45 30]);              % azim=45, elev=30 (Python view_init(elev=30, azim=45))
ax.Projection = 'orthographic'; % orthographic projection
set(ax, 'Color', 'white');      % white background

% grid lines light gray (#C0C0C0), axis lines darker gray (#666666)
ax.GridColor = [192 192 192]/255;
ax.XColor = [102 102 102]/255;
ax.YColor = [102 102 102]/255;
ax.ZColor = [102 102 102]/255;

% colorbar: shared clim over both surfaces (Python uses cm.viridis;
% MATLAB has no built-in viridis, so use 'parula' — switch to 'turbo'
% to match your other figures if preferred)
colormap(ax, 'parula');
all_vals = [data1(:); data2(:)];
vmin = min(all_vals);
vmax = max(all_vals);

% plot two surfaces (data2 first, data1 on top, like the Python source)
surf(ax, self.X, self.Y, data2, 'FaceAlpha', 0.6, 'EdgeColor', 'none');
hold(ax, 'on');
h = surf(ax, self.X, self.Y, data1, 'FaceAlpha', 0.6, 'EdgeColor', 'none');
caxis(ax, [vmin vmax]);

cb = colorbar(ax);

xlabel(ax, 'Angle (rad)', 'FontWeight', 'bold');
ylabel(ax, 'Modulation Index', 'FontWeight', 'bold');
zlabel(ax, 'Zero-sequence Voltage (p.u.)', 'FontWeight', 'bold');

xticks      = [0, pi/2, pi, 3*pi/2, 2*pi];
xtick_labels = {'0', '\pi/2', '\pi', '3\pi/2', '2\pi'};
set(ax, 'XTick', xticks, 'XTickLabel', xtick_labels, 'FontSize', 12, 'FontWeight', 'bold');
end
