import os
from tkinter import Tk, messagebox, Frame, Button, Checkbutton, OptionMenu, Label, Message, Entry, \
    StringVar, IntVar, BooleanVar, BOTH, LEFT, NW, N, E, S, W, X, Menu
from PIL import Image, ImageTk

from enum import IntEnum
import random
import io
import json
import webbrowser

from dustmaker import MapReader, BitReader, MapParseException, LevelType

from CustomFileManager import loadmaps
from CustomFileManager.publishedsort import Published
from CustomFileManager.random_level_select import\
    Result, dustkid_link, atlas_link, launch, get_level_candidates, process_command

config_file = './_config.json'
_default_level_dir = "C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/levels"
_default_index = './_level_index.json'
_img_size = (382, 182)
_option_columns = 4
_blank_info = {'filename': None}
_blank_image = Image.new('RGB', _img_size, 0xAAAAAA)
_blank_text = '''filename:
readable:
level_type:
published:
has_end:
apples:
rank:
apple_rank:
hit_apples:
'''
_stats_text = '''Total levels\t: %d
Visible levels\t: %d
SSable levels\t: %d

Apple levels\t: %d
Apple SSable\t: %d

Completed count\t: %d
SS count\t\t: %d
'''
_download_text = 'The file for this map does not exist locally.'
_download_error = 'There was an error trying to download this map!'
_button_params = {
    'completed': None,
    'ss': False,
    'ssable': True,
    'ss_difficult': None,
    'apple_completed': None,
    'apple_ss': None,
    'apple_ssable': None,
    'apple_ss_difficult': None,
    'has_end': True,
    'playable_type': True,
    'has_apples': None,
}
_checkbox_params = {
    'allow_visible': True,
    'allow_hidden': False,
    'allow_unpublished': False,
    'allow_unknown': False,
    'choose_newest': False,
    'auto_launch': False
}
_entry_params = {
    'name_search': None,
}


class State(IntEnum):
    NO = 0
    YES = 1
    ___ = 2


