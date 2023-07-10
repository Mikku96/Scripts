#VALMISTELU:

#LUO KANSIORAKENNE:

#Tuolla pohjakansiossa oltava ne python scriptit! HUOM! TIEDOSTOJEN NIMET

#pohjakansio\
#|
#|--spec-aver.py, spec-barycorr.py, xs_clean_new.py, skylines.txt
#|
#|--renamed_VIS\
#|  |
#|  |-- 00_VIS.fits... 01_VIS.fits... 02_VIS.fits etc.
#|  |
#|  |--VIS_angs\
#|      |
#|      |--00_VIS_COMP.dat... 01_VIS_COMP.dat... 02_VIS_COMP.dat etc.
#|
#|--renamed_UVB
#|  |
#|  |-- 00_UVB.fits... 01_UVB.fits... 02_UVB.fits etc.
#|  |
#|  |--UVB_angs\
#|      |
#|      |--00_UVB_COMP.dat... 01_UVB_COMP.dat... 02_UVB_COMP.dat etc.
#|
#|--renamed_NIR
#|  |
#|  |-- 00_NIR.fits... 01_NIR.fits... 02_NIR.fits etc.
#|  |
#|  |--NIR_angs\
#|      |
#|      |--00_NIR_COMP.dat... 01_NIR_COMP.dat... 02_NIR_COMP.dat etc.
#|

#Ainoa input pitäisi olla ekassa vaiheessa; eli kirjoita tiedoston vika wavelength ja steppi.

import glob
import sys
import numpy as np
import os
from astropy.io import fits

def add_tag(name,tag):
    return name[:-4] + "_"+tag+".dat"


def get_files(band):
    path_to_datas = rf'{band}\{band}_angs'
    data_files = glob.glob(rf'{path_to_datas}\*_COMP.dat')
    orig_data_txt = path_to_datas+'\\orig_data.txt' #CREATE a text file with the data files

    with open(orig_data_txt,'w') as f:
        for data in data_files:
            f.writelines(data+'\n')

    return data_files,path_to_datas,orig_data_txt

def get_fits(band):
    path_to_datas = rf"{band}"
    fit_files= glob.glob(rf'{path_to_datas}\*.fits')

    return fit_files

def calculate_mean_bar(fit_files):
    bar = []

    for i in range(len(fit_files)):
        hdul = fits.open(fit_files[i])
        h1 = hdul[0].header
        obj_name = h1.get('HIERARCH ESO QC VRAD BARYCOR')
        bar.append(obj_name)

    result = np.mean(bar)
    return result

def sky_files(file_path):
    print(file_path)
    data_files = glob.glob(rf'{file_path}\*.sky')

    list_path = file_path + '\\sky_data.txt'
    with open(list_path, 'w') as f:
        for data in data_files:
            f.writelines(data + '\n')

    return list_path

def interp_files(file_path):
    data_files = glob.glob(rf'{file_path}\*_interp.dat')
    list_path = file_path + '\\cut_data.txt'
    with open(list_path, 'w') as f:
        for data in data_files:
            f.writelines(data + '\n')
    return list_path



def rename_and_clean(file_path,cleaning):
    sys_path = os.getcwd()
    data_files = glob.glob(rf'{file_path}\*_barycorr.dat')
    for i in data_files:
        temp_nimi = i.split('\\')[-1]
        os.system(f"RENAME {sys_path}\{i} {temp_nimi[:-23]}processed.dat") #Rename barycorr files to processed!

    data_files = glob.glob(rf'{file_path}\*processed.dat')
    list_path = file_path + '\\processed_data.txt'
    with open(list_path, 'w') as f:
        for data in data_files:
            f.writelines(data + '\n')
    if cleaning == "True":
        os.system(f"del {sys_path}\{file_path}\*_interp*")
        os.system(f"del {sys_path}\{file_path}\*.clean*")
        os.system(f"del {sys_path}\{file_path}\*.mask*")
        os.system(f"del {sys_path}\{file_path}\*.sky")
        os.system(f"del {sys_path}\{file_path}\\sky_data.txt")
        os.system(f"del {sys_path}\{file_path}\\cut_data.txt")
        os.system(f"del {sys_path}\{file_path}\\orig_data.txt")

    return list_path

################################################################
#1 Start by getting argument from input; which spectral feature
if __name__=="__main__":
    args = sys.argv
    if len(args) < 6:
        print("python pipe_process2_cleaned.py {UVB,VIS,NIR} {True, False} {w1} {w2} {step}")
        print("-"*10)
        print("{UVB,VIS,NIR} eli valittu spektrikaista")
        print("{True, False} eli puhdistetaanko spektriä")
        print("{w1} {w2} {step} Minimi ja maksimi aallonpituudet, sekä step")
        exit(-1)
    band = args[1]
    clean = args[2]
################################################################
#2 GET file path (data, and fits). MAKE sure that 1. folder is the same name as the parameter (above)
    data_files, file_path, orig_data_txt =get_files(band)
    print(f".dat file amount: {len(data_files)}")

#3 GET .fits files - one folder above the former
    fit_files = get_fits(band)
    print(f".fits file amount: {len(fit_files)}")

#4 Calculate barionic correction from .fits files (average)
    mean_bar = calculate_mean_bar(fit_files)

#5 Minimum, maximum and stepsize for the spectrum; CHANGE HERE!
    if band == "VIS" or band=="UVB" or band=="NIR":
        minim_wave = args[3] #Gradussa 3210, 5336.6 ja 9940
        w2 = args[4] # Gradussa 5559.8, 10200, 22725
        step = args[5] # Gradussa 0.2 ja NIR kaistalla 0.6
    else:
        print("Nothing was done, 'cause band name?")
        exit(-1)
    print("#####################################")
    print(f"Maximum Å: {w2} Å") 
    print(f"Minimum Å: {minim_wave} Å")
    print(f"Step Å: {step} Å")
    print("#####################################")
    print("Strength: 0.1, Cut off: 0.7, stand. dev.: 5 (2 for NIR), median filter: 21")

#6 FIRST Process - CLEAN (strength, standard deviation, median filter asked)
    os.system(f'python xs_clean_new.py +s -lm @{orig_data_txt}') #OUTPUTS
#Output is 3 files, .sky files are the real end results (will be removed at the end!)

#7 Create a list of .sky files
    sky_list = sky_files(file_path)

#8 Run the .sky files with barycorr; get interp (cutting the spec)

    os.system(f'python spec-barycorr.py @{sky_list} {minim_wave} {w2} {step}')

#Output is _interp

#9 Read _interp files to list
    cut_list = interp_files(file_path)

#10 Re-run barycorr (do barycorr
    os.system(f'python spec-barycorr.py @{cut_list} {mean_bar}')

#Output is .barcorr
    
#11 LASTLY! Do some renaming, and removal of the intermediate steps
    processed_list = rename_and_clean(file_path,clean)
#12 Combine the end results with spec-aver
    os.system(f'python spec-aver.py -cnqs @{processed_list} {file_path}\\output.dat')
