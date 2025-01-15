# Copyright (c) 2025 Nico Mullin
# Licensed under the MIT License. See LICENSE file for details.

import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json  # For saving and loading configurations as JSON

# Universal list of items and base prices
universal_items = {}

# Define islands
islands = {}

# Function to calculate fluctuated prices
def calculate_fluctuated_price(base_price):
    fluctuation = random.uniform(-0.2, 0.2)
    return round(base_price * (1 + fluctuation), 2)

# Function to calculate adjusted prices
def calculate_adjusted_price(price, modifier_percentage):
    return round(price * (1 + modifier_percentage / 100), 2)

# Tooltip class
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window is not None:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="yellow",
            relief="solid",
            borderwidth=1,
            font=("tahoma", "10", "normal"),
        )
        label.pack(ipadx=5, ipady=5)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

    def destroy_tooltip(self):
        """Explicitly destroy tooltip and unbind widget events."""
        self.hide_tooltip()
        self.widget.unbind("<Enter>")
        self.widget.unbind("<Leave>")

class TradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Trading Program")

        # Variables
        self.selected_island = tk.StringVar()
        self.global_modifier = tk.IntVar(value=0)
        self.item_entries = []

        # Island Selection
        ttk.Label(root, text="Select Island:").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.island_menu = ttk.Combobox(root, textvariable=self.selected_island, values=list(islands.keys()), state="readonly")
        self.island_menu.grid(row=0, column=2, padx=10, pady=5)
        Tooltip(self.island_menu, "Select an island to trade specific items.")
        self.island_menu.bind("<<ComboboxSelected>>", self.update_items_options)

        # Create New Island Button
        self.create_new_island_button = ttk.Button(root, text="Create New Island", command=self.create_new_island)
        self.create_new_island_button.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        Tooltip(self.create_new_island_button, "Create a new island with custom items.")

        # Global Modifier
        ttk.Label(root, text="Global Modifier (%):").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        global_modifier_spinbox = ttk.Spinbox(root, from_=-100, to=100, increment=5, textvariable=self.global_modifier, width=10)
        global_modifier_spinbox.grid(row=0, column=5, padx=10, pady=5)
        Tooltip(global_modifier_spinbox, "Adjust global price changes affecting all items.")

        # Item Selection with Headers
        ttk.Label(root, text="Select Items and Modifiers:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.items_frame = ttk.Frame(root)
        self.items_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=5, sticky="w")

        # Add headers for the item selection modifiers
        ttk.Label(self.items_frame, text="Category").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Item").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Sell Modifier (%)").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Buy Modifier (%)").grid(row=0, column=3, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Quantity").grid(row=0, column=4, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Actions").grid(row=0, column=5, padx=5, pady=2, sticky="w")

        # Add initial item row
        self.add_item_button = ttk.Button(self.items_frame, text="Add Another Item", command=self.add_item_row)
        self.add_item_row()

        # Add Custom Item Button
        self.add_custom_item_button = ttk.Button(root, text="Add Custom Item", command=self.add_custom_item)
        self.add_custom_item_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        Tooltip(self.add_custom_item_button, "Add a new item to the selected island.")

        # Calculate Prices Button
        self.calculate_prices_button = ttk.Button(root, text="Calculate Prices", command=self.calculate_prices)
        self.calculate_prices_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        Tooltip(self.calculate_prices_button, "Calculate final prices for selected items.")

        # Save and Load Buttons
        save_button = ttk.Button(root, text="Save Configuration", command=self.save_configuration)
        save_button.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        Tooltip(save_button, "Save the current configuration, including islands and items.")

        load_button = ttk.Button(root, text="Load Configuration", command=self.load_configuration)
        load_button.grid(row=6, column=2, padx=10, pady=10, sticky="w")
        Tooltip(load_button, "Load a previously saved configuration.")

        # Results Display
        ttk.Label(root, text="Results:").grid(row=7, column=1, padx=10, pady=5, sticky="nw")
      
        # Frame to hold scrollable text widget
        results_frame = ttk.Frame(root)
        results_frame.grid(row=7, column=2, columnspan=4, padx=10, pady=5, sticky="nsew")

        # Add scrollbars
        v_scrollbar = tk.Scrollbar(results_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = tk.Scrollbar(results_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")

        # Add a scrollable Text widget
        self.result_display = tk.Text(results_frame, wrap="none", height=10, width=50, 
        yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.result_display.pack(side="left", fill="both", expand=True)

        # Configure scrollbars to control the text widget
        v_scrollbar.config(command=self.result_display.yview)
        h_scrollbar.config(command=self.result_display.xview)


        # Credits Button
        credits_button = ttk.Button(root, text="Credits", command=self.show_credits)
        credits_button.grid(row=8, column=4, padx=10, pady=10, sticky="e")
        Tooltip(credits_button, "View application credits.")

    def show_credits(self):
        """Show a credits window."""
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.geometry("350x250")

        tk.Label(credits_window, text="Created by Nico Mullin.", font=("Arial", 12)).pack(pady=10)
        tk.Label(credits_window, text="Used ChatGPT to help with coding.", font=("Arial", 10)).pack(pady=5)
        tk.Label(credits_window, text="Github: NicoMullin", font=("Arial", 10)).pack(pady=5)
        tk.Label(credits_window, text="This will always be free. Never pay to use for the program.", font=("Arial", 10)).pack(pady=5)
        tk.Label(credits_window, text="https://github.com/NicoMullin/D-D-Trading-Program", font=("Arial", 10)).pack(pady=5)

        ttk.Button(credits_window, text="Close", command=credits_window.destroy).pack(pady=20)

    def add_item_row(self):
        """Add a new row for item selection and modifiers."""
        category_var = tk.StringVar()
        item_var = tk.StringVar()
        sell_modifier = tk.IntVar(value=0)
        buy_modifier = tk.IntVar(value=0)
        quantity_var = tk.StringVar(value="None")
    
        # Dynamically fetch the latest items and categories for the selected island
        selected_island = self.selected_island.get()
        categories = list(islands[selected_island].keys()) if selected_island in islands else []
        available_items = list(islands[selected_island][categories[0]].keys()) if categories else []
    
        row_index = len(self.item_entries) + 1
    
        # Category Dropdown
        category_dropdown = ttk.Combobox(self.items_frame, textvariable=category_var, values=categories, state="readonly", width=30)
        category_dropdown.grid(row=row_index, column=0, padx=5, pady=2, sticky="w")
        Tooltip(category_dropdown, "Select a category.")
    
        def update_items_for_category(event=None):
            """Update items dropdown when a category is selected."""
            selected_category = category_var.get()
            available_items = list(islands[selected_island][selected_category].keys()) if selected_category in islands[selected_island] else []
            dropdown["values"] = available_items
    
        category_dropdown.bind("<<ComboboxSelected>>", update_items_for_category)
    
        # Item Dropdown
        dropdown = ttk.Combobox(self.items_frame, textvariable=item_var, values=available_items, state="readonly")
        dropdown.grid(row=row_index, column=1, padx=5, pady=2, sticky="w")
        Tooltip(dropdown, "Select an item to trade.")
    
        # Sell Modifier Spinbox
        sell_spinbox = ttk.Spinbox(self.items_frame, from_=-100, to=100, increment=5, textvariable=sell_modifier, width=10)
        sell_spinbox.grid(row=row_index, column=2, padx=5, pady=2)
        Tooltip(sell_spinbox, "Set a modifier for the sell price of the selected item.")
    
        # Buy Modifier Spinbox
        buy_spinbox = ttk.Spinbox(self.items_frame, from_=-100, to=100, increment=5, textvariable=buy_modifier, width=10)
        buy_spinbox.grid(row=row_index, column=3, padx=5, pady=2)
        Tooltip(buy_spinbox, "Set a modifier for the buy price of the selected item.")
    
        # Quantity Dropdown
        quantity_dropdown = ttk.Combobox(self.items_frame, textvariable=quantity_var, values=["None", "Normal", "Low", "High"], state="readonly")
        quantity_dropdown.grid(row=row_index, column=4, padx=5, pady=2, sticky="w")
        Tooltip(quantity_dropdown, "Select the quantity of the item.")
    
        # Remove Button
        remove_button = ttk.Button(self.items_frame, text="Remove", command=lambda: self.remove_item_row(row_index - 1))
        remove_button.grid(row=row_index, column=5, padx=5, pady=2)
        Tooltip(remove_button, "Remove this item entry.")
    
        self.item_entries.append((category_var, item_var, sell_modifier, buy_modifier, quantity_var, category_dropdown, dropdown, sell_spinbox, buy_spinbox, quantity_dropdown, remove_button))
    
        self.add_item_button.grid(row=row_index + 1, column=5, padx=5, pady=10, sticky="w")


    def remove_item_row(self, row_index):
        """Remove a specific item row."""
        if 0 <= row_index < len(self.item_entries):
            entry = self.item_entries.pop(row_index)

            for widget in entry[4:]:
                if hasattr(widget, "destroy"):
                    widget.destroy()

            for i, (_, _, _, _, dropdown, sell_spinbox, buy_spinbox, quantity_dropdown, button) in enumerate(self.item_entries):
                dropdown.grid(row=i + 1, column=0, padx=5, pady=2, sticky="w")
                sell_spinbox.grid(row=i + 1, column=1, padx=5, pady=2)
                buy_spinbox.grid(row=i + 1, column=2, padx=5, pady=2)
                quantity_dropdown.grid(row=i + 1, column=3, padx=5, pady=2, sticky="w")
                button.grid(row=i + 1, column=4, padx=5, pady=2)

            self.add_item_button.grid(row=len(self.item_entries) + 1, column=4, padx=5, pady=10, sticky="w")

    def update_items_options(self, event=None):
        """Update the item dropdown options based on the selected island and categories."""
        selected_island = self.selected_island.get()
        if selected_island in islands:
            items = []
            for category, category_items in islands[selected_island].items():
                items.extend(category_items.keys())
            for entry in self.item_entries:
                dropdown = entry[4]
                dropdown["values"] = items

    def create_new_island(self):
       """Create a new island with predefined categories."""
       new_island_window = tk.Toplevel(self.root)
       new_island_window.title("Create New Island")
   
       tk.Label(new_island_window, text="Island Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
       island_name_entry = tk.Entry(new_island_window)
       island_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
  
       def save_new_island():
           island_name = island_name_entry.get().strip()
           if island_name and island_name not in islands:
               islands[island_name] = {
                   "Textiles and Fabrics": {},
                   "Food and Beverages": {},
                   "Spices and Plants": {},
                   "Tools, Ship and Supplies": {},
                   "Animal and Livestock Products": {},
                   "Trade Goods": {},
                   "Artistic and Decorative Items": {},
                   "Rare and Collectible Items": {},
                   "Religious and Cultural Items": {},
                   "Furniture and Household Goods": {},
                   "Navigation and Writing Tools": {},
                   "Weapons and Explosives": {},
               }
               self.island_menu["values"] = list(islands.keys())
               new_island_window.destroy()
           else:
               messagebox.showerror("Error", "Island name is invalid or already exists!")
  
       ttk.Button(new_island_window, text="Save", command=save_new_island).grid(row=1, column=0, columnspan=2, pady=10)



    def add_custom_item(self):
        """Add a custom item to the currently selected island and category."""
        if not self.selected_island.get():
            messagebox.showerror("Error", "Please select an island first!")
            return

        # Create a new window for custom item creation
        custom_item_window = tk.Toplevel(self.root)
        custom_item_window.title("Add Custom Item")
        custom_item_window.geometry("400x350")

        tk.Label(custom_item_window, text="Item Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        item_name_entry = tk.Entry(custom_item_window)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(custom_item_window, text="Base Price:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        item_price_entry = tk.Entry(custom_item_window)
        item_price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Dropdown to select category
        tk.Label(custom_item_window, text="Category:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        category_var = tk.StringVar()
        categories = list(islands[self.selected_island.get()].keys())
        category_menu = ttk.Combobox(custom_item_window, textvariable=category_var, values=categories, state="readonly")
        category_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Checkbox for applying to all islands
        apply_to_all_var = tk.BooleanVar()
        apply_to_all_checkbox = ttk.Checkbutton(
            custom_item_window,
            text="Apply to all islands (existing and future)",
            variable=apply_to_all_var
        )
        apply_to_all_checkbox.grid(row=3, column=0, columnspan=2, padx=10, pady=15, sticky="w")

        def save_custom_item():
            """Save the custom item."""
            item_name = item_name_entry.get().strip()
            try:
                item_price = int(item_price_entry.get())
                selected_category = category_var.get()
                if item_name and item_price > 0 and selected_category:
                    # Add item to the current island
                    islands[self.selected_island.get()][selected_category][item_name] = item_price

                    # If apply_to_all is checked, add the item to all other islands
                    if apply_to_all_var.get():
                        for island_name, island_categories in islands.items():
                            if selected_category not in island_categories:
                                island_categories[selected_category] = {}
                            island_categories[selected_category][item_name] = item_price

                    custom_item_window.destroy()
                    self.update_items_options()  # Refresh item dropdowns
                else:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid item name, base price, and category!")

        # Confirm Button
        ttk.Button(custom_item_window, text="Confirm", command=save_custom_item).grid(row=4, column=0, columnspan=2, pady=20)


    def calculate_prices(self):
        """Calculate and display final buy and sell prices grouped by categories."""
        selected_island = self.selected_island.get()
        if not selected_island:
            messagebox.showerror("Error", "Please select an island first!")
            return

        global_modifier = self.global_modifier.get()
        results = {}

        for category, items in islands[selected_island].items():
            results[category] = []
            for item_name, base_price in items.items():
                # Calculate fluctuated and adjusted prices
                fluctuated_price = calculate_fluctuated_price(base_price)

                # Find relevant modifiers from item entries
                sell_modifier = 0
                buy_modifier = 0
                for entry in self.item_entries:
                    if entry[1].get() == item_name:  # Match item_var
                        sell_modifier = entry[2].get()  # sell_modifier
                        buy_modifier = entry[3].get()  # buy_modifier
                        break

                # Apply modifiers
                final_sell_price = calculate_adjusted_price(fluctuated_price, sell_modifier + global_modifier)
                final_buy_price = calculate_adjusted_price(fluctuated_price, buy_modifier + global_modifier)

                # Add the result for this item
                results[category].append(
                    f"{item_name} - Sell Price: {final_sell_price}, Buy Price: {final_buy_price}"
                )

        # Clear and display categorized results
        self.result_display.delete(1.0, tk.END)
        for category, items in results.items():
            self.result_display.insert(tk.END, f"{category}\n{'=' * len(category)}\n")
            for item in items:
                self.result_display.insert(tk.END, f"{item}\n")
            self.result_display.insert(tk.END, "\n")


    def save_configuration(self):
        """Save the current configuration to a JSON file."""
        config = {
            "selected_island": self.selected_island.get(),
            "global_modifier": self.global_modifier.get(),
            "item_entries": [
                {
                    "category": entry[0].get(),
                    "item": entry[1].get(),
                    "sell_modifier": entry[2].get(),
                    "buy_modifier": entry[3].get(),
                    "quantity": entry[4].get(),
                }
                for entry in self.item_entries
            ],
            "islands": islands,  # Include the custom islands and their items
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Save Configuration",
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    json.dump(config, file, indent=4)
                messagebox.showinfo("Success", "Configuration saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def load_configuration(self):
        """Load a configuration from a JSON file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
            title="Load Configuration",
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    config = json.load(file)

                # Restore the islands and their items
                global islands
                islands = config.get("islands", {})  # Load islands, default to empty if not found
                self.island_menu["values"] = list(islands.keys())

                # Set the selected island and global modifier
                self.selected_island.set(config.get("selected_island", ""))
                self.global_modifier.set(config.get("global_modifier", 0))

                # Clear existing item rows
                for entry in self.item_entries:
                    for widget in entry[5:]:  # Widgets are stored starting from index 5
                        if hasattr(widget, "destroy"):
                            widget.destroy()

                self.item_entries = []  # Reset the item entries list

                # Recreate item rows from the loaded configuration
                for saved_entry in config.get("item_entries", []):
                    # Create a new row
                    self.add_item_row()

                    # Populate the row with saved data
                    current_entry = self.item_entries[-1]  # Get the most recently added entry
                    current_entry[0].set(saved_entry["category"])  # category_var
                    current_entry[1].set(saved_entry["item"])      # item_var
                    current_entry[2].set(saved_entry["sell_modifier"])  # sell_modifier
                    current_entry[3].set(saved_entry["buy_modifier"])   # buy_modifier
                    current_entry[4].set(saved_entry["quantity"])       # quantity_var

                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
