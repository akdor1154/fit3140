

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from fcode import fTree, fBlock



class codeSpace(App):


    def build(self):
        self.layout = BoxLayout()# the place to put palette and workspace
        
        self.tree = fTree()#for now there will be only one tree (will change in next version)
        
        self.workspace = BoxLayout(orientation="vertical", size_hint=(1, .9))#will contain a 'begin' button and label
        self.beginButton = Button(text="Begin", size_hint=(1, .1))#run the tree
        
        self.beginButton.bind(on_press=self.runProgram)
        
        self.code = Label()#code is just being shown as text for now, will change in the next version
        self.workspace.add_widget(self.code)
        self.workspace.add_widget(self.beginButton)
        
        self.layout.add_widget(self.palette())
        self.layout.add_widget(self.workspace)
        
        return self.layout
    
    #def workSpacePH(self):
    #    self.code = Label()
    
    def runProgram(self, button):
        try:
            self.code.text = "result= \n" + str(self.tree.execute())
        except:
            self.tree.execute()
    def addBlock(self, button):
        a = fBlock(button.text, self.arguments[0].text, self.arguments[1].text, self.arguments[2].text, self.arguments[3].text, self.arguments[4].text)
        self.tree.addBlock(a)
        self.code.text += "\n" + str(a.code)
        
    
    def palette(self):
        self.x = BoxLayout(orientation="vertical")
        
        argumentSection = BoxLayout()
        
        self.arguments = [TextInput(),TextInput(),TextInput(),TextInput(),TextInput()]
        for a in self.arguments:
            argumentSection.add_widget(a)
            
        
        self.turnButton = Button(text="turn")
        self.moveButton = Button(text="move")
        self.detectWallButton = Button(text="detect-wall")
        self.detectGoalButton = Button(text="detect-goal")
        self.addButton = Button(text="add")
        self.subButton = Button(text="subtract")
        self.multButton = Button(text="multiply")
        self.divButton = Button(text="divide")
        self.modButton = Button(text="modulus")
        self.equButton = Button(text="equals")
        self.lessButton = Button(text="lessthan")
        self.greatButton = Button(text="greaterthan")
        #self.defButton = Button(text="Define")
        
        
        self.turnButton.bind(on_press=self.addBlock)
        self.moveButton.bind(on_press=self.addBlock)
        self.detectWallButton.bind(on_press=self.addBlock)
        self.detectGoalButton.bind(on_press=self.addBlock)
        self.addButton.bind(on_press=self.addBlock)
        self.subButton.bind(on_press=self.addBlock)
        self.multButton.bind(on_press=self.addBlock)
        self.divButton.bind(on_press=self.addBlock)
        self.modButton.bind(on_press=self.addBlock)
        self.equButton.bind(on_press=self.addBlock)
        self.lessButton.bind(on_press=self.addBlock)
        self.greatButton.bind(on_press=self.addBlock)
        #self.defButton.bind(on_press=self.addBlock)
        
        
        
        self.x.add_widget(argumentSection)
        
        self.x.add_widget(self.turnButton)
        self.x.add_widget(self.moveButton)
        self.x.add_widget(self.detectWallButton)
        self.x.add_widget(self.detectGoalButton)
        self.x.add_widget(self.addButton)
        self.x.add_widget(self.subButton)
        self.x.add_widget(self.multButton)
        self.x.add_widget(self.divButton)
        self.x.add_widget(self.modButton)
        self.x.add_widget(self.equButton)
        self.x.add_widget(self.lessButton)
        self.x.add_widget(self.greatButton)
        #self.x.add_widget(self.defButton)
        
        return self.x
        
x = codeSpace()
x.run()