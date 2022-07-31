# external modules
from validators import url as validate

# internal modules
from generic import Activity, IntransitiveActivity
from actors import *

class Accept(Activity):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if target is not None:
      oftype = (Person, Group, Organization, Service)
      if isinstance(target, oftype):
        self.target = target
      elif isinstance(target, str):
        if validate.url(target):
          self.target = target
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(target, list):
        for t in target:
          if not isinstance(t, (oftype, str)):
            raise TypeConstraintError(nameof(t), (*oftype, str))

          self.target = target
      else:
        raise TypeConstraintError(nameof(target), (str, list, *oftype))

class TentativeAccept(Accept):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, target, result)

class Add(Activity):
  pass

class Create(Activity):
  pass

class Delete(Activity):
  pass

class Follow(Activity):
  pass

class Ignore(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Block(Ignore):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Join(Activity):
  pass

class Leave(Activity):
  pass

class Like(Activity):
  pass

class Dislike(Activity):
  pass

class Offer(Activity):
  def __init__(self, cntxt, identi, actr, obj, target, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    oftype = (Person, Group, Organization, Service)
    if isinstance(target, oftype):
      self.target = target
    elif isinstance(target, str):
      if validate.url(target):
        self.target = target
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(target, list):
      for t in target:
        if not isinstance(t, (oftype, str)):
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
  pass

class Undo(Activity):
  pass

class Update(Activity):
  pass

class View(Activity):
  pass

class Read(Activity):
  pass

class Listen(Activity):
  pass

class Move(Activity):
  pass

class Announce(Activity):
  pass

class Flag(Activity):
  pass

class Arrive(IntransitiveActivity):
  pass

class Travel(IntransitiveActivity):
  pass

class Question(IntransitiveActivity):
  pass