from .tag import Tag
from .auth import Auth

class IO(Tag):
  "Direct IO value"
  def __init__(self, ext: str, io: str, auth: Auth):
    Tag.__init__(self, {"ext": ext, "io": io}, auth)