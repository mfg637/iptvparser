import io
import pathlib
from typing import Final

from .Parser import Channel, Parser

image_file_extensions = {"jpg", "jpeg", "png", "gif"}


class HLSParser(Parser):
    def _parse(self, fp: io.TextIOBase):
        SIGNATURE: Final[str] = "#EXTM3U"
        TITLE_LABEL: Final[str] = "#EXTINF:"
        TITLE_OFFSET: Final[int] = len(TITLE_LABEL)
        CATEGORY_LABEL: Final[str] = "#EXTGRP:"
        CATEGORY_OFFSET: Final[int] = len(CATEGORY_LABEL)

        title_register = ""
        category_register = ""
        signature_verified = False
        for line in fp:
            if signature_verified:
                if TITLE_LABEL in line:
                    title_register = line[TITLE_OFFSET:].split(",")[-1].strip()
                elif CATEGORY_LABEL in line:
                    category_register = line[CATEGORY_OFFSET:].strip()
                elif line.split("?")[0].split(".")[-1].strip() in image_file_extensions:
                    self._playlist_icon = line.strip()
                else:
                    self._channels.append(Channel(title_register, line.strip(), category_register))
                    self._categories.add(category_register)
            elif SIGNATURE in line:
                signature_verified = True
            else:
                raise ValueError

