#! /usr/bin/python

import glib
from gi.repository import Gtk, Gdk

main_loop = None

def f_quit(widget):
    main_loop.quit()

def c_button(button):
    builder = Gtk.Builder()
    builder.add_from_file("selected_disks.glade")
    w = builder.get_object("selected_disks_dialog")
    store = builder.get_object("liststore_disks")
#    iter = store.insert(0)
#    store.set(iter, {0 : "yeah"})
    w.show_all()

def main():
    button = Gtk.Button("show")
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
