import argparse
import csv
import json
import logging
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import urllib.parse
import site
from typing import List
from typing import Text
from PIL import Image
from jinja2 import Template
import htmlmin
from requests.exceptions import HTTPError
from loguru import logger

import requests
import sentry_sdk
from sentry_sdk.integrations.tornado import TornadoIntegration
from google.cloud import translate_v2 as translate


def check_dependencies():
    # Operating system - ubuntu only
    logger.info('Checking that operating system is Ubuntu')
    current_distro = platform.version().lower()
    if not ('ubuntu' in current_distro):
        logger.error('This script only works on Ubuntu linux')
        logger.error('If you want to run it on other distros, please take care of installing depedencies well')
        logger.error('Try on your own as it could probably work without problems once dependencies are met')
        sys.exit(1)
    logger.info('Done [OK]')

    # pwgen
    logger.info('Checking that pwgen is installed')
    if not shutil.which('pwgen'):
        logger.error('Please install pwgen, you can copy and paste following commands:\n')
        logger.error('sudo apt-get install -y pwgen')
        sys.exit(1)
    logger.info('Done [OK]')

    # Miniconda
    # logger.info('Checking that miniconda is installed')
    # if not shutil.which('conda'):
    #     logger.error('Please install miniconda, you can copy and paste following commands:\n')
    #     logger.error('curl -L https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O')
    #     logger.error('bash Miniconda3-latest-Linux-x86_64.sh')
    #     logger.error('source $HOME/.bashrc')
    #     sys.exit(1)
    # logger.info('Done [OK]')

    # Spleeter
    # logger.info('Checking that spleeter is installed')
    # if not shutil.which('spleeter'):
    #     logger.error('Please install spleeter, you can copy and paste following commands:\n')
    #     logger.error('conda config --add channels conda-forge')
    #     logger.error('conda install -r requirements.txt')
    #     logger.error('conda install -c numpy numba')
    #     sys.exit(1)
    # logger.info('Done [OK]')


def run_command(command: List):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output, error


def is_valid_youtube(url):
    logger.info(f'Checking that youtube url {url} is valid')
    if re.compile(r'^(http(s)?://)?((w){3}.)?youtu(be|.be)?(\.com)?/.+').match(url):
        logger.info('Done [OK]')
        return True
    else:
        logger.error(f'Invalid youtube url {url}')
        return False


def get_youtube_json_dump(url, youtube_json_dump_file='./youtube_info_object.json'):
    if is_valid_youtube(url):
        logger.info("Checking if youtube json dump file exists")
        if os.path.exists(youtube_json_dump_file):
            logger.info(f'Skipping getting {youtube_json_dump_file}, file already exists')
        else:
            logger.info('Getting youtube url json dump file')
            try:
                get_youtube_info_object_command = ['youtube-dl',
                                                   '--ignore-errors',
                                                   '--flat-playlist',
                                                   '--dump-single-json',
                                                   '--no-warnings',
                                                   url]
                youtube_info_object, error = run_command(get_youtube_info_object_command)
                if not youtube_info_object == b'' and error == b'':
                    with open(youtube_json_dump_file, 'w') as file:
                        file.write(youtube_info_object.decode('utf-8'))
                        logger.info("Finished getting youtube url json dump file [OK]")
                        logger.debug(youtube_info_object)
                else:
                    logger.exception(error)
                    raise ValueError(error)
            except subprocess.CalledProcessError as e:
                logger.exception(e)
                raise ValueError(e)
    else:
        raise ValueError(f'Invalid youtube URL {url}')


