import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
from database import Database
from datetime import datetime
import os
import shutil
from PIL import Image, ImageTk

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")
        self.root.geometry("800x600")
        
        self.db = Database()
        self.current_user = None
        self.selected_user = None
        self.selected_group = None
        self.chat_mode = 'direct'  # 'direct' or 'group'
        
        # Create images directory if it doesn't exist
        self.images_dir = 'chat_images'
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        
        # Create login screen
        self.create_login_screen()
    
    def create_login_screen(self):
        """Create login interface"""
        self.clear_screen()
        
        # Login frame
        login_frame = tk.Frame(self.root, bg='#2c3e50', padx=50, pady=50)
        login_frame.pack(expand=True, fill='both')
        
        # Title
        tk.Label(login_frame, text="💬 Chat App Login", font=('Arial', 24, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=20)
        
        # Username
        tk.Label(login_frame, text="Username:", font=('Arial', 12), 
                bg='#2c3e50', fg='white').pack(pady=5)
        self.username_entry = tk.Entry(login_frame, font=('Arial', 12), width=30)
        self.username_entry.pack(pady=5)
        
        # Password
        tk.Label(login_frame, text="Password:", font=('Arial', 12), 
                bg='#2c3e50', fg='white').pack(pady=5)
        self.password_entry = tk.Entry(login_frame, font=('Arial', 12), 
                                      width=30, show='*')
        self.password_entry.pack(pady=5)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        tk.Button(login_frame, text="Login", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white', command=self.login, 
                 width=20, cursor='hand2').pack(pady=20)
        
        # Register button
        tk.Button(login_frame, text="Create Account", font=('Arial', 11),
                 bg='#2ecc71', fg='white', command=self.show_register_dialog, 
                 width=20, cursor='hand2').pack(pady=10)
        
        # Info label
        tk.Label(login_frame, text="Test users: alice/password123, bob/password123, charlie/password123", 
                font=('Arial', 10), bg='#2c3e50', fg='#95a5a6').pack(pady=10)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return
        
        user = self.db.login_user(username, password)
        
        if user:
            self.current_user = user
            self.create_chat_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_register_dialog(self):
        """Show registration dialog"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Create Account")
        register_window.geometry("500x650")
        register_window.configure(bg='#ecf0f1')
        register_window.transient(self.root)
        register_window.grab_set()
        
        # Title
        tk.Label(register_window, text="✨ Create Your Account", font=('Arial', 20, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        # Form frame
        form = tk.Frame(register_window, bg='#ecf0f1')
        form.pack(padx=40, pady=20, fill='both', expand=True)
        
        # Username
        tk.Label(form, text="Username:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        username_entry = tk.Entry(form, font=('Arial', 11), width=25)
        username_entry.grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        username_entry.focus()
        
        # Password
        tk.Label(form, text="Password:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        password_entry = tk.Entry(form, font=('Arial', 11), width=25, show='*')
        password_entry.grid(row=1, column=1, pady=10, padx=10, sticky='ew')
        
        # Confirm Password
        tk.Label(form, text="Confirm Password:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=2, column=0, sticky='w', pady=10)
        confirm_password_entry = tk.Entry(form, font=('Arial', 11), width=25, show='*')
        confirm_password_entry.grid(row=2, column=1, pady=10, padx=10, sticky='ew')
        
        # Display Name
        tk.Label(form, text="Display Name:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=10)
        display_name_entry = tk.Entry(form, font=('Arial', 11), width=25)
        display_name_entry.grid(row=3, column=1, pady=10, padx=10, sticky='ew')
        
        # Date of Birth
        tk.Label(form, text="Date of Birth:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=4, column=0, sticky='w', pady=10)
        dob_entry = tk.Entry(form, font=('Arial', 11), width=25)
        dob_entry.grid(row=4, column=1, pady=10, padx=10, sticky='ew')
        tk.Label(form, text="(Format: YYYY-MM-DD)", font=('Arial', 9),
                bg='#ecf0f1', fg='gray').grid(row=5, column=1, sticky='w', padx=10)
        
        # Country
        tk.Label(form, text="Country:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=6, column=0, sticky='w', pady=10)
        country_entry = tk.Entry(form, font=('Arial', 11), width=25)
        country_entry.grid(row=6, column=1, pady=10, padx=10, sticky='ew')
        
        # Bio
        tk.Label(form, text="Bio:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=7, column=0, sticky='nw', pady=10)
        bio_text = tk.Text(form, font=('Arial', 10), width=25, height=4)
        bio_text.grid(row=7, column=1, pady=10, padx=10, sticky='ew')
        
        # Configure column weights
        form.grid_columnconfigure(1, weight=1)
        
        result_label = tk.Label(form, text="", font=('Arial', 10),
                               bg='#ecf0f1', fg='red')
        result_label.grid(row=8, column=0, columnspan=2, pady=10)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            display_name = display_name_entry.get().strip() or None
            dob = dob_entry.get().strip() or None
            country = country_entry.get().strip() or None
            bio = bio_text.get('1.0', tk.END).strip() or None
            
            # Validation
            if not username:
                result_label.config(text="Username is required")
                return
            
            if len(username) < 3:
                result_label.config(text="Username must be at least 3 characters")
                return
            
            if not password:
                result_label.config(text="Password is required")
                return
            
            if len(password) < 5:
                result_label.config(text="Password must be at least 5 characters")
                return
            
            if password != confirm_password:
                result_label.config(text="Passwords do not match")
                return
            
            # Register user
            success, msg = self.db.register_user(username, password, display_name, dob, country, bio)
            
            if success:
                messagebox.showinfo("Success", "Account created successfully! Please login.", 
                                  parent=register_window)
                register_window.destroy()
                # Auto-fill username and focus password field
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, username)
                self.password_entry.focus()
            else:
                result_label.config(text=msg)
        
        # Buttons
        btn_frame = tk.Frame(form, bg='#ecf0f1')
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Register", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=register, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=register_window.destroy, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        # Bind Enter key to register
        username_entry.bind('<Return>', lambda e: password_entry.focus_set())
        password_entry.bind('<Return>', lambda e: confirm_password_entry.focus_set())
        confirm_password_entry.bind('<Return>', lambda e: display_name_entry.focus_set())
    
    def create_chat_screen(self):
        """Create main chat interface with tabs for Direct Messages and Groups"""
        self.clear_screen()
        
        # Top bar with user info
        top_bar = tk.Frame(self.root, bg='#34495e', height=50)
        top_bar.pack(fill='x')
        
        display_name = self.current_user.get('display_name') or self.current_user['username']
        tk.Label(top_bar, text=f"👤 {display_name}", 
                font=('Arial', 12, 'bold'), bg='#34495e', fg='white').pack(side='left', padx=10, pady=10)
        
        # Check for pending group invites
        group_invites = self.db.get_pending_invites(self.current_user['user_id'])
        if group_invites:
            invite_btn = tk.Button(top_bar, text=f"🔔 {len(group_invites)} Group Invite(s)", 
                                  command=self.show_invites,
                                  bg='#e74c3c', fg='white', cursor='hand2', font=('Arial', 10, 'bold'))
            invite_btn.pack(side='right', padx=5, pady=10)
        
        # Check for pending friend requests
        friend_requests = self.db.get_pending_friend_requests(self.current_user['user_id'])
        if friend_requests:
            friend_btn = tk.Button(top_bar, text=f"👤 {len(friend_requests)} Friend Request(s)", 
                                  command=self.show_friend_requests,
                                  bg='#3498db', fg='white', cursor='hand2', font=('Arial', 10, 'bold'))
            friend_btn.pack(side='right', padx=5, pady=10)
        
        tk.Button(top_bar, text="⚙️ Settings", command=self.open_settings,
                 bg='#9b59b6', fg='white', cursor='hand2').pack(side='right', padx=5, pady=10)
        
        tk.Button(top_bar, text="🚪 Logout", command=self.create_login_screen,
                 bg='#e74c3c', fg='white', cursor='hand2').pack(side='right', padx=5, pady=10)
        
        # Main container with notebook (tabs)
        main_container = tk.Frame(self.root)
        main_container.pack(expand=True, fill='both')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Direct Messages Tab
        dm_frame = tk.Frame(self.notebook)
        self.notebook.add(dm_frame, text='💬 Direct Messages')
        self.create_direct_messages_tab(dm_frame)
        
        # Group Chats Tab
        group_frame = tk.Frame(self.notebook)
        self.notebook.add(group_frame, text='👥 Group Chats')
        self.create_group_chats_tab(group_frame)
        
        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)
    
    def on_tab_change(self, event):
        """Handle tab change"""
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:
            self.chat_mode = 'direct'
        else:
            self.chat_mode = 'group'
    
    def create_direct_messages_tab(self, parent):
        """Create the Direct Messages interface"""
        # Left panel - Users list
        left_panel = tk.Frame(parent, bg='#ecf0f1', width=200, relief='raised', borderwidth=1)
        left_panel.pack(side='left', fill='y')
        
        # Header
        header_frame = tk.Frame(left_panel, bg='#ecf0f1')
        header_frame.pack(fill='x', pady=10, padx=5)
        
        tk.Label(header_frame, text="👥 Friends", font=('Arial', 14, 'bold'), 
                bg='#ecf0f1').pack(side='left', padx=5)
        
        tk.Button(header_frame, text="➕", font=('Arial', 14, 'bold'),
                 bg='#2ecc71', fg='white', cursor='hand2',
                 command=self.add_friend_dialog, width=3).pack(side='right', padx=5)
        
        # Users listbox
        self.users_listbox = tk.Listbox(left_panel, font=('Arial', 11), 
                                        bg='#ecf0f1', selectbackground='#3498db')
        self.users_listbox.pack(expand=True, fill='both', padx=5, pady=5)
        self.users_listbox.bind('<<ListboxSelect>>', self.on_user_select)
        
        # Load users
        self.load_users()
        
        # Right panel - Chat area
        right_panel = tk.Frame(parent)
        right_panel.pack(side='right', expand=True, fill='both')
        
        # Chat header
        self.dm_chat_header = tk.Frame(right_panel, bg='#bdc3c7', height=40)
        self.dm_chat_header.pack(fill='x', padx=10, pady=(10, 0))
        
        self.dm_selected_label = tk.Label(self.dm_chat_header, text="Select a user to chat", 
                                         font=('Arial', 12, 'bold'), bg='#bdc3c7')
        self.dm_selected_label.pack(side='left', padx=10, pady=8)
        
        self.dm_streak_label = tk.Label(self.dm_chat_header, text="", 
                                       font=('Arial', 10, 'bold'), bg='#bdc3c7', fg='#e74c3c')
        self.dm_streak_label.pack(side='left', padx=5, pady=8)
        
        # Search bar
        search_frame = tk.Frame(self.dm_chat_header, bg='#bdc3c7')
        search_frame.pack(side='left', padx=10, fill='x', expand=True)
        
        self.dm_search_entry = tk.Entry(search_frame, font=('Arial', 9), width=20)
        self.dm_search_entry.pack(side='left', padx=5)
        self.dm_search_entry.insert(0, "Search messages...")
        self.dm_search_entry.config(fg='gray')
        self.dm_search_entry.bind('<FocusIn>', lambda e: self.dm_search_entry.delete(0, tk.END) if self.dm_search_entry.get() == "Search messages..." else None)
        self.dm_search_entry.bind('<FocusOut>', lambda e: self.dm_search_entry.insert(0, "Search messages...") if not self.dm_search_entry.get() else None)
        self.dm_search_entry.bind('<Return>', lambda e: self.search_dm_messages())
        
        tk.Button(search_frame, text="🔍", font=('Arial', 10),
                 bg='#95a5a6', fg='white', command=self.search_dm_messages,
                 cursor='hand2', width=3).pack(side='left', padx=2)
        
        self.dm_view_profile_btn = tk.Button(self.dm_chat_header, text="👤 View Profile", 
                                            font=('Arial', 10), bg='#3498db', fg='white',
                                            cursor='hand2', command=self.view_user_profile,
                                            state='disabled')
        self.dm_view_profile_btn.pack(side='right', padx=10, pady=5)
        
        # Clear chat button
        self.dm_clear_chat_btn = tk.Button(self.dm_chat_header, text="🗑️ Clear", 
                                          font=('Arial', 9), bg='#e74c3c', fg='white',
                                          cursor='hand2', command=self.clear_dm_chat,
                                          state='disabled')
        self.dm_clear_chat_btn.pack(side='right', padx=5, pady=5)
        
        # Chat display
        self.dm_chat_display = scrolledtext.ScrolledText(right_panel, state='disabled', 
                                                         wrap=tk.WORD, font=('Arial', 10))
        self.dm_chat_display.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Message input area
        input_frame = tk.Frame(right_panel)
        input_frame.pack(fill='x', padx=10, pady=10)
        
        self.dm_message_entry = tk.Entry(input_frame, font=('Arial', 11))
        self.dm_message_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))
        self.dm_message_entry.bind('<Return>', lambda e: self.send_direct_message())
        
        # Emoji picker button
        tk.Button(input_frame, text="😀", font=('Arial', 14),
                 bg='#f39c12', fg='white', command=self.show_emoji_picker_dm, 
                 cursor='hand2', width=3).pack(side='right', padx=(0, 5))
        
        # Image upload button
        tk.Button(input_frame, text="📷", font=('Arial', 14),
                 bg='#3498db', fg='white', command=self.upload_image_dm, 
                 cursor='hand2', width=3).pack(side='right', padx=(0, 5))
        
        tk.Button(input_frame, text="📤 Send", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=self.send_direct_message, 
                 cursor='hand2', width=10).pack(side='right')
    
    def create_group_chats_tab(self, parent):
        """Create the Group Chats interface"""
        # Left panel - Groups list
        left_panel = tk.Frame(parent, bg='#ecf0f1', width=250, relief='raised', borderwidth=1)
        left_panel.pack(side='left', fill='y')
        
        # Header with Create Group button
        header_frame = tk.Frame(left_panel, bg='#ecf0f1')
        header_frame.pack(fill='x', pady=10, padx=5)
        
        tk.Label(header_frame, text="👥 My Groups", font=('Arial', 14, 'bold'), 
                bg='#ecf0f1').pack(side='left', padx=5)
        
        tk.Button(header_frame, text="➕", font=('Arial', 14, 'bold'),
                 bg='#2ecc71', fg='white', cursor='hand2',
                 command=self.create_group_dialog, width=3).pack(side='right', padx=5)
        
        # Groups listbox
        self.groups_listbox = tk.Listbox(left_panel, font=('Arial', 11), 
                                         bg='#ecf0f1', selectbackground='#3498db')
        self.groups_listbox.pack(expand=True, fill='both', padx=5, pady=5)
        self.groups_listbox.bind('<<ListboxSelect>>', self.on_group_select)
        
        # Load groups
        self.load_groups()
        
        # Right panel - Group chat area
        right_panel = tk.Frame(parent)
        right_panel.pack(side='right', expand=True, fill='both')
        
        # Group chat header
        self.group_chat_header = tk.Frame(right_panel, bg='#bdc3c7', height=40)
        self.group_chat_header.pack(fill='x', padx=10, pady=(10, 0))
        
        self.group_selected_label = tk.Label(self.group_chat_header, text="Select a group to chat", 
                                            font=('Arial', 12, 'bold'), bg='#bdc3c7')
        self.group_selected_label.pack(side='left', padx=10, pady=8)
        
        # Group action buttons
        self.group_info_btn = tk.Button(self.group_chat_header, text="ℹ️ Info", 
                                       font=('Arial', 10), bg='#3498db', fg='white',
                                       cursor='hand2', command=self.show_group_info,
                                       state='disabled')
        self.group_info_btn.pack(side='right', padx=5, pady=5)
        
        # Search bar
        group_search_frame = tk.Frame(self.group_chat_header, bg='#bdc3c7')
        group_search_frame.pack(side='left', padx=10, fill='x', expand=True)
        
        self.group_search_entry = tk.Entry(group_search_frame, font=('Arial', 9), width=20)
        self.group_search_entry.pack(side='left', padx=5)
        self.group_search_entry.insert(0, "Search messages...")
        self.group_search_entry.config(fg='gray')
        self.group_search_entry.bind('<FocusIn>', lambda e: self.group_search_entry.delete(0, tk.END) if self.group_search_entry.get() == "Search messages..." else None)
        self.group_search_entry.bind('<FocusOut>', lambda e: self.group_search_entry.insert(0, "Search messages...") if not self.group_search_entry.get() else None)
        self.group_search_entry.bind('<Return>', lambda e: self.search_group_messages())
        
        tk.Button(group_search_frame, text="🔍", font=('Arial', 10),
                 bg='#95a5a6', fg='white', command=self.search_group_messages,
                 cursor='hand2', width=3).pack(side='left', padx=2)
        
        self.group_members_btn = tk.Button(self.group_chat_header, text="👥 Members", 
                                          font=('Arial', 10), bg='#9b59b6', fg='white',
                                          cursor='hand2', command=self.show_group_members,
                                          state='disabled')
        self.group_members_btn.pack(side='right', padx=5, pady=5)
        
        # Clear chat button
        self.group_clear_chat_btn = tk.Button(self.group_chat_header, text="🗑️ Clear", 
                                              font=('Arial', 9), bg='#e74c3c', fg='white',
                                              cursor='hand2', command=self.clear_group_chat,
                                              state='disabled')
        self.group_clear_chat_btn.pack(side='right', padx=5, pady=5)
        
        # Group chat display
        self.group_chat_display = scrolledtext.ScrolledText(right_panel, state='disabled', 
                                                            wrap=tk.WORD, font=('Arial', 10))
        self.group_chat_display.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Group message input area
        group_input_frame = tk.Frame(right_panel)
        group_input_frame.pack(fill='x', padx=10, pady=10)
        
        self.group_message_entry = tk.Entry(group_input_frame, font=('Arial', 11))
        self.group_message_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))
        self.group_message_entry.bind('<Return>', lambda e: self.send_group_message())
        
        # Emoji picker button
        tk.Button(group_input_frame, text="😀", font=('Arial', 14),
                 bg='#f39c12', fg='white', command=self.show_emoji_picker_group, 
                 cursor='hand2', width=3).pack(side='right', padx=(0, 5))
        
        # Image upload button
        tk.Button(group_input_frame, text="📷", font=('Arial', 14),
                 bg='#3498db', fg='white', command=self.upload_image_group, 
                 cursor='hand2', width=3).pack(side='right', padx=(0, 5))
        
        tk.Button(group_input_frame, text="📤 Send", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=self.send_group_message, 
                 cursor='hand2', width=10).pack(side='right')
    
    def create_group_dialog(self):
        """Dialog to create a new group"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Create New Group")
        dialog.geometry("450x350")
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Create New Group", font=('Arial', 18, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        # Form frame
        form = tk.Frame(dialog, bg='#ecf0f1')
        form.pack(padx=30, pady=10, fill='both', expand=True)
        
        # Group Name
        tk.Label(form, text="Group Name:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        name_entry = tk.Entry(form, font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        name_entry.focus()
        
        # Group Avatar (emoji)
        tk.Label(form, text="Avatar (Emoji):", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        avatar_entry = tk.Entry(form, font=('Arial', 11), width=30)
        avatar_entry.insert(0, '👥')
        avatar_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Group Description
        tk.Label(form, text="Description:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=2, column=0, sticky='nw', pady=10)
        desc_text = tk.Text(form, font=('Arial', 10), width=30, height=4)
        desc_text.grid(row=2, column=1, pady=10, padx=10)
        
        def create():
            name = name_entry.get().strip()
            avatar = avatar_entry.get().strip() or '👥'
            description = desc_text.get('1.0', tk.END).strip()
            
            if not name:
                messagebox.showerror("Error", "Group name is required", parent=dialog)
                return
            
            group_id = self.db.create_group(name, description, 
                                           self.current_user['user_id'], avatar)
            
            if group_id:
                messagebox.showinfo("Success", f"Group '{name}' created successfully!", 
                                  parent=dialog)
                self.load_groups()
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to create group", parent=dialog)
        
        # Buttons
        btn_frame = tk.Frame(form, bg='#ecf0f1')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="Create Group", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=create, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=dialog.destroy, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
    
    def show_friend_requests(self):
        """Show pending friend requests"""
        requests = self.db.get_pending_friend_requests(self.current_user['user_id'])
        
        if not requests:
            messagebox.showinfo("Friend Requests", "No pending friend requests")
            return
        
        request_window = tk.Toplevel(self.root)
        request_window.title("Friend Requests")
        request_window.geometry("450x400")
        request_window.configure(bg='#ecf0f1')
        
        tk.Label(request_window, text=f"👤 You have {len(requests)} friend request(s)", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=15)
        
        # Scrollable frame for requests
        canvas = tk.Canvas(request_window, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(request_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for request in requests:
            request_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', 
                                   borderwidth=2, padx=15, pady=10)
            request_frame.pack(fill='x', padx=10, pady=5)
            
            # User info
            info_frame = tk.Frame(request_frame, bg='white')
            info_frame.pack(fill='x')
            
            requester_name = request.get('display_name') or request['username']
            tk.Label(info_frame, text=f"{requester_name}", 
                    font=('Arial', 13, 'bold'), bg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"@{request['username']}", 
                    font=('Arial', 10), bg='white', fg='#7f8c8d').pack(anchor='w', pady=2)
            
            # Buttons
            btn_frame = tk.Frame(request_frame, bg='white')
            btn_frame.pack(fill='x', pady=5)
            
            def accept(req_id=request['request_id']):
                success, msg = self.db.respond_to_friend_request(req_id, self.current_user['user_id'], True)
                if success:
                    messagebox.showinfo("Success", "Friend request accepted!", parent=request_window)
                    request_window.destroy()
                    self.create_chat_screen()  # Refresh
                else:
                    messagebox.showerror("Error", msg, parent=request_window)
            
            def decline(req_id=request['request_id']):
                success, msg = self.db.respond_to_friend_request(req_id, self.current_user['user_id'], False)
                if success:
                    messagebox.showinfo("Success", "Friend request declined", parent=request_window)
                    request_window.destroy()
                    self.create_chat_screen()  # Refresh
                else:
                    messagebox.showerror("Error", msg, parent=request_window)
            
            tk.Button(btn_frame, text="✓ Accept", font=('Arial', 10, 'bold'),
                     bg='#2ecc71', fg='white', command=accept, 
                     cursor='hand2', width=12).pack(side='left', padx=5)
            
            tk.Button(btn_frame, text="✗ Decline", font=('Arial', 10, 'bold'),
                     bg='#e74c3c', fg='white', command=decline, 
                     cursor='hand2', width=12).pack(side='left', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def show_invites(self):
        """Show pending group invitations"""
        invites = self.db.get_pending_invites(self.current_user['user_id'])
        
        if not invites:
            messagebox.showinfo("Invitations", "No pending invitations")
            return
        
        invite_window = tk.Toplevel(self.root)
        invite_window.title("Group Invitations")
        invite_window.geometry("500x400")
        invite_window.configure(bg='#ecf0f1')
        
        tk.Label(invite_window, text=f"🔔 You have {len(invites)} invitation(s)", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(pady=15)
        
        # Scrollable frame for invites
        canvas = tk.Canvas(invite_window, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(invite_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for invite in invites:
            invite_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', 
                                   borderwidth=2, padx=15, pady=10)
            invite_frame.pack(fill='x', padx=10, pady=5)
            
            # Group info
            info_frame = tk.Frame(invite_frame, bg='white')
            info_frame.pack(fill='x')
            
            tk.Label(info_frame, text=f"{invite['group_avatar']} {invite['group_name']}", 
                    font=('Arial', 13, 'bold'), bg='white').pack(anchor='w')
            
            inviter_name = invite.get('inviter_name') or invite['inviter_username']
            tk.Label(info_frame, text=f"Invited by: {inviter_name}", 
                    font=('Arial', 10), bg='white', fg='#7f8c8d').pack(anchor='w', pady=2)
            
            if invite['group_description']:
                tk.Label(info_frame, text=invite['group_description'], 
                        font=('Arial', 9), bg='white', fg='#95a5a6', 
                        wraplength=350).pack(anchor='w', pady=2)
            
            # Buttons
            btn_frame = tk.Frame(invite_frame, bg='white')
            btn_frame.pack(fill='x', pady=5)
            
            def accept(inv_id=invite['invite_id']):
                success, msg = self.db.respond_to_invite(inv_id, self.current_user['user_id'], True)
                if success:
                    messagebox.showinfo("Success", "Invitation accepted!", parent=invite_window)
                    invite_window.destroy()
                    self.create_chat_screen()  # Refresh
                else:
                    messagebox.showerror("Error", msg, parent=invite_window)
            
            def decline(inv_id=invite['invite_id']):
                success, msg = self.db.respond_to_invite(inv_id, self.current_user['user_id'], False)
                if success:
                    messagebox.showinfo("Success", "Invitation declined", parent=invite_window)
                    invite_window.destroy()
                    self.create_chat_screen()  # Refresh
                else:
                    messagebox.showerror("Error", msg, parent=invite_window)
            
            tk.Button(btn_frame, text="✓ Accept", font=('Arial', 10, 'bold'),
                     bg='#2ecc71', fg='white', command=accept, 
                     cursor='hand2', width=12).pack(side='left', padx=5)
            
            tk.Button(btn_frame, text="✗ Decline", font=('Arial', 10, 'bold'),
                     bg='#e74c3c', fg='white', command=decline, 
                     cursor='hand2', width=12).pack(side='left', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def show_group_info(self):
        """Show detailed group information"""
        if not self.selected_group:
            return
        
        group = self.db.get_group_by_id(self.selected_group['group_id'])
        if not group:
            return
        
        info_window = tk.Toplevel(self.root)
        info_window.title(f"{group['group_name']} - Info")
        info_window.geometry("450x500")
        info_window.configure(bg='#ecf0f1')
        
        # Header
        header = tk.Frame(info_window, bg='#3498db', height=100)
        header.pack(fill='x')
        
        tk.Label(header, text=f"{group['group_avatar']}", 
                font=('Arial', 36), bg='#3498db').pack(pady=10)
        tk.Label(header, text=group['group_name'], 
                font=('Arial', 20, 'bold'), bg='#3498db', fg='white').pack(pady=5)
        
        # Content
        content = tk.Frame(info_window, bg='#ecf0f1', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        # Description
        if group.get('group_description'):
            desc_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
            desc_frame.pack(fill='x', pady=10)
            
            tk.Label(desc_frame, text="Description", font=('Arial', 10, 'bold'),
                    bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
            tk.Label(desc_frame, text=group['group_description'], font=('Arial', 11),
                    bg='white', anchor='w', wraplength=380, justify='left').pack(fill='x', padx=10, pady=8)
        
        # Creator
        creator_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
        creator_frame.pack(fill='x', pady=10)
        
        tk.Label(creator_frame, text="Created By", font=('Arial', 10, 'bold'),
                bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
        creator_name = group.get('creator_name') or group['creator_username']
        tk.Label(creator_frame, text=creator_name, font=('Arial', 11),
                bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # Member count
        members_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
        members_frame.pack(fill='x', pady=10)
        
        tk.Label(members_frame, text="Members", font=('Arial', 10, 'bold'),
                bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
        tk.Label(members_frame, text=f"{group['member_count']} member(s)", font=('Arial', 11),
                bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # User's role
        role_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
        role_frame.pack(fill='x', pady=10)
        
        tk.Label(role_frame, text="Your Role", font=('Arial', 10, 'bold'),
                bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
        role_text = "Admin" if self.selected_group['role'] == 'admin' else "Member"
        tk.Label(role_frame, text=role_text, font=('Arial', 11),
                bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # Leave group button
        if self.selected_group['role'] != 'admin' or group['member_count'] > 1:
            def leave():
                if messagebox.askyesno("Confirm", "Are you sure you want to leave this group?", 
                                      parent=info_window):
                    success = self.db.leave_group(group['group_id'], self.current_user['user_id'])
                    if success:
                        messagebox.showinfo("Success", "You have left the group", parent=info_window)
                        info_window.destroy()
                        self.load_groups()
                    else:
                        messagebox.showerror("Error", "Failed to leave group", parent=info_window)
            
            tk.Button(content, text="🚪 Leave Group", font=('Arial', 11, 'bold'),
                     bg='#e74c3c', fg='white', command=leave, 
                     cursor='hand2', width=20).pack(pady=15)
        
        tk.Button(content, text="Close", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=info_window.destroy, 
                 cursor='hand2', width=20).pack(pady=5)
    
    def show_group_members(self):
        """Show group members with invite and remove options"""
        if not self.selected_group:
            return
        
        members = self.db.get_group_members(self.selected_group['group_id'])
        is_admin = self.selected_group['role'] == 'admin'
        
        members_window = tk.Toplevel(self.root)
        members_window.title(f"{self.selected_group['group_name']} - Members")
        members_window.geometry("500x500")
        members_window.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(members_window, bg='#ecf0f1')
        header_frame.pack(fill='x', padx=15, pady=15)
        
        tk.Label(header_frame, text=f"👥 Group Members ({len(members)})", 
                font=('Arial', 16, 'bold'), bg='#ecf0f1').pack(side='left')
        
        if is_admin:
            tk.Button(header_frame, text="➕ Invite", font=('Arial', 10, 'bold'),
                     bg='#2ecc71', fg='white', cursor='hand2',
                     command=lambda: self.invite_to_group(members_window)).pack(side='right', padx=5)
        
        # Members list
        canvas = tk.Canvas(members_window, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(members_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for member in members:
            member_frame = tk.Frame(scrollable_frame, bg='white', relief='raised', 
                                   borderwidth=1, padx=10, pady=8)
            member_frame.pack(fill='x', padx=10, pady=5)
            
            # Member info
            info_frame = tk.Frame(member_frame, bg='white')
            info_frame.pack(side='left', fill='x', expand=True)
            
            member_name = member.get('display_name') or member['username']
            role_badge = " 👑" if member['role'] == 'admin' else ""
            
            tk.Label(info_frame, text=f"{member_name}{role_badge}", 
                    font=('Arial', 12, 'bold'), bg='white').pack(anchor='w')
            tk.Label(info_frame, text=f"@{member['username']}", 
                    font=('Arial', 9), bg='white', fg='#7f8c8d').pack(anchor='w')
            
            # Remove button (only for admins and not self)
            if is_admin and member['user_id'] != self.current_user['user_id']:
                def remove(m_id=member['user_id'], m_name=member_name):
                    if messagebox.askyesno("Confirm", f"Remove {m_name} from group?", 
                                          parent=members_window):
                        success, msg = self.db.remove_member(
                            self.selected_group['group_id'],
                            self.current_user['user_id'],
                            m_id
                        )
                        if success:
                            messagebox.showinfo("Success", msg, parent=members_window)
                            members_window.destroy()
                            self.show_group_members()  # Refresh
                        else:
                            messagebox.showerror("Error", msg, parent=members_window)
                
                tk.Button(member_frame, text="✗ Remove", font=('Arial', 9),
                         bg='#e74c3c', fg='white', cursor='hand2',
                         command=remove, width=10).pack(side='right', padx=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def invite_to_group(self, parent_window):
        """Invite users to the group"""
        if not self.selected_group:
            return
        
        # Get all users except current members
        all_users = self.db.get_all_users()
        members = self.db.get_group_members(self.selected_group['group_id'])
        member_ids = [m['user_id'] for m in members]
        
        available_users = [u for u in all_users if u['user_id'] not in member_ids]
        
        if not available_users:
            messagebox.showinfo("Info", "All users are already members of this group", 
                              parent=parent_window)
            return
        
        invite_dialog = tk.Toplevel(parent_window)
        invite_dialog.title("Invite Users")
        invite_dialog.geometry("400x450")
        invite_dialog.configure(bg='#ecf0f1')
        invite_dialog.transient(parent_window)
        invite_dialog.grab_set()
        
        tk.Label(invite_dialog, text="Select users to invite", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=15)
        
        # Listbox with checkboxes (using multiple selection)
        tk.Label(invite_dialog, text="Available users:", 
                font=('Arial', 11), bg='#ecf0f1').pack(pady=5)
        
        users_listbox = tk.Listbox(invite_dialog, font=('Arial', 11), 
                                   selectmode=tk.MULTIPLE, height=15)
        users_listbox.pack(padx=20, pady=10, fill='both', expand=True)
        
        for user in available_users:
            display_name = user.get('display_name') or user['username']
            users_listbox.insert(tk.END, f"{display_name} (@{user['username']})")
        
        def send_invites():
            selected = users_listbox.curselection()
            if not selected:
                messagebox.showwarning("Warning", "Please select at least one user", 
                                     parent=invite_dialog)
                return
            
            success_count = 0
            for idx in selected:
                user = available_users[idx]
                success, msg = self.db.invite_to_group(
                    self.selected_group['group_id'],
                    self.current_user['user_id'],
                    user['user_id']
                )
                if success:
                    success_count += 1
            
            if success_count > 0:
                messagebox.showinfo("Success", 
                                  f"Sent {success_count} invitation(s) successfully!", 
                                  parent=invite_dialog)
                invite_dialog.destroy()
            else:
                messagebox.showerror("Error", "Failed to send invitations", 
                                   parent=invite_dialog)
        
        btn_frame = tk.Frame(invite_dialog, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Send Invites", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=send_invites, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=invite_dialog.destroy, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
    
    def load_users(self):
        """Load friends into the listbox"""
        self.users_listbox.delete(0, tk.END)
        friends = self.db.get_friends(self.current_user['user_id'])
        
        for friend in friends:
            display_name = friend.get('display_name') or friend['username']
            self.users_listbox.insert(tk.END, display_name)
        
        # If no friends, show message
        if not friends:
            self.users_listbox.insert(tk.END, "No friends yet")
    
    def add_friend_dialog(self):
        """Dialog to send a friend request"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Friend")
        dialog.geometry("400x200")
        dialog.configure(bg='#ecf0f1')
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Send Friend Request", font=('Arial', 16, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        tk.Label(dialog, text="Username:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        username_entry = tk.Entry(dialog, font=('Arial', 11), width=30)
        username_entry.pack(pady=5)
        username_entry.focus()
        
        result_label = tk.Label(dialog, text="", font=('Arial', 10),
                               bg='#ecf0f1', fg='red')
        result_label.pack(pady=10)
        
        def send_request():
            username = username_entry.get().strip()
            if not username:
                result_label.config(text="Please enter a username")
                return
            
            success, msg = self.db.send_friend_request(self.current_user['user_id'], username)
            if success:
                messagebox.showinfo("Success", msg, parent=dialog)
                dialog.destroy()
            else:
                result_label.config(text=msg)
        
        btn_frame = tk.Frame(dialog, bg='#ecf0f1')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Send Request", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=send_request, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=dialog.destroy, 
                 cursor='hand2', width=15).pack(side='left', padx=5)
        
        username_entry.bind('<Return>', lambda e: send_request())
    
    def load_groups(self):
        """Load user's groups into the listbox"""
        self.groups_listbox.delete(0, tk.END)
        groups = self.db.get_user_groups(self.current_user['user_id'])
        
        for group in groups:
            role_badge = " 👑" if group['role'] == 'admin' else ""
            display_text = f"{group['group_avatar']} {group['group_name']}{role_badge}"
            self.groups_listbox.insert(tk.END, display_text)
    
    def update_streak_display(self):
        """Update the streak display in chat header"""
        if not self.selected_user:
            self.dm_streak_label.config(text="")
            return
        
        streak = self.db.get_streak(self.current_user['user_id'], self.selected_user['user_id'])
        
        if streak and streak['streak_count'] > 0:
            self.dm_streak_label.config(text=f"🔥 {streak['streak_count']} day streak")
        else:
            self.dm_streak_label.config(text="")
    
    def on_user_select(self, event):
        """Handle user selection from list"""
        selection = self.users_listbox.curselection()
        if selection:
            display_name = self.users_listbox.get(selection[0])
            
            # Don't do anything if it's the "No friends yet" message
            if display_name == "No friends yet":
                return
            
            friends = self.db.get_friends(self.current_user['user_id'])
            
            for friend in friends:
                friend_display = friend.get('display_name') or friend['username']
                if friend_display == display_name:
                    self.selected_user = friend
                    self.dm_selected_label.config(text=f"💬 Chatting with: {friend_display}")
                    self.dm_view_profile_btn.config(state='normal')
                    self.dm_clear_chat_btn.config(state='normal')
                    self.update_streak_display()
                    self.load_dm_conversation()
                    break
    
    def on_group_select(self, event):
        """Handle group selection from list"""
        selection = self.groups_listbox.curselection()
        if selection:
            groups = self.db.get_user_groups(self.current_user['user_id'])
            if selection[0] < len(groups):
                self.selected_group = groups[selection[0]]
                group_name = self.selected_group['group_name']
                self.group_selected_label.config(text=f"👥 {group_name}")
                self.group_info_btn.config(state='normal')
                self.group_members_btn.config(state='normal')
                self.group_clear_chat_btn.config(state='normal')
                self.load_group_conversation()
    
    def load_dm_conversation(self):
        """Load direct message conversation with selected user"""
        if not self.selected_user:
            return
        
        self.dm_chat_display.config(state='normal')
        self.dm_chat_display.delete('1.0', tk.END)
        
        # Clear previous image references
        if hasattr(self, '_image_refs'):
            self._image_refs.clear()
        else:
            self._image_refs = []
        
        messages = self.db.get_conversation(self.current_user['user_id'], 
                                           self.selected_user['user_id'])
        
        selected_display = self.selected_user.get('display_name') or self.selected_user['username']
        
        if not messages:
            self.dm_chat_display.insert(tk.END, f"No messages yet with {selected_display}\n")
        else:
            for msg in messages:
                sender = msg['sender_name']
                timestamp = msg['sent_at'].strftime('%I:%M %p')
                text = msg['message_text']
                image_path = msg.get('image_path')
                message_id = msg['message_id']
                is_edited = msg.get('is_edited', 0)
                is_own = msg['sender_id'] == self.current_user['user_id']
                
                if is_own:
                    self.dm_chat_display.insert(tk.END, f"You [{timestamp}]", 'you')
                else:
                    self.dm_chat_display.insert(tk.END, f"{sender} [{timestamp}]", 'them')
                
                # Show edited indicator
                if is_edited:
                    self.dm_chat_display.insert(tk.END, " (edited)", 'edited')
                
                self.dm_chat_display.insert(tk.END, ":\n")
                
                # Display image if present
                if image_path and os.path.exists(image_path):
                    try:
                        # Load and resize image
                        img = Image.open(image_path)
                        img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        # Insert image
                        self.dm_chat_display.insert(tk.END, "\n")
                        self.dm_chat_display.image_create(tk.END, image=photo)
                        self.dm_chat_display.insert(tk.END, "\n")
                        
                        # Keep reference to prevent garbage collection
                        self._image_refs.append(photo)
                    except Exception as e:
                        self.dm_chat_display.insert(tk.END, f"[Image - Error loading: {str(e)}]\n")
                
                # Display text message
                if text and text != "[Image]":
                    self.dm_chat_display.insert(tk.END, f"{text}\n")
                elif not image_path:
                    self.dm_chat_display.insert(tk.END, "\n")
                
                # Show reactions
                reactions = self.db.get_message_reactions(message_id, 'direct')
                if reactions:
                    reaction_text = " ".join([r['reaction_type'] for r in reactions])
                    self.dm_chat_display.insert(tk.END, f"  {reaction_text}\n", 'reactions')
                
                # Show read receipt for own messages
                if is_own:
                    is_read = self.db.is_message_read(message_id, self.selected_user['user_id'], 'direct')
                    read_indicator = "✓✓" if is_read else "✓"
                    self.dm_chat_display.insert(tk.END, f"  {read_indicator}\n", 'read_receipt')
                else:
                    # Mark as read when viewing
                    self.db.mark_as_read(message_id, self.current_user['user_id'], 'direct')
                
                # Add action buttons for own messages
                if is_own:
                    start_pos = self.dm_chat_display.index(tk.END + "-2l")
                    self.dm_chat_display.insert(tk.END, "  [React] [Edit] [Delete] [Forward]\n", 'actions')
                    end_pos = self.dm_chat_display.index(tk.END + "-1l")
                    
                    # Use unique tag names for each message to avoid conflicts
                    react_tag = f"react_btn_{message_id}"
                    edit_tag = f"edit_btn_{message_id}"
                    delete_tag = f"delete_btn_{message_id}"
                    forward_tag = f"forward_btn_{message_id}"
                    
                    # Make action buttons clickable
                    def on_react(e, mid=message_id):
                        self.show_reaction_menu(mid, 'direct', e.x_root, e.y_root)
                    def on_edit(e, mid=message_id, txt=text):
                        self.edit_message_dialog(mid, txt, 'direct')
                    def on_delete(e, mid=message_id):
                        self.delete_message_confirm(mid, 'direct')
                    def on_forward(e, mid=message_id):
                        self.forward_message_dialog(mid, 'direct')
                    
                    # Find positions for each action
                    react_start = self.dm_chat_display.search("  [React]", start_pos, end_pos)
                    react_end = self.dm_chat_display.search("]", react_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(react_tag, react_start, react_end)
                    self.dm_chat_display.tag_config(react_tag, foreground='#3498db', underline=True)
                    self.dm_chat_display.tag_bind(react_tag, "<Button-1>", on_react)
                    
                    edit_start = self.dm_chat_display.search("[Edit]", react_end, end_pos)
                    edit_end = self.dm_chat_display.search("]", edit_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(edit_tag, edit_start, edit_end)
                    self.dm_chat_display.tag_config(edit_tag, foreground='#2ecc71', underline=True)
                    self.dm_chat_display.tag_bind(edit_tag, "<Button-1>", on_edit)
                    
                    delete_start = self.dm_chat_display.search("[Delete]", edit_end, end_pos)
                    delete_end = self.dm_chat_display.search("]", delete_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(delete_tag, delete_start, delete_end)
                    self.dm_chat_display.tag_config(delete_tag, foreground='#e74c3c', underline=True)
                    self.dm_chat_display.tag_bind(delete_tag, "<Button-1>", on_delete)
                    
                    forward_start = self.dm_chat_display.search("[Forward]", delete_end, end_pos)
                    forward_end = self.dm_chat_display.search("]", forward_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(forward_tag, forward_start, forward_end)
                    self.dm_chat_display.tag_config(forward_tag, foreground='#9b59b6', underline=True)
                    self.dm_chat_display.tag_bind(forward_tag, "<Button-1>", on_forward)
                
                # Add reaction button for other's messages
                else:
                    start_pos = self.dm_chat_display.index(tk.END + "-1l")
                    self.dm_chat_display.insert(tk.END, "  [React] [Forward]\n", 'actions')
                    end_pos = self.dm_chat_display.index(tk.END + "-1l")
                    
                    # Use unique tag names for each message
                    react_tag = f"react_btn_{message_id}"
                    forward_tag = f"forward_btn_{message_id}"
                    
                    def on_react(e, mid=message_id):
                        self.show_reaction_menu(mid, 'direct', e.x_root, e.y_root)
                    def on_forward(e, mid=message_id):
                        self.forward_message_dialog(mid, 'direct')
                    
                    react_start = self.dm_chat_display.search("  [React]", start_pos, end_pos)
                    react_end = self.dm_chat_display.search("]", react_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(react_tag, react_start, react_end)
                    self.dm_chat_display.tag_config(react_tag, foreground='#3498db', underline=True)
                    self.dm_chat_display.tag_bind(react_tag, "<Button-1>", on_react)
                    
                    forward_start = self.dm_chat_display.search("[Forward]", react_end, end_pos)
                    forward_end = self.dm_chat_display.search("]", forward_start, end_pos) + "+1c"
                    self.dm_chat_display.tag_add(forward_tag, forward_start, forward_end)
                    self.dm_chat_display.tag_config(forward_tag, foreground='#9b59b6', underline=True)
                    self.dm_chat_display.tag_bind(forward_tag, "<Button-1>", on_forward)
                
                self.dm_chat_display.insert(tk.END, "\n")
        
        self.dm_chat_display.tag_config('you', foreground='#2980b9', font=('Arial', 10, 'bold'))
        self.dm_chat_display.tag_config('them', foreground='#27ae60', font=('Arial', 10, 'bold'))
        self.dm_chat_display.tag_config('image_placeholder', foreground='#7f8c8d', font=('Arial', 9, 'italic'))
        self.dm_chat_display.tag_config('edited', foreground='#95a5a6', font=('Arial', 8, 'italic'))
        self.dm_chat_display.tag_config('reactions', font=('Arial', 12))
        self.dm_chat_display.tag_config('read_receipt', foreground='#3498db', font=('Arial', 9))
        self.dm_chat_display.config(state='disabled')
        self.dm_chat_display.see(tk.END)
        
        # Update streak display after loading conversation
        self.update_streak_display()
    
    def load_group_conversation(self):
        """Load group chat messages"""
        if not self.selected_group:
            return
        
        self.group_chat_display.config(state='normal')
        self.group_chat_display.delete('1.0', tk.END)
        
        # Clear previous image references
        if hasattr(self, '_group_image_refs'):
            self._group_image_refs.clear()
        else:
            self._group_image_refs = []
        
        messages = self.db.get_group_messages(self.selected_group['group_id'], 
                                              self.current_user['user_id'])
        
        if not messages:
            self.group_chat_display.insert(tk.END, "No messages yet in this group\n")
        else:
            for msg in messages:
                sender = msg['sender_name']
                timestamp = msg['sent_at'].strftime('%I:%M %p')
                text = msg['message_text']
                image_path = msg.get('image_path')
                message_id = msg['message_id']
                is_edited = msg.get('is_edited', 0)
                is_own = msg['sender_id'] == self.current_user['user_id']
                
                if is_own:
                    self.group_chat_display.insert(tk.END, f"You [{timestamp}]", 'you')
                else:
                    self.group_chat_display.insert(tk.END, f"{sender} [{timestamp}]", 'member')
                
                # Show edited indicator
                if is_edited:
                    self.group_chat_display.insert(tk.END, " (edited)", 'edited')
                
                self.group_chat_display.insert(tk.END, ":\n")
                
                # Display image if present
                if image_path and os.path.exists(image_path):
                    try:
                        # Load and resize image
                        img = Image.open(image_path)
                        img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        # Insert image
                        self.group_chat_display.insert(tk.END, "\n")
                        self.group_chat_display.image_create(tk.END, image=photo)
                        self.group_chat_display.insert(tk.END, "\n")
                        
                        # Keep reference to prevent garbage collection
                        self._group_image_refs.append(photo)
                    except Exception as e:
                        self.group_chat_display.insert(tk.END, f"[Image - Error loading: {str(e)}]\n")
                
                # Display text message
                if text and text != "[Image]":
                    self.group_chat_display.insert(tk.END, f"{text}\n")
                elif not image_path:
                    self.group_chat_display.insert(tk.END, "\n")
                
                # Show reactions
                reactions = self.db.get_message_reactions(message_id, 'group')
                if reactions:
                    reaction_text = " ".join([r['reaction_type'] for r in reactions])
                    self.group_chat_display.insert(tk.END, f"  {reaction_text}\n", 'reactions')
                
                # Mark as read when viewing
                self.db.mark_as_read(message_id, self.current_user['user_id'], 'group')
                
                # Add action buttons
                start_pos = self.group_chat_display.index(tk.END + "-1l")
                if is_own:
                    self.group_chat_display.insert(tk.END, "  [React] [Edit] [Delete] [Forward]\n", 'actions')
                    end_pos = self.group_chat_display.index(tk.END + "-1l")
                    
                    # Use unique tag names for each message
                    react_tag = f"react_btn_{message_id}"
                    edit_tag = f"edit_btn_{message_id}"
                    delete_tag = f"delete_btn_{message_id}"
                    forward_tag = f"forward_btn_{message_id}"
                    
                    def on_react(e, mid=message_id):
                        self.show_reaction_menu(mid, 'group', e.x_root, e.y_root)
                    def on_edit(e, mid=message_id, txt=text):
                        self.edit_message_dialog(mid, txt, 'group')
                    def on_delete(e, mid=message_id):
                        self.delete_message_confirm(mid, 'group')
                    def on_forward(e, mid=message_id):
                        self.forward_message_dialog(mid, 'group')
                    
                    react_start = self.group_chat_display.search("  [React]", start_pos, end_pos)
                    react_end = self.group_chat_display.search("]", react_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(react_tag, react_start, react_end)
                    self.group_chat_display.tag_config(react_tag, foreground='#3498db', underline=True)
                    self.group_chat_display.tag_bind(react_tag, "<Button-1>", on_react)
                    
                    edit_start = self.group_chat_display.search("[Edit]", react_end, end_pos)
                    edit_end = self.group_chat_display.search("]", edit_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(edit_tag, edit_start, edit_end)
                    self.group_chat_display.tag_config(edit_tag, foreground='#2ecc71', underline=True)
                    self.group_chat_display.tag_bind(edit_tag, "<Button-1>", on_edit)
                    
                    delete_start = self.group_chat_display.search("[Delete]", edit_end, end_pos)
                    delete_end = self.group_chat_display.search("]", delete_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(delete_tag, delete_start, delete_end)
                    self.group_chat_display.tag_config(delete_tag, foreground='#e74c3c', underline=True)
                    self.group_chat_display.tag_bind(delete_tag, "<Button-1>", on_delete)
                    
                    forward_start = self.group_chat_display.search("[Forward]", delete_end, end_pos)
                    forward_end = self.group_chat_display.search("]", forward_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(forward_tag, forward_start, forward_end)
                    self.group_chat_display.tag_config(forward_tag, foreground='#9b59b6', underline=True)
                    self.group_chat_display.tag_bind(forward_tag, "<Button-1>", on_forward)
                else:
                    self.group_chat_display.insert(tk.END, "  [React] [Forward]\n", 'actions')
                    end_pos = self.group_chat_display.index(tk.END + "-1l")
                    
                    # Use unique tag names for each message
                    react_tag = f"react_btn_{message_id}"
                    forward_tag = f"forward_btn_{message_id}"
                    
                    def on_react(e, mid=message_id):
                        self.show_reaction_menu(mid, 'group', e.x_root, e.y_root)
                    def on_forward(e, mid=message_id):
                        self.forward_message_dialog(mid, 'group')
                    
                    react_start = self.group_chat_display.search("  [React]", start_pos, end_pos)
                    react_end = self.group_chat_display.search("]", react_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(react_tag, react_start, react_end)
                    self.group_chat_display.tag_config(react_tag, foreground='#3498db', underline=True)
                    self.group_chat_display.tag_bind(react_tag, "<Button-1>", on_react)
                    
                    forward_start = self.group_chat_display.search("[Forward]", react_end, end_pos)
                    forward_end = self.group_chat_display.search("]", forward_start, end_pos) + "+1c"
                    self.group_chat_display.tag_add(forward_tag, forward_start, forward_end)
                    self.group_chat_display.tag_config(forward_tag, foreground='#9b59b6', underline=True)
                    self.group_chat_display.tag_bind(forward_tag, "<Button-1>", on_forward)
                
                self.group_chat_display.insert(tk.END, "\n")
        
        self.group_chat_display.tag_config('you', foreground='#2980b9', font=('Arial', 10, 'bold'))
        self.group_chat_display.tag_config('member', foreground='#8e44ad', font=('Arial', 10, 'bold'))
        self.group_chat_display.tag_config('image_placeholder', foreground='#7f8c8d', font=('Arial', 9, 'italic'))
        self.group_chat_display.tag_config('edited', foreground='#95a5a6', font=('Arial', 8, 'italic'))
        self.group_chat_display.tag_config('reactions', font=('Arial', 12))
        self.group_chat_display.config(state='disabled')
        self.group_chat_display.see(tk.END)
    
    def upload_image_dm(self):
        """Upload an image for direct message"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a friend to chat with")
            return
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Copy image to storage folder
            image_path = self.save_image(file_path)
            if image_path:
                # Send image message
                success, msg, msg_id, streak_count = self.db.send_message(
                    self.current_user['user_id'],
                    self.selected_user['user_id'],
                    "[Image]",
                    image_path
                )
                
                if success:
                    # Mark as read for sender
                    if msg_id:
                        self.db.mark_as_read(msg_id, self.current_user['user_id'], 'direct')
                    self.load_dm_conversation()
                    
                    # Update streak display
                    if streak_count > 0:
                        self.dm_streak_label.config(text=f"🔥 {streak_count} day streak!")
                        self.root.after(3000, lambda: self.dm_streak_label.config(text=""))
                    
                    self.update_streak_display()
                else:
                    messagebox.showerror("Error", msg if msg else "Failed to send image")
    
    def upload_image_group(self):
        """Upload an image for group message"""
        if not self.selected_group:
            messagebox.showwarning("Warning", "Please select a group to chat with")
            return
        
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Copy image to storage folder
            image_path = self.save_image(file_path)
            if image_path:
                # Send image message
                success = self.db.send_group_message(
                    self.selected_group['group_id'],
                    self.current_user['user_id'],
                    "[Image]",
                    image_path
                )
                
                if success:
                    self.load_group_conversation()
                else:
                    messagebox.showerror("Error", "Failed to send image")
    
    def save_image(self, source_path):
        """Copy image to storage folder and return the relative path"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            filename = os.path.basename(source_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{timestamp}_{name}{ext}"
            dest_path = os.path.join(self.images_dir, new_filename)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            # Return relative path
            return dest_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {str(e)}")
            return None
    
    def send_direct_message(self):
        """Send a direct message to selected user"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a friend to chat with")
            return
        
        message_text = self.dm_message_entry.get().strip()
        
        if not message_text:
            return
        
        success, msg, msg_id, streak_count = self.db.send_message(self.current_user['user_id'],
                                      self.selected_user['user_id'],
                                      message_text)
        
        if success:
            # Mark as read for sender
            if msg_id:
                self.db.mark_as_read(msg_id, self.current_user['user_id'], 'direct')
            self.dm_message_entry.delete(0, tk.END)
            self.load_dm_conversation()
            
            # Update streak display
            if streak_count > 0:
                self.dm_streak_label.config(text=f"🔥 {streak_count} day streak!")
                # Clear after 3 seconds
                self.root.after(3000, lambda: self.dm_streak_label.config(text=""))
            
            # Update streak display
            self.update_streak_display()
        else:
            messagebox.showerror("Error", msg if msg else "Failed to send message")
    
    def send_group_message(self):
        """Send a message to the selected group"""
        if not self.selected_group:
            messagebox.showwarning("Warning", "Please select a group to chat with")
            return
        
        message_text = self.group_message_entry.get().strip()
        
        if not message_text:
            return
        
        success = self.db.send_group_message(self.selected_group['group_id'],
                                            self.current_user['user_id'],
                                            message_text)
        
        if success:
            self.group_message_entry.delete(0, tk.END)
            self.load_group_conversation()
        else:
            messagebox.showerror("Error", "Failed to send message")
    
    def view_user_profile(self):
        """View selected user's profile"""
        if not self.selected_user:
            return
        
        user = self.db.get_user_by_id(self.selected_user['user_id'])
        if not user:
            messagebox.showerror("Error", "Could not load user profile")
            return
        
        # Create profile window
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"{user.get('display_name') or user['username']}'s Profile")
        profile_window.geometry("450x500")
        profile_window.configure(bg='#ecf0f1')
        
        # Profile header
        header = tk.Frame(profile_window, bg='#3498db', height=100)
        header.pack(fill='x')
        
        display_name = user.get('display_name') or user['username']
        tk.Label(header, text=display_name, font=('Arial', 24, 'bold'),
                bg='#3498db', fg='white').pack(pady=30)
        
        # Profile content
        content = tk.Frame(profile_window, bg='#ecf0f1', padx=30, pady=20)
        content.pack(fill='both', expand=True)
        
        # Username
        info_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=10)
        
        tk.Label(info_frame, text="Username", font=('Arial', 10, 'bold'),
                bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
        tk.Label(info_frame, text=user['username'], font=('Arial', 12),
                bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # Date of Birth
        if user.get('date_of_birth'):
            dob_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
            dob_frame.pack(fill='x', pady=10)
            
            tk.Label(dob_frame, text="Date of Birth", font=('Arial', 10, 'bold'),
                    bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
            tk.Label(dob_frame, text=str(user['date_of_birth']), font=('Arial', 12),
                    bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # Country
        if user.get('country'):
            country_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
            country_frame.pack(fill='x', pady=10)
            
            tk.Label(country_frame, text="Country", font=('Arial', 10, 'bold'),
                    bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
            tk.Label(country_frame, text=user['country'], font=('Arial', 12),
                    bg='white', anchor='w').pack(fill='x', padx=10, pady=8)
        
        # Bio
        if user.get('bio'):
            bio_frame = tk.Frame(content, bg='white', relief='solid', borderwidth=1)
            bio_frame.pack(fill='x', pady=10)
            
            tk.Label(bio_frame, text="Bio", font=('Arial', 10, 'bold'),
                    bg='#95a5a6', fg='white', anchor='w').pack(fill='x', padx=2, pady=2)
            
            bio_text = tk.Text(bio_frame, font=('Arial', 11), bg='white', 
                             height=5, wrap=tk.WORD, relief='flat')
            bio_text.insert('1.0', user['bio'])
            bio_text.config(state='disabled')
            bio_text.pack(fill='x', padx=10, pady=8)
        
        # Action buttons
        btn_frame = tk.Frame(profile_window, bg='#ecf0f1')
        btn_frame.pack(pady=15)
        
        # Check if already blocked
        is_blocked = self.db.is_blocked(self.current_user['user_id'], user['user_id'])
        is_friend = self.db.are_friends(self.current_user['user_id'], user['user_id'])
        
        # Block/Unblock button
        if is_blocked:
            def unblock():
                if messagebox.askyesno("Confirm", f"Unblock {display_name}?", parent=profile_window):
                    success = self.db.unblock_user(self.current_user['user_id'], user['user_id'])
                    if success:
                        messagebox.showinfo("Success", f"{display_name} has been unblocked", parent=profile_window)
                        profile_window.destroy()
                    else:
                        messagebox.showerror("Error", "Failed to unblock user", parent=profile_window)
            
            tk.Button(btn_frame, text="🔓 Unblock", font=('Arial', 11, 'bold'),
                     bg='#3498db', fg='white', command=unblock,
                     cursor='hand2', width=15).pack(side='left', padx=5)
        else:
            def block():
                if messagebox.askyesno("Confirm", f"Block {display_name}? This will remove them from your friends list and delete all messages.", parent=profile_window):
                    success, msg = self.db.block_user(self.current_user['user_id'], user['username'])
                    if success:
                        messagebox.showinfo("Success", msg, parent=profile_window)
                        profile_window.destroy()
                        self.create_chat_screen()  # Refresh
                    else:
                        messagebox.showerror("Error", msg, parent=profile_window)
            
            tk.Button(btn_frame, text="🚫 Block", font=('Arial', 11, 'bold'),
                     bg='#e74c3c', fg='white', command=block,
                     cursor='hand2', width=15).pack(side='left', padx=5)
        
        # Remove friend button
        if is_friend:
            def remove_friend():
                if messagebox.askyesno("Confirm", f"Remove {display_name} from your friends?", parent=profile_window):
                    success = self.db.remove_friendship(self.current_user['user_id'], user['user_id'])
                    if success:
                        messagebox.showinfo("Success", f"{display_name} has been removed from your friends", parent=profile_window)
                        profile_window.destroy()
                        self.create_chat_screen()  # Refresh
                    else:
                        messagebox.showerror("Error", "Failed to remove friend", parent=profile_window)
            
            tk.Button(btn_frame, text="👋 Remove Friend", font=('Arial', 11, 'bold'),
                     bg='#e67e22', fg='white', command=remove_friend,
                     cursor='hand2', width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Close", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=profile_window.destroy,
                 cursor='hand2', width=15).pack(side='left', padx=5)
    
    def open_settings(self):
        """Open settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Profile Settings")
        settings_window.geometry("600x700")
        settings_window.configure(bg='#ecf0f1')
        
        # Get current user info
        user = self.db.get_user_by_id(self.current_user['user_id'])
        
        # Title
        tk.Label(settings_window, text="⚙️ Profile Settings", font=('Arial', 18, 'bold'),
                bg='#ecf0f1').pack(pady=20)
        
        # Settings frame
        settings_frame = tk.Frame(settings_window, bg='#ecf0f1')
        settings_frame.pack(padx=30, pady=10, fill='both', expand=True)
        
        # Display Name
        tk.Label(settings_frame, text="Display Name:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=10)
        display_name_entry = tk.Entry(settings_frame, font=('Arial', 11), width=30)
        display_name_entry.insert(0, user.get('display_name') or user['username'])
        display_name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Date of Birth
        tk.Label(settings_frame, text="Date of Birth:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=10)
        dob_entry = tk.Entry(settings_frame, font=('Arial', 11), width=30)
        if user.get('date_of_birth'):
            dob_entry.insert(0, str(user['date_of_birth']))
        dob_entry.grid(row=1, column=1, pady=10, padx=10)
        tk.Label(settings_frame, text="(Format: YYYY-MM-DD)", font=('Arial', 9),
                bg='#ecf0f1', fg='gray').grid(row=2, column=1, sticky='w', padx=10)
        
        # Country
        tk.Label(settings_frame, text="Country:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=3, column=0, sticky='w', pady=10)
        country_entry = tk.Entry(settings_frame, font=('Arial', 11), width=30)
        if user.get('country'):
            country_entry.insert(0, user['country'])
        country_entry.grid(row=3, column=1, pady=10, padx=10)
        
        # Bio
        tk.Label(settings_frame, text="Bio:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=4, column=0, sticky='nw', pady=10)
        bio_text = tk.Text(settings_frame, font=('Arial', 10), width=30, height=4)
        if user.get('bio'):
            bio_text.insert('1.0', user['bio'])
        bio_text.grid(row=4, column=1, pady=10, padx=10)
        
        # Save profile button
        def save_profile():
            display_name = display_name_entry.get().strip()
            dob = dob_entry.get().strip() or None
            country = country_entry.get().strip() or None
            bio = bio_text.get('1.0', tk.END).strip() or None
            
            if not display_name:
                messagebox.showerror("Error", "Display name cannot be empty", parent=settings_window)
                return
            
            success = self.db.update_profile(self.current_user['user_id'], 
                                           display_name, dob, country, bio)
            
            if success:
                messagebox.showinfo("Success", "Profile updated successfully!", parent=settings_window)
                self.current_user['display_name'] = display_name
                self.create_chat_screen()  # Refresh to show new display name
                settings_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to update profile", parent=settings_window)
        
        tk.Button(settings_frame, text="💾 Save Profile", font=('Arial', 12, 'bold'),
                 bg='#3498db', fg='white', command=save_profile, 
                 cursor='hand2', width=20).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Change Password Section
        tk.Label(settings_window, text="🔒 Change Password", font=('Arial', 14, 'bold'),
                bg='#ecf0f1').pack(pady=(20, 10))
        
        password_frame = tk.Frame(settings_window, bg='#ecf0f1')
        password_frame.pack(padx=30, pady=10)
        
        tk.Label(password_frame, text="New Password:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=0, column=0, sticky='w', pady=5)
        new_password_entry = tk.Entry(password_frame, font=('Arial', 11), width=30, show='*')
        new_password_entry.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(password_frame, text="Confirm Password:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').grid(row=1, column=0, sticky='w', pady=5)
        confirm_password_entry = tk.Entry(password_frame, font=('Arial', 11), width=30, show='*')
        confirm_password_entry.grid(row=1, column=1, pady=5, padx=10)
        
        def change_password():
            new_pass = new_password_entry.get()
            confirm_pass = confirm_password_entry.get()
            
            if not new_pass:
                messagebox.showerror("Error", "Password cannot be empty", parent=settings_window)
                return
            
            if new_pass != confirm_pass:
                messagebox.showerror("Error", "Passwords do not match", parent=settings_window)
                return
            
            success = self.db.change_password(self.current_user['user_id'], new_pass)
            
            if success:
                messagebox.showinfo("Success", "Password changed successfully!", parent=settings_window)
                new_password_entry.delete(0, tk.END)
                confirm_password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to change password", parent=settings_window)
        
        tk.Button(password_frame, text="🔑 Change Password", font=('Arial', 11, 'bold'),
                 bg='#e67e22', fg='white', command=change_password, 
                 cursor='hand2', width=20).grid(row=2, column=0, columnspan=2, pady=15)
        
        # Blocklist Section
        tk.Label(settings_window, text="🚫 Blocked Users", font=('Arial', 14, 'bold'),
                bg='#ecf0f1').pack(pady=(20, 10))
        
        blocklist_frame = tk.Frame(settings_window, bg='#ecf0f1')
        blocklist_frame.pack(padx=30, pady=10, fill='both', expand=True)
        
        blocked_users = self.db.get_blocked_users(self.current_user['user_id'])
        
        if blocked_users:
            canvas = tk.Canvas(blocklist_frame, bg='#ecf0f1', height=150)
            scrollbar = tk.Scrollbar(blocklist_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for blocked in blocked_users:
                user_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', 
                                     borderwidth=1, padx=10, pady=5)
                user_frame.pack(fill='x', padx=5, pady=3)
                
                blocked_name = blocked.get('display_name') or blocked['username']
                tk.Label(user_frame, text=blocked_name, font=('Arial', 10),
                        bg='white').pack(side='left', padx=5)
                tk.Label(user_frame, text=f"@{blocked['username']}", font=('Arial', 9),
                        bg='white', fg='gray').pack(side='left', padx=5)
                
                def unblock(b_id=blocked['blocked_id'], b_name=blocked_name):
                    success = self.db.unblock_user(self.current_user['user_id'], b_id)
                    if success:
                        messagebox.showinfo("Success", f"{b_name} has been unblocked", parent=settings_window)
                        settings_window.destroy()
                        self.open_settings()  # Refresh
                    else:
                        messagebox.showerror("Error", "Failed to unblock user", parent=settings_window)
                
                tk.Button(user_frame, text="Unblock", font=('Arial', 9),
                         bg='#3498db', fg='white', command=unblock,
                         cursor='hand2', width=8).pack(side='right', padx=5)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            tk.Label(blocklist_frame, text="No blocked users", font=('Arial', 10),
                    bg='#ecf0f1', fg='gray').pack(pady=20)
    
    # ============= EMOJI PICKER =============
    
    def show_emoji_picker_dm(self):
        """Show emoji picker for direct messages"""
        self.show_emoji_picker(self.dm_message_entry)
    
    def show_emoji_picker_group(self):
        """Show emoji picker for group messages"""
        self.show_emoji_picker(self.group_message_entry)
    
    def show_emoji_picker(self, entry_widget):
        """Show emoji picker window"""
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Emoji Picker")
        emoji_window.geometry("400x300")
        emoji_window.configure(bg='#ecf0f1')
        emoji_window.transient(self.root)
        
        # Common emojis
        emojis = [
            '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇',
            '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
            '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩',
            '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '😣', '😖',
            '😫', '😩', '🥺', '😢', '😭', '😤', '😠', '😡', '🤬', '🤯',
            '😳', '🥵', '🥶', '😱', '😨', '😰', '😥', '😓', '🤗', '🤔',
            '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😦',
            '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴',
            '🤢', '🤮', '🤧', '😷', '🤒', '🤕', '🤑', '🤠', '😈', '👿',
            '👹', '👺', '🤡', '💩', '👻', '💀', '☠️', '👽', '👾', '🤖',
            '👍', '👎', '👊', '✊', '🤛', '🤜', '🤞', '✌️', '🤟', '🤘',
            '👌', '🤏', '👈', '👉', '👆', '👇', '☝️', '👍', '👋', '🤚',
            '🖐', '✋', '🖖', '👏', '🙌', '🤲', '🤝', '🙏', '✍️', '💪',
            '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔',
            '❣️', '💕', '💞', '💓', '💗', '💖', '💘', '💝', '💟', '☮️',
            '✝️', '☪️', '🕉', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐',
            '⛎', '♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐',
            '♑', '♒', '♓', '🆔', '⚛️', '🉑', '☢️', '☣️', '📴', '📳',
            '🈶', '🈚', '🈸', '🈺', '🈷️', '✴️', '🆚', '💮', '🉐', '㊙️',
            '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️',
            '🆘', '❌', '⭕', '🛑', '⛔', '📛', '🚫', '💯', '💢', '♨️',
            '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭', '❗', '❓', '❕',
            '❔', '‼️', '⁉️', '🔅', '🔆', '〽️', '⚠️', '🚸', '🔱', '⚜️',
            '🔰', '♻️', '✅', '🈯', '💹', '❇️', '✳️', '❎', '🌐', '💠',
            'Ⓜ️', '🌀', '💤', '🏧', '🚾', '♿', '🅿️', '🈳', '🈂️', '🛂',
            '🛃', '🛄', '🛅', '🚹', '🚺', '🚼', '🚻', '🚮', '🎦', '📶',
            '🈁', '🔣', 'ℹ️', '🔤', '🔡', '🔠', '🔢', '🔟', '🔢', '🔢'
        ]
        
        # Create scrollable frame
        canvas = tk.Canvas(emoji_window, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(emoji_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add emoji buttons in grid
        row, col = 0, 0
        for emoji in emojis:
            btn = tk.Button(scrollable_frame, text=emoji, font=('Arial', 16),
                          bg='white', command=lambda e=emoji: self.insert_emoji(entry_widget, e, emoji_window),
                          cursor='hand2', width=3, height=1)
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 9:
                col = 0
                row += 1
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    def insert_emoji(self, entry_widget, emoji, window):
        """Insert emoji into entry widget"""
        current_text = entry_widget.get()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, current_text + emoji)
        window.destroy()
    
    # ============= MESSAGE SEARCH =============
    
    def search_dm_messages(self):
        """Search messages in direct chat"""
        if not self.selected_user:
            messagebox.showwarning("Warning", "Please select a friend to search")
            return
        
        query = self.dm_search_entry.get().strip()
        if not query or query == "Search messages...":
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        results = self.db.search_messages(self.current_user['user_id'], query, 
                                         chat_with_id=self.selected_user['user_id'])
        
        if not results:
            messagebox.showinfo("Search Results", "No messages found")
            return
        
        # Show search results
        self.show_search_results(results, "Direct Messages")
    
    def search_group_messages(self):
        """Search messages in group chat"""
        if not self.selected_group:
            messagebox.showwarning("Warning", "Please select a group to search")
            return
        
        query = self.group_search_entry.get().strip()
        if not query or query == "Search messages...":
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        results = self.db.search_messages(self.current_user['user_id'], query, 
                                         group_id=self.selected_group['group_id'])
        
        if not results:
            messagebox.showinfo("Search Results", "No messages found")
            return
        
        # Show search results
        self.show_search_results(results, "Group Messages")
    
    def show_search_results(self, results, title):
        """Display search results in a window"""
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Search Results - {title}")
        result_window.geometry("600x500")
        result_window.configure(bg='#ecf0f1')
        
        tk.Label(result_window, text=f"Found {len(results)} message(s)", 
                font=('Arial', 14, 'bold'), bg='#ecf0f1').pack(pady=10)
        
        # Scrollable results
        canvas = tk.Canvas(result_window, bg='#ecf0f1')
        scrollbar = tk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for msg in results:
            msg_frame = tk.Frame(scrollable_frame, bg='white', relief='solid', 
                                borderwidth=1, padx=10, pady=5)
            msg_frame.pack(fill='x', padx=10, pady=5)
            
            sender = msg['sender_name']
            timestamp = msg['sent_at'].strftime('%Y-%m-%d %I:%M %p')
            text = msg['message_text']
            
            tk.Label(msg_frame, text=f"{sender} - {timestamp}", 
                    font=('Arial', 10, 'bold'), bg='white').pack(anchor='w')
            tk.Label(msg_frame, text=text, font=('Arial', 10), 
                    bg='white', wraplength=550, justify='left').pack(anchor='w', pady=2)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
    
    # ============= MESSAGE REACTIONS =============
    
    def show_reaction_menu(self, message_id, message_type='direct', x=0, y=0):
        """Show reaction menu for a message"""
        reaction_window = tk.Toplevel(self.root)
        reaction_window.overrideredirect(True)
        reaction_window.geometry(f"+{x}+{y}")
        reaction_window.configure(bg='white')
        
        reactions = ['❤️', '👍', '👎', '😂', '😮', '😢', '🔥']
        
        for reaction in reactions:
            btn = tk.Button(reaction_window, text=reaction, font=('Arial', 16),
                          bg='white', command=lambda r=reaction: self.add_reaction_to_message(
                              message_id, r, message_type, reaction_window),
                          cursor='hand2', width=3)
            btn.pack(side='left', padx=2)
    
    def add_reaction_to_message(self, message_id, reaction_type, message_type, window):
        """Add reaction to a message"""
        self.db.add_reaction(message_id, self.current_user['user_id'], reaction_type, message_type)
        window.destroy()
        # Reload conversation to show reactions
        if message_type == 'direct':
            self.load_dm_conversation()
        else:
            self.load_group_conversation()
    
    # ============= MESSAGE EDITING/DELETING =============
    
    def edit_message_dialog(self, message_id, current_text, message_type='direct'):
        """Show dialog to edit a message"""
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Message")
        edit_window.geometry("400x200")
        edit_window.configure(bg='#ecf0f1')
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        tk.Label(edit_window, text="Edit your message:", font=('Arial', 12, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        text_entry = tk.Text(edit_window, font=('Arial', 11), width=40, height=5)
        text_entry.pack(padx=20, pady=10)
        text_entry.insert('1.0', current_text)
        text_entry.focus()
        
        def save_edit():
            new_text = text_entry.get('1.0', tk.END).strip()
            if not new_text:
                messagebox.showwarning("Warning", "Message cannot be empty", parent=edit_window)
                return
            
            success = self.db.edit_message(message_id, new_text, message_type)
            if success:
                messagebox.showinfo("Success", "Message edited successfully!", parent=edit_window)
                edit_window.destroy()
                # Reload conversation
                if message_type == 'direct':
                    self.load_dm_conversation()
                else:
                    self.load_group_conversation()
            else:
                messagebox.showerror("Error", "Failed to edit message", parent=edit_window)
        
        btn_frame = tk.Frame(edit_window, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Save", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=save_edit,
                 cursor='hand2', width=10).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=edit_window.destroy,
                 cursor='hand2', width=10).pack(side='left', padx=5)
    
    def delete_message_confirm(self, message_id, message_type='direct'):
        """Confirm and delete a message"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this message?"):
            success = self.db.delete_message(message_id, message_type)
            if success:
                messagebox.showinfo("Success", "Message deleted")
                # Reload conversation
                if message_type == 'direct':
                    self.load_dm_conversation()
                else:
                    self.load_group_conversation()
            else:
                messagebox.showerror("Error", "Failed to delete message")
    
    # ============= MESSAGE FORWARDING =============
    
    def forward_message_dialog(self, message_id, message_type='direct'):
        """Show dialog to forward a message"""
        forward_window = tk.Toplevel(self.root)
        forward_window.title("Forward Message")
        forward_window.geometry("400x500")
        forward_window.configure(bg='#ecf0f1')
        forward_window.transient(self.root)
        forward_window.grab_set()
        
        tk.Label(forward_window, text="Forward to:", font=('Arial', 14, 'bold'),
                bg='#ecf0f1').pack(pady=10)
        
        # Friends list
        friends_frame = tk.Frame(forward_window, bg='#ecf0f1')
        friends_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        tk.Label(friends_frame, text="Friends:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').pack(anchor='w')
        
        friends_listbox = tk.Listbox(friends_frame, font=('Arial', 11), height=8)
        friends_listbox.pack(fill='both', expand=True, pady=5)
        
        friends = self.db.get_friends(self.current_user['user_id'])
        for friend in friends:
            display_name = friend.get('display_name') or friend['username']
            friends_listbox.insert(tk.END, f"{display_name} (Direct)")
        
        # Groups list
        tk.Label(friends_frame, text="Groups:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').pack(anchor='w', pady=(10, 0))
        
        groups_listbox = tk.Listbox(friends_frame, font=('Arial', 11), height=8)
        groups_listbox.pack(fill='both', expand=True, pady=5)
        
        groups = self.db.get_user_groups(self.current_user['user_id'])
        for group in groups:
            groups_listbox.insert(tk.END, f"{group['group_name']} (Group)")
        
        def forward():
            # Check which list has selection
            friend_selection = friends_listbox.curselection()
            group_selection = groups_listbox.curselection()
            
            if friend_selection:
                friend = friends[friend_selection[0]]
                success, msg = self.db.forward_message(message_id, self.current_user['user_id'],
                                                      friend['user_id'], message_type, 'direct')
                if success:
                    messagebox.showinfo("Success", "Message forwarded!", parent=forward_window)
                    forward_window.destroy()
                else:
                    messagebox.showerror("Error", msg, parent=forward_window)
            elif group_selection:
                group = groups[group_selection[0]]
                success, msg = self.db.forward_message(message_id, self.current_user['user_id'],
                                                      group['group_id'], message_type, 'group')
                if success:
                    messagebox.showinfo("Success", "Message forwarded!", parent=forward_window)
                    forward_window.destroy()
                    # Reload group conversation if it's the selected group
                    if self.selected_group and self.selected_group['group_id'] == group['group_id']:
                        self.load_group_conversation()
                else:
                    messagebox.showerror("Error", msg, parent=forward_window)
            else:
                messagebox.showwarning("Warning", "Please select a friend or group", parent=forward_window)
        
        btn_frame = tk.Frame(forward_window, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Forward", font=('Arial', 11, 'bold'),
                 bg='#2ecc71', fg='white', command=forward,
                 cursor='hand2', width=10).pack(side='left', padx=5)
        
        tk.Button(btn_frame, text="Cancel", font=('Arial', 11, 'bold'),
                 bg='#95a5a6', fg='white', command=forward_window.destroy,
                 cursor='hand2', width=10).pack(side='left', padx=5)
    
    # ============= CLEAR CHAT =============
    
    def clear_dm_chat(self):
        """Clear direct message conversation"""
        if not self.selected_user:
            return
        
        if messagebox.askyesno("Confirm Clear Chat", 
                              "Are you sure you want to clear all messages in this conversation? This cannot be undone."):
            success = self.db.clear_conversation(self.current_user['user_id'], 
                                                self.selected_user['user_id'])
            if success:
                messagebox.showinfo("Success", "Chat cleared successfully")
                self.load_dm_conversation()
            else:
                messagebox.showerror("Error", "Failed to clear chat")
    
    def clear_group_chat(self):
        """Clear group chat conversation"""
        if not self.selected_group:
            return
        
        if messagebox.askyesno("Confirm Clear Chat", 
                              "Are you sure you want to clear all messages in this group? This cannot be undone."):
            success = self.db.clear_group_chat(self.selected_group['group_id'])
            if success:
                messagebox.showinfo("Success", "Group chat cleared successfully")
                self.load_group_conversation()
            else:
                messagebox.showerror("Error", "Failed to clear chat")
    
    def clear_screen(self):
        """Clear all widgets from screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    app.run()