# Module for well application components.

import re
import math
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import patches

class WellPlot:
	def __init__(self, window):
		self.window = window
		self.figure = Figure(figsize=(6, 6), dpi=100)
		self.plot = self.figure.add_subplot(1, 1, 1)
		self.canvas = FigureCanvasTkAgg(self.figure, window)
		self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

	def replot(self, a, b, energy_level):
		#self.plot.plot(a, b, color="red", marker="o", linestyle="")
		self.plot.clear()
		self.plot.set_title("Probability Density, a=" + str(a) + ", b=" + str(b) + ", n=" + str(energy_level))
		self.bounds = patches.Ellipse((0, 0), 2*a, 2*b, edgecolor='black', facecolor='none')
		self.plot.add_patch(self.bounds)
		bound = WellPlot.find_bound(a, b)
		self.plot.set_xlim([-bound, bound])
		self.plot.set_ylim([-bound, bound])
		self.canvas.draw()
		#self.canvas = FigureCanvasTkAgg(self.figure, self.window)
		#self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

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
		self.energy_level = 0
		# Creates window.
		self.window = tk.Tk()
		# Creates title.
		self.frm_title = tk.Frame()
		self.lbl_title = tk.Label(master=self.frm_title, text="2d Particle in a Box Simulation", font=WellUI.title_font)
		self.lbl_title.pack()
		# Creates plot.
		self.plot_canvas = WellPlot(self.window)
		# Creates ui for ellipse parameters.
		self.frm_ellipse = tk.Frame(borderwidth=2, relief="solid")
		self.lbl_eqn = tk.Label(master=self.frm_ellipse, text="(x/a)^2 + (y/b)^2 = 1", font=WellUI.plain_font)
		self.lbl_eqn.pack()
		# Creates entry fields.
		self.a_entry = tk.Entry(master=self.frm_ellipse)
		self.b_entry = tk.Entry(master=self.frm_ellipse)
		self.level_slider = tk.Scale(
			master=self.frm_ellipse,
			from_=0,
			to=10,
			orient=tk.HORIZONTAL,
			command=self.apply_params
		)
		self.lbl_a = tk.Label(master=self.frm_ellipse, text="Enter a:")
		self.lbl_b = tk.Label(master=self.frm_ellipse, text="Enter b:")
		self.lbl_level = tk.Label(master=self.frm_ellipse, text="Set energy:")
		self.lbl_a.pack()
		self.a_entry.pack()
		self.lbl_b.pack()
		self.b_entry.pack()
		self.lbl_level.pack()
		self.level_slider.pack()
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
		self.energy_level = self.level_slider.get()
		self.a_entry.delete(0, tk.END)
		self.b_entry.delete(0, tk.END)
		self.plot_canvas.replot(self.a, self.b, self.energy_level)

	# Static Methods.
	@staticmethod
	def to_float(s):
		val = 0
		finds = re.findall(r"[-+]?\d*\.\d+|\d+", s)
		if len(finds) > 0:
			val = float(finds[0])
		return val
