import time
import numpy as np
from keras import backend as K
from keras.models import load_model
from music_tagger_cnn import MusicTaggerCNN
from music_tagger_crnn import MusicTaggerCRNN
import audio_processor as ap
import pdb
import os, glob

def sort_result(tags, preds):
    result = zip(tags, preds)
    sorted_result = sorted(result, key=lambda x: x[1], reverse=True)
    return [(name, '%5.3f' % score) for name, score in sorted_result]


def librosa_exists():
    try:
        __import__('librosa')
    except ImportError:
        return False
    else:
        return True

def store_csv(result):
    import csv
    result = result[0:25]
    with open(os.path.join(os.getcwd(), 'musictagger','static', 'music_tag.csv'), 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        f.write('Tag')
        f.write(',')
        f.write('Value')
        f.write('\n')
        for row in result:
            for i, column in enumerate(row):
                f.write(str(column))

                if i != len(row)-1:
                    f.write(',')
            f.write('\n')

# def music_tagger():

net = 'crnn'
''' *WARNIING*
This model use Batch Normalization, so the prediction
is affected by batch. Use multiple, different data 
samples together (at least 4) for reliable prediction.'''

print('Running main() with network: %s and backend: %s' % (net, K._BACKEND))
# setting
# audio_paths = ['data/bensound-cute.mp3',
#                'data/bensound-actionable.mp3',
#                'data/bensound-dubstep.mp3',
#                'data/bensound-thejazzpiano.mp3']
audio_paths = glob.glob(os.path.join(os.getcwd(), 'musictagger','media', 'extracted_audio')+os.sep+'*')

melgram_paths = ['data/bensound-cute.npy',
                 'data/bensound-actionable.npy',
                 'data/bensound-dubstep.npy',
                 'data/bensound-thejazzpiano.npy']

tags = ['rock', 'pop', 'alternative', 'indie', 'electronic',
        'female vocalists', 'dance', '00s', 'alternative rock', 'jazz',
        'beautiful', 'metal', 'chillout', 'male vocalists',
        'classic rock', 'soul', 'indie rock', 'Mellow', 'electronica',
        '80s', 'folk', '90s', 'chill', 'instrumental', 'punk',
        'oldies', 'blues', 'hard rock', 'ambient', 'acoustic',
        'experimental', 'female vocalist', 'guitar', 'Hip-Hop',
        '70s', 'party', 'country', 'easy listening',
        'sexy', 'catchy', 'funk', 'electro', 'heavy metal',
        'Progressive rock', '60s', 'rnb', 'indie pop',
        'sad', 'House', 'happy']

# prepare data like this
melgrams = np.zeros((0, 1, 96, 1366))

if librosa_exists:
    for audio_path in audio_paths:
        print 'extracting audio: ', audio_path
        melgram = ap.compute_melgram(audio_path)
        melgrams = np.concatenate((melgrams, melgram), axis=0)
else:

    for melgram_path in melgram_paths:
        print 'loading melgram: ', melgram_path
        melgram = np.load(melgram_path)
        melgrams = np.concatenate((melgrams, melgram), axis=0)

# load model like this
if net == 'cnn':
    model = MusicTaggerCNN(weights='msd')
elif net == 'crnn':
    # model = MusicTaggerCRNN(weights='msd')
    # model.save('/Users/Frank/Documents/UCSC/TIM_209/project/demo/test/mysite/trips/music-auto-tagging/music_tagger_crnn.model.h5')
    model = load_model(os.path.join(os.getcwd(), 'musictagger', 'music-auto-tagging', 'music_tagger_crnn.model.h5'))
# predict the tags like this
print('Predicting...')
start = time.time()
pred_tags = model.predict(melgrams)
# print like this...
print "Prediction is done. It took %d seconds." % (time.time()-start)
print('Printing top-10 tags for each track...')
for song_idx, audio_path in enumerate(audio_paths):
    sorted_result = sort_result(tags, pred_tags[song_idx, :].tolist())
    store_csv(sorted_result)
    # print(audio_path)
    # print(sorted_result[:5])
    # print(sorted_result[5:10])
    # print(' ')

# return

# if __name__ == '__main__':

# networks = ['crnn']
# for net in networks:
#     main(net)
