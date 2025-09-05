import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

class URLShortenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сокращатель ссылок - Локальная версия")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        self.api_url = "http://localhost:8001"
        self.setup_ui()
        
    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Собственный сокращатель ссылок", 
                               font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Поле для исходной ссылки
        ttk.Label(main_frame, text="Введите URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50, font=("Arial", 10))
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Поле для кастомного кода (опционально)
        ttk.Label(main_frame, text="Кастомный код (необязательно):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.custom_code_entry = ttk.Entry(main_frame, width=20, font=("Arial", 10))
        self.custom_code_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.shorten_btn = ttk.Button(button_frame, text="Сократить", command=self.shorten_url_thread)
        self.shorten_btn.pack(side=tk.LEFT, padx=5)
        
        self.stats_btn = ttk.Button(button_frame, text="Статистика", command=self.show_stats)
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        # Поле результата
        ttk.Label(main_frame, text="Сокращенная ссылка:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.result_entry = ttk.Entry(main_frame, width=50, font=("Arial", 10), state="readonly")
        self.result_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Кнопка копирования
        self.copy_btn = ttk.Button(main_frame, text="Копировать", command=self.copy_to_clipboard)
        self.copy_btn.grid(row=5, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Лог действий
        ttk.Label(main_frame, text="История действий:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.log_text = scrolledtext.ScrolledText(main_frame, width=55, height=10, font=("Consolas", 9))
        self.log_text.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def log_message(self, message):
        """Добавление сообщения в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        
    def shorten_url_thread(self):
        """Запуск в отдельном потоке"""
        thread = threading.Thread(target=self.shorten_url)
        thread.daemon = True
        thread.start()
        
    def shorten_url(self):
        """Сокращение ссылки"""
        try:
            self.shorten_btn.config(state="disabled")
            self.status_var.set("Сокращаем ссылку...")
            
            url = self.url_entry.get().strip()
            custom_code = self.custom_code_entry.get().strip() or None
            
            if not url:
                messagebox.showerror("Ошибка", "Введите URL для сокращения")
                return
                
            payload = {"original_url": url}
            if custom_code:
                payload["custom_code"] = custom_code
                
            response = requests.post(f"{self.api_url}/api/shorten", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                self.result_entry.config(state="normal")
                self.result_entry.delete(0, tk.END)
                self.result_entry.insert(0, data["short_url"])
                self.result_entry.config(state="readonly")
                
                self.log_message(f"✓ Сокращено: {url} -> {data['short_url']}")
                self.status_var.set("Ссылка успешно сокращена!")
                
            else:
                error_msg = response.json().get("detail", "Неизвестная ошибка")
                messagebox.showerror("Ошибка", error_msg)
                self.log_message(f"✗ Ошибка: {error_msg}")
                
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу. Запустите backend.")
            self.status_var.set("Ошибка подключения")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.log_message(f"✗ Критическая ошибка: {str(e)}")
            
        finally:
            self.shorten_btn.config(state="normal")
            
    def copy_to_clipboard(self):
        """Копирование в буфер обмена"""
        url = self.result_entry.get()
        if url:
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.status_var.set("Ссылка скопирована в буфер!")
            self.log_message("📋 Ссылка скопирована в буфер обмена")
            
    def show_stats(self):
        """Показать статистику"""
        try:
            response = requests.get(f"{self.api_url}/api/stats")
            if response.status_code == 200:
                stats = response.json()
                messagebox.showinfo(
                    "Статистика",
                    f"Всего ссылок: {stats['total_urls']}\n"
                    f"Всего переходов: {stats['total_clicks']}\n"
                    f"Среднее число кликов: {stats['average_clicks']:.1f}"
                )
                self.log_message("📊 Просмотрена статистика сервиса")
            else:
                messagebox.showerror("Ошибка", "Не удалось получить статистику")
        except:
            messagebox.showerror("Ошибка", "Не удалось подключиться к серверу")

def main():
    root = tk.Tk()
    app = URLShortenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
