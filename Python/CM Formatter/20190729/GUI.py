import os, re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

"""
REMOVE EXTRA SELF
"""



class Setup_Menu(tk.Tk):
    def __init__(self):
        self.isReady = False

        tk.Tk.__init__(self)
        self.title("CM Formatter")

        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()

        self.geometry("+{}+{}".format(self.screenWidth // 2 - self.windowWidth, self.screenHeight // 2 - self.windowHeight))
        self.resizable(width=False, height=False)

        self.createWidgets()

        self.isProgramRunning = tk.BooleanVar()
        self.isProgramRunning.set(tk.TRUE)
        self.lineExceptions = list()


    def createWidgets(self):
        # Specify data to be included
        self.dataLbl = tk.LabelFrame(text="Data to include on graphs")
        self.dataLbl.grid(row=0, column=0, padx=self.windowWidth // 100)

        self.includedData = dict()
        for dataType in ["HC", "HI", "PC", "PI"]:
            self.includedData[dataType] = tk.IntVar()
            self.includedData[dataType].set(1)

        self.includeHCBtn = tk.Checkbutton(self.dataLbl, text="HC", variable=self.includedData["HC"])
        self.includeHCBtn.grid(row=0, column=0, sticky="W")

        self.includeHIBtn = tk.Checkbutton(self.dataLbl, text="HI", variable=self.includedData["HI"])
        self.includeHIBtn.grid(row=0, column=1, sticky="W")

        self.includePCBtn = tk.Checkbutton(self.dataLbl, text="PC", variable=self.includedData["PC"])
        self.includePCBtn.grid(row=1, column=0, sticky="W")

        self.includePIBtn = tk.Checkbutton(self.dataLbl, text="PI", variable=self.includedData["PI"])
        self.includePIBtn.grid(row=1, column=1, sticky="W")

        self.includedData["isOmitExtra"] = tk.IntVar()
        self.includedData["isOmitExtra"].set(1)
        self.omitExtraBtn = tk.Checkbutton(self.dataLbl, text="Omit extra data? (pitch, roll, GPS, etc.)", variable=self.includedData["isOmitExtra"])
        self.omitExtraBtn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Lines settings
        self.linesLbl = tk.LabelFrame(text="Lines")
        self.linesLbl.grid(row=0, column=1, padx=self.windowWidth // 100, sticky="NE")

        self.lineLengthLbl = tk.Label(self.linesLbl, text="Target line length (m)")
        self.lineLengthLbl.grid(row=0, column=0, sticky="W")
        self.lineLengthEntry = tk.Entry(self.linesLbl, width=10, text="hello", justify=tk.CENTER)
        self.lineLengthEntry.grid(row=0, column=1, sticky="E")

        self.exceptionsBtn = tk.Button(self.linesLbl, text="Manage exceptions", command=self.openExceptionsWindow)
        self.exceptionsBtn.grid(row=2, column=0, columnspan=2)

        self.isLinesEqual = tk.IntVar()
        self.isLinesEqual.trace("w", lambda *args: self.exceptionsBtn.config(state=tk.DISABLED if self.exceptionsBtn.cget("state") == tk.NORMAL else tk.NORMAL))
        self.isLinesEqual.set(1)
        self.isLinesEqualBtn = tk.Checkbutton(self.linesLbl, text="All lines are approximately target length", variable=self.isLinesEqual)
        self.isLinesEqualBtn.grid(row=1, column=0, columnspan=2)

        #File settings
        self.fileLbl = tk.LabelFrame(text="File")
        self.fileLbl.grid(row=1, column=0, columnspan=2, sticky="W", padx=self.windowWidth // 100)

        self.pathLbl = tk.Label(self.fileLbl, text="Path")
        self.pathLbl.grid(row=1, column=0)
        self.filePath = tk.StringVar()
        self.filePath.set(r"C:\Users\BenPc\Desktop\Python\Projects\In Progress\CM Formatter\STJOHN_TEST.xlsx")
        self.pathEntry = tk.Entry(self.fileLbl, textvariable=self.filePath, width=50)
        self.pathEntry.grid(row=1, column=1, columnspan=2)
        self.pathBtn = tk.Button(self.fileLbl, text="Browse...", command=self.browseFiles)
        self.pathBtn.grid(row=1, column=3, padx=5)

        # Buttons
        self.buttonFrame = tk.Frame()
        self.buttonFrame.grid(row=2, column=1, sticky="SE", padx=(0, 2), pady=1)

        self.acceptBtn = tk.Button(self.buttonFrame, text="Format", command=self.readyFormat)
        self.acceptBtn.pack(side=tk.RIGHT, anchor="e")
        self.bind("<Return>", self.readyFormat)
        self.cancelBtn = tk.Button(self.buttonFrame, text="Cancel", command=self.killProgram)
        self.cancelBtn.pack(side=tk.RIGHT, anchor="e")
        self.bind("<Escape>", self.killProgram)


    def openExceptionsWindow(self):
    	ExceptionsManager = Exceptions_Window(self)


    def browseFiles(self):
        user = os.path.expanduser('~')
        filetypes = [("Excel Files", "*.xl *.xlsx *.xlsm *.xlsb *.xlam *.xltx *.xltm *.xlx *.xlt *.xlm *.xlw"), ("All Files", "*")]
        file = filedialog.askopenfilename(parent=self, initialdir="{}\\Desktop".format(user), filetypes=filetypes, title="Select a file...")
        if file is not None:
           self.filePath.set(file)


    def checkAllInputs(self):
        floatPattern = re.compile("^[0-9]+(\.[0-9]+)?$")
        exceptionLines = [i[0].get() for i in self.lineExceptions]

        if self.lineLengthEntry.get().strip() == "":
            messagebox.showerror("Error", "You must input a target line length.")
            return False
        elif not floatPattern.match(self.lineLengthEntry.get().strip()):
            messagebox.showerror("Error", "Invalid target line length given.")
            return False

        if self.isLinesEqual.get() == 0:
            for line, length in self.lineExceptions:
                if not (line.get() == length.get() == ""):
                    if not line.get().strip().isdigit() or not floatPattern.match(length.get().strip()):
                        messagebox.showerror("Error", "Invalid line length exception given for line <{}> with length <{}>.".format(line.get(), length.get()))
                        return False
        if list(set(exceptionLines)) != exceptionLines:
           messagebox.showerror("Error", "The same line cannot have more than one length exception. Manange exceptions and try again.")
           return False

        if self.filePath.get() == "":
            messagebox.showerror("Error", "You must select a file.")
            return False
        elif not os.path.isfile(self.filePath.get()):
             messagebox.showerror("Error", "{} does not exist.\nCheck spelling and try again.".format(self.filePath.get()))
             return False
        elif not re.compile("^.*\.(xl|xlsx|xlsm|xlsb|xlam|xltx|xltm|xlx|xlt|xlm|xlw)$").match(self.filePath.get()):
            if not messagebox.askokcancel("Warning", "Selected file is not a recognized Excel file type."):
                return False

        return True


    def killProgram(self, *args):
        self.destroy()
        self.quit()


    def readyFormat(self, *args):
        if self.checkAllInputs():
            print("Good")

            self.FILE_PATH = self.filePath.get()

            self.INCLUDED_DATA = dict()
            for data, val in self.includedData.items():
                self.INCLUDED_DATA[data] = bool(val.get())

            self.TARGET_LENGTH = float(self.lineLengthEntry.get().strip())

            self.IS_LINES_EQUAL = bool(self.isLinesEqual.get())

            self.LENGTH_EXCEPTIONS = dict()
            for line, length in self.lineExceptions:
                self.LENGTH_EXCEPTIONS[int(line.get().strip())] = float(length.get().strip())

            self.destroy()
            self.isReady = True
        else:
            print("Bad")


class Exceptions_Window(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self)
        self.geometry("+{}+{}".format(root.winfo_rootx() + 10, root.winfo_rooty() + 10))
        self.resizable(width=False, height=True)

        self.title("Manage Exceptions")
        self.grab_set()
        self.focus()

        self.root = root
        self.lineExceptionsTmp = root.lineExceptions[:]
        self.exceptionEntries = list()

        self.tableFrame = tk.Frame(self)
        self.tableFrame.grid(row=0, column=1, sticky="N")
        tk.Label(self.tableFrame, text="Line").grid(row=0, column=0)
        tk.Label(self.tableFrame, text="Length (m)").grid(row=0, column=1)

        self.mngTableFrame = tk.Frame(self)
        self.mngTableFrame.grid(row=0, column=2, sticky="N")
        self.addBtn = tk.Button(self.mngTableFrame, text="Add row", command=self.createRow)
        self.addBtn.pack(fill=tk.X)
        self.removeBtn = tk.Button(self.mngTableFrame, text="Remove row", command=self.deleteRow)
        self.removeBtn.pack(fill=tk.X)
        self.clearBtn = tk.Button(self.mngTableFrame, text="Clear all", command=self.clearAllRows)
        self.clearBtn.pack(fill=tk.X)

        self.btnFrame = tk.Frame(self)
        self.btnFrame.grid(row=1, column=2, sticky="E")
        self.acceptBtn = tk.Button(self.btnFrame, text="Accept", command=self.saveAndExit)
        self.acceptBtn.pack(side=tk.RIGHT)
        self.bind("<Return>", self.saveAndExit)
        self.cancelBtn = tk.Button(self.btnFrame, text="Cancel", command=self.destroy)
        self.cancelBtn.pack(side=tk.RIGHT)
        self.bind("<Escape>", self.exitWithoutSaving)

        if len(self.lineExceptionsTmp) == 0:
            self.createRow()
        else:
            for row in range(len(self.lineExceptionsTmp)):
                self.placeRowWidgets(row)


    def createRow(self):
        self.lineExceptionsTmp.append((tk.StringVar(), tk.StringVar()))

        row = len(self.lineExceptionsTmp) - 1
        self.placeRowWidgets(row)


    def placeRowWidgets(self, row):
        for col, var in enumerate(self.lineExceptionsTmp[row]):
            self.exceptionEntries.append(tk.Entry(self.tableFrame, textvariable=var))
            self.exceptionEntries[-1].grid(row=row + 1, column=col)


    def deleteRow(self):
        if len(self.exceptionEntries) > 2:
            for widget in self.exceptionEntries[-2:]:
                widget.destroy()

            del self.lineExceptionsTmp[-1], self.exceptionEntries[-2:]


    def clearAllRows(self):
        for row in range(len(self.exceptionEntries) - 1):
            self.deleteRow()


    def saveAndExit(self, *args):
        for i in range(len(self.lineExceptionsTmp) - 1, -1, -1):
            if self.lineExceptionsTmp[i][0].get() == "" == self.lineExceptionsTmp[i][1].get():
               for entry in self.exceptionEntries[i:i - 1]:
                   entry.destroy()

               del self.lineExceptionsTmp[i], self.exceptionEntries[i:i - 1]

        self.root.lineExceptions = self.lineExceptionsTmp[:]
        self.destroy()


    def exitWithoutSaving(self, *args):
        self.destroy()


def main():
    App = Setup_Menu()
    App.mainloop()

if __name__ == "__main__":
	main()




