"""
Contact Manager Pro - Business Edition
A comprehensive CRM solution for small businesses and professionals
"""

import json
import csv
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import uuid

class ContactManagerPro:
    def __init__(self, file_name="contacts.json"):
        self.file_name = file_name
        self.contacts = self.load_contacts()
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)

    # Enhanced file handling with backups
    def load_contacts(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_contacts(self):
        # Create backup before saving
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"contacts_backup_{timestamp}.json")
        with open(backup_file, "w") as backup:
            json.dump(self.contacts, backup)
            
        with open(self.file_name, "w") as file:
            json.dump(self.contacts, file, indent=4)

    # Premium Contact Features
    def add_contact(self, name, phone, email, address, tags=None, company="", notes=""):
        contact_id = str(uuid.uuid4())[:8]  # Unique ID
        new_contact = {
            "id": contact_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "company": company,
            "tags": tags or [],
            "notes": notes,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_contact": "",
            "value": 0.00  # For customer lifetime value tracking
        }
        self.contacts.append(new_contact)
        self.save_contacts()
        print(f"Contact '{name}' added successfully (ID: {contact_id}).")
        return contact_id

    # Enhanced Viewing Options
    def view_contacts(self, sort_by="name", filter_tags=None):
        if not self.contacts:
            print("No contacts found.")
            return

        filtered = self.contacts
        if filter_tags:
            filtered = [c for c in filtered if any(tag in c.get("tags", []) for tag in filter_tags)]

        sorted_contacts = sorted(filtered, key=lambda x: x.get(sort_by, ""))
        
        print("\n📋 Contact List:")
        print(f"{'ID':<8} {'Name':<20} {'Phone':<15} {'Company':<20} {'Tags':<15}")
        print("-" * 70)
        for contact in sorted_contacts:
            print(f"{contact['id']:<8} {contact['name'][:19]:<20} {contact['phone'][:14]:<15} "
                  f"{contact.get('company','')[:19]:<20} {', '.join(contact.get('tags',[]))[:14]:<15}")

    # Advanced Search
    def search_contact(self, query, search_fields=["name", "phone", "email", "company", "tags"]):
        results = []
        for contact in self.contacts:
            for field in search_fields:
                if field == "tags":
                    if any(query.lower() in tag.lower() for tag in contact.get(field, [])):
                        results.append(contact)
                        break
                elif query.lower() in str(contact.get(field, "")).lower():
                    results.append(contact)
                    break

        if not results:
            print("No contacts found matching your query.")
        else:
            print(f"\n🔍 Found {len(results)} matching contacts:")
            for contact in results:
                self.display_contact_details(contact)

    # Professional Display
    def display_contact_details(self, contact):
        print(f"\n📇 Contact ID: {contact['id']}")
        print(f"👤 Name: {contact['name']}")
        print(f"📞 Phone: {contact['phone']}")
        print(f"📧 Email: {contact['email']}")
        print(f"🏢 Company: {contact.get('company', 'N/A')}")
        print(f"🏠 Address: {contact['address']}")
        print(f"🏷️ Tags: {', '.join(contact.get('tags', [])) or 'None'}")
        print(f"💵 Estimated Value: ${contact.get('value', 0):.2f}")
        print(f"📅 Last Contact: {contact.get('last_contact', 'Never')}")
        print(f"⏰ Created: {contact.get('created_at', 'Unknown')}")
        print("-" * 40)

    # Business Features
    def export_contacts(self, format_type="csv"):
        filename = f"contacts_export_{datetime.now().strftime('%Y%m%d')}.{format_type}"
        if format_type == "csv":
            with open(filename, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.contacts[0].keys())
                writer.writeheader()
                writer.writerows(self.contacts)
        print(f"Contacts exported successfully to {filename}")

    def send_email_to_contact(self, contact_id, subject, body):
        contact = next((c for c in self.contacts if c["id"] == contact_id), None)
        if not contact:
            print("Contact not found.")
            return

        try:
            # Configure your SMTP settings here
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = "your_business@example.com"
            msg["To"] = contact["email"]

            with smtplib.SMTP("smtp.example.com", 587) as server:
                server.starttls()
                server.login("your_email@example.com", "password")
                server.send_message(msg)
            print(f"Email sent successfully to {contact['name']}")
            
            # Update last contact date
            contact["last_contact"] = datetime.now().strftime("%Y-%m-%d")
            self.save_contacts()
        except Exception as e:
            print(f"Error sending email: {str(e)}")

    # Monetization Features
    def calculate_customer_value(self):
        total_value = sum(contact.get("value", 0) for contact in self.contacts)
        print(f"\n💰 Total Customer Value: ${total_value:.2f}")
        print(f"👥 Average Value per Contact: ${total_value/len(self.contacts):.2f}" if self.contacts else "N/A")

    def add_transaction(self, contact_id, amount, description=""):
        for contact in self.contacts:
            if contact["id"] == contact_id:
                contact["value"] = contact.get("value", 0) + float(amount)
                if description:
                    contact.setdefault("transactions", []).append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "amount": amount,
                        "description": description
                    })
                self.save_contacts()
                print(f"Added ${amount} transaction to {contact['name']}'s record")
                return
        print("Contact not found.")

