"Frontend of database application."

from tkinter import filedialog
import customtkinter as ctk
from openpyxl import Workbook
import backend


class Sidebar(ctk.CTkFrame):

    "Sidebar for querying database."

    def __init__(self, master, width, height):

        "Construct layout with any needed variables."

        super().__init__(master)

        font = self.master.body_font

        valuesdict = {
            "Any": "Any",
            "$0-$10": [0,10],
            "$10-$25": [10,25],
            "$25-$50": [25,50],
            "$50-$100": [50,100],
            "$100-$500": [100,500],
            "$500-$1000": [500,1000]
            }

        self.width = self.winfo_width()
        self.height = self.winfo_height()

        self.configure(width=width, height=height)

        # Brand Textbox

        brand_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Brand",
            width=width,
            height=30,
        )

        brand_textbox.grid(
            column=0,
            row=0,
            pady=(0,10)
        )

        # Year Textbox

        year_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Year",
            width=width,
            height=30,
        )

        year_textbox.grid(
            column=0,
            row=1,
            pady=(0,10)
        )

        # Min Quantity Textbox

        min_textbox = ctk.CTkEntry(
            self,
            placeholder_text="Min Quantity",
            width=width,
            height=30,
        )

        min_textbox.grid(
            column=0,
            row=2,
            pady=(0,10)
        )

        # Max Quantity Textbox

        max_textbox = ctk.CTkEntry(
            self,
            width=width,
            placeholder_text="Max Quantity",
            height=30,
        )

        max_textbox.grid(
            column=0,
            row=3,
        )

        # Scale Menu

        scale_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Scale",
            font=font
        )

        scale_menu_textbox.grid(
            column=0,
            row=4
        )

        scale_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["Any", "1:12", "1:18", "1:24", "1:34", "1:36", "1:48"]
        )

        scale_menu.grid(
            column=0,
            row=5,
        )

        # Value Menu

        value_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Value",
            font=font
        )

        value_menu_textbox.grid(
            column=0,
            row=6
        )

        value_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["Any", "$0-$10", "$10-$25", "$25-$50", "$50-$100", "$100-$500", "$500-$1000"]
        )

        value_menu.grid(
            column=0,
            row=7,
        )

        # Condition Menu

        condition_menu_textbox = ctk.CTkLabel(
            self,
            height=30,
            width=width,
            text="Condition",
            font=font
        )

        condition_menu_textbox.grid(
            column=0,
            row=8,
        )

        condition_menu = ctk.CTkComboBox(
            self,
            width=width,
            values=["Any", "sealed", "opened"]
        )

        condition_menu.set("Any")

        condition_menu.grid(
            column=0,
            row=9,
            pady=(0,10)
        )

        # Search Button

        self.search_button = ctk.CTkButton(
            self,
            text="Search Catalogue",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            command=lambda: self.search_request(
                scale_menu.get(),
                valuesdict[value_menu.get()],
                condition_menu.get(),
                brand_textbox.get(),
                year_textbox.get(),
                min_textbox.get(),
                max_textbox.get()
                )
        )

        self.search_button.grid(
            column=0,
            row=11,
        )

        # Export Button

        self.export_button = ctk.CTkButton(
            self,
            text="Export Results",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            state="disabled",
            command=lambda: self.export_results()
        )

        self.export_button.grid(
            column=0,
            row=13,
            pady=(10,0)
        )

        # Edit Button

        self.edit_button = ctk.CTkButton(
            self,
            text="Edit Catalogue",
            width=width,
            fg_color=self.master.button_color,
            hover_color=self.master.button_hover_color,
            font=self.winfo_toplevel().button_font,
            command=lambda: self.edit_catalogue()
        )

        self.edit_button.grid(
            column=0,
            row=14,
            pady=(10,0)
        )

    def search_request(self, *args):

        "Construct search query to be passed to execute_query()."

        #print(f"{scale}, {value}, {condition}, {brand}, {year}, {minQ}, {maxQ}")

        attributes=["scale", "value", "condition", "brand", "year", "min", "max"]

        #print(args)

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

        search_query=(
            "SELECT * FROM models \nWHERE quantity BETWEEN "
            f"{arguments['min']} AND {arguments['max']}"
        )

        for key in arguments:
            if arguments[key] is not None:
                if key == "value":
                    #print(arguments[key])
                    search_query = (
                        search_query +
                        f"\nAND {key} BETWEEN {arguments[key][0]} AND {arguments[key][1]}"
                    )

                else:

                    if key != "min" and key != 'max':

                        search_query = search_query + f"\nAND {key}='{arguments[key]}'"

        #print(search_query)

        results = backend.execute_query(search_query)

        #print(results)

        self.master.queryresults = results

        self.master.main_window.display_query(self.master.queryresults)

        if len(results) > 0:
            self.export_button.configure(state="enabled")
        else:
            self.export_button.configure(state="disabled")

    def export_results(self):

        "Export App.queryresults to .xslx file."

        query_value = 0.0

        saveFile = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[("Excel - *.xlsx", "*.xlsx")]
        )

        if saveFile is None:
            return

        work_book = Workbook()

        work_sheet = work_book.active

        work_sheet.append([
            'ID',
            'BRAND',
            'YEAR',
            'DESCRIPTION',
            'SCALE',
            'CONDITION',
            'QUANTITY',
            'VALUE',
            '',
            'TOTAL VALUE'
        ])

        for result in self.master.queryresults:

            if result[7] is not None:

                query_value = query_value + (result[7])

                work_sheet.append(result)

        work_sheet['J2'] = f"${query_value}"

        work_book.save(saveFile)

    def edit_catalogue(self):

        "Toggle sidebar buttons and create EditWindow object."

        edit_window = EditWindow(self)

        self.edit_button.configure(state='disabled')
        self.search_button.configure(state='disabled')
        self.export_button.configure(state='disabled')

