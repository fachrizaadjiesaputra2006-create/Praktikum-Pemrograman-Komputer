# ============================================================
# FILE: views/gui.py
# ============================================================
"""GUI View untuk aplikasi konverter mata uang"""
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from utils.constants import CURRENCIES, COLORS, WINDOW_CONFIG


class CurrencyConverterGUI:
    """Class untuk GUI aplikasi konverter mata uang"""
    
    def __init__(self, root: tk.Tk):
        """
        Inisialisasi GUI
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.currencies = CURRENCIES
        self.colors = COLORS
        
        # Callback functions (akan diset oleh controller)
        self.on_convert: Optional[Callable] = None
        self.on_swap: Optional[Callable] = None
        self.on_refresh: Optional[Callable] = None
        self.on_clear: Optional[Callable] = None
        
        self._configure_window()
        self._create_widgets()
    
    def _configure_window(self):
        """Konfigurasi window utama"""
        self.root.title(WINDOW_CONFIG['title'])
        self.root.geometry(f"{WINDOW_CONFIG['width']}x{WINDOW_CONFIG['height']}")
        self.root.resizable(WINDOW_CONFIG['resizable'], WINDOW_CONFIG['resizable'])
        self.root.configure(bg=self.colors['background'])
    
    def _create_widgets(self):
        """Membuat semua widget GUI"""
        self._create_header()
        self._create_main_frame()
        self._create_from_section()
        self._create_swap_button()
        self._create_to_section()
        self._create_rate_info()
        self._create_buttons()
        self._create_status_bar()
    
    def _create_header(self):
        """Membuat header aplikasi"""
        header_frame = tk.Frame(
            self.root,
            bg=self.colors['primary'],
            height=80
        )
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="💱 KONVERTER MATA UANG",
            font=('Arial', 20, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(pady=20)
    
    def _create_main_frame(self):
        """Membuat main container"""
        self.main_frame = tk.Frame(
            self.root,
            bg=self.colors['background'],
            padx=30,
            pady=20
        )
        self.main_frame.pack(fill='both', expand=True)
    
    def _create_from_section(self):
        """Membuat section 'Dari'"""
        from_frame = tk.LabelFrame(
            self.main_frame,
            text="Dari",
            font=('Arial', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        from_frame.pack(fill='x', pady=(0, 10))
        
        input_frame = tk.Frame(from_frame, bg=self.colors['background'])
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
        self.amount_entry.bind('<KeyRelease>', lambda e: self._trigger_convert())
        
        self.from_currency = ttk.Combobox(
            input_frame,
            values=list(self.currencies.values()),
            font=('Arial', 11),
            width=20,
            state='readonly'
        )
        self.from_currency.pack(side='left', ipady=8)
        self.from_currency.current(0)
        self.from_currency.bind('<<ComboboxSelected>>', lambda e: self._trigger_convert())
    
    def _create_swap_button(self):
        """Membuat tombol swap"""
        swap_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        swap_frame.pack(pady=10)
        
        self.swap_button = tk.Button(
            swap_frame,
            text="⇅ Tukar",
            font=('Arial', 12, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            command=self._trigger_swap,
            padx=20,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        self.swap_button.pack()
    
    def _create_to_section(self):
        """Membuat section 'Ke'"""
        to_frame = tk.LabelFrame(
            self.main_frame,
            text="Ke",
            font=('Arial', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text_dark'],
            padx=15,
            pady=15
        )
        to_frame.pack(fill='x', pady=(0, 10))
        
        output_frame = tk.Frame(to_frame, bg=self.colors['background'])
        output_frame.pack(fill='x')
        
        self.result_var = tk.StringVar(value='0.00')
        self.result_entry = tk.Entry(
            output_frame,
            textvariable=self.result_var,
            font=('Arial', 16, 'bold'),
            width=15,
            justify='right',
            state='readonly',
            bd=2,
            relief='solid',
            bg=self.colors['disabled']
        )
        self.result_entry.pack(side='left', padx=(0, 10), ipady=8)
        
        self.to_currency = ttk.Combobox(
            output_frame,
            values=list(self.currencies.values()),
            font=('Arial', 11),
            width=20,
            state='readonly'
        )
        self.to_currency.pack(side='left', ipady=8)
        self.to_currency.current(3)
        self.to_currency.bind('<<ComboboxSelected>>', lambda e: self._trigger_convert())
    
    def _create_rate_info(self):
        """Membuat label info rate"""
        self.rate_label = tk.Label(
            self.main_frame,
            text="",
            font=('Arial', 10),
            bg=self.colors['info_bg'],
            fg=self.colors['info_text'],
            padx=15,
            pady=10,
            relief='solid',
            bd=1
        )
        self.rate_label.pack(fill='x', pady=(10, 0))
    
    def _create_buttons(self):
        """Membuat tombol-tombol aksi"""
        button_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        button_frame.pack(pady=15)
        
        self.refresh_button = tk.Button(
            button_frame,
            text="🔄 Refresh Kurs",
            font=('Arial', 11, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            command=self._trigger_refresh,
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        self.refresh_button.pack(side='left', padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            font=('Arial', 11, 'bold'),
            bg=self.colors['danger'],
            fg=self.colors['white'],
            command=self._trigger_clear,
            padx=15,
            pady=8,
            cursor='hand2',
            relief='flat'
        )
        self.clear_button.pack(side='left', padx=5)
    
    def _create_status_bar(self):
        """Membuat status bar"""
        self.status_label = tk.Label(
            self.main_frame,
            text="Memuat data kurs...",
            font=('Arial', 9),
            bg=self.colors['background'],
            fg=self.colors['text_light'],
            anchor='w'
        )
        self.status_label.pack(fill='x', pady=(10, 0))
    
    # Trigger methods
    def _trigger_convert(self):
        """Trigger callback konversi"""
        if self.on_convert:
            self.on_convert()
    
    def _trigger_swap(self):
        """Trigger callback swap"""
        if self.on_swap:
            self.on_swap()
    
    def _trigger_refresh(self):
        """Trigger callback refresh"""
        if self.on_refresh:
            self.on_refresh()
    
    def _trigger_clear(self):
        """Trigger callback clear"""
        if self.on_clear:
            self.on_clear()
    
    # Getter methods
    def get_amount(self) -> str:
        """Mendapatkan nilai amount"""
        return self.amount_entry.get()
    
    def get_from_currency(self) -> str:
        """Mendapatkan mata uang asal"""
        return self.from_currency.get()
    
    def get_to_currency(self) -> str:
        """Mendapatkan mata uang tujuan"""
        return self.to_currency.get()
    
    def get_from_index(self) -> int:
        """Mendapatkan index mata uang asal"""
        return self.from_currency.current()
    
    def get_to_index(self) -> int:
        """Mendapatkan index mata uang tujuan"""
        return self.to_currency.current()
    
    # Setter methods
    def set_result(self, value: str):
        """Set hasil konversi"""
        self.result_var.set(value)
    
    def set_rate_info(self, text: str):
        """Set info rate"""
        self.rate_label.config(text=text)
    
    def set_status(self, text: str):
        """Set status message"""
        self.status_label.config(text=text)
    
    def set_from_currency_index(self, index: int):
        """Set index mata uang asal"""
        self.from_currency.current(index)
    
    def set_to_currency_index(self, index: int):
        """Set index mata uang tujuan"""
        self.to_currency.current(index)
    
    def clear_amount(self):
        """Clear amount entry"""
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, '1')
    
    def get_currency_code_from_display(self, display_name: str) -> Optional[str]:
        """
        Mendapatkan kode mata uang dari display name
        
        Args:
            display_name: Nama tampilan mata uang
            
        Returns:
            Kode mata uang atau None
        """
        for code, name in self.currencies.items():
            if name == display_name:
                return code
        return None