import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


class CurrencyConverter:
    """Class untuk menangani konversi mata uang"""
    
    def __init__(self):
        self.rates = {}
        self.base_currency = 'USD'
        self.last_update = None
        
    def fetch_rates(self):
        """Mengambil data kurs dari API"""
        try:
            url = f'https://api.exchangerate-api.com/v4/latest/{self.base_currency}'
            response = requests.get(url, timeout=10)
            data = response.json()
            self.rates = data['rates']
            self.last_update = datetime.now()
            return True
        except Exception as e:
            print(f"Error fetching rates: {e}")
            return False
    
    def convert(self, amount, from_currency, to_currency):
        """Konversi mata uang"""
        if not self.rates:
            return None
        
        try:
            amount = float(amount)
            if from_currency == self.base_currency:
                result = amount * self.rates[to_currency]
            elif to_currency == self.base_currency:
                result = amount / self.rates[from_currency]
            else:
                # Konversi ke USD dulu, baru ke target currency
                usd_amount = amount / self.rates[from_currency]
                result = usd_amount * self.rates[to_currency]
            return result
        except (ValueError, KeyError) as e:
            print(f"Conversion error: {e}")
            return None
    
    def get_rate(self, from_currency, to_currency):
        """Mendapatkan rate antara dua mata uang"""
        if not self.rates:
            return None
        
        try:
            if from_currency == self.base_currency:
                return self.rates[to_currency]
            elif to_currency == self.base_currency:
                return 1 / self.rates[from_currency]
            else:
                return self.rates[to_currency] / self.rates[from_currency]
        except KeyError:
            return None


