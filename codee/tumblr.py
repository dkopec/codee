# PyTumblr Wrapper v0.0.1
#
# Utilzers PyTumblr CLient
# https://api.tumblr.com/console/calls/blog/posts

# client.reblog(blog+'.tumblr.com', id=id, reblog_key=reblog_key)
# client.tagged(tag,before=timestamp)
# client.posts(blog, limit=20, offset=offset,reblog_info=True, notes_info=True)
# client.like(id, reblog_key)

import pytumblr
import re, sys, os, json, time, random
from time import sleep

class Tumblr(): # Establishes connection to Tumblr and contains basic functions for retriving information

    def __init__(self):
        self.TUMBLR_CONSUMER_KEY = os.environ["TUMBLR_CONSUMER_KEY"]
        self.TUMBLR_CONSUMER_SECRET = os.environ["TUMBLR_CONSUMER_SECRET"]
        self.TUMBLR_OAUTH_TOKEN = os.environ["TUMBLR_OAUTH_TOKEN"]
        self.TUMBLR_OAUTH_SECRET = os.environ["TUMBLR_OAUTH_SECRET"]
        self.type = "connection"

        try:
            print("Connecting to Tumblr API.")
            self.client = pytumblr.TumblrRestClient(TUMBLR_CONSUMER_KEY,TUMBLR_CONSUMER_SECRET,TUMBLR_OAUTH_TOKEN,TUMBLR_OAUTH_SECRET)
        except:
            print("Error connecting to API")

    def pull(self):
        pass

    def save(self):
        pass

    # saves data to file default json
    def save_to(data, filename, filetype = "json"):
        with open('{}.{}'.format(filename, filetype), 'w') as out_file:
            json.dump(data, out_file)

    # Random duration sleep method with a default minimum delay of 1 minute and a max delay of 1 hour.
    def randsleep(min=60,max=3600):
        random_n = random.randint(min,max)
        sleep(random_n)

    # Iterates through and returns all avialable data for given dataset through tumblr API in json format
    # TODO caching files
    def pull_all(limit=None, before, max=None):
        offset = 0
        container = None;

        while True:
            if max and offset >= max: return container

            response = self.pull(offset)

            # if first run store full response
            if not container:
                container = response
                # otherwise update posts elements
            else:
                #check to see if there are any more posts
                if not response[self.type]: return container
                else: container[self.type] += response[self.type]

                # move to the next offset
                offset += 20

class User(Tumblr): # has 1 or more UserBlogs, and a Following and Liked

    def __init__(self):
        Tumblr.__init__(self)
        self.type = "user"
        self.user_info = self.pull()
        self.user_blogs = [Blog()]
        self.following = Following(self)

    def info(self):

    def pull(self):
        return = self.client.info()

class Following(User): #list of Blogs the User followed TODO: implement

    def __init__(self):
        User.__init__(self)
        self.type = "following"
        self.all_following = self.client.

    def pull(self, offset=None):
        self.client.following(offset=offset)

class Liked(Tumblr): # list of Posts that the User liked TODO: implement

class Queue(Tumblr): # collection of Posts, published according to schedule TODO: implement

class Drafts(Tumblr): # collection of Posts TODO: implement

class Blog(Tumblr): # has 0 or more Posts, 0 or more Followers (can be hiddem)

    def __init__(blog_name):
        Tumblr.__init__()
        self.type = "blog"
        self.blog_name = blog_name
        self.blog_url = "{}.tumblr.com".format(blog_name)
        self.info = self.client.blog_info()

    def info(self):
        # return info on blog

    def follow(self):
        self.client.follow(blog_url)

    def unfollow(self):
        self.client.unfollow(blog_url)

    def pull(self):
        return self.client.posts(self.blogname, limit=20, offset=offset, reblog_info=True, notes_info=True)

class UserBlog(Blog): # has Queue and Drafts TODO: implement

class Post(Blog): #has 0 or more Tags and Content
    def __init__( post_id, reblog_key):
        Blog.__init__(blog_name)
        self.type = "posts"
        self.post_id = post_id
        self.reblog_key = reblog_key
        self.post_info = self.pull()

    def pull(self):
        """use api to download data from tumblr"""
        return client.posts(self.blog_name, id=self.post_id, reblog_info=True, notes_info=True)
    # reblog
    def reblog(comment=None):
        """ reblog the post"""
        self.client.reblog(self.blogname, id=self.post_id, reblog_key=self.reblog_key, comment=comment)

    # like
    def like(self):
        """ like the post. """
        try:
            self.client.like(self.post_id, self.reblog_key)
            return True
        except:
            return False

    # unlike
    def unlike(self):
        """ unlike the post. """
        try:
            self.client.unlike(self.post_id, self.reblog_key)
            return True
        except:
            return False

    # like and reblog
    def like_reblog(comment=None):
        self.reblog(comment)
        self.like()

    # delete post from blog TODO: figure out if how to ensure it pull deleted from cache or wherever it's being kept locally
    def delete(self):
        try:
            self.client.delete_post(self.blog_name, self.post_id)
            return True
        except:
            return False

    # TODO develope this, figure out the criteria and how to learn
    def check_if_spam(self):

        rules for spam
        if :
            return True
        else:
            return False

    def queue() 



class Content(): #TODO: implement

class Tag(): #TODO: implement

    def __init__:
        self.tag = ""
        self.posts =
