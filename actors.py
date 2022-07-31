# external modules
import langcodes as lang

# internal modules
from generic import APObject
from custerr import *

class Application(APObject):
  def __init__(self, cntxt, identi, name, altname = None):
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

class Group(APObject):
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

    if isinstance(altname, str):
      self.preferredUsername = altname
    else:
      raise TypeConstraintError(nameof(altname), str)

    self.possible_attrs += [
      'preferredUsername',
      'inbox',
      'outbox',
      'following',
      'followers',
      'liked',
      'streams',
      'endpoints'
    ]

class Organization(APObject):
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

class Person(APObject):
  def __init__(self, cntxt, identi, name, altname = None):
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

    if altname is not None:
      if isinstance(altname, str):
        self.preferredUsername = altname
      else:
        raise TypeConstraintError(nameof(altname), str)

    self.possible_attrs += [
      'preferredUsername',
      'inbox',
      'outbox',
      'following',
      'followers',
      'liked',
      'streams',
      'endpoints'
    ]

class Service(APObject):
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