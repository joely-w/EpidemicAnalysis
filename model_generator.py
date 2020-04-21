# Import interface libraries
from tkinter import *
from tkinter import filedialog
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import subprocess
# Import mathematical libraries
import scipy.optimize as opt
import numpy as np
import pandas as pd

matplotlib.use("TkAgg")
matplotlib.rcParams['toolbar'] = 'None'


# Create template logistic curve
def logistic(time, a_const, b_const, c_const):
    return c_const / (1 + a_const * np.exp(-time * b_const))


class Generator:
    filename = ""
    a = 0
    b = 0
    c = 0
    percentage_error = 0
    t = None
    n = None
    entry = None
    graph_canv = None
    green_canvas = None
    orange_canvas = None

    def __init__(self):

        self.window = Tk()
        self.window.title("Model Generator")
        self.window.geometry("800x1000")

        self.lbl = Label(self.window, text="Model Generator", font=("Arial Bold", 25), bg="#415a5f", fg="white",
                         padx=200,
                         pady=20)
        self.lbl.pack()

        self.canvas = Canvas(width=675, height=300, bg='#369693')
        self.canvas.pack()

        self.btn = Button(self.canvas, text="Select CSV File", command=self.open_file)
        self.btn.place(y=75, x=150)

        self.csv_lbl = Message(self.canvas,
                               text="File should have columns:\n Time - Days since start of disease \n Cases - Number "
                                    "of cases on particular day", width="200px", bg="#369693", fg="white")
        self.csv_lbl.place(y=75, x=350)

        self.generate_btn = Button(self.window, text="Generate model", command=self.generate_model, padx=15, pady=15,
                                   bg="#ce6664", fg="white")
        self.generate_btn.place(y=500, x=350)

        self.window.mainloop()

    # Generate model from data
    def generate_model(self):

        # Read processes data
        dataset = pd.read_csv(self.filename)
        dataset = dataset['Cases']
        dataset = dataset.reset_index(drop=False)
        dataset.columns = ["Time", "Cases"]

        # Set initial model data
        initial = np.random.exponential(size=3)
        bounds = (0, [100000., 3., 1000000000.])
        self.t = np.array(dataset['Time'])
        self.n = np.array(dataset['Cases'])

        # Run a curve fit using logistic function
        (a, b, c), cov = opt.curve_fit(logistic, self.t, self.n, bounds=bounds, p0=initial)
        self.a = a
        self.b = b
        self.c = c

        # Declare variable to store sum of errors
        sum_of_errors = int(0)

        # Record sum of percentage errors
        for i in range(len(self.t) - 1):
            error = abs((int(self.n[i]) - int(self.initialised_logistic(i))) / int(self.n[i]))
            sum_of_errors += error

        # Store average percentage error
        self.percentage_error = sum_of_errors / len(self.n)
        self.graph_results()

    # Create logistic model using found values
    def initialised_logistic(self, time):
        # Return logistic function using constants previously calculate
        return self.c / (1 + self.a * np.exp(-time * self.b))

    # Open CSV file dialogue
    def open_file(self):
        rep = filedialog.askopenfilenames(
            parent=self.window,
            initialdir='./',
            initialfile='processed.csv',
            filetypes=[
                ("CSV", "*.csv")])
        try:
            self.filename = rep[0]
        except IndexError:
            return False

    def calc_cases(self, time):
        number_cases = math.floor(self.c / (1 + self.a * math.exp(-int(time) * self.b)))
        case_lbl = Label(self.green_canvas, text="Number of cases " + str(number_cases))
        case_lbl.pack()

    def calc_time(self, cases):
        cases = int(cases)
        time_val = math.ceil(math.log(((cases * self.a) / (self.c - cases)) ** (1 / self.b)))
        case_lbl = Label(self.orange_canvas,
                         text="Day at which disease has " + str(cases) + " cases: " + str(
                             time_val) + " days into disease")
        case_lbl.pack()

    def graph_results(self):
        printable_equation = "N = (" + str(self.c) + ")/(1+" + str(self.a) + "*e^(-" + str(self.c) + "*t))"
        math_fig = Figure(figsize=(4, 0.5), dpi=100)
        math_graph = math_fig.add_subplot(1, 1, 1)

        expression = "N = \\frac{" + str(self.c) + "}{1+" + str(self.a) + "\\times{\\exp(-" + str(
            self.c) + "\\times{t})}}"
        math_graph.axis('off')
        math_graph.plot()
        math_graph.text(0, 0.5, '$%s$' % expression)
        math_canvas = FigureCanvasTkAgg(math_fig, self.window)

        math_canvas.get_tk_widget().pack()

        figure = Figure(figsize=(5, 4), dpi=100)
        graph = figure.add_subplot(1, 1, 1)

        # Plot logistic function with new constants
        graph.plot(self.t, self.initialised_logistic(self.t))

        # Plot scatter graph of actual data
        graph.scatter(self.t, self.n, color="red", linewidths=0.00001)

        # Set labels for graph
        graph.set_title("Global logistics curve")
        graph.set_ylabel('Infections')
        graph.set_xlabel('Time (days)')

        # Destroy previous menu
        self.lbl.config(text="Generated Model")
        self.csv_lbl.destroy()
        self.generate_btn.destroy()
        self.canvas.destroy()
        self.graph_canv = Canvas(self.window)
        self.graph_canv.pack()
        canvas = FigureCanvasTkAgg(figure, self.graph_canv)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        copy_graph = Button(self.window, text="Copy raw text equation",
                            command=lambda: self.copy_to_clipboard(printable_equation))
        copy_graph.place(x=350, y=600)
        copy_tex = Button(self.window, text="Copy latex equation",
                          command=lambda: self.copy_to_clipboard(expression))
        copy_tex.place(x=350, y=650)
        self.green_canvas = Canvas(self.window, width=600)
        self.green_canvas.place(x=600, y=600)
        case_time = Label(self.green_canvas, text="Enter time in days")
        case_time.pack()
        case_time_entry = Entry(self.green_canvas)
        case_time_entry.pack()
        case_time_calc = Button(self.green_canvas, text="Calculate number of cases",
                                command=lambda: self.calc_cases(case_time_entry.get()))
        case_time_calc.pack()
        self.orange_canvas = Canvas(self.window, width=600)
        self.orange_canvas.place(x=150, y=600)
        time_case = Label(self.orange_canvas, text="Enter number of cases")
        time_case.pack()
        time_case_entry = Entry(self.orange_canvas)
        time_case_entry.pack()
        time_case_calc = Button(self.orange_canvas, text="Calculate time taken",
                                command=lambda: self.calc_time(time_case_entry.get()))
        time_case_calc.pack()

    def copy_to_clipboard(self, text):
        self.window.clipboard_clear()
        self.window.clipboard_append(text)
        self.window.update()


Generator()
