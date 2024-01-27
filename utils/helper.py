from typing import List, Tuple
import datetime
import re
import unicodedata
from utils.constants import *


def get_formatted_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024 * 1024:
        size_str = f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        size_str = f"{size_in_bytes / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
    return size_str

def get_formatted_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        formatted_time = f"{hours}:{minutes:02d}:{remaining_seconds:02d} hours"
    elif minutes > 0:
        formatted_time = f"{minutes}:{remaining_seconds:02d} minutes"
    else:
        formatted_time = f"{round(remaining_seconds)} seconds"

    return formatted_time

def get_formatted_upload_date(upload_date_str: str) -> str:
    upload_date = datetime.datetime.strptime(upload_date_str, '%Y%m%d')
    formatted_date = upload_date.strftime('%d %B, %Y')

    return formatted_date

def format_size(fmt):
    filesize = fmt.get('filesize')
    filesize_apporx = fmt.get('filesize_approx')
    downloader_options = fmt.get('downloader_options')
    if filesize:
        fmt['formatted_filesize'] = get_formatted_size(filesize)
    elif filesize_apporx:
        fmt['formatted_filesize_approx'] = get_formatted_size(filesize_apporx)
    elif downloader_options:
        http_chunk_size = downloader_options.get('http_chunk_size')
        if http_chunk_size:
            fmt['formatted_http_chunk_size'] = get_formatted_size(http_chunk_size)
    return fmt

def get_video_with_audio_formats(formats):
    video_with_audio_extensions = set()
    video_with_audio_formats = []

    for fmt in formats:
        ext = fmt.get('ext')
        if ext == 'mhtml':
            continue
        url = fmt.get('url')
        if url.startswith('https://manifest.googlevideo.com'):
            continue
        acodec = fmt.get('acodec', NONE)
        vcodec = fmt.get('vcodec', NONE)

        if (vcodec != NONE) and (acodec != NONE):
            fmt = format_size(fmt)
            video_with_audio_extensions.add(ext)
            video_with_audio_formats.append(fmt)

    return video_with_audio_extensions, video_with_audio_formats

def get_audio_only_formats(formats):
    audio_only_extensions = set()
    audio_only_formats = []

    for fmt in formats:
        ext = fmt.get('ext')
        if ext == 'mhtml':
            continue
        url = fmt.get('url')
        if url.startswith('https://manifest.googlevideo.com'):
            continue
        acodec = fmt.get('acodec', NONE)
        vcodec = fmt.get('vcodec', NONE)

        if (vcodec == NONE) and (acodec != NONE):
            fmt = format_size(fmt)
            audio_only_extensions.add(ext)
            audio_only_formats.append(fmt)

    return audio_only_extensions, audio_only_formats

def get_video_only_formats(formats):
    video_only_extensions = set()
    video_only_formats = []

    for fmt in formats:
        ext = fmt.get('ext')
        if ext == 'mhtml':
            continue
        url = fmt.get('url')
        if url.startswith('https://manifest.googlevideo.com'):
            continue
        acodec = fmt.get('acodec', NONE)
        vcodec = fmt.get('vcodec', NONE)

        if (vcodec != NONE) and (acodec == NONE):
            fmt = format_size(fmt)
            video_only_extensions.add(ext)
            video_only_formats.append(fmt)

    return video_only_extensions, video_only_formats

def get_download_type_extensions_and_formats(download_type: str, formats) -> Tuple[List, List]:
    ## video with audio
    if download_type == VIDEO_WITH_AUDIO:
        extensions, formats = get_video_with_audio_formats(formats)
        return extensions, formats

    ## only audio
    if download_type == AUDIO_ONLY:
        extensions, formats = get_audio_only_formats(formats)
        return extensions, formats

    ## only video
    if download_type == VIDEO_ONLY:
        extensions, formats = get_video_only_formats(formats)
        return extensions, formats

    else:
        raise Exception(f"Unknown download type: {download_type}")
    

def is_valid_youtube_url(url: str) -> bool:
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    matches = re.match(pattern, url)

    return bool(matches)

def sanitize_filename(filename: str) -> str:
    sanitized_filename = re.sub(r'[\/:*?,"<>|]', '_', filename)
    sanitized_filename = unicodedata.normalize('NFKD', sanitized_filename).encode('ASCII', 'ignore').decode('utf-8')
    return sanitized_filename