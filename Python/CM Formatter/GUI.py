import os, re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox


class SetupMenu(tk.Tk):

    def __init__(self):

        self.isReady = False
        self.lineExceptionVars = list()

        tk.Tk.__init__(self)
        self.title("CM Formatter")
        self.screenWidth = self.winfo_screenwidth()
        self.screenHeight = self.winfo_screenheight()
        self.windowWidth = self.winfo_reqwidth()
        self.windowHeight = self.winfo_reqheight()
        self.geometry("+{}+{}".format(
            self.screenWidth // 2 - self.windowWidth,
            self.screenHeight // 2 - self.windowHeight
            ))
        self.resizable(width=False, height=False)

        self.create_widgets()
        self.isProgramRunning = tk.BooleanVar()
        self.isProgramRunning.set(tk.TRUE)


    def create_widgets(self):

        # Specify data to be included
        self.dataLbl = tk.LabelFrame(text="Data to include on graphs")
        self.dataLbl.grid(row=0, column=0, padx=self.windowWidth // 100)

        self.includedData = dict()
        for dataType in ["HC", "HI", "PC", "PI"]:
            self.includedData[dataType] = tk.IntVar()
            self.includedData[dataType].set(1)

        self.includeHCBtn = tk.Checkbutton(
            self.dataLbl,
            text="HC",
            variable=self.includedData["HC"]
            )
        self.includeHCBtn.grid(row=0, column=0, sticky="W")

        self.includeHIBtn = tk.Checkbutton(
            self.dataLbl,
            text="HI",
            variable=self.includedData["HI"]
            )
        self.includeHIBtn.grid(row=0, column=1, sticky="W")

        self.includePCBtn = tk.Checkbutton(
            self.dataLbl,
            text="PC",
            variable=self.includedData["PC"]
            )
        self.includePCBtn.grid(row=1, column=0, sticky="W")

        self.includePIBtn = tk.Checkbutton(
            self.dataLbl,
            text="PI",
            variable=self.includedData["PI"]
            )
        self.includePIBtn.grid(row=1, column=1, sticky="W")

        self.includedData["isOmitExtra"] = tk.IntVar()
        self.includedData["isOmitExtra"].set(1)
        self.omitExtraBtn = tk.Checkbutton(
            self.dataLbl,
            text="Omit extra data? (pitch, roll, GPS, etc.)",
            variable=self.includedData["isOmitExtra"]
            )
        self.omitExtraBtn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Lines settings
        self.linesLbl = tk.LabelFrame(text="Lines")
        self.linesLbl.grid(
            row=0,
            column=1,
            padx=self.windowWidth // 100,
            sticky="NE"
            )

        self.lineLengthLbl = tk.Label(
            self.linesLbl,
            text="Target line length (m)"
            )
        self.lineLengthLbl.grid(row=0, column=0, sticky="W")
        self.lineLengthEntry = tk.Entry(
            self.linesLbl,
            width=15,
            text="hello",
            justify=tk.CENTER
            )
        self.lineLengthEntry.grid(row=0, column=1, sticky="E")

        self.exceptionsBtn = tk.Button(
            self.linesLbl,
            text="Manage exceptions",
            command=self.open_exceptions_window
            )
        self.exceptionsBtn.grid(row=2, column=0, columnspan=2)

        self.isLinesEqual = tk.IntVar()
        self.isLinesEqual.trace(
            mode="w",
            callback=lambda *args: self.exceptionsBtn.config(
                state=tk.DISABLED if self.exceptionsBtn.cget("state") == tk.NORMAL else tk.NORMAL
                )
            )
        self.isLinesEqual.set(1)
        self.isLinesEqualBtn = tk.Checkbutton(
            self.linesLbl,
            text="All lines are approximately target length",
            variable=self.isLinesEqual
            )
        self.isLinesEqualBtn.grid(row=1, column=0, columnspan=2)

        #File settings
        self.fileLbl = tk.LabelFrame(text="File")
        self.fileLbl.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="W",
            padx=self.windowWidth // 100
            )

        self.pathLbl = tk.Label(self.fileLbl, text="Path")
        self.pathLbl.grid(row=1, column=0)
        self.filePath = tk.StringVar()
        self.pathEntry = tk.Entry(
            self.fileLbl,
            textvariable=self.filePath,
            width=60
            )
        self.pathEntry.grid(row=1, column=1, columnspan=2)
        self.pathBtn = tk.Button(
            self.fileLbl,
            text="Browse...",
            command=self.browse_files
            )
        self.pathBtn.grid(row=1, column=3, padx=5)

        # Buttons
        self.buttonFrame = tk.Frame()
        self.buttonFrame.grid(row=2, column=1, sticky="SE", padx=(0, 2), pady=1)

        self.acceptBtn = tk.Button(
            self.buttonFrame,
            text="Format",
            command=self.ready_format
            )
        self.acceptBtn.pack(side=tk.RIGHT, anchor="e")
        self.bind("<Return>", self.ready_format)
        self.cancelBtn = tk.Button(
            self.buttonFrame,
            text="Cancel",
            command=self.kill_program
            )
        self.cancelBtn.pack(side=tk.RIGHT, anchor="e")
        self.bind("<Escape>", self.kill_program)


    def open_exceptions_window(self):

    	ExceptionsManager = ExceptionsWindow(self)


    def browse_files(self):

        user = os.path.expanduser('~')
        file = filedialog.askopenfilename(
            parent=self,
            initialdir="{}\\Desktop".format(user),
            filetypes=[("Excel Workbook Files", ".xlsx")],
            title="Select a file..."
            )
        if file is not None:
           self.filePath.set(file)


    def check_all_inputs(self):

        floatPattern = re.compile("^[0-9]+(\.[0-9]+)?$")
        exceptionLines = [i[0].get() for i in self.lineExceptionVars]

        if self.lineLengthEntry.get().strip() == "":
            messagebox.showerror("Error", "You must input a target line length.")
            return False
        elif not floatPattern.match(self.lineLengthEntry.get().strip()):
            messagebox.showerror("Error", "Invalid target line length given.")
            return False

        if self.isLinesEqual.get() == 0:
            for line, length in self.lineExceptionVars:
                if not (line.get() == length.get() == ""):
                    if not line.get().strip().isdigit() \
                    or not floatPattern.match(length.get().strip()):
                        messagebox.showerror(
                            "Error",
                            "Invalid line length exception given for line <{}> with length <{}>.".format(line.get(), length.get())
                            )
                        return False
        if list(set(exceptionLines)) != exceptionLines:
            messagebox.showerror(
                "Error",
                "The same line cannot have more than one length exception. Manange exceptions and try again."
                )
            return False

        if self.filePath.get() == "":
            messagebox.showerror("Error", "You must select a file.")
            return False
        elif not os.path.isfile(self.filePath.get()):
             messagebox.showerror(
                "Error",
                "{} does not exist.\nCheck spelling and try again.".format(self.filePath.get())
                )
             return False
        elif not re.compile("^.*\.xlsx$").match(self.filePath.get()):
            messagebox.showerror(
                "Error",
                "Selected file is not an accepted Excel file type."
                )
            return False

        return True


    def kill_program(self, *args):

        self.destroy()
        self.quit()


    def ready_format(self, *args):

        if self.check_all_inputs():
            self.FILE_PATH = self.filePath.get()

            self.INCLUDED_DATA = dict()
            for data, val in self.includedData.items():
                self.INCLUDED_DATA[data] = bool(val.get())

            self.TARGET_LENGTH = float(self.lineLengthEntry.get().strip())

            self.IS_LINES_EQUAL = bool(self.isLinesEqual.get())

            self.LENGTH_EXCEPTIONS = dict()
            for line, length in self.lineExceptionVars:
                self.LENGTH_EXCEPTIONS[int(line.get().strip())] = float(length.get().strip())

            self.destroy()
            self.isReady = True