def create_ia_identifier(video_id, tmp_sha_file='./pwgen_video_sha_file'):
    try:
        logger.info(f'Creating unique identifier for video {video_id} for internet archive')
        subprocess.call(f'echo {video_id} > {tmp_sha_file}', shell=True)
        logger.info('Done [OK]')
        output, error = run_command(['pwgen', '20', '-n1', '-H', f'{tmp_sha_file}#{video_id}'])
        if not error == b'' or output == b'':
            logger.exception("Failed during metadata id generation")
            sys.exit(1)
        else:
            logger.info(f'Created ia id {output} for video {video_id}')
            return output.strip().decode('utf-8')
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def create_csv_row(file, row, mode):
    try:
        if mode == 'write':
            logger.info(f'Writing into file {file} csv row {row}')
            with open(file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(row)
                logger.info('Done, row added [OK]')
                logger.debug(row)
        else:
            with open(file, 'a', newline='') as csv_file:
                logger.info(f'Appending into file {file} csv row {row}')
                writer = csv.writer(csv_file)
                writer.writerow(row)
                logger.info('Done, row added [OK]')
                logger.debug(row)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def safe_to_skip_video(video_title):
    return any(substring in video_title for substring in ['Deleted video', 'Private video'])


def create_ia_metadata_file_from_youtube_playlist(youtube_info_object, ia_metadata_file):
    logger.info('It is a playlist url')
    logger.info(f'Creating metadata file for youtube videos list {youtube_info_object["title"]}')
    for video_object in youtube_info_object['entries']:
        video_id = video_object['id']
        video_title = video_object['title'].replace(',', '').replace('"', '').replace('/', '_')
        logger.info(f'Creating ia entry for video {video_id}: {video_title}')
        logger.info(f'Skip this entry {video_title} if it is for a deleted video')
        if safe_to_skip_video(video_title):
            logger.info(f'Skipped {video_id}: {video_title}')
            logger.info(f'Video {video_id}: {video_title} is either private or deleted, skipping...')
            continue
        ia_identifier = create_ia_identifier(video_id)
        create_csv_row(ia_metadata_file, [ia_identifier, f'{video_title}-{video_id}-nomusic.mpeg4',
                                          'Gharbala Website <gharbala.com>', 'movies',
                                          'opensource_movies', 'no music',
                                          video_title, video_title], 'append')
        logger.info(f'Done adding ia entry for {video_id}: {video_title} [OK]')
    logger.info(
        f'Done creating ia file for playlist'
        f'{youtube_info_object["id"]}: {youtube_info_object["title"]} [OK]')


def create_ia_metadata_file_from_youtube_video(youtube_info_object, ia_metadata_file):
    logger.info(f'Creating metadata file for youtube single video {youtube_info_object["title"]}')
    video_id = youtube_info_object['id']
    video_title = youtube_info_object['title'].replace(',', '').replace('"', '').replace('/', '_')
    logger.info(f'Creating ia entry for single video {video_id}: {video_title}')
    ia_identifier = create_ia_identifier(video_id)
    create_csv_row(ia_metadata_file, [ia_identifier, f'{video_title}-{video_id}-nomusic.mpeg4',
                                      'Gharbala Website <gharbala.com>', 'movies',
                                      'opensource_movies',
                                      'no music',
                                      video_title, video_title], 'append')
    logger.info(f'Done ia entry for {video_id}: {video_title} [OK]')


def get_youtube_info_object(youtube_json_dump_file):
    try:
        with open(youtube_json_dump_file) as file:
            logger.info(f'Load youtube json object from {youtube_json_dump_file}')
            youtube_info_object = json.loads(file.read())
            logger.info('Done loaded [OK]')
            logger.debug(youtube_info_object)
            return youtube_info_object
    except Exception as e:
        raise e


def create_ia_metadata_file(filename='./ia_metadata.csv', youtube_json_dump_file='./youtube_info_object.json'):
    ia_metadata_file = f'{filename}'
    logger.info('Creating ia metadata csv file header line')
    create_csv_row(ia_metadata_file, ['identifier', 'file', 'creator', 'mediatype',
                                      'collection', 'subject', 'title', 'description'], 'write')
    logger.info('Done [OK]')
    youtube_json_dump_file = f'{youtube_json_dump_file}'
    logger.info(f'Check that youtube dump file {youtube_json_dump_file} exists')
    if os.path.exists(youtube_json_dump_file):
        logger.info('Done youtube dump file {youtube_json_dump_file} exists [OK]')
        try:
            logger.info(f'Opening youtube dump file {youtube_json_dump_file} to load json string from it')
            youtube_info_object = get_youtube_info_object(youtube_json_dump_file)
            logger.info('Check that youtube json object is for a playlist url')
            if 'entries' in youtube_info_object:
                create_ia_metadata_file_from_youtube_playlist(youtube_info_object, ia_metadata_file)
            else:
                create_ia_metadata_file_from_youtube_video(youtube_info_object, ia_metadata_file)
        except Exception as e:
            logger.exception(f'Can not read proper json string from youtube url object file {e}')


def get_list_from_iametadata_file(ia_metadata_file):
    with open(ia_metadata_file, 'r') as iameta_file:
        logger.info(f'Reading all rows in {ia_metadata_file} into a list')
        reader = list(csv.reader(iameta_file))
        logger.info('Done, all read [OK]')
        logger.debug(reader)
        return reader


def is_english(text: Text):
    """Check if the characters in string s are in ASCII, U+0-U+7F."""
    return len(text) == len(text.encode())


def google_translate(text: Text, target_language: Text):
    translate_client = translate.Client()
    return translate_client.translate(text, target_language)['translatedText']


def create_wordpress_video_with_header_from_iameta_entry(wp_video_arabic_title: Text, wp_video_english_title,
                                                         ia_identifier, video_filename):
    return f'''
<!-- wp:heading {{"align":"right"}} -->
<h2 class="has-text-align-right">{wp_video_arabic_title} | {wp_video_english_title}  
<a href="https://archive.org/download/{ia_identifier}/{
    urllib.parse.quote(video_filename, safe='/:')}" download>(رابط التحميل)</a></h2>
<!-- /wp:heading -->
<!-- wp:video {{"preload":"auto","src":"https://archive.org/download/{
    ia_identifier}/{urllib.parse.quote(video_filename, safe='/:')}"}} -->
<figure class="wp-block-video"><video controls preload="auto" src="https://archive.org/download/{
    ia_identifier}/{urllib.parse.quote(video_filename, safe='/:')}"></video></figure>
<!-- /wp:video -->
'''


def get_youtube_playlist_or_video_title(youtube_json_dump_file):
    with open(youtube_json_dump_file) as file:
        return json.loads(file.read())['title']


def get_thumbnail_url_from_youtube_object(youtube_json_dump_file):
    youtube_json_object = get_youtube_info_object(youtube_json_dump_file)
    if 'thumbnail' in youtube_json_object and youtube_json_object['thumbnail'] is not None:
        thumbnail_url = youtube_json_object['thumbnail']
        logger.info('It is a single video')
        logger.debug(f'Thumbnail url is {thumbnail_url}')
    elif 'entries' in youtube_json_object:
        logger.info('It is a playlist, Getting the thumbnail from first video of the playlist')
        thumbnail_video_id = youtube_json_object['entries'][0]['id']
        logger.info(f'Thumbnail video id is {thumbnail_video_id}')
        logger.info('Getting thumbnail url via youtube-dl command')
        thumbnail_url, error = run_command(
            ['youtube-dl', '--get-thumbnail', '--force-ipv4', thumbnail_video_id])
        if thumbnail_url == b'':
            thumbnail_url = 'https://bit.ly/3eF1jzD'
        logger.info(f'Done, thumbnail url is {thumbnail_url}')
    else:
        logger.error(f'Failed getting thumbnail url from youtube, skip adding thumbnail url, using default url')
        thumbnail_url = 'https://bit.ly/3eF1jzD'

    try:
        thumbnail_url = thumbnail_url.strip().decode('utf-8')
    except AttributeError:
        thumbnail_url = thumbnail_url.strip()

    return thumbnail_url


def download_image(image_url, filename='/tmp/default.jpg'):
    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(r.content)
        f.close()

        logger.info(f'Image sucessfully Downloaded: {filename}')
    else:
        logger.error('Image Couldn\'t be retreived')


def convert_image_to_webp(image_path, webp_path):
    try:
        im = Image.open(image_path)
        im.convert('RGB')
        im.save(webp_path, 'WebP')
    except Exception as e:
        logger.exception(e)


def convert_image_to_jpg(image_path, jpg_path):
    try:
        im = Image.open(image_path)
        im.convert('RGB')
        im.save(jpg_path, 'JPEG')
    except Exception as e:
        logger.exception(e)


def upload_image_to_wordpress(thumbnail_url, ia_identifier, wp_post_final_title, wordpress_domain='wp.gharbala.com',
                              wordpress_auth_file=f'{os.environ["HOME"]}/.wordpress_user_password'):
    thumbnail_path = f'/tmp/{ia_identifier}.jpg'
    thumbnail_filename = f'{ia_identifier}.jpg'
    # thumbnail_filename = thumbnail_filename.replace('-', '').replace('|', '').replace(' ', '-')
    download_image(thumbnail_url, thumbnail_path)
    # webp not yet supported in wordpress
    convert_image_to_jpg(thumbnail_path, thumbnail_path)
    logger.info(f'Upload thumbnail {thumbnail_filename} for {wp_post_final_title} to wordpress')
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))
    with open(thumbnail_path, 'rb') as wp_image_thumbnail:
        image_thumbnail = wp_image_thumbnail.read()

    uploaded_thumbnail_response = requests.post(
        f'https://{wordpress_domain}/wp-json/wp/v2/media',
        auth=wordpress_auth,
        json={"title": wp_post_final_title, "status": "publish",
              "alt_text": wp_post_final_title
              },
        data=image_thumbnail,
        headers={
            'Content-Disposition': f'attachment; filename="{thumbnail_filename}"'})
    logger.info(f'Uploaded thumbnail url {thumbnail_url} to wordpress')
    logger.debug(uploaded_thumbnail_response.json())
    logger.info('Setting new uploaded thumbnail id')

    wp_post_thumbnail_id = uploaded_thumbnail_response.json()['id']
    logger.info(f'New uploaded thumbnail id is {wp_post_thumbnail_id}')
    logger.info(f'Setting title and alt text of newly uploaded image {wp_post_thumbnail_id}')
    uploaded_thumbnail_response = requests.post(
        f'https://{wordpress_domain}/wp-json/wp/v2/media/{wp_post_thumbnail_id}',
        auth=wordpress_auth,
        json={"title": wp_post_final_title, "alt_text": wp_post_final_title,
              "description": wp_post_final_title})
    logger.info(f'Done setting title and alt text of newly uploaded image {wp_post_thumbnail_id}')

    return uploaded_thumbnail_response, wp_post_thumbnail_id


