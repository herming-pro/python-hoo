class main():
    def info(self):
        colors = ['white', 'black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
        sty = {
            # Label
            "TLabel":{
                "configure":{
                    "anchor":"center",
                    "font":('Helvetica',9),
                }
            },
            "l.TLabel":{
                "configure":{
                    # "relief":'ridge',
                    "anchor":"w",
                    "font":('Helvetica',9),
                }
            },
            "TRadiobutton":{
                "configure":{
                    "font":('Helvetica',12),
                    "relief":'ridge',
                },
            }
        }
        # Label
        sty.update(
            {
                color+".TLabel":{
                    "configure":{
                        "background":color,
                    }
                } for color in colors
            }
        )
        # Frame
        sty.update(
            {
                color+".TFrame":{
                    "configure":{
                        "background":color,
                    }
                } for color in colors
            }
        )
        return sty 
    def insdevset(self):
        sty = {
            "TNotebook":{
                "configure": {
                    "tabmargins": [2, 5, 2, 0],
                    "background":"#3e4345",
                    'relief':'flat'
                            }
                },
            "TNotebook.Tab": {
                "configure": {
                    "padding": [5, 1],
                    "background": '#4d5255',
                    "foreground":"#989b9d",
                    'font':('PingFangTCRegular',15,"")
                    },
                "map":{
                    "background": [("selected", '#5e6366')],
                    "foreground": [("selected", '#61edf2')],
                    "expand": [("selected", [1, 1, 1, 0])]
                    }
                },
            'TLabel':{
                "configure": {
                    'background':'#5e6366',
                    'relief':"flat",
                    'foreground':"#d1d4d4",
                    'border':"0",
                    'font':('Arial',10,""),
                    'anchor':'center'
                    }
                },
            'TLabelframe':{
                "configure": {
                    'background':'#4d5255'
                    }
                },
            'TLabelframe.Label':{
                "configure": {
                    'foreground':'#61edf2',
                    'background':'#4d5255',
                    'bordercolor':'#5e6366',
                    'borderwidth ':'1',
                    'font':('Arial',12,"")
                    }
                },
            'com.TLabelframe':{
                "configure": {
                    'background':'#3e4345',
                    'bordercolor':'#d1d4d4',
                    'borderwidth':'1',
                    'labelmargins':'0',
                    'labeloutside':True,
                    'relief':'solid'
                    }
                },
            'fist.TLabelframe':{
                "configure": {
                    'background':'#5e6366',
                    'bordercolor':'#d1d4d4',
                    'borderwidth':'1',
                    'labelmargins':'0',
                    'labeloutside':True,
                    'relief':'solid'
                    }
                },
            'com.TLabelframe.Label':{
                "configure": {
                    'foreground':'#61edf2',
                    'background':'#3e4345',
                    'bordercolor':'#3e4345',
                    'borderwidth ':'0',
                    'font':('Arial',10,"")
                    }
                },
            'fist.TLabelframe.Label':{
                "configure": {
                    'foreground':'#61edf2',
                    'background':'#5e6366',
                    'bordercolor':'#5e6366',
                    'borderwidth ':'0',
                    'font':('Arial',10,"")
                    }
                },
            'TEntry':{
                "configure": {
                    'fieldbackground':'#313537',
                    'foreground':"#d1d4d4",
                    'relief':'flat',
                    'font':('Arial',15,"")
                    }
                },
            'TFrame':{
                "configure": {
                    'background':'#5e6366',
                    'foreground':"#61edf2",
                    'font':('Arial',15,"")
                    }
                },
            "TScrollbar":{
                "configure": {
                    'fieldbackground':"#313537",
                    'selectbackground':'#313537',
                    'background':'#313537',
                    'foreground':'#d1d4d4',
                    'arrowsize':'-10',
                    'arrowcolor':'#61edf2',
                    'relief':'flat',
                    'border':'0'
                    }
                },
            "TCombobox":{
                "configure": {
                    'fieldbackground':"#313537",
                    'selectbackground':'#313537',
                    'background':'#313537',
                    'foreground':'#d1d4d4',
                    'arrowsize':'25',
                    'arrowcolor':'#61edf2',
                    'relief':'flat',
                    'shiftrelief':"flat",
                    'border':'10',
                    'font':('Arial',15,"")
                    },
                'map':{
                    'arrowcolor':[('disabled','#313537'),('readonly','#61edf2')]
                }
                },
            "ComboboxPopdownFrame":{
                "configure": {
                    'font':('Arial',15,""),
                    'relief':'flat'
                    }
                },
            "TCheckbutton":{
                "configure": {
                    'compound':'None',
                    'background':'#4d5255',
                    'foreground':'#d1d4d4',
                    'indicatorcolor':'#313537',
                    'indicatorrelief':"flat",
                    'font':('Arial',12,"")
                    }
                },
            "TRadiobutton":{
                "configure": {
                    'compound':'None',
                    'background':'#4d5255',
                    'foreground':'#d1d4d4',
                    'indicatorcolor':'#313537',
                    'indicatorrelief':"flat",
                    'font':('Arial',12,"")
                    }
                },
            "RED.TLabel":{
                "configure": {
                    'font':('Arial',12,""),
                    'background':'#4d5255',
                    'relief':'flat',
                    'foreground':'#d1d4d4',
                    'border':"0"
                    }
                },
            "gee.TLabel":{
                "configure": {
                    'font':('Arial',12,""),
                    'background':'#3e4345',
                    'relief':'flat',
                    'foreground':'#d1d4d4',
                    'border':"0"
                    }
                },
            "blue.TLabel":{
                "configure": {
                    'font':('Arial',12,""),
                    'background':'#5e6366',
                    'relief':'flat',
                    'foreground':'#61edf2',
                    'border':"0"
                    }
                },
            "fist.TLabel":{
                "configure": {
                    'font':('Arial',12,""),
                    'background':'#313537',
                    'relief':'flat',
                    'foreground':'#d1d4d4',
                    'border':"0"
                    }
                },
            "TButton":{
                "configure": {
                    'background': "#61edf2", 
                    'foreground': "#313537",
                    'relief':'flat',
                    'anchor':'center'
                    },
                "map":{
                    'background': [('pressed', '!disabled', '#d1d4d4'),("disabled", "#d1d4d4")],
                    'foreground':[("disabled", "#313537")],
                    }
                },
            "TProgressbar":{
                "configure": {
                    'background': "#61edf2", 
                    'foreground': "#313537",
                    }
                }
            }
        return sty