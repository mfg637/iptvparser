import abc
import io
import pathlib
import typing
import requests
from dataclasses import dataclass


@dataclass(frozen=True)
class Channel:
    title: str
    playlist: typing.Any
    category: str


class Parser(abc.ABC):
    def __init__(self):
        self._channels: list[Channel] = []
        self._categories: set[str] = set()
        self._playlist_icon = None

        self.title: str | None = None
        self.origin: str | None = None
        self.is_file: bool | None = None

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
