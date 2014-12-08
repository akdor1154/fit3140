#!/usr/bin/env python2

# Almost all of the Lispy code has been taken unashamedly from Peter Norvig
# at http://norvig.com/lispy.html. 

import __future__

def tokenize(lispyString):
    "Read a lispy statement into a list of tokens"
    return lispyString.replace('(',' ( ').replace(')', ' ) ').split()
    
def parse(lispyString):
    return buildTree(tokenize(lispyString))

def buildTree(tokens):
    if len(tokens) == 0:
        raise SyntaxError('buildTree called on an empty list')
    token = tokens.pop(0)
    if token == '(':
        branch = []
        while tokens[0] != ')':
            branch.append(buildTree(tokens))
        tokens.pop(0) # drop the end )
        return branch
    elif token == ')':
        raise SyntaxError('got a ) without a (')
    else:
        return atom(token)

Symbol = str          # A Scheme Symbol is implemented as a Python str
List   = list         # A Scheme List is implemented as a Python list
Number = (int, float) # A Scheme Number is implemented as a Python int or float
Env    = dict         #

def atom(token):
    "read a non-bracket into an atom"
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)
            
            

class Procedure(object):
    def __init__(self, parameters, body, env):
        self.parameters, self.body, self.env = parameters, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parameters, args, self.env))

class Env(dict):
    def __init__(self, parameters=(), args=(), parent=None):
        self.update(zip(parameters, args))
        self.parent = parent
    #the given code raises a silly exception, this works better because it lets our UI handle it
    #instead of the user's console crashing when they make a typo.
    def find(self, var):
        if (var in self):
            return self
        elif self.parent is not None:
            return self.parent.find(var)
        else:
            raise NameError(var+' is not defined in the current Lispy environment')
        
program = "(begin (define r 10) (* pi (* r r)))"

def build_global_env():
    import math, operator as op
    env = Env()
    env.update(vars(math))
    env.update({
        'add':op.add, 'subtract':op.sub, 'multiply':op.mul, 'divide':op.div, 
        'lessthan':op.gt, 'greaterthan':op.lt, 'equals':op.eq, 'modulus':op.mod,
		'comment': lambda x: pass
		'move':    pass
		'turn':	   lambda x: pass
		'detect-wall': pass,
		'detect-goal': pass,
        'begin':   lambda *x: x[-1],
    })
    return env

global_env = build_global_env()

def eval(tree, env=global_env):
    "evaluate some Lispy in a given environment"
    if isinstance(tree, Symbol):
        return env.find(tree)[tree]
    elif not isinstance(tree, List):
        return tree
    elif tree[0] == 'if':
        (_, test, consequence, alternative) = tree
        exp = (consequence if eval(test, env) else alternative)
        return eval(exp, env)
    elif tree[0] == 'set':
        (_, var, exp) = tree
        env[var] = eval(exp, env)
    elif tree[0] == 'define':
        (_, parameters, body) = tree
        return Procedure(parameters, body, env)
    else:
        head = eval(tree[0], env)
        args = [eval(arg, env) for arg in tree[1:]]
        return head(*args)

def repl(prompt='> '):
    while True:
        val = eval(parse(raw_input(prompt)))
        if val is not None:
            print(treeToString(val))

def treeToString(tree):
    if isinstance(tree, list):
        return '(' + ' '.join(map(treeToString,tree))+')'
    else:
        return str(tree)


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button