class EditWindow(ctk.CTkToplevel) :

    "Secondary window for editing database entries."

    def __init__(self,master):

        "Construct layout for window as well as needed variables."

        super().__init__(master)

        self.attribute = ([
            "Brand",
            "Year",
            "Description",
            "Quantity",
            "Value",
            "Scale",
            "Condition"
        ])

        self.attribute_list = []

        self.button_font = ctk.CTkFont(
            family="Helvetica",
            size=18
        )

        width=250
        height=450

        self.title('Edit Catalogue')
        self.geometry(f'{width}x{height}')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.attributes('-topmost', True)

        self.resizable(False, False)

        for i in range(len(self.attribute) - 2):

            self.attribute_textbox = ctk.CTkEntry(
                self,
                placeholder_text=f'{self.attribute[i]}',
                width=width,
                height=30,
            )

            self.attribute_textbox.grid(
                column=0,
                row=i,
                pady=(0,10)
            )

            self.attribute_list.append(self.attribute_textbox)

        self.scale_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["1:12", "1:18", "1:24", "1:34", "1:36", "1:48"]
        )

        self.scale_menu.grid(
            column=0,
            row=7,
        )

        self.condition_menu= ctk.CTkComboBox(
            self,
            width=width,
            height=30,
            values=["sealed", "opened"]
        )

        self.condition_menu.grid(
            column=0,
            row=8,
        )

        self.attribute_list.append(self.scale_menu)
        self.attribute_list.append(self.condition_menu)

        self.add_button = ctk.CTkButton(
            self,
            text="Add Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command=lambda: backend.add_model(
                self.attribute_list[1].get(),
                self.attribute_list[2].get(),
                self.scale_menu.get(),
                self.condition_menu.get(),
                self.attribute_list[4].get(),
                self.attribute_list[3].get(),
                self.attribute_list[5].get()
            )
        )

        self.add_button.grid(
            column=0,
            row=9,
            pady=(10,0)
        )

        self.update_button = ctk.CTkButton(
            self,
            text="Update Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command=lambda: backend.update_model(
                self.attribute_list[0].get(),
                self.attribute_list[1].get(),
                self.attribute_list[2].get(),
                self.scale_menu.get(),
                self.condition_menu.get(),
                self.attribute_list[4].get(),
                self.attribute_list[3].get(),
                self.attribute_list[5].get()
            )
        )

        self.update_button.grid(
            column=0,
            row=10,
            pady=(10,0)
        )

        self.delete_button = ctk.CTkButton(
            self,
            text="Delete Model",
            width=width,
            fg_color="#4ab1ff",
            hover_color="#286b9e",
            font=self.button_font,
            command = lambda: backend.delete_model(self.attribute_list[0].get())
        )

        self.delete_button.grid(
            column=0,
            row=11,
            pady=(10,0)
        )

        self.protocol('WM_DELETE_WINDOW', self.close)

    def close(self):

        "Toggle sidebar buttons and destroy window on close."

        self.master.edit_button.configure(state='enabled')
        self.master.search_button.configure(state='enabled')
        self.master.export_button.configure(state='enabled')

        self.destroy()


