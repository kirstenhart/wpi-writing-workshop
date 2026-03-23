This README provides an overview of **SecureBank Pro**, a Python-based desktop simulation of a banking system.

---

# SecureBank Pro

**SecureBank Pro** is a lightweight GUI application built with Python and Tkinter. It simulates a core banking experience, allowing users to securely create accounts, manage balances, and track their financial history through a responsive interface.

## Features

* **Secure Authentication**: Employs SHA-256 hashing to ensure user passwords are never stored in plain text.
* **User Registration**: New users can register an account and receive a default starting balance of $1,000.00.
* **Dynamic Dashboard**: A dedicated user interface that displays real-time balance updates.
* **Transaction Management**: Users can perform "Transfer Funds" actions, including both deposits and withdrawals.
* **Transaction History**: A detailed log of all account activity, featuring timestamps and a calculated running balance for every entry.
* **Responsive Design**: The UI utilizes Tkinter’s grid and weight configurations to remain functional across different window sizes.

## Requirements

* **Python 3.x**
* **Tkinter library** (standard in most Python distributions)

## How to Run

1. Download or clone the project files into a single directory.
2. Open your terminal or command prompt.
3. Navigate to the project folder.
4. Execute the application by running:
```bash
python main.py
```



## File Layout

* **`main.py`**: The entry point of the application. It handles the primary window, login logic, and user registration UI.
* **`auth.py`**: The security and data layer. It manages SHA-256 hashing and handles reading/writing to the local database.
* **`dashboard.py`**: Contains the `BankDashboard` class, which manages the post-login experience, including transactions and history views.
* **`users.json`**: (Automatically generated) A local JSON file that acts as the database for user credentials, balances, and logs.

## Security Notes

* **Data Privacy**: By using the `hashlib` module, the app ensures that even if the `users.json` file is accessed, original passwords remain protected via one-way encryption.
* **Local Storage**: All data is stored locally on your machine.
* **Purpose**: This application is intended for **educational and prototyping purposes**. It should not be used to store actual financial data or sensitive personal information.