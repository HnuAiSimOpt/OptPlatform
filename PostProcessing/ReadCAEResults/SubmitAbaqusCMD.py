from abaqus import *
from abaqusConstants import *
import job
import winsound
import os

setpath = r'D:\project_optPlatform\opt_platform\PostProcessing\ReadCAEResults'
os.chdir(setpath)
mdb.JobFromInputFile(name='testtc3d4', inputFileName=r'D:\project_optPlatform\opt_platform\PostProcessing\ReadCAEResults\testtc3d4.inp', numCpus=2, numDomains=2)
mdb.jobs['testtc3d4'].submit()
mdb.jobs['testtc3d4'].waitForCompletion()
winsound.Beep(1000,1000)