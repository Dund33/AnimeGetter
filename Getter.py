import requests


def generate_url(episode):
    return 'link{}'\
    .format(episode)


def get_video_url(episode):
    url = generate_url(episode)
    resp = requests.get(url)

    if resp.status_code != 200:
        print('Bad request')
        return None

    html = str(resp.content)
    found = html.find('file:"')
    parsed = html[found + 6:]
    end = parsed.find('"')
    link = parsed[:end]
    return link


def get_video(url):
    resp = requests.head(url)
    length_str = resp.headers['content-length']
    length = int(length_str)
    length /= 1048576
    print('downloading {} MB'.format(length))

    resp = requests.get(url)
    video = resp.content

    return video


def get_title(url):
    beg = url.find('[')
    end = url.find('.mp4')
    return url[beg:end]+'.mp4'


for episode in range(1, 27):
    url = get_video_url(episode)

    if url is None:
        print('sorry can\'t do')
        continue

    video = get_video(url)

    if video is None:
        print('sorry can\'t do')
        continue

    name = get_title(url)

    if name is None:
        print('sorry can\'t do')
        continue

    file = open(name, 'wb')
    file.write(video)
    file.close()
