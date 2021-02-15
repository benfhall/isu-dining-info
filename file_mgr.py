import os
import numpy as np 

async def save_scores(name,old_arr):
    array = np.array(old_arr)
    with open(name, 'wb') as f:
        np.save(f, np.array(array))

async def load_scores(name):
    with open(name, 'rb') as f:
        return np.load(f,None,True)
            