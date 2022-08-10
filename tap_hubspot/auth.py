import datetime
from typing import Optional

from singer_sdk import Stream
from singer_sdk.authenticators import OAuthAuthenticator


class HubspotOAuthAuthenticator(OAuthAuthenticator):
    def __init__(
        self,
        stream: Stream,
        auth_endpoint: Optional[str] = None,
        oauth_scopes: Optional[str] = None,
        default_expiration: Optional[int] = None,
    ) -> None:
        """Create a new authenticator.

        Args:
            stream: The stream instance to use with this authenticator.
            auth_endpoint: API username.
            oauth_scopes: API password.
            default_expiration: Default token expiry in seconds.
        """
        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._default_expiration = default_expiration
        self._oauth_scopes = oauth_scopes

        # Initialize internal tracking attributes
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = self.config["refresh_token"]
        self.last_refreshed: Optional[datetime] = None
        self.expires_in: Optional[int] = None

    @property
    def oauth_request_body(self) -> dict:
        return {
            "grant_type": "refresh_token",
            "redirect_uri": "https://www.example.com",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
