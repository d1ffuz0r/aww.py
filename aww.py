from random import randint
from PIL import Image
import json
import urllib2
import StringIO
import sys

# TODO: Error handling.
# Works if Reddit's permalink is an absolute image;
# will require some finagling down the line to make it work
# with the inevitable edge cases.


# This is where the magic happens.
def grab_cute_image(username=None, trials=3):

    # three trials to grab an acceptable image;
    # if no dice, return None
    if not trials:
        return None

    # Grab the JSON of the r/aww subreddit, which displays
    # adorable images -- and convert it to a dict.
    cuteness_url = "http://www.reddit.com/r/aww.json"
    opener = urllib2.build_opener()

    # if the user supplies a username, we add it to the UA.
    if username:
        opener.addheaders = [('User-agent',
                              'aww.py, invoked by /u/' + username)]
    else:
        opener.addheaders = [('User-agent', 'aww.py, a CLI for r/aww!')]

    response = opener.open(cuteness_url)
    j = json.load(response)

    # By default, a subreddit displays the top 25 images;
    # we grab a random one of those
    random_index = randint(0, 24)

    # Next, we navigate the json and grab the link (generally imgur)
    # to the adorable image in question.
    image_link = j['data']['children'][random_index]['data']['url']

    # Now, we open the link with imgur!
    img = urllib2.urlopen(image_link).read()

    # Make sure everything works nice;
    # if it does, return our image
    try:
        im = Image.open(StringIO.StringIO(img))
        return im

        # What's a silly side project without unncessary recursion?
    except Exception:
        return grab_cute_image(username, trials - 1)


# A main to parse command-line arguments and display the image (if possible)
def main():
    argv = sys.argv
    argc = len(argv)

    im = None
    if argc < 2:
        im = grab_cute_image()
    else:
        im = grab_cute_image(argv[1])

    # If we fail to fetch an image, display an error-message
    if im is None:
        print('Unable to retrieve images after three tries :(.')
        return

    # Display our image using PIL
    im.show()
