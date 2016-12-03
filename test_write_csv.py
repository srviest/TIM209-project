
import csv

test = [('jazz', '0.299'), ('instrumental', '0.174'), ('electronic', '0.089'), ('ambient', '0.061'), ('chillout', '0.052')]

with open('/Users/Frank/Documents/UCSC/TIM_209/project/music_tag.csv', 'w') as f:
	writer = csv.writer(f, delimiter='\t')
	f.write('Tag')
	f.write(',')
	f.write('Value')
	f.write('\n')
	for row in test:
		for i, column in enumerate(row):
			f.write(str(column))

			if i != len(row)-1:
				f.write(',')
		f.write('\n')