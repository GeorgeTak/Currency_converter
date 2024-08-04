import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

# API endpoint and your API key
API_URL = "https://v6.exchangerate-api.com/v6/0026ccf01fb51924732ba83d/latest/USD"

# Comprehensive Currency Information
currency_info = {
    'USD': ('United States Dollar', 'United States'),
    'EUR': ('Euro', 'Eurozone'),
    'GBP': ('British Pound', 'United Kingdom'),
    'JPY': ('Japanese Yen', 'Japan'),
    'INR': ('Indian Rupee', 'India'),
    'AUD': ('Australian Dollar', 'Australia'),
    'CAD': ('Canadian Dollar', 'Canada'),
    'CHF': ('Swiss Franc', 'Switzerland'),
    'CNY': ('Chinese Yuan', 'China'),
    'SEK': ('Swedish Krona', 'Sweden'),
    'NZD': ('New Zealand Dollar', 'New Zealand'),
    'MXN': ('Mexican Peso', 'Mexico'),
    'SGD': ('Singapore Dollar', 'Singapore'),
    'HKD': ('Hong Kong Dollar', 'Hong Kong'),
    'NOK': ('Norwegian Krone', 'Norway'),
    'KRW': ('South Korean Won', 'South Korea'),
    'TRY': ('Turkish Lira', 'Turkey'),
    'RUB': ('Russian Ruble', 'Russia'),
    'BRL': ('Brazilian Real', 'Brazil'),
    'ZAR': ('South African Rand', 'South Africa'),
    'DKK': ('Danish Krone', 'Denmark'),
    'PLN': ('Polish Zloty', 'Poland'),
    'THB': ('Thai Baht', 'Thailand'),
    'IDR': ('Indonesian Rupiah', 'Indonesia'),
    'HUF': ('Hungarian Forint', 'Hungary'),
    'CZK': ('Czech Koruna', 'Czech Republic'),
    'ILS': ('Israeli Shekel', 'Israel'),
    'CLP': ('Chilean Peso', 'Chile'),
    'PHP': ('Philippine Peso', 'Philippines'),
    'AED': ('United Arab Emirates Dirham', 'United Arab Emirates'),
    'COP': ('Colombian Peso', 'Colombia'),
    'SAR': ('Saudi Riyal', 'Saudi Arabia'),
    'MYR': ('Malaysian Ringgit', 'Malaysia'),
    'RON': ('Romanian Leu', 'Romania')
}

class CurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("650x400")
        self.configure(bg='#b2d8d8')  # Set the background color
        self.resizable(False, False)
        
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Arial', 12), background="#ADD8E6")
        self.style.configure('TCombobox', font=('Arial', 12), background="#ADD8E6")
        self.style.configure('TEntry', padding=5, font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12, 'bold'), background='#ADD8E6', foreground='white', relief='flat')
        self.style.map('TButton', background=[('active', '#ADD8E6')], foreground=[('active', 'white')], relief=[('pressed', 'sunken')], borderwidth=[('pressed', 2), ('!pressed', 1)])


        # Amount
        self.amount_label = ttk.Label(self, text="Amount:", style='TLabel')
        self.amount_label.grid(column=0, row=0, padx=10, pady=10, sticky='E')
        
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.grid(column=1, row=0, padx=10, pady=10, sticky='W')
        
        # From Currency
        self.from_currency_label = ttk.Label(self, text="From Currency:", style='TLabel')
        self.from_currency_label.grid(column=0, row=1, padx=10, pady=10, sticky='E')
        
        self.from_currency_combobox = ttk.Combobox(self, values=[], style='TCombobox')
        self.from_currency_combobox.grid(column=1, row=1, padx=10, pady=10, sticky='W')
        
        # To Currency
        self.to_currency_label = ttk.Label(self, text="To Currency:", style='TLabel')
        self.to_currency_label.grid(column=0, row=2, padx=10, pady=10, sticky='E')
        
        self.to_currency_combobox = ttk.Combobox(self, values=[], style='TCombobox')
        self.to_currency_combobox.grid(column=1, row=2, padx=10, pady=10, sticky='W')
        
        # Convert Button
        self.convert_button = ttk.Button(self, text="Convert", style='TButton', command=self.convert_currency)
        self.convert_button.grid(column=0, row=3, columnspan=2, pady=10)
        
        # Result Label
        self.result_label = ttk.Label(self, text="")
        self.result_label.grid(column=0, row=4, columnspan=2, pady=10)
        
        # Scrolled Text for Currency Info
        self.currency_info_label = ttk.Label(self, text="Currency Information:")
        self.currency_info_label.grid(column=2, row=0, padx=10, pady=10, sticky='W')
        
        self.currency_info_text = scrolledtext.ScrolledText(self, width=40, height=15)
        self.currency_info_text.grid(column=2, row=1, rowspan=4, padx=10, pady=10, sticky='W')
        
        # Add exit button
        self.exit_button = ttk.Button(self, text="Exit", style='TButton', command=self.quit)
        self.exit_button.place(x=0, y=370)

        self.exchange_rates = {}
        self.populate_currency_info()
        self.fetch_exchange_rates()
    
    def populate_currency_info(self):
        for code, (name, country) in currency_info.items():
            self.currency_info_text.insert(tk.END, f"{code} - {name} ({country})\n")
        self.currency_info_text.config(state=tk.DISABLED)
    
    def fetch_exchange_rates(self):
        try:
            response = requests.get(API_URL)
            data = response.json()
            if response.status_code == 200:
                self.exchange_rates = data['conversion_rates']
                currencies = list(self.exchange_rates.keys())
                self.from_currency_combobox['values'] = currencies
                self.to_currency_combobox['values'] = currencies
                self.from_currency_combobox.current(0)
                self.to_currency_combobox.current(1)
            else:
                self.result_label.config(text="Failed to fetch exchange rates.")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}")
    
    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_currency = self.from_currency_combobox.get()
            to_currency = self.to_currency_combobox.get()
            
            if from_currency in self.exchange_rates and to_currency in self.exchange_rates:
                converted_amount = amount * (self.exchange_rates[to_currency] / self.exchange_rates[from_currency])
                self.result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            else:
                self.result_label.config(text="Invalid currency selected.")
        except ValueError:
            self.result_label.config(text="Invalid amount entered.")
        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()
