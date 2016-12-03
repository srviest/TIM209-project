
import glob
import multiprocessing as mp
import numpy as np


data_path='/Users/Frank/Documents/UCSC/TIM_209/project/feature'
label_path='/Users/Frank/Documents/UCSC/TIM_209/project/label.txt'

def load_data(data_path):

    
    file_path_all = []
    for root, dirs, files in os.walk(data_path):
        # print root
        files = [f for f in files if not f[0] == '.']
        # print 'root:', root
        for f in files:
            file_path = os.path.join(root, f)
            file_path_all+=[file_path]
        
    d=np.load(file_path_all[0]).shape
    data=np.empty([0,d[0],d[1]])

    for f in file_path_all:
        feature=np.load(f)
        f_dim=feature.shape[0]
        t_dim=feature.shape[1]
        data = np.append(data, feature.reshape(1, f_dim, t_dim), axis=0)

    return data

afp = '/Users/Frank/Documents/UCSC/TIM_209/project/feature/blues/'
asid = glob.glob(afp+"*.npy")


def loads_x(path):
	x = np.load(path)

	return x


mup = mp.Pool(processes=20)
x = np.array(mup.map(loads_x, asid))
mup.close()
mup.join()

print x.shape