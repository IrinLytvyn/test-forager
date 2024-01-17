"""Storage class for spotify objects."""
from typing import List, Union


class StorageService(object):
    """CRUD operations for spotify objects."""

    def __init__(self) -> None:
        """Initialise local storage."""
        self._storage: dict = {}

    def add_item(self, spotify_item: dict) -> dict:
        """
        Add spotify item to storage.

        :param spotify_item: spotify object
        :return: item that was added to storage
        """
        self._storage[spotify_item.get('id')] = spotify_item
        return spotify_item

    def get_all_items(self) -> List[dict]:
        """
        Get all spotify items.

        :return: list of all spotify items
        """
        return list(self._storage.values())

    def get_item_by_id(self, key: str) -> Union[dict, None]:
        """
        Get spotify item by id.

        :param key: spotify item id
        :return: spotify item if exists
        :raises: KeyError if key doesn't exist
        """
        if key in self._storage:
            return self._storage.get(key)
        raise KeyError("the {0} doesn't exist".format(key))

    def update_item(self, spotify_item: dict, key: str) -> dict:
        """
        Update item by id.

        :param spotify_item: spotify object
        :param key: spotify item id
        :return: updated item if key exists
        :raises: KeyError if key doesn't exist
        """
        old_spotify_item = self._storage.get(key)
        if old_spotify_item is not None:
            self._storage[key] = spotify_item
            return spotify_item
        raise KeyError("the {0} doesn't exist".format(key))

    def delete_by_id(self, key: str) -> None:
        """
        Delete item by id.

        :param key: spotify item id
        :return: None if deleted
        :raises: KeyError if key doesn't exist
        """
        if key in self._storage:
            self._storage.pop(key)
            return
        raise KeyError("the {0} doesn't exist".format(key))
