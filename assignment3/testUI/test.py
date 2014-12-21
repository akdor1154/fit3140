#!/usr/bin/env python2

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.uix.label import Label
from kivy.properties import NumericProperty, OptionProperty, VariableListProperty
from kivy.graphics import *

from pdb import set_trace


from DragNDropWidget import DragNDropWidget

class FArgument(Widget):
	def __init__(self, text="__", **kwargs):
		self.name = text
		super(self.__class__,self).__init__(**kwargs)
		with self.canvas:
			Color(0.6,0.4,0.4)
			self.bg = Rectangle(size=self.size, pos=self.pos)
		self.label = Label(text=self.name, padding=[-FLayout.blockIndent, 0], valign="middle")
		self.add_widget(self.label)
		self.bind(size=self.redoLayout, pos=self.redoLayout)
		
	def redoLayout(self, instance, value):
		self.bg.size = self.size
		self.label.size = self.size
		self.label.text_size = self.size
		
		self.bg.pos = self.pos
		self.label.pos = self.pos
		
	
	def __repr__(self):
		return self.name
		
	
class FName(Widget):
	def __init__(self, text, **kwargs):
		self.name = text
		super(self.__class__,self).__init__(**kwargs)
		with self.canvas:
			Color(0.4,0.4,0.4, 0.4)
			self.bg = Rectangle(size=self.size, pos=self.pos)
		self.label = Label(text=self.name, padding=[-FLayout.blockIndent, 0])
		self.add_widget(self.label)
		self.bind(size=self.redoLayout, pos=self.redoLayout)
		
	
	def redoLayout(self, instance, value):
		self.bg.pos = (self.pos[0], self.pos[1]-(self.parent.calculateHeight()-self.height))
		self.bg.size = (self.parent.calculateWidth(), self.parent.calculateHeight())
		self.label.size = self.size
		self.label.text_size = self.size
		
		self.bg.pos = (self.pos[0], self.pos[1]-(self.parent.calculateHeight()-self.height))
		self.label.pos = self.pos
		

	def __repr__(self):
		return self.name
		
