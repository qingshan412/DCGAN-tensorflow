from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s","--SampleDir", type=str,
                    help="directory for samples",
                    default = 'samples')
parser.add_argument("-r","--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors')
parser.add_argument("-t","--Threshold", type=float,
                    help="threshold for every placement",
                    default = 0.9)
args = parser.parse_args()


PicPath = args.SampleDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

print(len(PicFiles))

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

print(AllPx)
print(AllPx.shape)

AllPxs = AllPx
### Place Sensors
Places = []
for i in xrange(Nsensor):
    print(i)
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1:
        print('All covered')
        break
    ### Select A Sensor
    idxc = np.argmax(np.sum(AllPxs, axis=0))
    Places.append(str(int(idxc)))
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)

### Store Results
if not path.exists(args.ResultDir):
    makedirs(args.ResultDir)

fo = open(path.join(args.ResultDir,'sensor_from_'+ args.SampleDir + '_' + str(threshold)),'w')
fo.write(','.join(Places))
fo.close()