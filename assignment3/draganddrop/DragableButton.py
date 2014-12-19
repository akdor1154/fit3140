'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''


from DragNDropWidget import DragNDropWidget
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.uix.button import Button
import copy


dropZones = []

"""
class DragableButton(Button, DragNDropWidget):
    '''
    classdocs
    '''
    def __init__(self, **kw):
        '''
        Constructor
        '''
        #Button.__init__(self, **kw)
        super(DragableButton, self).__init__(**kw)
        self.size_hint = (None, None)

    def __deepcopy__(self, dumb):
        return DragableButton(text=self.text,
                              droppable_zone_objects=self.droppable_zone_objects,
                              bound_zone_objects=self.bound_zone_objects,
                              drag_opacity=self.drag_opacity,
                              drop_func=self.drop_func,
                              remove_on_drag=self.remove_on_drag)
"""     

class FArgument(Widget):
    def __init__(self, text, **kwargs):
        super(self.__class__,self).__init__(**kwargs)
        self.width = 80
        self.height = 50
        self.label = Label(text=text)
        with self.canvas:
            Color(0.6,0.4,0.4)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.add_widget(self.label)
        
    def on_size(self, instance, value):
        self.bg.size = self.size
        
    def on_pos(self, instance, value):
        self.bg.pos = self.pos
        self.label.pos = self.pos
        
        
    
class FName(Widget):
    def __init__(self, text, **kwargs):
        super(self.__class__,self).__init__(**kwargs)
        self.width = 80
        self.height = 80
        self.label = Label(text=text)
        with self.canvas:
            Color(0.4,0.4,0.4)
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.add_widget(self.label)
        
    
    def on_size(self, instance, value):
        self.bg.size = self.size
        
    def on_pos(self, instance, value):
        self.bg.pos = self.pos
        self.label.pos = self.pos
       
     
    
class DragableLayout(BoxLayout, DragNDropWidget):
    '''
    classdocs
    '''
    def __init__(self, **kw):
        '''
        Constructor
        '''
        #Button.__init__(self, **kw)
        super(DragableLayout, self).__init__(**kw)
        self.size_hint = (None, None)
        self.droppable_zone_objects = dropZones
        self.mainLayout = BoxLayout(orientation="vertical")
        self.add_widget(self.mainLayout)
        
        self.drop_func = self.replaceWidget
        
        print (self.parent, "<<<<<<<<<<<PARENT")
        
    def makeFunction(self, functionName, nArgs):
        functionName = FName(text=str(functionName))
        
        self.mainLayout.add_widget(functionName)
        for _ in range(nArgs):
            l = FArgument(text="drop arguments here")
            dropZones.append(l)
            #with l.canvas:
            #    Rectangle(pos=l.pos, size=l.size, color=(0,0,1))
            self.mainLayout.add_widget(l)
            
    def replaceWidget(self):
        '''
        '''
        print (self.lastDroppedZone, "<<ZONE")
        print (self.lastDroppedZone.parent, "<<ZONEPARENT")

        argumentToReplace = self.lastDroppedZone
        fBlockParent = argumentToReplace.parent
        
        indexOfArgument = fBlockParent.children.index(argumentToReplace)
        fBlockParent.remove_widget(argumentToReplace)
        self.parent.remove_widget(self)
        fBlockParent.add_widget(self, index=indexOfArgument)
        
        

        #self.size_hint = (2,2)    
        #self.canvas.ask_update
        #self.parent.canvas.ask_update
        
        #self.do_layout()
        
    def __deepcopy__(self, dumb):
        return DragableLayout(droppable_zone_objects=self.droppable_zone_objects,
                              bound_zone_objects=self.bound_zone_objects,
                              drag_opacity=self.drag_opacity,
                              drop_func=self.drop_func,
                              remove_on_drag=self.remove_on_drag)