def display_premium_menu():
    print("\nCONTACT MANAGER PRO - Business Edition")
    print("1.  Add Contact")
    print("2.  View Contacts")
    print("3.  Search Contacts")
    print("4.  Update Contact")
    print("5.  Delete Contact")
    print("6.  Export Contacts")
    print("7.  Email Contact")
    print("8.  Add Transaction")
    print("9.  Calculate Customer Value")
    print("10. Exit")
    print("\n💎 Premium Features:")
    print("- Customer Value Tracking")
    print("- Bulk Email Integration")
    print("- Transaction History")
    print("- Advanced Tagging System")

def main():
    manager = ContactManagerPro()
    
    print("""
    ██████╗ ██████╗ ███╗   ██╗████████╗ █████╗  ██████╗████████╗
    ██╔═══██╗██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚══██╔══╝
    ██║   ██║██████╔╝██╔██╗ ██║   ██║   ███████║██║        ██║   
    ██║   ██║██╔══██╗██║╚██╗██║   ██║   ██╔══██║██║        ██║   
    ╚██████╔╝██║  ██║██║ ╚████║   ██║   ██║  ██║╚██████╗   ██║   
     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝   ╚═╝   
    """)

    while True:
        display_premium_menu()
        choice = input("\nChoose an option (1-10): ").strip()
        
        if choice == "1":
            print("\n➕ Add New Contact")
            name = input("Full Name: ").strip()
            phone = input("Phone: ").strip()
            email = input("Email: ").strip()
            address = input("Address: ").strip()
            company = input("Company (optional): ").strip()
            tags = input("Tags (comma separated): ").strip().split(",")
            notes = input("Notes: ").strip()
            manager.add_contact(name, phone, email, address, [t.strip() for t in tags if t], company, notes)
            
        elif choice == "2":
            print("\nViewing Options:")
            print("1. Basic List")
            print("2. Sorted by Company")
            print("3. Filter by Tags")
            view_choice = input("Choose view option: ").strip()
            if view_choice == "1":
                manager.view_contacts()
            elif view_choice == "2":
                manager.view_contacts(sort_by="company")
            elif view_choice == "3":
                tags = input("Enter tags to filter (comma separated): ").strip().split(",")
                manager.view_contacts(filter_tags=[t.strip() for t in tags])
            else:
                print("Invalid choice, showing default view")
                manager.view_contacts()
                
        elif choice == "3":
            query = input("Enter search term: ").strip()
            print("Search in: 1) All Fields 2) Name/Phone Only")
            search_choice = input("Choose search option: ").strip()
            if search_choice == "1":
                manager.search_contact(query)
            else:
                manager.search_contact(query, ["name", "phone"])
                
        elif choice == "4":
            contact_id = input("Enter contact ID to update: ").strip()
            manager.update_contact(contact_id)
            
        elif choice == "5":
            contact_id = input("Enter contact ID to delete: ").strip()
            manager.delete_contact(contact_id)
            
        elif choice == "6":
            print("Export Format: 1) CSV 2) JSON")
            export_choice = input("Choose format: ").strip()
            manager.export_contacts("csv" if export_choice == "1" else "json")
            
        elif choice == "7":
            contact_id = input("Enter contact ID to email: ").strip()
            subject = input("Email subject: ").strip()
            body = input("Email body: ").strip()
            manager.send_email_to_contact(contact_id, subject, body)
            
        elif choice == "8":
            contact_id = input("Enter contact ID: ").strip()
            amount = input("Transaction amount: $").strip()
            description = input("Description: ").strip()
            manager.add_transaction(contact_id, amount, description)
            
        elif choice == "9":
            manager.calculate_customer_value()
            
        elif choice == "10":
            print("Thank you for using Contact Manager Pro!")
            break
            
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
