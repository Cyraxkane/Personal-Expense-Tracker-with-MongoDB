# Personal Expense Tracker (OOP + MongoDB)

A Python console application to track daily spending using Object-Oriented Programming and MongoDB.

## Setup Instructions

1. **Install MongoDB**: Ensure you have MongoDB installed and running locally on port 27017, or use a MongoDB Atlas URI.
2. **MongoDB Installation on Ubuntu 24.04"
  ```bash
  sudo apt update
  sudo apt install -y gnupg curl
  curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor
  echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
  sudo apt update
  sudo apt install -y mongodb-org
```
3. **Clone the Repo**:
   ```bash
   git clone [(https://github.com/Cyraxkane/Personal-Expense-Tracker-with-MongoDB.git)]
   cd expense-tracker
   ```
4. **Install Depedencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run an app**:
   ```bash
   python3 main.py
   ```
**Features**

- OOP Design: Separate classes for Data (Expense) and Logic (ExpenseTracker).

- Data Persistence: Connects to MongoDB to store and retrieve records.

- Validation: Ensures dates are correctly formatted and amounts are positive.

