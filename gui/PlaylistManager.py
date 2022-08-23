import pathlib

import wx
import json

import parser
from .add_playlist_dialog import AddPlaylistDialog
from .PlaylistView import PlaylistViewer


class PlaylistManager(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Playlist manager', size=(256, 256+32))

        self._playlists: list[parser.Parser] = []
        self.load_playlists()

        self.top_panel = wx.Panel(self, wx.ID_ANY)
        self.playlist_element = wx.ListBox(self.top_panel, size=(256, 256))
        self.playlist_element.Bind(wx.EVT_LISTBOX_DCLICK, self.open_playlist_event)
        self.buttons_pannel = wx.Panel(self.top_panel, wx.ID_ANY)
        self.add_playlist_button = wx.Button(self.buttons_pannel, wx.ID_ANY, label="Add playlist…")
        self.add_playlist_button.Bind(wx.EVT_BUTTON, self.add_playlist_event)
        self.delete_playlist = wx.Button(self.buttons_pannel, wx.ID_ANY, label="Delete playlist")
        self.delete_playlist.Bind(wx.EVT_BUTTON, self.delete_playlist_event)
        self.top_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_sizer.Add(self.playlist_element)
        self.buttons_sizer.Add(self.add_playlist_button)
        self.buttons_sizer.Add(self.delete_playlist)
        self.buttons_pannel.SetSizer(self.buttons_sizer)
        self.top_sizer.Add(self.buttons_pannel)
        self.top_panel.SetSizer(self.top_sizer)
        self._update_playlist_control()

    def _serialise(self):
        with open("playlists.json", "w") as f:
            prepared_data = []
            for playlist in self._playlists:
                prepared_data.append(playlist.get_serializable_data())
            json.dump(prepared_data, f)

    def load_playlists(self):
        try:
            with open("playlists.json", "r") as f:
                playlists_data = json.load(f)
                for pl_data in playlists_data:
                    _parser = parser.hls_parser.HLSParser()
                    _parser.title = pl_data["title"]
                    if pl_data["is_file"]:
                        _parser.parse_file(pathlib.Path(pl_data["origin"]))
                    else:
                        _parser.parse_url(pl_data["origin"])
                    self._playlists.append(_parser)
        except FileNotFoundError:
            pass

    def _update_playlist_control(self):
        self.playlist_element.Clear()
        for playlist in self._playlists:
            self.playlist_element.Append(playlist.title)

    def delete_playlist_event(self, event):
        playlist_id = self.playlist_element.GetSelection()
        self._playlists.pop(playlist_id)
        self._serialise()
        self._update_playlist_control()

    def add_playlist_event(self, event):
        dialog = AddPlaylistDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            title, file_path, url = dialog.get_values()
            _parser = parser.hls_parser.HLSParser()
            _parser.title = title
            if file_path is not None:
                _parser.origin = str(file_path)
                _parser.is_file = True
                _parser.parse_file(file_path)
            elif url is not None:
                _parser.origin = url
                _parser.is_file = False
                _parser.parse_url(url)
            else:
                raise ValueError("No playlist address provided")
            self._playlists.append(_parser)
            self._serialise()
            self._update_playlist_control()

    def open_playlist_event(self, event):
        playlist_id = self.playlist_element.GetSelection()
        pl_viewer = PlaylistViewer(self._playlists[playlist_id], self)
        pl_viewer.Show()
