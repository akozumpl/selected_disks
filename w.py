#! /usr/bin/python

import glib
from gi.repository import Gtk

main_loop = None


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

def f_quit(widget):
    main_loop.quit()

def c_button(button):
    dialog = SelectedDisksDialog()
    dialog.show()

def main():
    button = Gtk.Button.new_with_mnemonic("sh_ow")
    button.connect('clicked', c_button)
    window = Gtk.Window(title="W")
    window.connect('destroy', f_quit)
    window.add(button)
    window.show_all()
    global main_loop
    main_loop= glib.MainLoop()
    main_loop.run()

if __name__ == "__main__":
    main()
