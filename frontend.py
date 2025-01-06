import os
import backend as backend
import customtkinter as ctk
from tkinter import filedialog
from openpyxl import Workbook, load_workbook

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master)        
        
        valuesdict = {"Any": "Any", "$0-$10": [0,10], "$10-$25": [10,25], "$25-$50": [25,50], "$50-$100": [50,100], "$100-$500": [100,500], "$500-$1000": [500,1000],}
                
        self.width = self.winfo_width()
        self.height = self.winfo_height()
                
        self.configure(width=width, height=height) #border_width=3, border_color="red"
        
        # Brand Textbox
        
        self.brand_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Brand",
            width=width,
            height=30,
        )
        
        self.brand_textbox.grid(
            column=0,
            row=0,
            pady=(0,10)
        )
        
        # Year Textbox
        
        self.year_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Year",
            width=width,
            height=30,
        )
        
        self.year_textbox.grid(
            column=0,
            row=1,
            pady=(0,10)
        )
        
        # Min Quantity Textbox
        
        self.min_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Min Quantity",
            width=width,
            height=30,
        )

        self.min_textbox.grid(
            column=0,
            row=2,
            pady=(0,10)
        )
        
        # Max Quantity Textbox
        
        self.max_textbox = ctk.CTkEntry(
            self,
            width=width,
            placeholder_text="Max Quantity",
            height=30,
        )

        self.max_textbox.grid(
            column=0,
            row=3,
        )
        
        # Scale Menu
        
        self.scale_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Scale",
            font=("Arial", 16)
        )
        
        self.scale_menu_textbox.grid(
            column=0,
            row=4
        )
        
        self.scale_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["Any", "1:12", "1:18", "1:24", "1:34", "1:36", "1:48"]
        )
        
        self.scale_menu.grid(
            column=0,
            row=5,
        )
        
        # Value Menu
        
        self.value_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Value",
            font=("Arial", 16)
        )
        
        self.value_menu_textbox.grid(
            column=0,
            row=6
        )
        
        self.value_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["Any", "$0-$10", "$10-$25", "$25-$50", "$50-$100", "$100-$500", "$500-$1000"]
        )
        
        self.value_menu.grid(
            column=0,
            row=7,
        )
        
        # Condition Menu
        
        self.condition_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Condition",
            font=("Arial", 16)
        )
        
        self.condition_menu_textbox.grid(
            column=0,
            row=8,
        )
        
        self.condition_menu = ctk.CTkComboBox(
            self,
            width=width,
            values=["Any", "sealed", "opened"]
        )
        
        self.condition_menu.set("Any")
        
        self.condition_menu.grid(
            column=0,
            row=9,
            pady=(0,10)
        )
        
        # Search Button
        
        self.search_button = ctk.CTkButton(
            self,
            text="Search",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.winfo_toplevel().button_font,
            command=lambda: self.search_request(
                self.scale_menu.get(),
                valuesdict[self.value_menu.get()],
                self.condition_menu.get(),
                self.brand_textbox.get(),
                self.year_textbox.get(),
                self.min_textbox.get(),
                self.max_textbox.get()
                )
        )
        
        self.search_button.grid(
            column=0,
            row=11,
        )
        
        self.export_button = ctk.CTkButton(
            self,
            text="Export Results",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.winfo_toplevel().button_font,
            state="disabled",
            command=lambda: self.export_results()
        )
        
        self.export_button.grid(
            column=0,
            row=13,
            pady=(10,0)
        )

    def search_request(self, *args):
        #print(f"{scale}, {value}, {condition}, {brand}, {year}, {minQ}, {maxQ}")
        
        attributes=["scale", "value", "condition", "brand", "year", "min", "max"]
        
        print(args)
        
        arguments={}
        
        for attribute in attributes:
            arguments[attribute] = None
           
        arguments["min"] = 0
        arguments["max"] = 1000
        
           
        for i in range(len(args)):
            if(len(args[i]) != 0 and args[i] != "Any"):
                
                arguments[attributes[i]] = args[i]   
                
        # print(args)
        # print(arguments)
      
        search_query=f"SELECT * FROM models \nWHERE quantity BETWEEN {arguments['min']} AND {arguments['max']}"
        
        for key in arguments:
            if arguments[key] is not None:
                if(key == "value"):
                    print(arguments[key])
                    search_query = search_query + f"\nAND {key} BETWEEN {arguments[key][0]} AND {arguments[key][1]}"
                   
                else:
                    
                    if key != "min" and key != 'max':
                        
                        search_query = search_query + f"\nAND {key}='{arguments[key]}'"
                    
        #print(search_query)
        
        results = backend.execute_query(search_query)
        
        #print(results)
        
        self.master.queryresults = results
        
        self.master.main_window.display_query(self.master.queryresults)
        
        if len(results) > 0:
            self.export_button.configure(state="normal")
        else:
            self.export_button.configure(state="disabled")
            
    def export_results(self):
        
        query_valuee = 0.0
        
        saveFile = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel - *.xlsx", "*.xlsx")])
        
        if saveFile is None:
            return
            
        work_book = Workbook()
        
        work_sheet = work_book.active
        
        work_sheet.append(['ID', 'BRAND', 'YEAR', 'DESCRIPTION', 'SCALE', 'CONDITION', 'QUANTITY', 'VALUE', '', 'TOTAL VALUE'])
            
        for result in self.master.queryresults:
            
            query_valuee = query_valuee + result[7]
            
            work_sheet.append(result)
                
        work_sheet['J2'] = f"${query_valuee}"
                
        work_book.save(saveFile)
  
        
