#!/usr/bin/env python2

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from kivy.properties import NumericProperty, OptionProperty, VariableListProperty
from kivy.graphics import *

class FArgument(Widget):
	def __init__(self, text, **kwargs):
		super(self.__class__,self).__init__(**kwargs)
		with self.canvas:
			Color(0.6,0.4,0.4)
			self.bg = Rectangle(size=self.size, pos=self.pos)
		self.label = Label(text=text, padding=[-FLayout.blockIndent, 0], valign="middle")
		self.add_widget(self.label)
		self.bind(size=self.on_size, pos=self.on_pos)
		
	def on_size(self, instance, value):
		self.bg.size = self.size
		self.label.size = self.size
		self.label.text_size = self.size
		
	def on_pos(self, instance, value):
		self.bg.pos = self.pos
		self.label.pos = self.pos
		
		
	
class FName(Widget):
	def __init__(self, text, **kwargs):
		super(self.__class__,self).__init__(**kwargs)
		with self.canvas:
			Color(0.4,0.4,0.4)
			self.bg = Rectangle(size=self.size, pos=self.pos)
		self.label = Label(text=text, padding=[-FLayout.blockIndent, 0])
		self.add_widget(self.label)
		self.bind(size=self.on_size, pos=self.on_pos)
		
	
	def on_size(self, instance, value):
		self.bg.pos = (self.pos[0], self.pos[1]-(self.parent.calculateHeight()-self.height))
		self.bg.size = (self.parent.calculateWidth(), self.parent.calculateHeight())
		self.label.size = self.size
		self.label.text_size = self.size
		
	def on_pos(self, instance, value):
		self.bg.pos = (self.pos[0], self.pos[1]-(self.parent.calculateHeight()-self.height))
		self.label.pos = self.pos



class FLayout(Layout):
	'''Box layout class. See module documentation for more information.
	'''

	nameHeight = 50
	argHeight = nameHeight
	blockWidth = 100
	blockIndent = 10

	spacing = NumericProperty(0)
	'''Spacing between children, in pixels.

	:data:`spacing` is a :class:`~kivy.properties.NumericProperty`, default to
	0.
	'''

	padding = VariableListProperty([0, 0, 0, 0])
	'''Padding between layout box and children: [padding_left, padding_top,
	padding_right, padding_bottom].

	padding also accepts a two argument form [padding_horizontal,
	padding_vertical] and a one argument form [padding].

	.. versionchanged:: 1.7.0

	Replaced NumericProperty with VariableListProperty.

	:data:`padding` is a :class:`~kivy.properties.VariableListProperty`, default to
	[0, 0, 0, 0].

	'''

	def __init__(self, fName=None, fArgs=[], **kwargs):
		super(FLayout, self).__init__(**kwargs)
		self.bind(
			spacing=self._trigger_layout,
			padding=self._trigger_layout,
			children=self._trigger_layout,
			parent=self._trigger_layout,
			size=self._trigger_layout,
			pos=self._trigger_layout)
			
		if fName:
			self.add_widget(FName(fName))
		
		if fArgs:
			for arg in fArgs:
				self.add_widget(FArgument(arg))

	def do_layout(self, *largs):
		# optimize layout by preventing looking at the same attribute in a loop
		len_children = len(self.children)
		if len_children == 0:
			return
		selfx = self.x
		selfy = self.y
		selfw = self.width
		selfh = self.height
		padding_left = self.padding[0]
		padding_top = self.padding[1]
		padding_right = self.padding[2]
		padding_bottom = self.padding[3]
		spacing = self.spacing
		padding_x = padding_left + padding_right
		padding_y = padding_top + padding_bottom


		y = padding_bottom
		
		for child in self.children:
			
			if child.__class__ is FLayout:
				childHeight = child.calculateHeight()
			elif child.__class__ is FName:
				childWidth = self.calculateWidth()
				childHeight = self.nameHeight
			elif child.__class__ is FArgument:
				childWidth = self.calculateWidth()-self.blockIndent
				childHeight = self.argHeight
				
			
			
			childX = selfx + padding_left
			childY = selfy + y
			
			
			if child.__class__ in (FLayout, FArgument):
				childX += self.blockIndent

			child.x = childX
			child.y = childY
			child.width = childWidth
			child.height = childHeight
			y += childHeight + spacing


	def calculateHeight(self):
		neededHeight = 0
		for child in self.children:
			if child.__class__ is FLayout:
				neededHeight += child.calculateHeight()
			elif child.__class__ is FName:
				neededHeight += self.nameHeight
			elif child.__class__ is FArgument:
				neededHeight += self.argHeight
		return neededHeight
		
	def calculateWidth(self):
		neededWidths = []
		for child in self.children:
			if child.__class__ is FLayout:
				neededWidths.append(self.blockIndent+child.calculateWidth())
			elif child.__class__ is FName:
				neededWidths.append(self.blockIndent+self.blockWidth)
			elif child.__class__ is FArgument:
				neededWidths.append(self.blockIndent+self.blockWidth)
		return max(neededWidths)
		pass
		
	def add_widget(self, widget, index=0):
		widget.bind(
			pos_hint=self._trigger_layout)
		return super(FLayout, self).add_widget(widget, index)

	def remove_widget(self, widget):
		widget.unbind(
			pos_hint=self._trigger_layout)
		return super(FLayout, self).remove_widget(widget)

	def setName(self):
		#TODO:
		pass
		
	def addArgument(self):
		#TODO:
		pass

if __name__ == '__main__':
	class TestApp(App):
		def build(self):
			fTest = FLayout(orientation="vertical", pos=(50,50))
			
			fSubTest = FLayout()
			
			fSubSubTest = FLayout("subsubfunc()", ["arg3_1", "arg3_2", "arg3_3"])
			
			fSubTest.add_widget(FName("subfunctionlonglonglong()"))
			fSubTest.add_widget(FArgument("arg1_1"))
			fSubTest.add_widget(fSubSubTest)
			fSubTest.add_widget(FArgument("arg2_3"))
			
			fTest.add_widget(FName("hello()"))
			
			fTest.add_widget(fSubTest)
			fTest.add_widget(FArgument("arg2"))
			
			
			
			return fTest
		
	TestApp().run()
	

	