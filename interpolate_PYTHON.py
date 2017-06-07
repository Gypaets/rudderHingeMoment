# Needed Packages
import numpy as np
from scipy.interpolate import griddata

# Import data from CSV file
hingeMomentCoefficient = np.genfromtxt(airfoilName+'_aeroGrid.csv', delimiter=',')

# Get index of converged values
converged = np.flatnonzero(hingeMomentCoefficient[:,4])


# Create interpolating function
def cmInterp(v,alfa, eta):
    return griddata(hingeMomentCoefficient[converged,0:3], hingeMomentCoefficient[converged,3:4][converged,0], [v, alfa, eta], method='linear')[0]


# Function usage
cmInterp(113,6,-4)

