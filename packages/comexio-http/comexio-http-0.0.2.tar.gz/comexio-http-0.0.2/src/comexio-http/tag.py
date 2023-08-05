from .auth import Auth

class Tag:
  """
  Abstract Comexio tag,
  Address is a dictionary that defines the data point in one of the following formats:
    {
      ext: "IO-Server",
      io: "Q1",
    }
    {
      marker: "M1"
    }
    {
      onewire: "OT1"
    }
  """
  def __init__(self,  address: dict, auth: Auth):
    self.auth = auth
    self.address = address

  @property
  def value(self):
    self.raw_data

  async def async_set(self, value):
    """Set the IO value"""
    await self.auth.request(self.address | {"action": "set", "value": value})
    await self.async_update()

  async def async_get(self):
    """Refresh the IO data."""
    self.raw_data = await self.auth.request(self.address | {"action": "get"})
