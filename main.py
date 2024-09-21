from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import os
from send2trash import send2trash

window = tk.Tk()
window.title("DeleteRaw")
window.resizable(False, False)
window.configure(padx=30, pady=30, background="#3C3D37", width=600, height=220)

def handle_button_press(event):
    window.destroy()

def getDir():
    fileDir = filedialog.askdirectory()
    if len(fileDir) == 0:
        return
    label_dir.config(text=fileDir)

def deleteRaw():
    deleteButton["state"] = "disabled"
    fileDir = label_dir.cget("text")
    if fileDir == "Nothing selected...":
        messagebox.showerror("Error", "Please select a directory")
        deleteButton["state"] = "active"
        return
    selected = textDelete.get("1.0", "end-1c").split(",")
    if selected[0] == '':
        messagebox.showerror("Error", "Please enter selection")
        deleteButton["state"] = "active"
        return

    if jpgCheck.get() == 0 and rawCheck.get() == 0:
        messagebox.showerror("Error", "Please select a file type")
        deleteButton["state"] = "active"
        return

    toBeRemoved = []
    totalRemoved = 0
    totalRAW = 0
    totalJPG = 0
    for filename in os.listdir(fileDir):
        currFile = filename.split(".")[0]
        checkName = currFile[4:]
        if (filename.endswith(".JPG") and jpgCheck.get() == 1) or (filename.endswith(".RAF") and rawCheck.get() == 1):
            if filename.endswith(".RAF"):
                totalRAW += 1
            if filename.endswith(".JPG"):
                totalJPG += 1

            if (checkName not in selected and saveCheck.get() == 1) or (checkName in selected and saveCheck.get() == 0):
                toBeRemoved.append(filename)
                totalRemoved += 1
    totalCheck = 0
    
    checkSum = 0
    if saveCheck.get() == 1:
        if jpgCheck.get() == 1:
            totalCheck += totalJPG-len(selected)
        if rawCheck.get() == 1:
            totalCheck += totalRAW-len(selected)
    if saveCheck.get() == 0:
        if jpgCheck.get() == 1:
            totalCheck += len(selected)
        if rawCheck.get() == 1:
            totalCheck += len(selected)



    if totalCheck != totalRemoved:
        messagebox.showerror("Error", "You made a mistake in the photos you want to keep")
        deleteButton["state"] = "active"
        return
    
    for file in toBeRemoved:
        full_path = fileDir + "/" + file
        full_path = full_path.replace("/", "\\")
        send2trash(full_path)
    messagebox.showinfo("Info", f"{totalRemoved} files removed from the directory\n ")
    deleteButton["state"] = "active"
    return


tk.Label(window,text="Choose directory: ", bg='#3C3D37', fg='#ECDFCC').place(x=40, y=6)
tk.Button(window, text="Browse", command=getDir, bg='#3C3D37', fg='#ECDFCC', activebackground='#3C3D37', activeforeground='#ECDFCC').place(x=400, y=6)
label_dir = tk.Label(window,text="Nothing selected...",bg='#1E201E', fg='#ECDFCC', height=2, width=34)

label_dir.place(x=150, y=0)

tk.Label(window,text="Enter selection of photos for DSCFxxxx (e.g 123,321...)", bg='#3C3D37', fg='#ECDFCC').place(x=100, y=50)

textDelete = tk.Text(window, height=2, width=50, bg='#1E201E', fg='#ECDFCC')
textDelete.place(x=50, y=70)
deleteButton = tk.Button(window, text="Delete", bg='#3C3D37', fg='#ECDFCC', command=deleteRaw, activebackground='#3C3D37', activeforeground='#ECDFCC')
deleteButton.place(x=250, y=120)


saveCheck = tk.IntVar()
jpgCheck = tk.IntVar()
rawCheck = tk.IntVar()
c1 = tk.Checkbutton(window, text='Save selected',variable=saveCheck, onvalue=1, offvalue=0,  bg='#3C3D37', fg='#ECDFCC', activebackground='#3C3D37', activeforeground='#ECDFCC', selectcolor='#3C3D37')
c1.place(x=10,y=120)
c2 = tk.Checkbutton(window, text='JPG',variable=jpgCheck, onvalue=1, offvalue=0,  bg='#3C3D37', fg='#ECDFCC', activebackground='#3C3D37', activeforeground='#ECDFCC', selectcolor='#3C3D37')
c2.place(x=10,y=140)
c3 = tk.Checkbutton(window, text='RAW',variable=rawCheck, onvalue=1, offvalue=0,  bg='#3C3D37', fg='#ECDFCC', activebackground='#3C3D37', activeforeground='#ECDFCC', selectcolor='#3C3D37')
c3.place(x=10,y=160)


window.mainloop()
