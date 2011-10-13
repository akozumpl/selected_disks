import glib
from gi.repository import Gtk

class SelectedDisksDialog(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("selected_disks.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("selected_disks_dialog")

    def cb_close(self, button):
        self.window.destroy()

    def cb_remove(self, button):
        print "cb_remove()"

    def show(self):
        self.window.show_all()

