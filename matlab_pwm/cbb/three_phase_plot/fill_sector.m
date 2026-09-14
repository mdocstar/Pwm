function fill_sector(self, ax, x_start, x_end, color, label)
% FILL_SECTOR  Fill one sector band and place its label.
%   Equivalent to Python `ThreePhaseVoltagePlot.fill_sector`.

% default color 'lightblue' and empty label (mirrors the Python defaults)
if nargin < 5 || isempty(color), color = [173 216 230]/255; end
if nargin < 6,                   label = '';                 end

xs = linspace(x_start, x_end, 1000);
top = self.y_max * ones(size(xs));
bot = self.y_min * ones(size(xs));
fill_between(ax, xs, top, bot, color, 0.3);

text(ax, 0.5 * (x_start + x_end), -1.10, label, ...
    'FontSize', 12, 'FontWeight', 'bold', ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
    'Color', [0 0 0]);
end
