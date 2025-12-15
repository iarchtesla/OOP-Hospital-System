import customtkinter as ctk
from tkinter import messagebox, ttk
import datetime
import json
from abc import ABC, abstractmethod

# ==============================================
# إعدادات ألوان التصميم الجديد (أصفر/أسود)
# ==============================================
ctk.set_appearance_mode("dark")

# الألوان الجديدة
COLORS = {
    "primary": "#FFD700",       # أصفر ذهبي
    "primary_dark": "#B8860B",  # أصفر داكن
    "primary_light": "#FFFACD", # أصفر فاتح جداً
    "secondary": "#1A1A1A",     # أسود داكن
    "secondary_light": "#2A2A2A", # رمادي داكن جداً
    "secondary_dark": "#0A0A0A", # أسود نقي تقريباً
    "accent": "#FFA500",        # برتقالي ذهبي
    "text": "#FFFFFF",          # أبيض للنصوص
    "text_secondary": "#CCCCCC", # رمادي فاتح للنصوص الثانوية
    "success": "#32CD32",       # أخضر فاتح
    "warning": "#FFA500",       # برتقالي للتحذيرات
    "error": "#FF4500",         # أحمر برتقالي
    "card": "#222222",          # خلفية البطاقات
    "navbar": "#000000",        # شريط التنقل العلوي
}

# ==============================================
# فئات النظام الأساسية (نفس الكود بدون تغيير)
# ==============================================

class Patient:
    def __init__(self, patient_id, name, age, gender, phone, address="", medical_history=""):
        self._patient_id = patient_id
        self._name = name
        self._age = age
        self._gender = gender
        self._phone = phone
        self._address = address
        self._medical_history = medical_history
        self._appointments = []
        self._prescriptions = []
    
    @property
    def patient_id(self):
        return self._patient_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def age(self):
        return self._age
    
    @property
    def gender(self):
        return self._gender
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def address(self):
        return self._address
    
    @property
    def medical_history(self):
        return self._medical_history
    
    @property
    def appointments(self):
        return self._appointments.copy()
    
    @property
    def prescriptions(self):
        return self._prescriptions.copy()
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @age.setter
    def age(self, value):
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value
    
    @phone.setter
    def phone(self, value):
        if not value or not value.strip():
            raise ValueError("Phone cannot be empty")
        self._phone = value.strip()
    
    def add_appointment(self, appointment_data):
        self._appointments.append(appointment_data)
    
    def add_prescription(self, prescription_data):
        self._prescriptions.append(prescription_data)
    
    def to_dict(self):
        return {
            'patient_id': self._patient_id,
            'name': self._name,
            'age': self._age,
            'gender': self._gender,
            'phone': self._phone,
            'address': self._address,
            'medical_history': self._medical_history,
            'appointments': self._appointments,
            'prescriptions': self._prescriptions
        }
    
    @classmethod
    def from_dict(cls, data):
        patient = cls(
            data['patient_id'],
            data['name'],
            data['age'],
            data['gender'],
            data['phone'],
            data.get('address', ''),
            data.get('medical_history', '')
        )
        patient._appointments = data.get('appointments', [])
        patient._prescriptions = data.get('prescriptions', [])
        return patient

class Doctor:
    def __init__(self, doctor_id, name, specialty, phone, email="", schedule=""):
        self._doctor_id = doctor_id
        self._name = name
        self._specialty = specialty
        self._phone = phone
        self._email = email
        self._schedule = schedule
        self._appointments = []
    
    @property
    def doctor_id(self):
        return self._doctor_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def specialty(self):
        return self._specialty
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def email(self):
        return self._email
    
    @property
    def schedule(self):
        return self._schedule
    
    @property
    def appointments(self):
        return self._appointments.copy()
    
    def add_appointment(self, appointment_data):
        self._appointments.append(appointment_data)
    
    def to_dict(self):
        return {
            'doctor_id': self._doctor_id,
            'name': self._name,
            'specialty': self._specialty,
            'phone': self._phone,
            'email': self._email,
            'schedule': self._schedule,
            'appointments': self._appointments
        }
    
    @classmethod
    def from_dict(cls, data):
        doctor = cls(
            data['doctor_id'],
            data['name'],
            data['specialty'],
            data['phone'],
            data.get('email', ''),
            data.get('schedule', '')
        )
        doctor._appointments = data.get('appointments', [])
        return doctor

class Medicine:
    def __init__(self, medicine_id, name, price, quantity, category, dosage=""):
        self._medicine_id = medicine_id
        self._name = name
        self._price = price
        self._quantity = quantity
        self._category = category
        self._dosage = dosage
    
    @property
    def medicine_id(self):
        return self._medicine_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def quantity(self):
        return self._quantity
    
    @property
    def category(self):
        return self._category
    
    @property
    def dosage(self):
        return self._dosage
    
    def to_dict(self):
        return {
            'medicine_id': self._medicine_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'category': self._category,
            'dosage': self._dosage
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['medicine_id'],
            data['name'],
            data['price'],
            data['quantity'],
            data['category'],
            data.get('dosage', '')
        )

# ==============================================
# فئات إدارة المستخدمين
# ==============================================

class User(ABC):
    def __init__(self, username, password, role):
        self._username = username
        self._password = password
        self._role = role
    
    @property
    def username(self):
        return self._username
    
    @property
    def role(self):
        return self._role
    
    def verify_password(self, password):
        return self._password == password
    
    @abstractmethod
    def get_permissions(self):
        pass
    
    def to_dict(self):
        return {
            'username': self._username,
            'password': self._password,
            'role': self._role
        }

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")
    
    def get_permissions(self):
        return {
            'manage_patients': True,
            'manage_doctors': True,
            'manage_medicines': True,
            'manage_appointments': True,
            'manage_users': True,
            'view_reports': True
        }

class DoctorUser(User):
    def __init__(self, username, password, doctor_id):
        super().__init__(username, password, "doctor")
        self._doctor_id = doctor_id
    
    @property
    def doctor_id(self):
        return self._doctor_id
    
    def get_permissions(self):
        return {
            'manage_patients': True,
            'manage_doctors': False,
            'manage_medicines': False,
            'manage_appointments': True,
            'manage_users': False,
            'view_reports': True
        }

