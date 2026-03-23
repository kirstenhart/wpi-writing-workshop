import tkinter as tk
from tkinter import messagebox
import auth
from dashboard import BankDashboard

# Login attempt
def attempt_login():
    u, p = user_ent.get(), pass_ent.get()
    success, user_data = auth.authenticate_user(u, p)
    if success:
        user_ent.delete(0, tk.END)
        pass_ent.delete(0, tk.END)
        BankDashboard(u) # Launch the dashboard from the other file
    else:
        messagebox.showerror("Error", "Invalid Login")

# Registration attempt
def attempt_register():
    u, p = user_ent.get(), pass_ent.get()
    if u and p:
        success, msg = auth.register_user(u, p)
        if success: messagebox.showinfo("Success", msg)
        else: messagebox.showwarning("Error", msg)

# Main application window
root = tk.Tk()
root.title("SecureBank Pro")

# Set window size and minimum size
root.geometry("520x200")
root.minsize(520, 175)

# Make root responsive
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create containers and widgets
content = tk.Frame(root, padx=5, pady=5)
frame = tk.Frame(content, borderwidth=5, width=200, height=100, padx=5, pady=5)

login_lbl = tk.Label(frame, text="SecureBank Login", font=("Arial", 14, "bold"))
user_lbl = tk.Label(content, text="Username: ")
user_ent = tk.Entry(content)
pass_lbl = tk.Label(content, text="Password: ")
pass_ent = tk.Entry(content, show="*")

login_bttn = tk.Button(content, text="Login", command=attempt_login, width=15)
reg_bttn = tk.Button(content, text="Register New Account", command=attempt_register, width=20)

# Layout the widgets
content.grid(column=0, row=0, sticky="nsew")
frame.grid(column=0, row=0, sticky="ew")

# Make content and frame responsive
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# Position widgets
login_lbl.grid(column=0, row=0, pady=(0,8), sticky="ew")
user_lbl.grid(column=0, row=1, sticky="e", padx=(0,6), pady=4)
user_ent.grid(column=1, row=1, sticky="ew", pady=4)
pass_lbl.grid(column=0, row=2, sticky="e", padx=(0,6), pady=4)
pass_ent.grid(column=1, row=2, sticky="ew", pady=4)
login_bttn.grid(column=0, row=3, padx=2, pady=(8,0), sticky="ew")
reg_bttn.grid(column=1, row=3, padx=2, pady=(8,0), sticky="ew")

root.mainloop()