import tkinter as tk  
from tkinter import messagebox  
import matplotlib.pyplot as plt  
import pandas as pd  
from datetime import datetime  

# File to store data  
DATA_FILE = "study_data.csv"  

# Function to save study data  
def save_data():  
    name = entry_name.get()  
    date = entry_date.get()  
    hours = entry_hours.get()  
    roll_no = entry_rollno.get()  

    if not (name and date and hours and roll_no):  
        messagebox.showerror("Error", "All fields are required!")  
        return  
      
    try:  
        hours = float(hours)  
    except ValueError:  
        messagebox.showerror("Error", "Hours studied must be a number!")  
        return  

    df = pd.DataFrame([[name, date, hours, roll_no]],  
                      columns=["Name", "Date", "Hours Studied", "Roll Number"])  
    df.to_csv(DATA_FILE, mode='a', header=not pd.io.common.file_exists(DATA_FILE), index=False)  
      
    messagebox.showinfo("Success", "Data saved successfully!")  
    entry_name.delete(0, tk.END)  
    entry_date.delete(0, tk.END)  
    entry_hours.delete(0, tk.END)  
    entry_rollno.delete(0, tk.END)  

# Function to display Bar Graph  
def show_bar_graph():  
    try:  
        df = pd.read_csv(DATA_FILE)  
        df.groupby("Name")["Hours Studied"].sum().plot(kind="bar", color="skyblue", edgecolor="black")  
        plt.title("Total Hours Studied by Students")  
        plt.xlabel("Student Name")  
        plt.ylabel("Hours Studied")  
        plt.show()  
    except FileNotFoundError:  
        messagebox.showerror("Error", "No data found!")  

# Function to display Line Graph  
def show_line_graph():  
    try:  
        df = pd.read_csv(DATA_FILE)  
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  
        df.sort_values("Date", inplace=True)  
        for name, group in df.groupby("Name"):  
            plt.plot(group["Date"], group["Hours Studied"], marker='o', label=name)  
        plt.title("Study Progress Over Time")  
        plt.xlabel("Date")  
        plt.ylabel("Hours Studied")  
        plt.legend()  
        plt.show()  
    except FileNotFoundError:  
        messagebox.showerror("Error", "No data found!")  

# Function to display Histogram  
def show_histogram():  
    try:  
        df = pd.read_csv(DATA_FILE)  
        plt.hist(df["Hours Studied"], bins=5, color="lightgreen", edgecolor="black")  
        plt.title("Distribution of Study Hours")  
        plt.xlabel("Hours Studied")  
        plt.ylabel("Frequency")  
        plt.show()  
    except FileNotFoundError:  
        messagebox.showerror("Error", "No data found!")  

# GUI Setup  
root = tk.Tk()  
root.title("Student Performance Tracker")  
root.geometry("400x400")  
root.configure(bg="#f2f2f2")  

tk.Label(root, text="Name:", bg="#f2f2f2").pack()  
entry_name = tk.Entry(root)  
entry_name.pack()  

tk.Label(root, text="Date (YYYY-MM-DD):", bg="#f2f2f2").pack()  
entry_date = tk.Entry(root)  
entry_date.pack()  

tk.Label(root, text="Hours Studied:", bg="#f2f2f2").pack()  
entry_hours = tk.Entry(root)  
entry_hours.pack()  

tk.Label(root, text="Roll Number:", bg="#f2f2f2").pack()  
entry_rollno = tk.Entry(root)  
entry_rollno.pack()  

tk.Button(root, text="Save Data", command=save_data, bg="#4CAF50", fg="white").pack(pady=5)  
tk.Button(root, text="Show Bar Graph", command=show_bar_graph, bg="#2196F3", fg="white").pack(pady=5)  
tk.Button(root, text="Show Line Graph", command=show_line_graph, bg="#FF9800", fg="white").pack(pady=5)  
tk.Button(root, text="Show Histogram", command=show_histogram, bg="#9C27B0", fg="white").pack(pady=5)  

root.mainloop()