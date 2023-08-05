from .tag import Tag
from .auth import Auth

class Onewire(Tag):
  "Onewire value"
  def __init__(self, address: str, auth: Auth):
    Tag.__init__(self, {"onewire": address}, auth)