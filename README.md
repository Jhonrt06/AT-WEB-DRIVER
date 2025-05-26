# 🛒 AT-WEB-DRIVER

Automated test and interaction framework for web applications, designed using **Playwright** and **FastAPI**.

This modular and scalable project automates interactions with [Amazon.com.mx](https://www.amazon.com.mx/) and can be extended to other sites.  
It also exposes a backend API for integration with external tools or dashboards.

---

## 🚀 Features

- ✅ Opens Amazon homepage  
- ✅ Logs in with user credentials  
- ✅ Product search functionality  
- 🛒 Purchase flow 
- 📄 Logging system for all interactions  
- 🧱 Modular architecture following Clean Code principles  
- ⚙️ RESTful API via FastAPI

---

## 📁 Project Structure

AT-WEB-DRIVER/  
├── automation/           # Playwright automation scripts  
│   └── test_cases/       # Modular automation flows  
├── api/                  # FastAPI endpoints (optional)  
├── config/               # Configuration and environment loading  
├── logs/                 # Execution logs  
├── main.py               # Entry point for FastAPI app  
├── requirements.txt      # Runtime dependencies  
├── dev-requirements.txt  # Developer tools (e.g., linters, formatters)  
├── .env                  # Environment variables (excluded from Git)  
└── README.md             # Project documentation  

---

## ⚙️ Prerequisites

- Python 3.9 to 3.10  
- Playwright for Python  
- Uvicorn for FastAPI  
- A `.env` file containing credentials and configurations  

---

## 📦 Installation

### 1. Clone the repository

git clone https://github.com/Jhonrt06/AT-WEB-DRIVER.git  
cd AT-WEB-DRIVER

### 2. Create a virtual environment

python -m venv venv

#### Activate the environment:

On Windows:  
.\venv\Scripts\activate

On macOS/Linux:  
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt  
pip install -r dev-requirements.txt  
playwright install

### 4. Configure environment variables

Create a `.env` file in the root directory with the following content:

AMAZON_EMAIL=your_email@example.com  
AMAZON_PASSWORD=your_password  
HEADLESS=true  
API_HOST=http://127.0.0.1:8000

**Never commit your `.env` file to version control.**

---

## ▶️ Running the Project

### Start the FastAPI server

uvicorn main:app

- Starts the API defined in `main.py`  
- Enables hot-reloading on code changes  
- Default access: http://127.0.0.1:8000

### Access the API documentation

Swagger UI: http://127.0.0.1:8000/docs  
ReDoc: http://127.0.0.1:8000/redoc

---

## 🤖 Running Automation Flows

    Expose these flows through API endpoints.

---

## ✅ Best Practices

- Logging is configured in `config/logs/logger_config.py`  
- Selectors are centralized in `playwright_constants.py`  
- Common actions are implemented in `PlaywrightUtils`  
- Decorators like `@log_step` and `@safe_action` are used for clean logging and error handling  

---

## 📬 Contact

Maintained by [@Jhonrt06](https://github.com/Jhonrt06)
