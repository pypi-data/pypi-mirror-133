#!/usr/bin/python3
###############################################################################
# Copyright 2015-2018 Tim Stephenson and contributors
# 
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not
#  use this file except in compliance with the License.  You may obtain a copy
#  of the License at
# 
#    http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations under
#  the License.
#
# Command line client for interacting with REST services
#
###############################################################################
import argparse
import configparser
from configparser import ConfigParser
import json
from oauthlib.oauth2 import LegacyApplicationClient
from pathlib import Path
from requests_oauthlib import OAuth2Session
import sys
import urllib.request
import urllib.parse

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("url", help="api url to call")
parser.add_argument("-d", "--data", help="payload, if expected by server")
parser.add_argument("-u", "--user",
    help="USER[:PASSWORD]  Server user and password")
parser.add_argument("-X", "--verb", help="specify HTTP verb explicitly (GET and POST are implicit)")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
    action="store_true")
args = parser.parse_args()

cfg_file = Path.home().joinpath(".kp.conf")
config = ConfigParser()
config.read(str(cfg_file))

host = args.url[:args.url.index('/', 8)]

# find credentials
if args.user:
  usr = args.user[:args.user.index(':')]
  pwd = args.user[args.user.index(':')+1:]
elif cfg_file.is_file():
  try:
    key = host[host.index('://')+3:]
    if args.verbose:
      print('looking up credentials for {} ...'.format(key))
    auth_url = config.get(key, 'auth_url')
    usr = config.get(key, 'username')
    pwd = config.get(key, 'password')
    if args.verbose:
      print('... found {}:**** ...'.format(usr))
      print('... {} ...'.format(auth_url))
  except configparser.NoSectionError as e:
    print("ERROR: No section named '{}' in config file".format(key))
    parser.print_help()
    sys.exit(-1)
  except configparser.NoOptionError as e:
    print("ERROR: No user parameter and no key in config file for '{}'".format(key))
    parser.print_help()
    sys.exit(-1)
else:
  parser.print_help()
  sys.exit(0)
 
# login 
auth_url = 'https://auth.knowprocess.com/auth/realms/knowprocess/protocol/openid-connect/token'
if args.verbose:
  print('attempt to login to {} ...'.format(auth_url))

try:
  client_id = 'srp'
  oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
  token = oauth.fetch_token(token_url=auth_url, client_id=client_id, username=usr, password=pwd)
  if args.verbose:
    print('... login succeeded')

  #token = json.loads(respData.decode("utf-8"))['token']
except Exception as e:
  print('{} Unable to login'.format(e))
  sys.exit(0)

# make request
headers = {
  "X-Requested-With": "XMLHttpRequest",
  "Content-Type": "application/json",
  "Cache-Control": "no-cache",
  "Authorization": 'Bearer '+token['access_token'],
  "X-RunAs": usr

}

if args.verbose:
  print('connecting to {}'.format(args.url))

if args.data:
  if args.verbose:
    print('payload is: {}'.format(args.data))
  if args.data.find('=') != -1:
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    if args.verbose:
      print('content type: {}'.format(headers['Content-Type']))
  data = args.data.encode('utf-8')
  req = urllib.request.Request(args.url, data, headers = headers)
else:
  req = urllib.request.Request(args.url, headers = headers)

if args.verb:
  if args.verbose:
    print('HTTP method: '+args.verb)
  req.get_method = lambda: args.verb
try:
  resp = urllib.request.urlopen(req)
  respData = resp.read()
  if args.verbose:
    print('SUCCESS')
  print(respData.decode('UTF-8'))
except urllib.error.HTTPError as e:
  if args.verbose:
    print('ERROR: {}: {}'.format(e.code, e.reason))