class FLayout(Layout, DragNDropWidget):
	'''Box layout class. See module documentation for more information.
	'''

	droppable_zone_objects = []
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

	def __init__(self, fNameString=None, fArgStrings=[], numArgs=0, **kwargs):
		self.neededWidthCache = None
		self.neededHeightCache = None
		self.fName = None
		self.fArgs = []
		super(FLayout, self).__init__(**kwargs)
		self.bind(
			spacing=self._trigger_layout,
			padding=self._trigger_layout,
			children=self._update_children,
			parent=self._trigger_layout,
			size=self._trigger_layout,
			pos=self._trigger_layout
		)
			
		if fNameString:
			self.add_widget(FName(fNameString))
		
		if numArgs and fArgStrings and numArgs < len(fArgStrings):
			raise ValueError('you passed more arguments that you said your function could take')
		
		self.numArgs = max(numArgs, len(fArgStrings))
		for i in range(self.numArgs):
			try:
				self.fArgs.append(FArgument(fArgStrings[i]))
			except ValueError:
				self.fArgs.append(FArgument())
				
		map(lambda x: self.add_widget(x, forceAdd=True), self.fArgs)
				
		self.drop_func = self.replaceWidget
		
	def __repr__(self):
		return repr(self.fName)+'('+','.join(map(repr,self.fArgs))+')'
		
	def isRoot(self):
		try:
			return self.parent.__class__ is not FLayout
		except AttributeError:
			return True
			
	def getRootFLayouts(self):
		try: return [widget for widget in self.get_root_window().children if widget.__class__ is FLayout]
		except AttributeError: return []
			
	def getRootFLayout(self): #yay recursion
		return self if self.isRoot else self.parent.getRootFLayout()
	
	def _update_children(self, instance, value):
		self._invalidateSizeCache()
		self._trigger_layout(instance, value)
		self.updateDropZones()
		
	def updateDropZones(self):
		#"Functional programming can be concise, logical, and easy-to-read" -- someone who didn't read the next line
		FLayout.droppable_zone_objects = reduce(lambda listOfDropZones, rootFLayout: listOfDropZones+rootFLayout._getDropZones(), self.getRootFLayouts(), [])

				
	def _getDropZones(self):
		dropZones = []
		for child in self.children:
			if (
				(child.__class__ is FName and not self.isRoot())
			or
				(child.__class__ is FArgument)
			):
				dropZones.append(child)
			elif child.__class__ is FLayout:
				dropZones += child._getDropZones()
		return dropZones
				
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
			else:
				raise Exception("tried to add a ",child.__class__,"to an FLayout")
			
			
			childX = selfx + padding_left
			childY = selfy + y
			
			
			if child.__class__ in (FLayout, FArgument):
				childX += self.blockIndent

			child.x = childX
			child.y = childY
			if child.__class__ is not FLayout:
				child.width = childWidth
			child.height = childHeight
			y += childHeight + spacing
		
		try:
			self.parent.do_layout()
		except AttributeError:
			pass
			
		self.width = self.calculateWidth()
		self.height = self.calculateHeight()


	def calculateHeight(self):
		if self.neededHeightCache is None:
			neededHeight = 0
			for child in self.children:
				if child.__class__ is FLayout:
					neededHeight += child.calculateHeight()
				elif child.__class__ is FName:
					neededHeight += self.nameHeight
				elif child.__class__ is FArgument:
					neededHeight += self.argHeight
			self.neededHeightCache = neededHeight
		return self.neededHeightCache
		
	def calculateWidth(self):
		if self.neededWidthCache is None:
			neededWidths = []
			for child in self.children:
				if child.__class__ is FLayout:
					neededWidths.append(self.blockIndent+child.calculateWidth())
				elif child.__class__ is FName:
					neededWidths.append(self.blockIndent+self.blockWidth)
				elif child.__class__ is FArgument:
					neededWidths.append(self.blockIndent+self.blockWidth)
			self.neededWidthCache = max(neededWidths)
		return self.neededWidthCache
		
	def _invalidateSizeCache(self):
		self.neededHeightCache = None
		self.neededWidthCache = None
		try:
			self.parent._invalidateSizeCache()
		except AttributeError:
			pass
	
	def replaceArgument(self, argToAdd, argToReplace):
		self.fArgs[self.fArgs.index(argToReplace)] = argToAdd
		childrenIndex = self.children.index(argToReplace)
		self.remove_widget(argToReplace, forceRemove=True)
		self.add_widget(argToAdd, childrenIndex, forceAdd=True)
	
	def add_widget(self, widget, index=0, forceAdd=False):
		if widget.__class__ is FName:
			if self.fName:
				self.remove_widget(self.fName)
			self.fName = widget
			index = -1
		elif isinstance(widget, (FArgument, FLayout)):
			if not forceAdd:
				raise ValueError('you can\'t manually add/remove arguments. Use replaceArgument instead!')
		widget.bind(pos_hint=self._trigger_layout)
		self._invalidateSizeCache()
		return super(FLayout, self).add_widget(widget, index)

	def remove_widget(self, widget, forceRemove=False):
		if widget.__class__ is FName:
			self.fName = None
		elif isinstance(widget, FArgument):
			if not forceRemove:
				raise ValueError('you can\'t manually add/remove arguments. Use replaceArgument instead!')
		elif isinstance(widget, FLayout):
			if not forceRemove:
				return self.replaceArgument(FArgument(), widget)
		widget.unbind(
			pos_hint=self._trigger_layout)
		self._invalidateSizeCache()
		return super(FLayout, self).remove_widget(widget)
	
		
	def setName(self):
		#TODO:
		pass
		
	def addArgument(self):
		#TODO:
		pass
		
	def on_touch_down(self, touch):

		if self.fName and self.fName.collide_point(touch.x, touch.y): #we only handle the touch if it's over our Name. Making the Name object handle the touch itself
														#might seem more sensible but I promise it's not. :)
			if not self.isRoot():
				print("need to deparent and stuff")
			else:
				print("I AM ROOT")
				
			DragNDropWidget.on_touch_down(self, touch)
		else:
			#this make the touch bubble to some other widget. maybe touch.bubble() would be a less retarded syntax, Kivy folks?
			return Widget.on_touch_down(self, touch)
	
	def replaceWidget(self, widgetToReplace):
		
		if widgetToReplace.__class__ is FName:
			if widgetToReplace.parent.isRoot():
				raise Exception('tried to replace the root layout, this should be impossible as it shouldn\'t be a drop target')
			widgetToReplace = widgetToReplace.parent
			
		if widgetToReplace.__class__ in (FArgument, FLayout):
			fBlockParent = widgetToReplace.parent
			
			#nonetype has no parent??????????????
			
			
			self.parent.remove_widget(self)
			fBlockParent.replaceArgument(self, widgetToReplace)

        

if __name__ == '__main__':
	class TestApp(App):
		def build(self):
			
			fTest = FLayout("hello()", ["arg1", "arg2"], pos=(50,50))
			
			fSubTest = FLayout("subfunctionlonglonglong", ["arg1_1", "arg1_2", "arg1_3"])
			
			fSubSubTest = FLayout("subsubfunc()", ["arg3_1", "arg3_2", "arg3_3"])
			
			fSubTest.replaceArgument(fSubSubTest, fSubTest.fArgs[1])
			
			fTest.replaceArgument(fSubTest, fTest.fArgs[0])
			
			
			print("fTest is root: ",fTest.isRoot())
			print("fSubTest is root: ",fSubTest.isRoot())
			print("fSubSubTest is root: ",fSubSubTest.isRoot())
			
			print("root layouts:", fSubTest.getRootFLayouts())
			
			
			return fTest
	
	TestApp().run()
	

	