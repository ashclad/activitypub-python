from validators import url as urlvalidate

def createValidator(vfunc):
  def subfunc(*args):
    if len(args) > 3 or len(args) == 0:
      raise TypeError()

    if len(args) == 2:
      raise TypeError()

    if len(args) == 1:
      return vfunc(args[0])

    if len(args) == 3:
      if vfunc(args[0]):
        if callable(args[1]):
          return args[1]()
        else:
          return args[1]
      else:
        if callable(args[2]):
          return args[2]()
        else:
          return args[2]

  return subfunc