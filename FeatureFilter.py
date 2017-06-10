from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-r","--RawDir", type=str,
                    help="directory for train raw samples",
                    default = '../data/1_s_4_p')
parser.add_argument("-s","--SourceDir", type=str,
                    help="directory for test raw samples",
                    default = '../data/1_s_4_p')
parser.add_argument("-r","--ResultDir", type=str,
                    help="directory for samples",
                    default = 'sensors')
parser.add_argument("-t","--Threshold", type=float,
                    help="threshold for every placement",
                    default = 0.9)
args = parser.parse_args()


PicPath = args.RawDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

print('There are ' + str(len(PicFiles)) + ' files')

#px_per_pic = 1082
#Nsensor = 9impo
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

PicPath = args.SourceDir
PicFiles = [ f for f in listdir(PicPath) if path.isfile(path.join(PicPath,f)) and f.strip().split('.')[-1]=='png']

print('2nd!\nThere are ' + str(len(PicFiles)) + ' files')

#px_per_pic = 1082
#Nsensor = 9impo
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

    #if countflag == 0:
    #    AllPx = line6
    #else:
    #    AllPx = np.vstack((AllPx, line6))
    AllPx = np.vstack((AllPx, line6))
    
    countflag = countflag + 1


print('end_data')

AllPxs = AllPx

sumPxs = np.sum(AllPxs, axis=0)
uni, unicon = np.unique(sumPxs, return_counts=True)
if (not np.any(uni)):
    NewPxs = np.delete(AllPxs,np.where(sumPxs == 0),axis=1)
    print(NewPxs.shape)
    #for line in NewPxs:
    #    line = np.reshape(line, (2,541))
    #    im = Image.fromarray(line)
    #    seed = np.random.random()
    #    if seed < 0.5:
    #        im.save(path.join(rtmpdirtr, str(i) + '.png'))
    #    else:
    #        im.save(path.join(rtmpdirte, str(i) + '.png'))
        ### sequentially divide data into train and test datasets
    #    if i%2 < 1:
    #        im.save(path.join(stmpdirtr, str(i) + '.png'))
    #    else:
    #        im.save(path.join(stmpdirte, str(i) + '.png'))
else:
    print('No features to remove!')