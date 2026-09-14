function fill_between(ax, x, y1, y2, color, alpha)
% FILL_BETWEEN  Mimic matplotlib's fill_between (vertical band between two curves).
%   Fills the region between y1 (top) and y2 (bottom) over x, skipping NaN
%   segments (matplotlib fill_between leaves gaps where the curves are NaN).
%
%   color: 1x3 RGB vector or a MATLAB color character.
%   alpha: face alpha (default 0.3).

if nargin < 6, alpha = 0.3; end

x = x(:);
y1 = y1(:);
y2 = y2(:);

nanmask = isnan(y1) | isnan(y2);

% find contiguous non-NaN runs
d = [true; diff(nanmask) ~= 0; true];
idx = find(d);

for k = 1:numel(idx) - 1
    seg = idx(k):idx(k+1) - 1;
    if ~nanmask(seg(1))
        xs = x(seg);
        top = y1(seg);
        bot = y2(seg);
        patch(ax, [xs; flipud(xs)], [top; flipud(bot)], color, ...
            'FaceAlpha', alpha, 'EdgeColor', 'none');
    end
end
end
