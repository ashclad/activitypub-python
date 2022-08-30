# external modules
import langcodes as lang
from validators import url
import socket
import crypt

# internal modules
from generic import APObject
from custerr import *
from oauth import AuthCommunication, OAuthentication

class Actor(APObject):
  def __init__(self, cntxt, identi, name):
    super().__init__(cntxt, identi)
    
    if isinstance(name, str):
      self.name = name
    elif isinstance(name, dict):
      self.nameMap = {}
      for k in name:
        if lang.tag_is_valid(k):
          self.nameMap[k] = name[k]
        else:
          raise ValueError('Invalid language code')
    else:
      raise TypeConstraintError(nameof(name), (str, dict))

    self.possible_attrs += [
      'inbox',
      'outbox',
      'following',
      'followers',
      'liked',
      'streams',
      'endpoints'
    ]

    self.streams = []
    self.endpoints = []

  def set_inbox(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, str):
        if url(endpoint):
          self.inbox = endpoint
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(endpoint), str)
    else:
      self.inbox = socket.getfqdn() + '/ap/@' + self.name + '/in'

  def set_outbox(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, str):
        if url(endpoint):
          self.outbox = endpoint
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(endpoint), str)
    else:
      self.outbox = socket.getfqdn() + '/ap/@' + self.name + '/out'

  def set_following(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, str):
        if url(endpoint):
          self.following = endpoint
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(endpoint), str)
    else:
      self.following = socket.getfqdn() + '/ap/@' + self.name + '/following'

  def set_followers(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, str):
        if url(endpoint):
          self.followers = endpoint
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(endpoint), str)
    else:
      self.followers = socket.getfqdn() + '/ap/@' + self.name + '/followers'

  def set_liked(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, str):
        if url(endpoint):
          self.liked = endpoint
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(endpoint), str)
    else:
      self.liked = socket.getfqdn() + '/ap/@' + self.name + '/likes'

  def add_stream(self, endpoint = None):
    if endpoint is not None:
      if isinstance(endpoint, list):
        for end in endpoint:
          if not isinstance(end, str):
            raise TypeConstraintError(nameof(end), str)

          if not url(end):
            if not match('^\/[a-zA-Z0-9]+$', end):
                raise ValueError('Invalid URI link')
          
        self.streams += endpoint
      elif isinstance(endpoint, str):
        if url(endpoint):
          self.streams.append(endpoint)

  def add_endpoint(self, endpoint = None):    
    if endpoint is not None:
      if isinstance(endpoint, list):
        for end in endpoint:
          if not isinstance(end, (AuthCommunication, OAuthentication)):
            raise Exception()
        
        self.endpoints = endpoint
      elif isinstance(endpoint, (AuthCommunication, OAuthentication)):
        self.endpoints = endpoint

class Application(Actor):
  def __init__(self, cntxt, identi, name, altname = None):
    super().__init__(cntxt, identi, name)

    if isinstance(altname, str):
      self.preferredUsername = altname
    else:
      raise TypeConstraintError(nameof(altname), str)

class Group(Actor):
  def __init__(self, cntxt, identi, name):
    super().__init__(cntxt, identi, name)

    self.possible_attrs += [
      'preferredUsername'
    ]

class Organization(Actor):
  def __init__(self, cntxt, identi, name):
    super().__init__(cntxt, identi, name)

class Person(Actor):

  def __init__(self, cntxt, identi, name, altname = None):
    super().__init__(cntxt, identi, name)

    if altname is not None:
      if isinstance(altname, str):
        self.preferredUsername = altname
      else:
        raise TypeConstraintError(nameof(altname), str)

    self.possible_attrs += [
      'preferredUsername'
    ]

class Service(Actor):
  def __init__(self, cntxt, identi, name):
    super().__init__(cntxt, identi, name)