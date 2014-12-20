'''
Created on Oct 24, 2012

@author: Pavel Kostelnik
'''


from DragNDropWidget import DragNDropWidget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import copy



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
    dropZones = []
    def __init__(self, **kw):
        '''
        Constructor
        '''
        #Button.__init__(self, **kw)
        super(DragableLayout, self).__init__(**kw)
        self.size_hint = (None, None)
        self.droppable_zone_objects = DragableLayout.dropZones
        self.mainLayout = BoxLayout(orientation="vertical", padding=[10,0,0,0])
        self.add_widget(self.mainLayout)
        
        self.set_remove_on_drag(False)
        
        self.drop_func = self.replaceWidget
        
        self.palette = False
        

    def makeFunction(self, FName, NArgs):
        self.mainLayout.add_widget(Button(text=str(FName)))
        
        self.FName = FName
        self.NArgs = NArgs
        
        
        for _ in range(NArgs):
            l = TextInput()
            DragableLayout.dropZones.append(l)
            self.mainLayout.add_widget(l)
            
    def replaceWidget(self):
        '''
        '''
        print (self.lastDroppedZone, "<<ZONE")
        print (self.lastDroppedZone.parent, "<<ZONEPARENT")

        argumentToReplace = self.lastDroppedZone
        fBlockParent = argumentToReplace.parent
        
        #nonetype has no parent??????????????
        
        indexOfArgument = fBlockParent.children.index(argumentToReplace)
        fBlockParent.remove_widget(argumentToReplace)
        self.parent.remove_widget(self)
        fBlockParent.add_widget(self, index=indexOfArgument)
        self.size_hint = (1, 3)
        
        p = self.parent
        mult = 1
        while (p is not None):
            try:
                PH = p.size_hint
                if not ((PH[0] is None) or (PH[1] is None)):
                        p.size_hint = (PH[0]+(PH[0]*mult), PH[1]+(PH[1]*mult))
                p = p.parent
                mult = mult * 0.25
            except:
                break
        
        
        
        self.parent.canvas.ask_update
        self.canvas.ask_update
        
    
    def updateDropZones(self):
        self.droppable_zone_objects = DragableLayout.dropZones
        
    def __deepcopy__(self, dumb):
        DL = DragableLayout(droppable_zone_objects=DragableLayout.dropZones,
                              bound_zone_objects=self.bound_zone_objects,
                              drag_opacity=self.drag_opacity,
                              drop_func=self.drop_func,
                              remove_on_drag=True)
        DL.makeFunction(self.FName, self.NArgs)
        #DL.set_remove_on_drag(False)
        print DL.remove_on_drag, "rod"
        
        return DL
