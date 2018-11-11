from __future__ import absolute_import
from builtins import str
from builtins import object
from .helpers import validate_params, validate_blogname
from .request import TumblrRequest

import pytumblr

class TumblrClient(object):
    """
    A Python automation tool for the Tumblr
    """

    def __init__(self, consumer_key, consumer_secret="", oauth_token="", oauth_secret=""):
        """
        Initializes the Codee object, creating the pytumblr TumblrRestClient
        object which deals with all API requests.

        :param consumer_key:    a string, the consumer key of your
                                Tumblr Application
        :param consumer_secret: a string, the consumer secret of
                                your Tumblr Application
        :param oauth_token:     a string, the user specific token, received
                                from the /access_token endpoint
        :param oauth_secret:    a string, the user specific secret, received
                                from the /access_token endpoint

        :returns: None
        """

        self.client = pytumblr.TumblrRestClient(consumer_key, consumer_secret, oauth_token, oauth_secret)

        self.user_info = self.client.info()

        self.blogs = []

        for blog in self.user_info['user']['blogs']:
            self.blogs.append(blog['name'])

    def say_hello(self):
        """
        Simple hello world function.

        :returns: a string, Hello!
        """
        return "Hello!"

    def queue_post(self, blog, post_id, type):
        """
        Transfers post from a given blogs drafts to its queue.

        :param blog_name: a string, the name of the blog you want to use
        :param post_id:   a string, the unique id of the post you want to queue
        :param type:      a string, the type of post it is, required for editing

        :returns: None
        """
        self.client.edit_post(blog, id=post_id, type=type, state='queue')

    def draft_post(self, blog, post_id, type):
        """
        Transfers post from a given blogs drafts to its queue.

        :param blog_name: a string, the name of the blog you want to use
        :param post_id:   a string, the unique id of the post you want to queue
        :param type:      a string, the type of post it is, required for editing

        :returns: None
        """
        self.client.edit_post(blog, id=post_id, type=type, state='draft')

    def draft_queued(self, blog_name):
        """
        Transfers posts from a given blogs queue to its drafts until the queue
        is empty.

        :param blog_name:       a string, the name of the blog you want to use

        :returns: None
        """

        queued = self.client.queue(blog_name)

        for index, post in enumerate(queued["posts"]):
            self.draft_post(blog_name, post['id'], type=post['type'])

    def queue_drafts(self, blog_name, organic=True):
        """
        Transfers posts from a given blogs drafts to its queue until the queue
        is full or drafts are empty.

        :param blog_name:       a string, the name of the blog you want to use
        :param organic:         a boolean, an option to queue posts in a organic
                                fashion (one post from a author at a time)
                                rather than as is in the drafts.

        :returns: None
        """
        drafts = self.client.drafts(blog_name)

        for index, post in enumerate(drafts["posts"]):
            # If organic option is enabled
            if organic and index > 0:
                # Skip the post if it is not by the same author as the last
                try:
                    current_author = drafts["posts"][index]['trail'][0]['blog']['name']
                except:
                    try:
                        current_author = drafts["posts"][index]['tags'][0]
                    except:
                        continue
                try:
                    previous_author = drafts["posts"][index-1]['trail'][0]['blog']['name']
                except:
                    try:
                        previous_author = drafts["posts"][index-1]['tags'][0]
                    except:
                        continue

                print("Current author is:  ", current_author)
                print("Previous author is: ", previous_author)

                if current_author == previous_author:
                    print("skipping...")
                    continue

            print("Queuing post#", post['id'])
            self.queue_post(blog_name, post['id'], type=post['type'])

        self.queue_drafts(blog_name, organic)

    #TODO:def reblog_every(self,post_id,blog_id):
