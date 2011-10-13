import glib
from gi.repository import Gtk

class SelectedDisksDialog(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("selected_disks.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("selected_disks_dialog")
        self.store = builder.get_object("liststore_disks")
        self.store.set_sort_func(2, self.cmp_device, "size")
        self.store.set_sort_func(3, self.cmp_device, "size")

    def cb_close(self, button):
        self.window.destroy()

    def cb_remove(self, button):
        print "cb_remove()"

    def cmp_device(self, model, a_iter, b_iter, attr):
        device1 = self.store.get_value(a_iter, 0)
        device2 = self.store.get_value(b_iter, 0)
        attr1 = getattr(device1, attr)
        attr2 = getattr(device2, attr)
        return attr1 - attr2

    def populate(self, devices):
        for d in devices:
            it = self.store.append()
            self.store.set_value(it, 0, d)
            self.store.set_value(it, 1, d.model)
            self.store.set_value(it, 2, "%d GB" % (d.size / 1000))
            self.store.set_value(it, 3, "%d GB" % (d.size / 1000))
            self.store.set_value(it, 4, d.serial)

    def run(self):
        self.window.show_all()
        self.window.run()
        self.window.hide()
