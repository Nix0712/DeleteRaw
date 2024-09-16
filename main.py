from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import os

window = tk.Tk()
window.title("DeleteRaw")
window.resizable(False, False)
window.configure(padx=30, pady=30, background="#3C3D37", width=600, height=200)

def handle_button_press(event):
    window.destroy()

def getDir():
    fileDir = filedialog.askdirectory()
    if len(fileDir) == 0:
        return
    label_dir.config(text=fileDir)

def deleteRaw():
    fileDir = label_dir.cget("text")
    if fileDir == "Nothing selected...":
        messagebox.showerror("Error", "Please select a directory")
        return
    secureRaw = textDelete.get("1.0", "end-1c").split(",")
    if secureRaw[0] == '':
        messagebox.showerror("Error", "Please enter the photos you want to keep")
        return
    toBeRemoved = []
    totalRemoved = 0
    trackCout = 0
    for filename in os.listdir(fileDir):
        if filename.endswith(".RAF"):
            currFile = filename.split(".")[0]
            checkName = currFile[4:]
            if checkName not in secureRaw:
                toBeRemoved.append(filename)
                totalRemoved += 1
            else:
                trackCout += 1
    if trackCout != len(secureRaw):
        messagebox.showerror("Error", "You made a mistake in the photos you want to keep")
        return
    
    for file in toBeRemoved:
        os.remove(fileDir + "/" + file)
    messagebox.showinfo("Info", f"{totalRemoved} files removed from the directory\n ")
    return


tk.Label(window,text="Choose directory: ", bg='#3C3D37', fg='#ECDFCC').place(x=50, y=6)
tk.Button(window, text="Browse", command=getDir, bg='#3C3D37', fg='#ECDFCC').place(x=400, y=6)
label_dir = tk.Label(window,text="Nothing selected...",bg='#1E201E', fg='#ECDFCC', height=2, width=34)

label_dir.place(x=150, y=0)

tk.Label(window,text="Enter photos NOT to be deleted (e.g 123,321...)", bg='#3C3D37', fg='#ECDFCC').place(x=140, y=50)

textDelete = tk.Text(window, height=2, width=50, bg='#1E201E', fg='#ECDFCC')
textDelete.place(x=50, y=70)
tk.Button(window, text="Delete", bg='#3C3D37', fg='#ECDFCC', command=deleteRaw).place(x=250, y=120)

# Start the event loop.
window.mainloop()
