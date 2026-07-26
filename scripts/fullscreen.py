import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

win = Gtk.Window()
win.fullscreen()

css = b"window { background-color: black; }"
provider = Gtk.CssProvider()
provider.load_from_data(css)
win.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()