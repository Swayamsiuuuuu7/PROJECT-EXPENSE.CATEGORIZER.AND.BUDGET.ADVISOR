import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Expense Dashboard")
app.geometry("900x600")

expenses = []

categories = {
    "Food": ["pizza", "burger", "food", "restaurant"],
    "Travel": ["uber", "bus", "train", "taxi"],
    "Shopping": ["amazon", "clothes", "shopping"],
    "Bills": ["rent", "electricity", "wifi"]
}

def categorize(item):
    item = item.lower()
    for cat, words in categories.items():
        for w in words:
            if w in item:
                return cat
    return "Other"

def add_expense():
    text = entry.get()
    if text == "":
        return
    
    try:
        name, amount = text.rsplit(" ", 1)
        amount = float(amount)
    except:
        return
    
    category = categorize(name)
    expenses.append((name, category, amount))
    
    tree.insert("", "end", values=(name, category, amount))
    entry.delete(0, "end")
    update_summary()

def update_summary():
    total = sum(x[2] for x in expenses)
    summary = {}
    
    for _, cat, amt in expenses:
        summary[cat] = summary.get(cat, 0) + amt
    
    text = f"Total: ₹{total}\n\n"
    
    for cat, amt in summary.items():
        percent = (amt / total) * 100 if total else 0
        text += f"{cat}: ₹{amt} ({percent:.1f}%)\n"
        if percent > 40:
            text += f"⚠ High spending on {cat}\n"
    
    summary_label.configure(text=text)

def show_pie():
    summary = {}
    
    for _, cat, amt in expenses:
        summary[cat] = summary.get(cat, 0) + amt
    
    if not summary:
        return
    
    plt.figure()
    plt.pie(summary.values(), labels=summary.keys(), autopct='%1.1f%%')
    plt.title("Expense Distribution")
    plt.show()

title = ctk.CTkLabel(app, text="💰 Expense Dashboard", font=("Arial", 28))
title.pack(pady=15)

input_frame = ctk.CTkFrame(app, corner_radius=15)
input_frame.pack(pady=10, padx=20, fill="x")

entry = ctk.CTkEntry(input_frame, width=400, placeholder_text="Enter expense (Pizza 300)")
entry.pack(side="left", padx=10, pady=10)

add_btn = ctk.CTkButton(input_frame, text="Add", fg_color="#4CAF50", hover_color="#45a049", command=add_expense)
add_btn.pack(side="left", padx=10)

table_frame = ctk.CTkFrame(app, corner_radius=15)
table_frame.pack(pady=10, padx=20, fill="both", expand=True)

tree = ttk.Treeview(table_frame, columns=("Name", "Category", "Amount"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")

tree.column("Name", width=250)
tree.column("Category", width=150)
tree.column("Amount", width=100)

tree.pack(fill="both", expand=True, padx=10, pady=10)

bottom_frame = ctk.CTkFrame(app, corner_radius=15)
bottom_frame.pack(pady=10, padx=20, fill="x")

summary_label = ctk.CTkLabel(bottom_frame, text="", justify="left", font=("Arial", 14))
summary_label.pack(side="left", padx=10, pady=10)

graph_btn = ctk.CTkButton(bottom_frame, text="📊 Show Pie Chart", fg_color="#2196F3", hover_color="#1976D2", command=show_pie)
graph_btn.pack(side="right", padx=10)

app.mainloop()
