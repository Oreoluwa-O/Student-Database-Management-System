#frontend
from tkinter import *
import tkinter.messagebox
import dbbackend

class StudentDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database Management System")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg="#1C1C1C")  # Black background for the main window

        # Initialize StringVar variables for form fields
        self.StdID = StringVar()
        self.Firstname = StringVar()
        self.Surname = StringVar()
        self.DoB = StringVar()
        self.Age = StringVar()
        self.Gender = StringVar()
        self.Address = StringVar()
        self.Mobile = StringVar()

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        MainFrame = Frame(self.root, bg="#2E2E2E")  # Dark gray for contrast
        MainFrame.grid()

        # Title frame
        TitFrame = Frame(MainFrame, bd=2, padx=54, pady=8, bg="#FF4C4C", relief=RIDGE)  # Red background
        TitFrame.pack(side=TOP)
        lblTit = Label(TitFrame, font=('times new roman', 48, 'bold'), text="Student Database Management System", bg="#FF4C4C", fg="#1C1C1C")
        lblTit.grid()

        # Button frame
        ButtonFrame = Frame(MainFrame, bd=2, width=1350, height=70, padx=19, pady=10, bg="#FF4C4C", relief=RIDGE)
        ButtonFrame.pack(side=BOTTOM)

        # Data frame
        DataFrame = Frame(MainFrame, bd=1, width=1300, height=400, padx=20, pady=20, relief=RIDGE, bg="#2E2E2E")
        DataFrame.pack(side=BOTTOM)

        # Left data frame for form inputs
        DataFrameLEFT = LabelFrame(DataFrame, bd=1, width=1000, height=600, padx=20, relief=RIDGE, bg="#FF4C4C", font=('times new roman', 26, 'bold'), text="Student Info\n", fg="#1C1C1C")
        DataFrameLEFT.pack(side=LEFT)

        # Right data frame for listbox
        DataFrameRIGHT = LabelFrame(DataFrame, bd=1, width=450, height=300, padx=31, pady=3, relief=RIDGE, bg="#FF4C4C", font=('times new roman', 20, 'bold'), text="Student Details\n", fg="#1C1C1C")
        DataFrameRIGHT.pack(side=RIGHT)

        # Form fields
        self.create_form_fields(DataFrameLEFT)

        # Listbox and scrollbar
        self.create_listbox(DataFrameRIGHT)

        # Buttons
        self.create_buttons(ButtonFrame)

    def create_form_fields(self, parent):
        # Create form fields with labels and entry boxes
        labels = ["Student ID:", "Firstname:", "Surname:", "Date of Birth:", "Age:", "Gender:", "Address:", "Mobile:"]
        variables = [self.StdID, self.Firstname, self.Surname, self.DoB, self.Age, self.Gender, self.Address, self.Mobile]

        for i, (label_text, var) in enumerate(zip(labels, variables)):
            label = Label(parent, font=('times new roman', 20, 'bold'), text=label_text, padx=2, pady=2, bg="#FF4C4C", fg="#1C1C1C")
            label.grid(row=i, column=0, sticky=W)
            entry = Entry(parent, font=('times new roman', 20, 'bold'), textvariable=var, width=39)
            entry.grid(row=i, column=1)

    def create_listbox(self, parent):
        # Create listbox with scrollbar
        scrollbar = Scrollbar(parent)
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.studentlist = Listbox(parent, width=41, height=16, font=('times new roman', 12, 'bold'), yscrollcommand=scrollbar.set, bg="#FF4C4C", fg="#1C1C1C")
        self.studentlist.bind('<<ListboxSelect>>', self.StudentRec)
        self.studentlist.grid(row=0, column=0, padx=8)
        scrollbar.config(command=self.studentlist.yview)

    def create_buttons(self, parent):
        # Create buttons with associated commands
        buttons = [
            ("Add New", self.addData),
            ("Display", self.DisplayData),
            ("Clear", self.clearData),
            ("Delete", self.DeleteData),
            ("Search", self.searchDatabase),
            ("Update", self.update),
            ("Exit", self.iExit)
        ]

        for i, (text, command) in enumerate(buttons):
            button = Button(parent, text=text, font=('times new roman', 20, 'bold'), height=1, width=10, bd=4, command=command, bg="#1C1C1C", fg="#FF4C4C")
            button.grid(row=0, column=i)

    def iExit(self):
        # Exit the application
        if tkinter.messagebox.askyesno("Student Database Management Systems", "Confirm if you want to exit"):
            self.root.destroy()

    def clearData(self):
        # Clear all form fields
        for var in [self.StdID, self.Firstname, self.Surname, self.DoB, self.Age, self.Gender, self.Address, self.Mobile]:
            var.set("")

    def addData(self):
        # Add new student record
        if self.StdID.get():
            dbbackend.addStdRec(self.StdID.get(), self.Firstname.get(), self.Surname.get(), self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get())
            self.studentlist.delete(0, END)
            self.studentlist.insert(END, (self.StdID.get(), self.Firstname.get(), self.Surname.get(), self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get()))

    def DisplayData(self):
        # Display all student records
        self.studentlist.delete(0, END)
        for row in dbbackend.viewData():
            self.studentlist.insert(END, row)

    def StudentRec(self, event):
        # Populate form fields with selected record
        searchStd = self.studentlist.curselection()[0]
        sd = self.studentlist.get(searchStd)

        self.StdID.set(sd[1])
        self.Firstname.set(sd[2])
        self.Surname.set(sd[3])
        self.DoB.set(sd[4])
        self.Age.set(sd[5])
        self.Gender.set(sd[6])
        self.Address.set(sd[7])
        self.Mobile.set(sd[8])

    def DeleteData(self):
        # Delete selected student record
        if self.StdID.get():
            dbbackend.deleteRec(self.StdID.get())
            self.clearData()
            self.DisplayData()

    def searchDatabase(self):
        # Search for student records
        self.studentlist.delete(0, END)
        for row in dbbackend.searchData(self.StdID.get(), self.Firstname.get(), self.Surname.get(), self.DoB.get(), self.Age.get(), self.Gender.get(), self.Address.get(), self.Mobile.get()):
            self.studentlist.insert(END, row)

    def update(self):
        # Update selected student record
        if self.StdID.get():
            selected_index = self.studentlist.curselection()[0]
            selected_record = self.studentlist.get(selected_index)
            record_id = selected_record[0]  # Assuming the ID is the first element

            dbbackend.dataUpdate(
                record_id,
                self.StdID.get(),
                self.Firstname.get(),
                self.Surname.get(),
                self.DoB.get(),
                self.Age.get(),
                self.Gender.get(),
                self.Address.get(),
                self.Mobile.get()
            )
            self.DisplayData()

if __name__ == '__main__':
    root = Tk()
    app = StudentDatabaseApp(root)
    root.mainloop()
