clc,clear

Gap = 5e-2;
wt = 0:Gap:2 * pi / 3;
Modu = 0:Gap:2 / sqrt(3);
[X,Y] = meshgrid(wt,Modu);
[Row,Line] = size(X);

Vzmax = zeros(Row,Line);
Vzmin = zeros(Row,Line);

Division_Line = pi / 3;
for i = 1:Row
    for j = 1:Line
        %%%% calculate the limitation of zero-sequence voltage
        umax = Modu(i) * sin(wt(j) + pi / 6);
        if(wt(j) < Division_Line)
            umin = Modu(i) * sin(wt(j) - pi / 2);
        else
            umin = Modu(i) * sin(wt(j) + 5 * pi / 6);
        end

        %%%% set zero-sequence voltage value
        Vzmax(i,j) = min(1 - umax,-umin);
        Vzmin(i,j) = max(-1 - umin,-umax);
    end
end

% 设置全局字体和线条属性
set(groot, 'defaultAxesFontName', 'Times New Roman');
set(groot, 'defaultAxesFontSize', 14);
set(groot, 'defaultAxesFontWeight', 'bold');

% 创建图形窗口
figure();
ax = axes('Position', [0.1, 0.1, 0.7, 0.8]);

% 绘制曲面
% 上边界 Uzs_max
Yscale = sqrt(3) / 2;
h1 = surf(X, Y * Yscale, Vzmax, ...
         'FaceColor', 'flat', ...
         'EdgeColor', 'k', ...
         'FaceAlpha', 0.6, ...
         'LineStyle','-', ...
         'LineWidth',0.5);
hold on;
grid on;

h2 = surf(X, Y * Yscale, Vzmin, ...
         'FaceColor', 'flat', ...
         'EdgeColor', 'k', ...
         'FaceAlpha', 0.6, ...
         'LineStyle','-', ...
         'LineWidth',0.5);

set(gca,"XLim",[0 2 * pi / 3],...
        'XTick', [0, pi/3, 2*pi/3], ...  % 设置刻度位置为弧度值
        'XTickLabel', {'0', '\pi/3', '2\pi/3'}, ... % 设置LaTeX格式的标签
        "YLim",[0 1.0],...
        "ZTick",[-0.8 -0.4 0 0.4 0.8], ...
        "ZLim",[-0.8 0.8])

set(ax, ...
    'GridLineStyle', '--', ...      
    'GridColor', [0.8 0.8 0.8], ...  
    'GridAlpha', 0.8, ...            
    'MinorGridLineStyle', '--', ...  
    'MinorGridColor', [0.8 0.8 0.8]);


view([45 12.5]);
colormap turbo
cb = colorbar;
set(cb, 'Position', [0.88, 0.15, 0.03, 0.7]);