class Window(Frame):
    def __init__(self, master, level_dict, level_dir, show_stats=False):
        Frame.__init__(self, master)
        self.master = master
        self.level_dict = level_dict
        self.level_dir = level_dir

        self.candidates = []
        self.kwargs = {}
        self.level_key = None
        self.level_name = None
        self._show_stats = show_stats

        self.master.title('Level Select')
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)

        left = Frame(self)
        left.grid(row=0, column=0, sticky=(N, E, S, W))
        right = Frame(self)
        right.grid(row=0, column=1, sticky=(N, E, S, W))

        self.stats_frame = Frame(self, relief='ridge', borderwidth=2)
        self.stats_text = StringVar(value='test')
        Message(self.stats_frame, textvariable=self.stats_text, justify=LEFT).pack()
        self.show_stats(show_stats)

        photo = ImageTk.PhotoImage(_blank_image)
        self.image_label = Label(left, image=photo)
        self.image_label.image = photo
        self.image_label.pack(anchor=NW)

        self.download_label = Label(left, text=_download_text)
        self.download_button = Button(left, text='Download', command=self.download_map)
        self.download_label.pack_forget()
        self.download_button.pack_forget()

        self.level_text = StringVar()
        self.level_text.set(_blank_text)
        self.message = Message(left, textvariable=self.level_text, justify=LEFT, width=_img_size[0])
        self.message.pack(anchor=NW)

        self.button_params = []
        for key in _button_params:
            value = int(State.___)
            if _button_params[key] is True:
                value = int(State.YES)
            elif _button_params[key] is False:
                value = int(State.NO)
            var = IntVar(value=value, name=key)
            self.button_params.append(var)
        next_row = self.build_buttons(right, _option_columns)

        self.checkbox_params = []
        for key in _checkbox_params:
            value = bool(State.NO)
            if _checkbox_params[key]:
                value = bool(State.YES)
            var = BooleanVar(value=value, name=key)
            self.checkbox_params.append(var)
        next_row = self.build_checkbuttons(right, _option_columns, next_row)

        self.entry_params = []
        for key in _entry_params:
            value = _entry_params[key]
            if value is None:
                value = ''
            var = StringVar(value=value, name=key)
            self.entry_params.append(var)
            Label(right, text=key).grid(row=next_row, column=0, sticky=W)
            Entry(right, textvariable=var).grid(row=next_row, column=1, columnspan=_option_columns - 1, sticky=(W, E))
            next_row += 1

        def dustkid():
            if self.level_name is not None:
                webbrowser.open(dustkid_link(self.level_name))

        def atlas():
            if self.level_name is not None:
                webbrowser.open(atlas_link(self.level_name))

        Button(right, text='Dustkid', command=dustkid)\
            .grid(row=next_row, column=0, sticky=(W, E), padx=5, pady=5)
        Button(right, text='Atlas', command=atlas)\
            .grid(row=next_row, column=1, sticky=(W, E), padx=5, pady=5)
        Button(right, text='Play', command=lambda: launch(self.level_name))\
            .grid(row=next_row, column=_option_columns - 2, sticky=(W, E), padx=5, pady=5)
        Button(right, text='Next', command=self.next_map)\
            .grid(row=next_row, column=_option_columns - 1, sticky=(W, E), ipadx=5, pady=5)
        next_row += 1

        right.grid_rowconfigure(next_row, weight=1)
        next_row += 1

        Label(right, text='Result:').grid(row=next_row, column=0, sticky=W)
        self.result = StringVar(value='ss')
        values = [res.name.lower() for res in list(Result) if res not in (Result.EXIT, Result.NEXT)]
        menu = OptionMenu(right, self.result, *values)
        menu.grid(row=next_row, column=1, sticky=(W, E), columnspan=2)

        def submit():
            if self.level_key is None:
                return
            process_command(Result[self.result.get().upper()],
                            self.level_dict.get(self.level_key, None),
                            self.result_comment.get())
            self.result_comment.set('')
            self.next_map()
            if self._show_stats:
                self.update_stats()

        Button(right, text='Submit', command=submit).grid(row=next_row, column=_option_columns - 1)
        next_row += 1

        self.result_comment = StringVar()
        Label(right, text='Reason:').grid(row=next_row, column=0, sticky=W)
        Entry(right, textvariable=self.result_comment).grid(row=next_row, column=1, columnspan=_option_columns - 1, sticky=(N, E, S, W))
        next_row += 1
        right.grid_rowconfigure(next_row, weight=1)

    def build_buttons(self, container, columns, first_row=0):
        def get_button_func(button: Button, var: IntVar):
            def callback():
                var.set((var.get() + 1) % len(list(State)))
                button.config(text=State(var.get()).name)
            return callback

        count = 0
        for r in range(first_row, 100, 2):
            for c in range(columns):
                var = self.button_params[count]
                Label(container, text=var._name).grid(row=r, column=c)
                button_text = State(var.get()).name
                b = Button(container, text=button_text)
                b.config(command=get_button_func(b, var))
                b.grid(row=r+1, column=c)
                count += 1
                if count >= len(self.button_params):
                    return r+2

    def build_checkbuttons(self, container, columns, first_row=0):
        count = 0
        for r in range(first_row, 100):
            for c in range(columns):
                var = self.checkbox_params[count]
                Checkbutton(container, variable=var, text=var._name).grid(row=r, column=c, sticky=W)
                count += 1
                if count >= len(self.checkbox_params):
                    return r+1

    def build_kwargs(self):
        kwargs = {}
        kwargs.update({var._name:bool(var.get()) if var.get() != State.___ else None for var in self.button_params})
        kwargs.update({var._name:var.get() for var in self.checkbox_params})
        kwargs.update({var._name:var.get() for var in self.entry_params})
        return kwargs

    def next_map(self):
        kwargs = self.build_kwargs()
        if kwargs != self.kwargs:
            # args have changed so we must reload candidates
            self.kwargs = kwargs
            self.candidates = get_level_candidates(self.level_dict, **kwargs)
        if not self.candidates:
            img_tk = ImageTk.PhotoImage(_blank_image)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk
            self.level_text.set(_blank_text+"\n~~No more levels match this criteria~~")
            self.level_key = None
            self.level_name = None
            return
        elif kwargs['choose_newest']:
            key = self.candidates[-1]
        else:
            key = random.choice(self.candidates)
        self.candidates.remove(key)
        self.level_key = key
        self.level_name = self.level_dict.get(key, _blank_info)['filename']
        self.load_level(key, len(self.candidates))
        if kwargs['auto_launch']:
            launch(self.level_name)

    def load_level(self, key, candidate_count=-1):
            info = self.level_dict[key]
            filename = info['filename']
            self.load_image(filename)
            self.load_message(info, candidate_count)

            if os.path.isfile(self.level_dir % filename):
                self.download_label.pack_forget()
                self.download_button.pack_forget()
            else:
                self.message.pack_forget()
                self.download_label.config(text=_download_text)
                self.download_label.pack(anchor=NW)
                self.download_button.pack(expand=1, fill=X)
                self.message.pack(anchor=NW)

    def load_message(self, info, candidate_count=-1):
        text = ''
        for key in info:
            space = '\t'
            if len(key) < 8:
                space += '\t'
            value = info[key]
            if key == 'level_type':
                value = LevelType(value).name.lower()
            elif key == 'published':
                value = Published(value).name.lower()
            text += '%s:%s%s\n' % (key, space, value)
        if candidate_count > 0:
            text += '\n%d other levels match this criteria' % candidate_count
        self.level_text.set(text)

    def load_image(self, filename):
        try:
            with open(self.level_dir % filename, 'rb') as f:
                # read only the info necessary to reach the image
                data = f.read()
                reader = BitReader.BitReader(data)
                MapReader.read_expect(reader, b"DF_LVL")
                version = reader.read(16)
                if version <= 42:
                    raise MapParseException("unsupported level version")
                # skip over unneeded info
                reader.read(64)
                meta = MapReader.read_metadata(reader)
                # finally reach the screen shot
                sshot_data = b""
                if version > 43:
                    sshot_len = reader.read(32)
                    sshot_data = reader.read_bytes(sshot_len)

            stream = io.BytesIO(sshot_data)
            img = Image.open(stream)
        except Exception:
            img = _blank_image

        img_tk = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk

    def download_map(self):
        filename = loadmaps.download_map(int(self.level_key))
        if filename is None:
            self.download_label.config(text=_download_error)
        else:
            self.level_dict[self.level_key]['filename']=filename
            self.download_label.pack_forget()
            self.download_button.pack_forget()
            self.load_image(filename)

    def show_stats(self, show=True):
        self._show_stats = show
        if show:
            self.stats_frame.grid(row=0, column=2, sticky=(N, E, S, W))
            self.update_stats()
        else:
            self.stats_frame.grid_forget()

    def update_stats(self):
        levels = len(self.level_dict)
        visible = len(get_level_candidates(self.level_dict))
        ssable = len(get_level_candidates(self.level_dict, ssable=True, playable_type=True,
                                          allow_hidden=True, allow_unpublished=True, allow_unknown=True))
        apples = len(get_level_candidates(self.level_dict, has_apples=True,
                                          allow_hidden=True, allow_unpublished=True, allow_unknown=True))
        apple_ssable = len(get_level_candidates(self.level_dict, apple_ssable=True, playable_type=True,
                                                allow_hidden=True, allow_unpublished=True, allow_unknown=True))
        complete_count = len(get_level_candidates(self.level_dict, completed=True))
        ss_count = len(get_level_candidates(self.level_dict, ss=True))
        self.stats_text.set(_stats_text % (levels, visible, ssable, apples, apple_ssable, complete_count, ss_count))

