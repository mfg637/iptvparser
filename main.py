import wx
import gui
import logging

logging.basicConfig(level=logging.INFO)


def main():
    app = wx.App()
    gui.PlaylistManager.PlaylistManager().Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

