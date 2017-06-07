# rudderHingeMoment

The script rudderHingeMoment.py runs [XFOIL](http://web.mit.edu/drela/Public/web/xfoil/) for every combination of given airspeeds, angles of attack and rudder deflection angles. The calculated rudder hinge moment coefficients are saved along with the input data in a CSV file.

In "interpolate_LANGUAGE.xx" an interpolation function is created to get the rudder hinge moment coefficient for arbitrary input data. Not converged coefficients are automatically excluded from being used. Extrapolation is not supported. 

To calculate the rudder hinge moment from the coefficient you can use the equation provided in xfoil's documentation:

Hinge moment / Span = C_m  x  1/2 rho V^2  c^2 

## Requierements
Linux, xfoil, Python 3.5
