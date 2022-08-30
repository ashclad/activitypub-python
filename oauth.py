# external modules
from validators import url
from re import search as match
import socket
from hashlib import sha256 as hash256
from uuid import uuid5, NAMESPACE_DNS
import secrets
import yaml as yml
from authlib.integrations import requests_client as rqclient
import requests

# internal modules
import parsers

conf = parsers.ConfMan()

class Client:
  red_uri = socket.getfqdn() + '/ap/receptor'

  def __init__(self, name, config = conf, reduri = None):
    self.config = config
    self.current_index = -1

    if isinstance(name, str):
      self.name = name
    
    clientid = str(uuid5(NAMESPACE_DNS, self.name))
    clientsecret = hash256(clientid.encode('utf8') + secrets.token_hex(128).encode('utf8')).hexdigest()

    self.cid = clientid
    self.secret = clientsecret

    if 'APPS' not in self.config:
      self.config['APPS'] = []

    self.config['APPS'].append({
      'NAME': self.name,
      'ID': clientid,
      'SECRET': clientsecret
    })

    if reduri is None:
      self.config['APPS'][-1]['RED_URI'] = Client.red_uri
    else:
      if isinstance(reduri, str):
        if url(reduri):
          self.red_uri = reduri
          self.config['APPS'][-1]['RED_URI'] = reduri
        else:
          raise Exception()
      else:
        raise Exception()

    self.config.commit()

  def key_uris(self, ckeyuri, skeyuri):
    if isinstance(ckeyuri, str):
      if url(ckeyuri):
        self.provideClientKey = ckeyuri
      elif match('^\/[a-zA-Z0-9]+$', ckeyuri) is not None:
        self.provideClientKey = socket.getfqdn() + '/ap/httsign' + ckeyuri

    if isinstance(skeyuri, str):
      if url(skeyuri):
        self.signClientKey = skeyuri
      elif match('^\/[a-zA-Z0-9]+$', skeyuri) is not None:
        self.signClientKey = socket.getfqdn() + '/ap/httsign' + skeyuri

  def append(self, clientname):
    if isinstance(clientname, str):
      clientid = str(uuid5(NAMESPACE_DNS, clientname))
      clientsecret = hash256(clientid.encode('utf8') + secrets.token_hex(128).encode('utf8')).hexdigest()

    self.config['APPS'].append({
      'NAME': clientname,
      'ID': clientid,
      'SECRET': clientsecret
    })

    self.config.commit()

  def __len__(self):
    return len(self.config['APPS'])

  def __getitem__(self, k):
    if isinstance(k, int):
      return self.config['APPS'][k]
    elif isinstance(k, str):
      for app in self.config['APPS']:
        if app['NAME'] == k:
          return app

  def __setitem__(self, k, v):
    if isinstance(k, int):
      if isinstance(v, dict):        
        self.config['APPS'][k] = v
      else:
        raise Exception()
    elif isinstance(k, str):
      for i in range(len(self.config['APPS'])):
        if self.config['APPS'][i]['NAME'] == k:
          if isinstance(v, dict):
            self.config['APPS'][i] = v
            break
          else:
            raise Exception()
    else:
      raise Exception()

  def __delitem__(self, k):
    if isinstance(k, int):
      del self.config['APPS'][k]
    elif isinstance(k, str):
      for i in range(len(self.config['APPS'])):
        if self.config['APPS'][i]['NAME'] == k:
          del self.config['APPS'][i]
          break
    else:
      raise Exception()

  def __iter__(self):
    return iter(self.config['APPS'])

  def switch(self, k = None):
    if k is not None:
      if isinstance(k, int):
        self.name = self.config['APPS'][k]['NAME']
        self.cid = self.config['APPS'][k]['ID']
        self.secret = self.config['APPS'][k]['SECRET']
        self.red_uri = self.config['APPS'][k]['RED_URI']
      elif isinstance(k, str):
        for i in range(len(self.config['APPS'])):
          if self.config['APPS'][i]['NAME'] == k:
            self.name = self.config['APPS'][i]['NAME']
            self.cid = self.config['APPS'][i]['ID']
            self.secret = self.config['APPS'][i]['SECRET']
            self.red_uri = self.config['APPS'][i]['RED_URI']
            break
    else:
      self.current_index += 1

      self.current_index = self.current_index % len(self.config)

      self.name = self.config['APPS'][self.current_index]['NAME']
      self.cid = self.config['APPS'][self.current_index]['ID']
      self.secret = self.config['APPS'][self.current_index]['SECRET']
      self.red_uri = self.config['APPS'][self.current_index]['RED_URI']

  def commit(self):
    self.config.commit()

  def init_session(self, scope, endpoint = None):
    if isinstance(scope, (list, str)):
      oauthclient = rqclient.OAuth2Session(self.cid, self.secret, scope = scope)
    else:
      raise Exception()

    if endpoint is None:
      return oauthclient
    else:
      if isinstance(endpoint, str):
        if url(endpoint):
          uri, state = oauthclient.create_authorization_url(endpoint)
          self.state = {}
          self.state[self.name] = state
        else:
          raise Exception()
      else:
        raise Exception()

      return (uri, state)

