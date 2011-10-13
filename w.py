#! /usr/bin/python

import glib
from gi.repository import Gtk

from selected_disks_dialog import SelectedDisksDialog

class MockStorageDevice(object):
    def __init__(self, model, size, serial):
        self.model = model
        self.size = size
        self.serial = serial

def list_of_devices():
    return [
        MockStorageDevice("HITACHI HTS72323", 320e3, "HITACHI_HTS723232A7A364_E3834563J41DPN"),
        MockStorageDevice("SDD device", 32e3, "31a6bdf5c570c15efcb7fa56c45928cd8977714c"),
        MockStorageDevice("western digital", 540e3, "67fe5ab0bf5d4be77b27f0ff253810acb50a22be")]

main_loop = None

def f_quit(widget):
    main_loop.quit()

def c_button(button):
    dialog = SelectedDisksDialog()
    dialog.populate(list_of_devices())
    dialog.run()

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
