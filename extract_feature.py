#!/usr/bin/env python
# encoding: utf-8
"""
Author: Yuan-Ping Chen
Data: 2016/11/7
"""

import librosa
import os, sys, glob
import numpy as np

def extract_feature(input_dir, ouput_dir):
	for root, dirs, files in os.walk(input_dir):
		# print root
		files = [f for f in files if not f[0] == '.']
		print 'root:', root
		for f in files:
			# print os.path.join(root, f)
			# print root
			# print f
			file_path = os.path.join(root, f)
			print 'file:', file_path
			y, sr = librosa.load(file_path, sr=22050, duration=30)
			S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=96)
			D = librosa.logamplitude(S,ref_power=np.max)
			if S.shape[0]!=96:
				print S.shape
			feature_dir = ouput_dir+os.sep+root.split('/')[-1]
			if not os.path.exists(feature_dir):
				os.makedirs(feature_dir)
			feature_name = f.split('.')[0]+'.'+f.split('.')[1]+'.melgram.npy'
			np.save(feature_dir+os.sep+feature_name, D)
	
if __name__ == '__main__':

	input_dir = '/Users/Frank/Documents/UCSC/TIM_209/project/genres'
	ouput_dir = '/Users/Frank/Documents/UCSC/TIM_209/project/feature'
	extract_feature(input_dir, ouput_dir)

