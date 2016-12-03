#!/usr/bin/env python
# encoding: utf-8
"""
Author: Yuan-Ping Chen
Data: 2016/11/8
"""
import numpy as np
import os,sys,glob
from sklearn.model_selection import StratifiedKFold

def shuffle_indice(input_dir, output_dir, ratio):

	classes_label_dic = {'blues':0, 
						'classical':1, 
						'country':2, 
						'disco':3, 
						'hiphop':4, 
						'jazz':5, 
						'metal':6, 
						'pop':7, 
						'reggae':8, 
						'rock':9}
	label_all = []
	count = 0
	# count the number of all instances
	for root, dirs, files in os.walk(input_dir):
		# print root
		files = [f for f in files if not f[0] == '.']
		print 'root:', root
		for f in files:

			label = []
			# print os.path.join(root, f)
			# print root
			# print f
			file_path = os.path.join(root, f)
			# print 'file:', file_path
			F = np.load(file_path)
			count+=1
			# inspect the feature dimensin and padding
			if F.shape!=(96, 1292):
				print file_path
				print 'Dimension error:', F.shape
				num_2_pad = 1292-F.shape[1]
				F = np.pad(F, ((0,0), (0,num_2_pad)), mode='edge')
				print 'Dimension after padding:', F.shape
				np.save(file_path, F)
			# make label
			genre = root.split('/')[-1]
			label = [classes_label_dic[c] for c in classes_label_dic.keys() if genre==c]
			label_all+=label

			# feature_dir = ouput_dir+os.sep+root.split('/')[-1]
	print 'Number of instances:', count
	# print 'label_all: ', label_all
	# save the labels					 		
	if not os.path.exists(output_dir): os.makedirs(output_dir)
	np.savetxt(output_dir+os.sep+'label.txt', label_all, fmt='%s')

	fold = int(1/ratio[-1])

	# split labels
	print 'Shuffling the samples and dividing them into ', fold, ' folds...'
	CVfold = StratifiedKFold(label_all, fold, shuffle=True)
	for train_indices, test_indices in CVfold:
		print 'train_indices: ',train_indices
		print 'test_indices: ',test_indices
	# save cv-folds
	np.save(output_dir+os.sep+'CVFold.npy', CVfold)
	

def main():

	trainin_validation_testing_ratio = [0.75, 0.25]
	input_dir='/Users/Frank/Documents/UCSC/TIM_209/project/feature'
	output_dir='/Users/Frank/Documents/UCSC/TIM_209/project'
	shuffle_indice(input_dir, output_dir, trainin_validation_testing_ratio)


if __name__ == '__main__':
	main()