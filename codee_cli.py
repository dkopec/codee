#!/usr/bin/python
"""Codee CLI

Automation tool for Tumblr

Usage:
    codee_cli.py [options] <input>

Options:
    -h, --help  display this text.

"""

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import input

import codee
import json
import errno
import os
import code
from requests_oauthlib import OAuth1Session
import webbrowser

class CodeeCLI():

    def __init__(self, save_folder = os.path.join(os.path.expanduser('~'), '.codee')):
        self.save_folder = save_folder

        if not os.path.exists(self.save_folder):
            print("{0} does not exist, create? (y/n):").format(self.save_folder)
            answer = input().lowercase

            if answer in ['y', 'yes']:
                os.mkdir(self.save_folder)
            else:
                exit()

        tumblr_auth_save_path = os.path.join(save_folder, 'tumblr')

        self.tumblroauth = TumblrOAuth(tumblr_auth_save_path)

        self.handler = FileHandler()

class FileHandler():

    def load(self, path):
        with open(path, "r") as file:
            print("Loading from: ", path)
            loaded = json.load(file)
            return loaded

    def save(self, path, data):
        with open(path, 'w+') as file:
            print("Saving to: ", path)
            json.dump(data, file, indent=2)


class TumblrOAuth():
    """
    Obtains and stores authorization information for OAuth1 connection.

    :param save_path:   a string, the name of the blog you want to use

    :returns: a dictionary, tokens for connecting using OAuth.
    """

    def __init__(self, save_path, consumer_key="", consumer_secret="", oauth_token="", oauth_secret =""):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_secret = oauth_secret

        handler = FileHandler()

        request_token_url = 'http://www.tumblr.com/oauth/request_token'
        authorize_url = 'http://www.tumblr.com/oauth/authorize'
        access_token_url = 'http://www.tumblr.com/oauth/access_token'

        if not os.path.exists(save_path):
            print(save_path, " not found, create new tumblr authorization file? (y/n)")
            answer = input().lower()

            if answer in ['y', 'yes']:
                handler.save(save_path, self.to_json())

            else:
                exit()

        else:
            print(save_path, "found, loading.")
            save_file = handler.load(save_path)
            self.consumer_key = save_file['consumer_key']
            self.consumer_secret = save_file['consumer_secret']
            self.oauth_token = save_file['oauth_token']
            self.oauth_secret = save_file['oauth_secret']

        if self.consumer_key == "" or self.consumer_secret == "" :
            print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
            self.consumer_key = input('Paste the consumer key here: ')
            self.consumer_secret = input('Paste the consumer secret here: ')
            handler.save(save_path, self.to_json())

        if self.oauth_token == "" or self.oauth_secret == "":
            # STEP 1: Obtain request token
            oauth_session = OAuth1Session(self.consumer_key, client_secret=self.consumer_secret)
            fetch_response = oauth_session.fetch_request_token(request_token_url)
            resource_owner_key = fetch_response.get('oauth_token')
            resource_owner_secret = fetch_response.get('oauth_token_secret')

            # STEP 2: Authorize URL + Rresponse
            full_authorize_url = oauth_session.authorization_url(authorize_url)

            # Redirect to authentication page
            webbrowser.open(full_authorize_url)
            print("\nPlease go here and authorize if the page hasn't opened:\n{}".format(full_authorize_url))
            redirect_response = input('Allow then paste the full redirect URL here:\n')

            # Retrieve oauth verifier
            oauth_response = oauth_session.parse_authorization_response(redirect_response)

            verifier = oauth_response.get('oauth_verifier')

            # STEP 3: Request final access token
            oauth_session = OAuth1Session(
                self.consumer_key,
                client_secret=self.consumer_secret,
                resource_owner_key=resource_owner_key,
                resource_owner_secret=resource_owner_secret,
                verifier=verifier
            )
            oauth_tokens = oauth_session.fetch_access_token(access_token_url)

            self.oauth_token = oauth_tokens.get('oauth_token')
            self.oauth_secret = oauth_tokens.get('oauth_token_secret')

            handler.save(save_path, self.to_json())

    def to_json(self):

        return {
            'consumer_key': self.consumer_key,
            'consumer_secret': self.consumer_secret,
            'oauth_token': self.oauth_token,
            'oauth_secret': self.oauth_secret
        }

if __name__ == '__main__':

    cli = CodeeCLI()

    tumblrapi = codee.TumblrRestClient(
        cli.tumblroauth.consumer_key,
        cli.tumblroauth.consumer_secret,
        cli.tumblroauth.oauth_token,
        cli.tumblroauth.oauth_secret
    )

    print('codee client created. You may run codee commands prefixed with "tumblrapi" and "cli".\n')

    code.interact(local=dict(globals(), **{'tumblrapi': tumblrapi, 'cli': cli}))
