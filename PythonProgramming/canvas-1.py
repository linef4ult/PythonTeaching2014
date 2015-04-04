"""
Demonstrates the use of a tkinter 'canvas' widget to create a simple free-form drawing window.
"""
__author__ = 'mark'

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox


class GUI:
    def __init__(self, parent):
        # Remember the parent Tk object and configure the window to resize at the correct rate
        self.parent = parent
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        self.parent.title("Draw Canvas")

        # Make protocol handler to manage interaction between the application and the window handler
        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Don't allow 'tear-off' menus
        self.parent.option_add("*tearOff", FALSE)

        # Set up menus
        self.menu = Menu(self.parent)

        self.file_menu = Menu(self.menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save as", command=self.save_file)
        self.file_menu.add_command(label="Clear canvas", command=self.clear_canvas)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.catch_destroy)

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.parent.config(menu=self.menu)

        # Starting defaults
        self.lastx, self.lasty = 0, 0
        self.colour = "black"
        self.pen_weight = 1

        # self.frame1 = ttk.Frame(self.parent)
        # self.frame1.grid(row=0, column=0)

        # Create canvas
        self.canvas = Canvas(self.parent, border=1, scrollregion=(0, 0, 2000, 2000), bg="white")
        self.canvas.grid(row=0, column=0, sticky=N + S + E + W)
        self.canvas.bind("<Button-1>", self.xy)
        self.canvas.bind("<B1-Motion>", self.addLine)

        # Create scrollbars
        self.yscroll = ttk.Scrollbar(self.parent, orient=VERTICAL, command=self.canvas.yview)
        self.yscroll.grid(row=0, column=1, sticky=N + S)
        self.canvas["yscrollcommand"] = self.yscroll.set

        self.xscroll = ttk.Scrollbar(self.parent, orient=HORIZONTAL, command=self.canvas.xview)
        self.xscroll.grid(row=1, column=0, sticky=W + E)
        self.canvas["xscrollcommand"] = self.xscroll.set

        # Set up palette of colours and pen widths
        self.set_palette()

    def set_palette(self):
        colours = ["black", "blue", "red", "green", "white"]
        x1 = y1 = 10
        x2 = y2 = 30
        jump = 25

        for colour in colours:
            tag = "pen-"+colour
            self.canvas.create_rectangle((x1, y1, x2, y2), fill=colour, tags=tag)
            self.canvas.tag_bind(tag, "<Button-1>", lambda x: self.set_colour(colour))
            y1 += jump
            y2 += jump

        max_pen_width = 10
        pen_widths = [i for i in range(max_pen_width) if i % 2 == 1]

        for width in pen_widths:
            tag = "pen-" + str(width)
            self.canvas.create_rectangle((x1, y1, x2, y2), fill="white", outline="silver", tags=tag)
            self.canvas.create_line((x1, y1, x2, y2), fill="black", width=width)
            self.canvas.tag_bind(tag, "<Button-1>", lambda x: self.set_pen_weight(width))
            y1 += jump
            y2 += jump

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def xy(self, event):
        # Get coordinates of mouse click
        self.lastx, self.lasty = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

    def addLine(self, event):
        # Draw line on drag. Uses last known x/y values and recomputes new ones for each point on a linestring.
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.canvas.create_line((self.lastx, self.lasty, x, y), fill=self.colour, width=self.pen_weight)
        self.lastx, self.lasty = x, y

    def set_colour(self, new_colour):
        self.colour = new_colour

    def set_pen_weight(self, new_pen_weight):
        self.pen_weight = new_pen_weight

    def open_file(self):
        # Display gif image on canvas
        chosen_file = filedialog.askopenfilename(filetypes=(("GIF files", "*.gif"), ("All files", "*.*")))

        if chosen_file:
            self.gif = PhotoImage(file=chosen_file)
            self.clear_canvas()
            self.canvas.create_image(40, 0, anchor=NW, image=self.gif)

    def save_file(self):
        # Save canvas as psotscript (.ps) file
        target = filedialog.asksaveasfilename(filetypes=(("Postscript files", "*.ps"), ("All files", "*.*")))

        # If we have a filename write to it
        if target:
            # Make sure that we get the whole canvas, not just the visible part
            self.canvas.xview_moveto(0.0)
            self.canvas.yview_moveto(0.0)
            width = self.canvas.bbox("all")[2]
            height = self.canvas.bbox("all")[3]

            self.canvas.postscript(file=target, colormode='color', width=width, height=height, pagewidth=width,
                                   pageheight=height)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.set_palette()


def main():
    root = Tk()
    GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()