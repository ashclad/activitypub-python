# external modules
from re import search as match
from validators import url, uuid
import json
import yaml as yml
from collections.abc import Iterable
from cerberus import Validator

# internal modules
from validap import *

allowed_exports = {
  '^[Jj][Aa]?[Ss][Oo][Nn]$': {
    'dump': json.dumps,
    'load': json.loads
  },
  '^[Yy][Aa]?[Mm][Ll]$': {
    'dump': yml.dump,
    'load': yml.load
  }
}

def allowMarkup(mkupname, dumper, loader):
  if isinstance(mkupname, str) and callable(dumper) and callable(loader):
    allowed_exports[name] = {
      'dump': dumper,
      'load': loader
    }

    return allowed_exports
  else:
    raise TypeError('At least one argument is of invalid type')

# TODO: Use `schema` package to validate configuration 
# dictionary structures
class ConfMan:
  def __init__(self):
    self.config = {}
    self.mode = 's'

    def is_url(field, value, error):
      if not url(value):
        error(field, 'Value must be a URI')

    def is_uuid(field, value, error):
      if not uuid(value):
        error(field, 'Value must be a UUID')

    schema = {
      'APPS': {
        'type': 'list',
        'schema': {
          'type': 'dict',
          'schema': {
            'NAME': {
              'type': 'string'
            },
            'ID': {
              'type': 'string',
              'check_with': is_uuid
            },
            'SECRET': {
              'type': 'string',
              'regex': '^[0-9AaBbCcDdEeFf]+$'
            },
            'RED_URI': {
              'type': 'string',
              'check_with': is_url
            }
          }
        }
      },
      'OAUTH': {
        'type': 'dict',
        'schema': {
          'AUTH_URI': {
            'type': 'string',
            'check_with': is_url
          },
          'TOKE_URI': {
            'type': 'string',
            'check_with': is_url
          }
        }
      }
    }

    self.validator = Validator(schema, require_all = False)

  def set_mode(self, access = 's'):
    access_list = [
      'm',
      's'
    ]

    if access in access_list:
      self.mode = access
    else:
      raise Exception()

  def __len__(self):
    if self.mode == 's':
      with open('config.yaml', 'r') as conffile:
        confcontents = conffile.read()
        conf = yml.load(confcontents, yml.CLoader)

      return len(conf)
    elif self.mode == 'm':
      return len(self.config)

  def __setitem__(self, k, v):
    if isinstance(k, (str, int)):
      if self.validator.validate({k: v}):
        self.config[k] = v
      else:
        raise Exception()

      return self.config
    else:
      raise Exception()

  def __getitem__(self, k):
    if isinstance(k, (str, int)):
      if self.mode == 'm':
        if k in self.config:
          return self.config[k]
        else:
          raise Exception()
      elif self.mode == 's':
        with open('config.yaml', 'r') as conffile:
          confcontents = conffile.read()
          conf = yml.load(confcontents, yml.CLoader)

        if conf is not None:
          return conf
        else:
          raise Exception()
    else:
      raise Exception()

  def __delitem__(self, k):
    if isinstance(k, (str, int)):
      if k in self.config:
        del self.config[k]
      else:
        raise Exception()
    else:
      raise Exception()

  def __iter__(self):
    if self.mode == 's':
      with open('config.yaml', 'r') as conffile:
        confcontents = conffile.read()
        conf = yml.load(confcontents, yml.CLoader)

      return iter(conf)
    elif self.mode == 'm':
      return iter(self.config)

  def synchronized(self):
    with open('config.yaml', 'r+') as conffile:
      conf = yml.load(confcontents, yml.CLoader)
      confkeys = zip(self.config.keys(), conf.keys())
      confvals = zip(self.config.values(), conf.values())
      key_state = list(filter(lambda x: True if x[0] != x[1] else False, confkeys))
      val_state = list(filter(lambda x: True if x[0] != x[1] else False, confvals))

      if len(key_state) > 0 or len(val_state) > 0:
        return False
      else:
        return True

  def revert(self, favor = None):
    if favor is None:
      favor = self.mode
    else:
      if not isinstance(favor, str):
        raise Exception()
    
    access_list = [
      's',
      'm'
    ]

    if favor in access_list:
      if favor == 's':
        with open('config.yaml', 'r') as conffile:
          confcontents = conffile.read()
          conf = yml.load(confcontents, yml.CLoader)

        self.config = conf
      elif favor == 'm':
        with open('config.yaml', 'w') as conffile:
          if self.validator.validate(self.config):
            conf = yml.dump(self.config, yml.CDumper)
          else:
            raise Exception()

          conffile.write(conf)
      else:
        raise Exception()
    else:
      raise Exception()

  def commit(self):
    if self.validator.validate(self.config):
      with open('config.yaml', 'w') as conffile:
        conf = yml.dump(self.config, yml.CDumper)
        conffile.write(conf)
    else:
      raise Exception()

  # def __reversed__(self):
  #   raise NotImplementedError()

  # def __contains__(self, item):
  #   raise NotImplementedError()

  # def __missing__(self, k):
  #   raise NotImplementedError()