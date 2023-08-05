from aiohttp import ClientSession, ClientResponse
import base64


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, session: ClientSession, host: str, user_name: str, password: str):
        """Initialize the auth."""
        self.session = session
        self.host = host
        self.user_name = user_name
        self.password = password

    async def request(self, params: dict, **kwargs) -> ClientResponse:
      """Get or set a data point"""
      headers = kwargs.get("headers")

      if headers is None:
          headers = {}
      else:
          headers = dict(headers)

      headers["authorization"] = f"Basic {self.encoded_login}"

      resp = await self.session.request(
          "get", f"http://{self.host}/api", **kwargs, params=params, headers=headers,
      )

      resp.raise_for_status()
      return await resp.text()

    def encoded_login(self):
      login = f"{self.user_name}:{self.password}"
      return base64.b64encode(login.encode("utf-8")).decode("ascii")
