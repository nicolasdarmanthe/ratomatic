#IMPROVE: this software should have the ability to ammend trdatlorebindat file from a template
#IMPROVE: remove the need for standard nomenclature assumption
#IMPROVE: add the ability to save new default paths

## --------------------------------------------------------------------------- ##
# This program is intended to make motion correction and image reconstruction   #
# for awake animal studies as easy as possible. It will ask the user for a few  #
# inputs and will take care of modifying all the appropriate fields in scripts  #
# and parameter files. The program will generate the following files(_) and     #
# replace them in a systematic & reasonable location.                           #
## --------------------------------------------------------------------------- ##

print('')
print('     THIS PROGRAM IS FOR USE IN PYTHON 2 (Python 3 not supported)') #for use with python 3, simply replace raw_input() with input()
print('')
print('     FOR THESE SCRIPTS TO WORK, MAKE SURE THE NOMENCLATURES IN - trdatlorebindat.pro - RunJob.pbs - reconstruction_parameters.par - MATCH YOUR NOMENCLATURE/FILE NAMING CONVENTION e.g. DATE_PTSD_STUDY')
print('')
print('     BEFORE RUNNING THIS PROGRAM, MAKE SURE YOU HAVE RunJob_template.pbs and reconstruction_parameters_template.par files IN PYTHONS WORKING DIRECTORY')
print('')

##--Import necessary modules and create simple function necessary for this program

import sys
import os
import errno

##------------------------------------------------------------------------------
#   creates function 'replace_all' to replace all occurences of target keyword
#   replace_all(text, dic) takes 2 arguments: text and dic
#       text argument is the file in which to search
#       dic argument is the dictionary with
#            words to be search for as the key
#            words by which they should be replaced as the value
#               e.g. searchnreplace = {key1:value1, key2:value2, ...}
#               e.g. searchnreplace = {'NORMPATHx':normpath, 'DATAPATHx:datapath'}
##------------------------------------------------------------------------------

