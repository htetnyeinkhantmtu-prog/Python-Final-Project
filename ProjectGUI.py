import tkinter as tk
from tkinter import ttk, messagebox
import auth
from storage import load_users, save_users
from matching import find_all_matches

# ---------------------------
# Constants / Option Lists
# ---------------------------
MUSIC_OPTIONS = [
    ("Pop", 1),
    ("Rock", 2),
    ("Classical", 3),
    ("K-pop", 4)
]

ACTIVITY_OPTIONS = [
    ("Reading", 1),
    ("Sports", 2),
    ("Gaming", 3),
    ("Cooking", 4),
    ("Traveling", 5)
]

PERSONALITY_OPTIONS = [
    ("Introvert", 1),
    ("Extrovert", 2)
]

MOOD_OPTIONS = [
    ("Calm", 1),
    ("Energetic", 2),
    ("Talkative", 3),
    ("Quiet", 4)
]

ZODIAC_EXAMPLES = [
    "aries","taurus","gemini","cancer","leo","virgo","libra","scorpio","sagittarius","capricorn","aquarius","pisces"
]

# ---------------------------
# Helper functions
# ---------------------------
def find_user_record(username):
    data = load_users()
    return next((u for u in data["users"] if u["username"] == username), None)

def update_user_questionnaire(username, answers):
    data = load_users()
    for u in data["users"]:
        if u["username"] == username:
            u["questionnaire"] = answers
            u["profile_complete"] = True
            break
    save_users(data)

