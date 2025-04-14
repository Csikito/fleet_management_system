# 🚚 Fleet Management System

This is a web-based application designed for small and large transportation companies to manage vehicles, deliveries, generate reports, and handle user permissions in a centralized system.

---

## 🚀 Setup & Launch

### 1. Clone the repository
```bash
    git clone https://github.com/Csikito/fleet_management_system.git
    cd fleet_management_system
```

### 2. Create and activate a virtual environment
``` bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate      # Windows
```
### 3. Install dependencies
``` bash
    pip install -r requirements.txt
```

### 4. Set up .fleet.ini and .flaskenv files
Copy the example files to create your actual config files and fill in your own values:
``` bash
    cp .fleet.ini.example .fleet.ini
    cp flaskenv.example .flaskenv
```

### 5. Initialize the database
``` bash
    flask --app migrate_runner.py db upgrade
```

### 6. Start the application
``` bash
    flask run --app fleet_app.py

```


## 📋 Features

- ✅ Vehicle tracking and management
- ✅ User and permission control
- ✅ Delivery logging and monitoring
- ✅ Report generation in PDF, CSV, and XLSX formats
- ✅ Data visualization with Chart.js
- ✅ Full access for admin users


## 🧪 Test Data

You can add new users or vehicles through the admin interface. All features are available for admin-level users.

## 📸 Screenshots
    ...

## 📃 Licenc
This project was created for educational and personal learning purposes.

Author: Csikito