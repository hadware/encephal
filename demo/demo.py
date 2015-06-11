__author__ = 'hadware'

# !/usr/bin/python3.4

from gi.repository import Gtk
from datasets import MNIST


class Main(Gtk.Window):
    def __init__(self):
        super().__init__()

        self._set_up_layout()
        self._set_up_signals()

        # temporary tests
        self.progress_bar.set_fraction(0.7)
        self.image_display.set_from_file("sample_digit.png")
        self.result_label.set_markup("<span  font='100'>5</span>")

        self.show_all()

    def _set_up_neural_lib(self):
        self.learn_db = MNIST("training")
        self.test_db = MNIST("testing")

    def _set_up_layout(self):
        """Sets up the whole window layout"""
        # setting up the grid and the windows size
        self.grid = Gtk.Grid()
        self.add(self.grid)

        # window properties
        self.set_size_request(600, 400)
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(20)
        self.set_title("Encephal Demo")
        self.set_icon_from_file("encephal_logo_only.png")

        # adding elements
        self.grid.set_column_homogeneous(True)
        self.progress_bar = Gtk.ProgressBar()
        self.image_display = Gtk.Image()
        self.train_button, self.new_example_button, self.recognize_button = \
            (Gtk.Button(label="Train"), Gtk.Button(label="New Example"), Gtk.Button(label="Recognize"))
        self.result_label = Gtk.Label()

        # laying out the icons in a grid
        self.grid.attach(self.train_button, 0, 0, 2, 1)
        self.grid.attach_next_to(self.progress_bar, self.train_button, Gtk.PositionType.RIGHT, 8, 1)
        self.grid.attach_next_to(self.image_display, self.train_button, Gtk.PositionType.BOTTOM, 5, 6)
        self.grid.attach_next_to(self.result_label, self.image_display, Gtk.PositionType.RIGHT, 5, 6)
        self.grid.attach_next_to(self.new_example_button, self.image_display, Gtk.PositionType.BOTTOM, 5, 1)
        self.grid.attach_next_to(self.recognize_button, self.new_example_button, Gtk.PositionType.RIGHT, 5, 1)

    def _set_up_signals(self):
        """Setting up button events"""
        self.connect("delete-event", Gtk.main_quit)
        self.train_button.connect("clicked", self._start_learning)
        self.new_example_button.connect("clicked", self._get_new_image)
        self.new_example_button.connect("clicked", self._recognize)

    def _start_learning(self):
        """Launches the learning"""
        pass

    def _get_new_image(self):
        """Requests a new image from the MNIST database, display it"""
        pass

    def _recognize(self):
        """Asks the network to recognize the current digit, and displays it on the label"""
        pass

    def _update_label(self, number):
        pass


if __name__ == "__main__":
    main = Main()
    Gtk.main()
