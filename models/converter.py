# ============================================================
# FILE: models/converter.py
# ============================================================
"""Model untuk konversi mata uang"""
import requests
from datetime import datetime
from typing import Optional, Dict


class CurrencyConverter:
    """Class untuk menangani konversi mata uang"""
    
    def __init__(self, base_currency: str = 'USD'):
        """
        Inisialisasi converter
        
        Args:
            base_currency: Mata uang dasar untuk konversi
        """
        self.rates: Dict[str, float] = {}
        self.base_currency = base_currency
        self.last_update: Optional[datetime] = None
        self.api_url = f'https://api.exchangerate-api.com/v4/latest/{base_currency}'
    
    def fetch_rates(self) -> bool:
        """
        Mengambil data kurs dari API
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            self.rates = data['rates']
            self.last_update = datetime.now()
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching rates: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        """
        Konversi mata uang
        
        Args:
            amount: Jumlah uang yang akan dikonversi
            from_currency: Kode mata uang asal
            to_currency: Kode mata uang tujuan
            
        Returns:
            Hasil konversi atau None jika error
        """
        if not self.rates:
            return None
        
        try:
            amount = float(amount)
            
            if from_currency == self.base_currency:
                result = amount * self.rates[to_currency]
            elif to_currency == self.base_currency:
                result = amount / self.rates[from_currency]
            else:
                # Konversi ke base currency dulu, baru ke target
                base_amount = amount / self.rates[from_currency]
                result = base_amount * self.rates[to_currency]
                
            return result
            
        except (ValueError, KeyError, ZeroDivisionError) as e:
            print(f"Conversion error: {e}")
            return None
    
    def get_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """
        Mendapatkan rate antara dua mata uang
        
        Args:
            from_currency: Kode mata uang asal
            to_currency: Kode mata uang tujuan
            
        Returns:
            Nilai tukar atau None jika error
        """
        if not self.rates:
            return None
        
        try:
            if from_currency == self.base_currency:
                return self.rates[to_currency]
            elif to_currency == self.base_currency:
                return 1 / self.rates[from_currency]
            else:
                return self.rates[to_currency] / self.rates[from_currency]
                
        except (KeyError, ZeroDivisionError):
            return None
    
    def get_last_update_formatted(self) -> str:
        """
        Mendapatkan waktu update terakhir dalam format string
        
        Returns:
            String waktu update atau 'Belum ada data'
        """
        if self.last_update:
            return self.last_update.strftime('%d/%m/%Y %H:%M:%S')
        return 'Belum ada data'