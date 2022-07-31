# external modules
from validators import url as validate
from re import search as match

# internal modules
from generic import APObject, Link

class Note(APObject):
  def __init__(self, cntxt, identi, content):
    super().__init__(cntxt, identi)

    if isinstance(content, str):
      self.content = content

class Article(APObject):
  def __init__(self, cntxt, identi, by):
    super().__init__(cntxt, identi)

    if isinstance(content, str):
      self.content = content

    if isinstance(by, str):
      self.attributedTo = by

class Event(APObject):
  def __init__(self, cntxt, identi, start, end):
    super().__init__(cntxt, identi)

    if isinstance(content, str):
      # TODO: add regex pattern check for xsd:dateTime format
      self.startTime = start

    if isinstance(content, str):
      # TODO: add regex pattern check for xsd:dateTime format
      self.endTime = end

class Document(APObject):
  def __init__(self, cntxt, identi, name, url):
    super().__init__(cntxt, identi)

    if isinstance(name, str):
      self.name = name

    if isinstance(url, str):
      if validate.url(url):
        self.url = url
    elif isinstance(url, list):
      for lnk in url:
        if isinstance(lnk, Link):
          self.url = url
          break
    elif isinstance(url, Link):
      self.url = url

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
      xsddurstr = '^P([0-9]+Y)?([0-9]+M)?([0-9]+D)?(T([0-9]+H)?([0-9]+M)?([0-9]+S)?)?$'
      if match(dur, xsddurstr) is not None:
        self.duration = dur

class Profile(APObject):
  def __init__(self, cntxt, identi, summ, about):
    super().__init__(cntxt, identi)

    if isinstance(summ, str):
      self.summary = summ

    if isinstance(about, APObject):
      self.describes = about

    self.possible_attrs += [
      'describes'
    ]

class Relationship(APObject):
  def __init__(self, cntxt, identi, rel, subj, obj):
    super().__init__(cntxt, identi)

    if isinstance(subj, (str, Link, APObject)):
      self.subject = subj

    if isinstance(obj, (str, Link, APObject)):
      self.object = obj

    if isinstance(rel, str):
      self.relationship = rel

# TODO: Place and Tombstone APObject child classes
# TODO: Mention Link child class