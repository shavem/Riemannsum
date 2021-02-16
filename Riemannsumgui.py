import tkinter as tk
from tkinter import ttk
import sympy
from fractions import Fraction
import tabulate
import matplotlib.pyplot as plt
import matplotlib.figure as pltfig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import ImageTk, Image, ImageFont, ImageDraw
import os


class Riemann:
    # function = string representing function
    # a = starting value
    # b = ending value
    # n = number of subintervals
    # type = type of Riemann sum
    # work = whether or not/what type of work to show (optional)
    def __init__(self, function, a, b, n, type, work="df"):
        # Parse the input function with implicit multiplication support
        self.func = sympy.parse_expr(function,
                                     transformations=(sympy.parsing.sympy_parser.standard_transformations +
                                                      (
                                                          sympy.parsing.sympy_parser.implicit_multiplication_application,))).subs("e", sympy.exp(1))
        self.a = float(a)
        self.b = float(b)
        self.n = int(n)
        self.sublength = (self.b - self.a) / self.n
        # all significant x and y values for the curve
        self.xvalues = []
        self.yvalues = []
        # overall sum
        self.sum = 0
        # this sum is used in the work displaying process. It is the final answer without (divided by) delta x
        self.worksum = 0
        # these are the work steps. The number after work corresponds to the step and the letter refers to decimal and fraction
        self.work1d = u"S = \u0394x["
        self.work1f = u"S = \u0394x["
        self.work2f = f"S = {self.sublength} * ["
        self.work2d = f"S = {self.sublength} * ["
        self.work3f = f"S = {'%g' % self.sublength} * "
        self.work3d = f"S = {'%g' % self.sublength} * "
        # this value is used in the work displaying process for a midpoint sum
        self.midvalues = []
        self.midyvalues = []
        # verify that the work input is valid
        if work.lower() == "f" or work.lower() == "d" or work.lower() == "df" or work.lower() == "fd":
            self.showwork = True
        elif work.lower() == "n":
            self.showwork = False
        else:
            raise ValueError(f'{work} is not a valid input. Please input "d", "f", or "n"')
        # populate xvalues with all significant x values
        for i in range(self.n + 1):
            self.xvalues.append(self.a + (i * self.sublength))
        for xval in self.xvalues:
            self.yvalues.append(self.func.subs("x", xval))
        # populate midvalues with all significant x values for midpoint sum
        for value in self.xvalues[:-1]:
            self.midvalues.append((1 / 2) * (self.xvalues[self.xvalues.index(value) + 1] + value))
        for value in self.midvalues:
            self.midyvalues.append(self.func.subs("x", value))
        # handle basic plot creation with line
        self.plotpath = "test.png"
        self.workpath = "work.png"
        plt.clf()
        self.plotx = np.linspace(self.a, self.b, self.n * (self.n + 30))
        self.lamb = sympy.lambdify("x", self.func, np)
        fig, ax = plt.subplots()
        ax.plot(self.plotx, self.lamb(self.plotx))
        # left Riemann sum
        if type.lower() == "left":
            for value in self.xvalues[:-1]:
                self.sum += (self.func.subs("x", value) * self.sublength)
                self.worksum += self.func.subs("x", value)
                # add to the work strings and remove unnecessary characters
                self.work1f += f"f({Fraction(value)}) + "
                self.work1d += f"f({'%g' % (value)}) + "
                self.work2d += f"{'%g' % self.func.subs('x', value)} + "
                try:
                    self.work2f += f"{str(Fraction(str(self.func.subs('x', value))))} + "
                    self.work3f += f"({str(Fraction(str(self.worksum)))})"
                    self.finalf = str(Fraction(str(self.sum)))
                except:
                    self.work2f += f"{self.func.subs('x', value)}"
                    self.work3f += f"({self.worksum})"
                    self.finalf = self.sum

            self.work1f = self.work1f[:-3] + "]"
            self.work1d = self.work1d[:-3] + "]"
            self.work2f = self.work2f[:-3] + "]"
            self.work2d = self.work2d[:-3] + "]"
            self.work3d += '%g' % (self.worksum)
            # add sum to plot
            ax.plot(self.xvalues[:-1], self.yvalues[:-1], "b.", markersize=10)
            plt.title(f"Left Riemann sum of {self.n} subintervals")
            ax.bar(self.xvalues[:-1], self.yvalues[:-1], width=self.sublength, alpha=0.35, align="edge", edgecolor="b")
            ax.set_aspect('equal')
            ax.grid(True, which='both')
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.yaxis.tick_left()
            ax.spines['bottom'].set_position('zero')
            ax.spines['top'].set_color('none')
            ax.xaxis.tick_bottom()
            plt.savefig(self.plotpath)
        # right Riemann sum
        elif type.lower() == "right":
            for value in self.xvalues[1:]:
                self.sum += (self.func.subs("x", value) * self.sublength)
                self.worksum += self.func.subs("x", value)
                # add to the work strings and remove unnecessary characters
                self.work1f += f"f({Fraction(value)}) + "
                self.work1d += f"f({'%g' % (value)}) + "
                self.work2d += f"{'%g' % self.func.subs('x', value)} + "
                try:
                    self.work2f += f"{str(Fraction(str(self.func.subs('x', value))))} + "
                    self.work3f += f"({str(Fraction(str(self.worksum)))})"
                    self.finalf = str(Fraction(str(self.sum)))
                except:
                    self.work2f += f"{self.func.subs('x', value)}"
                    self.work3f += f"({self.worksum})"
                    self.finalf = self.sum
            self.work1f = self.work1f[:-3] + "]"
            self.work1d = self.work1d[:-3] + "]"
            self.work2f = self.work2f[:-3] + "]"
            self.work2d = self.work2d[:-3] + "]"
            self.work3d += '%g' % (self.worksum)
            ax.plot(self.xvalues[1:], self.yvalues[1:], "b.", markersize=10)
            plt.title(f"Right Riemann sum of {self.n} subintervals")
            ax.bar(self.xvalues[1:], self.yvalues[1:], width=-self.sublength, align="edge", alpha=0.35, edgecolor="b")
            ax.set_aspect('equal')
            ax.grid(True, which='both')
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.yaxis.tick_left()
            ax.spines['bottom'].set_position('zero')
            ax.spines['top'].set_color('none')
            ax.xaxis.tick_bottom()
            plt.savefig(self.plotpath)
        # middle Riemann sum
        elif type.lower() == "midpoint" or type.lower() == "middle":
            for value in self.xvalues[:-1]:
                self.sum += (self.func.subs("x", 0.5 * (
                        self.xvalues[self.xvalues.index(value) + 1] + value)) * self.sublength)
                self.worksum += self.func.subs("x", 0.5 * (self.xvalues[self.xvalues.index(value) + 1] + value))
                # add to the work strings and remove unnecessary characters
                self.work2d += f"{'%g' % self.func.subs('x', 0.5 * (self.xvalues[self.xvalues.index(value) + 1] + value))} + "
                try:
                    self.work2f += f"{str(Fraction(str(self.func.subs('x', 0.5 * (self.xvalues[self.xvalues.index(value) + 1] + value)))))} + "
                    self.work3f += f"({str(Fraction(str(self.worksum)))})"
                    self.finalf = str(Fraction(str(self.sum)))
                except:
                    self.work2f += f"{self.func.subs('x', 0.5 * (self.xvalues[self.xvalues.index(value) + 1] + value))} + "
                    self.work3f += f"({self.worksum})"
                    self.finalf = self.sum
            for value in self.midvalues:
                self.work1f += f"f({Fraction(value)}) + "
                self.work1d += f"f({'%g' % (value)}) + "
            self.work1f = self.work1f[:-3] + "]"
            self.work1d = self.work1d[:-3] + "]"
            self.work2f = self.work2f[:-3] + "]"
            self.work2d = self.work2d[:-3] + "]"
            self.work3d += '%g' % (self.worksum)
            self.work3f += f"({str(Fraction(str(self.worksum)))})"
            ax.plot(self.midvalues, self.midyvalues, "b.", markersize=10)
            ax.bar(self.midvalues, self.midyvalues, width=self.sublength, alpha=0.35, edgecolor="b")
            plt.title(f"Midpoint Riemann sum of {self.n} subintervals")
            ax.set_aspect('equal')
            ax.grid(True, which='both')
            ax.spines['left'].set_position('zero')
            ax.spines['right'].set_color('none')
            ax.yaxis.tick_left()
            ax.spines['bottom'].set_position('zero')
            ax.spines['top'].set_color('none')
            ax.xaxis.tick_bottom()
            plt.savefig(self.plotpath)
        else:
            raise TypeError(f"{type} is not a supported Riemann sum type")

        # final statements for the sum output and print formatting
        # self.sum can be used to increase flexibility
        if work.lower() == "d":
            self.final = f"{self.work1d}\n{self.work2d}\n{self.work3d}\nS = {self.sum}"
        elif work.lower() == "f":
            self.final = f"{self.work1f}\n{self.work2f}\n{self.work3f}\nS = {str(Fraction(str(self.sum)))}"
        elif work.lower() == "df" or work.lower() == "fd":
            self.final = tabulate.tabulate({
                "Decimal": [self.work1d, self.work2d, self.work3d, f"Final approximation: {'%g' % self.sum}"],
                "Fraction": [self.work1f, self.work2f, self.work3f,
                             f"Final approximation: {self.finalf}"]
            }, headers="keys", colalign=("center", "center")) + f"\n\nUnrounded sum: {self.sum}"
        else:
            self.final = f"Riemann sum approximation: {self.sum}"

        self.worklines = self.final.split("\n")
        self.maxWidth = 0
        for workline in self.worklines:
            if len(workline) > self.maxWidth:
                self.maxWidth = len(workline)

        self.workimage = Image.new(size=(self.maxWidth * 10, (self.final.count("\n") + 1) * 18), mode="L", color=(255))
        self.workdraw = ImageDraw.Draw(self.workimage)
        self.font = ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf', 16)
        self.workdraw.text(xy=(0, 0), text=self.final, font=self.font)
        self.workimage.save(self.workpath)

        self.pfunc = sympy.pretty(self.func)


