import mysql.connector

# Establish a connection to the MySQL server
conn = mysql.connector.connect(host="localhost",user="root",password="Push@123",database="health")

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Example: Execute a query to create a table
create_table_query = '''CREATE TABLE IF NOT EXISTS example_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255)
    )'''
cursor.execute(create_table_query)

# Example: Insert data into the table
insert_data_query = "INSERT INTO example_table (name) VALUES (%s)"
data_to_insert = ("John Doe",)
cursor.execute(insert_data_query, data_to_insert)

# Commit the changes
conn.commit()

# Example: Select data from the table
select_data_query = "SELECT * FROM example_table"
cursor.execute(select_data_query)

# Fetch all the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()


import tkinter as tk
from tkinter import ttk
from datetime import date

class HealthTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Tracker")

        # Entry fields
        self.date_entry = ttk.Entry(root)
        self.weight_entry = ttk.Entry(root)

        # Buttons
        ttk.Button(root, text="Add Record", command=self.add_record).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(root, text="View Records", command=self.view_records).grid(row=2, column=2, columnspan=2, pady=10)

        # Labels
        ttk.Label(root, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(root, text="Weight (kg):").grid(row=0, column=2, padx=10, pady=10)

        # Set default date to today
        self.date_entry.insert(0, str(date.today()))

    def add_record(self):
        date_val = self.date_entry.get()
        weight_val = self.weight_entry.get()

        # Validate input
        if not date_val or not weight_val:
            return

        # Insert record into the database
        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO weight_records (date, weight) VALUES (?, ?)", (date_val, float(weight_val)))
        conn.commit()
        conn.close()

        # Clear entry fields
        self.date_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')

    def view_records(self):
        # Open a new window to view records
        view_window = tk.Toplevel(self.root)
        view_window.title("Weight Records")

        # Treeview to display records
        tree = ttk.Treeview(view_window)
        tree["columns"] = ("ID", "Date", "Weight")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", anchor=tk.CENTER, width=50)
        tree.column("Date", anchor=tk.CENTER, width=100)
        tree.column("Weight", anchor=tk.CENTER, width=100)

        tree.heading("#0", text="", anchor=tk.CENTER)
        tree.heading("ID", text="ID", anchor=tk.CENTER)
        tree.heading("Date", text="Date", anchor=tk.CENTER)
        tree.heading("Weight", text="Weight (kg)", anchor=tk.CENTER)

        # Fetch records from the database and populate the Treeview
        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weight_records")
        records = cursor.fetchall()
        for record in records:
            tree.insert("", tk.END, values=record)

        tree.pack()

# Run the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthTrackerApp(root)
    root.mainloop()
