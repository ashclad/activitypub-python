# external modules
from validators import url as validate
import datetime as dt
from re import search as match

# internal modules
from generic import APObject, Activity, IntransitiveActivity, Collection, Profile
from actors import *

actors_coll = (Group, Organization, Application, Service, Person)

class Accept(Activity):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if target is not None:
      oftype = (Collection, Profile, *actors_coll)
      if isinstance(target, oftype):
        self.target = target
      elif isinstance(target, str):
        if validate.url(target):
          self.target = target
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(target, list):
        for t in target:
          if not isinstance(t, (*oftype, str)):
            raise TypeConstraintError(nameof(t), (*oftype, str))

          self.target = target
      else:
        raise TypeConstraintError(nameof(target), (str, list, *oftype))

class TentativeAccept(Accept):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, target, result)

class Add(Activity):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if target is not None:
      oftype = (Collection, Profile, *actors_coll)
      if isinstance(target, oftype):
        self.target = target
      elif isinstance(target, str):
        if validate.url(target):
          self.target = target
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(target, list):
        for t in target:
          if not isinstance(t, (*oftype, str)):
            raise TypeConstraintError(nameof(t), (*oftype, str))

          self.target = target
      else:
        raise TypeConstraintError(nameof(target), (str, list, *oftype))

class Create(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Delete(Activity):
  def __init__(self, cntxt, identi, actr, obj, origin = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if origin is not None:
      oftype = (Collection, Profile, *actors_coll)
      if isinstance(origin, oftype):
        self.origin = origin
      elif isinstance(origin, str):
        if validate.url(origin):
          self.origin = origin
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(origin, list):
        for o in origin:
          if not isinstance(o, (*oftype, str)):
            raise TypeConstraintError(nameof(o), (*oftype, str))

        self.target = target
      else:
        raise TypeConstraintError(nameof(origin), (str, list, *oftype))

class Follow(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Ignore(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Block(Ignore):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Join(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Leave(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Like(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Dislike(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Offer(Activity):
  def __init__(self, cntxt, identi, actr, obj, target, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    oftype = (Collection, Profile, *actors_coll)
    if isinstance(target, oftype):
      self.target = target
    elif isinstance(target, str):
      if validate.url(target):
        self.target = target
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(target, list):
      for t in target:
        if not isinstance(t, (*oftype, str)):
          raise TypeConstraintError(nameof(t), (*oftype, str))

        self.target = target
    else:
      raise TypeConstraintError(nameof(target), (str, list, *oftype))

class Invite(Offer):
  def __init__(self, cntxt, identi, actr, obj, target, result = None):
    super().__init__(cntxt, identi, actr, obj, target, result)

class Reject(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class TentativeReject(Reject):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Remove(Activity):
  def __init__(self, cntxt, identi, actr, obj, origin = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if origin is not None:
      oftype = (Collection, Profile, *actors_coll)
      if isinstance(origin, oftype):
        self.origin = origin
      elif isinstance(origin, str):
        if validate.url(origin):
          self.origin = origin
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(origin, list):
        for o in origin:
          if not isinstance(o, (*oftype, str)):
            raise TypeConstraintError(nameof(o), (*oftype, str))

        self.target = target
      else:
        raise TypeConstraintError(nameof(origin), (str, list, *oftype))

class Undo(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Update(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class View(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Read(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Listen(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Move(Activity):
  def __init__(self, cntxt, identi, actr, obj, origin, target, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    oftype = (Collection, Profile, *actors_coll)
    if isinstance(origin, oftype):
      self.origin = origin
    elif isinstance(origin, str):
      if validate.url(origin):
        self.origin = origin
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(origin, list):
      for o in origin:
        if not isinstance(o, (*oftype, str)):
          raise TypeConstraintError(nameof(o), (*oftype, str))

      self.target = target
    else:
      raise TypeConstraintError(nameof(origin), (str, list, *oftype))

    if isinstance(target, oftype):
      self.target = target
    elif isinstance(target, str):
      if validate.url(target):
        self.target = target
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(target, list):
      for t in target:
        if not isinstance(t, (*oftype, str)):
          raise TypeConstraintError(nameof(t), (*oftype, str))

        self.target = target
    else:
      raise TypeConstraintError(nameof(target), (str, list, *oftype))

class Announce(Activity):
  def __init__(self, cntxt, identi, actr, obj, target, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    oftype = (Collection, Profile, *actors_coll)
    if isinstance(target, oftype):
      self.target = target
    elif isinstance(target, str):
      if validate.url(target):
        self.target = target
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(target, list):
      for t in target:
        if not isinstance(t, (*oftype, str)):
          raise TypeConstraintError(nameof(t), (*oftype, str))

        self.target = target
    else:
      raise TypeConstraintError(nameof(target), (str, list, *oftype))

class Flag(Activity):
  def __init__(self, cntxt, identi, actr, target, result = None, obj = None):
    super().__init__(cntxt, identi, actr, target, result, obj)

class Arrive(IntransitiveActivity):
  def __init__(self, cntxt, identi, actr, target = None, result = None, obj = None):
    super().__init__(cntxt, identi, actr, target, result, obj)

class Travel(IntransitiveActivity):
  def __init__(self, cntxt, identi, actr, target = None, origin = None, result = None, obj = None):
    super().__init__(cntxt, identi, actr, target, result, obj)

    if origin is not None:
      oftype = (Collection, Profile, *actors_coll)
      if isinstance(origin, oftype):
        self.origin = origin
      elif isinstance(origin, str):
        if validate.url(origin):
          self.origin = origin
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(origin, list):
        for o in origin:
          if not isinstance(o, (*oftype, str)):
            raise TypeConstraintError(nameof(o), (*oftype, str))

        self.target = target
      else:
        raise TypeConstraintError(nameof(origin), (str, list, *oftype))    

class Question(IntransitiveActivity):
  def __init__(self, cntxt, identi, actr, name, opts = None, mode = 0, target = None, origin = None, result = None, obj = None):
    super().__init__(cntxt, identi, actr, target, result, obj)

    if isinstance(name, str):
      self.name = name

    if opts is not None:
      if isinstance(opts, list):
        for o in opts:
          if not isinstance(o, (APObject, str)):
            raise TypeConstraintError(nameof(o), (APObject, str))

        if mode == 0:
          self.anyOf = opts
        elif mode == 1:
          self.oneOf = opts
        else:
          raise ValueError('Integer above acceptable integer range')
      else:
        raise TypeConstraintError(nameof(opts), list)
    else:
      self.closed = dt.datetime.now()

  def close(self, dtstr = None):
    if dtstr is None:
      self.closed = dt.datetime.now()
    else:
      if match(dtstr, xsd['datetime']) is not None:
        self.closed = dtstr
      else:
        raise InvalidXSDError(nameof(dtstr))