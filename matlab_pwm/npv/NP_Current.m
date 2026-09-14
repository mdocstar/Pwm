clc,clear

%%% system variable parameters
Modulation = 0:5e-2:2 / sqrt(3); 
wt = 0:5e-2:2 * pi / 3;
[X,Y] = meshgrid(Modulation,wt);
[Lenx,Leny] = size(X);

%%% three-phase voltage
Ua  = zeros(Lenx,Leny);
Ub  = zeros(Lenx,Leny);
Uc  = zeros(Lenx,Leny);
Umax = zeros(Lenx,Leny);
Umin = zeros(Lenx,Leny);
U0   = zeros(Lenx,Leny);

Mjust = 2 / sqrt(3);
for i = 1:Lenx
    for j = 1:Leny
        Ua(i,j) = Modulation(j) * sin(wt(i)) * Mjust;
        Ub(i,j) = Modulation(j) * sin(wt(i) - 2 * pi / 3) * Mjust;
        Uc(i,j) = Modulation(j) * sin(wt(i) + 2 * pi / 3) * Mjust;

        Umax(i,j) = max([Ua(i,j) Ub(i,j) Uc(i,j)]);
        Umin(i,j) = min([Ua(i,j) Ub(i,j) Uc(i,j)]);
        U0(i,j)   = 0;
    end
end

%%% zero-sequence voltage limitation
Uzsmax  = zeros(Lenx,Leny);
Uzsmin  = zeros(Lenx,Leny);
for i = 1:Lenx
    for j = 1:Leny
        Uzsmax(i,j) = min([(1 - Umax(i,j)) -Umin(i,j)]);
        Uzsmin(i,j) = max([(-1 - Umin(i,j)) -Umax(i,j)]);
    end
end

%%% 科研绘图设置
% 设置全局字体和线条属性
set(groot, 'defaultAxesFontName', 'Times New Roman');
set(groot, 'defaultAxesFontSize', 14);
set(groot, 'defaultAxesFontWeight', 'bold');

% 创建图形窗口
figure();
ax = axes('Position', [0.1, 0.1, 0.7, 0.8]);

% 绘制曲面
% 上边界 Uzs_max
h1 = surf(X, Y, Uzsmax, ...
         'FaceColor', 'flat', ...
         'EdgeColor', 'k', ...
         'FaceAlpha', 0.8, ...
         'LineStyle','-', ...
         'LineWidth',0.5);
hold on;
grid on;

% 下边界 Uzs_min
h2 = surf(X, Y, Uzsmin, ...
         'FaceColor', 'flat', ...
         'EdgeColor', 'k', ...
         'FaceAlpha', 0.8, ...
         'LineStyle','-', ...
         'LineWidth',0.5);

h3 = surf(X, Y, U0, ...
         'FaceColor', [255 255 255] / 255, ...
         'EdgeColor', 'k', ...
         'FaceAlpha', 0.8, ...
         'LineStyle','-', ...
         'LineWidth',0.5);

set(gca,"XTick",[0 0.5 1.0], ...
        "XLim",[0 1.0],...
        'YTick', [0, pi/3, 2*pi/3], ...  % 设置刻度位置为弧度值
        'YTickLabel', {'0', '\pi/3', '2\pi/3'}, ... % 设置LaTeX格式的标签
        "YLim",[0 2*pi/3],...
        "ZTick",[-0.8 -0.4 0 0.4 0.8], ...
        "ZLim",[-0.8 0.8])

set(ax, ...
    'GridLineStyle', '--', ...      
    'GridColor', [0.8 0.8 0.8], ...  
    'GridAlpha', 0.8, ...            
    'MinorGridLineStyle', '--', ...  
    'MinorGridColor', [0.8 0.8 0.8]);

view([45 22.5]);
colormap turbo
cb = colorbar;
set(cb, 'Position', [0.90, 0.15, 0.03, 0.7]);


