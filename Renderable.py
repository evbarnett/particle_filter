class Renderable(object):
	"""An object that can be rendered"""
	def __init__(self):
		pass

	def render(self, window, square_width):
		raise NotImplementedError
		