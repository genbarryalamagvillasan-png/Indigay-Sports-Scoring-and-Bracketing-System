import tkinter as tk
import os
import customtkinter
from admindash.sportselect import SportSelection
from admindash.admindashboard import AdminDashboard
from studentdash.sportselect import SportSelect
from studentdash.studentdashboard import StudentDashboard
from authActivity.backend.UserAccount import UserAccount, COLLEGES, SCHOOL_DOMAIN, make_username
from PIL import Image, ImageTk

class Auth(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.user = UserAccount()
        self.role = "student"
        self.pack(fill="both", expand=True)
        self.configure(bg="#191a20")


        self.logo_photo = None
        project_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        logo_path = os.path.join(project_folder, "images", "logo.png")

        if os.path.exists(logo_path):
            try:
                logo_image = Image.open(logo_path)
                logo_image.thumbnail((150, 150))
                self.logo_photo = ImageTk.PhotoImage(logo_image)
            except Exception:
                self.logo_photo = None

        self.bg_label = tk.Label(self, bg="#191a20")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_label.lower()

        self.notif_label = customtkinter.CTkLabel(
            self,
            text="",
            fg_color="#0866ff",
            bg_color="#191a20",
            text_color="#ffffff",
            font=("Arial", 16),
            height=50,
            padx=35,
            corner_radius=25
        )
        self.notif_label.place_forget()
        self.notif_timer = None

        self.current_frame = None
        self.show_login()

    def eye_button(self, parent, entry):
        def toggle_password():
            if eye.cget("text_color") == "#888888":
                entry.configure(show="")
                eye.configure(text_color="#111111")
            else:
                entry.configure(show="*")
                eye.configure(text_color="#888888")

        eye = customtkinter.CTkButton(
            parent, text="\U0001F441", width=30, height=26,
            fg_color="#ffffff", hover_color="#ffffff", text_color="#888888",
            border_width=0, corner_radius=0,
            font=("Segoe UI Emoji", 14),
            command=toggle_password
        )
        eye.place(in_=entry, relx=1.0, x=-6, rely=0.5, anchor="e")

    def show_notif(self, message, color="blue"):
        if message:
            if color == "red":
                notifcolor = "#ab001d"
            else:
                notifcolor = "#00358b"

            self.notif_label.place(relx=0.5, y=40, anchor="n")
            self.notif_label.configure(text=message, fg_color=notifcolor)
            self.notif_label.lift()

            if self.notif_timer is not None:
                self.after_cancel(self.notif_timer)
            self.notif_timer = self.after(3000, self.clear_notif)
        else:
            self.clear_notif()

    def clear_notif(self):
        self.notif_label.place_forget()


    def clear_frame(self):
        if hasattr(self, "current_frame") and self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def switch_to_register(self, event=None):
        self.show_register()

    def switch_to_login(self, event=None):
        self.show_login()

    def switch_to_password(self, event=None):
        self.show_password()


    def handle_password(self):
        username = self.username_entry.get()
        newpass = self.newpass_entry.get()
        confirmpass = self.confirmpass_entry.get()
        message = self.user.password(username, newpass, confirmpass)

        if message == "Password changed successfully!":
            self.show_notif(message, "blue")
            self.show_login()
        else:
            self.show_notif(message, "red")


    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        message = self.user.login(username, password, self.role)

        if message == "Login successful!":
            self.show_notif(message, "blue")
            if self.role == "admin":
                self.show_sportselection()
            else:
                self.show_studentsports()
        else:
            self.show_notif(message, "red")

    def handle_register(self):
        firstname = self.firstname_entry.get()
        middlename = self.middlename_entry.get()
        lastname = self.lastname_entry.get()
        password = self.password_entry.get()
        confirmpass = self.confirmpass_entry.get()
        college = self.college_menu.get()
        message = self.user.register(firstname, middlename, lastname,
                                     password, confirmpass, college)

        if message == "Registration successful!":
            username = make_username(firstname, middlename, lastname)
            self.show_login()
            self.username_entry.insert(0, username)
            self.show_notif("Registration successful! Your username is " + username, "blue")
        else:
            self.show_notif(message, "red")

    def update_username_preview(self, event=None):
        firstname = self.firstname_entry.get()
        middlename = self.middlename_entry.get()
        lastname = self.lastname_entry.get()
        username = make_username(firstname, middlename, lastname)

        if username == "":
            username = "namemiddlename.lastname" + SCHOOL_DOMAIN

        self.username_preview.configure(text=username)

    def adminlogin(self):
        self.role = "admin"
        self.show_login()

    def studentlogin(self):
        self.role = "student"
        self.show_login()

    def show_login(self):
        self.clear_frame()

        mainFrame = tk.Frame(self, bg="#111111", width=430, height=550,
                             highlightbackground="#444444", highlightthickness=1)
        mainFrame.place(relx=0.5, rely=0.5, anchor="center")
        mainFrame.pack_propagate(False)

        if self.logo_photo:
            tk.Label(mainFrame, image=self.logo_photo, bg="#111111").pack(pady=(18, 10))

        rolebuttons = tk.Frame(mainFrame, bg="#111111")
        rolebuttons.pack(fill="x", padx=35, pady=(0, 14))

        if self.role == "admin":
            admincolor = "#ffffff"
            adminhover = "#d9d9d9"
            admintext = "#111111"
            studentcolor = "#111111"
            studenthover = "#292929"
            studenttext = "#ffffff"
        else:
            admincolor = "#111111"
            adminhover = "#292929"
            admintext = "#ffffff"
            studentcolor = "#ffffff"
            studenthover = "#d9d9d9"
            studenttext = "#111111"

        customtkinter.CTkButton(
            rolebuttons, text="Admin", command=self.adminlogin,
            fg_color=admincolor, hover_color=adminhover, text_color=admintext,
            border_color="#777777", border_width=1, corner_radius=8, height=36,
            font=("Arial", 13, "bold")
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        customtkinter.CTkButton(
            rolebuttons, text="Student", command=self.studentlogin,
            fg_color=studentcolor, hover_color=studenthover, text_color=studenttext,
            border_color="#777777", border_width=1, corner_radius=8, height=36,
            font=("Arial", 13, "bold")
        ).pack(side="left", expand=True, fill="x", padx=(5, 0))

        if self.role == "admin":
            logintitle = "Admin Login"
        else:
            logintitle = "Student Login"

        tk.Label(mainFrame, text=logintitle, bg="#111111",
                 font=("Arial", 23, "bold"), fg="#ffffff").pack(pady=(0, 6))
        tk.Label(mainFrame, text="Enter your account details", bg="#111111",
                 font=("Arial", 10), fg="#bdbdbd").pack(pady=(0, 20))

        tk.Label(mainFrame, text="Username", bg="#111111",
                 font=("Arial", 10, "bold"), fg="#ffffff", anchor="w").pack(
                     fill="x", padx=35, pady=(0, 5))
        if self.role == "student":
            username_hint = "namemiddlename.lastname" + SCHOOL_DOMAIN
        else:
            username_hint = "Enter username"

        self.username_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text=username_hint,
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=42, corner_radius=7
        )
        self.username_entry.pack(fill="x", padx=35, pady=(0, 14))

        tk.Label(mainFrame, text="Password", bg="#111111",
                 font=("Arial", 10, "bold"), fg="#ffffff", anchor="w").pack(
                     fill="x", padx=35, pady=(0, 5))
        self.password_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Enter password", show="*",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=42, corner_radius=7
        )
        self.password_entry.pack(fill="x", padx=35, pady=(0, 8))
        self.eye_button(mainFrame, self.password_entry)

        if self.role == "student":
            forgotpass = tk.Label(mainFrame, text="Forgot Password?",
                                  fg="#d0d0d0", font=("Arial", 9),
                                  cursor="hand2", bg="#111111")
            forgotpass.pack(anchor="e", padx=35, pady=(0, 12))
            forgotpass.bind("<Button-1>", self.switch_to_password)

        customtkinter.CTkButton(
            mainFrame, command=self.handle_login, text="Sign In",
            fg_color="#ffffff", hover_color="#d9d9d9", text_color="#111111",
            cursor="hand2", height=42, corner_radius=7,
            font=("Arial", 13, "bold")
        ).pack(fill="x", padx=35, pady=(8, 12))

        if self.role == "student":
            signup = tk.Frame(mainFrame, bg="#111111")
            signup.pack(pady=(0, 4))
            tk.Label(signup, text="Don't have an account? ", bg="#111111",
                     fg="#bdbdbd", font=("Arial", 9)).pack(side="left")
            signuplabel = tk.Label(signup, text="Register", bg="#111111",
                                   fg="#ffffff", font=("Arial", 9, "bold"),
                                   cursor="hand2")
            signuplabel.pack(side="left")
            signuplabel.bind("<Button-1>", self.switch_to_register)

        self.current_frame = mainFrame

    def show_password(self):
        self.clear_frame()

        mainFrame = tk.Frame(self, bg="#111111", width=430, height=540,
                             highlightbackground="#444444", highlightthickness=1)
        mainFrame.place(relx=0.5, rely=0.5, anchor="center")
        mainFrame.pack_propagate(False)

        if self.logo_photo:
            tk.Label(mainFrame, image=self.logo_photo, bg="#111111").pack(pady=(20, 6))

        tk.Label(mainFrame, text="Forgot Password", bg="#111111",
                 font=("Arial", 22, "bold"), fg="#ffffff").pack(pady=(0, 5))
        tk.Label(mainFrame, text="Create a new password", bg="#111111",
                 font=("Arial", 10), fg="#bdbdbd").pack(pady=(0, 18))

        tk.Label(mainFrame, text="Username", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 5))
        self.username_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="name.lastname" + SCHOOL_DOMAIN, font=("Arial", 13),
            text_color="#111111", fg_color="#ffffff", border_color="#d0d0d0",
            border_width=1, height=42, corner_radius=7
        )
        self.username_entry.pack(fill="x", padx=35, pady=(0, 12))

        tk.Label(mainFrame, text="New Password", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 5))
        self.newpass_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Enter new password", show="*",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=42, corner_radius=7
        )
        self.newpass_entry.pack(fill="x", padx=35, pady=(0, 12))
        self.eye_button(mainFrame, self.newpass_entry)

        tk.Label(mainFrame, text="Confirm Password", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 5))
        self.confirmpass_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Confirm new password", show="*",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=42, corner_radius=7
        )
        self.confirmpass_entry.pack(fill="x", padx=35, pady=(0, 14))
        self.eye_button(mainFrame, self.confirmpass_entry)

        customtkinter.CTkButton(
            mainFrame, command=self.handle_password, text="Change Password",
            fg_color="#ffffff", hover_color="#d9d9d9", text_color="#111111",
            cursor="hand2", height=42, corner_radius=7,
            font=("Arial", 12, "bold")
        ).pack(fill="x", padx=35, pady=(0, 8))

        backtologin = tk.Label(mainFrame, text="← Back to login", bg="#111111",
                               fg="#bdbdbd", font=("Arial", 9), cursor="hand2")
        backtologin.pack(pady=(8, 0))
        backtologin.bind("<Button-1>", self.switch_to_login)

        self.current_frame = mainFrame

    def show_register(self):
        self.clear_frame()

        mainFrame = tk.Frame(self, bg="#111111", width=460, height=820,
                             highlightbackground="#444444", highlightthickness=1)
        mainFrame.place(relx=0.5, rely=0.5, anchor="center")
        mainFrame.pack_propagate(False)

        if self.logo_photo:
            tk.Label(mainFrame, image=self.logo_photo, bg="#111111").pack(pady=(18, 6))

        tk.Label(mainFrame, text="Create Account", bg="#111111",
                 font=("Arial", 22, "bold"), fg="#ffffff").pack(pady=(0, 4))
        tk.Label(mainFrame, text="Register as a St. Michael's College of Iligan student",
                 bg="#111111", font=("Arial", 10), fg="#bdbdbd").pack(pady=(0, 14))

        tk.Label(mainFrame, text="First Name", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.firstname_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Enter first name",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=38, corner_radius=7
        )
        self.firstname_entry.pack(fill="x", padx=35, pady=(0, 10))

        tk.Label(mainFrame, text="Middle Name", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.middlename_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Enter middle name",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=38, corner_radius=7
        )
        self.middlename_entry.pack(fill="x", padx=35, pady=(0, 10))

        tk.Label(mainFrame, text="Last Name", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.lastname_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Enter last name",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=38, corner_radius=7
        )
        self.lastname_entry.pack(fill="x", padx=35, pady=(0, 10))

        self.firstname_entry.bind("<KeyRelease>", self.update_username_preview)
        self.middlename_entry.bind("<KeyRelease>", self.update_username_preview)
        self.lastname_entry.bind("<KeyRelease>", self.update_username_preview)

        tk.Label(mainFrame, text="College / Department", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.college_menu = customtkinter.CTkOptionMenu(
            mainFrame, values=COLLEGES, font=("Arial", 13),
            dropdown_font=("Arial", 12), fg_color="#ffffff", text_color="#111111",
            button_color="#d0d0d0", button_hover_color="#bdbdbd",
            height=38, corner_radius=7
        )
        self.college_menu.set("Select your college")
        self.college_menu.pack(fill="x", padx=35, pady=(0, 10))

        tk.Label(mainFrame, text="Password", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.password_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Create password", show="*",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=38, corner_radius=7
        )
        self.password_entry.pack(fill="x", padx=35, pady=(0, 10))
        self.eye_button(mainFrame, self.password_entry)

        tk.Label(mainFrame, text="Confirm Password", bg="#111111", font=("Arial", 10, "bold"),
                 fg="#ffffff", anchor="w").pack(fill="x", padx=35, pady=(0, 4))
        self.confirmpass_entry = customtkinter.CTkEntry(
            mainFrame, placeholder_text="Confirm password", show="*",
            font=("Arial", 13), text_color="#111111", fg_color="#ffffff",
            border_color="#d0d0d0", border_width=1, height=38, corner_radius=7
        )
        self.confirmpass_entry.pack(fill="x", padx=35, pady=(0, 10))
        self.eye_button(mainFrame, self.confirmpass_entry)

        tk.Label(mainFrame, text="Your username will be:", bg="#111111",
                 font=("Arial", 9), fg="#bdbdbd", anchor="w").pack(fill="x", padx=35)
        self.username_preview = tk.Label(mainFrame, bg="#111111", font=("Arial", 10, "bold"),
                                         fg="#ffffff", anchor="w")
        self.username_preview.pack(fill="x", padx=35, pady=(0, 12))
        self.update_username_preview()

        customtkinter.CTkButton(
            mainFrame, command=self.handle_register, text="Register",
            fg_color="#ffffff", hover_color="#d9d9d9", text_color="#111111",
            cursor="hand2", height=42, corner_radius=7,
            font=("Arial", 13, "bold")
        ).pack(fill="x", padx=35, pady=(0, 12))

        already = tk.Frame(mainFrame, bg="#111111")
        already.pack(pady=(0, 6))
        tk.Label(already, text="Already have an account? ", bg="#111111",
                 fg="#bdbdbd", font=("Arial", 9)).pack(side="left")
        signuplabel = tk.Label(already, text="Login", bg="#111111",
                               fg="#ffffff", font=("Arial", 9, "bold"),
                               cursor="hand2")
        signuplabel.pack(side="left")
        signuplabel.bind("<Button-1>", self.switch_to_login)

        self.current_frame = mainFrame

    def show_dashboard(self):
        self.clear_frame()

        dashFrame = tk.Frame(self, bg="#ffffff", width=600, height=400)
        dashFrame.place(relx=0.5, rely=0.5, anchor="center")
        dashFrame.pack_propagate(False)

        tk.Label(dashFrame, text=f"Welcome, {self.user.current_user}!",
                bg="#ffffff", font=("Arial", 20, "bold"), fg="#2d3748").pack(pady=20)
        tk.Label(dashFrame, text = (f"Role: {self.role.title()}"), bg="white", font=("Arial", 12), fg = "#718096").pack(pady=5)

        customtkinter.CTkButton(dashFrame, text="Logout", fg_color="red",
                                hover_color="#8b0000", command=self.logout).pack(pady=10)

        self.current_frame = dashFrame

    def show_sportselection(self):
        self.clear_frame()

        self.current_frame = SportSelection(self, self.open_admindashboard, on_logout=self.logout)
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_label.lower()
        self.current_frame.lift()
        self.notif_label.lift()

    def open_admindashboard(self, sport):
        self.clear_frame()

        self.current_frame = AdminDashboard(self, sport, self.show_sportselection)
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_label.lower(self.current_frame)
        self.current_frame.lift()
        self.notif_label.lift()

    def show_studentsports(self):
        self.clear_frame()

        self.current_frame = SportSelect(self, on_sport_select=self.open_studentdashboard, on_logout=self.logout, username=self.user.get_firstname() or "Student")
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_label.lower(self.current_frame)
        self.current_frame.lift()
        self.notif_label.lift()

    def open_studentdashboard(self, sport):
        self.clear_frame()

        self.current_frame = StudentDashboard(self, sport, on_back=self.show_studentsports, username=self.user.current_user)
        self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.bg_label.lower(self.current_frame)
        self.current_frame.lift()
        self.notif_label.lift()
        
    def logout(self):
        self.user.current_user = None
        self.show_login()
