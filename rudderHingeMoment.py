## Input Data & Parameters
# Rudder hinge axis position relative to chord length [x_hinge/chord y_hinge/chord]
rHinge = [0.8, 0.0425]

# Input speeds [km/h]
velInp = [85, 95, 100, 105, 110, 120]

# Kinematic air viscosity [m^(2)s^(-1)]. Needed to calculate Re-Numbers
nu0 = 1.4e-5

# Input AOA [°]
aoaInp = [-5, 0, 5, 10]

# Input rudder deflection angles [°]
etaInp = [-5, 0.1, 5, 10]

# Airfoil Data
airfoilGeometryFile = "Fx63_137.txt"
airfoilName = "FX63-137"

# Delete auxiliary files after calculation?
# Values: 1 (yes), 0 (no)
rmAuxF = 1

#---------------------------------------------------------------------#
## Imports
import os
import itertools as it
import csv
import math as m
import numpy as np
import subprocess

## Files and directories creation
# Create speed directories
for v in velInp:
    dPath = "v"+str(v)
    if not os.path.exists(dPath):
        os.makedirs(dPath)
        print("Directory "+dPath+" created")
    else:
        print("Directory "+dPath+" exists, content will be overweritten.")

# All possible AOA and rudder angle combinations
aetaComb = [p for p in it.product(*[aoaInp, etaInp])];

# All possible airspeed, AOA and rudder angle combinations
vaetaComb = [p for p in it.product(*[velInp, aoaInp, etaInp])];

# Loop over every airspeed, aoa and rudder deflection angle to create input files for XFOIL
vDirs = []
for v in velInp:
    dPath = "v"+str(v)
    vDirs.append(dPath)
    for aeta in aetaComb:
        alfa = aeta[0]
        eta = aeta[1]
        re = m.floor(v/3.6/nu0)
        f = open('./'+dPath+'/'+airfoilName+'_v'+str(v)+'_a'+str(alfa)+'_e'+str(eta)+'.xf','w')
        f.write('load ./'+airfoilGeometryFile+
                '\nGDES'+
                '\nFlap'+str(rHinge[0])+' '+str(rHinge[1])+' '+str(eta)+
                '\neXec'+
                '\n '+
                '\nOPER'+
                '\nRE '+str(re)+
                '\nMACH'+str(v/3.6/np.sqrt(1.4*287*298))+
                '\nv'+
                '\nITER'+
                '\n300'+
                '\nALFA '+str(alfa)+
                '\nFMOM '+str(rHinge[0])+' '+str(rHinge[1])+
                ''+
                '\n\nQUIT'\
               )
        f.close()

# Shell script to run XFOIL-input files
xrun = open('xrun','w')
xrun.write('\nXvfb :1 & \
\nsleep 1 \
\nfor i in v*/*.xf \
\ndo \
\nDISPLAY=:1 xfoil < $i > "${i%.xf}".out \
\necho $i \
\ndone \
\nkill -15 $! \
')
xrun.close()

# Run shell script
subprocess.run(['sh', 'xrun'])

# As xfoil does not provide a command to output the hinge moment but only prints it out on STDOUT, each output file has to be read and scanned for the hinge moment.
hingeMomentCoefficient=np.empty((len(vaetaComb),5)) #initialize array
j = 0
for v in velInp:
    dPath = "v"+str(v)
    for aeta in aetaComb:
        alfa = aeta[0]
        eta = aeta[1]
        f = open('./'+dPath+'/'+airfoilName+'_v'+str(v)+'_a'+str(alfa)+'_e'+str(eta)+'.out','r')
        converg = 1
        for line in f:
            if line[0:28] == " VISCAL:  Convergence failed":
                converg = 0
            if line[0:13] == ' Hinge moment':
                hingeMomentCoefficient[j] = [v, alfa, eta, line.split()[3], converg]
                j = j+1
                

# Save calculated hinge moment to CSV file
np.savetxt(airfoilName+'_aeroGrid.csv', hingeMomentCoefficient, delimiter=',')

# Remove auxiliary files if rmAuxF flag is set to true
if rmAuxF:
    subprocess.run(['rm', '-r', 'xrun'] + vDirs)
