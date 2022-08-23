import io
import pathlib
import re
import typing
from typing import Final

from .Parser import Channel, Parser

image_file_extensions = {"jpg", "jpeg", "png", "gif"}

raw_info_template = re.compile("[a-zA-Z\_].[\w\-\+]*\=[\"\'].[^\"\']*[\"\']")


class HLSParser(Parser):
    def _parse(self, fp: io.TextIOBase):
        def channel_info_parser(info_list_raw: str) -> dict[str, typing.Any]:
            info_list = raw_info_template.findall(info_list_raw)
            info_dict = dict()
            for info in info_list:
                info_data = info.split("=")
                if len(info_data) != 2:
                    continue
                info_key = info_data[0]
                info_value = info_data[1]
                if info_data[1][0] in {"\"", "\'"} and info_data[1][0] == info_data[1][-1]:
                    info_value = info_data[1][1:-1]
                info_dict[info_key] = info_value
            return info_dict

        SIGNATURE: Final[str] = "#EXTM3U"
        TITLE_LABEL: Final[str] = "#EXTINF:"
        TITLE_OFFSET: Final[int] = len(TITLE_LABEL)
        CATEGORY_LABEL: Final[str] = "#EXTGRP:"
        CATEGORY_OFFSET: Final[int] = len(CATEGORY_LABEL)
        CATEGORY_TITLE_INNER_LABEL: Final[str] = "group-title"
        ICON_IMAGE_URL_LABEL: Final[str] = "tvg-logo"

        title_register = ""
        category_register = ""
        icon_image_register = None
        signature_verified = False
        for line in fp:
            if signature_verified:
                if TITLE_LABEL in line:
                    title_data = line[TITLE_OFFSET:].split(",")
                    title_register = title_data[-1].strip()
                    channel_info_raw = title_data[0].replace("-1", "").strip()
                    channel_info = channel_info_parser(channel_info_raw)
                    if CATEGORY_TITLE_INNER_LABEL in channel_info:
                        category_register = channel_info[CATEGORY_TITLE_INNER_LABEL]
                    if ICON_IMAGE_URL_LABEL in channel_info:
                        icon_image_register = channel_info[ICON_IMAGE_URL_LABEL]
                elif CATEGORY_LABEL in line:
                    category_register = line[CATEGORY_OFFSET:].strip()
                elif line.split("?")[0].split(".")[-1].strip() in image_file_extensions:
                    self._playlist_icon = line.strip()
                else:
                    self._channels.append(Channel(title_register, line.strip(), category_register, icon_image_register))
                    self._categories.add(category_register)
                    icon_image_register = None
            elif SIGNATURE in line:
                signature_verified = True
            else:
                raise ValueError

