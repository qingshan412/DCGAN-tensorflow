from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s","--SampleDir", type=str,
                    help="directory for samples",
                    default = '../data/pre_noise/ibm1jpg41')
parser.add_argument("-r","--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors')
parser.add_argument("-t","--Threshold", type=float,
                    help="threshold for every placement",
                    default = 0.9)
args = parser.parse_args()


PicPath = args.SampleDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='jpg']

print(str(len(PicFiles)) + ' files.')

px_per_pic = 1082
Nsensor = 9
threshold = args.Threshold

### Read Pixels Out
countflag = 0
for Pic in PicFiles:
    Im = Image.open(path.join(PicPath, Pic))
    Im = Im.convert('L')
    pic_per_Pic = Im.size[1]*Im.size[1]
    Px = np.asarray(Im) > threshold*255
    ImPx = np.reshape(1*Px,(pic_per_Pic,-1))
    if countflag == 0:
        AllPx = ImPx
    else:
        AllPx = np.vstack((AllPx, ImPx))
    countflag = countflag + 1
    print(countflag)

print(AllPx)
print(AllPx.shape)

AllPxs = AllPx
### Place Sensors
Places = [535, 85, 11]
for i in xrange(len(Places)):
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1:
        print('All covered')
        break
    ### Select A Sensor
    print(np.unique(np.sum(AllPxs, axis=0)))
    #idxc = np.argmax(np.sum(AllPxs, axis=0))
    #Places.append(str(int(idxc)))
    idxc = Places[i]
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)
    print(str(i+1) + '-th sensor...')
    print('Left uncovered:')
    print(AllPxs.shape)


### Store Results
#if not path.exists(args.ResultDir):
#    makedirs(args.ResultDir)

#fo = open(path.join(args.ResultDir,'cover1_from_'+ path.basename(args.SampleDir) + '_' + str(threshold)),'w')
#fo.write(','.join(Places))
#fo.close()