def get_wp_post_footer_content():
    return f'''
    <!-- wp:separator -->
    <hr class="wp-block-separator"/>
    <!-- /wp:separator -->
    <!-- wp:list -->
    <ul>
    <li><a href="https://gharbala.com/%d8%a7%d9%84%d8%a7%d8%b3%d8%a6%d9%84%d8%a9-%d8%a7%d9%84%d8%b4%d8%a7%d8%a6%d8%b9%d8%a9-faq/#lwptoc1">1.1&nbsp;كيف اقوم بتحميل فيديو من علي الموبيل؟</a></li>
    <li><a href="https://gharbala.com/%d8%a7%d9%84%d8%a7%d8%b3%d8%a6%d9%84%d8%a9-%d8%a7%d9%84%d8%b4%d8%a7%d8%a6%d8%b9%d8%a9-faq/#lwptoc2">1.2&nbsp;كيف اقوم بتحميل الفيديو من علي جهاز الكمبيوتر؟</a></li>
    <li><a href="https://gharbala.com/%d8%a7%d9%84%d8%a7%d8%b3%d8%a6%d9%84%d8%a9-%d8%a7%d9%84%d8%b4%d8%a7%d8%a6%d8%b9%d8%a9-faq/#lwptoc3">1.3&nbsp;اشتركت في القائمة البريدية ولم يصلني شيء؟!</a></li>
    <li><a href="https://gharbala.com/%d8%a7%d9%84%d8%a7%d8%b3%d8%a6%d9%84%d8%a9-%d8%a7%d9%84%d8%b4%d8%a7%d8%a6%d8%b9%d8%a9-faq/#lwptoc4">1.4&nbsp;هل يمكن تحميل جميع الفيديوهات في المقال مرة واحدة؟</a></li>
    </ul>
    <!-- /wp:list -->'''


def add_wp_post_heading_and_footer(wordpress_post_file, post_title, uploaded_thumbnail_response, wp_post_thumbnail_id,
                                   wp_post_final_title, wp_post_file_content, wp_post_file_content_footer):
    logger.info(f'Add heading at start of the content for {post_title} to be targeted by keywords for seo')
    with open(wordpress_post_file, 'w') as wp_post_file:
        try:
            logger.info('Getting sized source url of thumbnail image')
            large_pic_url = urllib.parse.urlparse(uploaded_thumbnail_response.json(
            )["media_details"]["sizes"]["jannah-image-large"]["source_url"])
        except KeyError:
            logger.info('Failed getting sized image, using default orginal thumbnail image size')
            large_pic_url = urllib.parse.urlparse(uploaded_thumbnail_response.json(
            )["source_url"])
        wp_post_file.write(
            f'<!-- wp:heading {{"align":"right"}} --><h2 class="has-text-align-right">{wp_post_final_title}</h2><!-- /wp:heading -->'
            f'<!-- wp:image {{"id":{wp_post_thumbnail_id},"align":"center","sizeSlug":"large"}} -->'
            f'''<figure class="wp-block-image size-large aligncenter"><img src="{large_pic_url[0] + "://" + large_pic_url[1] + large_pic_url[2]}" alt="{uploaded_thumbnail_response.json()['alt_text']}" class="wp-image-{wp_post_thumbnail_id}"/><figcaption>{uploaded_thumbnail_response.json()['alt_text']}</figcaption></figure>'''
            f'<!-- /wp:image -->'
            '<!-- wp:separator --><hr class="wp-block-separator"/><!-- /wp:separator -->'
            + wp_post_file_content + wp_post_file_content_footer)


