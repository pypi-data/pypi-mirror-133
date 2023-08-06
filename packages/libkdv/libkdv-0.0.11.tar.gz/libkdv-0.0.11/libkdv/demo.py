from . import compute_kdv
import pandas as pd
from .utils import *
from .kdv import kdv
import os
import numpy as np


os.chdir(os.path.dirname(__file__))
    
def demo():
    kernel = kdv('Atlanta.csv')
    result = kernel.compute()
    #result.to_csv('result.csv',index=False)
    result.plot()
    #print(result[:5])
    

