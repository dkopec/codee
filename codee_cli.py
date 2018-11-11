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

from docopt import docopt
import codee
import json
import os
import code
from requests_oauthlib import OAuth1Session

version="Codee CLI v0.0.1"

def new_oauth(save_path, tokens={}):
    """
    Obtains and stores authorization information for OAuth1 connection.

    :param save_path:   a string, the name of the blog you want to use

    :returns: a dictionary, tokens for connecting using OAuth.
    """

    print('Adding new authorization credentials:')

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    if not 'consumer_key' in tokens:
        print('Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps')
        consumer_key = input('Paste the consumer key here: ')
        consumer_secret = input('Paste the consumer secret here: ')
        tokens['consumer_key'] = consumer_key;
        tokens['consumer_secret'] = consumer_secret;

    # STEP 1: Obtain request token
    oauth_session = OAuth1Session(tokens['consumer_key'], client_secret=tokens['consumer_secret'])
    fetch_response = oauth_session.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    # STEP 2: Authorize URL + Rresponse
    full_authorize_url = oauth_session.authorization_url(authorize_url)

    # Redirect to authentication page
    print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
    redirect_response = input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    oauth_response = oauth_session.parse_authorization_response(redirect_response)

    verifier = oauth_response.get('oauth_verifier')

    # STEP 3: Request final access token
    oauth_session = OAuth1Session(
        tokens['consumer_key'],
        client_secret=tokens['consumer_secret'],
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=verifier
    )
    oauth_tokens = oauth_session.fetch_access_token(access_token_url)

    tokens['oauth_token'] = oauth_tokens.get('oauth_token')
    tokens['oauth_token_secret'] = oauth_tokens.get('oauth_token_secret')

    with open(save_path, 'w+') as save_file:
        print("Saving to", save_path)
        json.dump(tokens, save_file)

    return tokens

if __name__ == '__main__':
    # arguments = docopt(__doc__, version=version)
    # print(arguments)

    save_path = os.path.join(os.path.expanduser('~'), '.tumblr')
    tokens = {}

    if not os.path.exists(save_path):
        print(save_path, "not found, creating.")
        tokens = new_oauth(save_path)
    else:
        print(save_path, "found, loading.")
        with open(save_path, "r") as save_file:
            tokens = json.load(save_file)

    client = codee.TumblrClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    print('codee client created. You may run codee commands prefixed with "client".\n')

    code.interact(local=dict(globals(), **{'client': client,'save_path':save_path}))
