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
        self.result_text = tk.StringVar(value="")

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
        ttk.Label(self.items_frame, text="Item").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Sell Modifier (%)").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Buy Modifier (%)").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Quantity").grid(row=0, column=3, padx=5, pady=2, sticky="w")
        ttk.Label(self.items_frame, text="Actions").grid(row=0, column=4, padx=5, pady=2, sticky="w")

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
        self.result_display = ttk.Label(root, textvariable=self.result_text, anchor="w", justify="left")
        self.result_display.grid(row=7, column=2, columnspan=4, padx=10, pady=5, sticky="w")

        # Credits Button
        credits_button = ttk.Button(root, text="Credits", command=self.show_credits)
        credits_button.grid(row=8, column=4, padx=10, pady=10, sticky="e")
        Tooltip(credits_button, "View application credits.")

    def show_credits(self):
        """Show a credits window."""
        credits_window = tk.Toplevel(self.root)
        credits_window.title("Credits")
        credits_window.geometry("300x150")

        tk.Label(credits_window, text="Created by Nico Mullin.", font=("Arial", 12)).pack(pady=10)
        tk.Label(credits_window, text="Help by ChatGPT to get correct values for working.", font=("Arial", 10)).pack(pady=5)

        ttk.Button(credits_window, text="Close", command=credits_window.destroy).pack(pady=20)

    def add_item_row(self):
        """Add a new row for item selection and modifiers."""
        item_var = tk.StringVar()
        sell_modifier = tk.IntVar(value=0)
        buy_modifier = tk.IntVar(value=0)
        quantity_var = tk.StringVar(value="None")

        # Dynamically fetch the latest items for the selected island
        selected_island = self.selected_island.get()
        available_items = list(islands[selected_island].keys()) if selected_island in islands else []

        row_index = len(self.item_entries) + 1  # Determine the new row index dynamically
        dropdown = ttk.Combobox(self.items_frame, textvariable=item_var, values=available_items, state="readonly")
        dropdown.grid(row=row_index, column=0, padx=5, pady=2, sticky="w")
        Tooltip(dropdown, "Select an item to trade.")

        sell_spinbox = ttk.Spinbox(self.items_frame, from_=-100, to=100, increment=5, textvariable=sell_modifier, width=10)
        sell_spinbox.grid(row=row_index, column=1, padx=5, pady=2)
        Tooltip(sell_spinbox, "Set a modifier for the sell price of the selected item.")

        buy_spinbox = ttk.Spinbox(self.items_frame, from_=-100, to=100, increment=5, textvariable=buy_modifier, width=10)
        buy_spinbox.grid(row=row_index, column=2, padx=5, pady=2)
        Tooltip(buy_spinbox, "Set a modifier for the buy price of the selected item.")

        quantity_dropdown = ttk.Combobox(self.items_frame, textvariable=quantity_var, values=["None", "Normal", "Low", "High"], state="readonly")
        quantity_dropdown.grid(row=row_index, column=3, padx=5, pady=2, sticky="w")
        Tooltip(quantity_dropdown, "Select the quantity of the item.")

        remove_button = ttk.Button(self.items_frame, text="Remove", command=lambda: self.remove_item_row(row_index - 1))
        remove_button.grid(row=row_index, column=4, padx=5, pady=2)
        Tooltip(remove_button, "Remove this item entry.")

        self.item_entries.append((item_var, sell_modifier, buy_modifier, quantity_var, dropdown, sell_spinbox, buy_spinbox, quantity_dropdown, remove_button))

        self.add_item_button.grid(row=row_index + 1, column=4, padx=5, pady=10, sticky="w")

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
        """Update the item dropdown options based on the selected island."""
        selected_island = self.selected_island.get()
        if selected_island in islands:
            items = list(islands[selected_island].keys())
            for entry in self.item_entries:
                dropdown = entry[4]
                dropdown["values"] = items

    def create_new_island(self):
        """Create a new island with custom items."""
        new_island_window = tk.Toplevel(self.root)
        new_island_window.title("Create New Island")

        tk.Label(new_island_window, text="Island Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        island_name_entry = tk.Entry(new_island_window)
        island_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        def save_new_island():
            island_name = island_name_entry.get()
            if island_name and island_name not in islands:
                islands[island_name] = universal_items.copy()
                self.island_menu["values"] = list(islands.keys())
                new_island_window.destroy()
            else:
                messagebox.showerror("Error", "Island name is invalid or already exists!")

        ttk.Button(new_island_window, text="Save", command=save_new_island).grid(row=1, column=0, columnspan=2, pady=10)

    def add_custom_item(self):
        """Add a custom item to the currently selected island."""
        if not self.selected_island.get():
            messagebox.showerror("Error", "Please select an island first!")
            return

        custom_item_window = tk.Toplevel(self.root)
        custom_item_window.title("Add Custom Item")

        tk.Label(custom_item_window, text="Item Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        item_name_entry = tk.Entry(custom_item_window)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(custom_item_window, text="Base Price:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        item_price_entry = tk.Entry(custom_item_window)
        item_price_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        def save_custom_item():
            item_name = item_name_entry.get()
            try:
                item_price = int(item_price_entry.get())
                if item_name and item_price > 0:
                    islands[self.selected_island.get()][item_name] = item_price
                    custom_item_window.destroy()
                    self.update_items_options()  # Refresh all dropdowns
                else:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Invalid item name or price!")

        ttk.Button(custom_item_window, text="Save", command=save_custom_item).grid(row=2, column=0, columnspan=2, pady=10)

    def calculate_prices(self):
        """Calculate final prices for all selected items."""
        selected_island = self.selected_island.get()
        if not selected_island:
            messagebox.showerror("Error", "Please select an island first!")
            return

        global_modifier = self.global_modifier.get()
        results = []

        for item_var, sell_modifier, buy_modifier, quantity_var, dropdown, _, _, _, _ in self.item_entries:
            item_name = item_var.get()
            if not item_name:
                continue

            base_price = islands[selected_island][item_name]
            fluctuated_price = calculate_fluctuated_price(base_price)
            sell_price = calculate_adjusted_price(fluctuated_price, sell_modifier.get() - global_modifier)
            buy_price = calculate_adjusted_price(fluctuated_price, buy_modifier.get() + global_modifier)

            # Apply quantity-based adjustments
            quantity = quantity_var.get()
            if quantity == "None":
                sell_price = 0
                buy_price = calculate_adjusted_price(buy_price, 100)
            elif quantity == "Normal":
                pass
            elif quantity == "Low":
                sell_price = calculate_adjusted_price(sell_price, 75)
                buy_price = calculate_adjusted_price(buy_price, 50)
            elif quantity == "High":
                sell_price = calculate_adjusted_price(sell_price, -75)
                buy_price = 0

            results.append(
                f"Item: {item_name}\n"
                f"  Base Price: {base_price}\n"
                f"  Fluctuated Price: {fluctuated_price}\n"
                f"  Selling Price (with {sell_modifier.get()}%, global {global_modifier}%, quantity {quantity}): {sell_price}\n"
                f"  Buying Price (with {buy_modifier.get()}%, global {global_modifier}%, quantity {quantity}): {buy_price}"
            )

        self.result_text.set("\n\n".join(results))

    def save_configuration(self):
        """Save the current configuration to a JSON file."""
        config = {
            "selected_island": self.selected_island.get(),
            "global_modifier": self.global_modifier.get(),
            "item_entries": [
                {
                    "item": item_var.get(),
                    "sell_modifier": sell_modifier.get(),
                    "buy_modifier": buy_modifier.get(),
                    "quantity": quantity_var.get(),
                }
                for item_var, sell_modifier, buy_modifier, quantity_var, _, _, _, _, _ in self.item_entries
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
                    for widget in entry[4:]:  # Widgets are stored starting from index 4
                        if hasattr(widget, "destroy"):
                            widget.destroy()

                self.item_entries = []  # Reset the item entries list

                # Recreate item rows from the loaded configuration
                for entry in config.get("item_entries", []):
                    self.add_item_row()  # Add a new row
                    self.item_entries[-1][0].set(entry["item"])  # item_var
                    self.item_entries[-1][1].set(entry["sell_modifier"])  # sell_modifier
                    self.item_entries[-1][2].set(entry["buy_modifier"])  # buy_modifier
                    self.item_entries[-1][3].set(entry["quantity"])  # quantity_var

                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingApp(root)
    root.mainloop()
