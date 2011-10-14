import glib
from gi.repository import Gtk
import operator

class SelectedDisksDialog(object):
    COL_OBJECT = 0
    COL_NAME = 1
    COL_CAPACITY = 2
    COL_FREE = 3
    COL_ID = 4
    SUMMARY_TEMPLATE="<b>%(count)d disks; %(capacity).1f GB capacity; " \
        "%(free).1f GB free space</b> (unpartitioned &amp; filesystems)"

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("selected_disks.glade")
        builder.connect_signals(self)
        self.window = builder.get_object("selected_disks_dialog")
        self.view = builder.get_object("treeview_disks")
        self.store = builder.get_object("liststore_disks")
        self.label = builder.get_object("label_summary")
        self.store.set_sort_func(self.COL_CAPACITY, self.cmp_device, "size")
        self.store.set_sort_func(self.COL_FREE, self.cmp_device, "size")

    def cb_close(self, button):
        self.window.destroy()

    def cb_remove(self, button):
        path = self.view.get_cursor()[0]
        it = self.store.get_iter(path)
        self.store.remove(it)
        self.update_label()

    def cmp_device(self, model, a_iter, b_iter, attr):
        device1 = self.store.get_value(a_iter, self.COL_OBJECT)
        device2 = self.store.get_value(b_iter, self.COL_OBJECT)
        attr1 = getattr(device1, attr)
        attr2 = getattr(device2, attr)
        return attr1 - attr2

    def populate(self, devices):
        for d in devices:
            it = self.store.append()
            self.store.set_value(it, self.COL_OBJECT, d)
            self.store.set_value(it, self.COL_NAME, d.model)
            self.store.set_value(it, self.COL_CAPACITY, "%d GB" % (d.size / 1000))
            self.store.set_value(it, self.COL_FREE, "%d GB" % (d.size / 1000))
            self.store.set_value(it, self.COL_ID, d.serial)
        self.update_label()

    def run(self):
        self.window.show_all()
        self.window.run()
        self.window.destroy()
        return [r[self.COL_OBJECT] for r in self.store]

    def update_label(self):
        vals = {
            "count" : len(self.store),
            "capacity" : reduce(lambda acc, row: acc + row[self.COL_OBJECT].size,
                                self.store, 0) / 1000,
            "free" : reduce(lambda acc, row: acc + row[self.COL_OBJECT].size,
                                self.store, 0) / 1000
            }
        self.label.set_markup(self.SUMMARY_TEMPLATE % vals)
