import abc
import io
import pathlib
import logging
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Channel:
    title: str
    playlist: str
    category: str
    icon_url: str | None = None


class Parser(abc.ABC):
    def __init__(self):
        self._channels: list[Channel] = []
        self._categories: set[str] = set()
        self._playlist_icon = None

        self._title: str | None = None
        self._origin: str | None = None
        self._is_file: bool | None = None

    @abc.abstractmethod
    def _parse(self, fp: io.TextIOBase):
        pass

    def parse_file(self, file: [pathlib.Path, io.TextIOBase]):

        if isinstance(file, pathlib.Path):
            with file.open("r") as f:
                self._parse(f)
        elif isinstance(file, io.TextIOBase):
            self._parse(file)
        else:
            raise ValueError(file, type(file))

    def parse_url(self, url):
        http_request = requests.get(url)
        if http_request.status_code == requests.codes.ok:
            with io.StringIO(http_request.text) as f:
                self._parse(f)
        else:
            raise BlockingIOError("HTTP ERROR CODE {} RECEIVED".format(http_request.status_code))

    def get_categories(self) -> set[str]:
        return self._categories

    def get_all_channels(self) -> list[Channel]:
        return self._channels

    def get_channels_by_category(self, category: str) -> list[Channel]:
        result: list[Channel] = []
        for channel in self._channels:
            if channel.category == category:
                result.append(channel)
        return result

    def get_playlist_icon(self) -> [None, str]:
        return self._playlist_icon

    def get_serializable_data(self) -> dict[str, str | bool]:
        return {
            "title": self.title,
            "origin": self.origin,
            "is_file": self.is_file
        }

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, _title):
        logger.debug("Property title set value {}".format(_title))
        self._title = _title

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, _origin):
        logger.debug("Property origin set value {}".format(_origin))
        self._origin = _origin

    @property
    def is_file(self):
        return self._is_file

    @is_file.setter
    def is_file(self, _is_file):
        logger.debug("Property is_file set value {}".format(_is_file))
        self._is_file = _is_file
