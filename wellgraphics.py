# Module for well application components.

import re
import math
import tkinter as tk
import matplotlib
import seaborn as sns
import WellSolver
import pandas
import pathlib
import numpy
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import patches

class WellPlot:
	def __init__(self, window, a, b, energy_level_1, energy_level_2, n):
		self.a = a
		self.b = b
		self.n = n
		self.energy_level_1 = energy_level_1
		self.energy_level_2 = energy_level_2
		self.window = window
		self.figure = Figure(figsize=(6, 6), dpi=100)
		self.plot = self.figure.add_subplot(2, 1, 1)
		self.density_plot = self.figure.add_subplot(2, 1, 2)
		self.canvas = FigureCanvasTkAgg(self.figure, window)
		self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	def replot(self, a, b, energy_level_1, energy_level_2):
		self.a = a
		self.b = b
		self.energy_level_1 = energy_level_1
		self.energy_level_2 = energy_level_2
		self.plot.clear()
		self.density_plot.clear()
		self.plot.set_title("Probability Density, a=" + str(a) + ", b=" + str(b) + ", n1,n2=" + str(energy_level_1) + "," + str(energy_level_2))
		self.bounds = patches.Ellipse((0, 0), 2*a, 2*b, edgecolor='black', facecolor='none')
		self.plot.add_patch(self.bounds)
		bound = WellPlot.find_bound(a, b)
		self.plot.set_xlim([-bound, bound])
		self.plot.set_ylim([-bound, bound])
		self.plot_density()
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	def plot_density(self):
		x = self.a * numpy.random.normal(size=self.n)
		y = x * self.b + numpy.random.normal(size=self.n)
		data = WellSolver.solve(self.a, self.b, int(self.n), int(self.energy_level_1), int(self.energy_level_2))
		data = numpy.copy(numpy.transpose(data))
		x = data[0]
		y = data[1]
		self.density_plot.hist2d(x, y, bins=(100, 100), cmap=matplotlib.pyplot.cm.jet)
		#self.plot.plot(x, y, 's')

	@staticmethod
	def find_bound(a, b):
		high = max(a, b)
		return 1.1*high

class WellUI:
	# Class variables.
	title_font = "Helvetica 18 bold"
	plain_font = "Helvetica 16"
	
	def __init__(self):
		# Initial parameters.
		self.a = 1
		self.b = 1
		self.energy_level_n1 = 1
		self.energy_level_n2 = 0
		self.resolution = 100000;
		# Creates window.
		self.window = tk.Tk()
		# Creates title.
		self.frm_title = tk.Frame()
		self.lbl_title = tk.Label(master=self.frm_title, text="2d Particle in a Box Simulation", font=WellUI.title_font)
		self.lbl_title.pack()
		# Creates plot.
		self.plot_canvas = WellPlot(self.window, self.a, self.b, self.energy_level_n1, self.energy_level_n2, self.resolution)
		# Creates ui for ellipse parameters.
		self.frm_ellipse = tk.Frame(borderwidth=2, relief="solid")
		self.lbl_eqn = tk.Label(master=self.frm_ellipse, text="(x/a)^2 + (y/b)^2 = 1", font=WellUI.plain_font)
		self.lbl_eqn.pack()
		# Creates entry fields.
		self.a_entry = tk.Entry(master=self.frm_ellipse)
		self.b_entry = tk.Entry(master=self.frm_ellipse)
		self.level_slider_n1 = tk.Scale(
			master=self.frm_ellipse,
			from_= 1,
			to= 5,
			orient=tk.HORIZONTAL,
			command=self.apply_energy
		)
		self.level_slider_n2 = tk.Scale(
			master=self.frm_ellipse,
			from_= 0,
			to= 5,
			orient=tk.HORIZONTAL,
			command=self.apply_energy
		)
		self.lbl_a = tk.Label(master=self.frm_ellipse, text="Enter a:")
		self.lbl_b = tk.Label(master=self.frm_ellipse, text="Enter b:")
		self.lbl_level_n1 = tk.Label(master=self.frm_ellipse, text="Set 1st Energy:")
		self.lbl_level_n2 = tk.Label(master=self.frm_ellipse, text="Set 2nd Energy:")
		self.lbl_a.pack()
		self.a_entry.pack()
		self.lbl_b.pack()
		self.b_entry.pack()
		self.lbl_level_n1.pack()
		self.level_slider_n1.pack()
		self.lbl_level_n2.pack()
		self.level_slider_n2.pack()
		# Creates submit button.
		self.frm_submit = tk.Frame()
		self.btn_submit = tk.Button(
			master=self.frm_submit,
			text="APPLY",
			command=self.apply_params
		)
		self.btn_submit.pack()
		# Packs frames and initializes window.
		self.frm_title.pack()
		self.frm_ellipse.pack()
		self.frm_submit.pack()
		self.window.mainloop()

	def apply_params(self, energy_level=0):
		self.a = max(1, WellUI.to_float(self.a_entry.get()))
		self.b = max(1, WellUI.to_float(self.b_entry.get()))
		higher = max(self.a, self.b)
		lower = min(self.a, self.b)
		self.a = higher
		self.b = lower
		self.energy_level_n1 = self.level_slider_n1.get()
		self.energy_level_n2 = self.level_slider_n2.get()
		self.a_entry.delete(0, tk.END)
		self.b_entry.delete(0, tk.END)
		self.plot_canvas.replot(self.a, self.b, self.energy_level_n1, self.energy_level_n2)

	def apply_energy(self, energy_level):
		self.energy_level_n1 = self.level_slider_n1.get()
		self.energy_level_n2 = self.level_slider_n2.get()
		self.plot_canvas.replot(self.a, self.b, self.energy_level_n1, self.energy_level_n2)

	# Static Methods.
	@staticmethod
	def to_float(s):
		val = 0
		finds = re.findall(r"[-+]?\d*\.\d+|\d+", s)
		if len(finds) > 0:
			val = float(finds[0])
		return val
