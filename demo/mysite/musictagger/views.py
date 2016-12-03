# Create your views here.
from .models import Post
from datetime import datetime
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from .forms import NameForm
from video_handler import get_video
import sys, os
import subprocess

# sys.path.append('/Users/Frank/Documents/UCSC/TIM_209/project/demo/test/mysite/trips/music-auto-tagging')

# from music_tagger import music_tagger


def result(request):
    return render(request, 'test_2.html', {
        'current_time': str(datetime.now()),
    })

def home(request):
    return render(request, 'hello_world.html', {
        'current_time': str(datetime.now()),
    })

class urlForm(forms.Form):
    url = forms.CharField(label='url', max_length=100)


def get_name(request):
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # form = NameForm(request.POST)
        # check whether it's valid:
        # if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    # else:
        # form = NameForm()
    get_video(request.POST['url'])
    subprocess.call('python ./musictagger/music-auto-tagging/music_tagger.py', shell=True)
    os.remove(os.path.join(os.getcwd(), 'musictagger/media/extracted_audio/audio.wav'))
    return render(request, 'tag_render.html', {'Test': request.POST['url']})


#test video url:
#https://youtu.be/oFUYnR90c3s
