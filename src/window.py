from gi.repository import Adw, Gtk, Gdk

class IDEConfig:
    def __init__(self):
        self.CodeEditorFontSize = 25
        self.EditorBackgroundColor = '#1A1A1A'

config = IDEConfig()


@Gtk.Template(resource_path='/dev/anarg/PortableIDE/window.ui')
class IdeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'IdeWindow'

    code_editor = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        css = Gtk.CssProvider()
        css.load_from_data(f"""
            .CodeEditor {{
                font-size: {config.CodeEditorFontSize}px;
                background-color: {config.EditorBackgroundColor};
            }}

            window {{
                background-color: {config.EditorBackgroundColor};
            }}
        """.encode())
        

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )