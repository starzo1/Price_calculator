import logging
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from calculation import markup_calculation, save_to_csv, read_file, config_import_strip


logging.basicConfig(filename="calculation.log", level=logging.ERROR, format="%(asctime)s:%(levelname)s:%(message)s")

root = Tk()
root.title("Pricing app")
root.geometry("653x400")
root.iconbitmap('usd.ico')
style = ttk.Style()
menu = Menu(root)
submenu = Menu(menu, tearoff=0)
helpmenu = Menu(menu, tearoff=0)
root.config(menu=menu)
#frames
frame1 = LabelFrame(root, text="Mark-up table", bg="#f7f8f5", fg="black", padx=36, pady=15)
frame1.grid(row=0, column=0)
frame2 = LabelFrame(root, text="File settings", bg="#b1b6a7", fg="black", padx=15, pady=15)
frame2.grid(row=1, column=0, columnspan=2)
frame3 = LabelFrame(root, text="Configs", bg="#eaece2", fg="black", padx=15, pady=42)
frame3.grid(row=0, column=1)
#saved locations
import_file_var = StringVar()
export_folder_var = StringVar()


def choose_file():
    file_path = fd.askopenfilename(initialdir="/", title="Select a file", filetypes=[("CSV Files", "*.csv")])
    import_file_var.set(file_path)
    
def choose_folder():
    
    folder_path = fd.askdirectory(initialdir="/", title="Select a folder")
    export_folder_var.set(folder_path)

def file_save_path():
    try:
        file_folder = export_file_path.get()
        file_name = export_file_name.get()
        full_path = f"{file_folder}/{file_name}.csv"
        return full_path
    
    except PermissionError:
        messagebox.showerror("Error", "Can't save file, no folder or file name selected")
        logging.exception('empty entries in save location')
        status["text"] = "Check for empty save location entries"  
        
def calculate():
    #nuskaito pasirinkta faila #padaryti try except jei koks value error
    status["text"] = "Calculating..."
    try: 
        path = import_file_path.get()
        df_read = read_file(path)
    except FileNotFoundError:  
        messagebox.showerror("Error", "Can't open file, check if file exists")
        logging.exception('import file not found')
        status["text"] = "Check if import file exists"  
    #paimami visi uzpildyti laukeliai
    try:
        cost1 = float(field_cost1.get())
        cost2 = float(field_cost2.get()) 
        cost3 = float(field_cost3.get())
        vat = float(field_vat.get())
        trnsp_cost = float(field_trnsp.get())
        additional_cost = float(field_add_tax.get())
        additional_taxes = (1+vat/100) * (1+trnsp_cost/100) * (1+additional_cost/100)
        #A
        value_a1 = ["A", cost1, float(field1.get())/100]
        value_a2 = ["A", cost2, float(field5.get())/100]
        value_a3 = ["A", cost3, float(field9.get())/100]
        value_a4 = ["A", cost3, float(field13.get())/100]
        #B
        value_b1 = ["B", cost1, float(field2.get())/100]
        value_b2 = ["B", cost2, float(field6.get())/100]
        value_b3 = ["B", cost3, float(field10.get())/100]
        value_b4 = ["B", cost3, float(field14.get())/100]
        #C
        value_c1 = ["C", cost1, float(field3.get())/100]
        value_c2 = ["C", cost2, float(field7.get())/100]
        value_c3 = ["C", cost3, float(field11.get())/100]
        value_c4 = ["C", cost3, float(field15.get())/100]
        #D
        value_d1 = ["D", cost1, float(field4.get())/100]
        value_d2 = ["D", cost2, float(field8.get())/100]
        value_d3 = ["D", cost3, float(field12.get())/100]
        value_d4 = ["D", cost3, float(field16.get())/100]
       
        #skaiciavimo funkcija
        markup_calculation(df_read, value_a1, value_a2, value_a3, value_a4, value_b1, value_b2, value_b3, value_b4, value_c1, value_c2, value_c3, value_c4, value_d1, value_d2, value_d3, value_d4, additional_taxes)
        save_to_csv(file_save_path())
        status["text"] = "Calculated!"
        
    except ValueError:
        messagebox.showerror("Error", "Can't calculate with zero values")
        logging.exception('empty entries error')
        status["text"] = "Check settings"
   
    except UnboundLocalError:
        logging.exception('empty dataframe error')
    
def import_config():
    file_name = fd.askopenfilename(initialdir="/", title="Select a file", filetypes=[("Text files", "*.txt")])
    fields1 = [field_cost1, field1, field2, field3, field4]
    fields2 = [field_cost2, field5, field6, field7, field8]
    fields3 = [field_cost3, field9, field10, field11, field12]
    fields4 = [field13, field14, field15, field16]
    
    try:
        with open(file_name, 'r') as file_object:
            lines = file_object.readlines()
            line1 = lines[0]
            line2 = lines[1]
            line3 = lines[2]
            line4 = lines[3]
            status["text"] = "Mark-up's imported"
    except FileNotFoundError:
        logging.exception('file not found importing settings')
        status["text"] = "File not found!"
    
    i = -1
    for var in fields1:
        i = i + 1
        var.delete(0, END)
        var.insert(0, config_import_strip(line1)[i])
    z = -1
    for var in fields2:
        z = z + 1
        var.delete(0, END)
        var.insert(0, config_import_strip(line2)[z])
    c = -1
    for var in fields3:
        c = c + 1
        var.delete(0, END)
        var.insert(0, config_import_strip(line3)[c])
    d = -1
    for var in fields4:
        d = d + 1
        var.delete(0, END)
        var.insert(0, config_import_strip(line4)[d])
    
def export_config():
    file_name = fd.asksaveasfilename(filetypes=[("Text files", "*.txt")], defaultextension='.txt', confirmoverwrite=True)
    my_markup_settings = [
                        (field_cost1, field1, field2, field3, field4),
                        (field_cost2, field5, field6, field7, field8 ),
                        (field_cost3, field9, field10, field11, field12 ),
                        (field_cost3, field13, field14, field15, field16)
    ]
    try:
        with open(file_name, 'w') as file_object:
            for line in my_markup_settings:
                lines = ()
                for entry in line:
                    lines = lines + (entry.get(),)
                file_object.write(f"{lines}\n")  
        status["text"] = "Settings saved to file"
    except FileNotFoundError:
        logging.exception('file not found exporting settings')
        return "cancelled"
    
 
def reset():
    reset_fields = [
                    field_cost1, field1, field2, field3, field4,
                    field_cost2, field5, field6, field7, field8,
                    field_cost3, field9, field10, field11, field12,
                    field13, field14, field15, field16
    ]
    for var in reset_fields:
        var.delete(0, END)

def close():
    root.destroy()
    
def help():
    messagebox.showinfo("info", "This is an example of short help how to use app.")

#Menu
menu.add_cascade(label="View", menu=submenu)
menu.add_cascade(label="Help", menu=helpmenu)
submenu.add_command(label="Reset all fields", command=reset)
submenu.add_separator()
submenu.add_command(label="Close", command=close)
helpmenu.add_command(label="View help", command=help)
helpmenu.add_separator()
helpmenu.add_command(label="About pricing app", command=close)
 
#Labels  
label1 = ttk.Label(frame1, text="Turnover group")
label2 = ttk.Label(frame1, text="A")
label3 = ttk.Label(frame1, text="B")
label4 = ttk.Label(frame1, text="C")
label5 = ttk.Label(frame1, text="D")
label8 = ttk.Label(frame2, text="Import file path")
label9 = ttk.Label(frame2, text="File name:")
label10 = ttk.Label(frame2, text="Calculated file export path")
label11 = ttk.Label(frame2, text=".csv")
label_cost1 = Label(frame1, text="Unit cost (€)")
label_mokesciai = Label(frame3, text="Add. Taxes %")
label_vat = Label(frame3, text="VAT:")
label_trnsp = Label(frame3, text="Trnsp.:")
label_add_tax = Label(frame3, text="Add. Tax:")

#Entry fields
field1 = ttk.Entry(frame1, width=10)
field2 = ttk.Entry(frame1, width=10)
field3 = ttk.Entry(frame1, width=10)
field4 = ttk.Entry(frame1, width=10)
field5 = ttk.Entry(frame1, width=10)
field6 = ttk.Entry(frame1, width=10)
field7 = ttk.Entry(frame1, width=10)
field8 = ttk.Entry(frame1, width=10)
field9 = ttk.Entry(frame1, width=10)
field10 = ttk.Entry(frame1, width=10)
field11 = ttk.Entry(frame1, width=10)
field12 = ttk.Entry(frame1, width=10)
field13 = ttk.Entry(frame1, width=10)
field14 = ttk.Entry(frame1, width=10)
field15 = ttk.Entry(frame1, width=10)
field16 = ttk.Entry(frame1, width=10)
field_cost1 = ttk.Entry(frame1, width=10)
field_cost2 = ttk.Entry(frame1, width=10)
field_cost3 = ttk.Entry(frame1, width=10)
field_cost1.insert(0, "120")
field_cost2.insert(0, "250")
field_cost3.insert(0, "450")
field_vat = ttk.Entry(frame3, width=10)
field_vat.insert(0, "21")
field_trnsp = ttk.Entry(frame3, width=10)
field_trnsp.insert(0, "0")
field_add_tax = ttk.Entry(frame3, width=10)
field_add_tax.insert(0, "0")

#import/export
import_file_path = ttk.Entry(frame2, width=30, textvariable=import_file_var)
export_file_path = ttk.Entry(frame2, width=30, textvariable=export_folder_var)
export_file_name = ttk.Entry(frame2, width=15)

#Buttons
button = ttk.Button(frame3, width=24, text="Import mark-up config", command=import_config)
button4 = ttk.Button(frame3, width=24, text="Export mark-up config", command=export_config)
button1 = ttk.Button(frame2, text="CALCULATE", style = 'W.TButton', command=calculate)
button2 = ttk.Button(frame2, width=17, text="Browse import file", command=choose_file)
button3 = ttk.Button(frame2, width=17, text="Export folder...", command=choose_folder)
status = Label(root, text="Waiting user input...", bd=1, relief=SUNKEN, anchor=W)

#Button styles
style.configure('W.TButton', font =
               ('calibri', 10, 'bold', 'underline'),
                foreground = 'red', background = 'blue')

#Placing in grid
label1.grid(row=0, column=2, columnspan=2, sticky=N)
label2.grid(row=1, column=1)
label3.grid(row=1, column=2)
label4.grid(row=1, column=3)
label5.grid(row=1, column=4)
label8.grid(row=9, column=0, sticky=W)
label9.grid(row=10, column=4)
label10.grid(row=10, column=0)
label11.grid(row=10, column=6, sticky=W)
label_mokesciai.grid(row=4, column=6, sticky=W)
label_vat.grid(row=5, column=5, sticky=E)
label_trnsp.grid(row=6, column=5, sticky=E)
label_add_tax.grid(row=7, column=5, sticky=E)

field1.grid(row=2, column=1)
field2.grid(row=2, column=2)
field3.grid(row=2, column=3)
field4.grid(row=2, column=4, sticky=E)
field5.grid(row=4, column=1)
field6.grid(row=4, column=2)
field7.grid(row=4, column=3)
field8.grid(row=4, column=4, sticky=E)
field9.grid(row=6, column=1)
field10.grid(row=6, column=2)
field11.grid(row=6, column=3)
field12.grid(row=6, column=4, sticky=E)
field13.grid(row=8, column=1)
field14.grid(row=8, column=2)
field15.grid(row=8, column=3)
field16.grid(row=8, column=4, sticky=E)

label_cost1.grid(row=1, column=0)
field_cost1.grid(row=3, column=0, sticky=E)
field_cost2.grid(row=5, column=0, sticky=E)
field_cost3.grid(row=7, column=0, sticky=E)
field_vat.grid(row=5, column=6, sticky=W)
field_trnsp.grid(row=6, column=6, sticky=W)
field_add_tax.grid(row=7, column=6, sticky=W)

export_file_path.grid(row=10, column=1, columnspan=2)
import_file_path.grid(row=9, column=1, columnspan=2)
export_file_name.grid(row=10, column=5)

button.grid(row=1, column=6, sticky=W)
button4.grid(row=2, column=6, sticky=W)
button1.grid(row=12, column=0, sticky=W)
button2.grid(row=9, column=3, sticky=W)
button3.grid(row=10, column=3, sticky=W)
status.grid(row=2, columnspan=8, sticky=W+E)


if __name__ == "__main__":
    root.mainloop()
