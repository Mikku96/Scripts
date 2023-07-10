
#TO GET PHASES FROM A MJD FILE (OT_MJD.dat); |FILE NAME.fits|MJD-time|Third mystery column

#GOAL: |FILE NAME.dat|PHASE-accumulated (0->x, NOT 0->1)

#OT PERIOD: 0.05887496

#EG Cnc period: 0.05997


import numpy as np
import sys
import glob
import itertools
import os
from statistics import mean

def folding(zipped):
    groups = np.arange(0,1,0.005)
    arrays = [[] for x in range(200)]
    phases_group = [[] for x in range(200)]
    new_arrays = []
    new_groups = []
    new_phases = []
    for filename, phase in zipped:
        #if phase >= 0.98:
        #    phase = phase-1.0
        comparison_to_bins = abs(groups-phase)
        index = np.where(comparison_to_bins == comparison_to_bins.min())
        #print(index[0][0])
        arrays[index[0][0]].append(filename)
        phases_group[index[0][0]].append(phase)
    for i in range(len(arrays)):
        """print(groups[i])
        print(arrays[i])
        print(20*'-')"""
        if arrays[i] != []:
            new_arrays.append(arrays[i])
            new_groups.append(groups[i])
            new_phases.append(phases_group[i])
    grouping = [[] for x in range(len(new_groups))]
    phase_grouping = [[] for x in range(len(new_groups))]
    for i in range(len(new_groups)):
        mean_difference = []
        print(20*'-')
        #print(len(new_arrays[i]))
        try:
            if (new_groups[i-1] > 10*new_groups[i+1]) or (new_groups[i-2] > 10*new_groups[i+1]) or (new_groups[i-1] > 10*new_groups[i+2]):
                print("here!")
                if new_groups[i] == 0:
                    mean_difference.append(abs(((new_groups[i]*len(new_arrays[i])+abs((new_groups[i-1]-1))*len(new_arrays[i-1])+new_groups[i+1]*len(new_arrays[i+1]))/(len(new_arrays[i])+len(new_arrays[i+1])+len(new_arrays[i-1]))) - new_groups[i]))
                else:
                    mean_difference.append(abs(((new_groups[i]*len(new_arrays[i])+new_groups[i-1]*len(new_arrays[i-1])+new_groups[i+1]*len(new_arrays[i+1]))/(len(new_arrays[i])+len(new_arrays[i+1])+len(new_arrays[i-1]))) - new_groups[i]))
                mean_difference.append(abs(((new_groups[i+1]*len(new_arrays[i+1])+new_groups[i]*len(new_arrays[i])+new_groups[i+2]*len(new_arrays[i+2]))/(len(new_arrays[i+1])+len(new_arrays[i])+len(new_arrays[i+2]))) - new_groups[i]))
                if new_groups[i] == 0:
                    mean_difference.append(abs(((abs(new_groups[i-1]-1)*len(new_arrays[i-1])+abs(new_groups[i-2]-1)*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - new_groups[i]))
                else:
                    mean_difference.append(abs(((new_groups[i-1]*len(new_arrays[i-1])+abs(new_groups[i-2]-1)*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - new_groups[i]))
            else:
                try:
                    mean_difference.append(abs(((new_groups[i]*len(new_arrays[i])+new_groups[i-1]*len(new_arrays[i-1])+new_groups[i+1]*len(new_arrays[i+1]))/(len(new_arrays[i])+len(new_arrays[i+1])+len(new_arrays[i-1]))) - new_groups[i]))
                except IndexError:
                    mean_difference.append(abs(((new_groups[i]*len(new_arrays[i])+new_groups[i-1]*len(new_arrays[i-1])+new_groups[0]*len(new_arrays[0]))/(len(new_arrays[i])+len(new_arrays[0])+len(new_arrays[i-1]))) - new_groups[i]))
                try:
                    mean_difference.append(abs(((new_groups[i+1]*len(new_arrays[i+1])+new_groups[i]*len(new_arrays[i])+new_groups[i+2]*len(new_arrays[i+2]))/(len(new_arrays[i+1])+len(new_arrays[i])+len(new_arrays[i+2]))) - new_groups[i]))
                except IndexError:
                    mean_difference.append(abs(((new_groups[0]*len(new_arrays[0])+new_groups[i]*len(new_arrays[i])+new_groups[1]*len(new_arrays[1]))/(len(new_arrays[0])+len(new_arrays[i])+len(new_arrays[1]))) - new_groups[i]))
                try:
                    mean_difference.append(abs(((new_groups[i-1]*len(new_arrays[i-1])+new_groups[i-2]*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - new_groups[i]))
                except IndexError:
                    mean_difference.append(abs(((new_groups[i-1]*len(new_arrays[i-1])+new_groups[i-2]*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - new_groups[i]))
        except IndexError:
            try:
                mean_difference.append(abs(((new_groups[i]*len(new_arrays[i])+new_groups[i-1]*len(new_arrays[i-1])+new_groups[i+1]*len(new_arrays[i+1]))/(len(new_arrays[i])+len(new_arrays[i+1])+len(new_arrays[i-1]))) - new_groups[i]))
            except IndexError:
                print("Eka")
                mean_difference.append(abs(((abs(new_groups[i]-1)*len(new_arrays[i])+abs(new_groups[i-1]-1)*len(new_arrays[i-1])+new_groups[0]*len(new_arrays[0]))/(len(new_arrays[i])+len(new_arrays[0])+len(new_arrays[i-1]))) - abs(new_groups[i]-1)))
            try:
                mean_difference.append(abs(((new_groups[i+1]*len(new_arrays[i+1])+new_groups[i]*len(new_arrays[i])+new_groups[i+2]*len(new_arrays[i+2]))/(len(new_arrays[i+1])+len(new_arrays[i])+len(new_arrays[i+2]))) - new_groups[i]))
            except IndexError:
                print("Toka")
                mean_difference.append(abs(((new_groups[0]*len(new_arrays[0])+abs(new_groups[i]-1)*len(new_arrays[i])+new_groups[1]*len(new_arrays[1]))/(len(new_arrays[0])+len(new_arrays[i])+len(new_arrays[1]))) - abs(new_groups[i]-1)))
            try:
                mean_difference.append(abs(((new_groups[i-1]*len(new_arrays[i-1])+new_groups[i-2]*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - new_groups[i]))
            except IndexError:
                print("Kolmas")
                mean_difference.append(abs(((new_groups[i-1]*len(new_arrays[i-1])+new_groups[i-2]*len(new_arrays[i-2])+new_groups[i]*len(new_arrays[i]))/(len(new_arrays[i-1])+len(new_arrays[i-2])+len(new_arrays[i]))) - abs(new_groups[i]-1)))
        #print(mean_difference) #MEAN difference is ordered as: middle - higher - lower
        tmp = min(mean_difference)
        index = mean_difference.index(tmp)
        """if index==0:
            print(i)
        if index==1:
           if (i+1) == len(new_arrays):
            print(0)
           else:
            print(i+1)
        if index==2:
            print(i-1)"""
        if index == 0:
            grouping[i].append(new_arrays[i])
            phase_grouping[i].append(new_phases[i])
        elif index ==1:
            if (i+1) ==len(new_arrays):
                grouping[0].append(new_arrays[i])
                phase_grouping[0].append(new_phases[i])
            else:
                grouping[i+1].append(new_arrays[i])
                phase_grouping[i+1].append(new_phases[i])
        elif index==2:
            grouping[i-1].append(new_arrays[i])
            phase_grouping[i-1].append(new_phases[i])
            
    list2 = [e for e in grouping if e]
    list2_phases = [e for e in phase_grouping if e]
    combined_groups = []
    combined_phases = []
    for i in list2:
        list3 = [item for sublist in i for item in sublist]
        combined_groups.append(list3)
    for i in list2_phases:
        list3 = [item for sublist in i for item in sublist]
        combined_phases.append(list3)
    print(len(combined_groups))
    print(combined_phases)
    last_combine = [[] for x in range(43)]
    last_combine_phase = [[] for x in range(43)]
    for i in range (len(combined_groups)):
        if len(combined_groups[i]) < 2:
            #print(combined_phases[i][0])
            diff1 = abs((mean(combined_phases[i-1]) - combined_phases[i][0]))
            #print(diff1)
            diff2 = abs((mean(combined_phases[i+1]) - combined_phases[i][0]))
            #print(diff2)
            #print(i)
            if diff1 < diff2:
                last_combine[i-1].append(combined_groups[i])
                last_combine_phase[i-1].append(combined_phases[i])
            elif (diff2 < diff1) and (len(combined_groups[i+1]) == 1):
                last_combine[i].append(combined_groups[i])
                last_combine_phase[i].append(combined_phases[i])
            else:
                last_combine[i+1].append(combined_groups[i])
                last_combine_phase[i+1].append(combined_phases[i])
        else:
            last_combine[i].append(combined_groups[i])
            last_combine_phase[i].append(combined_phases[i])
    #print(last_combine_phase)

    list2 = [e for e in last_combine if e]
    list2_phases = [e for e in last_combine_phase if e]
    #print(list2)
    print(len(list2_phases))
    combined_groups = []
    combined_phases = []
    for i in list2:
        list3 = [item for sublist in i for item in sublist]
        combined_groups.append(list3)
    for i in list2_phases:
        #print(i)
        #print(i)
        #print(20*'-')
        list3 = [item for sublist in i for item in sublist]
        combined_phases.append(list3)
    meaned_phases = []
    for i in range(len(combined_phases)):
        if i==0:
            separate = [[] for x in range(len(combined_phases[i]))]
            for j in range (len(combined_phases[i])):
                if combined_phases[i][j] > 0.5:
                    separate[j] = (combined_phases[i][j]-1)
                else:
                    separate[j] = combined_phases[i][j]
            calc = mean(separate)
        else:
            calc = mean(combined_phases[i])
        meaned_phases.append(calc)
    for i in combined_phases:
        print(i)
        print(20*'-')
    with open("combined_phases.dat", 'w') as g:
        for i in range(len(combined_groups)):
            with open("temp_list.dat",'w') as t:
                for j in combined_groups[i]:
                    t.write(f'{j}\n')
            os.system(f'python spec-aver_multi.py -cnqs @temp_list.dat RV_combine_{i}.dat')
            if i == len(combined_groups):
                g.write(f'RV_combine_{i}.dat {meaned_phases[i]}')
            else:
                g.write(f'RV_combine_{i}.dat {meaned_phases[i]}\n')
        
        


args = sys.argv
data_filename = args[1]
if len(args) < 2:
	print("Usage: phase_accum_OT.py <file_name> <period (in days) > <normal,accumulate,sorted>")
if len(args) > 2:
	period = float(args[2])
else:
	period = 0.05884



output_filename = 'phases.dat'
print(f'Data file {data_filename} , period {period} , output file {output_filename}')

filenames = []
MJDtimes  = []
exptimes  = []

with open(data_filename,'r') as f:
	for row in f.readlines()[0:]:
		print(row)
		filenames.append(row.split(' ')[0])
		MJDtimes.append(float(row.split(' ')[1]))
		#exptimes.append(float(row.split(' ')[2]))
#filenames = glob.glob("*.dat")
#print(filenames)
ref_MJD = MJDtimes[0]
phases = []
if len(args) > 3:
	if args[3] == "accumulate":
		for MJD in MJDtimes:
			phases.append((MJD-ref_MJD)/period)
	else:
		for MJD in MJDtimes:
			phases.append((MJD-ref_MJD)/period - int((MJD-ref_MJD)/period))
else:
	for MJD in MJDtimes:
		phases.append( (MJD - ref_MJD)/period - int((MJD - ref_MJD)/period))

with open(output_filename, 'w') as f:
	zipped = zip(filenames,phases)
	if args[3] == "sorted":
		zipped = sorted(zipped,key=lambda x: x[1])
	for filename, phase in zipped:
		#print(phase)
		#f.write(f'{filename[:-5]}.dat {phase}\n')
		f.write(f'{phase}\n')
print(f'Saved to: {output_filename}')

do_we_fold = input("Do we fold the phases? (yes/no) " )
if do_we_fold == "yes":
    folding(zipped)
else:
    print("DONE")

#print(MJDtimes)