class DoubleScrolledFrame:
    """
    A vertically scrolled Frame that can be treated like any other Frame
    ie it needs a master and layout and it can be a master.
    keyword arguments are passed to the underlying Frame
    except the keyword arguments 'width' and 'height', which
    are passed to the underlying Canvas
    note that a widget layed out in this frame will have Canvas as self.master,
    if you subclass this there is no built in way for the children to access it.
    You need to provide the controller separately.

    Class credit - https://gist.github.com/novel-yet-trivial/2841b7b640bba48928200ff979204115
    """

    def __init__(self, master, **kwargs):
        width = kwargs.pop('width', None)
        height = kwargs.pop('height', None)
        self.outer = tk.Frame(master, **kwargs)

        self.vsb = ttk.Scrollbar(self.outer, orient=tk.VERTICAL)
        self.vsb.grid(row=0, column=1, sticky='ns')
        self.hsb = ttk.Scrollbar(self.outer, orient=tk.HORIZONTAL)
        self.hsb.grid(row=1, column=0, sticky='ew')
        self.canvas = tk.Canvas(self.outer, highlightthickness=0, width=width, height=height)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.outer.rowconfigure(0, weight=1)
        self.outer.columnconfigure(0, weight=1)
        self.canvas['yscrollcommand'] = self.vsb.set
        self.canvas['xscrollcommand'] = self.hsb.set
        # mouse scroll does not seem to work with just "bind"; You have
        # to use "bind_all". Therefore to use multiple windows you have
        # to bind_all in the current widget
        self.canvas.bind("<Enter>", self._bind_mouse)
        self.canvas.bind("<Leave>", self._unbind_mouse)
        self.vsb['command'] = self.canvas.yview
        self.hsb['command'] = self.canvas.xview

        self.inner = tk.Frame(self.canvas)
        # pack the inner Frame into the Canvas with the topleft corner 4 pixels offset
        self.canvas.create_window(4, 4, window=self.inner, anchor='nw')
        self.inner.bind("<Configure>", self._on_frame_configure)

        self.outer_attr = set(dir(tk.Widget))

    def __getattr__(self, item):
        if item in self.outer_attr:
            # geometry attributes etc (eg pack, destroy, tkraise) are passed on to self.outer
            return getattr(self.outer, item)
        else:
            # all other attributes (_w, children, etc) are passed to self.inner
            return getattr(self.inner, item)

    def _on_frame_configure(self, event=None):
        x1, y1, x2, y2 = self.canvas.bbox("all")
        height = self.canvas.winfo_height()
        width = self.canvas.winfo_width()
        self.canvas.config(scrollregion=(0, 0, max(x2, width), max(y2, height)))

    def _bind_mouse(self, event=None):
        self.canvas.bind_all("<4>", self._on_mousewheel)
        self.canvas.bind_all("<5>", self._on_mousewheel)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse(self, event=None):
        self.canvas.unbind_all("<4>")
        self.canvas.unbind_all("<5>")
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        pfuncanvas.draw()
        func = self.canvas.xview_scroll if event.state & 1 else self.canvas.yview_scroll
        if event.num == 4 or event.delta > 0:
            func(-1, "units")
        elif event.num == 5 or event.delta < 0:
            func(1, "units")

    def __str__(self):
        return str(self.outer)


