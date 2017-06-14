from __future__ import division
from PIL import Image
from os import listdir, path, makedirs
#from os.path import isfile, join, exist
import numpy as np
import argparse

#np.save("AllPxs.npy",AllPx)
#np.save("AllPxsF.npy",AllPxF)
# numpy.load("AllPxs.npy")
AllPxsF = np.load("AllPxsF.npy")
AllPxs = np.load("AllPxs.npy")
print('AllPxs:')
print(AllPxs.dtype)
print(AllPxs.shape)
print(AllPxs[0].dtype)
sumPxs = np.sum(AllPxs, axis=0)
uni, unicon = np.unique(sumPxs, return_counts=True)
print(uni)
print(unicon)
if (0 in uni):
    NewPxs = np.delete(AllPxsF,np.where(sumPxs == 0),axis=1)
    print(NewPxs.shape)
    rtmpdirtr='data/ibmpg1t1/lrtr'
    rtmpdirte='data/ibmpg1t1/lrte'
    stmpdirtr='data/ibmpg1t1/lstr'
    stmpdirte='data/ibmpg1t1/lste'
    i = 0
    for line in NewPxs:
        print(i)
        #print(line.shape)
        line = np.reshape(line, (36,1))
        #print(line.shape)
        im = Image.fromarray(line)
        seed = np.random.random()
        if seed < 0.5:
            im.save(path.join(rtmpdirtr, str(i) + '.png'))
        else:
            im.save(path.join(rtmpdirte, str(i) + '.png'))
        ### sequentially divide data into train and test datasets
        if i%2 < 1:
            im.save(path.join(stmpdirtr, str(i) + '.png'))
        else:
            im.save(path.join(stmpdirte, str(i) + '.png'))
        i = i + 1
else:
    print('No features to remove!')