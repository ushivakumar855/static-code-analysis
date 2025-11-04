"""Inventory management system.
This module manages stock items with add, remove, and tracking capabilities.
It supports loading and saving inventory data to JSON files.
"""
import json
from datetime import datetime

stock_data = {}

def add_item(item="default", qty=0, logs=None):
    """Add an item to inventory with quantity tracking."""
    if logs is None:
        logs = []
    if not isinstance(item, str) or not item:
        print("Error: Item must be a non-empty string")
        return
    if not isinstance(qty, int):
        print("Error: Quantity must be an integer")
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")

def remove_item(item, qty):
    """Remove quantity of an item from inventory."""
    try:
        if not isinstance(qty, int) or qty < 0:
            print("Error: Quantity must be a positive integer")
            return
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            print(f"Removed {item} from inventory")
    except KeyError:
        print(f"Item '{item}' not found in inventory.")

def get_qty(item):
    """Get quantity of an item in inventory."""
    return stock_data.get(item, 0)

def load_data(file="inventory.json"):
    """Load inventory data from JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Update the existing stock_data dict in-place to avoid using 'global'
            if isinstance(data, dict):
                stock_data.clear()
                stock_data.update(data)
                print(f"Loaded inventory from {file}")
            else:
                print(f"Warning: {file} does not contain a valid inventory map")
    except FileNotFoundError:
        print(f"File {file} not found. Starting with empty inventory.")
    except json.JSONDecodeError:
        print(f"Error: {file} is not valid JSON")

def save_data(file="inventory.json"):
    """Save inventory data to JSON file."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f)
            print(f"Saved inventory to {file}")
    except IOError as e:
        print(f"Error saving to {file}: {e}")

def print_data():
    """Print all items in inventory."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")

def check_low_items(threshold=5):
    """Check items with quantity below threshold."""
    result = []
    for item, qty in stock_data.items():
        if qty < threshold:
            result.append(item)
    return result

def main():
    """Main execution function."""
    add_item("apple", 10)
    add_item("banana", 5)
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()

if __name__ == "__main__":
    main()
