# ============================================================
# FILE: main.py
# ============================================================
"""Entry point aplikasi"""
import tkinter as tk
from views import CurrencyConverterGUI
from controllers import AppController


def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    root = tk.Tk()
    view = CurrencyConverterGUI(root)
    controller = AppController(view)
    root.mainloop()


if __name__ == "__main__":
    main()
