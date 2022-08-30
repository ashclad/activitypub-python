# external modules
from validators import url
from varname import nameof
from re import search as match
import socket

# internal modules
import parsers
from custerr import *
from validap import *

@createValidator
def chkapValidity(data):
  if isinstance(data, (dict,str,list,APObject)):
    return True
  else:
    return False

class APObject(object):
  def __init__(self, cntxt, identi):
    if isinstance(cntxt, (list,dict,str)):
      self.context = cntxt
    else:
      raise TypeConstraintError(nameof(cntxt), (list,dict,str))

    if isinstance(identi, int):
      self.id = identi
    elif isinstance(identi, str):
      if url(identi):
        self.id = identi
      elif match('^\/[a-zA-Z0-9]+$', identi) is not None:
        self.id = socket.getfqdn() + identi
      else:
        raise ValueError('Invalid URI link')
    else:
      raise TypeConstraintError(nameof(identi), (int,str))

    self.type = type(self).__name__

    self.source = {}

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
      'nameMap',
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

  def __setattr__(self, k, v):
    if k in self.possible_attrs:
      if self.chkapValidity(v):
        object.__setattr__(self, k, v)
      else:
        raise TypeConstraintError(nameof(v), APObject)
    else:
      raise UnallowableAttributeError(k)

  def dump(self, targetstruct = '^[Jj][Aa]?[Ss][Oo][Nn]$'):
    for allowable in parsers.allowed_exports:
      if match(targetstruct, allowable) is not None:
        parsers.allowed_exports[allowable]['dump'](vars(self))
        break

  def load(self, data, sourcestruct = '^[Jj][Aa]?[Ss][Oo][Nn]$'):
    for allowable in parsers.allowed_exports:
      if match(sourcestruct, allowable) is not None and isinstance(data, str):
        new_dict = parsers.allowed_exports[allowable]['load'](data)

        for key in new_dict:
          setattr(self, key, new_dict[key])
        break

  def source(self, content, mtype):
    if isinstance(content, str):
      self.source['content'] = content
    else:
      raise TypeConstraintError(nameof(content), str)
    
    if isinstance(mtype, str):
      self.source['mediaType'] = mtype
    else:
      raise TypeConstraintError(nameof(content), str)

@createValidator
def chkapValidity(data):
  if isinstance(data, (dict,str,list,APObject)):
    return True
  else:
    return False

class Link(object):
  def __init__(self, href, rel, w = None, h = None):
    if isinstance(href, str):
      if url(href):
        self.href = href
      else:
        raise ValueError('Invalid URI link')
    else:
      raise TypeConstraintError(nameof(href), str)

    if isinstance(rel, (list,str)):
      self.rel = rel

    if h is not None and w is not None:
      if isinstance(w, int) and isinstance(h, int):
        self.width = w
        self.height = h
    
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

  def __setattr__(self, k, v):
    if k in self.possible_attrs:
      if self.chkapValidity(v):
        object.__setattr__(self, k, v)
      else:
        raise TypeConstraintError(nameof(v), APObject)
    else:
      raise UnallowableAttributeError(k)

  def dump(self, targetstruct = '^[Jj][Aa]?[Ss][Oo][Nn]$'):
    for allowable in parsers.allowed_exports:
      if match(targetstruct, allowable) is not None:
        parsers.allowed_exports[allowable]['dump'](vars(self))
        break

  def load(self, data, sourcestruct = '^[Jj][Aa]?[Ss][Oo][Nn]$'):
    for allowable in parsers.allowed_exports:
      if match(sourcestruct, allowable) is not None and isinstance(data, str):
        new_dict = parsers.allowed_exports[allowable]['load'](data)

        for key in new_dict:
          setattr(self, key, new_dict[key])
        break

class Activity(APObject):
  def __init__(self, cntxt, identi, actr, obj = None, result = None):
    super().__init__(cntxt, identi)

    oftype = (APObject, Link)
    if isinstance(actr, oftype):
      self.actor = actr
    elif isinstance(actr, str):
      if url(actr):
        self.actor = actr
      elif match('^\/[a-zA-Z0-9]+$', actr) is not None:
        self.actor = socket.getfqdn() + actr
      else:
        raise ValueError('Invalid URI link')
    else:
      raise TypeConstraintError(nameof(actr), (*oftype, str))

    if obj is not None:
      if isinstance(obj, oftype):
        self.object = obj
      elif isinstance(obj, str):
        if url(obj):
          self.object = obj
        elif match('^\/[a-zA-Z0-9]+$', obj) is not None:
          self.object = socket.getfqdn() + obj
        else:
          raise ValueError('Invalid URI link')
      else:
        raise TypeConstraintError(nameof(obj), (*oftype, str))

    if result is not None:
      if isinstance(result, (*oftype, str)):
        self.result = result
      elif isinstance(result, list):
        for r in result:
          if not isinstance(r, oftype):
            raise TypeConstraintError(nameof(r), oftype)

        self.result = result
      else:
        raise TypeConstraintError(nameof(result), (*oftype, list, str))

    self.possible_attrs += [
      'actor',
      'object',
      'target',
      'result',
      'origin',
      'instrument'
    ]

class IntransitiveActivity(Activity):
  def __init__(self, cntxt, identi, actr, target = None, result = None, obj = None):
    super().__init__(cntxt, identi, actr, obj, result)
    delattr(self, 'obj')

    if target is not None:
      if isinstance(target, (list,dict,str,APObject)):
        self.target = target
      else:
        raise TypeConstraintError(nameof(target), (list,dict,str,APObject))

class Collection(APObject):
  def __init__(self, cntxt, identi, items):
    super().__init__(cntxt, identi)

    if isinstance(items, list):
      for i in items:
        if not isinstance(i, (dict,APObject)):
          raise TypeConstraintError(nameof(i), dict)

      self.items = items
    else:
      raise TypeConstraintError(nameof(items), list)

    self.totalItems = len(items)

    self.possible_attrs += [
      'items',
      'first',
      'current',
      'last'
    ]

class OrderedCollection(Collection):
  def __init__(self, cntxt, identi, items):
    super().__init__(cntxt, identi, items)
    self.orderedItems = self.items
    delattr(self, 'items')

class CollectionPage(Collection):
  def __init__(self, cntxt, identi, items, memberof, nxt = None, prev = None):
    super().__init__(cntxt, identi, items)

    if isinstance(memberof, (Link, Collection)):
      self.partOf = memberof
    else:
      raise TypeConstraintError(nameof(memberof), (Link, Collection))

    if nxt is not None:
      if isinstance(nxt, (CollectionPage, Link)):
        self.next = nxt
      else:
        raise TypeConstraintError(nameof(nxt), (CollectionPage, Link))

    if prev is not None:
      if isinstance(prev, (CollectionPage, Link)):
        self.next = prev
      else:
        raise TypeConstraintError(nameof(nxt), (CollectionPage, Link))
    
    self.possible_attrs += [
      'partOf',
      'next',
      'prev'
    ]

class OrderedCollectionPage(OrderedCollection,CollectionPage):
  def __init__(self, cntxt, identi, items, memberof, start, nxt = None, prev = None):
    OrderedCollection.__init__(self, cntxt, identi, items)
    CollectionPage.__init__(self, cntxt, identi, items, memberof, nxt, prev)

    if isinstance(start, int):
      self.startIndex = start