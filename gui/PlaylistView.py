import wx
import parser
import subprocess


class PlaylistViewer(wx.Frame):
    def __init__(self, _parser: parser.Parser, parent):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title='{} playlist'.format(_parser.title), size=(256*3, 256))
        self._current_channels: list[parser.Channel] = []
        self._parser = _parser
        self.panel = wx.Panel(self, wx.ID_ANY)
        categories = ["*"]
        categories.extend(_parser.get_categories())
        self._category_list = wx.ListBox(self.panel, size=(256, -1), choices=categories)
        self._channels_list = wx.ListBox(self.panel, size=(512, -1))
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self._category_list, 1, wx.EXPAND | wx.ALL)
        self._category_list.Bind(wx.EVT_LISTBOX_DCLICK, self._select_category_event)
        self.sizer.Add(self._channels_list, 1, wx.EXPAND | wx.ALL)
        self._channels_list.Bind(wx.EVT_LISTBOX_DCLICK, self._play_channel)
        self.panel.SetSizer(self.sizer)

    def _select_category_event(self, event):
        category = self._category_list.GetString(self._category_list.GetSelection())
        if category == "*":
            self._current_channels = self._parser.get_all_channels()
        else:
            self._current_channels = self._parser.get_channels_by_category(category)
        self._channels_list.Clear()
        channel_titles = []
        for channel in self._current_channels:
            channel_titles.append(channel.title)
        self._channels_list.InsertItems(channel_titles, 0)

    def _play_channel(self, event):
        selected_channel: parser.Channel = self._current_channels[self._channels_list.GetSelection()]
        commandline = ["vlc", str(selected_channel.playlist)]
        mpv_process = subprocess.Popen(commandline)
