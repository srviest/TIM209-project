
import os, glob, sys
import numpy as np
import math
import multiprocessing as mp
from sklearn.preprocessing import Imputer, scale, robust_scale, StandardScaler, RobustScaler

def standadization(X):
    # replace nan feature with the median of column values
    # imp = Imputer(missing_values='NaN', strategy='median', axis=0)
    # raw_data = imp.fit_transform(raw_data)

    # # remove inf and -inf
    # if np.where(np.isinf(raw_data)==True)[0].size!=0:
    #     print 'Removing Inf and -Inf values...'
    #     med = np.median(raw_data, axis=0)
    #     axis_0 = np.where(np.isinf(raw_data)==True)[0]
    #     axis_1 = np.where(np.isinf(raw_data)==True)[1]
    #     for index in range(len(axis_0)):
    #         raw_data[axis_0[index], axis_1[index]]=med[axis_1[index]]

    # standardization
        
    scaler = StandardScaler().fit(X)
    X_stdized = scaler.transform(X)
    
    return X_stdized

def load_data(data_path):
    
    file_path_all = []
    for root, dirs, files in os.walk(data_path):
        # print root
        files = [f for f in files if not f[0] == '.']
        # print 'root:', root
        for f in files:
            file_path = os.path.join(root, f)
            file_path_all+=[file_path]

    mup = mp.Pool(processes=20)
    data = np.array(mup.map(np.load, file_path_all))
    mup.close()
    mup.join()

    return data


def main():
    data_path='/Users/Frank/Documents/UCSC/TIM_209/project/feature'
    # data_save_path='/Users/Frank/Documents/UCSC/TIM_209/project'
    label_path='/Users/Frank/Documents/UCSC/TIM_209/project/label.txt'
    
    X=load_data(data_path)
    mean=np.mean(X, axis=0)
    std=np.std(X, axis=0)
    X=(X-mean)/std
    y=np.loadtxt(label_path).astype(int)

    # # print 'Splitting data into training set and testing set...'
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # data pre-processing 
    print 'Reshape data to fit CNN input...'
    X = X.reshape(X.shape[0], 1, X.shape[1], X.shape[2])
    
    

    # model = build_model()
    # train_and_evaludate(X_train, X_test, y_train, y_test, model)

if __name__ == '__main__':
    main()

