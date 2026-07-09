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

# the command prompt for debugging and power users
class CommandPalette(Gtk.Revealer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_transition_type(Gtk.RevealerTransitionType.SLIDE_DOWN)
        self.set_transition_duration(150)
        self.set_valign(Gtk.Align.START)
        self.set_halign(Gtk.Align.CENTER)

        # Conteneur visuel de la palette
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.add_css_class("card")  # style libadwaita "carte" flottante
        box.set_margin_top(12)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Tapez une commande…")
        self.entry.set_width_chars(50)
        self.entry.connect("activate", self.on_command_entered)

        box.append(self.entry)
        self.set_child(box)
        self.set_reveal_child(False)

    def toggle(self):
        showing = self.get_reveal_child()
        self.set_reveal_child(not showing)
        if not showing:
            self.entry.grab_focus()

    def on_command_entered(self, entry):
        command = entry.get_text()
        print(f"Commande exécutée : {command}")
        self.set_reveal_child(False)
        entry.set_text("")
        

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

        # test = Gtk.Label(label="abab")
        overlay = Gtk.Overlay()
        self.set_content(overlay)
        overlay.set_child(self.code_editor)

        self.command_palette = CommandPalette()
        overlay.add_overlay(self.command_palette)

        # Raccourci clavier pour ouvrir/fermer
        controller = Gtk.ShortcutController()
        controller.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("<Ctrl><Shift>p"),
                Gtk.CallbackAction.new(lambda *a: self.command_palette.toggle())
            )
        )
        self.add_controller(controller)