#coding=UTF-8

import sys

if sys.version_info[0] < 3:
    from Tkinter import *
    from tkMessageBox import *
    from tkFont import *
    from tkFileDialog import *
    from ScrolledText import *
    from ttk import Notebook
else:
    from tkinter import *
    from tkinter.messagebox import *
    from tkinter.font import *
    from tkinter.filedialog import *
    from tkinter.scrolledtext import *
    from tkinter.ttk import Notebook

ABOUT = "Program created by Florian AYMARD\nhttps://github.io/flaymard\nI'm a beginner. Feel free to contribute, I'll appreciate it !"

FILETYPES = [('All files', '.*'), ('Plain text', '.txt'), ('Cancer files', '.php'), ('OMG MUCH SKILL', '.doge')]

FILE_SAVED = True

def about():
    showinfo("À propos", ABOUT)

def ctrlEventHandler(event):
    if event.keysym == 's':
        saveFile()
    if event.keysym == 'o':
        openFile()
    if event.keysym == 'z':
        undo()
    if event.keysym == 'y':
        redo()

def openFile():
    filepath = askopenfilename(title='Open document',filetypes=FILETYPES)
    savePath(filepath, "save")
    with open(filepath, "r") as userFile:
        fileData = userFile.read().decode('UTF-8')
        text.delete(0.0, END)
        text.insert(INSERT, fileData)
        userFile.close()
        initialLoad(text.get(0.0, END), "save")

def initialLoad(inputVar, request):
    global savedLoad
    if request == "save":
        savedLoad = inputVar
    if request == "load":
        return savedLoad

def savePath(inputVar, request):
    global saved
    try:
        if request == "save":
            saved = inputVar
        if request == "load":
            return saved
    except UnboundLocalError:
        return "NO PATH"


def saveFile():
    try:
        filepath = savePath("", "load")
        data = text.get(0.0, END)
        with open(filepath, "w") as userFile:
            userFile.write(data.encode('UTF-8'))

    except NameError:
        saveAsFile()

    #if NEW_FILE == True:
        #saveAsFile()

def saveAsFile():
    filepath = asksaveasfilename(title='Save document as',filetypes=FILETYPES)
    if filepath != '':
        NEW_FILE = False
        savePath(filepath, "save")
        saveFile()

def saveCheck():
    try:
        if text.get(0.0, END).encode('UTF-8') == initialLoad("", "load").encode('UTF-8'):
            mainWindow.destroy()

        else:
            if askquestion("Quit", "Document has been changed, do you want to quit anyway?") == 'yes':
                mainWindow.destroy()

    except NameError:
        if text.get(0.0, END) == '\n':
            mainWindow.destroy()
        else:
            if askquestion("Quit", "Document has been changed, do you want to quit anyway?") == 'yes':
                mainWindow.destroy()

def copy():
    try:
        text.clipboard_clear()
        sel = text.selection_get()
        text.clipboard_append(sel)
    except TclError:
        return -1

def paste():
    try:
        clip = text.clipboard_get()
        text.insert(INSERT, clip)
    except TclError:
        return -1

def cut():
    try:
        text.clipboard_clear()
        sel = text.selection_get()
        text.clipboard_append(sel)
        text.selection_clear()
    except TclError:
        return -1

def undo():
    text.edit_undo()
def redo():
    text.edit_redo()

def changePrefs():
    global fontList
    global prefsEdit
    global sizeEntry
    #initiating font list for font editing
    fonts_list = list(families())
    fonts_list.sort()
    #creating window
    prefsEdit = Toplevel()
    prefsEdit.title("Change parameters")
    prefsEdit.geometry("300x300")
    prefsEdit.resizable(False,False)
    #creating notebook for multiple tabs
    prefsBook = Notebook(prefsEdit)

    #creating frame which will contain text preferences (font, size)
    textFrame = Frame(prefsBook)

    fontFrame = LabelFrame(textFrame, borderwidth=2, relief=GROOVE, text="Font")
    fontFrame.pack(padx=10, pady=10, side=LEFT)
    fontFrame.place(rely=1.0, relx=0.0, x=10, y=-10, anchor=SW)

    sel_font = StringVar()
    sel_font.set(font.actual()["family"])
    fontList = OptionMenu(fontFrame, sel_font, *fonts_list)
    fontList.pack()

    buttonFrame = Frame(textFrame, borderwidth=2, relief=GROOVE)
    buttonFrame.pack(side=BOTTOM, padx=10, pady=10)
    buttonFrame.place(rely=1.0, relx=1.0, x=-10, y=-10, anchor=SE)
    bouton = Button(buttonFrame, text="Set font", command=setFont)
    bouton.pack()

    sizeFrame = LabelFrame(textFrame, borderwidth=2, relief=GROOVE, text="Font size", width=200, height=50)
    sizeFrame.pack(side=TOP, padx=10, pady=10)
    sizeFrame.place(relx=0.0, rely=0.0, x=10, y=10, anchor=NW)
    sizeEntry = Entry(sizeFrame, width=30)
    sizeEntry.pack()
    #adding it to the notebook as a new tab
    prefsBook.add(textFrame, text="Font")
    prefsBook.pack(fill=BOTH, expand=1)

def setFont():
    newFont = fontList.get(ACTIVE)
    newSize = sizeEntry.getint()
    font.config(family=newFont, size=newSize)
    prefsEdit.destroy()



#creating editor window
mainWindow = Tk()
mainWindow.geometry("600x600")
mainWindow.title("JPP Text Editor")

#creating text field
frame = Frame(mainWindow)
global font
font = Font(family="Calibri", size=12)
text = ScrolledText(frame, width=mainWindow.winfo_screenwidth(), height=mainWindow.winfo_screenheight(), font=font)
text.pack()
frame.pack()

#creating menu bar
menuBar = Menu(mainWindow)


fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Open", command=openFile, accelerator="Ctrl+O")
fileMenu.add_command(label="Save", command=saveFile, accelerator="Ctrl+S")
fileMenu.add_command(label="Save as", command=saveAsFile, accelerator="Ctrl+Shift+S (todo)")
menuBar.add_cascade(label="File", menu=fileMenu)

editMenu = Menu(menuBar, tearoff=0)
editMenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
editMenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
editMenu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
editMenu.add_separator()
editMenu.add_command(label="Undo", command=undo, accelerator="Ctrl+Z")
editMenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")
editMenu.add_separator()
editMenu.add_command(label="Preferences", command=changePrefs)
menuBar.add_cascade(label="Edit", menu=editMenu)

moreMenu = Menu(menuBar, tearoff=0)
moreMenu.add_command(label="About...", command=about)
menuBar.add_cascade(label="More", menu=moreMenu)

mainWindow.config(menu=menuBar)

mainWindow.bind("<Control-s>", ctrlEventHandler)
mainWindow.bind("<Control-o>", ctrlEventHandler)
mainWindow.bind("<Control-z>", ctrlEventHandler)
mainWindow.bind("<Control-y>", ctrlEventHandler)


mainWindow.protocol("WM_DELETE_WINDOW", saveCheck)
mainWindow.mainloop()
