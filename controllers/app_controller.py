# ============================================================
# FILE: controllers/app_controller.py
# ============================================================

"""Controller untuk mengatur logika aplikasi"""
from tkinter import messagebox
from models import CurrencyConverter
from views import CurrencyConverterGUI


class AppController:
    """Controller utama aplikasi"""
    
    def __init__(self, view: CurrencyConverterGUI):
        """
        Inisialisasi controller
        
        Args:
            view: Instance dari GUI view
        """
        self.view = view
        self.model = CurrencyConverter()
        
        # Set callback functions
        self.view.on_convert = self.handle_convert
        self.view.on_swap = self.handle_swap
        self.view.on_refresh = self.handle_refresh
        self.view.on_clear = self.handle_clear
        
        # Load initial rates
        self.handle_refresh()
    
    def handle_convert(self):
        """Handle konversi mata uang"""
        try:
            amount = self.view.get_amount()
            if not amount:
                return
            
            from_display = self.view.get_from_currency()
            to_display = self.view.get_to_currency()
            
            from_code = self.view.get_currency_code_from_display(from_display)
            to_code = self.view.get_currency_code_from_display(to_display)
            
            if not from_code or not to_code:
                return
            
            result = self.model.convert(amount, from_code, to_code)
            
            if result is not None:
                self.view.set_result(f"{result:,.2f}")
                
                # Update rate info
                rate = self.model.get_rate(from_code, to_code)
                if rate:
                    rate_text = f"1 {from_code} = {rate:,.4f} {to_code}"
                    self.view.set_rate_info(rate_text)
            else:
                self.view.set_result("Error")
                messagebox.showerror("Error", "Gagal melakukan konversi")
                
        except Exception as e:
            print(f"Conversion error: {e}")
            self.view.set_result("0.00")
    
    def handle_swap(self):
        """Handle swap mata uang"""
        from_idx = self.view.get_from_index()
        to_idx = self.view.get_to_index()
        
        self.view.set_from_currency_index(to_idx)
        self.view.set_to_currency_index(from_idx)
        
        self.handle_convert()
    
    def handle_refresh(self):
        """Handle refresh data kurs"""
        self.view.set_status("Memuat data kurs...")
        self.view.root.update()
        
        success = self.model.fetch_rates()
        
        if success:
            update_time = self.model.get_last_update_formatted()
            status_text = f"✅ Data kurs diperbarui: {update_time}"
            self.view.set_status(status_text)
            self.handle_convert()
            messagebox.showinfo("Sukses", "Data kurs berhasil diperbarui!")
        else:
            self.view.set_status("❌ Gagal memuat data kurs")
            messagebox.showerror(
                "Error",
                "Gagal memuat data kurs.\nPeriksa koneksi internet Anda."
            )
    
    def handle_clear(self):
        """Handle clear/reset form"""
        self.view.clear_amount()
        self.view.set_result('0.00')
        self.view.set_rate_info('')
        self.view.set_from_currency_index(0)
        self.view.set_to_currency_index(3)
