import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import auth

# The BankDashboard class handles the user dashboard after login.
class BankDashboard:

    # Initialize with username
    def __init__(self, username):
        self.username = username
        self.window = tk.Toplevel()
        self.window.title("SecureBank Dashboard")
        self.window.geometry("520x200")
        self.window.minsize(520, 175)

        # Load user data
        user_data = auth.load_data()[username]
        self.balance_var = tk.StringVar(value=f"${user_data['balance']:,.2f}")

        # Build the dashboard UI
        self._build_header()
        self._build_action_buttons()
        self._build_logout()

    # Refresh balance display
    def _refresh_balance(self):
        data = auth.load_data()
        self.balance_var.set(f"${data[self.username]['balance']:,.2f}")

    # Perform deposit/withdrawal
    def _perform_transaction(self, amount, operation):
        data = auth.load_data()
        if operation == "Withdraw":
            if data[self.username]["balance"] < amount: # insufficient funds
                return False, "Insufficient funds."
            data[self.username]["balance"] -= amount # withdraw funds
        elif operation == "Deposit": 
            data[self.username]["balance"] += amount # deposit funds
        else: # invalid operation
            return False, "Invalid operation."

        # Log the transaction
        log = {"type": operation, "amount": amount, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}
        data[self.username].setdefault("history", []).append(log) # add to history
        auth.save_data(data) # save updated data
        self._refresh_balance() # update balance display
        return True, "Transaction complete." # success message

    # Build header section
    def _build_header(self):
        tk.Label(self.window, text=f"Welcome, {self.username}", font=("Arial", 14)).pack(pady=10)
        bal_frame = tk.Frame(self.window)
        bal_frame.pack(pady=5)
        tk.Label(bal_frame, text="Current Balance:", font=("Arial", 12, "bold")).pack(side="left", padx=(0,8))
        tk.Label(bal_frame, textvariable=self.balance_var, font=("Arial", 14, "bold"), fg="green").pack(side="left")

    # Build action buttons
    def _build_action_buttons(self):
        top_btn_frame = tk.Frame(self.window)
        top_btn_frame.pack(pady=10, fill="x", padx=10)
        tk.Button(top_btn_frame, text="Transfer Funds", command=self.open_transfer_dialog).pack(side="left", expand=True, fill="x", padx=6)
        tk.Button(top_btn_frame, text="View Transaction History", command=self.show_history).pack(side="left", expand=True, fill="x", padx=6)

    # Build logout button
    def _build_logout(self):
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(side="bottom", fill="x", pady=10, padx=10)
        tk.Button(bottom_frame, text="Logout", command=self.window.destroy).pack(side="right")

    # Open dialog for transfer funds
    def open_transfer_dialog(self):
        dlg = tk.Toplevel(self.window)
        dlg.title("Transfer Funds")
        dlg.transient(self.window)
        dlg.grab_set()

        # Amount entry
        tk.Label(dlg, text="Amount:").grid(column=0, row=0, padx=8, pady=8, sticky="e")
        amt_ent = tk.Entry(dlg)
        amt_ent.grid(column=1, row=0, padx=8, pady=8, sticky="w")

        # Action selection
        action_var = tk.StringVar(value="Withdraw")
        tk.Radiobutton(dlg, text="Deposit", variable=action_var, value="Deposit").grid(column=0, row=1, padx=8, pady=4)
        tk.Radiobutton(dlg, text="Withdraw", variable=action_var, value="Withdraw").grid(column=1, row=1, padx=8, pady=4)

        # OK and Cancel buttons
        def on_ok():
            try:
                amount = float(amt_ent.get()) # parse amount
            except Exception: # invalid amount
                messagebox.showerror("Error", "Invalid amount.", parent=dlg, icon='error')
                return
            if amount <= 0: # non-positive amount
                messagebox.showerror("Error", "Amount must be positive.", parent=dlg, icon='error')
                return

            op = action_var.get() 
            ok, msg = self._perform_transaction(amount, op) # perform transaction
            if not ok:
                messagebox.showerror("Error", msg, parent=dlg, icon='error')
                return
            messagebox.showinfo("Success", msg, parent=dlg, icon='info')
            dlg.destroy()

        tk.Button(dlg, text="OK", command=on_ok, width=10).grid(column=0, row=2, padx=8, pady=10)
        tk.Button(dlg, text="Cancel", command=dlg.destroy, width=10).grid(column=1, row=2, padx=8, pady=10)
        dlg.wait_window()

    # Show transaction history
    def show_history(self):
        hist_win = tk.Toplevel(self.window)
        hist_win.title("Transaction History")
        lb = tk.Listbox(hist_win, width=60, font=("Courier", 10))
        lb.pack(padx=10, pady=10)

        # Load transaction history
        data = auth.load_data()
        history = data[self.username].get("history", []) 
        if not history: # no history
            lb.insert(tk.END, "No transactions.")
            return

        # Display history with running balance
        running_balance = data[self.username].get("balance", 0.0)
        for entry in reversed(history):  # show most recent first
            typ = (entry.get("type") or "").capitalize()
            amt = float(entry.get("amount", 0.0))
            sign = "-" if typ.lower().startswith("withdraw") else "+"
            lb.insert(tk.END, f"{entry.get('date','?')} | {typ:<7} | {sign}${amt:,.2f} | Balance: ${running_balance:,.2f}")
            
            # Update running balance
            if typ.lower().startswith("withdraw"):
                running_balance += amt
            else:
                running_balance -= amt