% Import data from CSV file
data = csvread('FX63-137_aeroGrid.csv');
v = data(:,1);
aoa = data(:,2);
eta = data(:,3);
cm = data(:,4);

% Index of converged values 
converged = find(data(:,5));
notConverged = find(not(data(:,5)));

% Plot points on 3D diagramm to see which points converge and which do not
plot3(v(converged),aoa(converged),eta(converged),'sb')
hold on
plot3(v(notConverged),aoa(notConverged),eta(notConverged),'dr')
xlabel('Airspeed [kmh]')
ylabel('AOA [°]')
zlabel('Rudder deflection angle [°]')

% Create interpolating function
cmInterpolationFunction = scatteredInterpolant(v(converged),aoa(converged),eta(converged),cm(converged),'linear','none');

% Function usage
cM = cmInterpolationFunction(88,1,1)
 