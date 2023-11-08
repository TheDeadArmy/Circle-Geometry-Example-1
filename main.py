from renderer import *
from model import *
import pygame as pg
	
pg.init()

class Main:
	def __init__(self):
		self.bounds = (800, 600)
		#delta time
		self.model = Model(self)
		self.renderer = Renderer(self)

	def pg_events_manager(self):
		for e in pg.event.get():
			if e.type == pg.QUIT:
				pg.quit()
				self.running = False

	def tick(self):
		pos = pg.mouse.get_pos()
		pos = [pos[0], pos[1]]
		pos[0] -= self.bounds[0] / 2
		pos[1] -= self.bounds[1] / 2
		# pos = (-500, 0)
		self.model.UpdateModel(pos)

	def run(self):
		self.running = True
		while self.running:
			self.renderer.clear()
			self.tick()
			self.renderer.render_all()
			self.pg_events_manager()

main = Main()
main.run()