class ExceptionsWindow(tk.Toplevel):

    def __init__(self, root):

        tk.Toplevel.__init__(self)
        self.geometry(
            "+{}+{}".format(root.winfo_rootx() + 10, root.winfo_rooty() + 10)
            )
        self.resizable(width=False, height=True)

        self.title("Manage Exceptions")
        self.grab_set()
        self.focus()

        self.root = root
        # Related lists; index = row
        self.lineExceptionVarsTmp = root.lineExceptionVars[:]
        self.lineExceptionEntries = list()

        self.lineLbl = tk.Label(self, text="             Line")
        self.lineLbl.grid(row=0, column=0, sticky="W")
        self.lengthLbl = tk.Label(self, text="Length (m)        ")
        self.lengthLbl.grid(row=0, column=0, sticky="E")

        self.tableFrame = tk.Frame(self)
        self.tableFrame.grid(row=1, column=0, sticky="N")

        self.mngTableFrame = tk.Frame(self)
        self.mngTableFrame.grid(row=0, column=2, rowspan=2, sticky="N")
        self.addBtn = tk.Button(
            self.mngTableFrame,
            text="Add row",
            command=self.create_row
            )
        self.addBtn.pack(fill=tk.X)
        self.removeBtn = tk.Button(
            self.mngTableFrame,
            text="Remove row",
            command=self.delete_last_row
            )
        self.removeBtn.pack(fill=tk.X)
        self.clearBtn = tk.Button(
            self.mngTableFrame,
            text="Clear all",
            command=self.clear_all_rows
            )
        self.clearBtn.pack(fill=tk.X)

        self.btnFrame = tk.Frame(self)
        self.btnFrame.grid(row=2, column=2, sticky="E")
        self.acceptBtn = tk.Button(
            self.btnFrame,
            text="Accept",
            command=self.save_and_exit
            )
        self.acceptBtn.pack(side=tk.RIGHT)
        self.bind("<Return>", self.save_and_exit)
        self.cancelBtn = tk.Button(
            self.btnFrame,
            text="Cancel",
            command=self.destroy
            )
        self.cancelBtn.pack(side=tk.RIGHT)
        self.bind("<Escape>", self.exit_without_saving)



        if len(self.lineExceptionVarsTmp) == 0:
            self.create_row()
        else:
            for row in range(len(self.lineExceptionVarsTmp)):
                self.place_row_widgets(row)


    def create_row(self):

        newRow = len(self.lineExceptionVarsTmp)
        self.lineExceptionVarsTmp.append((tk.StringVar(), tk.StringVar()))
        self.place_row_widgets(newRow)


    def place_row_widgets(self, row):

        var1, var2 = self.lineExceptionVarsTmp[row]
        self.lineExceptionEntries.append((
            tk.Entry(self.tableFrame, textvariable=var1),
            tk.Entry(self.tableFrame, textvariable=var2)
            ))
        for col, entry in enumerate(self.lineExceptionEntries[row]):
            entry.grid(row=row, column=col)


    def delete_last_row(self):

        if len(self.lineExceptionEntries) > 1:
            entry1, entry2 = self.lineExceptionEntries.pop()
            entry1.destroy()
            entry2.destroy()
            del self.lineExceptionVarsTmp[-1]


    def clear_all_rows(self):

        for row in range(len(self.lineExceptionEntries) - 1):
            self.delete_last_row()
        var1, var2 = self.lineExceptionVarsTmp[0]
        var1.set("")
        var2.set("")


    def save_and_exit(self, *args):

        # Iterate over the values from bottom to top and delete the empty rows
        # (backwards to make sure not to mess with next indices on deletion)
        for row, (var1, var2) in reversed(list(enumerate(self.lineExceptionVarsTmp))):
            if (var1.get() == var2.get() == ""):
                del self.lineExceptionVarsTmp[row]
        self.root.lineExceptionVars = self.lineExceptionVarsTmp[:]
        self.destroy()


    def exit_without_saving(self, *args):

        self.destroy()


def main():

    App = SetupMenu()
    App.mainloop()
    print("Done")

if __name__ == "__main__":
	main()




