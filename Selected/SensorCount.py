from PIL import Image
from os import listdir, path
#from os.path import isfile, join, exist
import numpy as np
from __future__ import division
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--SampleDir", type=str,
                    help="directory for samples",
                    default = 'samples')
parser.add_argument("--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors')
args = parser.parse_args()


PicPath = args.SampleDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

px_per_pic = 1082
Nsensor = 9
threshold = 0.9

### Read Pixels Out
count = 0
for Pic in PicFiles:
    Im = Image.open(Pic)
    Im = Im.convert('L')
    pic_per_Pic = Im.size(1)*Im.size(1)
    Px = np.asarray(Im) > threshold*255
    ImPx = np.reshape(1*Px,(pic_per_Pic,-1))
    if count == 0:
        AllPx = ImPx
    els0e:
        AllPx = np.vstack((AllPx, ImPx))

AllPxs = AllPx
### Place Sensors
Places = []
for i in xrange(Nsensor):
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1:
        print('All covered')
        break
    ### Select A Sensor
    idxc = np.argmax(np.sum(AllPxs, axis=0))
    Places.append(idxc)
    col = AllPxs[:,idxc]
    idxt = numpy.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)

### Store Results
if not path.exists(args.ResultDir):
    os.makedirs(args.ResultDir)

fo = open(path.join(args.ResultDir,'sensor_from_'+args.SampleDir),'w'
fo.write(','.join(Places))
fo.close()