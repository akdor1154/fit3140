from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
#import DragableButton  # import to get auto register
from DragableButton import DragableLayout#, DragableButton
"""
kv = '''
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'cannot drag here'
    BoxLayout:
        id: from_box
        DragableButton:
            text: 'Drag me!!!'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            drop_func: app.greet

        DragableButton:
            text: 'Drag me!!!'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            remove_on_drag: False
            drop_func: app.greet

        DragableButton:
            text: 'Drag me!!!'
            bound_zone_objects: [from_box, to_box ]
            droppable_zone_objects: [to_box, ]
            drag_opacity: .5
            drop_func: app.greet
    Label:
        id: to_box
        text: 'grad here for some effect'
'''
"""

class MyPaintApp(App):
    def build(self):
        #return Builder.load_string(kv)
        codeSpace = BoxLayout(orientation="vertical")
        for n in range(3):
            x = DragableLayout()
            x.makeFunction(n, 2)
            x.bound_zone_objects.append(codeSpace)
            codeSpace.add_widget(x)
        return codeSpace
    def greet(self):
        print "Dragging done!!!"

if __name__ == '__main__':
    MyPaintApp().run()
