"""Client for spotify API."""
import base64
from typing import Union

import requests
from requests.models import Response

GOOD_STATUS_CODE: int = 200
DEFAULT_TIMEOUT: int = 30


class NoAccessTokenError(Exception):
    """Access token is not received exception."""


class SpotifyClient(object):
    """Class that communicates with spotify API."""

    spotify_url: str = 'https://api.spotify.com/v1'

    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        Initialise access token.

        :param client_id: client id provided by spotify
        :param client_secret: client secret provided by spotify
        """
        self.access_token: str = self.retrieve_access_token(client_id, client_secret)

    @classmethod
    def retrieve_access_token(cls, client_id: str, client_secret: str) -> str:
        """
        Get access token from spotify.

        :param client_id: client id provided by spotify
        :param client_secret: client secret provided by spotify
        :return: access token from spotify API
        :raises: Exception if can not get access token
        """
        encoded: bytes = base64.b64encode('{0}:{1}'.format(client_id, client_secret).encode())
        response: Response = requests.post(
            'https://accounts.spotify.com/api/token',
            data={'grant_type': 'client_credentials'},
            headers={'Authorization': 'Basic {0}'.format(encoded.decode())},
            timeout=DEFAULT_TIMEOUT,
        )
        if response.status_code == GOOD_STATUS_CODE:
            return response.json()['access_token']
        raise NoAccessTokenError('Can not get access token')

    def get_item(self, endpoint: str) -> Union[dict, str]:
        """
        Get item data from spotify by id.

        :param endpoint: spotify API path to get item's information. Example: tracks/11dFghVXANMlKmJXsNCbNl
        :return: response json from spotify. If request failed return string with response.status_code
        """
        response: Response = requests.get(
            '{0}/{1}'.format(self.spotify_url, endpoint),
            headers={'Authorization': 'Bearer {0}'.format(self.access_token)},
            timeout=DEFAULT_TIMEOUT,
        )

        if response.status_code == GOOD_STATUS_CODE:
            return response.json()
        return 'Error {0}'.format(response.status_code)

    def get_track(self, track_id: str) -> Union[dict, str]:
        """
        Get track data from spotify by id.

        :param track_id: track id in spotify
        :return: dict with track data
        """
        return self.get_item('tracks/{0}'.format(track_id))

    def get_artist(self, artist_id: str) -> Union[dict, str]:
        """
        Get artist data from spotify by id.

        :param artist_id: artist id in spotify
        :return: dict with artist data
        """
        return self.get_item('artists/{0}'.format(artist_id))

    def get_album(self, album_id: str) -> Union[dict, str]:
        """
        Get album data from spotify by id.

        :param album_id: album id in spotify
        :return: dict with album data
        """
        return self.get_item('albums/{0}'.format(album_id))