class QueryWindow(ctk.CTkFrame):
    def __init__(self, master, width, height):
        super().__init__(master)
        
        self.configure(width=width, height=height, border_width=3, border_color="red")

 
class MainWindow(ctk.CTkScrollableFrame):
    def __init__(self, master, width, height):
        super().__init__(master)
        
        self.models = []
        
        #, border_width=3, border_color="red"
        
        self.configure(width=width, height=height)
        
        # self.querywindow = QueryWindow(self, width, height)
        # self.querywindow.pack(pady=0, padx=0)
        
    def display_query(self, queryresults) -> list:
        
        if len(self.models) > 0:
            for i in range(len(self.models)):
                self.models[i].destroy()
                
        label = ctk.CTkLabel(self, text=f"{'ID' : >4}: {'BRAND'  : <12} {'YEAR' : <4} {'SCALE' : <5} {'CONDITION' : <9} {'QUANTITY' : <8} {'VALUE' : <5}", font=("Courier", 16))
        
        label.grid(row=0, column=0, pady=(0,5), sticky="w")

        for j in range(1, len(queryresults)):
           
            i = j - 1
           
            label = ctk.CTkLabel(self, text=f"{queryresults[i][0] : >4}: {queryresults[i][1]  : <12} {queryresults[i][2] : <4} {queryresults[i][4] : <5} {queryresults[i][5] : <9} {queryresults[i][6] : <8} ${queryresults[i][7] : <5}", font=("Courier", 16))
            
            self.models.append(label)     
            
            label.grid(row=j+1, column=0, pady=(0,5), sticky="w")
            
# Main App Class. Variables stored here are able to be used by all children of the class.            

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        AppWidth=1000
        AppHeight=600
        
        self.queryresults = []
        self.queryresultsvalue = None
        
        self.resizable(False, False)
        
        backend.create_table(backend.creation_query)
        
        ctk.set_appearance_mode('dark')
        self.title('Model Car Catalogue')
        self.geometry(f'{AppWidth}x{AppHeight}')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.title_font = ctk.CTkFont(
            family="Arial",
            size=40,
            weight='bold'
        )
        
        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=18
        )
        
        self.body_font = ctk.CTkFont(
            family="Helvetica",
            size=16
        )
        
        # Sidebar
        self.sidebar = Sidebar(self, 250, 600)
        self.sidebar.grid(
            column=0,
            row=0,
            padx=(10, 5),
            pady=10,
            sticky="ns"
        )
        
        # Main Window
        self.main_window = MainWindow(self, AppWidth - self.sidebar.width, AppHeight - self.sidebar.height - 200)
        self.main_window.grid(
            column=1,
            row=0,
            padx=(5, 10),
            pady=10,
            sticky="nsew"
        )
        
        
            
    