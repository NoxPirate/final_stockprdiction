# Stock Prediction Application



This repository contains a stock market prediction application utilizing deep learning and web technologies. The project provides a platform for analyzing historical stock data and forecasting future trends.

## Features

The application incorporates various functionalities related to stock analysis:

* **User Registration and Authentication**: The platform allows users to register and log in securely. The user data is managed within the `instance/users.db` database file.


* **Database Management**: Includes Python scripts for database operations, such as adding test users (`scripts/add_test_user.py`) and inspecting the database structure (`scripts/inspect_db.py`).


* **Predictive Modeling**: Utilizes a pre-trained Keras model (`mainapp/Stock Prediction model.keras`) for generating stock price predictions. The architecture suggests an LSTM (Long Short-Term Memory) approach (`lstm.py`, `mainapp/lstm v1.py`), commonly used for time-series forecasting.


* **Web Interface**: The application features a front-end developed with CSS and HTML. It includes specific stylesheets for different sections like cryptocurrencies (`static/css/crypto.css`), news (`static/css/news.css`), and registration (`static/css/register.css`).


* **Data Handling**: Contains components for fetching or managing financial data, potentially including mutual funds (`mutualfunds.py`) and historical stock screener data (`nasdaq_screener_1729353736245.csv`).



## Technologies Used

* **Backend**: Python.


* **Deep Learning**: Keras (implied by the `.keras` model file) and likely TensorFlow.


* **Database**: SQLite (implied by the `.db` files in the `instance` directory).


* **Frontend**: HTML, CSS, JavaScript (implied by the `static` directory).



## Repository Structure

The project is structured into several key directories:

* **`instance/`**: Contains the SQLite database files (`app.db`, `database.db`, `users.db`).


* **`stockpr/stockpr-main/`**: The primary application directory.


* **`mainapp/`**: Contains the core application logic, views, URLs, and the saved Keras model.


* **`scripts/`**: Utility scripts for database management.


* **`static/`**: Holds static assets like CSS stylesheets and images.


* **Root files**: Includes setup scripts (`start_platform.bat`), environment configuration examples (`.env.example`), and core Python modules.





## Setup and Installation

1. Review the `requirements.txt` file for necessary Python dependencies.


2. Use the `start_platform.bat` script (for Windows) to potentially automate the setup or launch process.


3. Ensure environment variables are configured correctly, referencing the `.env.example` file.