def render_jinja_template(template_file, template_data):
    with open(template_file) as t:
        template = Template(htmlmin.minify(t.read(), reduce_empty_attributes=False,
                                           remove_optional_attribute_quotes=False,
                                           convert_charrefs=False,
                                           remove_empty_space=False))
        return template.render(template_data)


def post_to_wordpress_from_html_file(wordpress_post_file, wp_post_final_title, wp_post_thumbnail_id,
                                     wordpress_domain='wp.gharbala.com', post_status='pending',
                                     wordpress_auth_file=f'{str(pathlib.Path.home())}/.wordpress_user_password'):
    with open(wordpress_post_file) as wp_post_file:
        wp_post_file_content = wp_post_file.read()
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))
    logger.info(f'Content prepared for {wp_post_final_title}')
    logger.info(f'Create wordpress draft post for {wp_post_final_title}')
    wp_post_response = requests.post(f'https://{wordpress_domain}/wp-json/wp/v2/posts',
                                     json={"title": wp_post_final_title, "status": f"{post_status}",
                                           "content": wp_post_file_content,
                                           "featured_media": wp_post_thumbnail_id,
                                           "excerpt": wp_post_final_title
                                           },
                                     auth=wordpress_auth)
    logger.info(f'Created wordpress post for {wp_post_final_title}')
    logger.debug(wp_post_response.json())


def post_to_wordpress_from_html_jinja(template_file, template_data,
                                      wordpress_domain='wp.gharbala.com', post_status='pending',
                                      wordpress_auth_file=f'{str(pathlib.Path.home())}/.wordpress_user_password'):
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))
    logger.info(f'Content prepared for {template_data["post_title"]}')
    logger.info(f'Create wordpress draft post for {template_data["post_title"]}')
    wp_post_content = render_jinja_template(template_file, template_data)
    wp_post_response = requests.post(f'https://{wordpress_domain}/wp-json/wp/v2/posts',
                                     json={"title": template_data["post_title"], "status": f"{post_status}",
                                           "content": wp_post_content,
                                           "featured_media": template_data["featured_image_id"],
                                           "excerpt": template_data["post_title"]
                                           },
                                     auth=wordpress_auth)
    logger.info(f'Created wordpress post for {template_data["post_title"]}')
    logger.debug(wp_post_response.json())
    return wp_post_response


def wp_video_search(filename, wp_domain='wp.gharbala.com'):
    search_result = requests.get(
        f'https://{wp_domain}/wp-json/wp/v2/media?media_type=video&per_page=2&search={filename}')
    if search_result.status_code == requests.codes.ok:
        search_result = search_result.json()
    else:
        raise HTTPError(search_result.content)
    if len(search_result) == 0:
        return None
    else:
        return search_result[0]


def upload_video_to_gharbala_server(video_path, video_filename, video_title, wordpress_domain='wp.gharbala.com',
                                    wordpress_auth_file=f'{os.environ["HOME"]}/.wordpress_user_password'):
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))

    try:
        logger.info(f'Sanitizing video filename')
        special_characters = ['?', '[', ']', '/', '\\', '=', '<', '>', ':', ';', ',', "'", '"', '&', '$', '#', '*',
                              '(', ')', '|', '~', '`', '!', '{', '}', '%', '+', chr(0)]
        filename = video_filename
        for special_character in special_characters:
            filename = filename.replace(special_character, '')
        filename = filename.replace(' ', '-').replace('+', '-')
        filename = re.sub('[\r\n\t -]+', '-', filename)
        filename = filename.strip('.-_')
        filename = f'{filename}'
        print(f'Done sanitizing {filename}')

        print(f'Searching for video filename {filename} before uploading')
        video_search_result = wp_video_search(filename)
        if video_search_result is None:
            logger.info(f'Uploading video {video_title} to wordpress')
            with open(video_path, 'rb') as video_file:
                uploaded_video_response = requests.post(
                    f'https://{wordpress_domain}/wp-json/wp/v2/media',
                    auth=wordpress_auth,
                    json={"title": video_title, "status": "publish",
                          "alt_text": video_title, "description": {video_title}
                          },
                    data=video_file.read(),
                    headers={
                        'Content-Disposition': f'attachment; filename="{video_filename}"'})
            logger.debug(f'Video upload response {uploaded_video_response}')
            video_id = uploaded_video_response.json()['id']
            uploaded_video_response = requests.post(
                f'https://{wordpress_domain}/wp-json/wp/v2/media/{video_id}',
                auth=wordpress_auth,
                json={"title": video_title, "alt_text": video_title,
                      "description": video_title, "caption": video_title})
            logger.debug(f'Video metadata update response after uploading {uploaded_video_response}')
            video_object = uploaded_video_response.json()
            return video_object
        else:
            video_object = video_search_result
            logger.info(f'video {filename} already exists, skip uploading')
            logger.info(f'Using existing video object {video_object}')
            uploaded_video_response = requests.post(
                f'https://{wordpress_domain}/wp-json/wp/v2/media/{video_object["id"]}',
                auth=wordpress_auth,
                json={"title": video_title, "alt_text": video_title,
                      "description": video_title, "caption": video_title})
            logger.debug(f'Video metadata update response after uploading {uploaded_video_response}')
            video_object = uploaded_video_response.json()
            return video_object
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6


