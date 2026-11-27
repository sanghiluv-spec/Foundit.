"""
Campus Lost & Found System
Team: Code Plus
Course: Computational Thinking and Programming
Course Code: 2026CSAE100
Academic Year: 2026-27
"""

import json
from datetime import datetime

DATA_FILE = "lost_found_data.json"
items = []


def load_data():
    """Load saved item records from JSON file."""
    global items
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            items = json.load(file)
    except FileNotFoundError:
        items = []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with empty records.")
        items = []


def save_data():
    """Save all item records to JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4)
    except OSError as error:
        print(f"Error saving data: {error}")


def get_non_empty(prompt):
    """Read a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_date():
    """Read a date in DD-MM-YYYY format, with today as the default."""
    while True:
        value = input(
            "Date (DD-MM-YYYY, press Enter for today's date): "
        ).strip()
        if not value:
            return datetime.now().strftime("%d-%m-%Y")
        try:
            datetime.strptime(value, "%d-%m-%Y")
            return value
        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY.")


def next_id():
    """Generate the next numeric item ID."""
    if not items:
        return 1
    return max(int(item["id"]) for item in items) + 1


def report_item(item_type):
    """Add a lost or found item."""
    print(f"\n--- Report {item_type} Item ---")
    item = {
        "id": next_id(),
        "type": item_type,
        "name": get_non_empty("Item name: "),
        "category": get_non_empty("Category: "),
        "description": get_non_empty("Description: "),
        "location": get_non_empty("Location: "),
        "date": get_date(),
        "contact": get_non_empty("Contact information: "),
        "status": "Open"
    }
    items.append(item)
    save_data()
    print(f"Item reported successfully. Item ID: {item['id']}")


def report_lost_item():
    report_item("Lost")


def report_found_item():
    report_item("Found")


def display_item(item):
    print(
        f"ID: {item['id']} | {item['type']} | {item['name']} | "
        f"{item['category']} | {item['location']} | "
        f"{item['date']} | Status: {item['status']}"
    )
    print(f"  Description: {item['description']}")
    print(f"  Contact: {item['contact']}")


def search_item():
    """Search records using name, category, location, or description."""
    print("\n--- Search Items ---")
    keyword = get_non_empty("Enter search keyword: ").lower()

    matches = []
    for item in items:
        searchable = " ".join([
            str(item["name"]),
            str(item["category"]),
            str(item["location"]),
            str(item["description"]),
            str(item["type"])
        ]).lower()
        if keyword in searchable:
            matches.append(item)

    if not matches:
        print("No matching items found.")
        return

    print(f"\n{len(matches)} matching item(s) found:")
    for item in matches:
        display_item(item)


def similarity_score(lost, found):
    """Calculate a simple rule-based matching score out of 4."""
    score = 0
    if lost["name"].lower() == found["name"].lower():
        score += 1
    if lost["category"].lower() == found["category"].lower():
        score += 1
    if lost["location"].lower() == found["location"].lower():
        score += 1
    if lost["description"].lower() == found["description"].lower():
        score += 1
    return score


def match_items():
    """Find possible lost/found matches using simple rules."""
    print("\n--- Possible Matches ---")
    lost_items = [item for item in items
                  if item["type"] == "Lost" and item["status"] == "Open"]
    found_items = [item for item in items
                   if item["type"] == "Found" and item["status"] == "Open"]

    if not lost_items or not found_items:
        print("At least one open Lost and one open Found record are required.")
        return

    found_match = False
    for lost in lost_items:
        for found in found_items:
            score = similarity_score(lost, found)
            if score >= 2:
                found_match = True
                print(
                    f"Possible match: Lost ID {lost['id']} "
                    f"<-> Found ID {found['id']} | Score: {score}/4"
                )
                print(f"  Lost:  {lost['name']} at {lost['location']}")
                print(f"  Found: {found['name']} at {found['location']}")

    if not found_match:
        print("No possible matches found.")


def view_all_items():
    """Display all records."""
    print("\n--- All Items ---")
    if not items:
        print("No records available.")
        return

    for item in items:
        display_item(item)


def update_status():
    """Update the status of an item."""
    print("\n--- Update Item Status ---")
    try:
        item_id = int(input("Enter Item ID: ").strip())
    except ValueError:
        print("Invalid Item ID. Please enter a number.")
        return

    item = next((record for record in items if record["id"] == item_id), None)
    if item is None:
        print("Item ID not found.")
        return

    print("1. Open")
    print("2. Resolved")
    choice = input("Choose status: ").strip()

    if choice == "1":
        item["status"] = "Open"
    elif choice == "2":
        item["status"] = "Resolved"
    else:
        print("Invalid choice.")
        return

    save_data()
    print(f"Item {item_id} status updated to {item['status']}.")


def print_menu():
    print("\n" + "=" * 45)
    print("        CAMPUS LOST & FOUND SYSTEM")
    print("=" * 45)
    print("1. Report Lost Item")
    print("2. Report Found Item")
    print("3. Search Item")
    print("4. Find Possible Matches")
    print("5. View All Items")
    print("6. Update Item Status")
    print("7. Exit")
    print("=" * 45)


def main():
    load_data()

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            report_lost_item()
        elif choice == "2":
            report_found_item()
        elif choice == "3":
            search_item()
        elif choice == "4":
            match_items()
        elif choice == "5":
            view_all_items()
        elif choice == "6":
            update_status()
        elif choice == "7":
            save_data()
            print("Thank you for using Campus Lost & Found System.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
