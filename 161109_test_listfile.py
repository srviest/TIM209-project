
import os


def load_data(data_path):

    
	file_path_all = []
	for root, dirs, files in os.walk(data_path):
        # print root
		files = [f for f in files if not f[0] == '.']
		print 'root:', root
		for f in files:
			file_path = os.path.join(root, f)
			file_path_all+=[file_path]

    
	return file_path_all

data_path='/Users/Frank/Documents/UCSC/TIM_209/project/feature'
file_path_all =load_data(data_path)

for f in file_path_all:
	print f