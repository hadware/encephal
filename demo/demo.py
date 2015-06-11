__author__ = 'hadware'

# !/usr/bin/python3.4

from gi.repository import Gtk, GObject, GLib, GdkPixbuf
import time
import threading
from execution.testing.labeled_database import TestLabeledDatabase
from execution.training.labeled_database import TrainLabeledDatabase
from datasets import MNIST, Onehot
from subnet_architectures.subnet_topology import SubnetTopology
from subnet import Network
from nodes.math_function.math_function import QuadraticError
from matplotlib import pyplot as plt
from  scipy import misc
import array

LEARNING_ITERATION_NB = 10000


class Main(Gtk.Window):
    def __init__(self):
        super().__init__()

        self._set_up_layout()
        self._set_up_signals()
        self._set_up_neural_lib()

        self.set_border_width(20)
        self.set_icon_from_file("demo/encephal_logo_only.png")
        self.image_display.set_from_file("demo/question_mark.png")
        self.result_label.set_markup("<span  font='100'>?</span>")

        GObject.threads_init()

        self.show_all()

    def _set_up_neural_lib(self):
        # building the neural network
        self.learn_db = MNIST("training")
        self.test_db = MNIST("testing")
        input_datasink = self.learn_db.input_datasink
        output_datasink = self.learn_db.output_datasink

        # setting up the learning and testing objects
        self.network = Network(SubnetTopology.MLP_simple(input_datasink, output_datasink, 100))
        self.network.randomize()
        encoder = Onehot(output_datasink)
        self.learning = TrainLabeledDatabase(self.network, self.learn_db, encoder, QuadraticError.differential)
        self.testing = TestLabeledDatabase(self.network, self.test_db, encoder)

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

        # adding elements
        self.grid.set_column_homogeneous(True)
        self.progress_bar = Gtk.ProgressBar()
        self.image_display = Gtk.Image()
        self.train_button, self.new_example_button, self.recognize_button = \
            (Gtk.Button(label="Train"), Gtk.Button(label="New Example"), Gtk.Button(label="Recognize"))
        self.result_label, self.status_label = Gtk.Label(), Gtk.Label("NN Idle")

        # laying out the icons in a grid
        self.grid.attach(self.train_button, 0, 0, 2, 1)
        self.grid.attach_next_to(self.progress_bar, self.train_button, Gtk.PositionType.RIGHT, 8, 1)
        self.grid.attach_next_to(self.status_label, self.train_button, Gtk.PositionType.BOTTOM, 10, 1)
        self.grid.attach_next_to(self.image_display, self.status_label, Gtk.PositionType.BOTTOM, 5, 6)
        self.grid.attach_next_to(self.result_label, self.image_display, Gtk.PositionType.RIGHT, 5, 6)
        self.grid.attach_next_to(self.new_example_button, self.image_display, Gtk.PositionType.BOTTOM, 5, 1)
        self.grid.attach_next_to(self.recognize_button, self.new_example_button, Gtk.PositionType.RIGHT, 5, 1)

    def _set_up_signals(self):
        """Setting up button events"""
        self.connect("delete-event", Gtk.main_quit)
        self.train_button.connect("clicked", self._start_learning)
        self.new_example_button.connect("clicked", self._get_new_image)
        self.recognize_button.connect("clicked", self._recognize)

    def _start_learning(self, widget):
        """Launches the learning"""
        # the learning function has a callback to update the progress
        self.is_learning = True
        thread = threading.Thread(target=self.learning.online_learn,
                                  args=(LEARNING_ITERATION_NB, 0.5, self._update_progressbar))
        thread.daemon = True
        thread.start()

    def _get_new_image(self, widget):
        """Requests a new image from the MNIST database, displays it"""
        # what we actually do is asking the testing for a single test, returning the data AND the result
        img_array, self.current_result = self.testing.single_test()
        data = array.array('B', img_array.tostring())
        width, height = img_array.shape
        # pixbuf = GdkPixbuf.Pixbuf.new_from_data(data, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width * 4)
        # self.image_display.set_from_pixbuf(pixbuf)
        misc.imsave('/tmp/current_img.jpg', img_array)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale('/tmp/current_img.jpg', width=220, height=220,
                                                         preserve_aspect_ratio=False)
        self.image_display.set_from_pixbuf(pixbuf)

    def _recognize(self, widget):
        """Asks the network to recognize the current digit, and displays it on the label"""
        # simply displays the result
        self._update_label(self.current_result)

    def _update_label(self, number):
        self.result_label.set_markup("<span font='100'>%i</span>" % number)

    def _update_progressbar(self, percentage):
        self.progress_bar.set_fraction(percentage)
        if percentage != 1.0:
            self.status_label.set_text("Training the Network")
        else:
            self.status_label.set_text("Training Ended")
        return False


if __name__ == "__main__":
    main = Main()
    Gtk.main()
