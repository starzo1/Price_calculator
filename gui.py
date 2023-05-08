import logging
import pandas as pd
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
from calculation import markup_calculation
from file_utils import save_to_csv, build_df, create_df, combine_price_records
from utils import get_field_value, get_table_data


logging.basicConfig(filename="calculation.log", level=logging.ERROR, format="%(asctime)s:%(levelname)s:%(message)s")

root = Tk()
root.title("Pricing app")
root.geometry("653x400")
root.iconbitmap('usd.ico')
style = ttk.Style()
style.configure('W.TButton', font=('calibri', 10, 'bold', 'underline'), foreground='red', background='blue')
menu = Menu(root)
root.config(menu=menu)


import_file_var = StringVar()
export_folder_var = StringVar()

def set_status(text):
    status["text"] = text

def choose_file():
    file_path = fd.askopenfilename(initialdir="/", title="Select a file", filetypes=[("CSV Files", "*.csv")])
    import_file_var.set(file_path)

def choose_folder():
    folder_path = fd.askdirectory(initialdir="/", title="Select a folder")
    export_folder_var.set(folder_path)

def save_file_path():
    try:
        file_folder = export_folder_path.get()
        file_name = export_file_name.get()

        return f"{file_folder}/{file_name}.csv"

    except PermissionError:
        messagebox.showerror("Error", "Can't save file, no folder or file name selected")
        logging.exception('empty entries in save location')
        set_status("Check for empty save location entries")

def calculate():
    set_status("Calculating...")

    try:
        df_read = create_df(import_file_path.get())
        price_records = combine_price_records(df_read)
        table_data = {
            'a1': get_table_data('A', field_cost1, field1),
            'a2': get_table_data('A', field_cost2, field5),
            'a3': get_table_data('A', field_cost3, field9),
            'a4': get_table_data('A', field_cost3, field13),
            'b1': get_table_data('B', field_cost1, field2),
            'b2': get_table_data('B', field_cost2, field6),
            'b3': get_table_data('B', field_cost3, field10),
            'b4': get_table_data('B', field_cost3, field14),
            'c1': get_table_data('C', field_cost1, field3),
            'c2': get_table_data('C', field_cost2, field7),
            'c3': get_table_data('C', field_cost3, field11),
            'c4': get_table_data('C', field_cost3, field15),
            'd1': get_table_data('D', field_cost1, field4),
            'd2': get_table_data('D', field_cost2, field8),
            'd3': get_table_data('D', field_cost3, field12),
            'd4': get_table_data('D', field_cost3, field16),
        }
        taxes = {
            'vat': get_field_value(field_vat),
            'trnsp_cost': get_field_value(field_trnsp),
            'additional_cost': get_field_value(field_add_tax)
        }
        markup = markup_calculation(price_records, taxes, table_data)

        save_to_csv(save_file_path(), build_df(df_read, markup))
        set_status("Calculated!")

    except FileNotFoundError:
        messagebox.showerror("Error", "Can't open file, check if file exists")
        logging.exception('import file not found')
        set_status("Check if import file exists")

    except ValueError:
        messagebox.showerror("Error", "Can't calculate with zero values")
        logging.exception('empty entries error')
        set_status("Check settings")

    except UnboundLocalError:
        logging.exception('empty dataframe error')


def import_config():
    try:
        file_name = fd.askopenfilename(initialdir="/", title="Select a file", filetypes=[("CSV files", "*.csv")])
        df = pd.read_csv(file_name)
        set_status("Mark-up's imported")

    except FileNotFoundError:
        logging.exception('file not found importing settings')
        set_status("File not found!")

    settings = {
        'Cost': df["Cost"].values.tolist(),
        'Mark_up_a': df["Mark_up_a"].values.tolist(),
        'Mark_up_b': df["Mark_up_b"].values.tolist(),
        'Mark_up_c': df["Mark_up_c"].values.tolist(),
        'Mark_up_d': df["Mark_up_d"].values.tolist(),
    }

    i = -1
    for var0, var1, var2, var3, var4 in zip(cost_fields, fields_column_a, fields_column_b, fields_column_c, fields_column_d):
        i = i + 1
        var0.delete(0, END)
        var0.insert(0, settings['Cost'][i])
        var1.delete(0, END)
        var1.insert(0, settings['Mark_up_a'][i])
        var2.delete(0, END)
        var2.insert(0, settings['Mark_up_b'][i])
        var3.delete(0, END)
        var3.insert(0, settings['Mark_up_c'][i])
        var4.delete(0, END)
        var4.insert(0, settings['Mark_up_d'][i])

