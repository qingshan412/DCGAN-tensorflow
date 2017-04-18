from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s","--SampleDir", type=str,
                    help="directory for samples",
                    default = 'samples/100o')
parser.add_argument("-r","--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors')
parser.add_argument("-t","--Threshold", type=float,
                    help="threshold for every placement",
                    default = 0.9)
args = parser.parse_args()


PicPath = args.SampleDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

print('There are ' + str(len(PicFiles)) + ' files')

#px_per_pic = 1082
Nsensor = 9
threshold = args.Threshold

### Read Pixels Out
countflag = 0
for Pic in PicFiles:
    tmp = Image.open(os.path.join(PicPath, Pic))
    line3 = np.array(tmp)
    line4 = line3 > .9*255
    line4 = np.reshape(1*line4,(1082,))
    #print(line4.size)
    print(line4)
    linemin = np.amin(line4)
    linemax = np.amax(line4)
    print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))

    if countflag == 0:
        AllPx = line4
    else:
        AllPx = np.vstack((AllPx, line4))
    #line3 = np.reshape(line3, (2,541))
    #im = Image.fromarray(line3)
    #im.save(str(i) + '.png')
    countflag = countflag + 1
    #raw_input('...')

print('end_data')

AllPxs = AllPx
Places = []
for i in xrange(Nsensor):
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1:
        print('All covered')
        break
    print(str(i+1) + '-th sensor...')
    ### Select A Sensor
    print(np.unique(np.sum(AllPxs, axis=0)))
    idxc = np.argmax(np.sum(AllPxs, axis=0))
    Places.append(str(int(idxc)))
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)

### Store Results
if not path.exists(args.ResultDir):
    makedirs(args.ResultDir)

fo = open(path.join(args.ResultDir,'sensor_from_'+ path.basename(args.SampleDir) + '_' + str(threshold)),'w')
fo.write(','.join(Places))
fo.close()