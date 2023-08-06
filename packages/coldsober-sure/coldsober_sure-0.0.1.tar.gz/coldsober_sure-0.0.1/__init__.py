from tkinter import *
class parent:
    def __init__(self):
        pass

    class sure_number:
        def __init__(self, widget, kind = None):
            self.widget = widget
            self.kind= kind
        def make(self, *args):
            try:
                int(float(self.widget.get()))
                if self.kind != "ttk":
                    self.widget.config(fg = "#000", highlightthickness = 1, highlightcolor = "#000", highlightbackground = "#000")
            except Exception:
                self.widget.delete(len(self.widget.get())-1, END)
                if self.kind != "ttk":
                    self.widget.config(fg = "#660099", highlightcolor = "#ff0066", highlightbackground = "#ff0066")