def export_config():
    file_name_csv = fd.asksaveasfilename(filetypes=[("CSV files", "*.csv")], defaultextension='.csv', confirmoverwrite=True)
    settings = {
        'Cost': [],
        'Mark_up_a': [],
        'Mark_up_b': [],
        'Mark_up_c': [],
        'Mark_up_d': [],
    }
   
    try:
        for cost, val_a, val_b, val_c, val_d in zip(cost_fields, fields_column_a, fields_column_b, fields_column_c, fields_column_d):
            settings['Cost'].append(cost.get())
            settings['Mark_up_a'].append(val_a.get())
            settings['Mark_up_b'].append(val_b.get())
            settings['Mark_up_c'].append(val_c.get())
            settings['Mark_up_d'].append(val_d.get())

        df = pd.DataFrame(settings)
        df.to_csv(file_name_csv, index=False, header=True)
        
        set_status("File exported succesfully")

    except FileNotFoundError:
        logging.exception('file not found exporting settings')

        return "cancelled"

def reset(): 
    fields = cost_fields + fields_column_a + fields_column_b + fields_column_c + fields_column_d  
    
    for var in fields:
        var.delete(0, END)
        
def close():
    root.destroy()

def help():
    messagebox.showinfo("info", "This is an example of short help how to use app.")

# Menu
#TODO: R
submenu = Menu(menu, tearoff=0)
helpmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=submenu)
submenu.add_command(label="Reset all fields", command=reset)
menu.add_cascade(label="Help", menu=helpmenu)
submenu.add_separator()
submenu.add_command(label="Close", command=close)
helpmenu.add_command(label="View help", command=help)
helpmenu.add_separator()
helpmenu.add_command(label="About pricing app", command=close)


# frames
frame1 = LabelFrame(root, text="Mark-up table", bg="#f7f8f5", fg="black", padx=36, pady=15)
frame1.grid(row=0, column=0)

frame2 = LabelFrame(root, text="File settings",bg="#b1b6a7", fg="black", padx=15, pady=15)
frame2.grid(row=1, column=0, columnspan=2)

frame3 = LabelFrame(root, text="Configs", bg="#eaece2", fg="black", padx=15, pady=42)
frame3.grid(row=0, column=1)

# Labels
lbl_turnover_group = ttk.Label(frame1, text="Turnover group", background="#f7f8f5")
lbl_turnover_group.grid(row=0, column=2, columnspan=2, sticky=N)

lbl_column_a = ttk.Label(frame1, text="A", background="#f7f8f5")
lbl_column_a.grid(row=1, column=1)

lbl_column_b = ttk.Label(frame1, text="B", background="#f7f8f5")
lbl_column_b.grid(row=1, column=2)

lbl_column_c = ttk.Label(frame1, text="C", background="#f7f8f5")
lbl_column_c.grid(row=1, column=3)

lbl_column_d = ttk.Label(frame1, text="D", background="#f7f8f5")
lbl_column_d.grid(row=1, column=4)

lbl_import_file_path = ttk.Label(frame2, text="Import file path", background="#b1b6a7")
lbl_import_file_path.grid(row=9, column=0, sticky=W)

lbl_file_name = ttk.Label(frame2, text="File name:", background="#b1b6a7")
lbl_file_name.grid(row=10, column=4)

lbl_calc_export_file_path = ttk.Label(frame2, text="Calculated file export path", background="#b1b6a7")
lbl_calc_export_file_path.grid(row=10, column=0)

lbl_csv = ttk.Label(frame2, text=".csv", background="#b1b6a7")
lbl_csv.grid(row=10, column=6, sticky=W)

lbl_unit_cost = Label(frame1, text="Unit cost (€)", background="#f7f8f5")
lbl_unit_cost.grid(row=1, column=0)

lbl_taxes = Label(frame3, text="Add. Taxes %")
lbl_taxes.grid(row=4, column=6, sticky=W)

lbl_vat = Label(frame3, text="VAT:")
lbl_vat.grid(row=5, column=5, sticky=E)

lbl_trnsp = Label(frame3, text="Trnsp.:")
lbl_trnsp.grid(row=6, column=5, sticky=E)

