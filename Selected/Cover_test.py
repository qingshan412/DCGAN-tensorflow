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
    #if countflag> 10:
    #    break
    tmp = Image.open(path.join(PicPath, Pic))
    print('\n\n\n' + str(countflag) + ':')
    line3 = np.array(tmp.convert('L'))
    print(line3.shape)
    print(line3)
    line3 = np.vsplit(line3, 8)#line4 = line3 > .9*255
    line4 = [np.hsplit(item, 8) for item in line3]
    print(len(line4))
    print(len(line4[0]))
    print(line4[0][0])
    print(line4[0][7])
    print(line4[7][0])
    print(line4[7][7])

    for i in xrange(len(line4)):
        item = line4[i]
        for j in xrange(len(item)):
            if i == 0 and j == 0:
                line5 = np.reshape(item[j],(1082, ))
                #print(line5.shape)
                #print(line5)
                #raw_input('...')
            else:
                line5 = np.vstack((line5, np.reshape(item[j],(1082, ))))
                #if (i == 0 and j == 7) or (i == 7 and j == 0) or (i == 7 and j == 7):
                #    print(line5.shape)
                #    print(line5)
                #    raw_input('...')
            
    line6 = line5 > .9*255#line4 = np.reshape(1*line4,(2,541,-1))
    line6 = 1*line6
    print(line6.shape)
    #print(line4.shape)
    print(line6)
    line7 = np.sum(line6, axis = 1)
    linemin = np.amin(line7)
    linemax = np.amax(line7)
    print(str(countflag) + ': min- ' + str(linemin) + ' max- ' + str(linemax))
    #raw_input('...')
    if countflag == 0:
        AllPx = line6
    else:
        AllPx = np.vstack((AllPx, line6))
    #line3 = np.reshape(line3, (2,541))
    #im = Image.fromarray(line3)
    #im.save(str(i) + '.png')
    countflag = countflag + 1
    #raw_input('...')

print('end_data')
#exit(0)

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
    print(idxc)
    Places.append(str(int(idxc)))
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)

### Store Results
#if not path.exists(args.ResultDir):
#    makedirs(args.ResultDir)

#fo = open(path.join(args.ResultDir,'sensor_from_'+ path.basename(args.SampleDir) + '_' + str(threshold)),'w')
#fo.write(','.join(Places))
#fo.close()