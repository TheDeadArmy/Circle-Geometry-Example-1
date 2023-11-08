import pygame as pg

class Renderer:
	def __init__(self, main):
		self.main = main
		self.screen = pg.display.set_mode(main.bounds)
		self.origin = (int(main.bounds[0] / 2), int(main.bounds[1] / 2))
		self.screen_colour = (255, 255, 255)
	
	def DrawCircle(self, circle):
		position = (circle.position[0] + self.origin[0], circle.position[1] + self.origin[1])
		pg.draw.circle(self.screen, "black", position, circle.radius, 1)

	def DrawLine(self, v1, v2):
		v1 = (v1[0] + self.origin[0], v1[1] + self.origin[1])
		v2 = (v2[0] + self.origin[0], v2[1] + self.origin[1])
		pg.draw.line(self.screen, "black", v1, v2, 2)

	def clear(self):
		self.screen.fill(self.screen_colour)

	def render_all(self):
		# render calls go here
		pg.display.update()
