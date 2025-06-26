import yfinance as yf
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Information App")
        self.geometry("800x800")

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Stock Ticker:").pack(side=tk.LEFT)
        self.ticker_entry = tk.Entry(input_frame, width=20)
        self.ticker_entry.pack(side=tk.LEFT, padx=5)
        self.ticker_entry.bind("<Return>", self.fetch_and_display_stock_info)

        fetch_button = tk.Button(input_frame, text="Fetch Info", command=self.fetch_and_display_stock_info)
        fetch_button.pack(side=tk.LEFT)

        # Info Display Frame
        self.info_frame = tk.LabelFrame(self, text="Stock Details", padx=10, pady=10)
        self.info_frame.pack(padx=10, pady=10, fill=tk.X)

        # Configure grid for info_frame
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure(1, weight=1)

        self.labels = {}
        info_fields = [
            ("Company Name:", "company_name"),
            ("Sector:", "sector"),
            ("Industry:", "industry"),
            ("Country:", "country"),
            ("Website:", "website"),
            ("Current Price:", "current_price"),
            ("Previous Close:", "previous_close"),
            ("Change:", "change"),
            ("Market Cap:", "market_cap"),
            ("PE Ratio:", "pe_ratio"),
            ("Dividend Yield:", "dividend_yield"),
            ("Beta:", "beta"),
            ("EPS:", "eps"),
            ("Price/Book Ratio:", "price_to_book"),
            ("52 Week High:", "fifty_two_week_high"),
            ("52 Week Low:", "fifty_two_week_low")
        ]

        for i, (text, key) in enumerate(info_fields):
            tk.Label(self.info_frame, text=text, anchor="w", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", pady=2, padx=5)
            self.labels[key] = tk.Label(self.info_frame, text="N/A", anchor="w", font=("Arial", 10))
            self.labels[key].grid(row=i, column=1, sticky="w", pady=2, padx=5)

        # Time Period Selection
        time_period_frame = tk.Frame(self)
        time_period_frame.pack(pady=5)

        tk.Label(time_period_frame, text="Select Time Period:").pack(side=tk.LEFT)
        self.time_period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        self.time_period_var = tk.StringVar(self)
        self.time_period_var.set("5d") # default value
        self.time_period_menu = tk.OptionMenu(time_period_frame, self.time_period_var, *self.time_period_options, command=self.fetch_and_display_stock_info)
        self.time_period_menu.pack(side=tk.LEFT, padx=5)

        # Plot Frame
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def update_info_label(self, key, value):
        if key in self.labels:
            self.labels[key].config(text=value)

    def fetch_stock_data(self, ticker):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get current price and change
            todays_data = stock.history(period='1d')
            current_price = "N/A"
            previous_close = "N/A"
            change = "N/A"
            change_percent = "N/A"

            if not todays_data.empty:
                current_price = todays_data['Close'].iloc[0]
                previous_close = info.get('previousClose')
                if previous_close is not None:
                    change = current_price - previous_close
                    change_percent = (change / previous_close) * 100
                
            # Get historical data based on selected period
            selected_period = self.time_period_var.get()
            hist_data = stock.history(period=selected_period)

            return {
                "company_name": info.get('longName', 'N/A'),
                "sector": info.get('sector', 'N/A'),
                "industry": info.get('industry', 'N/A'),
                "country": info.get('country', 'N/A'),
                "website": info.get('website', 'N/A'),
                "current_price": f"{current_price:.2f}" if isinstance(current_price, (int, float)) else current_price,
                "previous_close": f"{previous_close:.2f}" if isinstance(previous_close, (int, float)) else previous_close,
                "change": f"{change:.2f} ({change_percent:.2f}%)" if isinstance(change, (int, float)) else change,
                "market_cap": f"{info.get('marketCap', 'N/A'):,}",
                "pe_ratio": f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), (int, float)) else info.get('trailingPE', 'N/A'),
                "dividend_yield": f"{info.get('dividendYield', 0) * 100:.2f}%",
                "beta": f"{info.get('beta', 'N/A'):.2f}" if isinstance(info.get('beta'), (int, float)) else info.get('beta', 'N/A'),
                "eps": f"{info.get('trailingEps', 'N/A'):.2f}" if isinstance(info.get('trailingEps'), (int, float)) else info.get('trailingEps', 'N/A'),
                "price_to_book": f"{info.get('priceToBook', 'N/A'):.2f}" if isinstance(info.get('priceToBook'), (int, float)) else info.get('priceToBook', 'N/A'),
                "fifty_two_week_high": f"{info.get('fiftyTwoWeekHigh', 'N/A'):.2f}" if isinstance(info.get('fiftyTwoWeekHigh'), (int, float)) else info.get('fiftyTwoWeekHigh', 'N/A'),
                "fifty_two_week_low": f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f}" if isinstance(info.get('fiftyTwoWeekLow'), (int, float)) else info.get('fiftyTwoWeekLow', 'N/A'),
                "historical_data": hist_data
            }
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data for {ticker.upper()}: {e}\n\nCommon issues:\n- Invalid ticker symbol.\n- No internet connection.\n- API rate limit exceeded (try again later).")
            return None

    def fetch_and_display_stock_info(self, event=None):
        ticker = self.ticker_entry.get().strip().upper()
        if not ticker:
            messagebox.showwarning("Input Error", "Please enter a stock ticker symbol.")
            return

        data = self.fetch_stock_data(ticker)
        if data:
            self.update_info_label("company_name", data["company_name"])
            self.update_info_label("sector", data["sector"])
            self.update_info_label("industry", data["industry"])
            self.update_info_label("country", data["country"])
            self.update_info_label("website", data["website"])
            self.update_info_label("current_price", data["current_price"])
            self.update_info_label("previous_close", data["previous_close"])
            self.update_info_label("change", data["change"])
            self.update_info_label("market_cap", data["market_cap"])
            self.update_info_label("pe_ratio", data["pe_ratio"])
            self.update_info_label("dividend_yield", data["dividend_yield"])
            self.update_info_label("beta", data["beta"])
            self.update_info_label("eps", data["eps"])
            self.update_info_label("price_to_book", data["price_to_book"])
            self.update_info_label("fifty_two_week_high", data["fifty_two_week_high"])
            self.update_info_label("fifty_two_week_low", data["fifty_two_week_low"])

            self.plot_historical_data(data["historical_data"], ticker)

    def plot_historical_data(self, hist_data, ticker):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        if not hist_data.empty:
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(hist_data.index, hist_data['Close'], marker='o', linestyle='-', color='blue')
            ax.set_title(f"{ticker.upper()} Historical Close Price ({self.time_period_var.get()})", fontsize=12)
            ax.set_xlabel("Date", fontsize=10)
            ax.set_ylabel("Close Price", fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.7)
            fig.autofmt_xdate()
            plt.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
        else:
            tk.Label(self.plot_frame, text="No historical data available for plotting.").pack()

if __name__ == "__main__":
    app = StockApp()
    app.mainloop()
