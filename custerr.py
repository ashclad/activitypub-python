class TypeConstraintError(TypeError):
  def __init__(self, var_entered, type_required):
    if isinstance(type_required, tuple):
      new_str = ''
      last = type_required[-1]
      type_required_mod = type_required[0:len(type_required)-1]
      
      for t in tuple:
        new_str += t.__name__ + ', '

      new_str += 'or ' + last.__name__
    else:
      type_required = type_required.__name__

    self.message = str(var_entered) + ' is constrained to type ' + type_required
    super().__init__(message)

class UnallowableAttributeError(ValueError):
  def __init__(self, val):
    self.message = '"' + val + '" is not an allowed attribute'
    super().__init__(message)

class UnmutableAttributeError(AttributeError):
  def __init__(self, msg = 'New attribute cannot be created'):
    self.message = msg
    super().__init__(message)

class IllegalMethodError(NotImplementedError):
  def __init__(self, msg = 'This method call is illegal'):
    self.message = msg