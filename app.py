import tkinter as tk  
from tkinter import messagebox, simpledialog  
import matplotlib.pyplot as plt  
import pandas as pd  
from datetime import datetime  
from pathlib import Path  
import math  

# File to store data  
DATA_FILE = Path(__file__).with_name("study_data.csv")  
ASSESSMENT_TARGET_HOURS = 100  

REQUIRED_COLUMNS = ["Name", "Date", "Hours Studied", "Roll Number"]  

def load_data():  
    try:  
        df = pd.read_csv(DATA_FILE, dtype={"Roll Number": "string"})  
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):  
        messagebox.showerror("Error", "No valid study data found!")  
        return None  

    if df.empty or any(column not in df.columns for column in REQUIRED_COLUMNS):  
        messagebox.showerror("Error", "The study data file has no valid records.")  
        return None  

    df["Hours Studied"] = pd.to_numeric(df["Hours Studied"], errors="coerce")  
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  
    df = df.dropna(subset=["Name", "Date", "Hours Studied"])  
    if df.empty:  
        messagebox.showerror("Error", "The study data file has no valid records.")  
        return None  
    return df  

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
        if not math.isfinite(hours) or hours < 0:  
            raise ValueError  
    except ValueError:  
        messagebox.showerror("Error", "Hours studied must be a non-negative number!")  
        return  

    try:  
        datetime.strptime(date, "%Y-%m-%d")  
    except ValueError:  
        messagebox.showerror("Error", "Date must use YYYY-MM-DD format!")  
        return  

    df = pd.DataFrame([[name, date, hours, roll_no]],  
                      columns=["Name", "Date", "Hours Studied", "Roll Number"])  
    df.to_csv(DATA_FILE, mode='a', header=not DATA_FILE.exists(), index=False)  
      
    messagebox.showinfo("Success", "Data saved successfully!")  
    entry_name.delete(0, tk.END)  
    entry_date.delete(0, tk.END)  
    entry_hours.delete(0, tk.END)  
    entry_rollno.delete(0, tk.END)  

# Function to estimate fail risk or topper chance from study hours
def assess_student():  
    roll_no = simpledialog.askstring("Assess Student", "Enter the student's roll number:")  
    if roll_no is None:  
        return  
    roll_no = roll_no.strip()  
    if not roll_no:  
        messagebox.showerror("Error", "Roll number is required!")  
        return  

    df = load_data()  
    if df is None:  
        return  

    student_data = df[df["Roll Number"].str.strip() == roll_no]  
    if student_data.empty:  
        messagebox.showerror("Error", f"No study records found for roll number {roll_no}.")  
        return  

    total_hours = float(student_data["Hours Studied"].sum())  
    estimated_marks = min(max(total_hours / ASSESSMENT_TARGET_HOURS * 100, 0), 100)  
    student_name = student_data.iloc[0]["Name"]  
    result = (  
        f"Student: {student_name}\n"  
        f"Cumulative study hours: {total_hours:g} / {ASSESSMENT_TARGET_HOURS}\n"  
        f"Estimated marks: {estimated_marks:.1f}%\n\n"  
    )  
    disclaimer = "This is a rough estimate based only on study hours, not actual marks."  

    if estimated_marks < 30:  
        messagebox.showwarning(  
            "Risk Warning",  
            result + "Risk of failing: 99%\n" + disclaimer,  
        )  
    elif estimated_marks > 96:  
        messagebox.showinfo(  
            "CHEERS!",  
            result + "Chance of being a topper: 99%\n" + disclaimer,  
        )  
    else:  
        messagebox.showinfo(  
            "Assessment",  
            result + "Risk of failing: 50%\nChance of being a topper: 50%\n" + disclaimer,  
        )  

# Function to display Bar Graph  
def show_bar_graph():  
    df = load_data()  
    if df is None:  
        return  
    df.groupby("Name")["Hours Studied"].sum().plot(kind="bar", color="skyblue", edgecolor="black")  
    plt.title("Total Hours Studied by Students")  
    plt.xlabel("Student Name")  
    plt.ylabel("Hours Studied")  
    plt.show()  

# Function to display Line Graph  
def show_line_graph():  
    df = load_data()  
    if df is None:  
        return  
    df.sort_values("Date", inplace=True)  
    for name, group in df.groupby("Name"):  
        plt.plot(group["Date"], group["Hours Studied"], marker='o', label=name)  
    plt.title("Study Progress Over Time")  
    plt.xlabel("Date")  
    plt.ylabel("Hours Studied")  
    plt.legend()  
    plt.show()  

# Function to display Histogram  
def show_histogram():  
    df = load_data()  
    if df is None:  
        return  
    plt.hist(df["Hours Studied"], bins=5, color="lightgreen", edgecolor="black")  
    plt.title("Distribution of Study Hours")  
    plt.xlabel("Hours Studied")  
    plt.ylabel("Frequency")  
    plt.show()  

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
tk.Button(root, text="Assess Risk / Topper Chance", command=assess_student, bg="#607D8B", fg="white").pack(pady=5)  

root.mainloop()  