class CurrencyConverterGUI:
    """Class untuk GUI aplikasi konverter nilai mata uang"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Konverter Nilai Mata Uang")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Inisialisasi converter
        self.converter = CurrencyConverter()
        
        # Daftar mata uang
        self.currencies = {
            'USD': '🇺🇸 US Dollar',
            'EUR': '🇪🇺 Euro',
            'GBP': '🇬🇧 British Pound',
            'IDR': '🇮🇩 Indonesian Rupiah',
            'JPY': '🇯🇵 Japanese Yen',
            'CNY': '🇨🇳 Chinese Yuan',
            'SGD': '🇸🇬 Singapore Dollar',
            'MYR': '🇲🇾 Malaysian Ringgit',
            'AUD': '🇦🇺 Australian Dollar',
            'CAD': '🇨🇦 Canadian Dollar',
            'CHF': '🇨🇭 Swiss Franc',
            'KRW': '🇰🇷 South Korean Won',
            'THB': '🇹🇭 Thai Baht',
            'INR': '🇮🇳 Indian Rupee',
            'AED': '🇦🇪 UAE Dirham'
        }
        
        self.setup_ui()
        self.load_rates()
    
    def setup_ui(self):
        """Membuat tampilan UI"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#4F46E5', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="💱 KONVERTER NILAI MATA UANG",
            font=('Arial', 20, 'bold'),
            bg='#4F46E5',
            fg='white'
        )
        title_label.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#F3F4F6', padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Frame Dari (From)
        from_frame = tk.LabelFrame(
            main_frame,
            text="Dari",
            font=('Arial', 11, 'bold'),
            bg='#F3F4F6',
            fg='#1F2937',
            padx=15,
            pady=15
        )
        from_frame.pack(fill='x', pady=(0, 10))
        
        input_frame = tk.Frame(from_frame, bg='#F3F4F6')
        input_frame.pack(fill='x')
        
        self.amount_entry = tk.Entry(
            input_frame,
            font=('Arial', 16),
            width=15,
            justify='right',
            bd=2,
            relief='solid'
        )
        self.amount_entry.pack(side='left', padx=(0, 10), ipady=8)
        self.amount_entry.insert(0, '1')
        self.amount_entry.bind('<KeyRelease>', lambda e: self.convert_currency())
        
        self.from_currency = ttk.Combobox(
            input_frame,
            values=list(self.currencies.values()),
            font=('Arial', 11),
            width=20,
            state='readonly'
        )
        self.from_currency.pack(side='left', ipady=8)
        self.from_currency.current(0)  # USD
        self.from_currency.bind('<<ComboboxSelected>>', lambda e: self.convert_currency())
        
        # Tombol Swap
        swap_frame = tk.Frame(main_frame, bg='#F3F4F6')
        swap_frame.pack(pady=10)
        
        swap_button = tk.Button(
            swap_frame,
            text="⇅ Tukar",
            font=('Arial', 12, 'bold'),
            bg='#4F46E5',
            fg='white',
            command=self.swap_currencies,
            padx=20,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        swap_button.pack()
        
        # Frame Ke (To)
        to_frame = tk.LabelFrame(
            main_frame,
            text="Ke",
            font=('Arial', 11, 'bold'),
            bg='#F3F4F6',
            fg='#1F2937',
            padx=15,
            pady=15
        )
        to_frame.pack(fill='x', pady=(0, 10))
        
        output_frame = tk.Frame(to_frame, bg='#F3F4F6')
        output_frame.pack(fill='x')
        
        self.result_var = tk.StringVar(value='0.00')
        result_entry = tk.Entry(
            output_frame,
            textvariable=self.result_var,
            font=('Arial', 16, 'bold'),
            width=15,
            justify='right',
            state='readonly',
            bd=2,
            relief='solid',
            bg='#E5E7EB'
        )
        result_entry.pack(side='left', padx=(0, 10), ipady=8)
        
        self.to_currency = ttk.Combobox(
            output_frame,
            values=list(self.currencies.values()),
            font=('Arial', 11),
            width=20,
            state='readonly'
        )
        self.to_currency.pack(side='left', ipady=8)
        self.to_currency.current(3)  # IDR
        self.to_currency.bind('<<ComboboxSelected>>', lambda e: self.convert_currency())
        
        # Info Rate
        self.rate_label = tk.Label(
            main_frame,
            text="",
            font=('Arial', 10),
            bg='#DBEAFE',
            fg='#1E40AF',
            padx=15,
            pady=10,
            relief='solid',
            bd=1
        )
        self.rate_label.pack(fill='x', pady=(10, 0))
        
        # Button Frame
        button_frame = tk.Frame(main_frame, bg='#F3F4F6')
        button_frame.pack(pady=15)
        
        refresh_button = tk.Button(
            button_frame,
            text="🔄 Refresh Kurs",
            font=('Arial', 11, 'bold'),
            bg='#10B981',
            fg='white',
            command=self.load_rates,
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        refresh_button.pack(side='left', padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=('Arial', 11, 'bold'),
            bg='#EF4444',
            fg='white',
            command=self.clear_fields,
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        clear_button.pack(side='left', padx=5)
        
        # Status bar
        self.status_label = tk.Label(
            main_frame,
            text="Memuat data kurs...",
            font=('Arial', 9),
            bg='#F3F4F6',
            fg='#6B7280',
            anchor='w'
        )
        self.status_label.pack(fill='x', pady=(10, 0))
    
    def get_currency_code(self, full_name):
        """Mendapatkan kode mata uang dari nama lengkap"""
        for code, name in self.currencies.items():
            if name == full_name:
                return code
        return None
    
    def load_rates(self):
        """Memuat data kurs dari API"""
        self.status_label.config(text="Memuat data kurs...")
        self.root.update()
        
        success = self.converter.fetch_rates()
        
        if success:
            update_time = self.converter.last_update.strftime('%d/%m/%Y %H:%M:%S')
            self.status_label.config(
                text=f"✅ Data kurs diperbarui: {update_time}"
            )
            self.convert_currency()
            messagebox.showinfo("Sukses", "Data kurs berhasil diperbarui!")
        else:
            self.status_label.config(text="❌ Gagal memuat data kurs")
            messagebox.showerror("Error", "Gagal memuat data kurs. Periksa koneksi internet Anda.")
    
    def convert_currency(self):
        """Melakukan konversi mata uang"""
        try:
            amount = self.amount_entry.get()
            if not amount:
                return
            
            from_curr = self.get_currency_code(self.from_currency.get())
            to_curr = self.get_currency_code(self.to_currency.get())
            
            if not from_curr or not to_curr:
                return
            
            result = self.converter.convert(amount, from_curr, to_curr)
            
            if result is not None:
                self.result_var.set(f"{result:,.2f}")
                
                # Update rate info
                rate = self.converter.get_rate(from_curr, to_curr)
                if rate:
                    self.rate_label.config(
                        text=f"1 {from_curr} = {rate:,.4f} {to_curr}"
                    )
            else:
                self.result_var.set("Error")
                
        except Exception as e:
            print(f"Conversion error: {e}")
            self.result_var.set("0.00")
    
    def swap_currencies(self):
        """Menukar posisi mata uang"""
        from_idx = self.from_currency.current()
        to_idx = self.to_currency.current()
        
        self.from_currency.current(to_idx)
        self.to_currency.current(from_idx)
        
        self.convert_currency()
    
    def clear_fields(self):
        """Membersihkan input"""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '1')
        self.result_var.set('0.00')
        self.rate_label.config(text='')
        self.from_currency.current(0)
        self.to_currency.current(3)


def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()
    app = CurrencyConverterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