class Nurse(User):
    def __init__(self, username, password):
        super().__init__(username, password, "nurse")
    
    def get_permissions(self):
        return {
            'manage_patients': True,
            'manage_doctors': False,
            'manage_medicines': True,
            'manage_appointments': True,
            'manage_users': False,
            'view_reports': True
        }

class Receptionist(User):
    def __init__(self, username, password):
        super().__init__(username, password, "receptionist")
    
    def get_permissions(self):
        return {
            'manage_patients': True,
            'manage_doctors': False,
            'manage_medicines': False,
            'manage_appointments': True,
            'manage_users': False,
            'view_reports': False
        }

# ==============================================
# نظام إدارة المستشفى
# ==============================================

class HospitalManagementSystem:
    def __init__(self):
        self._patients = []
        self._doctors = []
        self._medicines = []
        self._appointments = []
        self._users = []
        self._current_user = None
        self._initialize_default_users()
        self._load_sample_data()
    
    def _initialize_default_users(self):
        default_admin = Admin("admin", "admin123")
        default_doctor = DoctorUser("doctor", "doc123", "D001")
        default_nurse = Nurse("nurse", "nurse123")
        default_reception = Receptionist("reception", "reception123")
        self._users = [default_admin, default_doctor, default_nurse, default_reception]
    
    def _load_sample_data(self):
        sample_patients = [
            Patient("P001", "Ahmed Mohamed", 35, "Male", "01001234567", "Cairo - New Cairo", "Penicillin allergy"),
            Patient("P002", "Fatma Ali", 28, "Female", "01009876543", "Giza - Dokki", "No medical history"),
            Patient("P003", "Mohamed Said", 45, "Male", "01005556677", "Alexandria - Smouha", "High blood pressure, Diabetes"),
        ]
        self._patients = sample_patients
        
        sample_doctors = [
            Doctor("D001", "Dr. Khalid Abdelrahman", "Internal Medicine", "01001112233", "khalid@hospital.com", "Sun-Thu 9AM-5PM"),
            Doctor("D002", "Dr. Mona Hussein", "Gynecology", "01002223344", "mona@hospital.com", "Sat-Wed 10AM-6PM"),
            Doctor("D003", "Dr. Amr Ibrahim", "Orthopedic Surgery", "01003334455", "amr@hospital.com", "Mon-Fri 8AM-4PM"),
            Doctor("D004", "Dr. Sara Mahmoud", "Pediatrics", "01004445566", "sara@hospital.com", "Sun-Thu 11AM-7PM"),
        ]
        self._doctors = sample_doctors
        
        sample_medicines = [
            Medicine("M001", "Paracetamol", 15, 500, "Analgesics", "500mg"),
            Medicine("M002", "Amoxicillin", 45, 200, "Antibiotics", "500mg"),
            Medicine("M003", "Atenolol", 30, 150, "Cardiac", "50mg"),
            Medicine("M004", "Metformin", 25, 300, "Diabetes", "850mg"),
            Medicine("M005", "Ibuprofen", 20, 400, "Anti-inflammatory", "400mg"),
            Medicine("M006", "Loratadine", 35, 250, "Antihistamine", "10mg"),
            Medicine("M007", "Omeprazole", 40, 180, "Gastrointestinal", "20mg"),
            Medicine("M008", "Citalopram", 55, 120, "Antidepressants", "20mg"),
        ]
        self._medicines = sample_medicines
    
    def login(self, username, password):
        for user in self._users:
            if user.username == username and user.verify_password(password):
                self._current_user = user
                return True
        return False
    
    def logout(self):
        self._current_user = None
    
    def get_current_user(self):
        return self._current_user
    
    def get_patients_list(self):
        return self._patients
    
    def get_doctors_list(self):
        return self._doctors
    
    def get_medicines_list(self):
        return self._medicines
    
    def get_appointments_list(self):
        return self._appointments
    
    def get_todays_appointments(self):
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        return [app for app in self._appointments if app.get('date') == today]
    
    def add_patient(self, patient_data):
        try:
            patient = Patient(**patient_data)
            self._patients.append(patient)
            return True, f"Patient '{patient.name}' added successfully!"
        except Exception as e:
            return False, str(e)
    
    def add_doctor(self, doctor_data):
        try:
            doctor = Doctor(**doctor_data)
            self._doctors.append(doctor)
            return True, f"Doctor '{doctor.name}' added successfully!"
        except Exception as e:
            return False, str(e)
    
    def add_medicine(self, medicine_data):
        try:
            medicine = Medicine(**medicine_data)
            self._medicines.append(medicine)
            return True, f"Medicine '{medicine.name}' added successfully!"
        except Exception as e:
            return False, str(e)
    
    def schedule_appointment(self, appointment_data):
        appointment_id = f"A{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        appointment_data['appointment_id'] = appointment_id
        appointment_data['status'] = 'Scheduled'
        appointment_data['created_by'] = self._current_user.username if self._current_user else "Unknown"
        
        self._appointments.append(appointment_data)
        
        for patient in self._patients:
            if patient.patient_id == appointment_data['patient_id']:
                patient.add_appointment(appointment_data)
                break
        
        for doctor in self._doctors:
            if doctor.doctor_id == appointment_data['doctor_id']:
                doctor.add_appointment(appointment_data)
                break
        
        return True, f"Appointment scheduled successfully! ID: {appointment_id}"
    
    def create_prescription(self, prescription_data):
        prescription_id = f"RX{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        prescription_data['prescription_id'] = prescription_id
        prescription_data['date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prescription_data['prescribed_by'] = self._current_user.username if self._current_user else "Unknown"
        
        for item in prescription_data.get('items', []):
            for medicine in self._medicines:
                if medicine.medicine_id == item['medicine_id']:
                    medicine.quantity -= item['quantity']
                    break
        
        for patient in self._patients:
            if patient.patient_id == prescription_data['patient_id']:
                patient.add_prescription(prescription_data)
                break
        
        return True, f"Prescription created successfully! ID: {prescription_id}"
    
    def save_data(self):
        try:
            patients_data = [patient.to_dict() for patient in self._patients]
            with open('patients.json', 'w') as f:
                json.dump(patients_data, f, indent=2)
            
            doctors_data = [doctor.to_dict() for doctor in self._doctors]
            with open('doctors.json', 'w') as f:
                json.dump(doctors_data, f, indent=2)
            
            medicines_data = [medicine.to_dict() for medicine in self._medicines]
            with open('medicines.json', 'w') as f:
                json.dump(medicines_data, f, indent=2)
            
            with open('appointments.json', 'w') as f:
                json.dump(self._appointments, f, indent=2)
            
            return True, "All data saved successfully!"
        except Exception as e:
            return False, f"Error saving data: {e}"
    
    def load_data(self):
        try:
            with open('patients.json', 'r') as f:
                patients_data = json.load(f)
            self._patients = [Patient.from_dict(data) for data in patients_data]
            
            with open('doctors.json', 'r') as f:
                doctors_data = json.load(f)
            self._doctors = [Doctor.from_dict(data) for data in doctors_data]
            
            with open('medicines.json', 'r') as f:
                medicines_data = json.load(f)
            self._medicines = [Medicine.from_dict(data) for data in medicines_data]
            
            with open('appointments.json', 'r') as f:
                self._appointments = json.load(f)
            
            return True, "All data loaded successfully!"
        except Exception as e:
            return False, f"Error loading data: {e}"

# ==============================================
# واجهة الدخول
# ==============================================

class HospitalLoginSystem:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Hospital Management System - Login")
        self.app.geometry("500x650")
        self.app.resizable(False, False)
        
        # تعيين خلفية سوداء
        self.app.configure(fg_color=COLORS["secondary_dark"])
        
        self.hospital_system = HospitalManagementSystem()
        self.setup_ui()
    
    def setup_ui(self):
        # إطار رئيسي بخلفية سوداء
        main_frame = ctk.CTkFrame(self.app, fg_color=COLORS["secondary_dark"], corner_radius=0)
        main_frame.pack(fill="both", expand=True)
        
        # شعار ونص مضيء
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(pady=40)
        
        logo_label = ctk.CTkLabel(
            header_frame,
            text="⚕️",
            font=("Arial", 60),
            text_color=COLORS["primary"]
        )
        logo_label.pack(pady=10)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="GOLDEN CARE HOSPITAL",
            font=("Arial", 28, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Management System",
            font=("Arial", 16),
            text_color=COLORS["text_secondary"]
        )
        subtitle_label.pack(pady=5)
        
        # إطار الدخول
        login_frame = ctk.CTkFrame(
            main_frame,
            fg_color=COLORS["card"],
            corner_radius=15,
            width=400,
            height=350
        )
        login_frame.pack(pady=20)
        login_frame.pack_propagate(False)
        
        login_title = ctk.CTkLabel(
            login_frame,
            text="STAFF LOGIN",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        login_title.pack(pady=30)
        
        # حقل اسم المستخدم
        self.username = ctk.CTkEntry(
            login_frame,
            placeholder_text="Username",
            width=300,
            height=50,
            font=("Arial", 16),
            corner_radius=8,
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["text_secondary"]
        )
        self.username.pack(pady=15)
        
        # حقل كلمة المرور
        self.password = ctk.CTkEntry(
            login_frame,
            placeholder_text="Password",
            show="•",
            width=300,
            height=50,
            font=("Arial", 16),
            corner_radius=8,
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"],
            placeholder_text_color=COLORS["text_secondary"]
        )
        self.password.pack(pady=15)
        
        # زر الدخول
        login_btn = ctk.CTkButton(
            login_frame,
            text="ACCESS SYSTEM",
            command=self.authenticate,
            width=300,
            height=55,
            font=("Arial", 18, "bold"),
            corner_radius=10,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            text_color=COLORS["secondary_dark"]
        )
        login_btn.pack(pady=25)
        
        # معلومات المستخدمين الافتراضيين
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(pady=20)
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Default Credentials:",
            font=("Arial", 12, "bold"),
            text_color=COLORS["text_secondary"]
        )
        info_label.pack()
        
        credentials = [
            "admin / admin123",
            "doctor / doc123",
            "nurse / nurse123",
            "reception / reception123"
        ]
        
        for cred in credentials:
            cred_label = ctk.CTkLabel(
                info_frame,
                text=f"• {cred}",
                font=("Arial", 11),
                text_color=COLORS["primary_light"]
            )
            cred_label.pack(pady=2)
        
        # تذييل الصفحة
        footer = ctk.CTkLabel(
            main_frame,
            text="© 2024 Golden Care Hospital | Secure Medical Management v3.0",
            font=("Arial", 10),
            text_color=COLORS["text_secondary"]
        )
        footer.pack(side="bottom", pady=20)
        
        # إضافة إمكانية الضغط على Enter للدخول
        self.app.bind('<Return>', lambda event: self.authenticate())
    
    def authenticate(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Input Error", "Please enter both username and password!")
            return
        
        if self.hospital_system.login(username, password):
            messagebox.showinfo("Login Successful", f"Welcome, {username}!\nLoading system...")
            self.app.destroy()
            
            # فتح النظام الرئيسي
            main_app = HospitalMainApp(self.hospital_system)
            main_app.run()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
            self.password.delete(0, 'end')
    
    def run(self):
        self.app.mainloop()

# ==============================================
# الواجهة الرئيسية - مع تحسينات التصميم
# ==============================================

class HospitalMainApp:
    def __init__(self, hospital_system):
        self.hospital = hospital_system
        self.current_user = hospital_system.get_current_user()
        
        self.app = ctk.CTk()
        self.app.title("Golden Care Hospital - Management System")
        self.app.geometry("1400x800")
        self.app.state('zoomed')  # فتح النافذة بحجم كامل
        
        # تعيين خلفية سوداء
        self.app.configure(fg_color=COLORS["secondary_dark"])
        
        # شريط التنقل العلوي (بدلاً من الشريط الجانبي)
        self.navbar = ctk.CTkFrame(
            self.app,
            height=70,
            fg_color=COLORS["navbar"],
            corner_radius=0
        )
        self.navbar.pack(side="top", fill="x")
        self.navbar.pack_propagate(False)
        
        # المنطقة الرئيسية
        self.main_content = ctk.CTkFrame(
            self.app,
            fg_color=COLORS["secondary_dark"]
        )
        self.main_content.pack(side="top", expand=True, fill="both")
        
        self.setup_navbar()
        self.show_dashboard()
    
    def setup_navbar(self):
        # الجزء الأيسر من شريط التنقل (الشعار)
        left_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        left_frame.pack(side="left", padx=20)
        
        logo_label = ctk.CTkLabel(
            left_frame,
            text="🏥 GOLDEN CARE HOSPITAL",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        logo_label.pack(side="left", padx=10)
        
        # الجزء الأوسط من شريط التنقل (أزرار التنقل)
        center_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        center_frame.pack(side="left", expand=True, padx=40)
        
        # أزرار التنقل في شريط علوي
        nav_items = [
            ("📊", "Dashboard", self.show_dashboard),
            ("👥", "Patients", self.show_patients),
            ("👨‍⚕️", "Doctors", self.show_doctors),
            ("💊", "Medicines", self.show_medicines),
            ("📅", "Appointments", self.show_appointments),
            ("📈", "Reports", self.show_reports),
            ("⚙️", "Settings", self.show_settings),
        ]
        
        for icon, text, command in nav_items:
            nav_btn = ctk.CTkButton(
                center_frame,
                text=f"  {icon} {text}",
                command=command,
                height=45,
                width=130,
                fg_color="transparent",
                hover_color=COLORS["secondary_light"],
                font=("Arial", 14),
                text_color=COLORS["text"],
                corner_radius=8
            )
            nav_btn.pack(side="left", padx=5)
        
        # الجزء الأيمن من شريط التنقل (معلومات المستخدم)
        right_frame = ctk.CTkFrame(self.navbar, fg_color="transparent")
        right_frame.pack(side="right", padx=20)
        
        # زر المستخدم مع معلومات
        user_info_btn = ctk.CTkButton(
            right_frame,
            text=f"👤 {self.current_user.username.upper()}",
            command=self.show_user_menu,
            height=45,
            width=180,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 14, "bold"),
            text_color=COLORS["secondary_dark"],
            corner_radius=8,
            anchor="center"
        )
        user_info_btn.pack(side="left", padx=10)
        
        # زر تسجيل الخروج
        logout_btn = ctk.CTkButton(
            right_frame,
            text="🚪",
            command=self.logout,
            height=45,
            width=50,
            fg_color=COLORS["error"],
            hover_color="#FF6347",
            font=("Arial", 18),
            corner_radius=8
        )
        logout_btn.pack(side="left")
    
    def show_user_menu(self):
        # قائمة منبثقة للمستخدم
        menu = ctk.CTkToplevel(self.app)
        menu.title("User Menu")
        menu.geometry("250x150")
        menu.resizable(False, False)
        menu.grab_set()
        
        menu.configure(fg_color=COLORS["card"])
        
        # معلومات المستخدم
        user_label = ctk.CTkLabel(
            menu,
            text=f"👤 {self.current_user.username}",
            font=("Arial", 18, "bold"),
            text_color=COLORS["primary"]
        )
        user_label.pack(pady=15)
        
        role_label = ctk.CTkLabel(
            menu,
            text=f"Role: {self.current_user.role.title()}",
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        role_label.pack(pady=5)
        
        # زر تغيير كلمة المرور
        change_pass_btn = ctk.CTkButton(
            menu,
            text="Change Password",
            command=lambda: messagebox.showinfo("Info", "Password change feature coming soon!"),
            height=35,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 12),
            text_color=COLORS["secondary_dark"]
        )
        change_pass_btn.pack(pady=10)
    
    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        self.clear_main_content()
        
        # شريط العنوان الفرعي
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="📊 DASHBOARD OVERVIEW",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        date_label = ctk.CTkLabel(
            subheader,
            text=datetime.datetime.now().strftime("%A, %B %d, %Y"),
            font=("Arial", 14),
            text_color=COLORS["text_secondary"]
        )
        date_label.pack(side="right", padx=40, pady=15)
        
        # إطار المحتوى الرئيسي
        content_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["secondary_dark"]
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # بطاقات الإحصائيات
        stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_frame.pack(pady=20, padx=20, fill="x")
        
        stats_data = [
            ("👥 Total Patients", len(self.hospital.get_patients_list()), COLORS["primary"]),
            ("👨‍⚕️ Total Doctors", len(self.hospital.get_doctors_list()), COLORS["accent"]),
            ("💊 Medicines Stock", len(self.hospital.get_medicines_list()), COLORS["success"]),
            ("📅 Today's Appointments", len(self.hospital.get_todays_appointments()), COLORS["warning"])
        ]
        
        for i, (title, count, color) in enumerate(stats_data):
            card = ctk.CTkFrame(
                stats_frame,
                width=320,
                height=140,
                fg_color=COLORS["card"],
                corner_radius=15,
                border_color=color,
                border_width=2
            )
            card.grid(row=0, column=i, padx=10, pady=10)
            card.grid_propagate(False)
            
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 16),
                text_color=COLORS["text_secondary"]
            )
            title_label.pack(pady=(25, 10), padx=25, anchor="w")
            
            count_label = ctk.CTkLabel(
                card,
                text=str(count),
                font=("Arial", 36, "bold"),
                text_color=color
            )
            count_label.pack(pady=10, padx=25, anchor="w")
            
            # إضافة مؤشرات طاقة للمخزون
            if i == 2:  # Medicines Stock
                indicator_frame = ctk.CTkFrame(card, fg_color="transparent")
                indicator_frame.pack(pady=10, padx=25, anchor="w", fill="x")
                
                # مؤشرات طاقة (مثل الصورة)
                for j in range(5):
                    indicator = ctk.CTkFrame(
                        indicator_frame,
                        width=40,
                        height=8,
                        fg_color=color if j < 3 else COLORS["secondary_light"],
                        corner_radius=2
                    )
                    indicator.pack(side="left", padx=2)
        
        # جدول المواعيد اليومية
        appointments_frame = ctk.CTkFrame(
            content_frame,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        appointments_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        appointments_title = ctk.CTkLabel(
            appointments_frame,
            text="📅 TODAY'S APPOINTMENTS",
            font=("Arial", 20, "bold"),
            text_color=COLORS["primary"]
        )
        appointments_title.pack(pady=25, padx=30, anchor="w")
        
        # إنشاء جدول
        columns = ("Time", "Patient", "Doctor", "Reason", "Status")
        tree = ttk.Treeview(
            appointments_frame,
            columns=columns,
            show="headings",
            height=12
        )
        
        # تنسيق الجدول
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["card"],
                       borderwidth=0,
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background=COLORS["primary"],
                       foreground=COLORS["secondary_dark"],
                       font=('Arial', 12, 'bold'),
                       relief="flat")
        style.map("Treeview", background=[('selected', COLORS["secondary_light"])])
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        # إضافة بيانات المواعيد
        today_appointments = self.hospital.get_todays_appointments()
        for app in today_appointments:
            status_color = COLORS["success"] if app['status'] == 'Completed' else COLORS["warning"]
            tree.insert("", "end", values=(
                app['time'],
                app['patient_name'],
                app['doctor_name'],
                app['reason'][:30] + "..." if len(app['reason']) > 30 else app['reason'],
                app['status']
            ))
        
        # إضافة شريط التمرير
        tree_scroll = ttk.Scrollbar(appointments_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=30, pady=(0, 30))
        tree_scroll.pack(side="right", fill="y", pady=(0, 30))
        
        # زر إضافة موعد جديد - تم تعديل النص
        if self.current_user.get_permissions()['manage_appointments']:
            new_appointment_btn = ctk.CTkButton(
                appointments_frame,
                text="➕ NEW APPOINTMENT",  # تم تعديل النص هنا
                command=self.schedule_appointment_dialog,
                height=50,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=("Arial", 16, "bold"),
                text_color=COLORS["secondary_dark"]
            )
            new_appointment_btn.pack(pady=(0, 20), padx=30, fill="x")
    
    def show_patients(self):
        self.clear_main_content()
        
        # شريط العنوان الفرعي
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="👥 PATIENTS MANAGEMENT",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        # شريط الأدوات
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent", height=70)
        toolbar.pack(fill="x", padx=40, pady=20)
        toolbar.pack_propagate(False)
        
        # زر إضافة مريض
        add_patient_btn = ctk.CTkButton(
            toolbar,
            text="➕ ADD PATIENT",
            command=self.add_patient_dialog,
            width=180,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 14, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        add_patient_btn.pack(side="left")
        
        # حقل البحث
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="right")
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search patients...",
            width=300,
            height=50,
            font=("Arial", 14),
            corner_radius=8,
            fg_color=COLORS["card"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"]
        )
        search_entry.pack(side="left", padx=5)
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=60,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 18),
            text_color=COLORS["secondary_dark"]
        )
        search_btn.pack(side="left")
        
        # جدول المرضى
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # إنشاء الجدول
        columns = ("ID", "Name", "Age", "Gender", "Phone", "Address")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        style = ttk.Style()
        style.configure("Treeview",
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["card"],
                       borderwidth=0,
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background=COLORS["primary"],
                       foreground=COLORS["secondary_dark"],
                       font=('Arial', 12, 'bold'),
                       relief="flat")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        
        # إضافة بيانات المرضى
        patients = self.hospital.get_patients_list()
        for patient in patients:
            tree.insert("", "end", values=(
                patient.patient_id,
                patient.name,
                patient.age,
                patient.gender,
                patient.phone,
                patient.address[:30] + "..." if len(patient.address) > 30 else patient.address
            ))
        
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        tree_scroll.pack(side="right", fill="y", pady=20)
    
    def show_doctors(self):
        self.clear_main_content()
        
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="👨‍⚕️ DOCTORS MANAGEMENT",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent", height=70)
        toolbar.pack(fill="x", padx=40, pady=20)
        toolbar.pack_propagate(False)
        
        if self.current_user.role == "admin":
            add_doctor_btn = ctk.CTkButton(
                toolbar,
                text="➕ ADD DOCTOR",
                command=self.add_doctor_dialog,
                width=180,
                height=50,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=("Arial", 14, "bold"),
                text_color=COLORS["secondary_dark"]
            )
            add_doctor_btn.pack(side="left")
        
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        columns = ("ID", "Name", "Specialty", "Phone", "Schedule")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        style = ttk.Style()
        style.configure("Treeview",
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["card"],
                       borderwidth=0,
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background=COLORS["primary"],
                       foreground=COLORS["secondary_dark"],
                       font=('Arial', 12, 'bold'),
                       relief="flat")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200)
        
        doctors = self.hospital.get_doctors_list()
        for doctor in doctors:
            tree.insert("", "end", values=(
                doctor.doctor_id,
                doctor.name,
                doctor.specialty,
                doctor.phone,
                doctor.schedule[:30] + "..." if len(doctor.schedule) > 30 else doctor.schedule
            ))
        
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        tree_scroll.pack(side="right", fill="y", pady=20)
    
    def show_medicines(self):
        self.clear_main_content()
        
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="💊 MEDICINES INVENTORY",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent", height=70)
        toolbar.pack(fill="x", padx=40, pady=20)
        toolbar.pack_propagate(False)
        
        if self.current_user.get_permissions()['manage_medicines']:
            add_medicine_btn = ctk.CTkButton(
                toolbar,
                text="➕ ADD MEDICINE",
                command=self.add_medicine_dialog,
                width=180,
                height=50,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=("Arial", 14, "bold"),
                text_color=COLORS["secondary_dark"]
            )
            add_medicine_btn.pack(side="left")
        
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        columns = ("ID", "Name", "Price", "Quantity", "Category", "Dosage")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        style = ttk.Style()
        style.configure("Treeview",
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["card"],
                       borderwidth=0,
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background=COLORS["primary"],
                       foreground=COLORS["secondary_dark"],
                       font=('Arial', 12, 'bold'),
                       relief="flat")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        medicines = self.hospital.get_medicines_list()
        for medicine in medicines:
            tree.insert("", "end", values=(
                medicine.medicine_id,
                medicine.name,
                f"${medicine.price:.2f}",
                medicine.quantity,
                medicine.category,
                medicine.dosage
            ))
        
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        tree_scroll.pack(side="right", fill="y", pady=20)
    
    def show_appointments(self):
        self.clear_main_content()
        
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="📅 APPOINTMENTS",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent", height=70)
        toolbar.pack(fill="x", padx=40, pady=20)
        toolbar.pack_propagate(False)
        
        if self.current_user.get_permissions()['manage_appointments']:
            schedule_btn = ctk.CTkButton(
                toolbar,
                text="➕ NEW APPOINTMENT",  # تم تعديل النص هنا
                command=self.schedule_appointment_dialog,
                width=200,
                height=50,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=("Arial", 14, "bold"),
                text_color=COLORS["secondary_dark"]
            )
            schedule_btn.pack(side="left")
        
        table_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        table_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        columns = ("ID", "Date", "Time", "Patient", "Doctor", "Reason", "Status")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        style = ttk.Style()
        style.configure("Treeview",
                       background=COLORS["card"],
                       foreground=COLORS["text"],
                       fieldbackground=COLORS["card"],
                       borderwidth=0,
                       font=('Arial', 11))
        style.configure("Treeview.Heading",
                       background=COLORS["primary"],
                       foreground=COLORS["secondary_dark"],
                       font=('Arial', 12, 'bold'),
                       relief="flat")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        appointments = self.hospital.get_appointments_list()
        for app in appointments:
            tree.insert("", "end", values=(
                app.get('appointment_id', 'N/A'),
                app.get('date', 'N/A'),
                app.get('time', 'N/A'),
                app.get('patient_name', 'N/A'),
                app.get('doctor_name', 'N/A'),
                app.get('reason', 'N/A')[:20] + "..." if len(app.get('reason', '')) > 20 else app.get('reason', 'N/A'),
                app.get('status', 'N/A')
            ))
        
        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        
        tree.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        tree_scroll.pack(side="right", fill="y", pady=20)
    
    def show_reports(self):
        self.clear_main_content()
        
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="📈 REPORTS & ANALYTICS",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        # بطاقات التقارير
        reports_frame = ctk.CTkFrame(self.main_content, fg_color="transparent")
        reports_frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        report_types = [
            ("📊 Patient Report", "Generate detailed patient reports", self.generate_patient_report),
            ("📦 Inventory Report", "View medicine stock levels", self.generate_inventory_report),
            ("📅 Daily Report", "Today's activities summary", self.generate_daily_report),
            ("💊 Prescription Report", "View prescription history", self.generate_prescription_report),
        ]
        
        for i, (title, desc, command) in enumerate(report_types):
            card = ctk.CTkFrame(
                reports_frame,
                width=350,
                height=200,
                fg_color=COLORS["card"],
                corner_radius=15,
                border_color=COLORS["primary"],
                border_width=2
            )
            card.grid(row=i//2, column=i%2, padx=20, pady=20, sticky="nsew")
            card.grid_propagate(False)
            
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Arial", 20, "bold"),
                text_color=COLORS["primary"]
            )
            title_label.pack(pady=(30, 15), padx=25, anchor="w")
            
            desc_label = ctk.CTkLabel(
                card,
                text=desc,
                font=("Arial", 14),
                text_color=COLORS["text_secondary"],
                wraplength=300
            )
            desc_label.pack(pady=10, padx=25, anchor="w")
            
            generate_btn = ctk.CTkButton(
                card,
                text="GENERATE REPORT",
                command=command,
                width=200,
                height=45,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_dark"],
                font=("Arial", 14, "bold"),
                text_color=COLORS["secondary_dark"]
            )
            generate_btn.pack(pady=20, padx=25, anchor="w")
        
        reports_frame.grid_columnconfigure(0, weight=1)
        reports_frame.grid_columnconfigure(1, weight=1)
        reports_frame.grid_rowconfigure(0, weight=1)
        reports_frame.grid_rowconfigure(1, weight=1)
    
    def show_settings(self):
        self.clear_main_content()
        
        subheader = ctk.CTkFrame(
            self.main_content,
            height=60,
            fg_color=COLORS["secondary"],
            corner_radius=0
        )
        subheader.pack(fill="x")
        subheader.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            subheader,
            text="⚙️ SETTINGS",
            font=("Arial", 24, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(side="left", padx=40, pady=15)
        
        settings_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=COLORS["card"],
            corner_radius=15
        )
        settings_frame.pack(pady=40, padx=40, fill="both", expand=True)
        
        # قسم إدارة البيانات
        data_section = ctk.CTkFrame(settings_frame, fg_color="transparent")
        data_section.pack(pady=30, padx=40, fill="x")
        
        data_label = ctk.CTkLabel(
            data_section,
            text="DATA MANAGEMENT",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        data_label.pack(anchor="w", pady=(0, 20))
        
        save_load_frame = ctk.CTkFrame(data_section, fg_color="transparent")
        save_load_frame.pack(fill="x")
        
        save_btn = ctk.CTkButton(
            save_load_frame,
            text="💾 SAVE ALL DATA",
            command=self.save_data,
            width=200,
            height=55,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        save_btn.pack(side="left", padx=10)
        
        load_btn = ctk.CTkButton(
            save_load_frame,
            text="📂 LOAD SAVED DATA",
            command=self.load_data,
            width=200,
            height=55,
            fg_color=COLORS["accent"],
            hover_color=COLORS["warning"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        load_btn.pack(side="left", padx=10)
    
    # ==============================================
    # نوافذ المحادثة (Dialogues) - نفسها مع تعديل النص
    # ==============================================
    
    def add_patient_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Add New Patient")
        dialog.geometry("500x650")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # تعيين الألوان للنافذة المنبثقة
        dialog.configure(fg_color=COLORS["secondary_dark"])
        
        title_label = ctk.CTkLabel(
            dialog,
            text="➕ ADD NEW PATIENT",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(pady=30)
        
        form_frame = ctk.CTkFrame(dialog, fg_color=COLORS["card"], corner_radius=15)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        fields = [
            ("Patient ID:", "P001"),
            ("Name:", "Ahmed Mohamed"),
            ("Age:", "35"),
            ("Gender:", "Male"),
            ("Phone:", "01001234567"),
            ("Address:", "Cairo - New Cairo"),
            ("Medical History:", "Penicillin allergy")
        ]
        
        entries = {}
        scrollable_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for label_text, placeholder in fields:
            label = ctk.CTkLabel(
                scrollable_frame, 
                text=label_text, 
                font=("Arial", 14, "bold"),
                text_color=COLORS["text"]
            )
            label.pack(anchor="w", pady=(15, 5))
            
            entry = ctk.CTkEntry(
                scrollable_frame,
                placeholder_text=placeholder,
                width=400,
                height=45,
                font=("Arial", 14),
                corner_radius=8,
                fg_color=COLORS["secondary_light"],
                border_color=COLORS["primary"],
                text_color=COLORS["text"]
            )
            entry.pack(pady=(0, 10))
            entries[label_text[:-1].lower().replace(" ", "_")] = entry
        
        def submit():
            try:
                patient_data = {
                    'patient_id': entries['patient_id'].get(),
                    'name': entries['name'].get(),
                    'age': int(entries['age'].get()),
                    'gender': entries['gender'].get(),
                    'phone': entries['phone'].get(),
                    'address': entries['address'].get(),
                    'medical_history': entries['medical_history'].get()
                }
                
                success, message = self.hospital.add_patient(patient_data)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_patients()
                else:
                    messagebox.showerror("Error", message)
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        submit_btn = ctk.CTkButton(
            buttons_frame,
            text="ADD PATIENT",
            command=submit,
            width=200,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCEL",
            command=dialog.destroy,
            width=200,
            height=50,
            fg_color=COLORS["error"],
            hover_color="#FF6347",
            font=("Arial", 16, "bold")
        )
        cancel_btn.pack(side="left", padx=10)
    
    def add_doctor_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Add New Doctor")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.configure(fg_color=COLORS["secondary_dark"])
        
        title_label = ctk.CTkLabel(
            dialog,
            text="➕ ADD NEW DOCTOR",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(pady=30)
        
        form_frame = ctk.CTkFrame(dialog, fg_color=COLORS["card"], corner_radius=15)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        fields = [
            ("Doctor ID:", "D001"),
            ("Name:", "Dr. Khalid Abdelrahman"),
            ("Specialty:", "Internal Medicine"),
            ("Phone:", "01001112233"),
            ("Email:", "khalid@hospital.com"),
            ("Schedule:", "Sun-Thu 9AM-5PM")
        ]
        
        entries = {}
        scrollable_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for label_text, placeholder in fields:
            label = ctk.CTkLabel(
                scrollable_frame, 
                text=label_text, 
                font=("Arial", 14, "bold"),
                text_color=COLORS["text"]
            )
            label.pack(anchor="w", pady=(15, 5))
            
            entry = ctk.CTkEntry(
                scrollable_frame,
                placeholder_text=placeholder,
                width=400,
                height=45,
                font=("Arial", 14),
                corner_radius=8,
                fg_color=COLORS["secondary_light"],
                border_color=COLORS["primary"],
                text_color=COLORS["text"]
            )
            entry.pack(pady=(0, 10))
            entries[label_text[:-1].lower().replace(" ", "_")] = entry
        
        def submit():
            doctor_data = {
                'doctor_id': entries['doctor_id'].get(),
                'name': entries['name'].get(),
                'specialty': entries['specialty'].get(),
                'phone': entries['phone'].get(),
                'email': entries['email'].get(),
                'schedule': entries['schedule'].get()
            }
            
            success, message = self.hospital.add_doctor(doctor_data)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_doctors()
            else:
                messagebox.showerror("Error", message)
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        submit_btn = ctk.CTkButton(
            buttons_frame,
            text="ADD DOCTOR",
            command=submit,
            width=200,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCEL",
            command=dialog.destroy,
            width=200,
            height=50,
            fg_color=COLORS["error"],
            hover_color="#FF6347",
            font=("Arial", 16, "bold")
        )
        cancel_btn.pack(side="left", padx=10)
    
    def add_medicine_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Add New Medicine")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.configure(fg_color=COLORS["secondary_dark"])
        
        title_label = ctk.CTkLabel(
            dialog,
            text="➕ ADD NEW MEDICINE",
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(pady=30)
        
        form_frame = ctk.CTkFrame(dialog, fg_color=COLORS["card"], corner_radius=15)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        fields = [
            ("Medicine ID:", "M001"),
            ("Name:", "Paracetamol"),
            ("Price:", "15.0"),
            ("Quantity:", "500"),
            ("Category:", "Analgesics"),
            ("Dosage:", "500mg")
        ]
        
        entries = {}
        scrollable_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        for label_text, placeholder in fields:
            label = ctk.CTkLabel(
                scrollable_frame, 
                text=label_text, 
                font=("Arial", 14, "bold"),
                text_color=COLORS["text"]
            )
            label.pack(anchor="w", pady=(15, 5))
            
            entry = ctk.CTkEntry(
                scrollable_frame,
                placeholder_text=placeholder,
                width=400,
                height=45,
                font=("Arial", 14),
                corner_radius=8,
                fg_color=COLORS["secondary_light"],
                border_color=COLORS["primary"],
                text_color=COLORS["text"]
            )
            entry.pack(pady=(0, 10))
            entries[label_text[:-1].lower().replace(" ", "_")] = entry
        
        def submit():
            try:
                medicine_data = {
                    'medicine_id': entries['medicine_id'].get(),
                    'name': entries['name'].get(),
                    'price': float(entries['price'].get()),
                    'quantity': int(entries['quantity'].get()),
                    'category': entries['category'].get(),
                    'dosage': entries['dosage'].get()
                }
                
                success, message = self.hospital.add_medicine(medicine_data)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_medicines()
                else:
                    messagebox.showerror("Error", message)
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        submit_btn = ctk.CTkButton(
            buttons_frame,
            text="ADD MEDICINE",
            command=submit,
            width=200,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCEL",
            command=dialog.destroy,
            width=200,
            height=50,
            fg_color=COLORS["error"],
            hover_color="#FF6347",
            font=("Arial", 16, "bold")
        )
        cancel_btn.pack(side="left", padx=10)
    
    def schedule_appointment_dialog(self):
        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Schedule Appointment")
        dialog.geometry("600x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.configure(fg_color=COLORS["secondary_dark"])
        
        title_label = ctk.CTkLabel(
            dialog,
            text="📅 NEW APPOINTMENT",  # تم تعديل النص هنا
            font=("Arial", 22, "bold"),
            text_color=COLORS["primary"]
        )
        title_label.pack(pady=30)
        
        form_frame = ctk.CTkFrame(dialog, fg_color=COLORS["card"], corner_radius=15)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        scrollable_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # اختيار المريض
        patient_label = ctk.CTkLabel(
            scrollable_frame, 
            text="Select Patient:", 
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        patient_label.pack(anchor="w", pady=(15, 5))
        
        patients = self.hospital.get_patients_list()
        patient_names = [f"{p.patient_id} - {p.name}" for p in patients]
        patient_var = ctk.StringVar(value=patient_names[0] if patient_names else "")
        
        patient_combo = ctk.CTkComboBox(
            scrollable_frame,
            values=patient_names,
            variable=patient_var,
            width=500,
            height=45,
            font=("Arial", 14),
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_dark"]
        )
        patient_combo.pack(pady=(0, 20))
        
        # اختيار الطبيب
        doctor_label = ctk.CTkLabel(
            scrollable_frame, 
            text="Select Doctor:", 
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        doctor_label.pack(anchor="w", pady=(15, 5))
        
        doctors = self.hospital.get_doctors_list()
        doctor_names = [f"{d.doctor_id} - {d.name}" for d in doctors]
        doctor_var = ctk.StringVar(value=doctor_names[0] if doctor_names else "")
        
        doctor_combo = ctk.CTkComboBox(
            scrollable_frame,
            values=doctor_names,
            variable=doctor_var,
            width=500,
            height=45,
            font=("Arial", 14),
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_dark"]
        )
        doctor_combo.pack(pady=(0, 20))
        
        # التاريخ والوقت
        date_time_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        date_time_frame.pack(fill="x", pady=10)
        
        date_label = ctk.CTkLabel(
            date_time_frame, 
            text="Date:", 
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        date_label.pack(side="left", padx=(0, 10))
        
        date_entry = ctk.CTkEntry(
            date_time_frame,
            placeholder_text="YYYY-MM-DD",
            width=230,
            height=45,
            font=("Arial", 14),
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"]
        )
        date_entry.pack(side="left", padx=(0, 20))
        
        time_label = ctk.CTkLabel(
            date_time_frame, 
            text="Time:", 
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        time_label.pack(side="left", padx=(0, 10))
        
        time_entry = ctk.CTkEntry(
            date_time_frame,
            placeholder_text="HH:MM",
            width=230,
            height=45,
            font=("Arial", 14),
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"]
        )
        time_entry.pack(side="left")
        
        # سبب الزيارة
        reason_label = ctk.CTkLabel(
            scrollable_frame, 
            text="Reason:", 
            font=("Arial", 14, "bold"),
            text_color=COLORS["text"]
        )
        reason_label.pack(anchor="w", pady=(30, 5))
        
        reason_entry = ctk.CTkEntry(
            scrollable_frame,
            placeholder_text="Reason for visit",
            width=500,
            height=45,
            font=("Arial", 14),
            fg_color=COLORS["secondary_light"],
            border_color=COLORS["primary"],
            text_color=COLORS["text"]
        )
        reason_entry.pack(pady=(0, 20))
        
        def submit():
            try:
                patient_id = patient_var.get().split(" - ")[0]
                doctor_id = doctor_var.get().split(" - ")[0]
                
                appointment_data = {
                    'patient_id': patient_id,
                    'patient_name': patient_var.get().split(" - ")[1],
                    'doctor_id': doctor_id,
                    'doctor_name': doctor_var.get().split(" - ")[1],
                    'date': date_entry.get(),
                    'time': time_entry.get(),
                    'reason': reason_entry.get()
                }
                
                success, message = self.hospital.schedule_appointment(appointment_data)
                if success:
                    messagebox.showinfo("Success", message)
                    dialog.destroy()
                    self.show_appointments()
                else:
                    messagebox.showerror("Error", message)
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
        
        buttons_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        buttons_frame.pack(pady=20)
        
        submit_btn = ctk.CTkButton(
            buttons_frame,
            text="SCHEDULE",
            command=submit,
            width=200,
            height=50,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_dark"],
            font=("Arial", 16, "bold"),
            text_color=COLORS["secondary_dark"]
        )
        submit_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="CANCEL",
            command=dialog.destroy,
            width=200,
            height=50,
            fg_color=COLORS["error"],
            hover_color="#FF6347",
            font=("Arial", 16, "bold")
        )
        cancel_btn.pack(side="left", padx=10)
    
    # ==============================================
    # دوال التقارير (نفسها بدون تغيير)
    # ==============================================
    
    def generate_patient_report(self):
        messagebox.showinfo("Patient Report", "Patient report generation will be implemented in the next version.")
    
    def generate_inventory_report(self):
        messagebox.showinfo("Inventory Report", "Inventory report generation will be implemented in the next version.")
    
    def generate_daily_report(self):
        messagebox.showinfo("Daily Report", "Daily report generation will be implemented in the next version.")
    
    def generate_prescription_report(self):
        messagebox.showinfo("Prescription Report", "Prescription report generation will be implemented in the next version.")
    
    def save_data(self):
        success, message = self.hospital.save_data()
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def load_data(self):
        success, message = self.hospital.load_data()
        if success:
            messagebox.showinfo("Success", message)
            current_page = self.get_current_page()
            if current_page:
                current_page()
        else:
            messagebox.showerror("Error", message)
    
    def get_current_page(self):
        for widget in self.main_content.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkLabel):
                        text = child.cget("text")
                        if "DASHBOARD" in text:
                            return self.show_dashboard
                        elif "PATIENTS" in text:
                            return self.show_patients
                        elif "DOCTORS" in text:
                            return self.show_doctors
                        elif "MEDICINES" in text:
                            return self.show_medicines
                        elif "APPOINTMENTS" in text:
                            return self.show_appointments
        return None
    
    def logout(self):
        self.hospital.logout()
        self.app.destroy()
        
        login_app = HospitalLoginSystem()
        login_app.run()
    
    def run(self):
        self.app.mainloop()

# ==============================================
# التشغيل الرئيسي
# ==============================================

def main():
    print("🏥 Starting Golden Care Hospital Management System...")
    login_app = HospitalLoginSystem()
    login_app.run()

if __name__ == "__main__":
    main()