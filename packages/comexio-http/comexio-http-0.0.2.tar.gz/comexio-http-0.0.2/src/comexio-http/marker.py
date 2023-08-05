from .tag import Tag
from .auth import Auth

class Marker(Tag):
  "Marker value"
  def __init__(self, address: str, auth: Auth):
    Tag.__init__(self, {"marker": address}, auth)