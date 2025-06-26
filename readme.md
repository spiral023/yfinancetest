# YFinance Stock App

This is a simple Streamlit application that uses the `yfinance` library to fetch and display stock data.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/yfinancetest.git
    cd yfinancetest
    ```
    (Note: Replace `your-username/yfinancetest.git` with the actual repository URL if you push this to GitHub.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Streamlit application:

```bash
streamlit run streamlit_app.py
```

This will open the application in your web browser.

## Project Structure

-   `streamlit_app.py`: The main Streamlit application file.
-   `stock_app.py`: Contains functions or classes for fetching and processing stock data (if separated from `streamlit_app.py`).
-   `requirements.txt`: Lists all Python dependencies.
-   `readme.md`: This README file.
