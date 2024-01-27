import requests
from django.shortcuts import render
from django.http import StreamingHttpResponse

import yt_dlp

from utils.constants import *
from utils.helper import *


def home(request):
    context = {
        'title': "HOME | YTVidDownloaderWeb",
    }

    if request.method == 'POST':
        url = request.POST.get('url')
        with yt_dlp.YoutubeDL() as ytdlp:
            video_info = ytdlp.extract_info(url, download=False)

        video_title = video_info.get("title", NOT_AVAILABLE)
        formats = video_info.get("formats", NOT_AVAILABLE)
        channel_url = video_info.get("channel_url", NOT_AVAILABLE)
        channel_name = video_info.get("channel", NOT_AVAILABLE)
        video_duration = video_info.get("duration", NOT_AVAILABLE)
        video_id = video_info.get("id", NOT_AVAILABLE)
        thumbnail_url = video_info.get("thumbnail", NOT_AVAILABLE)

        _, video_with_audio_formats = get_video_with_audio_formats(formats)
        _, audio_only_formats = get_audio_only_formats(formats)
        _, video_only_formats = get_video_only_formats(formats)
        context = {
            'title': video_title,
            'url': url,
            'video_id': video_id,
            'video_title': video_title,
            'video_duration': get_formatted_time(video_duration),
            'channel_name': channel_name,
            'channel_url': channel_url,
            'thumbnail_url': thumbnail_url,
            'formats': {
                "video_with_audio_formats": video_with_audio_formats,
                "audio_only_formats": audio_only_formats,
                "video_only_formats": video_only_formats,
            },
        }
        render(request, 'home/home.html', context)
    
    return render(request, 'home/home.html', context)

def download(request):
    url = request.GET.get('url')
    filename = request.GET.get('filename')
    ext = request.GET.get('ext')
    format_id = request.GET.get('fmt_id')
    filename = f'{filename}_{format_id}.{ext}'
    filename = sanitize_filename(filename)
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    res = requests.get(url, headers=headers, stream=True)
    content_length = res.headers.get('Content-Length')
    content_type = res.headers.get('Content-Type')
    
    response_headers = {
        'Content-Disposition': f'attachment; filename={filename}',
        'Content-Type': content_type,
        'Content-Length': int(content_length),
    }
    response = StreamingHttpResponse(
        res.iter_content(chunk_size=1024*1024),
        headers=response_headers,
    )
    return response