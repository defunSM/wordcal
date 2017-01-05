#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from subprocess import call

#list of tuples for each software, containing the software name, initial release, and main programming languages used
def getoutput():

    f = open("output.txt", 'r')
    array = []

    for line in f.readlines():
        words = line.split(",")
        array.append([words[0], words[1], words[2].split("\n")[0]])

    f.close()
    return array

software_list = getoutput()

class TreeViewFilterWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="WordCal GUI")
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.notebook.append_page(self.grid, Gtk.Label("WordCal"))


        self.grid2 = Gtk.Grid()
        self.add(self.grid2)

        self.label = Gtk.Label("Link:  ")
        self.add(self.label)
        self.grid2.add(self.label)

        self.textbox = Gtk.Entry()
        self.textbox.set_width_chars(50)
        self.textbox.set_text("https://en.wikipedia.org/wiki/Physics")
        self.grid2.add(self.textbox)

        self.linksearchbutton = Gtk.Button("Search")
        self.linksearchbutton.connect("clicked", self.searchwordsinlink)
        self.grid2.add(self.linksearchbutton)



        self.notebook.append_page(self.grid2, Gtk.Label("WebScraper"))

        width = 1400
        height = 840
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("graphpic.png", width, height)


        img = Gtk.Image.new_from_file("graphpic.png")
        img.set_from_pixbuf(self.pixbuf)
        self.notebook.append_page(img, Gtk.Label("Graph"))




        #Creating the ListStore model
        self.software_liststore = Gtk.ListStore(str, str, str)
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

        #Creating the filter, feeding it with the liststore model
        self.language_filter = self.software_liststore.filter_new()
        #setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        for i, column_title in enumerate(["Word", "Frequency", "Percentage (%)"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()

        button = Gtk.Button("Search")
        self.buttons.append(button)
        button.connect("clicked", self.on_selection_button_clicked)

        self.entry = Gtk.Entry()
        self.buttons.append(self.entry)





        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        self.show_all()

    def searchwordsinlink(self, widget):

        link = self.textbox.get_text()

        print(link)

        call(["python", "graphword.py", "-f", link])

        software_list = getoutput()

        self.software_liststore.clear()
        for software_ref in software_list:
            self.software_liststore.append(list(software_ref))
        self.current_filter_language = None

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True

        else:
            return model[iter][0] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        #we set the current language filter to the button's label
        self.current_filter_language = self.entry.get_text()

        if self.current_filter_language == "":
            self.current_filter_language = None

        print("%s language selected!" % self.current_filter_language)
        #we update the filter, which updates in turn the view
        self.language_filter.refilter()


win = TreeViewFilterWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