def main():
    root = Tk()

    try:
        with open(config_file, 'r') as f:
            config_dict = json.load(f)
    except FileNotFoundError:
        config_dict = {}

    index_file = config_dict.get('index_file', _default_index)
    level_dir = config_dict.get('level_dir', _default_level_dir) + '/%s'
    options = config_dict.get('level_select', dict())

    global _button_params, _checkbox_params, _entry_params
    _button_params = options.get('button_params', _button_params)
    _checkbox_params = options.get('checkbox_params', _checkbox_params)
    _entry_params = options.get('entry_params', _entry_params)
    stats_var = BooleanVar(value=options.get('show_stats', False))

    try:
        with open(index_file, 'r') as f:
            level_dict = json.load(f)
    except FileNotFoundError:
        root.withdraw()
        messagebox.showerror('Error', 'Could not find level index file.\npath: "%s"' % index_file)
        return

    window = Window(root, level_dict, level_dir, stats_var.get())

    def on_close():
        with open(index_file, 'w') as index:
            json.dump(level_dict, index, indent=4)
        kwargs = window.build_kwargs()
        for key in kwargs:
            if key in _button_params:
                _button_params[key] = kwargs[key]
            elif key in _checkbox_params:
                _checkbox_params[key] = kwargs[key]
            elif key in _entry_params:
                _entry_params[key] = kwargs[key]
        level_select_options = {
            'button_params': _button_params,
            'checkbox_params': _checkbox_params,
            'entry_params': _entry_params,
            'show_stats': stats_var.get()
        }
        config_dict['level_select'] = level_select_options
        with open(config_file, 'w') as config:
            json.dump(config_dict, config, indent=4)
        root.destroy()

    menu_bar = Menu(root)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='save and exit', command=on_close)
    file_menu.add_command(label='exit without saving', command=root.destroy)
    menu_bar.add_cascade(label='File', menu=file_menu)

    view_menu = Menu(menu_bar, tearoff=0)
    view_menu.add_checkbutton(label='Show stats',variable=stats_var,command=lambda:window.show_stats(stats_var.get()))
    menu_bar.add_cascade(label='View', menu=view_menu)

    root.config(menu=menu_bar)

    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()

if __name__ == '__main__':
    main()
