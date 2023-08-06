from .compute_kdv import compute_kdv
from libkdv.utils import GPS_bound_to_XY, GPS_to_XY, XY_to_GPS, is_pandas_df, shift,to_json,parse_result, unshift
import pandas as pd
from io import StringIO
from keplergl import KeplerGl
import os
os.chdir(os.path.dirname(__file__))

class kdv:
    def __init__(self, data=None,bound=[],GPS =True,KDV_type=1,num_threads=8,
            row_pixels=800,col_pixels=640,bandwidth_s =1000,
            t_L=0,t_U=100,t_pixels=32,bandwidth_t=6):
        '''
        bound = [X_L,X_U,Y_L,Y_U] or [Lon_L,Lon_U,Lat_L,Lat_U] (You can change it)
        GPS = True #using GPS coordinate 
        KDV_type=1,2,3 #1:Normal KDV,2:Online KDV, 3:Batch-based STKDV
        num_threads=16 #The number of threads
        row_pixels=32 #number of voxels in a row 
        col_pixels=32 #number of voxels in a column 
        kernel_s_type=1 #Epanechnikov kernel (Don't change it currently)
        bandwidth_s=1000 #Spatial bandwidth 
        t_L=0 #minimum time 
        t_U=100 #maximum time 
        t_pixels=32 #number of voxels in the time-axis 
        kernel_t_type=1 #Epanechnikov kernel (Don't change it currently)
        bandwidth_t=6 #Temporal bandwidth 
        '''
        kernel_s_type = 1 
        kernel_t_type = 1 
        
        self.GPS = GPS
        self.data = pd.DataFrame()
        self.bound = [0,0,0,0]
        self.KDV_type = KDV_type
        self.num_threads = num_threads
        self.row_pixels = row_pixels
        self.col_pixels = col_pixels
        self.kernel_s_type = kernel_s_type
        self.bandwidth_s = bandwidth_s
        self.t_L = t_L
        self.t_U = t_U
        self.t_pixels = t_pixels
        self.kernel_t_type = kernel_t_type
        self.bandwidth_t = bandwidth_t
        
        self.set_data(data)
        self.set_bound(bound)


                
    
    def set_data(self,data):
        if data is None:
            return
        if not is_pandas_df(data):
            try:
                data = pd.read_json(data)
            except:
                data = pd.read_csv(data)
        if self.GPS:
            self.middle_lat = min(data['lat'])+max(data['lat'])/2
            GPS_to_XY(data,self.middle_lat)


        self.min_x,self.min_y = shift(data)
        if 'w' not in data:
            data['w'] = 1
        self.data = data
        
        if self.KDV_type == 1:
            self.data_str = str(self.data[['x','y','w']].to_csv(index=False, float_format = '%.16f'))
        else:
            self.data_str = str(self.data[['x','y','t','w']].to_csv(index=False,float_format = '%.16f'))
        
              
    def set_bound(self,bound):
        try:
            if len(bound) !=4:
                bound = None
            if bound ==[0,0,0,0]:
                bound = None
    
        except:
            bound = None 
        if bound is None:
            bound = [min(self.data['x']), max(self.data['x']),min(self.data['y']),max(self.data['y'])]
        else:
            if self.GPS:
                self.middle_lat = bound[2]+bound[3]//2
                GPS_bound_to_XY(bound,self.middle_lat)

        self.bound =bound

    def set_args(self):
        self.args =[0,
            self.data_str,
            self.KDV_type,
            self.num_threads,
            self.bound[0],
            self.bound[1],
            self.bound[2],
            self.bound[3],
            self.row_pixels,
            self.col_pixels,
            self.kernel_s_type,
            self.bandwidth_s,
            self.t_L,
            self.t_U,
            self.t_pixels,
            self.kernel_t_type,
            self.bandwidth_t,
        ]
        
        self.args = [str(x).encode('ascii') for x in self.args]
    
        
    def compute(self):
        self.set_args()
        import time
        tik = time.time()
        kdv = compute_kdv(self.args)
        tok = time.time()
        result = pd.read_csv(StringIO(kdv))
        unshift(result,self.min_x,self.min_y)
        if self.GPS:
            XY_to_GPS(result,self.middle_lat)
        
        if self.GPS:
            self.result = result[['lat','lon','val']]
        else:
            self.result = result[['x','y','val']]
        if self.KDV_type ==3:
            self.result['t'] = result['t']
            
        return self.result
    

        
    def plot(self):
        map_1 = KeplerGl()
        map_1.add_data(data=self.result,name='data_1')
        map_1.save_to_html()
        
        