def post_to_wordpress_from_iametadata(youtube_json_dump_file='./youtube_info_object.json',
                                      wordpress_post_file='./wordpress_post.html',
                                      ia_metadata_file='./ia_metadata.csv'):
    wp_video_title = ''
    videos = []
    try:
        logger.info(f'Opening wordpress post file {wordpress_post_file} for writing')
        with open(wordpress_post_file, 'w') as wp_post_file:
            logger.info(f'Opening ia metadata file {ia_metadata_file} to read for generating wordpress posts file')
            reader = get_list_from_iametadata_file(ia_metadata_file)
            logger.info(f'Start looping over all entries of {ia_metadata_file}')
            for row in reader[1:]:
                ia_identifier = row[0]
                video_filename = row[1]
                wp_video_title = row[6]
                logger.info(f'Checking if the video title {wp_video_title} is english ascii')
                if is_english(wp_video_title):
                    logger.info(f'Video {wp_video_title} is English, translating to Arabic using google translate')
                    wp_video_english_title = wp_video_title
                    wp_video_arabic_title = google_translate(wp_video_english_title, 'ar')
                    logger.info(f'Translated {wp_video_english_title} to Arabic {wp_video_arabic_title}')
                    logger.info(f'Preparing wordpress post content for {wp_video_title}')
                    content_block = create_wordpress_video_with_header_from_iameta_entry(wp_video_arabic_title,
                                                                                         wp_video_english_title,
                                                                                         ia_identifier, video_filename)
                    wp_post_file.write(content_block)
                    logger.info(f'Added wordpress post entry for video {wp_video_title}')
                    logger.debug(content_block)
                    logger.info(f'Upload video {wp_video_title} to gharbala server')
                    uploaded_video = upload_video_to_gharbala_server(f'./{video_filename}',
                                                                     f'{wp_video_english_title}.mp4',
                                                                     f'{wp_video_arabic_title} | {wp_video_english_title}')
                    videos.append(uploaded_video)
                else:
                    logger.info(
                        f'Video {wp_video_title} is not English, translating to english using google translate')
                    wp_video_non_english_title = wp_video_title
                    wp_video_english_title = google_translate(wp_video_non_english_title, 'en')
                    logger.info(
                        f'Translated {wp_video_non_english_title} to English '
                        f'{wp_video_english_title} to preserve all languages')
                    content_block = create_wordpress_video_with_header_from_iameta_entry(wp_video_non_english_title,
                                                                                         wp_video_english_title,
                                                                                         ia_identifier, video_filename)
                    wp_post_file.write(content_block)
                    logger.info(f'Added wordpress post entry for video {video_filename}')
                    logger.debug(content_block)
                    logger.info(f'Upload video {wp_video_title} to gharbala server')
                    uploaded_video = upload_video_to_gharbala_server(f'./{video_filename}',
                                                                     f'{wp_video_english_title}.mp4',
                                                                     f'{wp_video_non_english_title} | {wp_video_english_title}')
                    videos.append(uploaded_video)
        wp_post_file.close()

        with open(wordpress_post_file) as wp_post_file:
            post_title = get_youtube_playlist_or_video_title(youtube_json_dump_file)
            logger.info(f'Original post title is {post_title}')
            if is_english(post_title):
                logger.info(f'Video {post_title} is English, translating the title using google translate')
                wp_post_english_title = post_title
                wp_post_arabic_title = google_translate(wp_post_english_title, 'ar') + ' بدون موسيقى'
                logger.info(f'Created Arabic title part {wp_post_arabic_title}')
                wp_post_english_title = wp_post_english_title + ' No Music'
                wp_post_final_title = f'{wp_post_arabic_title} | {wp_post_english_title}'
                logger.info(f'Created English title part {wp_post_english_title}')
                logger.info(f'Final post title is {wp_post_final_title}')
            else:
                logger.info(
                    f'Video {wp_video_title} is not English, translating the title using google translate')
                wp_post_non_english_title = post_title
                wp_post_english_title = google_translate(wp_post_non_english_title, 'en') + ' No Music'
                logger.info(f'Created English title part {wp_post_english_title}')
                wp_post_arabic_title = wp_post_non_english_title + ' بدون موسيقى'
                logger.info(f'Created Arabic title part {wp_post_arabic_title}')
                wp_post_final_title = wp_post_arabic_title + ' | ' + wp_post_english_title
                logger.info(f'Final post title is {wp_post_final_title}')
            wp_post_file_content = wp_post_file.read()
        wp_post_file.close()
        logger.info(f'Created content for post {post_title}')
        logger.debug(wp_post_file_content)

        logger.info(f'Getting thumbnail url for {wp_post_final_title}')
        thumbnail_url = get_thumbnail_url_from_youtube_object(youtube_json_dump_file)
        logger.info(f'Got thumbnail url for {wp_post_final_title}')

        uploaded_thumbnail_response, wp_post_thumbnail_id = upload_image_to_wordpress(thumbnail_url, ia_identifier,
                                                                                      wp_post_final_title)

        wp_post_file_content_footer = get_wp_post_footer_content()

        logger.info(f'Add heading at start of the content for {post_title} to be targeted by keywords for seo')
        add_wp_post_heading_and_footer(wordpress_post_file, post_title, uploaded_thumbnail_response,
                                       wp_post_thumbnail_id,
                                       wp_post_final_title, wp_post_file_content, wp_post_file_content_footer)
        logger.info('Done content added [OK]')
        logger.debug(
            f'<h2>{wp_post_final_title}</h2>' + '<hr class="wp-block-separator"/>' + wp_post_file_content)

        logger.info(f'Prepeare content for wordpress post {wp_post_final_title}')
        # post_to_wordpress_from_html_file(wordpress_post_file, wp_post_final_title, wp_post_thumbnail_id)
        number_of_videos = len(reader) - 1
        template_data = {"post_title": wp_post_final_title,
                         "number_of_videos": number_of_videos,
                         "featured_image_id": wp_post_thumbnail_id,
                         "featured_image_url": uploaded_thumbnail_response.json()["source_url"],
                         "featured_image_caption": wp_post_final_title,
                         "list_of_video_ids": [video['id'] for video in videos if video is not None],
                         "videos": [video for video in videos if video is not None]}
        post_to_wordpress_from_html_jinja(f'{site.getusersitepackages()}/gharbala/post_template.jinja.html',
                                          template_data)
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


