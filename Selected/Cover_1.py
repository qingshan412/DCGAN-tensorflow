from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s","--SampleDir", type=str,
                    help="directory for samples",
                    default = '../data/pre_noise/1_s_41_p')
parser.add_argument("-r","--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors/sensor_from_1_s_4_p_0.9')
parser.add_argument("-a","--AfterDir", type=str,
                    help="directory for results after covering",
                    default = 'after')
parser.add_argument("-t","--Threshold", type=float,
                    help="threshold for every placement",
                    default = 0.9)
args = parser.parse_args()


PicPath = args.SampleDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

print(str(len(PicFiles)) + ' files.')

px_per_pic = 1082
Nsensor = 9
threshold = args.Threshold

### Read Pixels Out
i = 0
for Pic in PicFiles:
    tmp = Image.open(path.join(PicPath,Pic))
    line3 = np.array(tmp)
    line4 = line3 > threshold*255
    line4 = np.reshape(1*line4,(1082,))
    #print(line4.size)
    print(line4)
    linemin = np.amin(line4)
    linemax = np.amax(line4)
    print(str(i) + ': min- ' + str(linemin) + ' max- ' + str(linemax))

    if i == 0:
        AllPx = line4
    else:
        AllPx = np.vstack((AllPx, line4))
    #line3 = np.reshape(line3, (2,541))
    #im = Image.fromarray(line3)
    #im.save(str(i) + '.png')
    i = i + 1
    #raw_input('...')
print('end')

Nsensor = 5
AllPxs = AllPx

PlacePath = args.ResultDir
line = open(PlacePath).readline().strip().split(',')
line = np.array(line)
line = line.astype(np.int)
Places = list(line)

After = args.AfterDir
fo = open(path.join(After,'result_after_' + path.basename(PlacePath) + '_in_' + path.basename(PicPath)), 'w')
#Places = [56, 219, 365, 47, 251, 34, 807, 48, 416, 3]
for i in xrange(len(Places)):
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1:
        fo.write('All covered')
        break
    fo.write(str(i+1) + '-th sensor...\n')
    print(str(i+1) + '-th sensor...')
    ### Select A Sensor
    uni, unicon = np.unique(np.sum(AllPxs, axis=0), return_counts=True)
    fo.write(','.join(list(uni.astype(str))))
    fo.write('\n')
    fo.write(','.join(list(unicon.astype(str))))
    fo.write('\n')
    print(uni)
    print(unicon)
    for item in uni:
        if item > 0:
            fo.write(str(item) + ':\n')
            fo.write(','.join(list(np.where(uni == item)[0].astype(str))))
            fo.write('\n')
            print(str(item) + ':')
            print(np.where(uni == item)[0])
    #idxc = np.argmax(np.sum(AllPxs, axis=0))
    idxc = Places[i]
    #Places.append(str(int(idxc)))
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], axis=0)

fo.close()
exit(0)