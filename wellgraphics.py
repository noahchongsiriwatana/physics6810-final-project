# Module for well application components.

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class WellPlot:
	def __init__(self):
		self.figure = Figure(figsize=(6, 6), dpi=100)
		self.plot = figure.add_subplot(1, 1, 1)


class WellUI:
	def __init__(self):
		# Creates window.
		self.window = tk.Tk()
		# Creates title.
		self.frm_title = tk.Frame()
		self.lbl_title = tk.Label(master=self.frm_title, text="2d Particle in a Box Simulation")
		self.lbl_title.pack()
		# Creates plot.
		self.frm_plot = tk.Frame()
		# Packs frames and initializes window.
		self.frm_title.pack()
		self.window.mainloop()
