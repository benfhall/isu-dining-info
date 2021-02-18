import os
import numpy as np

async def save_scores(name,old_arr):
    """Save array from file"""
    array = np.array(old_arr)
    with open(name, 'wb') as f:
        np.save(f, np.array(array))

async def load_scores(name):
    """Load array from file"""
    with open(name, 'rb') as f:
        try:
            return np.load(f,None,True)
        except OSError:
            pass