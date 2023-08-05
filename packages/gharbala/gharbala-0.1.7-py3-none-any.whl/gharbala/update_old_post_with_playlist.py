import re

from bs4 import BeautifulSoup
import requests
import os
from internetarchive import get_session
import urllib
from jinja2 import Template
import htmlmin
from google.cloud import translate_v2 as translate
from requests.exceptions import HTTPError
import sentry_sdk
from sentry_sdk.integrations.tornado import TornadoIntegration



def download_file(url, save_path):
    with open(save_path, 'wb') as file:
        file.write(requests.get(url, allow_redirects=True).content)
    return save_path


def google_translate(text, target_language):
    translate_client = translate.Client()
    return translate_client.translate(text, target_language)['translatedText']


def render_jinja_template(template_file, template_data):
    with open(template_file) as t:
        template = Template(htmlmin.minify(t.read(), reduce_empty_attributes=False,
                                           remove_optional_attribute_quotes=False,
                                           convert_charrefs=False,
                                           remove_empty_space=False))
        return template.render(template_data)


def upload_video_to_gharbala_server(video_data, video_filename, video_title, wordpress_domain='wp.gharbala.com',
                                    wordpress_auth_file=f'{os.environ["HOME"]}/.wordpress_user_password'):
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))

    try:
        uploaded_video_response = requests.post(
            f'https://{wordpress_domain}/wp-json/wp/v2/media',
            auth=wordpress_auth,
            json={"title": video_title, "status": "publish",
                  "alt_text": video_title, "description": {video_title}
                  },
            data=video_data,
            headers={
                'Content-Disposition': f'attachment; filename="{video_filename}"',
                'Content-Type': 'video/mp4'})
        # If the response was successful, no Exception will be raised
        print(f'Uploaded video status code: {uploaded_video_response.status_code}')
        if not uploaded_video_response.status_code in [200, 201]:
            raise HTTPError(uploaded_video_response.content)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Video upload Success!')

    video_id = uploaded_video_response.json()['id']

    try:
        uploaded_video_response = requests.post(
            f'https://{wordpress_domain}/wp-json/wp/v2/media/{video_id}',
            auth=wordpress_auth,
            json={"title": video_title, "alt_text": video_title,
                  "description": video_title, "caption": video_title})
        # If the response was successful, no Exception will be raised
        if not uploaded_video_response.status_code == requests.codes.ok:
            raise HTTPError(uploaded_video_response.content)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Add video meta info Success!')
    video_object = uploaded_video_response.json()
    return video_object

def wp_get_post(post_id, wordpress_domain='wp.gharbala.com',wordpress_auth_file=f'{os.environ["HOME"]}/.wordpress_user_password'):
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))
    
    try:
        post_response = requests.get(
            f'https://{wordpress_domain}/wp-json/wp/v2/posts/{post_id}',
            auth=wordpress_auth)
        # If the response was successful, no Exception will be raised
        if not post_response.status_code == requests.codes.ok:
            raise HTTPError(post_response.content)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print(f'Success got content of old post {post_id}!')
        return post_response.json()


def update_wordpress_post_from_html_jinja(template_file, post_id, template_data,
                                      wordpress_domain='wp.gharbala.com', post_status='publish',
                                      wordpress_auth_file=f'{os.environ["HOME"]}/.wordpress_user_password'):
    with open(wordpress_auth_file) as wp_auth_file:
        wordpress_auth = tuple(wp_auth_file.read().strip().split(':'))
    wp_post_content = render_jinja_template(template_file, template_data)
    wp_post_response = requests.post(f'https://{wordpress_domain}/wp-json/wp/v2/posts/{post_id}',
                                     json={"title": template_data["post_title"], "status": f"{post_status}",
                                           "content": wp_post_content,
                                           "featured_media": template_data["featured_image_id"],
                                           "excerpt": template_data["post_title"]
                                           },
                                     auth=wordpress_auth)
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


