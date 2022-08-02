# external modules
from validators import url as validate

# internal modules
from generic import Activity, IntransitiveActivity, Collection
# from actors import *

class Accept(Activity):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if target is not None:
      if isinstance(target, Collection):
        self.target = target
      elif isinstance(target, str):
        if validate.url(target):
          self.target = target
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(target, list):
        for t in target:
          if not isinstance(t, (Collection, str)):
            raise TypeConstraintError(nameof(t), (Collection, str))

          self.target = target
      else:
        raise TypeConstraintError(nameof(target), (str, list, Collection))

class TentativeAccept(Accept):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, target, result)

class Add(Activity):
  def __init__(self, contxt, identi, actr, obj, target = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if target is not None:
      if isinstance(target, Collection):
        self.target = target
      elif isinstance(target, str):
        if validate.url(target):
          self.target = target
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(target, list):
        for t in target:
          if not isinstance(t, (Collection, str)):
            raise TypeConstraintError(nameof(t), (Collection, str))

          self.target = target
      else:
        raise TypeConstraintError(nameof(target), (str, list, Collection))

class Create(Activity):
  def __init__(self, cntxt, identi, actr, obj, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

class Delete(Activity):
  def __init__(self, cntxt, identi, actr, obj, origin = None, result = None):
    super().__init__(cntxt, identi, actr, obj, result)

    if origin is not None:
      if isinstance(origin, Collection):
        self.origin = origin
      elif isinstance(origin, str):
        if validate.url(origin):
          self.origin = origin
        else:
          raise ValueError('Invalid URI link')
      elif isinstance(origin, list):
        for o in origin:
          if not isinstance(o, (Collection, str)):
            raise TypeConstraintError(nameof(o), (Collection, str))

        self.target = target
      else:
        raise TypeConstraintError(nameof(origin), (str, list, Collection))

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

    if isinstance(target, Collection):
      self.target = target
    elif isinstance(target, str):
      if validate.url(target):
        self.target = target
      else:
        raise ValueError('Invalid URI link')
    elif isinstance(target, list):
      for t in target:
        if not isinstance(t, (Collection, str)):
          raise TypeConstraintError(nameof(t), (Collection, str))

        self.target = target
    else:
      raise TypeConstraintError(nameof(target), (str, list, Collection))

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