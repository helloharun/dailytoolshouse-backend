from logging import raiseExceptions
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators import csrf
from pytube import YouTube
from django.views.decorators.csrf import csrf_exempt
import ffmpeg
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

'''
@csrf_exempt
def SingleVideoGenerator(request):
   print("request.POST: ", request.POST['raw_url'])
   raw_url =  request.POST['raw_url']
   try:
      yt = YouTube(raw_url)
      # print('YT.streams: ', yt.streams)
      available_video_formats = []
      for i in yt.streams.filter(file_extension='mp4').order_by('resolution'):
         print("Video: ", i.__dict__['resolution'])
         if i.__dict__['resolution'] not in available_video_formats:
            available_video_formats.append(i.__dict__['resolution'])
      print('available_video_formats: ', available_video_formats)
      print('filtered video: ',  yt.streams.filter(file_extension='mp4', resolution='144p'))
         
   except Exception as e:
      print("Exception: ", e)
   
   return HttpResponse(yt.title)

@csrf_exempt
def  SingleVideoDownloader(request):
   selected_video_format =  request.POST['selected_video_format']
   raw_url =  request.POST['raw_url']
   try:
      yt = YouTube(raw_url)     
      # print('filtered video: ',  yt.streams.filter(file_extension='mp4', resolution=selected_video_format))

      vid =  yt.streams.filter(file_extension='mp4', resolution=selected_video_format)
      try:
         vid.first().download(filename='video.mp4')
      except Exception as e:
         print('while downloadig a video: ', e)
      available_audio_formats = []
      auds =  yt.streams.filter(only_audio=True, file_extension='webm')
      for i in auds:
         if i.__dict__['abr'] not in available_audio_formats:
            available_audio_formats.append(i.__dict__['abr'])
      available_audio_formats.sort()
      print(available_audio_formats.sort())
      aud =  yt.streams.filter(only_audio=True, abr=available_audio_formats[0])
      print('Aud: ', aud)
      try:
         aud.first().download(filename='audio.webm')
      except Exception as e:
         print('while downloadig a video: ', e)
      print(yt.title, 'downloaded')

      if os.path.exists('output.mp4'):
         os.remove('output.mp4')
      video = ffmpeg.input('video.mp4')
      audio = ffmpeg.input('audio.webm')
      out = ffmpeg.output(video,audio, 'output.mp4', vcodec='copy', acodec='aac', strict='experimental')
      out.run()
      os.remove('video.mp4')
      os.remove('audio.webm')
   except Exception as e:
      print("Exception: ", e)
   
   return HttpResponse(yt.title, 'downloaded')
'''
      
# @csrf_exempt
@api_view(['POST'])
def OneHighestVideoDownloader(request):
   if request.method == 'POST':
      # print(request.data)
      raw_youtube_url = request.data['raw_youtube_url']
      
      yt = YouTube(raw_youtube_url)

      vids = yt.streams.filter(progressive=True)
      
      available_video_resolution = []
      for i in vids:
         if i.__dict__['resolution'] not in available_video_resolution:
            available_video_resolution.append(i.__dict__['resolution'])
      
      '''
      Sorting formats in ascending order
      '''
      
      available_video_resolution.sort()
      
      vids.filter(resolution=available_video_resolution[-1]).first().download()
      return Response({
         'msg':'Video downloaded!',
         'status':'success',
         'code':'200'
      })
      