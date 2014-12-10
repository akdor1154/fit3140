import kivy.app

class FIT3140App(kivy.app.App):
	def build(self):
		return FIT3140UI()

if __name__ == '__main__':
	FIT3140App().run()
	