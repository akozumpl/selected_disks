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
        self.store = builder.get_object("treestore_disks")
        self.label = builder.get_object("label_summary")
        self.store.set_sort_func(self.COL_CAPACITY, self._cmp_device, "size")
        self.store.set_sort_func(self.COL_FREE, self._cmp_device, "size")

    def _append_device(self, device, it_parent):
        it = self.store.append(it_parent)
        self.store.set_value(it, self.COL_OBJECT, device)
        self.store.set_value(it, self.COL_NAME, device.model)
        self.store.set_value(it, self.COL_CAPACITY, "%d GB" % (device.size / 1000))
        self.store.set_value(it, self.COL_FREE, "%d GB" % (device.size / 1000))
        self.store.set_value(it, self.COL_ID, device.serial)

    def _cmp_device(self, model, a_iter, b_iter, attr):
        def compute_for_iter(it):
            device = self.store.get_value(it, self.COL_OBJECT)
            if device:
                return getattr(device, attr)
            # if this is a category, compute the sum of attr over the children
            acc = 0
            it_children = self.store.iter_children(it)
            while it_children:
                acc += compute_for_iter(it_children)
                it_children = self.store.iter_next(it_children)
            return acc

        return compute_for_iter(a_iter) - compute_for_iter(b_iter)

    def _update_label(self):
        vals = {
            "count" : len(list(self.iter_device_rows())),
            "capacity" : reduce(lambda acc, row: acc + row[self.COL_OBJECT].size,
                                self.iter_device_rows(), 0) / 1000,
            "free" : reduce(lambda acc, row: acc + row[self.COL_OBJECT].size,
                                self.iter_device_rows(), 0) / 1000
            }
        self.label.set_markup(self.SUMMARY_TEMPLATE % vals)

    def cb_close(self, button):
        self.window.destroy()

    def cb_remove(self, button):
        path = self.view.get_cursor()[0]
        it = self.store.get_iter(path)
        self.store.remove(it)
        self.update()

    def iter_device_rows(self):
        """ Iterator for those rows of model that represent a real device. """
        return (it for it in self.store)

    def populate(self, devices):
        map(lambda d : self._append_device(d, None), devices)
        self.update()
        self.view.set_show_expanders(False)

    def run(self):
        self.window.show_all()
        self.window.run()
        self.window.destroy()
        return [r[self.COL_OBJECT] for r in self.iter_device_rows()]

    def update(self):
        self._update_label()

class SelectedDisksTreeDialog(SelectedDisksDialog):
    def iter_device_rows(self):
        """ Iterator for those rows of model that represent a real device.

            Categories, namely, are excluded.
        """
        for category in self.store:
            for it in category.iterchildren():
                yield it

    def _update_categories(self):
        """ Delete categories with no child. """
        categories = 0
        it = self.store.get_iter_first()
        while it:
            if self.store.iter_has_child(it):
                categories += 1
                it = self.store.iter_next(it)
            else:
                if not self.store.remove(it):
                    break

    def populate(self, devices):
        types = {d.type : None for d in devices}
        for t in types:
            types[t] = self.store.append(None)
            self.store.set_value(types[t], self.COL_NAME, t)
        map(lambda d: self._append_device(d, types[d.type]), devices)
        self.update()
        self.view.expand_all()

    def update(self):
        self._update_categories()
        self._update_label()
