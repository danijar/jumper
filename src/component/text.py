class Text(object):
	def __init__(self, evaluate=lambda: ''):
		self.evaluate = evaluate
		self.content = ''
