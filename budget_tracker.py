import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import hashlib
import json
from collections import defaultdict
import threading
import time

class ModernBudgetTracker:
    def __init__(self):
        self.current_user = None
        self.setup_files()
        self.setup_login()
        
    def setup_files(self):
        """Initialize all necessary files and directories"""
        self.files = {
            'transactions': "transactions.csv",
            'categories': "categories.json",
            'users': "users.json",
            'budgets': "budgets.json",
            'savings': "savings.json",
            'settings': "settings.json"
        }
        
        # Create default data files
        self.create_default_files()
    
    def create_default_files(self):
        """Create default data files if they don't exist"""
        if not os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount', 'User', 'Notes'])
        
        if not os.path.exists(self.files['categories']):
            default_categories = {
                'expense': ['🍕 Food & Dining', '🚗 Transportation', '🎬 Entertainment', 
                           '💡 Bills & Utilities', '🛒 Shopping', '🏥 Healthcare', 
                           '🎓 Education', '🏠 Housing', '💼 Business', '🎁 Gifts & Donations'],
                'income': ['💰 Salary', '💼 Freelance', '📈 Investment', '🎁 Gift', '💰 Other Income']
            }
            with open(self.files['categories'], 'w') as f:
                json.dump(default_categories, f, indent=2)
        
        if not os.path.exists(self.files['users']):
            with open(self.files['users'], 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.files['budgets']):
            with open(self.files['budgets'], 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.files['savings']):
            with open(self.files['savings'], 'w') as f:
                json.dump({}, f)
                
        if not os.path.exists(self.files['settings']):
            default_settings = {
                'theme': 'dark',
                'currency': 'USD',
                'date_format': '%Y-%m-%d',
                'notifications': True
            }
            with open(self.files['settings'], 'w') as f:
                json.dump(default_settings, f, indent=2)
    
    def create_demo_account(self):
        """Create a demo account for testing"""
        try:
            users = self.load_json_file(self.files['users'])
            
            if 'demo' not in users:
                users['demo'] = self.hash_password('demo')
                self.save_json_file(self.files['users'], users)
                
                # Add some demo transactions
                self.create_demo_data()
                
        except Exception as e:
            print(f"Failed to create demo account: {e}")
    
    def create_demo_data(self):
        """Create sample data for demo account"""
        try:
            demo_transactions = [
                ['2024-01-15', 'income', '💰 Salary', 'Monthly salary', 3500, 'demo', 'Regular income'],
                ['2024-01-16', 'expense', '🍕 Food & Dining', 'Grocery shopping', 85.50, 'demo', 'Weekly groceries'],
                ['2024-01-17', 'expense', '🚗 Transportation', 'Gas fill-up', 45.00, 'demo', 'Car fuel'],
                ['2024-01-18', 'expense', '🎬 Entertainment', 'Movie tickets', 28.00, 'demo', 'Weekend movie'],
                ['2024-01-19', 'expense', '💡 Bills & Utilities', 'Electric bill', 120.00, 'demo', 'Monthly electricity'],
                ['2024-01-20', 'expense', '🛒 Shopping', 'New shoes', 75.00, 'demo', 'Footwear'],
                ['2024-01-21', 'income', '💼 Freelance', 'Web design project', 500.00, 'demo', 'Side project'],
                ['2024-01-22', 'expense', '🏥 Healthcare', 'Doctor visit', 150.00, 'demo', 'Health checkup'],
            ]
            
            # Write demo transactions
            with open(self.files['transactions'], 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount', 'User', 'Notes'])
                writer.writerows(demo_transactions)
            
            # Create demo budgets
            demo_budgets = {
                'demo': {
                    '🍕 Food & Dining': 400.0,
                    '🚗 Transportation': 200.0,
                    '🎬 Entertainment': 100.0,
                    '💡 Bills & Utilities': 300.0,
                    '🛒 Shopping': 150.0,
                    '🏥 Healthcare': 200.0
                }
            }
            self.save_json_file(self.files['budgets'], demo_budgets)
            
        except Exception as e:
            print(f"Failed to create demo data: {e}")
    
    def load_json_file(self, filename):
        """Load JSON file safely"""
        try:
            if not os.path.exists(filename):
                return {}
            with open(filename, 'r') as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError, Exception) as e:
            print(f"Error loading {filename}: {e}")
            return {}
    
    def save_json_file(self, filename, data):
        """Save JSON file safely"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            raise
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setup_login(self):
        """Setup login window with modern design"""
        self.login_window = tk.Tk()
        self.login_window.title("💰 Budget Tracker - Login")
        self.login_window.geometry("450x550")
        self.login_window.configure(bg="#1a1a2e")
        self.login_window.resizable(False, False)
        
        # Center the window
        self.center_window(self.login_window, 450, 550)
        
        self.create_login_ui()
        self.login_window.mainloop()
    
    def center_window(self, window, width, height):
        """Center window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_login_ui(self):
        """Create modern login interface"""
        # Header with gradient effect
        header_frame = tk.Frame(self.login_window, bg="#16213e", height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="💰 Budget Tracker",
                              font=("Segoe UI", 28, "bold"),
                              fg="#00d4aa",
                              bg="#16213e")
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Manage your finances with style",
                                 font=("Segoe UI", 12),
                                 fg="#a8a8a8",
                                 bg="#16213e")
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.login_window, bg="#1a1a2e")
        main_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Login Form
        self.create_login_form(main_frame)
        
        # Add demo account info and create demo account
        self.add_login_info(main_frame)
    
    def create_login_form(self, parent):
        """Create login form"""
        form_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        form_frame.pack(fill="x", pady=20)
        
        # Form title
        title_frame = tk.Frame(form_frame, bg="#00d4aa", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🔐 Account Access",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#00d4aa").pack(expand=True)
        
        # Form content
        content_frame = tk.Frame(form_frame, bg="#0f3460")
        content_frame.pack(fill="x", padx=30, pady=20)
        
        # Username
        tk.Label(content_frame, text="👤 Username:",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").pack(anchor="w", pady=(0, 5))
        
        self.login_username = tk.Entry(content_frame,
                                      font=("Segoe UI", 12),
                                      bg="#1a1a2e", fg="#ffffff",
                                      relief="solid", bd=1,
                                      insertbackground="#ffffff")
        self.login_username.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Password
        tk.Label(content_frame, text="🔒 Password:",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").pack(anchor="w", pady=(0, 5))
        
        self.login_password = tk.Entry(content_frame,
                                      font=("Segoe UI", 12),
                                      bg="#1a1a2e", fg="#ffffff",
                                      show="*", relief="solid", bd=1,
                                      insertbackground="#ffffff")
        self.login_password.pack(fill="x", pady=(0, 20), ipady=8)
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg="#0f3460")
        button_frame.pack(fill="x")
        
        login_btn = tk.Button(button_frame, text="🚀 Login",
                             font=("Segoe UI", 12, "bold"),
                             bg="#00d4aa", fg="#ffffff",
                             relief="flat", padx=20, pady=10,
                             cursor="hand2",
                             command=self.login)
        login_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        signup_btn = tk.Button(button_frame, text="📝 Create New Account",
                              font=("Segoe UI", 12, "bold"),
                              bg="#e74c3c", fg="#ffffff",
                              relief="flat", padx=20, pady=10,
                              cursor="hand2",
                              command=self.show_signup)
        signup_btn.pack(side="right", fill="x", expand=True)
        
        # Add hover effects
        self.add_button_hover(login_btn, "#00d4aa", "#00b894")
        self.add_button_hover(signup_btn, "#e74c3c", "#d63031")
    
    def add_login_info(self, parent):
        """Add login information and demo account setup"""
        # Bind Enter key
        self.login_username.bind("<Return>", lambda e: self.login_password.focus())
        self.login_password.bind("<Return>", lambda e: self.login())
        
        # Focus on username field
        self.login_username.focus()
        
        # Add demo account info
        info_frame = tk.Frame(parent, bg="#1a1a2e")
        info_frame.pack(fill="x", pady=(20, 0))
        
        info_label = tk.Label(info_frame,
                             text="💡 New User? Click 'Create New Account' button above!\n" +
                                  "💡 Testing? Use demo account: username 'demo', password 'demo'\n" +
                                  "💡 Existing User? Just login with your credentials",
                             font=("Segoe UI", 10),
                             fg="#a8a8a8", bg="#1a1a2e",
                             justify="center")
        info_label.pack()
        
        # Auto-create demo account if it doesn't exist
        self.create_demo_account()
    
    def add_button_hover(self, button, original_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.configure(bg=hover_color)
        
        def on_leave(e):
            button.configure(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def show_signup(self):
        """Show signup window"""
        signup_window = tk.Toplevel(self.login_window)
        signup_window.title("📝 Create Account")
        signup_window.geometry("450x400")
        signup_window.configure(bg="#1a1a2e")
        signup_window.resizable(False, False)
        signup_window.grab_set()  # Make modal
        
        # Center the signup window
        self.center_window(signup_window, 450, 400)
        
        # Header
        header_frame = tk.Frame(signup_window, bg="#e74c3c", height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📝 Create New Account",
                font=("Segoe UI", 18, "bold"),
                fg="#ffffff", bg="#e74c3c").pack(expand=True)
        
        # Form
        form_frame = tk.Frame(signup_window, bg="#1a1a2e")
        form_frame.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Username
        tk.Label(form_frame, text="👤 Username:",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#1a1a2e").pack(anchor="w", pady=(0, 8))
        
        username_entry = tk.Entry(form_frame,
                                 font=("Segoe UI", 12),
                                 bg="#0f3460", fg="#ffffff",
                                 relief="solid", bd=1,
                                 insertbackground="#ffffff")
        username_entry.pack(fill="x", pady=(0, 20), ipady=8)
        
        # Password
        tk.Label(form_frame, text="🔒 Password:",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#1a1a2e").pack(anchor="w", pady=(0, 8))
        
        password_entry = tk.Entry(form_frame,
                                 font=("Segoe UI", 12),
                                 bg="#0f3460", fg="#ffffff",
                                 show="*", relief="solid", bd=1,
                                 insertbackground="#ffffff")
        password_entry.pack(fill="x", pady=(0, 20), ipady=8)
        
        # Confirm Password
        tk.Label(form_frame, text="🔒 Confirm Password:",
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#1a1a2e").pack(anchor="w", pady=(0, 8))
        
        confirm_entry = tk.Entry(form_frame,
                                font=("Segoe UI", 12),
                                bg="#0f3460", fg="#ffffff",
                                show="*", relief="solid", bd=1,
                                insertbackground="#ffffff")
        confirm_entry.pack(fill="x", pady=(0, 25), ipady=8)
        
        def create_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            confirm = confirm_entry.get().strip()
            
            # Validation
            if not username or not password or not confirm:
                messagebox.showerror("❌ Error", "Please fill in all fields!")
                return
            
            if len(username) < 3:
                messagebox.showerror("❌ Error", "Username must be at least 3 characters long!")
                return
            
            if len(password) < 4:
                messagebox.showerror("❌ Error", "Password must be at least 4 characters long!")
                return
            
            if password != confirm:
                messagebox.showerror("❌ Error", "Passwords don't match!")
                return
            
            try:
                users = self.load_json_file(self.files['users'])
                
                if username.lower() in [u.lower() for u in users.keys()]:
                    messagebox.showerror("❌ Error", "Username already exists!")
                    return
                
                # Save new user
                users[username] = self.hash_password(password)
                self.save_json_file(self.files['users'], users)
                
                messagebox.showinfo("✅ Success", f"Account '{username}' created successfully!\n\nYou can now login with your new account.")
                signup_window.destroy()
                
                # Auto-fill login form
                self.login_username.delete(0, tk.END)
                self.login_username.insert(0, username)
                self.login_password.focus()
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to create account: {str(e)}")
        
        def on_enter_pressed(event):
            create_account()
        
        # Create button (bigger and more prominent)
        create_btn = tk.Button(form_frame, text="🎉 CREATE ACCOUNT",
                              font=("Segoe UI", 14, "bold"),
                              bg="#27ae60", fg="#ffffff",
                              relief="flat", padx=20, pady=15,
                              cursor="hand2",
                              command=create_account)
        create_btn.pack(fill="x", pady=(0, 15))
        
        # Cancel button
        cancel_btn = tk.Button(form_frame, text="❌ Cancel",
                              font=("Segoe UI", 11, "bold"),
                              bg="#95a5a6", fg="#ffffff",
                              relief="flat", padx=20, pady=8,
                              cursor="hand2",
                              command=signup_window.destroy)
        cancel_btn.pack(fill="x")
        
        self.add_button_hover(create_btn, "#27ae60", "#229954")
        self.add_button_hover(cancel_btn, "#95a5a6", "#7f8c8d")
        
        # Bind Enter key to all entry fields
        username_entry.bind("<Return>", lambda e: password_entry.focus())
        password_entry.bind("<Return>", lambda e: confirm_entry.focus())
        confirm_entry.bind("<Return>", on_enter_pressed)
        
        # Focus on first entry
        username_entry.focus()
    
    def login(self):
        """Handle user login"""
        username = self.login_username.get().strip()
        password = self.login_password.get().strip()
        
        # Validation
        if not username or not password:
            messagebox.showerror("❌ Error", "Please enter both username and password!")
            return
        
        try:
            users = self.load_json_file(self.files['users'])
            
            # Check if any users exist
            if not users:
                messagebox.showinfo("👋 Welcome!", "No accounts found. Please create an account first!")
                return
            
            # Find user (case-insensitive)
            found_user = None
            for existing_user in users:
                if existing_user.lower() == username.lower():
                    found_user = existing_user
                    break
            
            if found_user and users[found_user] == self.hash_password(password):
                self.current_user = found_user
                messagebox.showinfo("✅ Success", f"Welcome back, {found_user}!")
                
                # Close login window and start main app
                self.login_window.destroy()
                self.setup_main_application()
            else:
                messagebox.showerror("❌ Login Failed", "Invalid username or password!\n\nPlease check your credentials or create a new account.")
                # Clear password field
                self.login_password.delete(0, tk.END)
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Login failed: {str(e)}")
            print(f"Login error: {e}")  # Debug info
    
    def setup_main_application(self):
        """Setup main application window"""
        self.root = tk.Tk()
        self.root.title(f"💰 Budget Tracker - Welcome {self.current_user}")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")
        self.root.minsize(1000, 700)
        
        # Center the main window
        self.center_window(self.root, 1200, 800)
        
        # Load settings
        self.settings = self.load_json_file(self.files['settings'])
        
        # Setup main UI
        self.create_main_ui()
        
        # Initial data load
        self.refresh_dashboard()
        
        # Start auto-refresh timer
        self.start_auto_refresh()
        
        self.root.mainloop()
    
    def create_main_ui(self):
        """Create main application interface"""
        # Create main container
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True)
        
        # Create header
        self.create_header(main_container)
        
        # Create main content area with notebook
        self.create_main_content(main_container)
        
        # Create status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """Create application header"""
        header_frame = tk.Frame(parent, bg="#16213e", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Left side - Title and user info
        left_frame = tk.Frame(header_frame, bg="#16213e")
        left_frame.pack(side="left", fill="y", padx=20)
        
        title_label = tk.Label(left_frame,
                              text="💰 Budget Tracker Pro",
                              font=("Segoe UI", 20, "bold"),
                              fg="#00d4aa",
                              bg="#16213e")
        title_label.pack(anchor="w")
        
        user_label = tk.Label(left_frame,
                             text=f"Welcome back, {self.current_user}! 👋",
                             font=("Segoe UI", 11),
                             fg="#a8a8a8",
                             bg="#16213e")
        user_label.pack(anchor="w")
        
        # Right side - Quick actions
        right_frame = tk.Frame(header_frame, bg="#16213e")
        right_frame.pack(side="right", fill="y", padx=20)
        
        # Quick add button
        quick_add_btn = tk.Button(right_frame, text="⚡ Quick Add",
                                 font=("Segoe UI", 11, "bold"),
                                 bg="#00d4aa", fg="#ffffff",
                                 relief="flat", padx=15, pady=5,
                                 cursor="hand2",
                                 command=self.show_quick_add)
        quick_add_btn.pack(side="right", pady=15, padx=5)
        
        # Logout button
        logout_btn = tk.Button(right_frame, text="🚪 Logout",
                              font=("Segoe UI", 11, "bold"),
                              bg="#e74c3c", fg="#ffffff",
                              relief="flat", padx=15, pady=5,
                              cursor="hand2",
                              command=self.logout)
        logout_btn.pack(side="right", pady=15, padx=5)
        
        self.add_button_hover(quick_add_btn, "#00d4aa", "#00b894")
        self.add_button_hover(logout_btn, "#e74c3c", "#d63031")
    
    def create_main_content(self, parent):
        """Create main content area with tabs"""
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook style
        style.configure('Modern.TNotebook',
                       background="#1a1a2e",
                       borderwidth=0)
        style.configure('Modern.TNotebook.Tab',
                       background="#0f3460",
                       foreground="#ffffff",
                       padding=[20, 10],
                       borderwidth=0)
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#00d4aa')],
                 foreground=[('selected', '#ffffff')])
        
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_transactions_tab()
        self.create_budget_tab()
        self.create_reports_tab()
        self.create_settings_tab()
    
    def create_dashboard_tab(self):
        """Create dashboard tab"""
        dashboard_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(dashboard_frame, text="📊 Dashboard")
        
        # Create scrollable canvas
        canvas = tk.Canvas(dashboard_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a2e")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Dashboard content
        self.create_dashboard_content(scrollable_frame)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.dashboard_frame = scrollable_frame
    
    def create_dashboard_content(self, parent):
        """Create dashboard content"""
        # Balance overview section
        self.create_balance_overview(parent)
        
        # Quick stats section
        self.create_quick_stats(parent)
        
        # Recent transactions section
        self.create_recent_transactions(parent)
        
        # Budget progress section
        self.create_budget_progress(parent)
        
        # Expense chart section
        self.create_expense_chart(parent)
    
    def create_balance_overview(self, parent):
        """Create balance overview section"""
        balance_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        balance_frame.pack(fill="x", pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(balance_frame, bg="#00d4aa", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="💰 Financial Overview",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#00d4aa").pack(expand=True)
        
        # Content
        content_frame = tk.Frame(balance_frame, bg="#0f3460")
        content_frame.pack(fill="x", padx=30, pady=20)
        
        # Balance cards
        cards_frame = tk.Frame(content_frame, bg="#0f3460")
        cards_frame.pack(fill="x")
        
        self.income_card = self.create_balance_card(cards_frame, "💚 Income", "$0.00", "#27ae60", 0)
        self.expense_card = self.create_balance_card(cards_frame, "💸 Expenses", "$0.00", "#e74c3c", 1)
        self.balance_card = self.create_balance_card(cards_frame, "💰 Balance", "$0.00", "#3498db", 2)
        self.savings_card = self.create_balance_card(cards_frame, "🏦 Savings", "0%", "#9b59b6", 3)
    
    def create_balance_card(self, parent, title, value, color, col):
        """Create individual balance card"""
        card_frame = tk.Frame(parent, bg=color, width=250, height=100, relief="solid", bd=1)
        card_frame.grid(row=0, column=col, padx=10, pady=10)
        card_frame.pack_propagate(False)
        card_frame.grid_propagate(False)
        
        tk.Label(card_frame, text=title,
                font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg=color).pack(pady=(15, 5))
        
        value_label = tk.Label(card_frame, text=value,
                              font=("Segoe UI", 18, "bold"),
                              fg="#ffffff", bg=color)
        value_label.pack()
        
        return value_label
    
    def create_quick_stats(self, parent):
        """Create quick stats section"""
        stats_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        stats_frame.pack(fill="x", pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(stats_frame, bg="#e74c3c", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📈 Quick Statistics",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#e74c3c").pack(expand=True)
        
        # Stats content
        content_frame = tk.Frame(stats_frame, bg="#0f3460")
        content_frame.pack(fill="x", padx=30, pady=20)
        
        stats_grid = tk.Frame(content_frame, bg="#0f3460")
        stats_grid.pack(fill="x")
        
        # Create stat items
        self.total_transactions_label = self.create_stat_item(stats_grid, "📊 Total Transactions", "0", 0, 0)
        self.avg_expense_label = self.create_stat_item(stats_grid, "💸 Avg Expense", "$0.00", 0, 1)
        self.top_category_label = self.create_stat_item(stats_grid, "🎯 Top Category", "None", 1, 0)
        self.monthly_total_label = self.create_stat_item(stats_grid, "📅 This Month", "$0.00", 1, 1)
    
    def create_stat_item(self, parent, title, value, row, col):
        """Create individual stat item"""
        item_frame = tk.Frame(parent, bg="#1a1a2e", relief="solid", bd=1)
        item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        tk.Label(item_frame, text=title,
                font=("Segoe UI", 10, "bold"),
                fg="#a8a8a8", bg="#1a1a2e").pack(pady=(10, 5))
        
        value_label = tk.Label(item_frame, text=value,
                              font=("Segoe UI", 14, "bold"),
                              fg="#ffffff", bg="#1a1a2e")
        value_label.pack(pady=(0, 10))
        
        parent.grid_columnconfigure(col, weight=1)
        
        return value_label
    
    def create_recent_transactions(self, parent):
        """Create recent transactions section"""
        recent_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        recent_frame.pack(fill="x", pady=(0, 15))
        
        # Title with view all button
        title_frame = tk.Frame(recent_frame, bg="#3498db", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        left_title = tk.Frame(title_frame, bg="#3498db")
        left_title.pack(side="left", fill="y")
        
        tk.Label(left_title, text="📋 Recent Transactions",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#3498db").pack(expand=True, padx=20)
        
        view_all_btn = tk.Button(title_frame, text="View All →",
                               font=("Segoe UI", 10, "bold"),
                               bg="#2980b9", fg="#ffffff",
                               relief="flat", padx=15, pady=5,
                               cursor="hand2",
                               command=lambda: self.notebook.select(1))
        view_all_btn.pack(side="right", pady=10, padx=20)
        
        # Recent transactions list
        content_frame = tk.Frame(recent_frame, bg="#0f3460")
        content_frame.pack(fill="x", padx=20, pady=15)
        
        # Create treeview for recent transactions
        columns = ("Date", "Type", "Category", "Description", "Amount")
        self.recent_tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=6)
        
        # Configure columns
        for col in columns:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=150, anchor="center")
        
        self.recent_tree.pack(fill="x")
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Recent.Treeview",
                       background="#1a1a2e",
                       foreground="#ffffff",
                       rowheight=25,
                       fieldbackground="#1a1a2e")
        style.configure("Recent.Treeview.Heading",
                       background="#00d4aa",
                       foreground="#ffffff")
        
        self.recent_tree.configure(style="Recent.Treeview")
    
    def create_budget_progress(self, parent):
        """Create budget progress section"""
        budget_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        budget_frame.pack(fill="x", pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(budget_frame, bg="#9b59b6", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🎯 Budget Progress",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#9b59b6").pack(expand=True)
        
        # Budget content
        self.budget_content_frame = tk.Frame(budget_frame, bg="#0f3460")
        self.budget_content_frame.pack(fill="x", padx=20, pady=15)
    
    def create_expense_chart(self, parent):
        """Create expense chart section"""
        chart_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        chart_frame.pack(fill="x", pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(chart_frame, bg="#f39c12", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📊 Expense Chart",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#f39c12").pack(expand=True)
        
        # Chart content
        self.chart_frame = tk.Frame(chart_frame, bg="#0f3460")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=15)
    
    def create_transactions_tab(self):
        """Create transactions management tab"""
        trans_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(trans_frame, text="💳 Transactions")
        
        # Input section
        self.create_transaction_input(trans_frame)
        
        # Filters and search
        self.create_transaction_filters(trans_frame)
        
        # Transactions list
        self.create_transactions_list(trans_frame)
    
    def create_transaction_input(self, parent):
        """Create transaction input section"""
        input_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        input_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        # Title
        title_frame = tk.Frame(input_frame, bg="#00d4aa", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="➕ Add New Transaction",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#00d4aa").pack(expand=True)
        
        # Input fields
        fields_frame = tk.Frame(input_frame, bg="#0f3460")
        fields_frame.pack(fill="x", padx=30, pady=20)
        
        # First row
        row1 = tk.Frame(fields_frame, bg="#0f3460")
        row1.pack(fill="x", pady=(0, 15))
        
        # Transaction Type
        tk.Label(row1, text="💳 Type:", font=("Segoe UI", 11, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.trans_type_var = tk.StringVar(value="expense")
        type_frame = tk.Frame(row1, bg="#0f3460")
        type_frame.grid(row=0, column=1, sticky="ew", padx=(0, 20))
        
        expense_rb = tk.Radiobutton(type_frame, text="💸 Expense", variable=self.trans_type_var,
                                   value="expense", bg="#0f3460", fg="#ffffff",
                                   selectcolor="#e74c3c", font=("Segoe UI", 10))
        expense_rb.pack(side="left", padx=(0, 15))
        
        income_rb = tk.Radiobutton(type_frame, text="💰 Income", variable=self.trans_type_var,
                                  value="income", bg="#0f3460", fg="#ffffff",
                                  selectcolor="#27ae60", font=("Segoe UI", 10))
        income_rb.pack(side="left")
        
        # Amount
        tk.Label(row1, text="💵 Amount:", font=("Segoe UI", 11, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(0, 10))
        
        self.amount_entry = tk.Entry(row1, font=("Segoe UI", 11),
                                    bg="#1a1a2e", fg="#ffffff",
                                    relief="solid", bd=1, width=15,
                                    insertbackground="#ffffff")
        self.amount_entry.grid(row=0, column=3, sticky="ew", padx=(0, 20))
        
        # Second row
        row2 = tk.Frame(fields_frame, bg="#0f3460")
        row2.pack(fill="x", pady=(0, 15))
        
        # Category
        tk.Label(row2, text="📂 Category:", font=("Segoe UI", 11, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.category_combo = ttk.Combobox(row2, font=("Segoe UI", 11), width=18)
        self.category_combo.grid(row=0, column=1, sticky="ew", padx=(0, 20))
        
        # Description
        tk.Label(row2, text="📝 Description:", font=("Segoe UI", 11, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(0, 10))
        
        self.desc_entry = tk.Entry(row2, font=("Segoe UI", 11),
                                  bg="#1a1a2e", fg="#ffffff",
                                  relief="solid", bd=1, width=25,
                                  insertbackground="#ffffff")
        self.desc_entry.grid(row=0, column=3, sticky="ew")
        
        # Third row
        row3 = tk.Frame(fields_frame, bg="#0f3460")
        row3.pack(fill="x", pady=(0, 15))
        
        # Notes
        tk.Label(row3, text="📋 Notes:", font=("Segoe UI", 11, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10))
        
        self.notes_entry = tk.Entry(row3, font=("Segoe UI", 11),
                                   bg="#1a1a2e", fg="#ffffff",
                                   relief="solid", bd=1,
                                   insertbackground="#ffffff")
        self.notes_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=(0, 20))
        
        # Configure grid weights
        for i in range(4):
            row1.grid_columnconfigure(i, weight=1)
            row2.grid_columnconfigure(i, weight=1)
        row3.grid_columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = tk.Frame(fields_frame, bg="#0f3460")
        button_frame.pack(fill="x", pady=(10, 0))
        
        add_btn = tk.Button(button_frame, text="➕ Add Transaction",
                           font=("Segoe UI", 12, "bold"),
                           bg="#27ae60", fg="#ffffff",
                           relief="flat", padx=20, pady=8,
                           cursor="hand2",
                           command=self.add_transaction)
        add_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="🧹 Clear Fields",
                             font=("Segoe UI", 12, "bold"),
                             bg="#95a5a6", fg="#ffffff",
                             relief="flat", padx=20, pady=8,
                             cursor="hand2",
                             command=self.clear_transaction_fields)
        clear_btn.pack(side="left")
        
        self.add_button_hover(add_btn, "#27ae60", "#229954")
        self.add_button_hover(clear_btn, "#95a5a6", "#7f8c8d")
        
        # Update category combo when type changes
        self.trans_type_var.trace('w', self.update_categories)
        self.update_categories()
    
    def create_transaction_filters(self, parent):
        """Create transaction filters section"""
        filter_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        filter_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(filter_frame, bg="#3498db", height=40)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🔍 Search & Filter",
                font=("Segoe UI", 14, "bold"),
                fg="#ffffff", bg="#3498db").pack(expand=True)
        
        # Filter controls
        controls_frame = tk.Frame(filter_frame, bg="#0f3460")
        controls_frame.pack(fill="x", padx=20, pady=15)
        
        # Search
        tk.Label(controls_frame, text="🔍 Search:", font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.search_entry = tk.Entry(controls_frame, font=("Segoe UI", 10),
                                    bg="#1a1a2e", fg="#ffffff",
                                    relief="solid", bd=1, width=15,
                                    insertbackground="#ffffff")
        self.search_entry.grid(row=0, column=1, padx=5)
        
        # Type filter
        tk.Label(controls_frame, text="💳 Type:", font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(15, 5))
        
        self.filter_type_combo = ttk.Combobox(controls_frame, values=["All", "Income", "Expense"],
                                             font=("Segoe UI", 10), width=12)
        self.filter_type_combo.set("All")
        self.filter_type_combo.grid(row=0, column=3, padx=5)
        
        # Date range
        tk.Label(controls_frame, text="📅 From:", font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=4, sticky="w", padx=(15, 5))
        
        self.date_from_entry = tk.Entry(controls_frame, font=("Segoe UI", 10),
                                       bg="#1a1a2e", fg="#ffffff",
                                       relief="solid", bd=1, width=12,
                                       insertbackground="#ffffff")
        self.date_from_entry.grid(row=0, column=5, padx=5)
        self.date_from_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        tk.Label(controls_frame, text="📅 To:", font=("Segoe UI", 10, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=6, sticky="w", padx=(15, 5))
        
        self.date_to_entry = tk.Entry(controls_frame, font=("Segoe UI", 10),
                                     bg="#1a1a2e", fg="#ffffff",
                                     relief="solid", bd=1, width=12,
                                     insertbackground="#ffffff")
        self.date_to_entry.grid(row=0, column=7, padx=5)
        self.date_to_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Filter button
        filter_btn = tk.Button(controls_frame, text="🔍 Apply Filters",
                              font=("Segoe UI", 10, "bold"),
                              bg="#3498db", fg="#ffffff",
                              relief="flat", padx=15, pady=5,
                              cursor="hand2",
                              command=self.apply_filters)
        filter_btn.grid(row=0, column=8, padx=15)
        
        self.add_button_hover(filter_btn, "#3498db", "#2980b9")
    
    def create_transactions_list(self, parent):
        """Create transactions list"""
        list_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Title with export button
        title_frame = tk.Frame(list_frame, bg="#e74c3c", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        left_title = tk.Frame(title_frame, bg="#e74c3c")
        left_title.pack(side="left", fill="y")
        
        tk.Label(left_title, text="📋 All Transactions",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#e74c3c").pack(expand=True, padx=20)
        
        # Export buttons
        export_frame = tk.Frame(title_frame, bg="#e74c3c")
        export_frame.pack(side="right", pady=10, padx=20)
        
        export_csv_btn = tk.Button(export_frame, text="📤 CSV",
                                  font=("Segoe UI", 10, "bold"),
                                  bg="#d63031", fg="#ffffff",
                                  relief="flat", padx=10, pady=5,
                                  cursor="hand2",
                                  command=self.export_csv)
        export_csv_btn.pack(side="right", padx=5)
        
        export_pdf_btn = tk.Button(export_frame, text="📄 PDF",
                                  font=("Segoe UI", 10, "bold"),
                                  bg="#d63031", fg="#ffffff",
                                  relief="flat", padx=10, pady=5,
                                  cursor="hand2",
                                  command=self.export_pdf)
        export_pdf_btn.pack(side="right", padx=5)
        
        # Transactions treeview
        tree_container = tk.Frame(list_frame, bg="#0f3460")
        tree_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        columns = ("Date", "Type", "Category", "Description", "Amount", "Notes")
        self.transactions_tree = ttk.Treeview(tree_container, columns=columns, show="headings")
        
        # Configure columns
        column_configs = [
            ("Date", 100), ("Type", 80), ("Category", 150),
            ("Description", 200), ("Amount", 100), ("Notes", 200)
        ]
        
        for col, width in column_configs:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=width, anchor="center")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.transactions_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient="horizontal", command=self.transactions_tree.xview)
        
        self.transactions_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.transactions_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Transactions.Treeview",
                       background="#1a1a2e",
                       foreground="#ffffff",
                       rowheight=25,
                       fieldbackground="#1a1a2e")
        style.configure("Transactions.Treeview.Heading",
                       background="#00d4aa",
                       foreground="#ffffff")
        
        self.transactions_tree.configure(style="Transactions.Treeview")
        
        # Context menu
        self.create_context_menu()
        
        # Delete button
        delete_btn = tk.Button(tree_container, text="🗑️ Delete Selected",
                              font=("Segoe UI", 11, "bold"),
                              bg="#e74c3c", fg="#ffffff",
                              relief="flat", padx=15, pady=8,
                              cursor="hand2",
                              command=self.delete_transaction)
        delete_btn.grid(row=2, column=0, pady=10, sticky="w")
        
        self.add_button_hover(delete_btn, "#e74c3c", "#d63031")
    
    def create_context_menu(self):
        """Create context menu for transactions"""
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#0f3460", fg="#ffffff")
        self.context_menu.add_command(label="✏️ Edit Transaction", command=self.edit_transaction)
        self.context_menu.add_command(label="🗑️ Delete Transaction", command=self.delete_transaction)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📋 Copy Description", command=self.copy_description)
        
        def show_context_menu(event):
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
        
        self.transactions_tree.bind("<Button-3>", show_context_menu)
    
    def create_budget_tab(self):
        """Create budget management tab"""
        budget_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(budget_frame, text="🎯 Budget")
        
        # Budget input section
        self.create_budget_input(budget_frame)
        
        # Budget overview
        self.create_budget_overview(budget_frame)
    
    def create_budget_input(self, parent):
        """Create budget input section"""
        input_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        input_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        # Title
        title_frame = tk.Frame(input_frame, bg="#9b59b6", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🎯 Set Budget Limits",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#9b59b6").pack(expand=True)
        
        # Budget form
        form_frame = tk.Frame(input_frame, bg="#0f3460")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        # Category
        tk.Label(form_frame, text="📂 Category:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        
        self.budget_category_combo = ttk.Combobox(form_frame, font=("Segoe UI", 12), width=20)
        self.budget_category_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Budget amount
        tk.Label(form_frame, text="💰 Budget Amount:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=10)
        
        self.budget_amount_entry = tk.Entry(form_frame, font=("Segoe UI", 12),
                                           bg="#1a1a2e", fg="#ffffff",
                                           relief="solid", bd=1, width=15,
                                           insertbackground="#ffffff")
        self.budget_amount_entry.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="#0f3460")
        button_frame.grid(row=1, column=0, columnspan=4, pady=20, sticky="ew")
        
        set_btn = tk.Button(button_frame, text="🎯 Set Budget",
                           font=("Segoe UI", 12, "bold"),
                           bg="#9b59b6", fg="#ffffff",
                           relief="flat", padx=20, pady=8,
                           cursor="hand2",
                           command=self.set_budget)
        set_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="🧹 Clear All Budgets",
                             font=("Segoe UI", 12, "bold"),
                             bg="#e74c3c", fg="#ffffff",
                             relief="flat", padx=20, pady=8,
                             cursor="hand2",
                             command=self.clear_all_budgets)
        clear_btn.pack(side="left")
        
        self.add_button_hover(set_btn, "#9b59b6", "#8e44ad")
        self.add_button_hover(clear_btn, "#e74c3c", "#d63031")
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(3, weight=1)
        
        # Update budget categories
        self.update_budget_categories()
    
    def create_budget_overview(self, parent):
        """Create budget overview section"""
        overview_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        overview_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Title
        title_frame = tk.Frame(overview_frame, bg="#f39c12", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📊 Budget Overview",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#f39c12").pack(expand=True)
        
        # Budget list container
        self.budget_overview_frame = tk.Frame(overview_frame, bg="#0f3460")
        self.budget_overview_frame.pack(fill="both", expand=True, padx=20, pady=15)
    
    def create_reports_tab(self):
        """Create reports tab"""
        reports_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(reports_frame, text="📊 Reports")
        
        # Report controls
        self.create_report_controls(reports_frame)
        
        # Charts container
        self.create_charts_container(reports_frame)
    
    def create_report_controls(self, parent):
        """Create report controls"""
        controls_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        controls_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        # Title
        title_frame = tk.Frame(controls_frame, bg="#16a085", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📊 Generate Reports",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#16a085").pack(expand=True)
        
        # Controls
        form_frame = tk.Frame(controls_frame, bg="#0f3460")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        # Report type
        tk.Label(form_frame, text="📈 Report Type:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        
        self.report_type_combo = ttk.Combobox(form_frame, 
                                             values=["Monthly Summary", "Category Analysis", "Income vs Expenses", "Budget Performance"],
                                             font=("Segoe UI", 12), width=20)
        self.report_type_combo.set("Monthly Summary")
        self.report_type_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Generate button
        generate_btn = tk.Button(form_frame, text="📊 Generate Report",
                                font=("Segoe UI", 12, "bold"),
                                bg="#16a085", fg="#ffffff",
                                relief="flat", padx=20, pady=8,
                                cursor="hand2",
                                command=self.generate_report)
        generate_btn.grid(row=0, column=2, padx=20, pady=10)
        
        self.add_button_hover(generate_btn, "#16a085", "#138d75")
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def create_charts_container(self, parent):
        """Create charts container"""
        charts_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Title
        title_frame = tk.Frame(charts_frame, bg="#e67e22", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📈 Visual Analytics",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#e67e22").pack(expand=True)
        
        # Charts content
        self.charts_content_frame = tk.Frame(charts_frame, bg="#0f3460")
        self.charts_content_frame.pack(fill="both", expand=True, padx=20, pady=15)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # User settings
        self.create_user_settings(settings_frame)
        
        # Category management
        self.create_category_management(settings_frame)
        
        # Data management
        self.create_data_management(settings_frame)
    
    def create_user_settings(self, parent):
        """Create user settings section"""
        settings_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        settings_frame.pack(fill="x", padx=20, pady=(10, 15))
        
        # Title
        title_frame = tk.Frame(settings_frame, bg="#34495e", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="👤 User Settings",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#34495e").pack(expand=True)
        
        # Settings form
        form_frame = tk.Frame(settings_frame, bg="#0f3460")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        # Currency
        tk.Label(form_frame, text="💱 Currency:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        
        self.currency_combo = ttk.Combobox(form_frame,
                                          values=["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "INR"],
                                          font=("Segoe UI", 12), width=10)
        self.currency_combo.set(self.settings.get('currency', 'USD'))
        self.currency_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Theme
        tk.Label(form_frame, text="🎨 Theme:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=10)
        
        theme_btn = tk.Button(form_frame, text="🌙 Dark Theme",
                             font=("Segoe UI", 12, "bold"),
                             bg="#2c3e50", fg="#ffffff",
                             relief="flat", padx=15, pady=8,
                             cursor="hand2",
                             command=self.toggle_theme)
        theme_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Save settings button
        save_btn = tk.Button(form_frame, text="💾 Save Settings",
                            font=("Segoe UI", 12, "bold"),
                            bg="#27ae60", fg="#ffffff",
                            relief="flat", padx=20, pady=8,
                            cursor="hand2",
                            command=self.save_settings)
        save_btn.grid(row=1, column=0, columnspan=2, pady=20, sticky="w")
        
        self.add_button_hover(save_btn, "#27ae60", "#229954")
    
    def create_category_management(self, parent):
        """Create category management section"""
        cat_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        cat_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Title
        title_frame = tk.Frame(cat_frame, bg="#8e44ad", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="📂 Category Management",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#8e44ad").pack(expand=True)
        
        # Category form
        form_frame = tk.Frame(cat_frame, bg="#0f3460")
        form_frame.pack(fill="x", padx=30, pady=20)
        
        # Add category
        tk.Label(form_frame, text="➕ Add Category:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        
        self.new_category_entry = tk.Entry(form_frame, font=("Segoe UI", 12),
                                          bg="#1a1a2e", fg="#ffffff",
                                          relief="solid", bd=1, width=20,
                                          insertbackground="#ffffff")
        self.new_category_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Category type
        tk.Label(form_frame, text="💳 Type:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#0f3460").grid(row=0, column=2, sticky="w", padx=(20, 10), pady=10)
        
        self.new_cat_type_combo = ttk.Combobox(form_frame, values=["expense", "income"],
                                              font=("Segoe UI", 12), width=10)
        self.new_cat_type_combo.set("expense")
        self.new_cat_type_combo.grid(row=0, column=3, padx=10, pady=10)
        
        # Add button
        add_cat_btn = tk.Button(form_frame, text="➕ Add",
                               font=("Segoe UI", 12, "bold"),
                               bg="#8e44ad", fg="#ffffff",
                               relief="flat", padx=15, pady=8,
                               cursor="hand2",
                               command=self.add_category)
        add_cat_btn.grid(row=0, column=4, padx=20, pady=10)
        
        self.add_button_hover(add_cat_btn, "#8e44ad", "#7d3c98")
        
        form_frame.grid_columnconfigure(1, weight=1)
    
    def create_data_management(self, parent):
        """Create data management section"""
        data_frame = tk.Frame(parent, bg="#0f3460", relief="solid", bd=1)
        data_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Title
        title_frame = tk.Frame(data_frame, bg="#c0392b", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text="🗂️ Data Management",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#c0392b").pack(expand=True)
        
        # Data options
        options_frame = tk.Frame(data_frame, bg="#0f3460")
        options_frame.pack(fill="x", padx=30, pady=20)
        
        # Import/Export section
        import_export_frame = tk.Frame(options_frame, bg="#0f3460")
        import_export_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(import_export_frame, text="📤 Import/Export Data:",
                font=("Segoe UI", 14, "bold"),
                fg="#ffffff", bg="#0f3460").pack(anchor="w", pady=(0, 10))
        
        button_frame = tk.Frame(import_export_frame, bg="#0f3460")
        button_frame.pack(fill="x")
        
        import_btn = tk.Button(button_frame, text="📥 Import CSV",
                              font=("Segoe UI", 12, "bold"),
                              bg="#3498db", fg="#ffffff",
                              relief="flat", padx=20, pady=8,
                              cursor="hand2",
                              command=self.import_data)
        import_btn.pack(side="left", padx=(0, 10))
        
        export_btn = tk.Button(button_frame, text="📤 Export CSV",
                              font=("Segoe UI", 12, "bold"),
                              bg="#2980b9", fg="#ffffff",
                              relief="flat", padx=20, pady=8,
                              cursor="hand2",
                              command=self.export_csv)
        export_btn.pack(side="left", padx=(0, 10))
        
        backup_btn = tk.Button(button_frame, text="💾 Backup Data",
                              font=("Segoe UI", 12, "bold"),
                              bg="#27ae60", fg="#ffffff",
                              relief="flat", padx=20, pady=8,
                              cursor="hand2",
                              command=self.backup_data)
        backup_btn.pack(side="left")
        
        self.add_button_hover(import_btn, "#3498db", "#2980b9")
        self.add_button_hover(export_btn, "#2980b9", "#2471a3")
        self.add_button_hover(backup_btn, "#27ae60", "#229954")
        
        # Danger zone
        danger_frame = tk.Frame(options_frame, bg="#0f3460")
        danger_frame.pack(fill="x", pady=20)
        
        tk.Label(danger_frame, text="⚠️ Danger Zone:",
                font=("Segoe UI", 14, "bold"),
                fg="#e74c3c", bg="#0f3460").pack(anchor="w", pady=(0, 10))
        
        clear_btn = tk.Button(danger_frame, text="🗑️ Clear All Data",
                             font=("Segoe UI", 12, "bold"),
                             bg="#e74c3c", fg="#ffffff",
                             relief="flat", padx=20, pady=8,
                             cursor="hand2",
                             command=self.clear_all_data)
        clear_btn.pack(anchor="w")
        
        self.add_button_hover(clear_btn, "#e74c3c", "#d63031")
    
    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_bar = tk.Frame(parent, bg="#16213e", height=30)
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar,
                                    text="Ready",
                                    font=("Segoe UI", 10),
                                    fg="#a8a8a8", bg="#16213e")
        self.status_label.pack(side="left", padx=20, expand=True, fill="y")
        
        # Current time
        self.time_label = tk.Label(self.status_bar,
                                  text="",
                                  font=("Segoe UI", 10),
                                  fg="#a8a8a8", bg="#16213e")
        self.time_label.pack(side="right", padx=20, fill="y")
        
        self.update_time()
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def show_quick_add(self):
        """Show quick add transaction dialog"""
        quick_window = tk.Toplevel(self.root)
        quick_window.title("⚡ Quick Add Transaction")
        quick_window.geometry("400x300")
        quick_window.configure(bg="#1a1a2e")
        quick_window.resizable(False, False)
        
        # Center the window
        self.center_window(quick_window, 400, 300)
        
        # Header
        header_frame = tk.Frame(quick_window, bg="#00d4aa", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚡ Quick Add Transaction",
                font=("Segoe UI", 16, "bold"),
                fg="#ffffff", bg="#00d4aa").pack(expand=True)
        
        # Form
        form_frame = tk.Frame(quick_window, bg="#1a1a2e")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Amount
        tk.Label(form_frame, text="💵 Amount:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#1a1a2e").pack(anchor="w", pady=(0, 5))
        
        amount_entry = tk.Entry(form_frame, font=("Segoe UI", 12),
                               bg="#0f3460", fg="#ffffff",
                               relief="solid", bd=1,
                               insertbackground="#ffffff")
        amount_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Description
        tk.Label(form_frame, text="📝 Description:", font=("Segoe UI", 12, "bold"),
                fg="#ffffff", bg="#1a1a2e").pack(anchor="w", pady=(0, 5))
        
        desc_entry = tk.Entry(form_frame, font=("Segoe UI", 12),
                             bg="#0f3460", fg="#ffffff",
                             relief="solid", bd=1,
                             insertbackground="#ffffff")
        desc_entry.pack(fill="x", pady=(0, 15), ipady=8)
        
        # Type
        type_var = tk.StringVar(value="expense")
        type_frame = tk.Frame(form_frame, bg="#1a1a2e")
        type_frame.pack(fill="x", pady=(0, 15))
        
        tk.Radiobutton(type_frame, text="💸 Expense", variable=type_var,
                      value="expense", bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#e74c3c", font=("Segoe UI", 11)).pack(side="left", padx=(0, 20))
        
        tk.Radiobutton(type_frame, text="💰 Income", variable=type_var,
                      value="income", bg="#1a1a2e", fg="#ffffff",
                      selectcolor="#27ae60", font=("Segoe UI", 11)).pack(side="left")
        
        def quick_add():
            amount = amount_entry.get().strip()
            description = desc_entry.get().strip()
            trans_type = type_var.get()
            
            if not amount or not description:
                messagebox.showerror("❌ Error", "Please fill in all fields!")
                return
            
            try:
                amount_val = float(amount)
                # Add transaction with default category
                default_cat = "🛒 Shopping" if trans_type == "expense" else "💰 Other Income"
                
                with open(self.files['transactions'], 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        datetime.now().strftime('%Y-%m-%d'),
                        trans_type,
                        default_cat,
                        description,
                        amount_val,
                        self.current_user,
                        ""  # notes
                    ])
                
                messagebox.showinfo("✅ Success", "Transaction added successfully!")
                quick_window.destroy()
                self.refresh_dashboard()
                
            except ValueError:
                messagebox.showerror("❌ Error", "Please enter a valid amount!")
        
        # Add button
        add_btn = tk.Button(form_frame, text="➕ Add Transaction",
                           font=("Segoe UI", 12, "bold"),
                           bg="#27ae60", fg="#ffffff",
                           relief="flat", padx=20, pady=10,
                           cursor="hand2",
                           command=quick_add)
        add_btn.pack(pady=20)
        
        self.add_button_hover(add_btn, "#27ae60", "#229954")
        
        # Focus on amount entry
        amount_entry.focus()
    
    def logout(self):
        """Handle user logout"""
        if messagebox.askyesno("🚪 Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            self.__init__()  # Restart the application
    
    def update_categories(self, *args):
        """Update category dropdown based on transaction type"""
        categories = self.load_json_file(self.files['categories'])
        trans_type = self.trans_type_var.get()
        
        if trans_type in categories:
            self.category_combo['values'] = categories[trans_type]
            if categories[trans_type]:
                self.category_combo.set(categories[trans_type][0])
    
    def update_budget_categories(self):
        """Update budget category dropdown"""
        categories = self.load_json_file(self.files['categories'])
        expense_categories = categories.get('expense', [])
        self.budget_category_combo['values'] = expense_categories
        if expense_categories:
            self.budget_category_combo.set(expense_categories[0])
    
    def add_transaction(self):
        """Add new transaction"""
        trans_type = self.trans_type_var.get()
        category = self.category_combo.get()
        description = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        notes = self.notes_entry.get().strip()
        
        if not all([category, description, amount]):
            messagebox.showerror("❌ Error", "Please fill in all required fields!")
            return
        
        try:
            amount_val = float(amount)
            
            with open(self.files['transactions'], 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d'),
                    trans_type,
                    category,
                    description,
                    amount_val,
                    self.current_user,
                    notes
                ])
            
            messagebox.showinfo("✅ Success", "Transaction added successfully!")
            self.clear_transaction_fields()
            self.refresh_dashboard()
            self.update_status("Transaction added successfully")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid amount!")
    
    def clear_transaction_fields(self):
        """Clear transaction input fields"""
        self.category_combo.set("")
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
    
    def apply_filters(self):
        """Apply filters to transactions list"""
        self.load_transactions()
    
    def load_transactions(self):
        """Load transactions into the list"""
        # Clear existing data
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)
        
        if not os.path.exists(self.files['transactions']):
            return
        
        # Get filter values
        search_text = self.search_entry.get().lower()
        type_filter = self.filter_type_combo.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        
        try:
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                transactions = []
                for row in reader:
                    if len(row) < 6:
                        continue
                    
                    # Filter by user
                    if len(row) > 5 and row[5] != self.current_user:
                        continue
                    
                    # Apply filters
                    if search_text and search_text not in row[3].lower():
                        continue
                    
                    if type_filter != "All" and row[1].lower() != type_filter.lower():
                        continue
                    
                    # Date filtering
                    try:
                        trans_date = datetime.strptime(row[0], '%Y-%m-%d')
                        if date_from:
                            from_date = datetime.strptime(date_from, '%Y-%m-%d')
                            if trans_date < from_date:
                                continue
                        if date_to:
                            to_date = datetime.strptime(date_to, '%Y-%m-%d')
                            if trans_date > to_date:
                                continue
                    except ValueError:
                        continue
                    
                    transactions.append(row[:6])  # Include notes if available
                
                # Sort by date (newest first)
                transactions.sort(key=lambda x: x[0], reverse=True)
                
                # Insert into treeview
                for i, transaction in enumerate(transactions):
                    # Ensure we have all columns
                    while len(transaction) < 6:
                        transaction.append("")
                    
                    tag = 'income' if transaction[1].lower() == 'income' else 'expense'
                    self.transactions_tree.insert("", "end", values=transaction, tags=(tag,))
                
                # Configure row colors
                self.transactions_tree.tag_configure('income', background='#d5f4e6')
                self.transactions_tree.tag_configure('expense', background='#ffeaa7')
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to load transactions: {str(e)}")
    
    def delete_transaction(self):
        """Delete selected transaction"""
        selected_items = self.transactions_tree.selection()
        if not selected_items:
            messagebox.showwarning("⚠️ Warning", "Please select a transaction to delete!")
            return
        
        if messagebox.askyesno("🗑️ Confirm Delete", "Are you sure you want to delete this transaction?"):
            selected_values = self.transactions_tree.item(selected_items[0])['values']
            
            # Remove from CSV file
            transactions = []
            if os.path.exists(self.files['transactions']):
                with open(self.files['transactions'], 'r') as f:
                    reader = csv.reader(f)
                    header = next(reader)
                    for row in reader:
                        if len(row) >= 5 and not (
                            row[0] == selected_values[0] and
                            row[1] == selected_values[1] and
                            row[2] == selected_values[2] and
                            row[3] == selected_values[3] and
                            float(row[4]) == float(selected_values[4])
                        ):
                            transactions.append(row)
                
                with open(self.files['transactions'], 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(transactions)
            
            messagebox.showinfo("✅ Success", "Transaction deleted successfully!")
            self.load_transactions()
            self.refresh_dashboard()
            self.update_status("Transaction deleted")
    
    def edit_transaction(self):
        """Edit selected transaction"""
        selected_items = self.transactions_tree.selection()
        if not selected_items:
            messagebox.showwarning("⚠️ Warning", "Please select a transaction to edit!")
            return
        
        # Implementation for edit transaction dialog
        messagebox.showinfo("🚧 Coming Soon", "Edit functionality will be available in the next update!")
    
    def copy_description(self):
        """Copy transaction description to clipboard"""
        selected_items = self.transactions_tree.selection()
        if not selected_items:
            messagebox.showwarning("⚠️ Warning", "Please select a transaction!")
            return
        
        description = self.transactions_tree.item(selected_items[0])['values'][3]
        self.root.clipboard_clear()
        self.root.clipboard_append(description)
        self.update_status("Description copied to clipboard")
    
    def set_budget(self):
        """Set budget for a category"""
        category = self.budget_category_combo.get()
        amount = self.budget_amount_entry.get().strip()
        
        if not category or not amount:
            messagebox.showerror("❌ Error", "Please select a category and enter an amount!")
            return
        
        try:
            amount_val = float(amount)
            
            budgets = self.load_json_file(self.files['budgets'])
            user_budgets = budgets.get(self.current_user, {})
            user_budgets[category] = amount_val
            budgets[self.current_user] = user_budgets
            
            self.save_json_file(self.files['budgets'], budgets)
            
            messagebox.showinfo("✅ Success", f"Budget set for {category}: ${amount_val:.2f}")
            self.budget_amount_entry.delete(0, tk.END)
            self.refresh_dashboard()
            self.update_status(f"Budget set for {category}")
            
        except ValueError:
            messagebox.showerror("❌ Error", "Please enter a valid amount!")
    
    def clear_all_budgets(self):
        """Clear all budgets for current user"""
        if messagebox.askyesno("🗑️ Clear Budgets", "Are you sure you want to clear all budgets?"):
            budgets = self.load_json_file(self.files['budgets'])
            if self.current_user in budgets:
                del budgets[self.current_user]
                self.save_json_file(self.files['budgets'], budgets)
            
            messagebox.showinfo("✅ Success", "All budgets cleared!")
            self.refresh_dashboard()
            self.update_status("All budgets cleared")
    
    def add_category(self):
        """Add new category"""
        category_name = self.new_category_entry.get().strip()
        category_type = self.new_cat_type_combo.get()
        
        if not category_name:
            messagebox.showerror("❌ Error", "Please enter a category name!")
            return
        
        categories = self.load_json_file(self.files['categories'])
        
        if category_type not in categories:
            categories[category_type] = []
        
        if category_name not in categories[category_type]:
            categories[category_type].append(category_name)
            self.save_json_file(self.files['categories'], categories)
            
            messagebox.showinfo("✅ Success", f"Category '{category_name}' added!")
            self.new_category_entry.delete(0, tk.END)
            self.update_categories()
            self.update_budget_categories()
            self.update_status(f"Category '{category_name}' added")
        else:
            messagebox.showwarning("⚠️ Warning", "Category already exists!")
    
    def export_csv(self):
        """Export transactions to CSV"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Transactions"
        )
        
        if filename:
            try:
                transactions = []
                if os.path.exists(self.files['transactions']):
                    with open(self.files['transactions'], 'r') as f:
                        reader = csv.reader(f)
                        header = next(reader)
                        for row in reader:
                            if len(row) > 5 and row[5] == self.current_user:
                                transactions.append(row[:6])  # Export user's transactions only
                
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Date', 'Type', 'Category', 'Description', 'Amount', 'Notes'])
                    writer.writerows(transactions)
                
                messagebox.showinfo("✅ Success", f"Transactions exported to {filename}")
                self.update_status("Transactions exported successfully")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to export: {str(e)}")
    
    def export_pdf(self):
        """Export transactions to PDF"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Export Transactions Report"
        )
        
        if filename:
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.pdfgen import canvas
                from reportlab.lib.units import inch
                
                c = canvas.Canvas(filename, pagesize=letter)
                width, height = letter
                
                # Title
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, f"Transaction Report - {self.current_user}")
                c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                
                # Table headers
                y = height - 120
                c.setFont("Helvetica-Bold", 10)
                headers = ["Date", "Type", "Category", "Description", "Amount"]
                x_positions = [50, 120, 180, 280, 450]
                
                for i, header in enumerate(headers):
                    c.drawString(x_positions[i], y, header)
                
                # Draw line
                y -= 15
                c.line(50, y, 550, y)
                y -= 10
                
                # Transaction data
                c.setFont("Helvetica", 9)
                if os.path.exists(self.files['transactions']):
                    with open(self.files['transactions'], 'r') as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip header
                        
                        for row in reader:
                            if len(row) > 5 and row[5] == self.current_user:
                                if y < 50:  # New page
                                    c.showPage()
                                    y = height - 50
                                
                                for i, value in enumerate(row[:5]):
                                    if i == 4:  # Amount column
                                        c.drawString(x_positions[i], y, f"${float(value):.2f}")
                                    else:
                                        # Truncate long text
                                        text = str(value)[:20] + "..." if len(str(value)) > 20 else str(value)
                                        c.drawString(x_positions[i], y, text)
                                y -= 15
                
                c.save()
                messagebox.showinfo("✅ Success", f"PDF report saved to {filename}")
                self.update_status("PDF report generated successfully")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to generate PDF: {str(e)}")
    
    def import_data(self):
        """Import data from CSV"""
        filename = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Import Transaction Data"
        )
        
        if filename:
            try:
                imported_count = 0
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)  # Skip header
                    
                    with open(self.files['transactions'], 'a', newline='') as output_file:
                        writer = csv.writer(output_file)
                        
                        for row in reader:
                            if len(row) >= 5:
                                # Add user and ensure proper format
                                new_row = [
                                    row[0],  # Date
                                    row[1],  # Type
                                    row[2],  # Category
                                    row[3],  # Description
                                    row[4],  # Amount
                                    self.current_user,  # User
                                    row[5] if len(row) > 5 else ""  # Notes
                                ]
                                writer.writerow(new_row)
                                imported_count += 1
                
                messagebox.showinfo("✅ Success", f"Imported {imported_count} transactions successfully!")
                self.refresh_dashboard()
                self.update_status(f"Imported {imported_count} transactions")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to import data: {str(e)}")
    
    def backup_data(self):
        """Create backup of all data"""
        backup_dir = filedialog.askdirectory(title="Select Backup Location")
        
        if backup_dir:
            try:
                import shutil
                backup_name = f"budget_tracker_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_name)
                os.makedirs(backup_path)
                
                # Copy all data files
                for file_key, filename in self.files.items():
                    if os.path.exists(filename):
                        shutil.copy2(filename, backup_path)
                
                messagebox.showinfo("✅ Success", f"Backup created successfully at:\n{backup_path}")
                self.update_status("Data backup created successfully")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to create backup: {str(e)}")
    
    def clear_all_data(self):
        """Clear all user data"""
        warning_msg = """⚠️ WARNING: This will permanently delete ALL your data including:
        
• All transactions
• Budget settings
• Categories (custom ones)
• All user accounts

This action cannot be undone!

Are you absolutely sure you want to continue?"""
        
        if messagebox.askyesno("⚠️ DANGER: Clear All Data", warning_msg):
            if messagebox.askyesno("⚠️ Final Confirmation", "Last chance! This will delete EVERYTHING. Continue?"):
                try:
                    # Remove all data files
                    for filename in self.files.values():
                        if os.path.exists(filename):
                            os.remove(filename)
                    
                    # Recreate default files
                    self.create_default_files()
                    
                    messagebox.showinfo("✅ Success", "All data has been cleared. Please restart the application.")
                    self.root.destroy()
                    
                except Exception as e:
                    messagebox.showerror("❌ Error", f"Failed to clear data: {str(e)}")
    
    def save_settings(self):
        """Save user settings"""
        self.settings['currency'] = self.currency_combo.get()
        self.save_json_file(self.files['settings'], self.settings)
        
        messagebox.showinfo("✅ Success", "Settings saved successfully!")
        self.update_status("Settings saved")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        # This is a placeholder - in a full implementation, you'd switch CSS/colors
        messagebox.showinfo("🎨 Theme", "Theme toggle feature coming soon!")
    
    def generate_report(self):
        """Generate selected report"""
        report_type = self.report_type_combo.get()
        
        # Clear previous charts
        for widget in self.charts_content_frame.winfo_children():
            widget.destroy()
        
        try:
            if report_type == "Monthly Summary":
                self.create_monthly_summary_chart()
            elif report_type == "Category Analysis":
                self.create_category_analysis_chart()
            elif report_type == "Income vs Expenses":
                self.create_income_expense_chart()
            elif report_type == "Budget Performance":
                self.create_budget_performance_chart()
            
            self.update_status(f"{report_type} report generated")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to generate report: {str(e)}")
    
    def create_monthly_summary_chart(self):
        """Create monthly summary chart"""
        # Get monthly data
        monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user:
                        try:
                            date = datetime.strptime(row[0], '%Y-%m-%d')
                            month_key = date.strftime('%Y-%m')
                            amount = float(row[4])
                            
                            if row[1].lower() == 'income':
                                monthly_data[month_key]['income'] += amount
                            else:
                                monthly_data[month_key]['expense'] += amount
                        except (ValueError, IndexError):
                            continue
        
        if not monthly_data:
            tk.Label(self.charts_content_frame,
                    text="📊 No data available for monthly summary",
                    font=("Segoe UI", 14),
                    fg="#ffffff", bg="#0f3460").pack(expand=True)
            return
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('#0f3460')
        ax.set_facecolor('#0f3460')
        
        months = sorted(monthly_data.keys())
        incomes = [monthly_data[month]['income'] for month in months]
        expenses = [monthly_data[month]['expense'] for month in months]
        
        x = range(len(months))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], incomes, width, label='Income', color='#27ae60', alpha=0.8)
        bars2 = ax.bar([i + width/2 for i in x], expenses, width, label='Expenses', color='#e74c3c', alpha=0.8)
        
        ax.set_xlabel('Month', color='#ffffff')
        ax.set_ylabel('Amount ($)', color='#ffffff')
        ax.set_title('Monthly Income vs Expenses', color='#ffffff', fontsize=16, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45, color='#ffffff')
        ax.tick_params(colors='#ffffff')
        ax.legend()
        
        # Add value labels on bars
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'${height:.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           color='#ffffff', fontsize=9)
        
        autolabel(bars1)
        autolabel(bars2)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_category_analysis_chart(self):
        """Create category analysis pie chart"""
        category_data = defaultdict(float)
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user and row[1].lower() == 'expense':
                        try:
                            category_data[row[2]] += float(row[4])
                        except (ValueError, IndexError):
                            continue
        
        if not category_data:
            tk.Label(self.charts_content_frame,
                    text="📊 No expense data available for category analysis",
                    font=("Segoe UI", 14),
                    fg="#ffffff", bg="#0f3460").pack(expand=True)
            return
        
        # Create pie chart
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('#0f3460')
        
        categories = list(category_data.keys())
        amounts = list(category_data.values())
        
        # Create pie chart with custom colors
        colors = plt.cm.Set3(range(len(categories)))
        wedges, texts, autotexts = ax.pie(amounts, labels=categories, autopct='%1.1f%%',
                                         startangle=90, colors=colors)
        
        # Customize text
        for text in texts:
            text.set_color('#ffffff')
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('#ffffff')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')
        
        ax.set_title('Expenses by Category', color='#ffffff', fontsize=16, pad=20)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_income_expense_chart(self):
        """Create income vs expense trend chart"""
        daily_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user:
                        try:
                            date_key = row[0]
                            amount = float(row[4])
                            
                            if row[1].lower() == 'income':
                                daily_data[date_key]['income'] += amount
                            else:
                                daily_data[date_key]['expense'] += amount
                        except (ValueError, IndexError):
                            continue
        
        if not daily_data:
            tk.Label(self.charts_content_frame,
                    text="📊 No data available for income vs expense analysis",
                    font=("Segoe UI", 14),
                    fg="#ffffff", bg="#0f3460").pack(expand=True)
            return
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#0f3460')
        ax.set_facecolor('#0f3460')
        
        dates = sorted(daily_data.keys())
        incomes = [daily_data[date]['income'] for date in dates]
        expenses = [daily_data[date]['expense'] for date in dates]
        
        # Convert dates for better plotting
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        
        ax.plot(date_objects, incomes, marker='o', linewidth=2, label='Income', color='#27ae60')
        ax.plot(date_objects, expenses, marker='o', linewidth=2, label='Expenses', color='#e74c3c')
        
        ax.set_xlabel('Date', color='#ffffff')
        ax.set_ylabel('Amount ($)', color='#ffffff')
        ax.set_title('Income vs Expenses Trend', color='#ffffff', fontsize=16, pad=20)
        ax.tick_params(colors='#ffffff')
        ax.legend()
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Add grid
        ax.grid(True, alpha=0.3, color='#ffffff')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_budget_performance_chart(self):
        """Create budget performance chart"""
        budgets = self.load_json_file(self.files['budgets']).get(self.current_user, {})
        
        if not budgets:
            tk.Label(self.charts_content_frame,
                    text="📊 No budgets set. Please set budgets first.",
                    font=("Segoe UI", 14),
                    fg="#ffffff", bg="#0f3460").pack(expand=True)
            return
        
        # Calculate actual spending
        actual_spending = defaultdict(float)
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user and row[1].lower() == 'expense':
                        try:
                            actual_spending[row[2]] += float(row[4])
                        except (ValueError, IndexError):
                            continue
        
        # Create budget performance chart
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#0f3460')
        ax.set_facecolor('#0f3460')
        
        categories = []
        budget_amounts = []
        actual_amounts = []
        
        for category, budget_amount in budgets.items():
            categories.append(category)
            budget_amounts.append(budget_amount)
            actual_amounts.append(actual_spending.get(category, 0))
        
        x = range(len(categories))
        width = 0.35
        
        bars1 = ax.bar([i - width/2 for i in x], budget_amounts, width, 
                      label='Budget', color='#3498db', alpha=0.8)
        bars2 = ax.bar([i + width/2 for i in x], actual_amounts, width, 
                      label='Actual', color='#e74c3c', alpha=0.8)
        
        ax.set_xlabel('Categories', color='#ffffff')
        ax.set_ylabel('Amount ($)', color='#ffffff')
        ax.set_title('Budget vs Actual Spending', color='#ffffff', fontsize=16, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right', color='#ffffff')
        ax.tick_params(colors='#ffffff')
        ax.legend()
        
        # Add value labels
        def autolabel(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'${height:.0f}',
                           xy=(bar.get_x() + bar.get_width() / 2, height),
                           xytext=(0, 3),
                           textcoords="offset points",
                           ha='center', va='bottom',
                           color='#ffffff', fontsize=9)
        
        autolabel(bars1)
        autolabel(bars2)
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, self.charts_content_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def refresh_dashboard(self):
        """Refresh all dashboard data"""
        self.update_balance_cards()
        self.update_quick_stats()
        self.update_recent_transactions()
        self.update_budget_progress()
        self.load_transactions()
    
    def update_balance_cards(self):
        """Update balance overview cards"""
        income_total = 0
        expense_total = 0
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user:
                        try:
                            amount = float(row[4])
                            if row[1].lower() == 'income':
                                income_total += amount
                            else:
                                expense_total += amount
                        except (ValueError, IndexError):
                            continue
        
        balance = income_total - expense_total
        
        # Update cards
        self.income_card.config(text=f"${income_total:.2f}")
        self.expense_card.config(text=f"${expense_total:.2f}")
        self.balance_card.config(text=f"${balance:.2f}")
        
        # Update balance card color based on positive/negative
        if balance >= 0:
            self.balance_card.master.config(bg="#27ae60")
        else:
            self.balance_card.master.config(bg="#e74c3c")
        
        # Calculate savings progress (placeholder)
        savings_goal = 1000  # This should come from settings
        savings_progress = min((balance / savings_goal) * 100, 100) if savings_goal > 0 else 0
        self.savings_card.config(text=f"{savings_progress:.1f}%")
    
    def update_quick_stats(self):
        """Update quick statistics"""
        if not os.path.exists(self.files['transactions']):
            return
        
        total_transactions = 0
        total_expense = 0
        expense_count = 0
        category_totals = defaultdict(float)
        current_month = datetime.now().strftime('%Y-%m')
        monthly_total = 0
        
        with open(self.files['transactions'], 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            for row in reader:
                if len(row) > 5 and row[5] == self.current_user:
                    total_transactions += 1
                    try:
                        amount = float(row[4])
                        
                        # Check if this month
                        if row[0].startswith(current_month):
                            if row[1].lower() == 'expense':
                                monthly_total += amount
                        
                        if row[1].lower() == 'expense':
                            total_expense += amount
                            expense_count += 1
                            category_totals[row[2]] += amount
                            
                    except (ValueError, IndexError):
                        continue
        
        # Update labels
        self.total_transactions_label.config(text=str(total_transactions))
        
        avg_expense = total_expense / expense_count if expense_count > 0 else 0
        self.avg_expense_label.config(text=f"${avg_expense:.2f}")
        
        top_category = max(category_totals, key=category_totals.get) if category_totals else "None"
        self.top_category_label.config(text=top_category)
        
        self.monthly_total_label.config(text=f"${monthly_total:.2f}")
    
    def update_recent_transactions(self):
        """Update recent transactions list"""
        # Clear existing items
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        
        if not os.path.exists(self.files['transactions']):
            return
        
        # Get recent transactions (last 10)
        transactions = []
        with open(self.files['transactions'], 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            
            for row in reader:
                if len(row) > 5 and row[5] == self.current_user:
                    transactions.append(row)
        
        # Sort by date and get latest
        transactions.sort(key=lambda x: x[0], reverse=True)
        recent_transactions = transactions[:10]
        
        # Insert into treeview
        for transaction in recent_transactions:
            tag = 'income' if transaction[1].lower() == 'income' else 'expense'
            display_values = transaction[:5]  # Show first 5 columns
            self.recent_tree.insert("", "end", values=display_values, tags=(tag,))
        
        # Configure colors
        self.recent_tree.tag_configure('income', background='#d5f4e6')
        self.recent_tree.tag_configure('expense', background='#ffeaa7')
    
    def update_budget_progress(self):
        """Update budget progress section"""
        # Clear existing budget displays
        for widget in self.budget_content_frame.winfo_children():
            widget.destroy()
        
        budgets = self.load_json_file(self.files['budgets']).get(self.current_user, {})
        
        if not budgets:
            tk.Label(self.budget_content_frame,
                    text="📝 No budgets set. Go to Budget tab to set limits.",
                    font=("Segoe UI", 12),
                    fg="#a8a8a8", bg="#0f3460").pack(pady=20)
            return
        
        # Calculate actual spending for each budget category
        actual_spending = defaultdict(float)
        
        if os.path.exists(self.files['transactions']):
            with open(self.files['transactions'], 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                
                for row in reader:
                    if len(row) > 5 and row[5] == self.current_user and row[1].lower() == 'expense':
                        try:
                            actual_spending[row[2]] += float(row[4])
                        except (ValueError, IndexError):
                            continue
        
        # Create progress bars for each budget
        for i, (category, budget_amount) in enumerate(budgets.items()):
            spent = actual_spending.get(category, 0)
            percentage = min((spent / budget_amount) * 100, 100) if budget_amount > 0 else 0
            
            # Budget item frame
            item_frame = tk.Frame(self.budget_content_frame, bg="#1a1a2e", relief="solid", bd=1)
            item_frame.pack(fill="x", pady=5, padx=10)
            
            # Category info
            info_frame = tk.Frame(item_frame, bg="#1a1a2e")
            info_frame.pack(fill="x", padx=15, pady=10)
            
            # Category name and amounts
            tk.Label(info_frame, text=category,
                    font=("Segoe UI", 12, "bold"),
                    fg="#ffffff", bg="#1a1a2e").pack(side="left")
            
            tk.Label(info_frame, text=f"${spent:.2f} / ${budget_amount:.2f}",
                    font=("Segoe UI", 11),
                    fg="#a8a8a8", bg="#1a1a2e").pack(side="right")
            
            # Progress bar
            progress_frame = tk.Frame(item_frame, bg="#1a1a2e")
            progress_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            # Progress bar background
            progress_bg = tk.Frame(progress_frame, bg="#34495e", height=20)
            progress_bg.pack(fill="x")
            
            # Progress bar fill
            fill_width = int((percentage / 100) * 300)  # Assuming 300px width
            color = "#e74c3c" if percentage > 100 else "#f39c12" if percentage > 80 else "#27ae60"
            
            if fill_width > 0:
                progress_fill = tk.Frame(progress_bg, bg=color, height=20, width=fill_width)
                progress_fill.pack(side="left", fill="y")
            
            # Percentage label
            tk.Label(progress_frame, text=f"{percentage:.1f}%",
                    font=("Segoe UI", 10, "bold"),
                    fg="#ffffff", bg="#1a1a2e").pack(pady=(5, 0))
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        # Clear status after 5 seconds
        self.root.after(5000, lambda: self.status_label.config(text="Ready"))
    
    def start_auto_refresh(self):
        """Start auto-refresh timer for dashboard"""
        def auto_refresh():
            self.refresh_dashboard()
            # Refresh every 30 seconds
            self.root.after(30000, auto_refresh)
        
        # Start the auto-refresh cycle
        self.root.after(30000, auto_refresh)

# Start the application
if __name__ == "__main__":
    try:
        app = ModernBudgetTracker()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Application Error", f"Failed to start Budget Tracker:\n{str(e)}")
