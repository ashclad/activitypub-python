# external modules
from validators import url as validate
from re import search as match
from varname import nameof
import datetime as dt
import langcodes as lang

# internal modules
from generic import APObject, Link
from actors import Group, Application, Organization, Person, Service
from regxsd import xsd
from custerr import *

class Note(APObject):
  def __init__(self, cntxt, identi, content):
    super().__init__(cntxt, identi)

    if isinstance(content, str):
      self.content = content
    else:
      raise TypeConstraintError(nameof(content), str)

class Article(APObject):
  def __init__(self, cntxt, identi, by):
    super().__init__(cntxt, identi)

    if isinstance(content, str):
      self.content = content

    oftype = (str, Link, Group, Application, Organization, Person, Service)
    if isinstance(by, oftype):
      self.attributedTo = by
    elif isinstance(by, list):
      for auth in by:
        if not isinstance(auth, oftype):
          raise TypeConstraintError(nameof(auth), oftype)
      
      self.attributedTo = by
        

class Event(APObject):
  def __init__(self, cntxt, identi, start, end):
    super().__init__(cntxt, identi)

    if isinstance(start, str):
      if match(start, xsd['datetime']) is not None:
        self.startTime = start
      else:
        raise InvalidXSDError(nameof(start))
    elif isinstance(start, dt.datetime):
      self.startTime = start
    else:
      raise TypeConstraintError(nameof(start), (str, dt.datetime))

    if isinstance(end, str):
      if match(end, xsd['datetime']) is not None:
        self.endTime = end
      else:
        raise InvalidXSDError(nameof(end))
    elif isinstance(end, dt.datetime):
      self.endTime = end
    else:
      raise TypeConstraintError(nameof(end), (str, dt.datetime))

class Document(APObject):
  def __init__(self, cntxt, identi, name, url):
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

    if isinstance(url, str):
      if validate.url(url):
        self.url = url
    elif isinstance(url, list):
      for lnk in url:
        if not isinstance(lnk, Link):
          raise TypeConstraintError(nameof(lnk), (Link, str))
        
        if not isinstance(lnk, str):
          raise TypeConstraintError(nameof(lnk), (Link, str))
        else:
          if not validate.url(lnk):
            raise ValueError('Invalid URI link')
          
      self.url = url
    elif isinstance(url, Link):
      self.url = url
    else:
      raise TypeConstraintError(nameof(url), (str, list, Link))

class Page(Document):
  def __init__(self, cntxt, identi, name, url):
    super().__init__(cntxt, identi, name, url)

class Audio(Document):
  def __init__(self, cntxt, identi, name, url):
    super().__init__(cntxt, identi, name, url)

class Image(Document):
  def __init__(self, cntxt, identi, name, url):
    super().__init__(cntxt, identi, name, url)

class Video(Document):
  def __init__(self, cntxt, identi, name, url, dur):
    super().__init__(cntxt, identi, name, url)

    if isinstance(dur, str):
      if match(dur, xsd['duration']) is not None:
        self.duration = dur
      else:
        raise InvalidXSDError(nameof(dur))
    else:
      raise TypeConstraintError(nameof(dur), str)

class Profile(APObject):
  def __init__(self, cntxt, identi, summ, about):
    super().__init__(cntxt, identi)

    if isinstance(summ, str):
      self.summary = summ
    else:
      raise TypeConstraintError(nameof(summ), str)

    oftype = (Link, Group, Application, Organization, Person, Service)
    if isinstance(about, oftype):
      self.describes = about
    else:
      raise TypeConstraintError(nameof(about), oftype)

    self.possible_attrs += [
      'describes'
    ]

class Relationship(APObject):
  def __init__(self, cntxt, identi, rel, subj, obj):
    super().__init__(cntxt, identi)

    oftype = (str, Group, Person, Organization, Application, Service, Link)
    
    if isinstance(subj, oftype):
      self.subject = subj
    else:
      raise TypeConstraintError(nameof(subj), oftype)

    if isinstance(obj, oftype):
      self.object = obj
    else:
      raise TypeConstraintError(nameof(obj), oftype)

    if isinstance(rel, str):
      self.relationship = rel
    else:
      raise TypeConstraintError(nameof(rel), str)

class Place(APObject):
  def __init__(self, cntxt, identi, name, lng, lat, units):
    super().__init__(cntxt, identi)
    
    if isinstance(name, str):
      self.name = name
    elif isinstance(name, dict):
      self.nameMap = {}
      for k in name:
        if not lang.tag_is_valid(k):
          raise ValueError('Invalid language code')
      
      self.nameMap[k] = name[k]
    else:
      raise TypeConstraintError(nameof(name), (str, dict))

    if isinstance(lng, float):
      self.longitude = lng
    else:
      raise TypeConstraintError(nameof(lng), float)

    if isinstance(lat, float):
      self.latitude = lat
    else:
      raise TypeConstraintError(nameof(lat), float)

    if isinstance(units, str):
      self.units = units
    else:
      raise TypeConstraintError(nameof(units), str)

    self.possible_attrs += [
      'longitude', 
      'latitude',
      'units',
      'radius'
    ]

class Mention(Link):
  def __init__(self, name, href, rel, w = None, h = None):
    super().__init__(href, rel, w, h)

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

class Tombstone(APObject):
  def __init__(self, cntxt, identi, former, deltime):
    super().__init__(cntxt, identi)

    if isinstance(former, APObject):
      self.formerType = former
    else:
      raise TypeConstraintError(nameof(former), APObject)

    if isinstance(deltime, str):
      if match(deltime, xsd['datetime']) is not None:
        self.deleted = deltime
      else:
        raise InvalidXSDError(nameof(deltime))
    elif isinstance(deltime, dt.datetime):
      self.deleted = deltime
    else:
      raise TypeConstraintError(nameof(deltime), (str, dt.datetime))

    self.possible_attrs += [
      'formerType',
      'deleted'
    ]