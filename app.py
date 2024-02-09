import math
import tkinter as tk
from tkinter import ttk


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BTS Sizing Tool")

        self.shared_values = {} # Initialize shared_values

        # Set dimensions for the whole window
        window_width = 700
        window_height = 790
        self.geometry(f"{window_width}x{window_height}")

        # Set maximum width and height
        self.maxsize(700, 790)
        self.resizable(True, True)

        # Set dimensions for the menu on the left
        menu_width = 120
        menu_height = window_height
        self.create_menu(width=menu_width, height=menu_height)

        self.create_pages()

        # Configure row 0 to expand vertically
        self.rowconfigure(0, weight=1)

    def create_menu(self, width, height):
        self.menu_frame = tk.Frame(self, bg="#252422", width=width, height=height)
        self.menu_frame.grid(row=0, column=0, sticky="ns", pady=0)

        # Frame for the menu list inside the menu frame
        menu_list_frame = tk.Frame(self.menu_frame, padx=20, bg="#252422", highlightthickness=2, highlightbackground="#252422")
        menu_list_frame.pack(fill=tk.Y, padx=(20, 20), pady=(50, 50), side="top", expand="yes")

        # Frame to wrap the buttons
        list_wrap = tk.Frame(menu_list_frame, bg="#252422")
        list_wrap.pack(expand=False, padx=(0, 0), pady=(50, 50), fill=tk.BOTH)

        self.step_names = ["Total BTS Size", "Total Usable Space", "Power Demand", "Solar Sizing", "Battery Sizing"]

        for i, name in enumerate(self.step_names):
            button = tk.Button(list_wrap, text=name, command=lambda i=i: self.show_page(i), bg="#ccc5b9", fg="black")
            button.pack(side=tk.TOP, anchor=tk.W, pady=(5, 10), fill=tk.BOTH, expand=True)

    def create_pages(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=1, sticky="nsew")

        style = ttk.Style()

        # Configure the notebook style
        style.configure("TNotebook", background="#ccc5b9", borderwidth=0)  

        # Configure the tab style
        style.configure("TNotebook.Tab", background="white", padding=[24, 10], borderwidth=1)  
        style.map("TNotebook.Tab", background=[("selected", "#ccc5b9")])  

        self.notebook.configure(style="TNotebook", padding=[0, 0]) 

        # Configure row and column weights
        for i in range(1, 6):
            self.notebook.rowconfigure(i, weight=1)
            self.notebook.columnconfigure(i, weight=1)

        self.pages = []

        for i in range(1, 6):
            page = ttk.Frame(self.notebook, style="TNotebook")  
            page.grid(row=1, column=0, sticky="nsew")
            self.pages.append(page)
            self.notebook.add(page, text=f"Step {i}")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        self.total_usable_space = [0.0]

        self.create_step1()
        self.create_step2()
        self.create_step3()
        self.create_step4()
        self.create_step5(self.shared_values["power_demand_entry"])

    def create_step1(self):
        frame = self.pages[0]

        button_font = ("Arial", 11)

        # Frame to wrap the input frames
        input_wrap = tk.Frame(frame, bg="#252422")
        input_wrap.grid(row=0, column=0, pady=15, padx=(15, 15), sticky="w")

        # Frame for Length of the site
        length_frame = tk.Frame(input_wrap)
        length_frame.grid(row=0, column=0, pady=(20, 20), padx=(15, 130), sticky="w")

        tk.Label(length_frame, text="Length of the site:").pack(side=tk.LEFT)
        length_entry = tk.Entry(length_frame)
        length_entry.pack(side=tk.LEFT)

        # Frame for Width of the site
        width_frame = tk.Frame(input_wrap)
        width_frame.grid(row=1, column=0, pady=(20, 20), padx=(15, 130), sticky="w")

        tk.Label(width_frame, text="Width of the site :").pack(side=tk.LEFT)
        width_entry = tk.Entry(width_frame)
        width_entry.pack(side=tk.LEFT)

        # Frame to wrap the result frames with fixed width
        results_wrap = tk.Frame(frame, bg="white", width=250, borderwidth=3, relief="sunken")  
        results_wrap.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="news")  

        # Frame for Result
        result_frame = tk.Frame(results_wrap, bg="white", pady=15) 
        result_frame.grid(row=1, column=0)

        result_label = tk.Label(result_frame, text="Result:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left") 
        result_label.grid(row=1, column=0, pady=15)

        # Frame to wrap the buttons frame
        buttons_wrap = tk.Frame(frame, bg="#252422")  
        buttons_wrap.grid(row=3, column=0, padx=(15, 15), pady=(0, 0), sticky="news") 

        # Frame for Calculate and Cancel buttons
        calculate_button_frame = tk.Frame(buttons_wrap, bg="#252422")
        calculate_button_frame.grid(row=1, column=2, pady=40, sticky="news")

        def calculate():
            try:
                length = float(length_entry.get())
                width = float(width_entry.get())
                result = round(length * width, 2)
                result_label.config(text=f"Total BTS site: {result} m²", pady=15, font=("Helvetica", 12, "bold"))
            except ValueError:
                result_label.config(text="Invalid input. Please enter valid numbers.", pady=15, font=("Helvetica", 12, "bold"))

        def clear_entry():
            current_entry = self.focus_get()
            current_text = current_entry.get()

            if current_text:
                # Delete the last character
                current_entry.delete(len(current_text) - 1, tk.END)

        def cancel():
            current_entry = self.focus_get()
            current_entry.delete(0, tk.END)

        # Calculate button
        calculate_button = tk.Button(calculate_button_frame, text="Calculate", command=calculate, bg="#ccc5b9", fg="black", activebackground="#008000", activeforeground="white", width=13, font=button_font)
        calculate_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))  

        # Cancel button
        cancel_button = tk.Button(calculate_button_frame, text="Cancel", command=cancel, bg="#ccc5b9", fg="black", activebackground="#FF0000", activeforeground="white", width=13, font=button_font)
        cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))  

        # Frame for additional buttons
        buttons_frame = tk.Frame(buttons_wrap, bg="#252422")
        buttons_frame.grid(row=1, column=0, pady=30, padx=10, sticky="news")

        # Function to update entry widgets
        def update_entry(value):
            current_entry = self.focus_get()
            current_entry.insert(tk.END, value)

        # Buttons for numbers 0-9
        for i in range(10):
            button_text = str(i)

            if i == 9:
                row_position = 3  
                column_position = 0  
            else:
                row_position = i // 3
                column_position = i % 3

            button = tk.Button(buttons_frame, text=button_text, command=lambda i=i: update_entry(i), width=5, height=3, bg="#ccc5b9", font=button_font)
            button.grid(row=row_position, column=column_position, padx=10, pady=10, sticky="news")

        # Button for decimal_button
        decimal_button = tk.Button(buttons_frame, text=".", command=lambda: update_entry("."), width=5, height=3, bg="#ccc5b9", font=button_font)
        decimal_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

        # Button for clearing the entry
        clear_button = tk.Button(buttons_frame, text="(C)", command=clear_entry, width=5, height=3, bg="#ccc5b9", font=button_font)
        clear_button.grid(row=3, column=2, padx=10, pady=10, sticky="news")
        
    def create_step2(self):
        frame = self.pages[1]

        button_font = ("Arial", 11)  

        input_wrap = tk.Frame(frame, bg="#252422")
        input_wrap.grid(row=0, column=0, pady=15, padx=(15, 15), sticky="w")

        # Frame for Length for solar installation
        length_frame = tk.Frame(input_wrap)
        length_frame.grid(row=0, column=0, pady=(20, 20), padx=(15, 65), sticky="w")

        tk.Label(length_frame, text="Length for solar installation:").pack(side=tk.LEFT)
        length_entry = tk.Entry(length_frame)
        length_entry.pack(side=tk.LEFT)

        # Frame for Width for solar installation
        width_frame = tk.Frame(input_wrap)
        width_frame.grid(row=1, column=0, pady=(20, 20), padx=(15, 50), sticky="w")

        tk.Label(width_frame, text="Width for solar installation  :").pack(side=tk.LEFT)
        width_entry = tk.Entry(width_frame)
        width_entry.pack(side=tk.LEFT)

        results_wrap = tk.Frame(frame, bg="white", width=250, borderwidth=3, relief="sunken")  
        results_wrap.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="news")  

        result_frame = tk.Frame(results_wrap, bg="white", pady=15)  
        result_frame.grid(row=1, column=0)

        result_label = tk.Label(result_frame, text="Result:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  # Explicitly set background color
        result_label.grid(row=1, column=0, pady=15)

        buttons_wrap = tk.Frame(frame, bg="#252422")  
        buttons_wrap.grid(row=3, column=0, padx=(15, 15), pady=(0, 0), sticky="news") 

        calculate_button_frame = tk.Frame(buttons_wrap, bg="#252422")
        calculate_button_frame.grid(row=1, column=2, pady=40, sticky="news")

        def calculate():
            try:
                length = float(length_entry.get())
                width = float(width_entry.get())
                result = round(length * width, 2)
                self.total_usable_space[0] = result
                result_label.config(text=f"Total Usable Site: {result} m²", pady=15, font=("Helvetica", 12, "bold"))
            except ValueError:
                result_label.config(text="Invalid input. Please enter valid numbers.", pady=15, font=("Helvetica", 12, "bold"))

        def clear_entry():
            current_entry = self.focus_get()
            current_text = current_entry.get()

            if current_text:
                current_entry.delete(len(current_text) - 1, tk.END)

        def cancel():
            current_entry = self.focus_get()
            current_entry.delete(0, tk.END)

        calculate_button = tk.Button(calculate_button_frame, text="Calculate", command=calculate, bg="#ccc5b9", fg="black", activebackground="#008000", activeforeground="white", width=13, font=button_font)
        calculate_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))  # Added expand and adjusted pady

        cancel_button = tk.Button(calculate_button_frame, text="Cancel", command=cancel, bg="#ccc5b9", fg="black", activebackground="#FF0000", activeforeground="white", width=13, font=button_font)
        cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))  # Added expand and adjusted pady

        buttons_frame = tk.Frame(buttons_wrap, bg="#252422")
        buttons_frame.grid(row=1, column=0, pady=30, padx=10, sticky="news")

        def update_entry(value):
            current_entry = self.focus_get()
            current_entry.insert(tk.END, value)

        for i in range(10):
            button_text = str(i)

            if i == 9:
                row_position = 3  
                column_position = 0  
            else:
                row_position = i // 3
                column_position = i % 3

            button = tk.Button(buttons_frame, text=button_text, command=lambda i=i: update_entry(i), width=5, height=3, bg="#ccc5b9", font=button_font)
            button.grid(row=row_position, column=column_position, padx=10, pady=10, sticky="news")

        decimal_button = tk.Button(buttons_frame, text=".", command=lambda: update_entry("."), width=5, height=3, bg="#ccc5b9", font=button_font)
        decimal_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

        clear_button = tk.Button(buttons_frame, text="(C)", command=clear_entry, width=5, height=3, bg="#ccc5b9", font=button_font)
        clear_button.grid(row=3, column=2, padx=10, pady=10, sticky="news")

    def create_step3(self):
        frame = self.pages[2]

        button_font = ("Arial", 11)  

        input_wrap = tk.Frame(frame, bg="#252422")
        input_wrap.grid(row=0, column=0, pady=15, padx=(15, 15), sticky="w")

        # Frame for Power Demand
        power_frame = tk.Frame(input_wrap)
        power_frame.grid(row=0, column=0, pady=(20, 50), padx=(15, 145), sticky="w")

        tk.Label(power_frame, text="Power Demand:").pack(side=tk.LEFT)
        power_demand_entry = tk.Entry(power_frame, name="power_demand")
        power_demand_entry.pack(side=tk.LEFT)

        # Store the power_demand_entry in the shared_values dictionary
        self.shared_values["power_demand_entry"] = power_demand_entry

        results_wrap = tk.Frame(frame, bg="white", width=250, borderwidth=3, relief="sunken")  
        results_wrap.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="news")  

        result_frame = tk.Frame(results_wrap, bg="white", pady=15)  
        result_frame.grid(row=1, column=0)

        result_label_power = tk.Label(result_frame, text="Power Demand:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  # Explicitly set background color
        result_label_power.grid(row=0, column=0, pady=10)

        result_label_energy = tk.Label(result_frame, text="Total Energy:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  # Explicitly set background color
        result_label_energy.grid(row=1, column=0, pady=10)

        buttons_wrap = tk.Frame(frame, bg="#252422")  
        buttons_wrap.grid(row=3, column=0, padx=(15, 15), pady=(0, 0), sticky="news") 

        calculate_button_frame = tk.Frame(buttons_wrap, bg="#252422")
        calculate_button_frame.grid(row=1, column=2, pady=40, sticky="news")

        def calculate():
            try:
                power_demand = float(power_demand_entry.get())
                # Perform calculation for Total Energy 
                total_energy = round (power_demand * 24, 2)
                result_label_power.config(text=f"Power Demand: {power_demand} kW", pady=10, font=("Helvetica", 12, "bold"))
                result_label_energy.config(text=f"Total Energy: {total_energy} kWh", pady=10, font=("Helvetica", 12, "bold"))
            except ValueError:
                result_label_power.config(text="Invalid input. Please enter valid numbers.", pady=10, font=("Helvetica", 12, "bold"))
                result_label_energy.config(text="", pady=10, font=("Helvetica", 12, "bold"))

        def clear_entry():
            current_entry = self.focus_get()
            current_text = current_entry.get()

            if current_text:
                current_entry.delete(len(current_text) - 1, tk.END)

        def cancel():
            current_entry = self.focus_get()
            current_entry.delete(0, tk.END)

        calculate_button = tk.Button(calculate_button_frame, text="Calculate", command=calculate, bg="#ccc5b9", fg="black", activebackground="#008000", activeforeground="white", width=13, font=button_font)
        calculate_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))  

        cancel_button = tk.Button(calculate_button_frame, text="Cancel", command=cancel, bg="#ccc5b9", fg="black", activebackground="#FF0000", activeforeground="white", width=13, font=button_font)
        cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))  

        buttons_frame = tk.Frame(buttons_wrap, bg="#252422")
        buttons_frame.grid(row=1, column=0, pady=30, padx=10, sticky="news")

        def update_entry(value):
            current_entry = self.focus_get()
            current_entry.insert(tk.END, value)

        for i in range(10):
            button_text = str(i)

            if i == 9:
                row_position = 3  
                column_position = 0  
            else:
                row_position = i // 3
                column_position = i % 3

            button = tk.Button(buttons_frame, text=button_text, command=lambda i=i: update_entry(i), width=5, height=3, bg="#ccc5b9", font=button_font)
            button.grid(row=row_position, column=column_position, padx=10, pady=10, sticky="news")

        decimal_button = tk.Button(buttons_frame, text=".", command=lambda: update_entry("."), width=5, height=3, bg="#ccc5b9", font=button_font)
        decimal_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

        clear_button = tk.Button(buttons_frame, text="(C)", command=clear_entry, width=5, height=3, bg="#ccc5b9", font=button_font)
        clear_button.grid(row=3, column=2, padx=10, pady=10, sticky="news")

    def create_step4(self):
        frame = self.pages[3]

        button_font = ("Arial", 11)  

        input_wrap = tk.Frame(frame, bg="#252422")
        input_wrap.grid(row=0, column=0, pady=15, padx=(15, 15), sticky="w")

        # Frame for Panel size
        panel_size_frame = tk.Frame(input_wrap)
        panel_size_frame.grid(row=0, column=0, pady=(15, 5), padx=(15, 140), sticky="w")

        tk.Label(panel_size_frame, text="Panel Size (m²) :").pack(side=tk.LEFT)
        panel_size_entry = tk.Entry(panel_size_frame)
        panel_size_entry.pack(side=tk.LEFT)

        # Frame for Panel rating
        panel_rating_frame = tk.Frame(input_wrap)
        panel_rating_frame.grid(row=1, column=0, pady=(5, 5), padx=(15, 140), sticky="w")

        tk.Label(panel_rating_frame, text="Panel Rating  :").pack(side=tk.LEFT)
        panel_rating_var = tk.StringVar()
        panel_rating_var.set("0.45kW")  # Default value
        panel_rating_dropdown = ttk.Combobox(panel_rating_frame, textvariable=panel_rating_var, values=["0.4kW", "0.45kW", "0.5kW"])
        panel_rating_dropdown.pack(side=tk.LEFT)

        # Frame for Solar sun hours
        solar_hours_frame = tk.Frame(input_wrap)
        solar_hours_frame.grid(row=2, column=0, pady=(5, 15), padx=(15, 140), sticky="w")

        tk.Label(solar_hours_frame, text="Solar Sun Hours:").pack(side=tk.LEFT)
        solar_hours_entry = tk.Entry(solar_hours_frame)
        solar_hours_entry.pack(side=tk.LEFT)

        results_wrap = tk.Frame(frame, bg="white", width=250, borderwidth=3, relief="sunken")  
        results_wrap.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="news")  

        result_frame = tk.Frame(results_wrap, bg="white", pady=15)  
        result_frame.grid(row=1, column=0)

        result_label_panels = tk.Label(result_frame, text="No. of Panels:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  
        result_label_panels.grid(row=0, column=0, pady=5, sticky="w")

        result_label_array = tk.Label(result_frame, text="Array Size:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  
        result_label_array.grid(row=1, column=0, pady=5, sticky="w")

        result_label_inverter = tk.Label(result_frame, text="Inverter/Rectifier Size:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left") 
        result_label_inverter.grid(row=2, column=0, pady=5, sticky="w")

        result_label_output = tk.Label(result_frame, text="Total Solar Output:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  
        result_label_output.grid(row=3, column=0, pady=5, sticky="w")

        buttons_wrap = tk.Frame(frame, bg="#252422")  
        buttons_wrap.grid(row=3, column=0, padx=(15, 15), pady=(0), sticky="news") 

        calculate_button_frame = tk.Frame(buttons_wrap, bg="#252422")
        calculate_button_frame.grid(row=1, column=2, pady=40, sticky="news")

        def calculate():
            try:
                panel_size = float(panel_size_entry.get())
                panel_rating = float(panel_rating_var.get().replace("kW", ""))
                solar_hours = float(solar_hours_entry.get())

                num_panels = math.ceil(self.total_usable_space[0] / panel_size)  # Round up
                array_size = round(num_panels * panel_rating, 2)
                inverter_size = round(1.2 * array_size, 2)
                total_solar_output = round(array_size * solar_hours, 2)

                result_label_panels.config(text=f"No. of Panels: {num_panels}", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")
                result_label_array.config(text=f"Array Size: {array_size} kWp", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")
                result_label_inverter.config(text=f"Inverter/Rectifier Size: {inverter_size} kW", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")
                result_label_output.config(text=f"Total Solar Output: {total_solar_output} kWh", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")
            except ValueError:
                result_label_panels.config(text="Invalid input. Please enter valid numbers.", pady=0, font=("Helvetica", 11, "bold"))
                result_label_array.config(text="", pady=0, font=("Helvetica", 11, "bold"))
                result_label_inverter.config(text="", pady=0, font=("Helvetica", 11, "bold"))
                result_label_output.config(text="", pady=0, font=("Helvetica", 11, "bold"))

        def clear_entry():
            current_entry = self.focus_get()
            current_text = current_entry.get()

            if current_text:
                current_entry.delete(len(current_text) - 1, tk.END)

        def cancel():
            current_entry = self.focus_get()
            current_entry.delete(0, tk.END)

        calculate_button = tk.Button(calculate_button_frame, text="Calculate", command=calculate, bg="#ccc5b9", fg="black", activebackground="#008000", activeforeground="white", width=13, font=button_font)
        calculate_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))  

        cancel_button = tk.Button(calculate_button_frame, text="Cancel", command=cancel, bg="#ccc5b9", fg="black", activebackground="#FF0000", activeforeground="white", width=13, font=button_font)
        cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))  

        buttons_frame = tk.Frame(buttons_wrap, bg="#252422")
        buttons_frame.grid(row=1, column=0, pady=30, padx=10, sticky="news")

        def update_entry(value):
            current_entry = self.focus_get()
            current_entry.insert(tk.END, value)

        for i in range(10):
            button_text = str(i)

            if i == 9:
                row_position = 3  
                column_position = 0  
            else:
                row_position = i // 3
                column_position = i % 3

            button = tk.Button(buttons_frame, text=button_text, command=lambda i=i: update_entry(i), width=5, height=3, bg="#ccc5b9", font=button_font)
            button.grid(row=row_position, column=column_position, padx=10, pady=10, sticky="news")

        decimal_button = tk.Button(buttons_frame, text=".", command=lambda: update_entry("."), width=5, height=3, bg="#ccc5b9", font=button_font)
        decimal_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

        clear_button = tk.Button(buttons_frame, text="(C)", command=clear_entry, width=5, height=3, bg="#ccc5b9", font=button_font)
        clear_button.grid(row=3, column=2, padx=10, pady=10, sticky="news")
                
    def create_step5(self, power_demand_entry):
        frame = self.pages[4]

        button_font = ("Arial", 11) 

        input_wrap = tk.Frame(frame, bg="#252422")
        input_wrap.grid(row=0, column=0, pady=15, padx=(15, 15), sticky="w")

        # Frame for Grid Unavailability
        grid_unavailability_frame = tk.Frame(input_wrap)
        grid_unavailability_frame.grid(row=0, column=0, pady=(20, 20), padx=(15, 25), sticky="w")

        tk.Label(grid_unavailability_frame, text="Input Grid Unavailability (No of hours):", font=("Helvetica", 10)).pack(side=tk.LEFT)
        grid_unavailability_entry = tk.Entry(grid_unavailability_frame, name="grid_unavailability_entry")
        grid_unavailability_entry.pack(side=tk.LEFT)

        # Frame for Maximum DoD of battery
        dod_frame = tk.Frame(input_wrap)
        dod_frame.grid(row=1, column=0, pady=(20, 20), padx=(15, 25), sticky="w")

        tk.Label(dod_frame, text="Maximum DoD of Battery (%):", font=("Helvetica", 10)).pack(side=tk.LEFT)
        dod_entry = tk.Entry(dod_frame, name="dod_entry")
        dod_entry.pack(side=tk.LEFT)

        results_wrap = tk.Frame(frame, bg="white", borderwidth=3, relief="sunken")  
        results_wrap.grid(row=1, column=0, pady=(0, 15), padx=15, sticky="news")  

        result_frame = tk.Frame(results_wrap, bg="white", pady=25)  
        result_frame.grid(row=1, column=0)

        result_label = tk.Label(result_frame, text="Battery Sizing:", bg="white", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")  
        result_label.grid(row=0, column=0, pady=10)

        buttons_wrap = tk.Frame(frame, bg="#252422")  
        buttons_wrap.grid(row=3, column=0, padx=(15, 15), pady=(0, 0), sticky="news") 

        calculate_button_frame = tk.Frame(buttons_wrap, bg="#252422")
        calculate_button_frame.grid(row=1, column=2, pady=40, sticky="news")

        def calculate():
            try:
                grid_unavailability = float(grid_unavailability_entry.get())
                dod = float(dod_entry.get())

                # Get the total power demand from step 3
                power_demand = float(power_demand_entry.get())
                battery_size = round(((grid_unavailability * power_demand) / (dod / 100)), 2)
                result_label.config(text=f"Battery Sizing: {battery_size} kWh", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")
            except ValueError:
                result_label.config(text="Invalid input. Please enter valid numbers.", pady=0, font=("Arial", 11, "bold"), anchor="w", justify="left")

        def clear_entry():
            current_entry = self.focus_get()
            current_text = current_entry.get()

            if current_text:
                current_entry.delete(len(current_text) - 1, tk.END)

        def cancel():
            current_entry = self.focus_get()
            current_entry.delete(0, tk.END)

        calculate_button = tk.Button(calculate_button_frame, text="Calculate", command=calculate, bg="#ccc5b9", fg="black", activebackground="#008000", activeforeground="white", width=13, font=button_font)
        calculate_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 5))  

        cancel_button = tk.Button(calculate_button_frame, text="Cancel", command=cancel, bg="#ccc5b9", fg="black", activebackground="#FF0000", activeforeground="white", width=13, font=button_font)
        cancel_button.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))  

        buttons_frame = tk.Frame(buttons_wrap, bg="#252422")
        buttons_frame.grid(row=1, column=0, pady=30, padx=10, sticky="news")

        def update_entry(value):
            current_entry = self.focus_get()
            current_entry.insert(tk.END, value)

        for i in range(10):
            button_text = str(i)

            if i == 9:
                row_position = 3  
                column_position = 0  
            else:
                row_position = i // 3
                column_position = i % 3

            button = tk.Button(buttons_frame, text=button_text, command=lambda i=i: update_entry(i), width=5, height=3, bg="#ccc5b9", font=button_font)
            button.grid(row=row_position, column=column_position, padx=10, pady=10, sticky="news")

        decimal_button = tk.Button(buttons_frame, text=".", command=lambda: update_entry("."), width=5, height=3, bg="#ccc5b9", font=button_font)
        decimal_button.grid(row=3, column=1, padx=10, pady=10, sticky="news")

        clear_button = tk.Button(buttons_frame, text="(C)", command=clear_entry, width=5, height=3, bg="#ccc5b9", font=button_font)
        clear_button.grid(row=3, column=2, padx=10, pady=10, sticky="news")

    def show_page(self, index):
        self.notebook.select(index)

    def on_tab_change(self, event):
        current_tab = self.notebook.index("current")
        print(f"Selected Tab: {current_tab}")

    def cancel(self):
        current_entry = self.focus_get()
        current_entry.delete(0, tk.END)

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
