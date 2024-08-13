%blackboxplots
%V2, 8/4/24
%works with main code version 3.7, 3.8

%changes since last version:
%read more data that's now included in blackbox
%can handle multiple separate runs in the same blackbox file, for example
%if boat is hard restarted during mission and clock goes back to zero

if ~exist('m', 'var')
    clc;
    clear vars;
    m = readmatrix('blackbox truncated.txt');
    time = m(:,1);
    state = m(:,2);
    lat = m(:,3);
    long = m(:,4);
    chead = m(:,5);
    ghead = m(:,6);
    tpoint = m(:,7);
    PIDO = m(:,8);
    pport = m(:,9);
    pstar = m(:,10);
    prud = m(:,11);
    Imot = m(:,12);
    vbat = m(:,13);
    Isol = m(:,14);
    vsol = m(:,15);
    vbat = vbat./1000;  %convert mV to V
    vsol = vsol./1000;
    Imot = Imot./1000;  %convert mA to A
    Isol = Isol./1000;
    Inet = Isol-Imot;
    Imot = Imot.*(-1);

    %if time is reset back to zero, add the previous max value to it so
    %that the whole set is continuous
    lastmaxt = 0;
    for i=2:length(time)
        lastt = time(i-1);
        if(time(i)<lastt)
            lastmaxt = lastt;
        end
        time(i) = time(i) + lastmaxt;
    end

    %create subsets for plotting where manual mode data is cut out
    plotpport = pport;
    plotpstar = pstar;
    plotprud = prud;
    plottime = time;
    plotchead = chead;
    plotghead = ghead;
    plotPIDO = PIDO;
    index = find(state<1);
    plotpport(index) = [];
    plotpstar(index) = [];
    plotprud(index) = [];
    plottime(index) = [];
    plotchead(index) = [];
    plotghead(index) = [];
    plotPIDO(index) = [];
    
end

figure('Name','Power');
tiledlayout(2,1);
nexttile
plot(time,Isol,'Color',[0 0 0]);
hold on;
plot(time,Imot,'Color',[0 0.4470 0.7410]);
plot(time,Inet,'Color',[0.196, 0.804, 0.196]);
title('Current Draw vs Time');
xlabel('Time (seconds)');
ylabel('Current (A)');
legend('Panel Supply','System Draw','Net to Battery');
nexttile
hold off;
plot(time,vbat,'Color',[0 0 0]);
hold on;
title('Battery Voltage Over Time')
xlabel('Time (seconds)');
ylabel('Battery Voltage (V)');

ahconsumed = trapz(Imot);
ahproduced = trapz(Isol);

%f2 = figure;
figure('name','PWM');
tiledlayout(2,1);
nexttile
hold on;
scatter(plottime,plotpport,'Color',[0 0 0], 'Marker', ".");
scatter(plottime,plotpstar,'Color',[0 0.4470 0.7410], 'Marker', ".");
title('Motor PWM (Auto Mode Only)');
legend('Port','Starboard');
xlabel('Time (seconds)');
ylabel('PWM Pulse Width (µS)');
nexttile
hold off;
scatter(plottime,plotprud,'Color',[0 0 0], 'Marker', ".");
hold on;
title('Rudder PWM (Auto Mode Only)');
xlabel('Time (seconds)');
ylabel('PWM Pulse Width (µS)');

figure('name','PID Control');
tiledlayout(2,1);
nexttile
hold on;
scatter(plottime,plotchead,'Color',[0 0 0], 'Marker', ".");
scatter(plottime,plotghead,'Color',[0 0.4470 0.7410], 'Marker', ".");
title('Actual vs Goal Heading');
xlabel('Time (seconds)');
ylabel('Compass heading (degrees)');
legend('Actual','Goal');
hold off;
nexttile
hold on;
scatter(plottime,plotPIDO,'Color',[0 0 0], 'Marker', ".");
xlabel('Time (seconds)');
ylabel('Raw PID Output');
title('PID Steering Output');