class OAuthentication:
  def __init__(self, granturi, tokenuri, config = conf):
    if url(granturi):
      self.oauthAuthorizationEndpoint = granturi
    elif match('^\/[a-zA-Z0-9]+$', granturi) is not None:
      self.oauthAuthorizationEndpoint = socket.getfqdn() + '/ap' + granturi

    if url(tokenuri):
      self.oauthTokenEndpoint = tokenuri
    elif match('^\/[a-zA-Z0-9]+$', tokenuri) is not None:
      self.oauthTokenEndpoint = socket.getfqdn() + '/ap' + tokenuri

    self.config = config
    self.config['OAUTH'] = {}

  def commit(self):
    self.config['OAUTH']['AUTH_URI'] = self.oauthAuthorizationEndpoint
    self.config['OAUTH']['TOKE_URI'] = self.oauthTokenEndpoint
    self.config.commit()

  def parametize(self, mode = 'authorize', **kwargs):
    allowed_modes = [
      '^[Aa][Uu][Tt][Hh]([Oo][Uu]?[Rr][Ii][ZzSs][Ee])?$',
      '^[Tt][Oo][Kk][Ee][Nn]([Ii][Zz][Ee]| ?[Ee][Xx][Cc][Hh][Aa][Nn][Gg][Ee])?$'
    ]

    resultstr = ''
    if match(allowed_modes[0], mode) is not None:
      resultstr = self.oauthAuthorizationEndpoint
    elif match(allowed_modes[1], mode) is not None:
      resultstr = self.oauthTokenEndpoint
    else:
      raise Exception()

    if len(kwargs) > 0:
      resultstr += '?'
      for k, v in kwargs.items():
        resultstr += str(k) + '=' + str(v)
        resultstr += '&'
      resultstr = resultstr[0:len(resultstr) - 1]

    return resultstr

class AuthCommunication:
  def __init__(self, proxuri = None, shareduri = None):
    if proxuri is not None:
      if isinstance(proxuri, str):
        if url(proxuri):
          self.proxyUrl = proxuri
        elif match('^/[a-zA-Z0-9]+$', proxuri):
          self.proxyUrl = socket.getfqdn() + proxuri
        else:
          raise Exception()
      else:
        raise Exception()
    else:
      self.proxyUrl = ''

    if shareduri is not None:
      if isinstance(shareduri, str):
        if url(shareduri):
          self.sharedInbox = shareduri
        elif match('^/[a-zA-Z0-9]+$', shareduri):
          self.sharedInbox = socket.getfqdn() + shareduri
        else:
          raise Exception()
      else:
        raise Exception()

  def init_client(self, name, config = None):    
    if config is not None:
      if isinstance(name, str):
        client = Client(name, config)
      else:
        raise Exception()
    else:
      client = Client(name)

    self.client = client
    self.client.commit()
    return self.client

  def init_oauth(self, granturi, tokenuri, config = None):
    if config is not None:
      oauth = OAuthentication(granturi, tokenuri, config)
    else:
      oauth = OAuthentication(granturi, tokenuri)

    self.oauth = oauth
    self.oauth.commit()
    return self.oauth

  def get_access(self, scope):
    if isinstance(scope, (list, str)):
      stateuri = self.client.init_session(scope, self.oauth.oauthAuthorizationEndpoint)
      self.scope = scope
    else:
      raise Exception()
    
    self.state = stateuri[1]
    token = self.client.fetch_token(self.oauthTokenEndpoint, authorization_response = stateuri[0])
    self.access_token = token['access_token']
    self.token_type = token['token_type']
    auth = rqclient.OAuth2Auth(token)
    self.authorizer = auth
    
    return auth

  def request(self, uri, rqtype = 'get', **kwargs):
    if isinstance(uri, str):
      if url(uri):
        if kwargs is None or len(kwargs.keys()) <= 0:
          result = requests.request(rqtype, uri, auth = self.authorizer)
        else:
          result = requests.request(rqtype, uri, auth = self.authorizer, **kwargs)
      else:
        raise Exception()
    else:
      raise Exception()

    return result