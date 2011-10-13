#! /usr/bin/python

import glib
from gi.repository import Gtk

from selected_disks_dialog import SelectedDisksDialog

main_loop = None


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
