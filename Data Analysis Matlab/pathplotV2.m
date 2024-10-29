clear vars;
close all;

m1 = readmatrix('blackbox truncated 1.txt');
time1 = m1(:,1);
lat1 = m1(:, 3);
long1 = m1(:, 4);
%long = long*(-1);

m2 = readmatrix('blackbox truncated 2.txt');
time2 = m2(:,1);
lat2 = m2(:, 3);
long2 = m2(:, 4);
%long = long*(-1);



c = readmatrix('COORDS Matricized.TXT');
clat = c(:,1);
clong = c(:,2);

plot(clong,clat,'Color',[0 0 0]);
hold on;
axis equal;
plot(long1, lat1, 'Color', [0,1,0], 'LineWidth', 2);
plot(long2, lat2, 'Color', [0,0,1], 'LineWidth', 2);
xlabel("Longitude");
ylabel("Latitude");
Title("Planned Path vs Actual");
%plot(clong,clat,'Color',[0 0.4470 0.7410]);
