# Module for well application components.

import re
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class WellPlot:
	def __init__(self, window):
		self.figure = Figure(figsize=(6, 6), dpi=100)
		self.plot = self.figure.add_subplot(1, 1, 1)
		self.canvas = FigureCanvasTkAgg(self.figure, window)
		self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


class WellUI:
	# Class variables.
	title_font = "Helvetica 18 bold"
	plain_font = "Helvetica 16"
	
	def __init__(self):
		# Initial parameters.
		self.a = 1
		self.b = 1
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
		self.lbl_a = tk.Label(master=self.frm_ellipse, text="Enter a:")
		self.lbl_b = tk.Label(master=self.frm_ellipse, text="Enter b:")
		self.lbl_a.pack()
		self.a_entry.pack()
		self.lbl_b.pack()
		self.b_entry.pack()
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

	def apply_params(self):
		self.a = WellUI.to_float(self.a_entry.get())
		self.b = WellUI.to_float(self.b_entry.get())
		print(self.a)
		print(self.b)
		self.a_entry.delete(0, tk.END)
		self.b_entry.delete(0, tk.END)
	
	# Static Methods.
	@staticmethod
	def to_float(s):
		val = 0
		finds = re.findall(r"[-+]?\d*\.\d+|\d+", s)
		if len(finds) > 0:
			val = float(finds[0])
		return val
