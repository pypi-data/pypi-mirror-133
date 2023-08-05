from vinca.lib import ansi
from vinca.lib.terminal import LineWrapOff, AlternateScreen
from vinca.lib.readkey import readkey, keys
from vinca.generators import generators_dict

FRAME_WIDTH = 6

class Browser():
	quit_keys = ('q', keys.ESC)
	move_keys = ('j','k',keys.DOWN, keys.UP)

	def __init__(self, cardlist):
		self.cardlist = cardlist
		self.reviewing = False
		self.sel = 0
		self.frame = 0

	@property
	def N(self):
		return len(self.cardlist)

	@property
	def selected_card(self):
		return self.cardlist[self.sel]

	@property
	def visible_lines(self):
		return min(self.N, FRAME_WIDTH) + (self.status_bar is not None)

	
	@property
	def status_bar(self):
		if not self.N > FRAME_WIDTH:
			return None
		return ansi.codes['light'] + f'{self.sel} of {self.N}' + ansi.codes['reset']


	def draw_browser(self):
		ansi.hide_cursor()
		with LineWrapOff():
			if self.status_bar:
				print(self.status_bar)
			for i, card in enumerate(self.cardlist[self.frame:self.frame+FRAME_WIDTH], start=self.frame):
				if card.is_due:
					ansi.blue()
				if card.deleted:
					ansi.red()
				if i==self.sel:
					ansi.highlight()
				print(card)
				ansi.reset()

	def clear_browser(self):
		ansi.up_line(self.visible_lines)
		ansi.clear_to_end()

	def close_browser(self):
		self.clear_browser()
		ansi.show_cursor()
		exit()

	def redraw_browser(self):
		self.clear_browser()
		self.draw_browser()
		
	def move(self, key):
		if key in ('j',keys.DOWN) and self.sel < self.N - 1:
			self.move_down()
		if key in ('k',keys.UP) and self.sel > 0:
			self.move_up()

	def move_down(self):
		self.sel += 1
		# scroll down if we are off the screen
		self.frame += (self.frame + FRAME_WIDTH == self.sel)  
	
	def move_up(self):
		self.sel -= 1
		# scroll down if we are off the screen
		self.frame -= (self.frame - 1 == self.sel)  

	def review(self):
		self.reviewing = True
		self.browse()
	
	def browse(self):
		if not self.cardlist:
			print('no cards')
			return
		self.draw_browser()
		while True:

			# if we are in reviewing mode continue on to the next due card
			if self.reviewing:
				if self.selected_card.is_due:
					self.selected_card.review()
					self.selected_card.schedule()
					if self.selected_card.history.last_grade == 'exit':
						self.reviewing = False
				while not self.selected_card.is_due:
					self.move_down()
					if self.sel >= self.N - 1:
						self.close_browser()
				self.redraw_browser()
				continue

			if not self.reviewing:
				k = readkey()
				if k == 'R':
					self.reviewing = True

			if k in self.quit_keys:
				self.close_browser()

			if k in self.move_keys:
				self.move(k)

				
			if command := self.selected_card._hotkeys.get(k):
				with AlternateScreen():
					command()
					if command in self.selected_card._confirm_exit_commands:
						print('\npress any key to continue')
						readkey()

			if generator := generators_dict.get(k):
				with AlternateScreen():
					new_card = generator()
					self.cardlist._insert_card(self.sel, new_card)
				ansi.down_line()
				if self.N == FRAME_WIDTH + 1:
					ansi.down_line()

			self.redraw_browser()




