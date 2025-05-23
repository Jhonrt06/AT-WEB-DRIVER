# 🛒 Amazon Automation Bot

This project is an automation system built with [Playwright](https://playwright.dev/python/) for interacting with [Amazon.com.mx](https://www.amazon.com.mx/).  
It supports automated flows such as logging in, searching for products, and more (extensible to checkout).

---

## 🚀 Features

- ✅ Open Amazon homepage
- ✅ Log in using credentials
- ✅ Search for products
- 🚧 [WIP] Add to cart
- 🚧 [WIP] Full purchase flow
- 📄 Logging and structured architecture
- 🌐 Ready for REST API integration (FastAPI)

---

## 📁 Project Structure

    AT-WEB-DRIVER/
    ├── automation/
    │ ├── base_bot.py # Launches and manages Playwright browser
    │ ├── playwright_utils.py # Reusable helper methods
    │ ├── playwright_constants.py # Centralized CSS selectors
    │ └── test_cases/
    │ └── comprar_bot.py # Main test bot class
    ├── config/
    │ ├── logger_config.py # Logging configuration
    │ └── settings.py # Loads environment variables
    ├── .vscode/
    │ └── settings.json # VS Code editor settings (80-char limit)
    ├── .env # URL and headless mode settings
    ├── main.py # Entry point for launching flows
    ├── requirements.in # Direct dependencies
    ├── requirements.txt # Frozen dependency versions
    ├── dev-requirements.in # Development-only dependencies
    ├── dev-requirements.txt # Frozen dev dependencies
    └── README.md

    
---

## ⚙️ Installation

### 1. Clone the repository

git clone https://github.com/Jhonrt06/AT-WEB-DRIVER.git
cd AT-WEB-DRIVER

### 2. Set up a virtual environment

python -m venv venv
.\venv\Scripts\activate           # On Windows

### 3. Install the required packages:

pip install -r requirements.txt

## Running the Application

python main.py