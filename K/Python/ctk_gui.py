import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent

os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(base_path / "playwright_browsers")

import customtkinter as ctk
import threading
import asyncio
from portal_scraper import portal_url, attendance_checker

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Portal Scraper")
        self.geometry("600x450")
        self.resizable(False, False)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.username = ctk.CTkEntry(self, placeholder_text="Username (Reg No)")
        self.username.pack(pady=10)
        
        self.password = ctk.CTkEntry(self, show="*", placeholder_text="Password")
        self.password.pack(pady=10)
        
        self.status = ctk.CTkLabel(self, text="Idle")
        self.status.pack(pady=10)
        
        self.start_btn = ctk.CTkButton(self, text="Start", command=self.on_start)
        self.start_btn.pack(pady=20)
        
        # Checkboxes
        self.check_lecture = ctk.BooleanVar(value=False)
        self.check_student = ctk.BooleanVar(value=False)
        self.check_result = ctk.BooleanVar(value=False)
        
        ctk.CTkLabel(self, text="Select what you want to check:").pack(pady=(10, 0))
        
        checkbox_frame = ctk.CTkFrame(self)
        checkbox_frame.pack(pady=10)
        
        ctk.CTkCheckBox(checkbox_frame, text="Lecture Attendance", variable=self.check_lecture).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkCheckBox(checkbox_frame, text="Chapel and Roll Call", variable=self.check_student).grid(row=0, column=1, padx=10)
        ctk.CTkCheckBox(checkbox_frame, text="Student Result", variable=self.check_result).grid(row=0, column=2, padx=10)
        
        self.disclaimer = ctk.CTkLabel(self, text="🔒 Your login credentials are used only during this session and are never stored.")
        self.disclaimer.pack(pady=50)
        
    def on_start(self):
        if self.start_btn.cget("state") == "disabled":
            return
        
        self.start_btn.configure(state="disabled")
        self.status.configure(text="Running...")
        
        username = self.username.get()
        password = self.password.get()
        self.password.delete(0, "end")
        
        #Build a list of selected modes
        selected_modes = []
        if self.check_lecture.get():
            selected_modes.append("1")
        if self.check_student.get():
            selected_modes.append("2")
        if self.check_result.get():
            selected_modes.append("3")
            
        if not username or not password:
            self.status.configure(text="Please enter your username and password.")
            self.start_btn.configure(state="normal")
            return
            
        if not selected_modes:
            self.status.configure(text="Please select at least one option.")
            self.start_btn.configure(state="normal")
            return
        
        # Start background thread
        threading.Thread(target=self.run_scraper_thread, args=(username, password, selected_modes), daemon=True).start()
    
    def update_status(self, message):
        self.after(0, lambda: self.status.configure(text=message))
        
    def run_scraper_thread(self, username, password, selected_modes):
        try:
            asyncio.run(attendance_checker(portal_url, username, password, selected_modes, status_callback=self.update_status))
            self.after(0, self.on_success)
            
        except ValueError as e:
            self.after(0, self.on_error, e)
            
        except Exception as e:
            self.after(0, self.on_error, e)
        
        finally:
            del password
                
    def on_success(self):
        self.status.configure(text="Done", text_color="green")
        self.start_btn.configure(state="normal")
            
    def on_error(self, error):
        self.status.configure(text=str(error), text_color="red")
        self.start_btn.configure(state="normal")

if __name__ == '__main__':
    app = App()
    app.mainloop()