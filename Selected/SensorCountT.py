from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-s","--SampleDir", type=str,
                    help="directory for samples",
                    default = '../data/1_s_4_p')
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
    tmp = Image.open(path.join(PicPath, Pic))
    print('\n\n\n' + str(countflag) + ':')
    line3 = np.array(tmp.convert('L'))
    line3 = line3.flatten()
    #line3 = np.vsplit(line3, 8)
    #line4 = [np.hsplit(item, 8) for item in line3]

    #for i in xrange(len(line4)):
    #    item = line4[i]
    #    for j in xrange(len(item)):
    #        if i == 0 and j == 0:
    #            line5 = np.reshape(item[j],(1082, ))
    #        else:
    #            line5 = np.vstack((line5, np.reshape(item[j],(1082, ))))
            
    line6 = line3 > threshold*255
    line6 = 1*line6
    print(np.amax(line6))
    print(np.amin(line6))

    if countflag == 0:
        AllPx = line6
    else:
        AllPx = np.vstack((AllPx, line6))

    countflag = countflag + 1

print('end_data')

fo0 = open(path.join('process','process_sensor_from_'+ path.basename(args.SampleDir) + '_' + str(threshold)),'w')

AllPxs = AllPx
Places = []
for i in xrange(Nsensor):
    ### Check Whether There Is Noise Left
    if AllPxs.size < 1 or (not np.any(np.unique(np.sum(AllPxs, axis=0)))):
        print('All covered')
        fo0.write('All covered')
        break
    print(str(i+1) + '-th sensor...')
    fo0.write(str(i+1) + '-th sensor...')
    ### Select A Sensor
    uni, unicon = np.unique(np.sum(AllPxs, axis=0), return_counts=True)
    print(uni)
    print(unicon)
    fo0.write(','.join(list(uni.astype(str))))
    fo0.write(','.join(list(unicon.astype(str))))
    #print(np.unique(np.sum(AllPxs, axis=0)))
    idxc = np.argmax(np.sum(AllPxs, axis=0))
    print(idxc)
    fo0.write(','.join(list(idxc.astype(str))))
    Places.append(str(int(idxc)))
    col = AllPxs[:,idxc]
    idxt = np.where(col==1)
    AllPxs = np.delete(AllPxs, idxt[0], 0)


print('final:')
fo0.write('final:\n')
sumt = np.sum(AllPxs, axis=0)
uni, unicon = np.unique(sumt, return_counts=True)
fo0.write(','.join(list(uni.astype(str))))
fo0.write('\n')
fo0.write(','.join(list(unicon.astype(str))))
fo0.write('\n')
print(uni)
print(unicon)

fo0.close()
### Store Results
if not path.exists(args.ResultDir):
    makedirs(args.ResultDir)

fo = open(path.join(args.ResultDir,'sensor_from_'+ path.basename(args.SampleDir) + '_' + str(threshold)),'w')
fo.write(','.join(Places))
fo.close()