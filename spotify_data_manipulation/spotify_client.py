"""Client for spotify API."""
import base64
from typing import Callable, Union

import requests
from requests.models import Response

DEFAULT_TIMEOUT: int = 30


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
        self.tracks: Track = Track(self)
        self.albums: Album = Album(self)
        self.artists: Artist = Artist(self)

    @classmethod
    def send_request(
        cls,
        method: str,
        timeout: int = DEFAULT_TIMEOUT,
        *args,
        **kwargs,
    ) -> dict:
        """
        Send requests. Base method.

        :param method: HTTP method
        :param timeout: request timeout
        :param args: request args
        :param kwargs: request kwargs
        :return: response json
        :raises: HTTPError if request failed
        """
        method_func: Callable = getattr(requests, method.lower(), None)
        if method_func is None:
            raise ValueError('method {0} does not exist'.format(method))
        response: Response = method_func(
            *args,
            timeout=timeout,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

    def retrieve_access_token(self, client_id: str, client_secret: str) -> str:
        """
        Get access token from spotify.

        :param client_id: client id provided by spotify
        :param client_secret: client secret provided by spotify
        :return: access token from spotify API
        :raises: Exception if can not get access token
        """
        encoded: bytes = base64.b64encode('{0}:{1}'.format(client_id, client_secret).encode())
        response = self.send_request(
            method='post',
            url='https://accounts.spotify.com/api/token',
            headers={'Authorization': 'Basic {0}'.format(encoded.decode())},
            data={'grant_type': 'client_credentials'},
        )
        return response['access_token']

    def get_item(self, endpoint: str) -> Union[dict, str]:
        """
        Get item data from spotify by id.

        :param endpoint: spotify API path to get item's information. Example: tracks/11dFghVXANMlKmJXsNCbNl
        :return: response json from spotify. If request failed return string with response.status_code
        """
        return self.send_request(
            method='get',
            url='{0}/{1}'.format(self.spotify_url, endpoint),
            headers={'Authorization': 'Bearer {0}'.format(self.access_token)},
        )


class Track(object):
    """Class for spotify API track data."""

    def __init__(self, spotify_client: SpotifyClient) -> None:
        """
        Initialise spotify_client.

        :param spotify_client: SpotifyClient instance
        """
        self.spotify_client: SpotifyClient = spotify_client

    def get_track(self, track_id: str) -> Union[dict, str]:
        """
        Get track data from spotify by id.

        :param track_id: track id in spotify
        :return: dict with track data
        """
        return self.spotify_client.get_item('tracks/{0}'.format(track_id))


class Artist(object):
    """Class for spotify API artist data."""

    def __init__(self, spotify_client: SpotifyClient) -> None:
        """
        Initialise spotify_client.

        :param spotify_client: SpotifyClient instance
        """
        self.spotify_client: SpotifyClient = spotify_client

    def get_artist(self, artist_id: str) -> Union[dict, str]:
        """
        Get artist data from spotify by id.

        :param artist_id: artist id in spotify
        :return: dict with artist data
        """
        return self.spotify_client.get_item('artists/{0}'.format(artist_id))


class Album(object):
    """Class for spotify API album data."""

    def __init__(self, spotify_client: SpotifyClient) -> None:
        """
        Initialise spotify_client.

        :param spotify_client: SpotifyClient instance
        """
        self.spotify_client: SpotifyClient = spotify_client

    def get_album(self, album_id: str) -> Union[dict, str]:
        """
        Get album data from spotify by id.

        :param album_id: album id in spotify
        :return: dict with album data
        """
        return self.spotify_client.get_item('albums/{0}'.format(album_id))