class MainWindow(ctk.CTkScrollableFrame):

    "Window class to display and filter query results."

    def __init__(self, master, width, height):

        "Set needed variables as well as preloaded buttons and text."

        super().__init__(master)

        self.master = master

        # list to

        self.models = []

        self.configure(width=width, height=height)

        # Main Window text and buttons are loaded on init,
        # rather than reloaded each time display_query() is called.

        label = ctk.CTkLabel(
            self,
            text=f"{'ID' : >4}: {'BRAND'  : <12} {'YEAR' : <4} {'SCALE' : <5} {'CONDITION' : <9} {'QUANTITY' : <8} {'VALUE' : <5}", font=("Courier", 16))

        label.grid(row=1, column=0, pady=(0,5), sticky="w")

        attrs = ["Id", "Brand", "Year", "Scale", "Condition", "Quantity", "Value"]

        # Loop to initialize and place filter buttons next to results.

        for i in range(len(attrs)):

            self.delete_button = ctk.CTkButton(
                self,
                text=attrs[i],
                width=100,
                fg_color="#4ab1ff",
                hover_color="#286b9e",
                command=lambda i=i : self.filter_results(
                    self.master.queryresults, i+1 if i > 2 else i
                )
            )

            self.delete_button.grid(
                column=11,
                row=i+1,
                pady=(10,0),
                padx=(20,0)
            )

    def display_query(self, queryresults) -> list:

        "Given a returned query from execute_query(), display to MainWindow object."

        # Max number of models to be shown when displaying results.
        # Loading in all results is not feasible.

        maxresults = 100

        # Current display must be destroyed before results can be shown.

        if len(self.models) > 0:
            for i in range(len(self.models)):
                self.models[i].destroy()

        # Display results up to maxresults to reduce loading time.
        # Append to models[] to allow for destruction on next display_query() call.

        for j in range(1, len(queryresults) if len(queryresults) < maxresults else maxresults):

            i = j - 1

            label = ctk.CTkLabel(self, text=f"{queryresults[i][0] : >4}: {queryresults[i][1]  : <12} {queryresults[i][2] : <4} {queryresults[i][4] : <5} {queryresults[i][5] : <9} {queryresults[i][6] : <8} ${queryresults[i][7] if queryresults[i][7] != 0.0 else 'N/A' : <7}", font=("Courier", 16))

            self.models.append(label)

            label.grid(row=j+1, column=0, pady=(0,5), sticky="w")

    # Function to filter and change ordering of App.queryresults.

    def filter_results(self, results, attr):

        "Reorder stored results from given input."

        results = sorted(results, key=lambda x: x[attr])

        self.master.queryresults  = results

        self.display_query(self.master.queryresults)

class App(ctk.CTk):

    "Main App class. Program is contained within this class."

    def __init__(self):

        "Create needed variables and objects to be placed."

        super().__init__()

        # Size of overall app.

        AppWidth=1000
        AppHeight=600

        # Stores results of database query to be filtered/exported.

        self.queryresults = []
        #self.queryresultsvalue = None

        # Limit resizing of window. App was not designed to be responsive.

        self.resizable(False, False)

        # When first running ,init database if not created.

        backend.create_table(backend.creation_query)

        # General format settings for app.

        ctk.set_appearance_mode('dark')
        self.title('Model Car Catalogue')
        self.geometry(f'{AppWidth}x{AppHeight}')
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Appearance variables to be used by all children objects.

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
            size=18
        )

        self.button_color = "#4ab1ff"
        self.button_hover_color = "#286b9e"

        # Sidebar object for querying.

        self.sidebar = Sidebar(self, 250, 600)
        self.sidebar.grid(
            column=0,
            row=0,
            padx=(10, 5),
            pady=10,
            sticky="ns"
        )

        # Main Window object to display results of query.

        self.main_window = MainWindow(
            self,
            AppWidth - self.sidebar.width,
            AppHeight - self.sidebar.height - 200
        )

        self.main_window.grid(
            column=1,
            row=0,
            padx=(5, 10),
            pady=10,
            sticky="nsew"
        )
