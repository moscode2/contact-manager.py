# File: contact_manager.py

import json

class ContactManager:
    def __init__(self, file_name="contacts.json"):
        self.file_name = file_name
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_contacts(self):
        with open(self.file_name, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self, name, phone, email, address):
        self.contacts.append({
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        })
        self.save_contacts()
        print(f"Contact '{name}' added successfully.")

    def view_contacts(self):
        if not self.contacts:
            print("No contacts found.")
            return
        print("\nContact List:")
        for idx, contact in enumerate(self.contacts, start=1):
            print(f"{idx}. {contact['name']} - {contact['phone']}")

    def search_contact(self, query):
        results = [c for c in self.contacts if query.lower() in c["name"].lower() or query in c["phone"]]
        if not results:
            print("No contacts found matching your query.")
        else:
            print("\nSearch Results:")
            for contact in results:
                print(f"Name: {contact['name']}")
                print(f"Phone: {contact['phone']}")
                print(f"Email: {contact['email']}")
                print(f"Address: {contact['address']}")
                print("-" * 20)

    def update_contact(self, name):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                print("Enter new details (leave blank to keep current value):")
                new_name = input(f"Name [{contact['name']}]: ").strip() or contact["name"]
                new_phone = input(f"Phone [{contact['phone']}]: ").strip() or contact["phone"]
                new_email = input(f"Email [{contact['email']}]: ").strip() or contact["email"]
                new_address = input(f"Address [{contact['address']}]: ").strip() or contact["address"]
                contact.update({"name": new_name, "phone": new_phone, "email": new_email, "address": new_address})
                self.save_contacts()
                print("Contact updated successfully.")
                return
        print("Contact not found.")

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact["name"].lower() == name.lower():
                self.contacts.remove(contact)
                self.save_contacts()
                print(f"Contact '{name}' deleted successfully.")
                return
        print("Contact not found.")

def display_menu():
    print("\nContact Manager Menu:")
    print("1. Add Contact")
    print("2. View Contact List")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

def main():
    manager = ContactManager()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone number: ").strip()
            email = input("Enter email: ").strip()
            address = input("Enter address: ").strip()
            manager.add_contact(name, phone, email, address)
        elif choice == "2":
            manager.view_contacts()
        elif choice == "3":
            query = input("Enter name or phone number to search: ").strip()
            manager.search_contact(query)
        elif choice == "4":
            name = input("Enter the name of the contact to update: ").strip()
            manager.update_contact(name)
        elif choice == "5":
            name = input("Enter the name of the contact to delete: ").strip()
            manager.delete_contact(name)
        elif choice == "6":
            print("Exiting Contact Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
