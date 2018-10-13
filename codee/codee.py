# codee v 0.0.1
# Copyright Dominik Kopec (kopec.dominik@gmailcom) dkopec.com
"""
    A bot to handle day to day tasks on tumblr:
    * reblog posts similair to past items you've rebloged and ensure they are tagged appropriatly.
    * queue posts from drafts so that it looks organic and non repetetive, aviod posts tagged with specific tags
    * look for and block spam bot accounts
    * find and queue posts from new sources found tagged with specific tag
    * Tumblrbot utilizes an internal queue that will adapt to the queue on tumblr allowing the user to have a clear distinction between the two sources.
    * be able to reblog same post over and over acording to a schedule
    *
"""

import tumblr
def __init__(self):


def main():


def queue_drafts(blog):
    while not blog.drafts.empty():
        if blog.queue.full():
            print("Queue is full.")
            return
        else:
            print("Checking posts $ agianst rules for $").format(blog.drafts.post.id, blog.name)
            if check_rules(blog.drafts.post):
                print("Post $ passed rules adding to $").format(blog.drafts.post.id, blog.name)
                blog.queue.add(blog.drafts.post)
            else:
                print("Post $ failed rules, skipping").format(blog.drafts.post.id)
    print("Drafts are empty.")

def process_tagged(tag):
    #TODO: implement

def process_submission(blog):
    #TODO: implement

def process_dashboard(user):
    #TODO: implement

def monitor_posts():
    #TODO: implement

def reblog_every(amount, unit):
    #TODO: implement
