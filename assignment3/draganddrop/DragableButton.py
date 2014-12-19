'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''


from DragNDropWidget import DragNDropWidget
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
        
    def makeFunction(self, FName, Nargs):
        self.mainLayout.add_widget(Button(text=str(FName)))
        for _ in range(Nargs):
            l = Button(text="drop arguments here")
            dropZones.append(l)
            #with l.canvas:
            #    Rectangle(pos=l.pos, size=l.size, color=(0,0,1))
            self.mainLayout.add_widget(l)
            
    def replaceWidget(self):
        '''
        '''
        print (self.lastDroppedZone, "<<ZONE")
        print (self.lastDroppedZone.parent, "<<ZONEPARENT")
        '''
        self.lastDroppedZone.parent.remove_widget(self.lastDroppedZone)
        self.lastDroppedZone.parent.add_widget(self)
        '''
        y = self.lastDroppedZone
        x = y.parent
        
        
        w = []
        for widget in x.children[:]:
            #print widget
            if widget is y:
                #new = copy.deepcopy(self)
                new = DragableLayout()
                for child in self.children[:]:
                    child.parent.remove_widget(child)
                    new.add_widget(child)
                #self.parent.remove_widget(self)
                w.append(new)
            else:
                w.append(widget)
        x.clear_widgets()
        #print w, "before"
        while w:
            x.add_widget(w.pop())
        #print w, "after"
        
        print new, new.children, self
        #print self.parent.children
        """print x, "x"
        print y, "y"
        print x.children, "xChildren"
        print "vvchild childrenvv"
        for child in x.children:
            if child.children:
                print child.children
                print child.children[0].children
        """
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
