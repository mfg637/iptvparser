import pathlib

import parser
import wx
import gui


def main():
    #my_parser: parser.Parser = parser.HLSParser.HLSParser()
    #my_parser.parse_file(pathlib.Path("/home/mfg637/Загрузки/freeiptv.m3u"))
    app = wx.App()
    frame = gui.PlaylistManager.PlaylistManager().Show()
    app.MainLoop()
    #
    # my_parser.parse_url("https://smarttvnews.ru/apps/freeiptv.m3u")
    # print(my_parser.get_categories())
    # print(my_parser.get_channels_by_category('Познавательные'))
    # print(my_parser.get_playlist_icon())


if __name__ == '__main__':
    main()

