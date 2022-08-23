import pathlib

import wx


class AddPlaylistDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title='add new playlist', size=(-1, 256))
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.top_sizer = wx.FlexGridSizer(rows=4, cols=2, gap=wx.Size(0, 0))
        input_title_label = wx.StaticText(self.panel, wx.ID_ANY, label="Title:", style=wx.ALIGN_RIGHT)
        self.title_field = wx.TextCtrl(self.panel, id=wx.ID_ANY, size=(256, -1))
        self.top_sizer.Add(input_title_label, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.top_sizer.Add(self.title_field)
        file_select_label = wx.StaticText(self.panel, wx.ID_ANY, label="File:", style=wx.ALIGN_RIGHT)
        self.file_field = wx.FilePickerCtrl(self.panel, size=(256, -1))
        self.top_sizer.Add(file_select_label, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.top_sizer.Add(self.file_field)
        url_input_label = wx.StaticText(self.panel, wx.ID_ANY, label="URL:", style=wx.ALIGN_RIGHT)
        self.url_field = wx.TextCtrl(self.panel, id=wx.ID_ANY, size=(256, -1))
        self.top_sizer.Add(url_input_label, flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.top_sizer.Add(self.url_field)
        self.ok_button = wx.Button(self.panel, id=wx.ID_OK, label="OK")
        self.ok_button.Bind(wx.EVT_BUTTON, self.button_click_event)
        self.cancel_button = wx.Button(self.panel, id=wx.ID_CANCEL, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.button_click_event)
        self.top_sizer.Add(self.ok_button)
        self.top_sizer.Add(self.cancel_button)
        self.panel.SetSizer(self.top_sizer)

    def button_click_event(self, event):
        if self.IsModal():
            if event.EventObject.Id == wx.ID_OK:
                if bool(self.file_field.GetPath()) or bool(self.url_field.GetValue()):
                    self.EndModal(event.EventObject.Id)
                else:
                    wx.MessageBox("File path OR url field should be not empty")
            else:
                self.EndModal(event.EventObject.Id)
        else:
            self.Close()
    
    def get_values(self) -> tuple[str, pathlib.Path | None, str | None]:
        file_path: [pathlib.Path | None] = self.file_field.GetPath()
        if bool(file_path):
            file_path = pathlib.Path(file_path)
        else:
            file_path = None
        url: str | None = self.url_field.GetLineText(0)
        if not bool(url):
            url = None

        if file_path is None and url is None:
            raise ValueError("File path OR url field should be not empty")

        title: str = self.title_field.GetLineText(0)
        if not bool(title):
            if file_path is not None:
                title = file_path.name
            else:
                title = url.split("?")[0].split("/")[-1]
        return title, file_path, url
