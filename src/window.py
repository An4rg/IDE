# This code is under GNU GPL 3.0. You can't reuse this code to produce non-free softwares.
# In GTK4, we separate the app from the window
# Here you are in the main window logic.
# You'll find the widget structure in src/window.ui :)

from gi.repository import Adw, Gtk, Gdk # Gtk4 imports


class IDEConfig: # the main object with every config you will find, very practical to make the settings 
    def __init__(self):
        self.CodeEditorFontSize = 25
        self.EditorBackgroundColor = '#1A1A1A'

config = IDEConfig()


@Gtk.Template(resource_path='/dev/anarg/PortableIDE/window.ui')
class IdeWindow(Adw.ApplicationWindow): # The window code
    __gtype_name__ = 'IdeWindow'

    code_editor = Gtk.Template.Child() # Getting the code widget

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css = Gtk.CssProvider() #adding the CSS to the app
        css.load_from_data(f"""
            .CodeEditor {{
                font-size: {config.CodeEditorFontSize}px;
                background-color: {config.EditorBackgroundColor};
            }}

            window {{
                background-color: {config.EditorBackgroundColor};
            }}
        """.encode())
        
        # Applying the Css
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )