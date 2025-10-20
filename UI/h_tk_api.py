import tkFileDialog
import tkMessageBox
import ttk as ttk
import Tkinter as tk
import copy as cp
import time

class main():
    def __init__(self,tk,oop,root):
        global tk_root 
        global oo
        self.API_version = "v0.0.1"
        self.tk_root = tk_root = root 
        self.tk = tk
        self.oo = oo = oop
        self.set_api_data()
        self.window_x   = 0
        self.window_y   = 0
        self.callback_data = []
    def init(self):
        pass
    def set_api_data(self,version = "",config_version = "",title = "" , Language = []):
        if version != "":
            self.version = version
        if config_version != "":
            self.config_version = config_version
        if title != "":
            self.title = title
        if Language != []:
            self.Language = Language[0]
            self.Language_callback = Language[1]
    def set_windows_size(self,window_x,window_y):
        self.window_y   =   window_y
        self.window_x   =   window_x
    def start(self):
        self.oo.Send('main','log','go')
        x = (self.tk_root.winfo_screenwidth()-self.window_x)/2
        y = (self.tk_root.winfo_screenheight()-self.window_y)/2
        self.tk_root.geometry('%sx%s+%s+%s'%(self.window_x,self.window_y,x,y))
        self.tk_root.minsize(self.window_x,self.window_y)
        #tk_root.update()
    def update(self):
        self.tk_root.update()
    ###自定義function###
    class FileDialog():
        def __init__(self,master=None,pattern='openname',*args,**kw):
            self.kw = kw
            # master - the window to place the dialog on top of
            # title - the title of the window
            # initialdir - the directory that the dialog starts in
            # initialfile - the file selected upon opening of the dialog
            # filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
            # defaultextension - default extension to append to file (save dialogs)
            # multiple - when true, selection of multiple items is allowed
            self.master = master
            self.pattern = pattern
            self.args = args
        def __call__(self):
            return {
                'directory':tkFileDialog.askdirectory,
                'openname':tkFileDialog.askopenfilename,
                'opennames':tkFileDialog.askopenfilenames,
                'open':tkFileDialog.askopenfile,
                'opens':tkFileDialog.askopenfiles,
                'save':tkFileDialog.asksaveasfile,
                'savename':tkFileDialog.asksaveasfilename,
            }.get(self.pattern,lambda *args,**kw:"")(parent=self.master,*self.args,**self.kw)
    class MessageBox():
        def __init__(self,master=None,pattern="info",*args,**kw):
            self.master = master
            self.pattern = pattern
            self.args = args
            self.kw = kw 
            # title
            # message
        def __call__(self):
            return {
                "okcancel":tkMessageBox.askokcancel,
                "question":tkMessageBox.askquestion,
                "retrycancel":tkMessageBox.askretrycancel,
                "yesnocancel":tkMessageBox.askyesnocancel,
                "yesno":tkMessageBox.askyesno,
                "error":tkMessageBox.showerror,
                "info":tkMessageBox.showinfo,
                "warning":tkMessageBox.showwarning,
            }.get(self.pattern,lambda *args,**kw:"")(parent=self.master,*self.args,**self.kw)
    class CustomizeMessageBox():
        def __init__(self,master=None,blank=False,height=50,fps=60,*args,**kw):
            global oo
            self.oo = oo
            self.res = None
            self.__blank = blank
            self.__period = 1./fps
            if 'grab' not in kw:
                kw['grab'] = True
            
            self.toplevel = main.Toplevel(master=master,*args,**kw)
            self.toplevel.state('withdrawn')
            if not self.__blank:
                self.height = height
                self.content = ttk.Frame(self.toplevel,style='white.TFrame')
                self.buttonFrame = ttk.Frame(self.toplevel,)
            
            self.__looper = {}
            self.updater(self.toplevel.update,60)
            self.__exitTask = []
        def __call__(self):
            self.toplevel.state('normal')
            
            if not self.__blank:
                self.content.place(relwidth=1,relheight=1,height=-self.height)
                self.buttonFrame.place(relwidth=1,rely=1,y=-self.height,height=self.height)
            
            self.__loop = True
            def leave(event):
                if event.widget == event.widget.winfo_toplevel():
                    self.__loop = False
                for task in self.__exitTask:
                    task()
            self.toplevel.bind('<Destroy>',lambda e: leave(e))
            
            t = time.time()
            while self.oo.running.isSet() and self.__loop:
                dt = time.time()-t
                if dt<self.__period:
                    time.sleep(self.__period-dt)
                else:
                    t = time.time()
                for task,(t0,period) in self.__looper.items():
                    t1 = time.time()
                    if t1-t0>period:
                        self.__looper[task][0] = t1
                        if task():
                            self.__looper.pop(task)
            
            return self.res
            
        def updater(self,func,fps=10):
            self.__looper[func] = [0,max(1./fps,1./120)]
        def ender(self,func):
            self.__exitTask.append(func)
    def button_check(self,data):pass
    def new_button(*args , **kw):
        print "please change name!"
    def Auto_text(self):
        self.Language_data = self.__Auto_text(self.Language,self.Language_callback)
        return self.Language_data
    def Language_change(self):
        self.Language_data.callback()
    class __Auto_text():
        def __init__(self,Language,callback):
            self.Language = Language
            self.__callback = callback
            self.__tk_dict = {}
            self.__tk_toplevel_dict = {}
            self.__tk_labelframe_dict = {}
            for name in self.Language.keys():
                    self.add(name)
        def add(self,name):
            self.__tk_dict[name]=tk.StringVar()
            self.__tk_dict.get(name,tk.StringVar()).set(self.Language.get(name))
        def remove(self,name):
            self.__tk_dict.pop(name)
        def get(self,name):
            return self.__tk_dict.get(name,tk.StringVar())
        def set_text(self,tkWidget,name):
            if tkWidget.__class__==main.Toplevel:
                tkWidget.title(self.Language.get(name))
                self.__tk_toplevel_dict[name]=tkWidget
            if tkWidget.__class__==main.LabelFrame:
                tkWidget.configure(text=self.Language.get(name))
                self.__tk_labelframe_dict[name]=tkWidget
        def set(self,name,str_data):
            self.__tk_dict.get(name,tk.StringVar()).set(self.Language.get(str_data))
        def swap(self,Language_name):
            self.Language.restart(Language_name)
            #self.callback()
            self.__callback()
        def callback(self):
            for key in self.__tk_dict.keys():
                self.__tk_dict[key].set(self.Language.get(key))
            for key in self.__tk_toplevel_dict:
                try:
                    self.__tk_toplevel_dict[key].title(self.Language.get(key))
                except:
                    pass
            for key in self.__tk_labelframe_dict:
                try:
                    self.__tk_labelframe_dict[key].configure(text=self.Language.get(key))
                except:
                    pass
    class Treeview(ttk.Treeview):
        #修改
        def set(self , name ,  data , nb = 0 ):
            for i in self.get_children():
                if self.item(i,"values")[nb] ==  name:
                    try:
                        self.item(i,values=data)
                    except:
                        return False
                    return True
            return False      
        #刪除
        def clean(self):
            items = self.get_children()
            [self.delete(item) for item in items] 
    class check_Toplevel():
        def __init__(self):
            self._window_Frame = False
        def set(self,data):
            self._window_Frame = data
        def get(self,):
            return self._window_Frame
        def swap(self):
            self._window_Frame = not(self._window_Frame)
            return self._window_Frame
    class Label(ttk.Label):pass
    def Button(self,master,tag="",args=[],kw={},img="",set_function =False,*button_args , **button_kw):
        button = ttk.Button(master,*button_args,**button_kw)
        if img!="":
            img=Image.open("./ico/%s.png"%img)
            photo = ImageTk.PhotoImage(img)#,relief=tk.GROOVE,bg="#5e6366",border="0"
            button.config(image=photo)
            button.image =photo
        if not set_function:
            set_function = self.button_check
        if 'command' not in button_kw:
            button.config(command=lambda:set_function(tag,*args,**kw))
        button.bind('<Return>', lambda e: button.invoke())
        return button
    #可擴充支援textvariable 參數
    class LabelFrame(ttk.LabelFrame):
        def __init__(self , master, textvariable = False ,*args , **kw):
            if textvariable:
                ttk.LabelFrame.__init__(self , master , *args, **kw)
                labelWidget = ttk.Label(self, textvariable=textvariable,style = self["style"]+".Label")
                self.configure( labelwidget = labelWidget)
            else:
                ttk.LabelFrame.__init__(self , master , *args, **kw)
    class Frame(ttk.Frame):pass
    class Progressbar(ttk.Progressbar):pass
    class Combobox(ttk.Combobox):
        def __init__(self, *args, **kw):
            ttk.Combobox.__init__(self, *args, **kw)
            self.bind("<Control-a>",self.__selectAll)
            self.bind("<Control-A>",self.__selectAll)
        def __selectAll(self,event):
            event.widget.select_range(0, 'end')
            event.widget.icursor('end')
            return 'break'
    class StringVar(tk.StringVar):pass
    class IntVar(tk.IntVar):pass
    class Notebook(ttk.Notebook):pass
    class Entry(ttk.Entry):
        def __init__(self, *args, **kw):
            ttk.Entry.__init__(self, *args, **kw)
            self.bind("<Control-a>",self.__selectAll)
            self.bind("<Control-A>",self.__selectAll)
        def __selectAll(self,event):
            event.widget.select_range(0, 'end')
            event.widget.icursor('end')
            return 'break'
    class Scrollbar(ttk.Scrollbar):pass
    class Radiobutton(ttk.Radiobutton):pass
    class PanedWindow(ttk.PanedWindow): pass
    class Style(ttk.Style):pass
    class Listbox(tk.Listbox):pass
    class Text(tk.Text):
        def __init__(self,*args,**kw):
            tk.Text.__init__(self,*args,**kw)
            self.bind('<Control-Shift-Z>',self.__redo)
            self.bind('<Control-Shift-z>',self.__redo)
            self.bind('<Control-a>',self.__selectAll)
            self.bind('<Control-A>',self.__selectAll)
            
        def __selectAll(self,event):
            event.widget.tag_add('sel','1.0','end')
            event.widget.mark_set('insert', 'end')
            event.widget.see('insert')
            return 'break'
            
        def __redo(self,event):
            try:
                event.widget.edit_redo()
            except:
                oo.Send('main','log',str(event.widget)+': no more redo')
            return 'break'
    class Menubutton(tk.Menubutton): pass
    class Menu(tk.Menu):pass
    class Spinbox(tk.Spinbox):pass  #旋轉框(可以點上點下的)
    class Scale(tk.Scale):pass      #拉條
    class FoldFrame(tk.Frame):#摺疊框?
        def __init__(self,master, *args, **kw):
            tk.Frame.__init__(self, master, *args, **kw) 
            self.size = {"relx":0,
                         "rely":0,
                         "relheight":0,
                         "relwidth":0,
                         "x":0,
                         "y":0,
                         "height":0,
                         "width":0,
                        }
        def place(**kw):
            for i in self.size.keys():
                if kw.get(i):
                    self.size[i] = kw[i]
                else:
                    self.size[i] = 0
            tk.Frame.place(self,**kw)       
    class Right_click_menu(tk.Menu):#右鍵點擊
        '''
        add_command(label="我的工作", command=lambda:self.button_cheak("a1_3")) --> 按鈕
        add_separator() --> ------
        '''
        def __init__(self,master, *args, **kw):
            tk.Menu.__init__(self, master, *args, **kw)
            master.bind("<Button-3>",self.click)
        def click(self,event):
            self.post(event.x_root, event.y_root)
    class Toplevel(tk.Toplevel):
        def __init__(self, master=None, toplevel_manager=None,size = "300x300",relsize = "0x0",grab=True, *args, **kw):
            global tk_root 
            self.grab = grab
            self.toplevel_manager = toplevel_manager
            if self.toplevel_manager:
                if self.toplevel_manager.get():
                    return
                self.toplevel_manager.set(True)
            tk.Toplevel.__init__(self, master, *args, **kw)
            self.resizable(0,0)
            self.set_position(size,relsize)
            if self.grab==True:
                self.grab_set()
            self.focus_set()
            
        def set_position(self, size, relsize):
            global tk_root 
            x = int(size.split("x")[0])
            y = int(size.split("x")[1])
            rex =   int(relsize.split("x")[0])
            rey =   int(relsize.split("x")[1])
            new_x = tk_root.winfo_x() + tk_root.winfo_width()  / 2 - x / 2 + rex
            new_y = tk_root.winfo_y() + tk_root.winfo_height() / 2 - y / 2 + rey
            self.geometry(size + "+" + str(new_x)+ "+" + str(new_y))  
        def destroy(self):
            global tk_root 
            if self.toplevel_manager:
                self.toplevel_manager.set(False)
            master = tk_root.nametowidget(self.winfo_parent())
            if master!=tk_root and master.grab:
                master.grab_set()
            tk.Toplevel.destroy(self)
    class VerticalScrolledText(tk.Frame):
        def __init__(self,master=None,title=None,undo=True,readonly=False, *args, **kw):
            tk.Frame.__init__(self, master, bg='#7b7b7b')
            
            default = {
                'font':("New Time Roman", 20),
                'undo':undo,
                'highlightthickness':1,
                'borderwidth':0,
                'highlightbackground':'#7b7b7b',
                'highlightcolor':'#1884da'
            }
            default.update(kw)
            kw = default
            self.font = kw['font']
            
            self.text = text = tk.Text(self, *args, **kw)
            self.vscrollbar = ttk.Scrollbar(self, orient='vertical')
            
            self.readonly = readonly
            if readonly:
                text.config(state='disabled',bg='#f0f0f0',highlightcolor='#7b7b7b')
            else:
                text.bind('<Control-Shift-Z>',self.redo)
                text.bind('<Control-Shift-z>',self.redo)
                text.bind('<Control-a>',self.selectAll)
                text.bind('<Control-A>',self.selectAll)
            
            text.xview_moveto(0)
            text.yview_moveto(0)
            self.vscrollbar.config(command=text.yview)
            text.config(yscrollcommand=self.vscrollbar.set)
            
            text.grid(column=1,row=1,sticky='news')
            self.vscrollbar.grid(column=2,row=1,sticky='news',padx=[0,1],pady=[1,1])
            
            self.columnconfigure(1,weight=1)
            self.columnconfigure(2,minsize=22)
            self.rowconfigure(1,weight=1)
            
            self.title = None
            if title:
                self.add_title(title)
            
            def _on_mousewheel(event):
                text.yview_scroll(-1 * (event.delta / 120), "units")
                return 'break'
            
            self.mouseIn = False
            def Enter(event):
                self.mouseIn = True
                if not readonly and text.focus_get()!=text:
                    text.config(highlightbackground='#2d2d2d')
                text.bind_all("<MouseWheel>", _on_mousewheel)
            self.bind('<Enter>', Enter)
            
            def Leave(event):
                self.mouseIn = False
                text.unbind_all("<MouseWheel>")
                if not readonly and text.focus_get()!=text:
                    text.config(highlightbackground='#7b7b7b')
            self.bind('<Leave>', Leave)
        def add_title(self,title):
            if self.title:
                self.title.destroy()
            else:
                self.text.grid(row=2)
                self.vscrollbar.grid(row=2)
                self.rowconfigure(1,weight=0)
                self.rowconfigure(2,weight=1)
            self.title = ttk.Label(self,font=self.font,textvariable=title)
            self.title.grid(column=1,columnspan=2,row=1,sticky='ew',padx=[1,1],pady=[1,0])
        def del_title(self,):
            if self.title:
                self.title.destroy()
                self.title = None
                self.text.grid(row=1)
                self.vscrollbar.grid(row=1)
                self.rowconfigure(1,weight=1)
                self.rowconfigure(2,weight=0)
        def selectAll(self,event):
            event.widget.tag_add('sel','1.0','end')
            event.widget.mark_set('insert', 'end')
            event.widget.see('insert')
            return 'break'
        def redo(self,event):
            try:
                event.widget.edit_redo()
            except:
                oo.Send('main','log',str(event.widget)+': no more redo')
            return 'break'
        def insert(self,index,text,*tags):
            if self.readonly:
                self.text.config(state='normal')
                res = self.text.insert(index, text, *tags)
                self.text.config(state='disabled')
                return res
            else:
                return self.text.insert(index,text,tags)
        def delete(self,index1,index2=None):
            if self.readonly:
                self.text.config(state='normal')
                res = self.text.delete(index1,index2)
                self.text.config(state='disabled')
                return res
            else:
                return self.text.delete(index1, index2=None)
        def see(self,index,checkmouse=True):
            if checkmouse and not self.mouseIn:
                return self.text.see(index)
    class VerticalScrolledFrame(ttk.Frame):
        def __init__(self, master, height = 30, *args, **kw):
            self.height = height
            
            ttk.Frame.__init__(self, master)            
            self.canvas = canvas = tk.Canvas(self,highlightthickness=0, *args, **kw)#,bg="white"
            vscrollbar = ttk.Scrollbar(self, orient='vertical')
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            vscrollbar.config(command=canvas.yview)
            canvas.config(yscrollcommand=vscrollbar.set)
            vscrollbar.place(relx =1,x=-20,relheight =1,width=20)
            canvas.place(relheight =1,relwidth =1,width=-20)
            
            self.interior = interior = tk.Frame(canvas,height=0)
            self.frame_list = []
            interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")
            def _configure_canvas(event):
                interior["width"] = int(canvas.winfo_width())
                return 'break'
            canvas.bind('<Configure>', _configure_canvas)
            
            def _configure_interior(event):
                size = (interior.winfo_width(), interior.winfo_height())
                canvas.config(scrollregion=(0,0,size[0],size[1]))
                return 'break'
            interior.bind('<Configure>', _configure_interior)
    
            def _on_mousewheel(event):
                if canvas.winfo_height() <= interior["height"]: 
                    canvas.yview_scroll(-1 * (event.delta / 120), "units")
                return 'break'
    
            def _bound_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
                return 'break'
            canvas.bind('<Enter>', _bound_to_mousewheel)
    
            def _unbound_to_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
                return 'break'
            canvas.bind('<Leave>', _unbound_to_mousewheel)
        def clean(self):
            for widget in self.interior.winfo_children():
                widget.destroy()  
            self.interior["height"] = self.height
            self.frame_list = []
            self.canvas.yview_moveto(0)
        def add_Title(self,height=None, *args, **kw):
            if height==None:
                height=self.height
            else:
                self.height=height
            self.title = ttk.Frame(self.canvas, *args, **kw)
            self.title.place(x =0,y=0,height =height,relwidth=1)
            self.interior["height"] += height
            return self.title
        def add_Frame(self,height,index=None, *args, **kw):
            if index==None or len(self.frame_list())==index:
                y = self.interior["height"]
                index = len(self.frame_list)
            else:
                y = int(self.frame_list[index].place_info()['y'])
                self.move_Frame(height,y)
            frame = ttk.Frame(self.interior, *args, **kw)
            frame.place(x=0, relwidth=1, y=y, height=height)
            self.frame_list.insert(index,frame)
            self.interior["height"] += height
            self.canvas.yview_moveto(1)
            return frame
        def move_Frame(self,height,y):
            for children in self.interior.winfo_children():
                tmp = int(children.place_info()['y'])
                if tmp>=y:
                    children.place(y=tmp+height)
        def delete_Frame(self, frame):
            height = int(frame.place_info()['height'])
            y = int(frame.place_info()['y'])
            self.move_Frame(-height,y)
            self.interior["height"] -= height
            self.frame_list.pop(self.frame_list.index(frame))
            frame.destroy()
    class FiltListbox(tk.Frame):
        def __init__(self,master,items=[],cmp = None,*args,**kw):
            self.cmp = cmp
            default = {
                'font':('New Time Roman',12),
                'bd':0,
                'selectmode':'multiple',
                'activestyle':'dotbox',
                'highlightthickness':1,
                'highlightbackground':'#7b7b7b',
                'highlightcolor':'#1884da',
            }
            default.update(kw)
            kw = default
            tk.Frame.__init__(self,master,bg='#7b7b7b')
            self.listbox = listbox = tk.Listbox(self,*args,**kw)
            vscrollbar = ttk.Scrollbar(self, orient='vertical')
            vscrollbar.configure(command=listbox.yview)
            listbox.config(yscrollcommand=vscrollbar.set)
            self.entry = entry = ttk.Entry(self,font=kw['font'])
            entry.grid(column=1,row=1,sticky='ew')
            
            vscrollbar.grid(column=2,row=1,rowspan=2,sticky='news',padx=[0,1],pady=[1,1])
            listbox.grid(column=1,row=2,sticky='news')
            
            self.columnconfigure(1,weight=1)
            self.columnconfigure(2,minsize=22)
            self.rowconfigure(2,weight=1)
            
            entry.bind('<Key>',lambda e:entry.after(1,self.filt))
            entry.lower()
            
            self.items = self.sort(items)
            listbox.insert(0,*self.items)
            
            def _on_mousewheel(event):
                listbox.yview_scroll(-1 * (event.delta / 120), "units")
                return 'break'
    
            def Enter(event):
                listbox.bind_all("<MouseWheel>", _on_mousewheel)
                widget = event.widget
                try:
                    if widget.focus_get()!=widget:
                        widget.config(highlightbackground='#2d2d2d')
                except KeyError: pass
            listbox.bind('<Enter>', Enter)
    
            def Leave(event):
                listbox.unbind_all("<MouseWheel>")
                widget = event.widget
                try:
                    if widget.focus_get()!=widget:
                        widget.config(highlightbackground='#7b7b7b')
                except KeyError: pass
            listbox.bind('<Leave>', Leave)
            
        def sort(self,items):
            if self.cmp != None:
                return sorted(items,cmp = self.cmp,)
            else:
                return sorted(items)
        def filt(self,):
            keyin = self.entry.get().lower()
            items = []
            for i in self.items:
                if keyin in i.lower():
                    items.append(i)
            self.listbox.delete(0,'end')
            self.listbox.insert(0,*items)
        def insert(self,*items):
            self.items += list(items)
            self.items = self.sort(self.items)
            self.filt()
        def delete(self,items):
            if type(items)==str:
                items = [items]
            for item in items:
                self.items.remove(item)
            self.filt()
        def clear(self,):
            self.items = []
            self.filt()
        def clearEntry(self):
            self.entry.delete(0,'end')
        def replace(self,replacer):
            tmp = self.items[:]
            self.items = []
            self.insert(*replacer)
            return tmp
        def curselection(self,):
            selected = self.listbox.curselection()
            curitems = self.listbox.get(0,'end')
            return {i:curitems[i] for i in selected}
        def get(self,first=None,last=None):
            if first==None:
                return self.items
            else:
                return self.listbox.get(first,last)
    class PromptLabel():
        def __init__(self,master=None,text=''):
            self.top = None
            self.master = master
            self.x,self.y = None,None
            self.text = text
        def set_master(self,master):
            self.master = master
        def set_xy(self,x,y):
            self.x,self.y = x,y
        def set_text(self,text):
            self.text = text
        def show(self,text=None,x=None,y=None,wrap=300):
            if self.top:
                return False
            if text==None:
                text = self.text
            if not text:
                return False
            if x==None:
                if self.x!=None:
                    x = self.x
                elif self.master:
                    x = int(self.master.winfo_rootx())
                else:
                    x = 0
            if y==None:
                if self.y!=None:
                    y = self.y
                elif self.master:
                    y = int(self.master.winfo_rooty())+int(self.master.winfo_height())
                else:
                    y = 0
            
            self.top = tk.Toplevel(self.master)
            self.top.wm_overrideredirect(1)
            self.top.wm_geometry("+%d+%d"%(x,y))
            label = tk.Label(self.top,text=text,justify='left',background="#ffffe0",relief='solid',borderwidth=1,wraplength=wrap)
            label.pack(ipadx=1)
            return True
        def hide(self):
            if self.top:
                self.top.destroy()
                self.top = None
                return True
            else:
                return False
        def timer_init(self):
            self.lastmove = time.time()
            self.terminate = False
        def timer(self,wait=1.5,cmd=lambda:None):
            def _timer():
                if time.time()-self.lastmove>wait:
                    if not self.top:
                        cmd()
                        if self.show():print 'show'
                else:
                    if self.terminate: print 'leave'
                    return self.terminate
            return _timer
        def timer_terminate(self):
            self.terminate = True
            self.hide()
        def motion(self):
            self.lastmove = time.time()
            self.hide()
    class Placer():
        def __init__(self, orient, *arg, **kw):
            if orient not in ['x','y']:
                raise "PlacerConfigError: orient must be 'x' or 'y'"
            self.orient = orient
            self.configlist = []
            self.config =   {
                            'length':0,
                            'weight':0
                            }
            self.configlist.append(self.config.copy())
            self.next_widget(*arg, **kw)
        def __call__(self, position):
            return self.get(position)
        def __str__(self,):
            return self.print_widget()
        def next_widget(self, length, weight=None):
            if type(length) == type(1):
                length = [length]
            if type(weight) == type(1):
                weight = [weight]
            if weight == None:
                weight = [0]*len(length)
            for i in weight:
                if i <0:
                    raise "weight can't be negative"
            for j in length:
                if length<0:
                    raise "length can't be negative"
            if len(length)!=len(weight):
                raise "length and Weight must have same number of elements"
            for i in xrange(len(length)):
                self.config['length'] += length[i]
                self.config['weight'] += weight[i]
                self.configlist.append(self.config.copy())
        def get(self, position ='all'):
            n = len(self.configlist)-1
            tot_len = self.configlist[-1]['length']
            tot_wei = float(self.configlist[-1]['weight'])
            
            if self.orient=='x':
                rela = 'relx'
                a = 'x'
                relq = 'relwidth'
                q = 'width'
            elif self.orient=='y':
                rela = 'rely'
                a = 'y'
                relq = 'relheight'
                q = 'height'
                
            
            def _get(nums):
                len_pre = self.configlist[nums[0]]['length']
                len_cur = self.configlist[nums[1]+1]['length']
                if tot_wei:
                    wei_pre = self.configlist[nums[0]]['weight']/tot_wei
                    wei_cur = self.configlist[nums[1]+1]['weight']/tot_wei
                else:
                    wei_pre = 0
                    wei_cur = 0
                    
                config =     {
                            rela:wei_pre,
                            a:int(len_pre-tot_len*wei_pre),
                            relq:wei_cur-wei_pre,
                            q:int(len_cur-tot_len*wei_cur)-int(len_pre-tot_len*wei_pre),
                            }
                return config
                
            if position == 'all':
                position = [0,n-1]
            elif type(position) == int:
                position = (position+n)%n
                position = [position,position]
            elif type(position) in {list,tuple} and len(position)==2:
                position = [(i+n)%n for i in position]
                if not position[0]<position[1]:
                    return
            else:
                return
            return _get(position)
        def print_widget(self, position='all'):
            if self.orient=='x':
                axis = 'x'
                quan = 'width'
            elif self.orient=='y':
                axis = 'y'
                quan = 'height'
            
            keys = ['rel%s'%axis,'%s'%axis,'rel%s'%quan,'%s'%quan]
            
            if position == 'all':
                result = self.get()
                string = ''
                for i in range(len(result)):
                    string += '*'*20+'Widget %-2d'%(i+1)+'*'*20+'\n'
                    for j in keys:
                        string += "%-9s = %.3f\n"%(j, result[i][j])
                string += '*'*49
                return string
            elif type(position) == list:
                string = ''
                for i in sorted(position):
                    string += '*'*20+'Widget %-2d'%(i+1)+'*'*20+'\n'
                    for j in keys:
                        string += "%-9s = %.3f\n"%(j, self.get(i)[j])
                string += '*'*49
                return string
            elif type(position) == int:
                string = ''
                string += '*'*20+'Widget %-2d'%(position+1)+'*'*20+'\n'
                for j in keys:
                    string += "%-9s = %.3f\n"%(j, self.get(position)[j])
                string += '*'*49
                return string
        def merge(self, placer):
            if self.orient == 'x' and placer.orient == 'y':
                xplacer = cp.deepcopy(self)
                yplacer = cp.deepcopy(placer)
            elif self.orient == 'y' and placer.orient == 'x':
                yplacer = cp.deepcopy(self)
                xplacer = cp.deepcopy(placer)
            def xyplacer(x,y):
                result = {}
                result.update(xplacer.get(x))
                result.update(yplacer.get(y))
                return result
            return xyplacer
    class TclError(tk.TclError): pass