# ---------------------------
# Application class
# ---------------------------
class FriendMatchmakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Friend Match Maker")
        self.root.geometry("620x520")
        self.root.resizable(False, False)

        self.current_user = None  # username string when logged in
        self._frame = None

        self.show_login_screen()

    def _switch_frame(self, new_frame):
        if self._frame:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

    # -----------------------
    # LOGIN / REGISTER SCREEN
    # -----------------------
    def show_login_screen(self):
        frame = ttk.Frame(self.root, padding=16)
        ttk.Label(frame, text="Friend Match Maker", font=("Helvetica", 20, "bold")).pack(pady=(0,10))

        # Notebook for Login / Register

        nb = ttk.Notebook(frame)
        login_tab = ttk.Frame(nb, padding=12)
        register_tab = ttk.Frame(nb, padding=12)
        nb.add(login_tab, text="Login")
        nb.add(register_tab, text="Register")
        nb.pack(fill="x", pady=10)

        # --- Login tab ---

        ttk.Label(login_tab, text="Username:").grid(row=0, column=0, sticky="w", pady=6)
        self.login_username = ttk.Entry(login_tab, width=30)
        self.login_username.grid(row=0, column=1, pady=6)

        ttk.Label(login_tab, text="Password:").grid(row=1, column=0, sticky="w", pady=6)
        self.login_password = ttk.Entry(login_tab, width=30, show="*")
        self.login_password.grid(row=1, column=1, pady=6)

        login_btn = ttk.Button(login_tab, text="Login", command=self._handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(10,0))

        # --- Register tab ---

        ttk.Label(register_tab, text="Username:").grid(row=0, column=0, sticky="w", pady=6)
        self.reg_username = ttk.Entry(register_tab, width=30)
        self.reg_username.grid(row=0, column=1, pady=6)

        ttk.Label(register_tab, text="Password:").grid(row=1, column=0, sticky="w", pady=6)
        self.reg_password = ttk.Entry(register_tab, width=30, show="*")
        self.reg_password.grid(row=1, column=1, pady=6)

        ttk.Label(register_tab, text="Confirm password:").grid(row=2, column=0, sticky="w", pady=6)
        self.reg_confirm = ttk.Entry(register_tab, width=30, show="*")
        self.reg_confirm.grid(row=2, column=1, pady=6)

        reg_btn = ttk.Button(register_tab, text="Register", command=self._handle_register)
        reg_btn.grid(row=3, column=0, columnspan=2, pady=(10,0))

        # Password requirements note
    
        pw_req = ("Password requirements:\n- At least 8 characters\n- Uppercase + lowercase\n- Number\n- Special character")
        ttk.Label(register_tab, text=pw_req, wraplength=420, foreground="gray").grid(row=4, column=0, columnspan=2, pady=(8,0))

        # Footer / quick-start
        ttk.Label(frame, text="Note: Use the Register tab to create an account, then login.").pack(pady=(12,0))

        self._switch_frame(frame)

    def _handle_register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()

        if not username:
            messagebox.showwarning("Registration", "Please enter a username.")
            return

        valid, msg = auth.username_valid(username)
        if not valid:
            messagebox.showwarning("Invalid username", msg)
            return

        if password != confirm:
            messagebox.showwarning("Registration", "Passwords do not match.")
            return

        strong, msg = auth.password_strength(password)
        if not strong:
            messagebox.showwarning("Weak password", msg)
            return

        success, msg = auth.register(username, password)
        if success:
            messagebox.showinfo("Registration", msg + " You may now login.")

            # Clear fields
            self.reg_username.delete(0, tk.END)
            self.reg_password.delete(0, tk.END)
            self.reg_confirm.delete(0, tk.END)
        else:
            messagebox.showerror("Registration failed", msg)

    def _handle_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password.")
            return

        success, msg, logged_in_user = auth.login(username, password)
        if success:
            self.current_user = logged_in_user
            messagebox.showinfo("Login", msg)
            self.show_main_menu()
        else:
            # show message from auth (may include lockout text)
            messagebox.showerror("Login failed", msg)

    # -----------------------
    # MAIN MENU
    # -----------------------
    def show_main_menu(self):
        frame = ttk.Frame(self.root, padding=12)
        ttk.Label(frame, text=f"Welcome, {self.current_user}", font=("Helvetica", 18, "bold")).pack(pady=(0,12))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=6)

        ttk.Button(btn_frame, text="Take / Edit Questionnaire", width=30, command=self.show_questionnaire).grid(row=0, column=0, pady=6)
        ttk.Button(btn_frame, text="Find Matches", width=30, command=self.show_matches).grid(row=1, column=0, pady=6)
        ttk.Button(btn_frame, text="View My Profile", width=30, command=self.show_profile).grid(row=2, column=0, pady=6)
        ttk.Button(btn_frame, text="Logout", width=30, command=self._logout).grid(row=3, column=0, pady=6)

        # show profile completeness status
        user = find_user_record(self.current_user)
        status = "Incomplete"
        if user and user.get("profile_complete"):
            status = "Complete"
        ttk.Label(frame, text=f"Profile status: {status}", foreground="gray").pack(pady=(12,0))

        self._switch_frame(frame)

    def _logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out.")
        self.show_login_screen()

    # -----------------------
    # QUESTIONNAIRE SCREEN
    # -----------------------
    def show_questionnaire(self):
        frame = ttk.Frame(self.root, padding=12)
        ttk.Label(frame, text="Questionnaire", font=("Helvetica", 18, "bold")).pack(pady=(0,8))

        form = ttk.Frame(frame)
        form.pack(pady=6, fill="x")

        # Username 
        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky="w", pady=6)
        username_entry = ttk.Entry(form, width=30)
        username_entry.insert(0, self.current_user)
        username_entry.config(state="readonly")
        username_entry.grid(row=0, column=1, pady=6)

        # Zodiac
        ttk.Label(form, text="Zodiac sign:").grid(row=1, column=0, sticky="w", pady=6)
        self.zodiac_var = tk.StringVar()
        zodiac_cb = ttk.Combobox(form, textvariable=self.zodiac_var, values=ZODIAC_EXAMPLES, width=28)
        zodiac_cb.set("")  # empty default
        zodiac_cb.grid(row=1, column=1, pady=6)

        # Morning or night
        ttk.Label(form, text="Morning or Night:").grid(row=2, column=0, sticky="w", pady=6)
        self.mornnight_var = tk.StringVar()
        mn_cb = ttk.Combobox(form, textvariable=self.mornnight_var, values=["morning", "night"], width=28)
        mn_cb.set("")
        mn_cb.grid(row=2, column=1, pady=6)

        # Music
        ttk.Label(form, text="Preferred Music:").grid(row=3, column=0, sticky="w", pady=6)
        self.music_var = tk.IntVar(value=0)
        music_names = [name for name, val in MUSIC_OPTIONS]
        music_cb = ttk.Combobox(form, values=music_names, width=28)
        music_cb.grid(row=3, column=1, pady=6)

        # Activity
        ttk.Label(form, text="Favorite Activity:").grid(row=4, column=0, sticky="w", pady=6)
        activity_names = [name for name, val in ACTIVITY_OPTIONS]
        self.activity_var = tk.StringVar()
        activity_cb = ttk.Combobox(form, values=activity_names, textvariable=self.activity_var, width=28)
        activity_cb.grid(row=4, column=1, pady=6)

        # Personality
        ttk.Label(form, text="Personality:").grid(row=5, column=0, sticky="w", pady=6)
        personality_names = [name for name, val in PERSONALITY_OPTIONS]
        self.personality_var = tk.StringVar()
        personality_cb = ttk.Combobox(form, values=personality_names, textvariable=self.personality_var, width=28)
        personality_cb.grid(row=5, column=1, pady=6)

        # Mood
        ttk.Label(form, text="Mood:").grid(row=6, column=0, sticky="w", pady=6)
        mood_names = [name for name, val in MOOD_OPTIONS]
        self.mood_var = tk.StringVar()
        mood_cb = ttk.Combobox(form, values=mood_names, textvariable=self.mood_var, width=28)
        mood_cb.grid(row=6, column=1, pady=6)

        # Pre-fill if existing answers
        existing = find_user_record(self.current_user)
        if existing and existing.get("questionnaire"):
            q = existing["questionnaire"]
            self.zodiac_var.set(q.get("zodiac", ""))
            self.mornnight_var.set(q.get("morning_or_night", ""))

            # mapping numeric values back to names

            # music
            music_val = q.get("music")
            for name, val in MUSIC_OPTIONS:
                if val == music_val:
                    music_cb.set(name)
                    break
            # activity
            act_val = q.get("activity")
            for name, val in ACTIVITY_OPTIONS:
                if val == act_val:
                    activity_cb.set(name)
                    break
            # personality
            pers_val = q.get("personality")
            for name, val in PERSONALITY_OPTIONS:
                if val == pers_val:
                    personality_cb.set(name)
                    break
            # mood
            mood_val = q.get("mood")
            for name, val in MOOD_OPTIONS:
                if val == mood_val:
                    mood_cb.set(name)
                    break

        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(12,0))
        ttk.Button(btn_frame, text="Submit", command=lambda: self._submit_questionnaire(
            zodiac_cb.get(), mn_cb.get(), music_cb.get(), activity_cb.get(), personality_cb.get(), mood_cb.get()
        )).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="Back", command=self.show_main_menu).grid(row=0, column=1, padx=8)

        self._switch_frame(frame)

    def _submit_questionnaire(self, zodiac, mn, music_name, activity_name, personality_name, mood_name):

        # Validate

        if not zodiac or not mn or not music_name or not activity_name or not personality_name or not mood_name:
            messagebox.showwarning("Questionnaire", "Please fill all fields.")
            return

        # mapping names back to numeric codes the matching module expects

        music_val = next((val for name, val in MUSIC_OPTIONS if name == music_name), None)
        activity_val = next((val for name, val in ACTIVITY_OPTIONS if name == activity_name), None)
        personality_val = next((val for name, val in PERSONALITY_OPTIONS if name == personality_name), None)
        mood_val = next((val for name, val in MOOD_OPTIONS if name == mood_name), None)

        answers = {
            "zodiac": zodiac.lower(),
            "morning_or_night": mn.lower(),
            "music": music_val,
            "activity": activity_val,
            "personality": personality_val,
            "mood": mood_val
        }

        update_user_questionnaire(self.current_user, answers)
        messagebox.showinfo("Saved", "Your answers have been saved.")
        self.show_main_menu()

    # -----------------------
    # PROFILE VIEW
    # -----------------------

    def show_profile(self):
        user = find_user_record(self.current_user)
        frame = ttk.Frame(self.root, padding=12)
        ttk.Label(frame, text=f"Profile: {self.current_user}", font=("Helvetica", 18, "bold")).pack(pady=(0,8))

        if not user:
            ttk.Label(frame, text="User not found.").pack()
            ttk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=8)
            self._switch_frame(frame)
            return

        info_frame = ttk.Frame(frame)
        info_frame.pack(pady=8, fill="x")
        ttk.Label(info_frame, text=f"Username: {user['username']}").pack(anchor="w")
        ttk.Label(info_frame, text=f"Profile complete: {user.get('profile_complete', False)}").pack(anchor="w")

        q = user.get("questionnaire")
        if q:
            ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=6)
            ttk.Label(frame, text="Questionnaire answers:", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(6,0))
            ttk.Label(frame, text=f"Zodiac: {q.get('zodiac')}").pack(anchor="w")
            ttk.Label(frame, text=f"Morning/Night: {q.get('morning_or_night')}").pack(anchor="w")

            # display numeric options as names
            music_name = next((n for n, v in MUSIC_OPTIONS if v == q.get("music")), str(q.get("music")))
            activity_name = next((n for n, v in ACTIVITY_OPTIONS if v == q.get("activity")), str(q.get("activity")))
            personality_name = next((n for n, v in PERSONALITY_OPTIONS if v == q.get("personality")), str(q.get("personality")))
            mood_name = next((n for n, v in MOOD_OPTIONS if v == q.get("mood")), str(q.get("mood")))

            ttk.Label(frame, text=f"Music: {music_name}").pack(anchor="w")
            ttk.Label(frame, text=f"Activity: {activity_name}").pack(anchor="w")
            ttk.Label(frame, text=f"Personality: {personality_name}").pack(anchor="w")
            ttk.Label(frame, text=f"Mood: {mood_name}").pack(anchor="w")
        else:
            ttk.Label(frame, text="No questionnaire found.").pack()

        ttk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=12)
        self._switch_frame(frame)

    # -----------------------
    # MATCHES SCREEN
    # -----------------------
    def show_matches(self):
        matches = find_all_matches(self.current_user)
        frame = ttk.Frame(self.root, padding=12)
        ttk.Label(frame, text="Matches", font=("Helvetica", 18, "bold")).pack(pady=(0,8))

        if not matches:
            ttk.Label(frame, text="No matches found or your profile is incomplete.").pack(pady=8)
            ttk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=8)
            self._switch_frame(frame)
            return

        # Treeview for match list

        cols = ("username", "score", "zodiac", "morning_night")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=12)
        tree.heading("username", text="Username")
        tree.heading("score", text="Score")
        tree.heading("zodiac", text="Zodiac")
        tree.heading("morning_night", text="Morning/Night")
        tree.column("username", width=160, anchor="w")
        tree.column("score", width=80, anchor="center")
        tree.column("zodiac", width=120, anchor="center")
        tree.column("morning_night", width=120, anchor="center")
        tree.pack(pady=8, fill="x")

        for m in matches:
            tree.insert("", tk.END, values=(m["username"], m["score"], m.get("zodiac", ""), m.get("morning_or_night", "")))

        # Buttons

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Back", command=self.show_main_menu).grid(row=0, column=0, padx=8)
        ttk.Button(btn_frame, text="View Selected Profile", command=lambda: self._view_selected_profile(tree)).grid(row=0, column=1, padx=8)

        self._switch_frame(frame)

    def _view_selected_profile(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Please select a match to view profile.")
            return
        values = tree.item(sel[0])["values"]
        username = values[0]

        # show profile popup for that username

        user = find_user_record(username)
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        popup = tk.Toplevel(self.root)
        popup.title(f"{username} - Profile")
        popup.geometry("380x300")
        ttk.Label(popup, text=f"Profile: {username}", font=("Helvetica", 14, "bold")).pack(pady=(8,6))

        q = user.get("questionnaire")
        if q:
            ttk.Label(popup, text=f"Zodiac: {q.get('zodiac')}").pack(anchor="w", padx=12, pady=4)
            ttk.Label(popup, text=f"Morning/Night: {q.get('morning_or_night')}").pack(anchor="w", padx=12, pady=4)
            music_name = next((n for n, v in MUSIC_OPTIONS if v == q.get("music")), str(q.get("music")))
            activity_name = next((n for n, v in ACTIVITY_OPTIONS if v == q.get("activity")), str(q.get("activity")))
            personality_name = next((n for n, v in PERSONALITY_OPTIONS if v == q.get("personality")), str(q.get("personality")))
            mood_name = next((n for n, v in MOOD_OPTIONS if v == q.get("mood")), str(q.get("mood")))
            ttk.Label(popup, text=f"Music: {music_name}").pack(anchor="w", padx=12, pady=4)
            ttk.Label(popup, text=f"Activity: {activity_name}").pack(anchor="w", padx=12, pady=4)
            ttk.Label(popup, text=f"Personality: {personality_name}").pack(anchor="w", padx=12, pady=4)
            ttk.Label(popup, text=f"Mood: {mood_name}").pack(anchor="w", padx=12, pady=4)
        else:
            ttk.Label(popup, text="No questionnaire available.").pack(padx=12, pady=12)

        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=12)

# ---------------------------
# Run the app
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FriendMatchmakerGUI(root)
    root.mainloop()