def download_from_youtube(video_id):
    output, error = run_command(['youtube-dl', '--force-ipv4', '-f',
                                 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
                                 '--merge-output-format', 'mp4', '--id', '--continue',
                                 # '--write-sub', '--write-auto-sub', '--embed-subs', '--sub-lang=ar',
                                 f'https://youtube.com/watch?v={video_id}'])
    return output, error


def delete_video_entry_from_iametadata_file(video_id, ia_metadata_file):
    subprocess.call(['sed', '-i', f'/.*{video_id}.*/d', ia_metadata_file])


def split_music_and_vocals_from_video(video_id):
    output, error = run_command(
        ['spleeter', 'separate', '-o', os.getcwd(),
         '-d', '20000', '-p', 'spleeter:2stems', '--verbose', f'./{video_id}.mp4'])
    return output, error


def remove_music_from_video(video_id):
    output, error = run_command(
        ['ffmpeg', '-i', f'./{video_id}.mp4', '-i', f'./{video_id}/vocals.wav',
         '-acodec', 'aac', '-vcodec', 'copy', '-map', '0:0', '-map', '1:0',
         f'./{video_id}-nomusic.mp4'])
    return output, error


def remove_music_from_youtube_videos(youtube_json_dump_file='./youtube_info_object.json',
                                     ia_metadata_file='./ia_metadata.csv'):
    logger.info(f'Check if youtube json dump file {youtube_json_dump_file} exists')
    if os.path.exists(youtube_json_dump_file):
        logger.info(f'{youtube_json_dump_file} exists [OK]')
        youtube_info_object = get_youtube_info_object(youtube_json_dump_file)
        logger.info(f'Check if {youtube_json_dump_file} is a playlist or a video')
        if 'entries' in youtube_info_object:
            logger.info(f'{youtube_json_dump_file} is a playlist')
            logger.info(f'Start downloading all videos in the playlist')
            for video_object in youtube_info_object['entries']:
                video_id = video_object['id']
                video_title = video_object['title'].replace(',', '').replace('"', '').replace('/', '_')
                logger.info(f'Check if {video_title}-{video_id} has been downloaded or not')
                if not os.path.exists(f'./{video_title}-{video_id}-nomusic.mpeg4'):
                    logger.info(f'./{video_title}-{video_id}-nomusic.mpeg4 does not exit')
                    try:
                        logger.info(f'Downloading video {video_id} from youtube')
                        output, error = download_from_youtube(video_id)
                        logger.info(f'Video {video_id} downloaded')
                        logger.debug(output)
                        if error:
                            logger.debug(error)
                            raise Exception(error)
                    except Exception as e:
                        # Skip to next video if there is an issues to get all working videos from a list
                        logger.error(f'{e}')
                        logger.info(f'Removing this video {video_id} entry from ia_metadata file')
                        delete_video_entry_from_iametadata_file(video_id, ia_metadata_file)
                        logger.info(f'Removed video {video_id} entry from ia_metadata file')
                        logger.exception(f'error downloading video from youtube {e}')
                        continue
                    logger.info(f'Removing music from {video_id} using spleeter')
                    try:
                        output, error = split_music_and_vocals_from_video(video_id)
                        logger.info(f'Removed music from {video_id} using spleeter')
                        logger.debug(output)
                    except Exception as e:
                        logger.error(f'Failed removing music from {video_id} using spleeter {error}')
                        logger.info(f'Removing this video {video_id} entry from ia_metadata file')
                        delete_video_entry_from_iametadata_file(video_id, ia_metadata_file)
                        logger.info(f'Removed video {video_id} entry from ia_metadata file')
                        logger.exception(e)
                        continue

                    logger.info(f'Replace voice from original video {video_id} with no music vocals using ffmpeg')
                    try:
                        output, error = remove_music_from_video(video_id)
                        logger.info(f'Music replaced in video {video_id}')
                        logger.debug(output)
                    except Exception as e:
                        logger.error(f'Replacing music in original video {video_id} failed {error}')
                        logger.info(f'Removing this video {video_id} entry from ia_metadata file')
                        delete_video_entry_from_iametadata_file(video_id, ia_metadata_file)
                        logger.info(f'Removed video {video_id} entry from ia_metadata file')
                        logger.exception(e)
                        continue

                    try:
                        logger.info(f'Renaming produced no music video {video_id}-nomusic.mp4 file')
                        shutil.move(f'./{video_id}-nomusic.mp4', f'./{video_title}-{video_id}-nomusic.mpeg4')
                        logger.info(f'Renamed to ./{video_title}-{video_id}-nomusic.mpeg4')
                    except Exception as e:
                        logger.error('Failed at renaming file {video_id}-nomusic.mp4')
                        logger.info(f'Removing this video {video_id} entry from ia_metadata file')
                        delete_video_entry_from_iametadata_file(video_id, ia_metadata_file)
                        logger.info(f'Removed video {video_id} entry from ia_metadata file')
                        logger.exception(e)
                        continue
                else:
                    logger.info(f'Skip processing video {video_title}-{video_id}, already existing')
        else:
            video_id = youtube_info_object['id']
            logger.info(f'Working on a single video {video_id} not a playlist')
            logger.info(f'Sanitizing video {video_id} title')
            video_title = youtube_info_object['title'].replace(',', '').replace('"', '').replace('/', '_')
            logger.info(f'Santized video title to {video_title}')
            logger.info(f'Chech that video ./{video_title}-{video_id}-nomusic.mpeg4 was not processed before')
            if not os.path.exists(f'./{video_title}-{video_id}-nomusic.mpeg4'):
                logger.info(f'Video has not been processed before')
                try:
                    logger.info(f'Downloading video {video_id} from youtube')
                    output, error = download_from_youtube(video_id)
                    logger.info(f'Video {video_id} downloaded')
                    logger.debug(output)
                    if error:
                        logger.debug(error)
                        raise Exception(error)
                except Exception as e:
                    # Skip to next video if there is an issues to get all working videos from a list
                    logger.exception(f'error downloading video from youtube {e}')

                logger.info(f'Removing music from {video_id} using spleeter')
                try:
                    output, error = split_music_and_vocals_from_video(video_id)
                    logger.info(f'Removed music from {video_id} using spleeter')
                    logger.debug(output)
                except Exception as e:
                    logger.error(f'Failed removing music from {video_id} using spleeter {e}')
                    logger.exception(e)

                logger.info(f'Replace voice from original video {video_id} with no music vocals using ffmpeg')
                try:
                    output, error = remove_music_from_video(video_id)
                    logger.info(f'Music replaced in video {video_id}')
                    logger.debug(output)
                except Exception as e:
                    logger.error(f'Replacing music in original video {video_id} failed {e}')
                    logger.exception(e)

                try:
                    logger.info(f'Renaming produced no music video {video_id}-nomusic.mp4 file')
                    shutil.move(f'./{video_id}-nomusic.mp4', f'./{video_title}-{video_id}-nomusic.mpeg4')
                    logger.info(f'Renamed to ./{video_title}-{video_id}-nomusic.mpeg4')
                except Exception as e:
                    logger.error('Failed at renaming file {video_id}-nomusic.mp4')
                    logger.exception(e)


