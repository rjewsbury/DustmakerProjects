from tkinter import *
import json
from CustomFileManager.level_stats import download_stat_files
from CustomFileManager.create_index import update_index

config_file = './_config.json'
_option_columns = 2
_checkbox_params = {
    'generate_rank_file': False,
    'generate_apple_rank_file': False,
    'load_extended': False,
    'load_missing': False,
    'reload_existing': False,
    'only_download_visible': True,
    'debug': False
}
_entry_params = {
    'lower_bound': 0,
    'upper_bound': 1000000,
    'min_missing_id': 93,
    'user_id': 0
}
_new_level_params = {
    'add_map': True,
    'add_ranks': False,
    'add_apple_ranks': False,
    'add_published': True,
}
_existing_level_params = {
    'update_map': False,
    'update_ranks': False,
    'update_apple_ranks': False,
    'update_published': False,
}


class Window(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        self.master.title('Level Index Builder')
        self.master.resizable(False, False)
        self.pack(fill=BOTH, expand=1)

        self.checkbox_params = []
        for key in _checkbox_params:
            value = _checkbox_params[key]
            var = BooleanVar(value=value, name=key)
            self.checkbox_params.append(var)
        next_row = self.build_checkbuttons(self, self.checkbox_params, _option_columns)

        self.entry_params = []
        for key in _entry_params:
            value = _entry_params[key]
            if value is None:
                value = ''
            var = StringVar(value=value, name=key)
            self.entry_params.append(var)
            Label(self, text=key).grid(row=next_row, column=0, sticky=W)
            Entry(self, textvariable=var).grid(row=next_row, column=1, columnspan=_option_columns - 1, sticky=(W, E))
            next_row += 1

        Label(self, text='Existing levels:').grid(row=next_row, column=0, sticky=W)
        next_row += 1

        self.existing_level_params = []
        for key in _existing_level_params:
            value = _existing_level_params[key]
            var = BooleanVar(value=value, name=key)
            self.existing_level_params.append(var)
        next_row = self.build_checkbuttons(self, self.existing_level_params, _option_columns, next_row)

        Label(self, text='New levels:').grid(row=next_row, column=0, sticky=W)
        next_row += 1

        self.new_level_params = []
        for key in _new_level_params:
            value = _new_level_params[key]
            var = BooleanVar(value=value, name=key)
            self.new_level_params.append(var)
        next_row = self.build_checkbuttons(self, self.new_level_params, _option_columns, next_row)

        def callback():
            existing_kwargs, kwargs = self.build_kwargs()
            download_stat_files(**kwargs)
            update_index(existing_kwargs, **kwargs)

        Button(self, text='Generate', command=callback).grid(row=next_row, column=_option_columns-1, sticky=(E, W))

    def build_checkbuttons(self, container, params, columns, first_row=0):
        count = 0
        for r in range(first_row, 100):
            for c in range(columns):
                var = params[count]
                Checkbutton(container, variable=var, text=var._name).grid(row=r, column=c, sticky=W)
                count += 1
                if count >= len(params):
                    return r+1

    def build_kwargs(self):
        existing_kwargs = {}
        kwargs = {}
        kwargs.update({var._name:var.get() for var in self.checkbox_params})
        kwargs.update({var._name:int(var.get()) for var in self.entry_params})
        kwargs.update({var._name:var.get() for var in self.new_level_params})

        existing_kwargs.update({var._name.replace('update','add'):var.get() for var in self.existing_level_params})
        return existing_kwargs, kwargs


def main():
    root = Tk()

    try:
        with open(config_file, 'r') as f:
            config_dict = json.load(f)
    except FileNotFoundError:
        config_dict = {}

    options = config_dict.get('create_index', dict())

    global _checkbox_params, _entry_params, _new_level_params, _existing_level_params
    _checkbox_params = options.get('checkbox_params', _checkbox_params)
    _entry_params = options.get('entry_params', _entry_params)
    _new_level_params = options.get('new_level_params', _new_level_params)
    _existing_level_params = options.get('existing_level_params', _existing_level_params)

    window = Window(root)

    def on_close():
        existing_kwargs, kwargs = window.build_kwargs()

        for key in kwargs:
            if key in _new_level_params:
                _new_level_params[key] = kwargs[key]
            elif key in _entry_params:
                _entry_params[key] = kwargs[key]
            elif key in _checkbox_params:
                _checkbox_params[key] = kwargs[key]
        _existing_level_params.update({key.replace('add', 'update'): val for (key, val) in existing_kwargs.items()})
        create_index_options = {
            'checkbox_params': _checkbox_params,
            'entry_params': _entry_params,
            'new_level_params': _new_level_params,
            'existing_level_params': _existing_level_params
        }
        config_dict['create_index'] = create_index_options
        with open(config_file, 'w') as config:
            json.dump(config_dict, config, indent=4)
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()

if __name__ == '__main__':
    main()