lbl_add_tax = Label(frame3, text="Add. Tax:")
lbl_add_tax.grid(row=7, column=5, sticky=E)

# Entry fields
field1 = ttk.Entry(frame1, width=10)
field1.grid(row=2, column=1)

field2 = ttk.Entry(frame1, width=10)
field2.grid(row=2, column=2)

field3 = ttk.Entry(frame1, width=10)
field3.grid(row=2, column=3)

field4 = ttk.Entry(frame1, width=10)
field4.grid(row=2, column=4, sticky=E)

field5 = ttk.Entry(frame1, width=10)
field5.grid(row=4, column=1)

field6 = ttk.Entry(frame1, width=10)
field6.grid(row=4, column=2)

field7 = ttk.Entry(frame1, width=10)
field7.grid(row=4, column=3)

field8 = ttk.Entry(frame1, width=10)
field8.grid(row=4, column=4, sticky=E)

field9 = ttk.Entry(frame1, width=10)
field9.grid(row=6, column=1)

field10 = ttk.Entry(frame1, width=10)
field10.grid(row=6, column=2)

field11 = ttk.Entry(frame1, width=10)
field11.grid(row=6, column=3)

field12 = ttk.Entry(frame1, width=10)
field12.grid(row=6, column=4, sticky=E)

field13 = ttk.Entry(frame1, width=10)
field13.grid(row=8, column=1)

field14 = ttk.Entry(frame1, width=10)
field14.grid(row=8, column=2)

field15 = ttk.Entry(frame1, width=10)
field15.grid(row=8, column=3)

field16 = ttk.Entry(frame1, width=10)
field16.grid(row=8, column=4)

field_cost1 = ttk.Entry(frame1, width=10)
field_cost1.grid(row=3, column=0, sticky=E)

field_cost2 = ttk.Entry(frame1, width=10)
field_cost2.grid(row=5, column=0, sticky=E)

field_cost3 = ttk.Entry(frame1, width=10)
field_cost3.grid(row=7, column=0, sticky=E)

#TODO: Rethink insert as init
field_vat = ttk.Entry(frame3, width=10)
field_vat.grid(row=5, column=6, sticky=W)
field_vat.insert(0, "21")

field_trnsp = ttk.Entry(frame3, width=10)
field_trnsp.grid(row=6, column=6, sticky=W)
field_trnsp.insert(0, "0")

field_add_tax = ttk.Entry(frame3, width=10)
field_add_tax.grid(row=7, column=6, sticky=W)
field_add_tax.insert(0, "0")

# import/export
import_file_path = ttk.Entry(frame2, width=30, textvariable=import_file_var)
import_file_path.grid(row=9, column=1, columnspan=2)

export_folder_path = ttk.Entry(frame2, width=30, textvariable=export_folder_var)
export_folder_path.grid(row=10, column=1, columnspan=2)

export_file_name = ttk.Entry(frame2, width=15)
export_file_name.grid(row=10, column=5)

# Buttons
btn_import_markup_cfg = ttk.Button(frame3, width=24, text="Import mark-ups", command=import_config)
btn_import_markup_cfg.grid(row=1, column=6, sticky=W)

btn_import_export_cfg = ttk.Button(frame3, width=24, text="Export mark-ups", command=export_config)
btn_import_export_cfg.grid(row=2, column=6, sticky=W)

btn_calculate = ttk.Button(frame2, text="CALCULATE", style='W.TButton', command=calculate)
btn_calculate.grid(row=12, column=0, sticky=W)

btn_browse_import_file = ttk.Button(frame2, width=17, text="Browse import file", command=choose_file)
btn_browse_import_file.grid(row=9, column=3, sticky=W)

btn_export_folder = ttk.Button(frame2, width=17, text="Export folder...", command=choose_folder)
btn_export_folder.grid(row=10, column=3, sticky=W)

status = Label(root, text="Waiting user input...",  bd=1, relief=SUNKEN, anchor=W)
status.grid(row=2, columnspan=8, sticky=W+E)

if __name__ == "__main__":
    fields_column_a = [field1, field5, field9, field13]
    fields_column_b = [field2, field6, field10, field14]
    fields_column_c = [field3, field7, field11, field15]
    fields_column_d = [field4, field8, field12, field16]
    cost_fields = [field_cost1, field_cost2, field_cost3, field_cost3]
    root.mainloop()
 