def upload_to_internet_archive(ia_metadata_file='./ia_metadata.csv'):
    # wait until all internet archive tasks are finished before uploading any new videos
    logger.info(f'Check to see if we should wait for other upload tasks before uploading or not')
    try:
        logger.info(f'Uploading to internet archive')
        output, _ = run_command(['ia', 'upload', '--retries', '15', f'--spreadsheet={ia_metadata_file}'])
        logger.info(f'Finished uploading vides to internet archive')
        logger.debug(output)
    except Exception as e:
        logger.exception(f'Failed uploading to internet archive {e}')
        sys.exit(1)


def get_trello_checklist_info(checklist_id):
    logger.info(f'Getting trello credentials key and token which needs to be provided as environment variables')
    api_key = os.environ['trello_api_key']
    api_token = os.environ['trello_api_token']
    api_url = 'https://api.trello.com/1'
    logger.info(f'Done [OK]')

    logger.info(f'Getting current checklist {checklist_id} items from Trello')
    checklist_items = requests.get(f'{api_url}/checklists/{checklist_id}?key={api_key}&token={api_token}').json()[
        'checkItems']
    logger.info(f'Got checklist {checklist_id} items')
    logger.debug(checklist_items)

    logger.info(f'Getting checklist {checklist_id} card id')
    checklist_card_id = requests.get(f'{api_url}/checklists/{checklist_id}?key={api_key}&token={api_token}').json()[
        'idCard']
    logger.info(f'Got checklist card id {checklist_card_id}')

    return checklist_items, checklist_card_id


def mark_trello_checklist_item_completed(checklist_card_id, item):
    api_key = os.environ['trello_api_key']
    api_token = os.environ['trello_api_token']
    api_url = 'https://api.trello.com/1'
    logger.info(f'Check finished trello item {item["name"]} completed')
    uri = f'cards/{checklist_card_id}/checkItem/{item["id"]}?key={api_key}&token={api_token}&state=complete'
    mark_trello_item_completed_response = requests.put(f'{api_url}/{uri}').json()
    logger.debug(mark_trello_item_completed_response)


