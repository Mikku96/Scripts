import os
import glob
import subprocess
from astropy.io import fits
import numpy as np

period = 0.05999 #days
obs_times = []
a_lista=[]
lista = glob.glob('*VIS.fits')
for i in range(len(lista)):
	#a = subprocess.check_output('gethead '+str(lista[i])+' MJD-OBS', shell=True)
	a = fits.open(lista[i])
	a_lista.append(float(a[0].header['MJD-OBS']))
Z = [x for  _,x in sorted(zip(a_lista,lista))]
print(Z)
print(a_lista)
#print(Z)


#for i in Z:
#	#tallennus_kohde = ''+str(i[:i.find('_')])+'_phase.txt'
#	tallennus_kohde = i.split("_")[1]+"_phase.txt"
#	obs_time = tyosta(i,tallennus_kohde)
#	#print(obs_time)
#	obs_times.append(obs_time)
phases = []

for i in a_lista:
	phase = (i - a_lista[0])/(period)# - int((i - a_lista[0])/(period))
	phases.append(phase+0.27)


"""for i in range(len(phases)):
	name = ''+str(Z[i][:Z[i].find('_')])+'_phase.txt'
	#print(name)
"""

#spectrum = glob.glob("spektrit/*.dat")
#spectrum = sorted(spectrum, key= lambda x:( int((x[:].split('/')[-1]).split("_")[1]), x))
#

print(len(phases))
#print(len(spectrum))
with open('phases.txt', "w") as f:
	for i in range(len(phases)):
		#name = Z[i]
		#f.write(spectrum[i].split("/")[-1])
		#f.write(' ')
		f.write(str(phases[i]))
		f.write(str("\n"))