class SemiMultilineTextInput(TextInput):
    '''
    I want behaviour whereby the user can have both multiline input and easy keyboard access to the
    'evaluate' functionality. This quick override of the TextInput class allows that.
    I opted to 'bolt on' to the existing functions (calling them with super) instead of
    copy-pasting and editing them, for both brevity and (hopefully) compatibility with multiple Kivy   
    versions.
    '''
    
    def __init__(self, shiftNewline=True, **kwargs):
        super(SemiMultilineTextInput, self).__init__(**kwargs)
        self.multiline = True
        self.shiftNewline = shiftNewline
        self.shiftDown = None
        
    def _key_down(self, key, repeat=False):
        displayed_str, internal_str, internal_action, scale = key
        if internal_action in ('shift', 'shift_L', 'shift_R'):
            self.shiftDown = True
        elif internal_action == 'enter':
            if self.shiftNewline:
                if self.shiftDown:
                    self.insert_text('\n')
                else:
                    self.dispatch('on_text_validate')
            else:
                if self.shiftDown:
                    self.dispatch('on_text_validate')
                else:
                    self.insert_text('\n')
             #stop TextInput's _key_down from handling Enter
            key = (displayed_str, internal_str, 'fakefakefake', scale)
        super(SemiMultilineTextInput, self)._key_down(key, repeat)
    
    def _key_up(self, key, repeat=False):
        displayed_str, internal_str, internal_action, scale = key
        if internal_action in ('shift', 'shift_L', 'shift_R'):
            self.shiftDown = False
        super(SemiMultilineTextInput, self)._key_up(key, repeat)

def appendToText(textInput, textToAppend, withNewline=True):
    nl = '\n' if withNewline else ''
    textInput.text = textInput.text+textToAppend+nl

class LispyUI(BoxLayout):
    def __init__(self, **kwargs):
        super(LispyUI, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.lispyInput = SemiMultilineTextInput(hint_text = 'Your input (type in here!)')
        self.lispyInput.bind(on_text_validate=lambda x: self.runFromInput())
        self.lispyOutput = TextInput(multiline=True, readonly=True, hint_text = 'Output and Input History')
        self.controls = BoxLayout(orientation='horizontal')
        
        #the user may wish to use this as either a console or as a text editor with bonus eval button.
        #this checkbox lets them switch this behaviour.
        self.shiftCheckbox = CheckBox()
        self.shiftCheckboxLabelGroup = BoxLayout(orientation='vertical')
        self.shiftCheckboxLabelHeader = Label(text="[b]Shift+Enter for newline[/b]", markup=True)
        self.shiftCheckboxLabelDescription = Label()
        self.shiftNewlineOnText = "Shift+Enter makes a newline, Enter evaluates"
        self.shiftNewlineOffText = "Shift+Enter evaluates, Enter makes a newline"
        self.shiftCheckboxLabelGroup.add_widget(self.shiftCheckboxLabelHeader)
        self.shiftCheckboxLabelGroup.add_widget(self.shiftCheckboxLabelDescription)
        
        #link the checkbox to the shiftNewline property of lispyInput
        self.shiftCheckbox.bind(active=self.checkShiftNewline)
        self.shiftCheckbox.active = self.lispyInput.shiftNewline
        self.checkShiftNewline(self.shiftCheckbox, self.shiftCheckbox.active)
        
        self.runButton = Button(text="Evaluate!")
        self.runButton.bind(on_press=lambda x: self.runFromInput())
        
        self.shiftCheckbox.size_hint = (None, 1)
        self.runButton.size_hint = (None, 1)
        self.runButton.width = 300
        
        self.shiftCheckboxLabelGroup.size_hint = (3, 1)
        
        self.controls.height = 60
        self.controls.size_hint = (1, None)
        
        self.controls.add_widget(self.shiftCheckbox)
        self.controls.add_widget(self.shiftCheckboxLabelGroup)
        self.controls.add_widget(self.runButton)
        
        self.add_widget(self.lispyInput)
        self.add_widget(self.controls)
        self.add_widget(self.lispyOutput)
        
    def checkShiftNewline(self, checkbox, value):
        self.lispyInput.shiftNewline = value
        self.shiftCheckboxLabelDescription.text = self.shiftNewlineOnText if value else self.shiftNewlineOffText
    
        
    def runFromInput(self):
        lispyString = self.lispyInput.text
        for line in lispyString.split('\n'):
            if len(line) <= 0:
                continue
            appendToText(self.lispyOutput, line+':')
            try:
                value = eval(parse(line))
            except (SyntaxError, AttributeError, NameError) as e:
                appendToText(self.lispyOutput, 'ERROR: '+str(e))
                return
            if value is not None:
                appendToText(self.lispyOutput, '  '+treeToString(value))
        self.lispyInput.text = ''
        

class LispyApp(App):
    def build(self):
        return LispyUI()

LispyApp().run()
