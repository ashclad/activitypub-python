# external modules
from validators import url as urlvalidate
from varname import nameof
from re import search as match

# internal modules
import config as conf
from custerr import *
from validap import *

class ObjectFreezer(object):
  __freeze = False

  def __setattr__(self, k, v):
    if self.__freeze and not hasattr(self, k):
      raise UnmutableAttributeError()
    else:
      object.__setattr__(self, k, v)

class sourceContent(ObjectFreezer):
  def __init__(self, cnt, mtype):
    self.content = cnt
    self.mediaType = mtype
    self.__freeze = True

class APObject(object):
  def __init__(self, cntxt, identi):
    if isinstance(cntxt, (list,dict,str)):
      self.context = cntxt
    else:
      raise TypeConstraintError(nameof(cntxt), (list,dict,str))

    if isinstance(identi, int):
      self.id = identi
    elif isinstance(identi, str):
      if urlvalidate(identi):
        self.id = identi
    else:
      raise TypeConstraintError(nameof(identi), (int,str))

    self.type = type(self).__name__

    self.possible_attrs = [
      'content',
      'contentMap',
      'context',
      'id',
      'type',
      'tag',
      'source',
      'summary',
      'attachment',
      'attributeTo',
      'audience',
      'name',
      'endTime',
      'startTime',
      'generator',
      'inReplyTo',
      'image',
      'icon',
      'location',
      'published',
      'preview',
      'replies',
      'updated',
      'url',
      'to',
      'bto',
      'cc',
      'bcc',
      'mediaType',
      'duration'
    ]

  @createValidator
  def chkapValidity(data):
    if isinstance(data, (dict,str,list,APObject)):
      return True
    else:
      return False

  def __setattr__(self, k, v):
    if k in self.possible_attrs:
      if self.chkapValidity(v):
        object.__setattr__(self, k, v)
      else:
        raise TypeConstraintError(nameof(v), APObject)
    else:
      raise UnallowableAttributeError(k)

  def drop(self, targetstruct = 'json'):
    for allowable in conf.allowed_exports:
      if match(allowable, targetstruct) is not None:
        conf.allowed_exports[allowable]['dump'](vars(self))
        break

  def load(self, data, sourcestruct = 'json'):
    for allowable in conf.allowed_exports:
      if match(allowable, sourcestruct) is not None and isinstance(data, str):
        new_dict = conf.allowed_exports[allowable]['load'](data)

        for key in new_dict:
          setattr(self, key, new_dict[key])
        break

class Link(object):
  def __init__(self, href, rel):
    if isinstance(href, str):
      if urlvalidate(href):
        self.href = href

    if isinstance(rel, (list,str)):
      self.rel = rel
    
    self.possible_attrs = [
      'href',
      'rel',
      'mediaType',
      'name',
      'hreflang',
      'height',
      'width',
      'preview'
    ]

  @createValidator
  def chkapValidity(data):
    if isinstance(data, (dict,str,list,APObject)):
      return True
    else:
      return False

  def __setattr__(self, k, v):
    if k in self.possible_attrs:
      if self.chkapValidity(v):
        object.__setattr__(self, k, v)
      else:
        raise TypeConstraintError(nameof(v), APObject)
    else:
      raise UnallowableAttributeError(k)

  def drop(self, targetstruct = 'json'):
    for allowable in conf.allowed_exports:
      if match(allowable, targetstruct) is not None:
        conf.allowed_exports[allowable]['dump'](vars(self))
        break

  def load(self, data, sourcestruct = 'json'):
    for allowable in conf.allowed_exports:
      if match(allowable, sourcestruct) is not None and isinstance(data, str):
        new_dict = conf.allowed_exports[allowable]['load'](data)

        for key in new_dict:
          setattr(self, key, new_dict[key])
        break

class Activity(APObject):
  def __init__(self, cntxt, identi, actr, obj):
    super().__init__(cntxt, identi)
    self.possible_attrs += [
      'actor',
      'object',
      'target',
      'result',
      'origin',
      'instrument'
    ]
    self.actor = actr
    self.object = obj

class Collection(APObject):
  def __init__(self, cntxt, identi, items):
    super().__init__(cntxt, identi)
    self.possible_attrs += [
      'items',
      'first',
      'current',
      'last'
    ]
    self.items = items
    self.totalItems = len(items)

class OrderedCollection(Collection):
  def __init__(self, cntxt, identi, items):
    super().__init__(cntxt, identi, items)
    self.orderedItems = self.items

class CollectionPage(Collection):
  def __init__(self, cntxt, identi, items, memberof):
    super().__init__(cntxt, identi, items)
    self.possible_attrs += [
      'partOf',
      'next',
      'prev'
    ]
    self.partOf = memberof

class OrderedCollectionPage(CollectionPage):
  def __init__(self, cntxt, identi, items, memberof, start):
    super().__init__(cntxt, identi, items, memberof)

    if isinstance(start, int):
      self.startIndex = start