def remove_music_from_trello_checklist(checklist_id):
    try:
        checklist_items, checklist_card_id = get_trello_checklist_info(checklist_id)
        logger.info('Start looping over all checklist items to process videos and playlists one by one')
        for item in checklist_items:
            logger.info(f'check if item {item} is not already processed before')
            if item['state'] == 'incomplete':
                logger.info(f'item {item} has not been processed before')
                logger.info(f'Making sure the item {item} contains a valid youtube url')
                youtube_url = item['name']
                if is_valid_youtube(youtube_url):
                    logger.info(f'Item {item} is a valid youtube url {youtube_url}')
                    logger.info(f'Create a directory for item {item} to store processed videos in it')
                    work_dir = youtube_url.replace(':', '_').replace('/', '_').replace('?', '_').replace('=', '_')
                    if not os.path.exists(work_dir):
                        os.mkdir(work_dir)
                    logger.info(f'Created a directory {work_dir} for item {item["name"]}')

                    logger.info(f'Change work dir to {work_dir}')
                    os.chdir(work_dir)
                    logger.info(f'Changed, current dir now is {work_dir}')
                    try:
                        logger.info(f'Getting youtube json dump object for item {item["name"]}')
                        get_youtube_json_dump(item['name'])
                        logger.info(f'Done [OK]')
                    except Exception as e:
                        logger.error(f'Could not get youtube json dump file for {item["name"]}')
                        if any(substring in str(e) for substring in
                               ['The uploader has not made this video available in your country', 'blocked it']):
                            logger.error(
                                f'Getting {youtube_url} url json info object failed due to country blocking by youtube')
                            logger.info(f'skipping item {item["name"]}')
                            mark_trello_checklist_item_completed(checklist_card_id, item)
                            continue
                        else:
                            logger.exception(f'Failed getting json dump file for item {item["name"]}')
                            logger.error(f'Continueing with next trello item in checklist')
                            continue

                    logger.info(f'Creating internet archive metadata file')
                    create_ia_metadata_file()
                    logger.info(f'Done [OK]')

                    if not args.skip_music_removal:
                        remove_music_from_youtube_videos()

                    # upload to internet archive
                    if args.upload_to_internet_archive:
                        upload_to_internet_archive()

                    # post to wordpress
                    if args.post_to_wordpress:
                        post_to_wordpress_from_iametadata()

                    # get back to parent directory
                    logger.info('Changing back to parent dir')
                    os.chdir('..')
                    logger.info(f'Changed back to dir {os.getcwd()}')

                    # eventually mark finished item checked
                    mark_trello_checklist_item_completed(checklist_card_id, item)

                    # report that item is finished
                    logger.info(f'Trello checklist item {item["name"]} done [OK]')
                else:
                    logger.error(f'Invalid trello checklist item with id {item["id"]}, skipping...')
                    continue
        logger.info('All incomplete trello checklist items has been processed!')
    except Exception as e:
        logger.exception(e)


def prepare_cli():
    global logger, cli_parser, args
    # configure logging
    logging_format = '%(asctime)s module(%(filename)s) function(%(funcName)s) line(%(lineno)d) %(levelname)s: %(message)s'
    date_format = '%d-%m-%y %H:%M:%S'
    # Create a custom logger
    logger = logging.getLogger(__name__)
    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('main.log')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)
    # Create formatters and add it to handlers
    c_format = logging.Formatter(logging_format, datefmt=date_format)
    f_format = logging.Formatter(logging_format, datefmt=date_format)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    # As the docs explain, the logger's default level is NOTSET
    # which means it checks with its parent, which is the root, which has a default of WARNING.
    logger.setLevel(logging.DEBUG)
    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    # define and parse command line args
    cli_parser = argparse.ArgumentParser(description='Remove music from youtube video or list')
    # either trello checklist or youtube url is required
    cli_group = cli_parser.add_mutually_exclusive_group(required=True)
    cli_group.add_argument('-y', '--youtube-url', action='store', type=str,
                           help='URL for a youtube video or list')
    cli_group.add_argument('-t', '--trello-checklist-id', action='store', type=str,
                           help='Trello checklist id to be traversed fetching links from it')
    # rest are optional
    cli_parser.add_argument('-u', '--upload-to-internet-archive', action='store_true',
                            help='Upload videos to logged in account on internet archive')
    cli_parser.add_argument('-p', '--post-to-wordpress', action='store_true',
                            help='Creates a wordpress draft post with all processed videos semi automating publishing')
    cli_parser.add_argument('-s', '--skip-music-removal', action='store_true',
                            help='Skips music removal step if you there is no need for videos downloading & processing')
    cli_parser.add_argument('-w', '--wait-for-tasks', action='store_true',
                            help='Awaits other running/queued tasks on internet archive before uploading new videos')
    args = cli_parser.parse_args()


def main():
    prepare_cli()
    # activate sentry logging
    logger.info('Set sentry logging')
    sentry_sdk.init(
        dsn="https://bdbb72a0607f4e698676fe51a0dda449@o393890.ingest.sentry.io/5243434",
        integrations=[TornadoIntegration()]
    )
    logger.info('Done setting sentry [OK]')

    # print help if no arguments passed
    if len(sys.argv) == 1:
        cli_parser.print_help()

    # exit if there is a unmet dependency before doing anything else
    logger.info('Checking for missing dependencies')
    check_dependencies()
    logger.info('Done [OK]')

    # if Youtube url give we prepare json dump and internet archive metadata files
    if args.youtube_url:
        logger.info(f'We got youtube url {args.youtube_url} to work on')
        try:
            youtube_url = args.youtube_url
            work_dir = youtube_url.replace(':', '_').replace('/', '_').replace('?', '_').replace('=', '_')
            if not os.path.exists(work_dir):
                os.mkdir(work_dir)
            logger.info(f'Created a directory {work_dir} for youtube {youtube_url}')

            logger.info(f'Change work dir to {work_dir}')
            os.chdir(work_dir)

            get_youtube_json_dump(args.youtube_url)
            create_ia_metadata_file()
            if not args.skip_music_removal:
                remove_music_from_youtube_videos()
            if args.upload_to_internet_archive:
                upload_to_internet_archive()
            if args.post_to_wordpress:
                post_to_wordpress_from_iametadata()
            logger.info(f'Done processing youtube url {args.youtube_url}')
            logger.info('----------------------------------------------')
            os.chdir('..')
        except Exception as e:
            if 'blocked it' in str(e):
                logger.exception(
                    f'Getting {args.youtube_url} url json info object failed due to country blocking by youtube')
                raise
            else:
                logger.exception('Failed getting json dump file, check main.log file for more info')
                raise

    # if we are going to work from trello checklist we just pass the id to trello function and it should handle the rest
    # if no trello checklist option we continue as normal and/or upload to archive, post to wordpress
    if args.trello_checklist_id:
        logger.info(f'Got a trello checklist {args.trello_checklist_id} to work on')
        remove_music_from_trello_checklist(args.trello_checklist_id)
        logger.info(f'Done processing trello checklist {args.trello_checklist_id}')
        logger.info('----------------------------------------------')