def reupload_videos(post_id, wp_domain='wp.gharbala.com', ia_config_file=f'{os.environ["HOME"]}/.ia'):
    sentry_sdk.init(
        dsn="https://bdbb72a0607f4e698676fe51a0dda449@o393890.ingest.sentry.io/5243434",
        integrations=[TornadoIntegration()]
    )
    id = post_id
    url = f'https://{wp_domain}/wp-json/wp/v2/posts/{id}'
    try:
        content = requests.get(url)
        # If the response was successful, no Exception will be raised
        if not content.status_code == requests.codes.ok:
            raise HTTPError(content.content)
        else:
            content = content.json()['content']['rendered']
            soup = BeautifulSoup(content, 'html.parser')
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print(f'Got content for post {post_id}!')

    ia_session = get_session(config_file=ia_config_file)
    old_videos = []
    videos = []

    for htwo in soup.find_all('h2'):
        try:
            print(f'getting href for {htwo}')
            old_link = htwo.a['href']
            print(f'got href {old_link}')

            print(f'getting old linke {old_link} id from archive.org')
            old_link_ia_id = urllib.parse.urlparse(old_link).path.split('/')[2]
            print(f'got id {old_link_ia_id}')

            print(f'getting old link metadata')
            ia_link_metadata = ia_session.get_metadata(old_link_ia_id)
            print('got old link metadata')

            print('Appending metadata to old_videos list')
            old_videos.append({"old_link": old_link, "new_link": "", "title": ia_link_metadata["metadata"]["title"]})
            print(f'Appended {old_videos}')
        except TypeError:
            print(f'Skipping {htwo} empty h2 tag with empty a href')
            continue


    for video in old_videos:
        try:
            print(f'Translating video title for {video["title"]}')
            wp_video_english_title = google_translate(video['title'], 'en')
            wp_video_arabic_title = google_translate(video['title'], 'ar')
            print(f'Done Translating video title for {video["title"]}')

            print(f'Sanitizing video filename')
            special_characters = ['?', '[', ']', '/', '\\', '=', '<', '>', ':', ';', ',', "'", '"', '&', '$', '#', '*',
                                  '(', ')', '|', '~', '`', '!', '{', '}', '%', '+', chr(0)]
            filename = wp_video_english_title
            for special_character in special_characters:
                filename = filename.replace(special_character, '')
            filename = filename.replace(' ', '-').replace('+', '-')
            filename = re.sub('[\r\n\t -]+', '-', filename)
            filename = filename.strip('.-_')
            filename = f'{filename}.mp4'
            print(f'Done sanitizing {filename}')

            print(f'Searching for video filename {filename} before uploading')
            video_search_result = wp_video_search(filename)
            if video_search_result is None:
                print(f'Video filename {filename} does not exist, uploading...')
                print(f'Downloading old archive.org video {video["old_link"]}')
                old_video_data = requests.get(video['old_link']).content
                print(f'Done Downloading old archive.org video {video["old_link"]}')
                print(f'Uploading video {filename} to wordpress')
                uploaded_video = upload_video_to_gharbala_server(old_video_data, filename,
                                                                 f'{wp_video_arabic_title} | {wp_video_english_title}')
                print(f'Done Uploading video {filename} to wordpress')

                print(f'Appending video {filename} to done videos list')
                videos.append(uploaded_video)
            else:
                print(f'video {filename} already exists, skip uploading')
                print(f'Appending video {filename} to done videos list')
                videos.append(video_search_result)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print(f'Success {filename}!')
            print(f'Videos list: {[video["id"] for video in videos]}')

    print(f'Getting old post {post_id} data to build template_data from it')
    old_wp_post = wp_get_post(post_id)
    old_wp_post_title = old_wp_post['title']['rendered']
    old_wp_post_featured_image_id = old_wp_post['featured_media']
    old_wp_post_featured_image_src = old_wp_post['jetpack_featured_media_url']
    template_data = {"post_title": old_wp_post_title,
                     "number_of_videos": len(videos),
                     "featured_image_id": old_wp_post_featured_image_id,
                     "featured_image_url": old_wp_post_featured_image_src,
                     "featured_image_caption": old_wp_post_title,
                     "list_of_video_ids": [video['id'] for video in videos],
                     "videos": videos}
    print(f'Done building {post_id} template_data')
    old_wp_post = wp_get_post(post_id)
    print(f'Create jinja template file for new post {post_id}')
    template_file = f'{os.environ["HOME"]}/gharbala-docker/post_template.jinja.html'
    print(f'Done creating jinja template file for new post {post_id}')
    print(f'Render new post jinja template {post_id}')
    wp_post_content = render_jinja_template(template_file, template_data)
    print(f'Done rendering new post jinja template {post_id}')

    print(f'Replacing old content for post {post_id}')
    new_post_response = update_wordpress_post_from_html_jinja(f'{os.environ["HOME"]}/gharbala-docker/post_template.jinja.html', post_id, template_data)
    if new_post_response.status_code == requests.codes.ok:
        print(f'Done replacing old content for post {post_id}')
    else:
        print(f'Failed replacing old content for post {post_id}')
    return videos, wp_post_content, new_post_response