#  **** SCROLL BAR TEST *****
root = tk.Tk()
root.title("Riemann Sum Calculator - Shivam")
root.state("zoomed")
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=1)

# use the Scrolled Frame just like any other Frame
frame = DoubleScrolledFrame(canvas)
# frame.grid(column=0, row=0, sticky='nsew') # fixed size
frame.pack(fill="both", expand=1)  # fill window

functionframe = tk.Frame(frame)
functionlabel = tk.Label(functionframe, text="Function: ")
functionbox = tk.Entry(functionframe)
pframe = tk.Label(functionframe)

functionframe.pack()
functionlabel.grid(row=0, column=0)
functionbox.grid(row=0, column=1)
pframe.grid(row=0, column=2)
plabel = tk.Label(pframe)
pfig = pltfig.Figure(figsize=(3, 1))
pax = pfig.add_subplot(111)
pfuncanvas = FigureCanvasTkAgg(pfig, master=pframe, )
pfuncanvas.draw()
pfuncanvas.get_tk_widget().pack()
pfuncanvas._tkcanvas.pack()
pax.get_xaxis().set_visible(False)
pax.get_yaxis().set_visible(False)


def ppack(event):
    global plabel
    global pax
    global pfuncanvas
    try:
        pfunc = sympy.parse_expr(functionbox.get().replace("^", "**") + event.char,
                                 transformations=(sympy.parsing.sympy_parser.standard_transformations +
                                                  (sympy.parsing.sympy_parser.implicit_multiplication_application,))).subs("e", sympy.exp(1))
        latexfunc = f"${sympy.latex(pfunc)}$"
        pax.clear()
        pax.text(0.2, 0.5, latexfunc, fontsize=15)
        pfuncanvas.draw()
    except:
        pass