if (sys.version_info > (3, 0)):
    #for python 3
    def replace_all(text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

else:
    #for python2
    def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

##------------------------------------------------------------------------------
# This small function ensures that directories are created if they do not exist
##------------------------------------------------------------------------------

def makedirnfile(filepathtocreate):
    if not os.path.exists(os.path.dirname(filepathtocreate)):
        try:
            os.makedirs(os.path.dirname(filepathtocreate))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

##--Paths---------------------------------------------------------------------

print('     Would you like to use default paths? yes - no')
usedefaults = raw_input()
if usedefaults == 'yes':
    idlpath = '/project/PET_PTSD/ListModeRecon_ndar/IDL'
    processpath = '/project/PET_PTSD/ListModeRecon_ndar/Process'
    reconpath = '/project/PET_PTSD/ListModeRecon_ndar/lmemmlv7'
    normpath = '/project/PET_PTSD/ListModeRecon_ndar/Data/FDG/Bennett/PTSD_Study/Ge68_20180627_Norm/Ge68_20180627_Norm_v1.nrm'
    datapath = '/project/PET_PTSD/ListModeRecon_ndar/Data/FDG/Bennett/PTSD_Study'
    syspath = '/project/PET_PTSD/ListModeRecon_ndar/Data/System/microPET_system_ordered_centre_doi_span1_v7.bin'
else:
    #IDL PATH
    print('     specify the path for IDL')
    idlpath = raw_input()
    print('')

    #PROCESS PATH
    print('     specify the path for process')
    processpath = raw_input()
    print('')

    #RECON PATH
    print('     specify the path for reconstruction software')
    reconpath = raw_input()
    print('')

    #NORM PATH
    print('     specify the path for normalisation file')
    normpath = raw_input()
    print('')

    #PATH FOR DATA OF CURRENT
    print('     specify the path for your data')
    datapath = raw_input()
    print('')

    #PATH FOR FOCUS220 SYSTEM FILE
    print('     Specify path for FOCUS220 system file')
    syspath = raw_input()
    print('')

    #print('Would you like to save these paths as your new defaults? yes -no')
    #savedefaults = input()
    #if savedefaults == 'yes':
        #ratomaticRAW = open(./ratomatic.py,'r')
        #ratomatic = ratomaticRAW.read()
        #ratomaticRAW.close()
        #ratomaticNEW = open(./ratomatic.py,'w')

##-----------------------------------------------------------------------------

##--STUDY DATE, NAME AND TYPE-------------------------------------------------

print('')
print('     --------------STUDY DETAILS-------------')
print('')

print('     specify the name of the subject e.g. Rat2Scan1')
STUDY = raw_input()
print('')

print('     specify the date of the study e.g. 20180628')
DATE = raw_input()
print('')

print('     Specify whether this study is tube bound (0) or open field (1)')
STYPE = input() #not raw_input because of replace glitch, doesn't know how to write 0 if it is a string
print('')

##-----------------------------------------------------------------------------

##--LOREbin options--------------------------------------------------------------

print('')
print('     --------------LOREBIN OPTIONS-------------')
print('')

print('     Specify whether to smooth (1) or not to smooth (0) the motion vector data')
SMOOTH = raw_input()

##-----------------------------------------------------------------------------

##--genlistmode options. Many more options are available by running ./mPET_genlistmode_v6 -H. This program can be updated to include more options later.

print('')
print('     --------------GENLISTMODE OPTIONS-------------')
print('')

print('     Specify the number of subsets you would like to use e.g. 10')
SUBSETS = raw_input()
print('')

print('     Specify type of reconstruction - static or dynamic')
RECONTYPE = raw_input()
print('')

if RECONTYPE == 'static':
    print('     Specify background frame duration and effective scan duration e.g. 276*1,3600*1 \
                note: to obtain a static scan of the last 30 mn of effective scan, input might be 276*1,1800*2 \
                        You would then discard the first two \'frames\'')
    FRAMETIME = raw_input()

else:
    print('     Specify duration of frames (in s) and number of frames with that duration e.g 276*1,300*12')
    print('     CAREFUL! DONT EXCEED DURATION OF .lst')

    FRAMETIME = raw_input()

#FIND SCANLEN code in progress
#how to extract scan duration from eader. Also need to convert it from format 01:03:53 to 3833 seconds
#lsthdrpath = datapath+DATE+'_PTSD_'+STUDY+'/'+DATE+'_PTSD_'+STUDY+'_v1.lst.hdr'
#lsthdr = open(lsthdrpath,'r')
#contents = lsthdr.read()
#lsthdr.close()
#contents.find('Format')
#print('note: the '+STUDY+' scan duration is'+SCANLEN+'seconds')

print('')
print('     Specify how many missed poses to replace before deleting the LOR data e.g. 100')
XVALUE = raw_input()

##-----------------------------------------------------------------------------

##--reconstruction parameter options. Many more options in reconstruction_parameters.par file.

print('')
print('     --------------RECONSTRUCTION OPTIONS-------------')
print('')

print('Would you like to use default image size and dimensions settings? yes-no')
usedefaults2 = raw_input()
print('')

if usedefaults2 == 'yes':
    MATSIZEX = '128'
    MATSIZEY = '128'
    MATSIZEZ = '95'
    VOXSIZEX = '0.949'
    VOXSIZEY = '0.949'
    VOXSIZEZ = '0.796'
    print('You are using a 128 x 128 x 95 matrix with 0.949 x 0.949 x 0.796 mm voxels')
    print('')

else:
    print('     Specify image matrix size X Y Z - 128 x 128 x 95 recommended ')
    print('')

    print('     X dim?')
    MATSIZEX = raw_input()
    print('')

    print('     Y dim?')
    MATSIZEY = raw_input()
    print('')

    print('     Z dim?')
    MATSIZEZ = raw_input()
    print('')

    print('     Specify image voxel size (in mm) - 0.949 x 0.949 x 0.796 recommended ')
    print('')

    print('     X dim?')
    VOXSIZEX = raw_input()
    print('')

    print('     Y dim?')
    VOXSIZEY = raw_input()
    print('')

    print('     Z dim?')
    VOXSIZEZ = raw_input()
    print('')

print('     Will be using generating frames '+FRAMETIME+' as specified previously. Will be using '+SUBSETS+' subsets as specified previously')
print('     Specify number of iterations')
ITERATIONS = raw_input()
print('')

#not working
#print('You have chosen to use '+SUBSETS+'subsets and '+ITERATIONS+' iterations. This is equivalent to reconstructing the image with an MLEM algorithm \
        #and '+str(float(SUBSETS)*float(ITERATIONS))+' iterations')

##-----------------------------------------------------------------------------

#define the file maker function
def fmaker(idlpath,processpath,reconpath,normpath,datapath,syspath,STUDY,DATE,STYPE,SMOOTH,SUBSETS,RECONTYPE,FRAMETIME,XVALUE,MATSIZEX,MATSIZEY,MATSIZEZ,VOXSIZEX,VOXSIZEY,VOXSIZEZ,ITERATIONS):
    ##--Amend template PBS file-------------------------------------------------
    PBSfileRAW = open('./RunJob_template.pbs', 'r') #imports the template PBS file
    pbs = PBSfileRAW.read() #converts the imported template file into  string, stored in pbs
    PBSfileRAW.close() #closes the template file

    #creates new RunJob_STUDYx_RECONTYPEx.pbs file
    pbsfilenewpath = './'+STUDY+'/RunJob_'+STUDY+'_'+RECONTYPE+'.pbs'
    makedirnfile(pbsfilenewpath)
    PBSfileNEW = open(pbsfilenewpath,'w')

    #define dictionary for search and replace
    searchnreplace = {'DATEx':DATE, 'STUDYx':STUDY,
        'PROCESSPATHx':processpath, 'DATAPATHx':datapath, 'NORMPATHx':normpath,
        'SUBSETSx':SUBSETS, 'FRAMETIMEx':FRAMETIME,
        'XVALUEx':XVALUE, 'RECONPATHx':reconpath, 'RECONTYPEx':RECONTYPE}

    #replace target words with user input variables
    pbs = replace_all(pbs, searchnreplace)
    PBSfileNEW.write(pbs) #write amended pbs contents in new .pbs file
    PBSfileNEW.close() #write to disk

    #--Amend reconstruction_parameters file-------------------------------------
    RPfileRAW = open('./reconstruction_parameters_template.par', 'r') #imports the template par file
    reconpar = RPfileRAW.read() #converts the imported template file into something readable, stored in reconpar
    RPfileRAW.close() #closes the template file

    #creates new reconstruction_parameters_STUDYx_RECONTYPEx.par file
    rpfilenewpath = './'+STUDY+'/reconstruction_parameters_'+STUDY+'_'+RECONTYPE+'.par'
    makedirnfile(rpfilenewpath)
    RPfileNEW = open(rpfilenewpath,'w')

    #define dictionary for search and replace
    searchnreplace2 = {'MATSIZEX':MATSIZEX, 'MATSIZEY':MATSIZEY,
        'MATSIZEZ':MATSIZEZ, 'VOXSIZEX':VOXSIZEX, 'VOXSIZEY':VOXSIZEY,
        'VOXSIZEZ':VOXSIZEZ, 'FRAMETIMEx':FRAMETIME, 'SUBSETSx':SUBSETS,
        'ITERATIONSx':ITERATIONS, 'SYSPATHx':syspath, 'NORMPATHx':normpath,
        'DATAPATHx':datapath, 'DATEx':DATE, 'STUDYx':STUDY,
        'RECONTYPEx':RECONTYPE}

    #replace target words with user input variables
    reconpar = replace_all(reconpar, searchnreplace2)
    RPfileNEW.write(reconpar) #write amended reconpar contents into new .par file
    RPfileNEW.close() #write to disk

    #--Amend trdatlorebindat_generator file-------------------------------------
    GENfileRAW = open('./trdatlorebindat_generator_template.txt','r')
    gendata = GENfileRAW.read()
    GENfileRAW.close()

    #creates new trlorebindat_generator_STUDYx file
    genfilenewpath = './'+STUDY+'/trdatlorebindat_generator_'+STUDY
    makedirnfile(genfilenewpath)
    GENfileNEW = open(genfilenewpath,'w')

    #define dictionary for search and replace
    searchnreplace3 = {'IDLPATHx':idlpath, 'DATEx':DATE, 'STUDYx':STUDY,
        'SMOOTHx':SMOOTH, 'STYPEx':str(STYPE), 'PROCESSPATHx':processpath,
        'DATAPATHx':datapath}

    #replace target words with user input variables
    gendata = replace_all(gendata, searchnreplace3)
    GENfileNEW.write(gendata)
    GENfileNEW.close()

#run the file maker function
fmaker(idlpath,processpath,reconpath,normpath,datapath,syspath,STUDY,DATE,STYPE,SMOOTH,SUBSETS,RECONTYPE,FRAMETIME,XVALUE,MATSIZEX,MATSIZEY,MATSIZEZ,VOXSIZEX,VOXSIZEY,VOXSIZEZ,ITERATIONS)

todo = 'empty'
while todo != '2':
    print('     Would you like to specify another type of recontruction for this study (0), another study (1), or are we ready to submit our jobs to PBS (2)?')
    todo = raw_input()
    print('')

    if todo == '0':
        print('     Specify type of reconstruction - static or dynamic')
        RECONTYPE = raw_input()
        print('')

        if RECONTYPE == 'static':
            print('     Specify background frame duration and effective scan duration e.g. 276*1,3600*1 \
                        note: to obtain a static scan of the last 30 mn of effective scan, input might be 276*1,1800*2 \
                                You would then discard the first two \'frames\'')
            FRAMETIME = raw_input()
            print('')

        if RECONTYPE == 'dynamic':
            print('     Specify duration of frames (in s) and number of frames with that duration e.g 276*1,300*12')
            print('     CAREFUL! DONT EXCEED DURATION OF .lst')
            FRAMETIME = raw_input()
            print('')

        fmaker(idlpath,processpath,reconpath,normpath,datapath,syspath,STUDY,DATE,STYPE,SMOOTH,SUBSETS,RECONTYPE,FRAMETIME,XVALUE,MATSIZEX,MATSIZEY,MATSIZEZ,VOXSIZEX,VOXSIZEY,VOXSIZEZ,ITERATIONS)

    elif todo == '1':
        print('     What is this study? e.g. Rat3Scan2')
        STUDY = raw_input()
        print('')

        print('     What was the study date? e.g. 20180725')
        DATE = raw_input()
        print('')

        print('     Specify type of reconstruction - static or dynamic')
        RECONTYPE = raw_input()
        print('')

        if RECONTYPE == 'static':
            print('     Specify background frame duration and effective scan duration e.g. 276*1,3600*1 \
                        note: to obtain a static scan of the last 30 mn of effective scan, input might be 276*1,1800*2 \
                                You would then discard the first two \'frames\'')
            FRAMETIME = raw_input()
            print('')
        if RECONTYPE == 'dynamic':
            print('     Specify duration of frames (in s) and number of frames with that duration e.g 276*1,300*12')
            print('     CAREFUL! DONT EXCEED DURATION OF .lst')
            FRAMETIME = raw_input()
            print('')

        fmaker(idlpath,processpath,reconpath,normpath,datapath,syspath,STUDY,DATE,STYPE,SMOOTH,SUBSETS,RECONTYPE,FRAMETIME,XVALUE,MATSIZEX,MATSIZEY,MATSIZEZ,VOXSIZEX,VOXSIZEY,VOXSIZEZ,ITERATIONS)

print('')
print('     Were done here. See you soon!')

print('')
print('Now for consistency, move the new RunJob_STUDYx_RECONTYPEx.pbs and reconstruction_parameters_STUDYx_RECONTYPEx.par files to the appropriate STUDYx directory')
print('')

exit()
