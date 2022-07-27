import json

allowed_exports = {
  '^[Jj][Aa]?[Ss][Oo][Nn]$': {
    'dump': json.dumps,
    'load': json.loads
  }
}