endpointframe = tk.LabelFrame(frame, text="Endpoints", padx=5, pady=5)
startlabel = tk.Label(endpointframe, text="Start point:")
startbox = tk.Entry(endpointframe)
endlabel = tk.Label(endpointframe, text="End point:")
endbox = tk.Entry(endpointframe)

endpointframe.pack(pady=5)
startlabel.grid(row=0, column=0)
startbox.grid(row=0, column=1)
endlabel.grid(row=1, column=0)
endbox.grid(row=1, column=1)

subframe = tk.Frame(frame)
sublabel = tk.Label(subframe, text="Number of subintervals:")
subbox = tk.Entry(subframe)

subframe.pack(pady=5)
sublabel.grid(row=0, column=0)
subbox.grid(row=0, column=1)

radioframe = tk.Frame(frame)
radioframe.pack()

typeframe = tk.LabelFrame(radioframe, text="Sum type")
rietypes = [
    ("Left", "left"),
    ("Midpoint", "midpoint"),
    ("Right", "right"),
]
rietype = tk.StringVar()
rietype.set("left")

for name, value in rietypes:
    tk.Radiobutton(typeframe, text=name, variable=rietype, value=value).pack(anchor="w")
typeframe.grid(row=0, column=0)

workdformat = tk.BooleanVar()
workfformat = tk.BooleanVar()
workframe = tk.LabelFrame(radioframe, text="Show work format")
workdecimal = tk.Checkbutton(workframe, text="Decimal", variable=workdformat, onvalue=True, offvalue=False)
workfraction = tk.Checkbutton(workframe, text="Fraction", variable=workfformat, onvalue=True, offvalue=False)
workdformat.set(value=True)
workfformat.set(value=True)

workframe.grid(row=0, column=1, padx=5)
workdecimal.pack()
workfraction.pack()

calculateframe = tk.Frame(frame)
calculateframe.pack()

workpasteframe = tk.Frame(frame)
workpasteframe.pack()


def enterpress(event):
    calculate()


def calculate():
    global pfuncanvas
    global prettyframe
    global canvas
    global workpasteframe
    if workdformat.get() == True and workfformat.get() == True:
        tempwork = "df"
    elif workdformat.get() == True and workfformat.get() == False:
        tempwork = "d"
    elif workdformat.get() == False and workfformat.get() == True:
        tempwork = "f"
    else:
        tempwork = "n"
    global rie
    rie = Riemann(functionbox.get().replace("^", "**"), startbox.get(), endbox.get(), subbox.get(), rietype.get(),
                  tempwork)
    workpasteframe.destroy()
    workpasteframe = tk.Frame(frame)
    workpasteframe.pack()
    plotload = Image.open(rie.plotpath)
    plotrender = ImageTk.PhotoImage(plotload)
    plotimage = tk.Label(workpasteframe, image=plotrender)
    plotimage.image = plotrender
    plotimage.grid(row=0, column=0)
    workload = Image.open(rie.workpath)
    workrender = ImageTk.PhotoImage(workload)
    workimage = tk.Label(workpasteframe, image=workrender)
    workimage.image = workrender
    workimage.grid(row=1, column=0, pady=5)
    canvas.focus_set()
    pfuncanvas.draw()
    os.remove(rie.plotpath)
    os.remove(rie.workpath)


functionbox.focus_set()
canvas.bind("<1>", lambda event: canvas.focus_set())
subbox.bind("<Return>", enterpress)
functionbox.bind("<Key>", ppack)
canvas.bind("<Left>", lambda event: canvas.xview_scroll(-1, "units"))
canvas.bind("<Right>", lambda event: canvas.xview_scroll(1, "units"))
canvas.bind("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
canvas.bind("<Down>", lambda event: canvas.yview_scroll(1, "units"))
calculatebutton = tk.Button(calculateframe, text="Calculate!", command=calculate)
calculatebutton.pack()
calculatebutton.pack(pady=10)
workpasteframe.pack()


root.mainloop()
