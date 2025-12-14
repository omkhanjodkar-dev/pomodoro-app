import tkinter as tk
from tkinter import ttk
import time
import random
import os
import pygame

# Sample distraction log
log_data = [
    "Instagram opened at 10:42 AM — Intervention: Auto-close triggered",
    "YouTube opened at 3:15 PM — Intervention: Nudge alert shown",
    "Netflix opened at 9:00 PM — Intervention: Auto-close triggered",
    "Twitter opened at 11:30 AM — Intervention: Dim screen applied",
    "YouTube opened at 4:05 PM — Intervention: Auto-close triggered",
    "Instagram opened at 2:20 PM — Intervention: Nudge alert shown"
]

# -------------------- Focus Dashboard --------------------
class FocusApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Dashboard")
        self.root.geometry("420x620")
        self.theme = tk.StringVar(value="Dark")
        self.focus_mode = tk.BooleanVar()
        self.timer_running = False
        self.time_left = 25 * 60
        self.style = ttk.Style()
        self.configure_theme()
        self.build_ui()

    def configure_theme(self):
        theme = self.theme.get()
        if theme == "Dark":
            self.bg = "#1e1e2f"
            self.fg = "#f8f8f2"
            self.accent = "#ff79c6"
            self.label = "#8be9fd"
            self.summary = "#f1fa8c"
        else:
            self.bg = "#ffffff"
            self.fg = "#1e1e2f"
            self.accent = "#007acc"
            self.label = "#333333"
            self.summary = "#444444"
        self.root.configure(bg=self.bg)
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 11), padding=6)
        self.style.configure("TCheckbutton", background=self.bg, foreground=self.fg, font=("Helvetica", 11))
        self.style.configure("TMenubutton", background=self.bg, foreground=self.fg)

    def build_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        theme_frame = tk.Frame(self.root, bg=self.bg)
        theme_frame.pack(pady=10)
        tk.Label(theme_frame, text="Theme:", bg=self.bg, fg=self.fg, font=("Helvetica", 11)).pack(side="left")
        ttk.OptionMenu(theme_frame, self.theme, self.theme.get(), "Dark", "Light", command=self.switch_theme).pack(side="left")

        tk.Label(self.root, text="🎯 Focus Dashboard", font=("Helvetica", 18, "bold"), bg=self.bg, fg=self.fg).pack(pady=10)
        ttk.Checkbutton(self.root, text="Enable Focus Mode", variable=self.focus_mode).pack(pady=10)

        self.start_button = ttk.Button(self.root, text="Start Session", command=self.toggle_timer)
        self.start_button.pack(pady=10)

        self.timer_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 36, "bold"), bg=self.bg, fg=self.accent)
        self.timer_label.pack(pady=20)

        tk.Label(self.root, text="📊 Session Summary", font=("Helvetica", 14, "bold"), bg=self.bg, fg=self.label).pack(pady=10)
        summary_frame = tk.Frame(self.root, bg=self.bg)
        summary_frame.pack()
        self.time_focused_label = tk.Label(summary_frame, text="Time Focused: 0 min", bg=self.bg, fg=self.summary, font=("Helvetica", 11))
        self.time_focused_label.pack(anchor="w")
        self.distractions_label = tk.Label(summary_frame, text="Distractions Blocked: 0", bg=self.bg, fg=self.summary, font=("Helvetica", 11))
        self.distractions_label.pack(anchor="w")
        self.productivity_label = tk.Label(summary_frame, text="Productivity Score: 0%", bg=self.bg, fg=self.summary, font=("Helvetica", 11))
        self.productivity_label.pack(anchor="w")

        tk.Label(self.root, text="⚡ Quick Actions", font=("Helvetica", 14, "bold"), bg=self.bg, fg=self.label).pack(pady=10)
        ttk.Button(self.root, text="Start Study Session", command=self.start_study_session).pack(pady=5)
        ttk.Button(self.root, text="View Distraction History", command=self.view_distractions).pack(pady=5)
        ttk.Button(self.root, text="Customize Block List", command=self.open_settings).pack(pady=5)
        ttk.Button(self.root, text="Gamification & Rewards", command=self.open_gamification).pack(pady=5)
        ttk.Button(self.root, text="Open Timer Screen", command=self.open_timer_screen).pack(pady=5)

    def switch_theme(self, *_):
        self.configure_theme()
        self.build_ui()

    def format_time(self, seconds):
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def update_timer(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=self.format_time(self.time_left))
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            self.start_button.config(text="Start Session")
            self.time_focused_label.config(text="Time Focused: 25 min")
            self.distractions_label.config(text="Distractions Blocked: 3")
            self.productivity_label.config(text="Productivity Score: 85%")

    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(text="Stop Session")
            self.update_timer()
        else:
            self.timer_running = False
            self.start_button.config(text="Start Session")

    def start_study_session(self):
        print("Study session started!")

    def view_distractions(self):
        DistractionLogViewer(self.root, log_data)

    def open_settings(self):
        SettingsPanel(self.root)

    def open_gamification(self):
        GamificationPanel(self.root)

    def open_timer_screen(self):
        TimerScreen(tk.Toplevel(self.root))

# -------------------- Timer Screen --------------------
class TimerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Timer")
        self.root.geometry("420x500")
        self.root.configure(bg="#1e1e2f")
        self.time_left = 25 * 60
        self.timer_running = False
        self.paused = False
        self.music_on = tk.BooleanVar(value=False)
        self.quotes = [
            "Stay focused and never give up.",
            "Small steps lead to big results.",
            "Discipline is the bridge to success.",
            "Your future is created by what you do today.",
            "Push yourself, because no one else will."
        ]
        self.build_ui()

    def build_ui(self):
        self.timer_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 36, "bold"), bg="#1e1e2f", fg="#ff79c6")
        self.timer_label.pack(pady=20)
        self.quote_label = tk.Label(self.root, text=random.choice(self.quotes), font=("Helvetica", 12, "italic"), wraplength=360, bg="#1e1e2f", fg="#8be9fd")
        self.quote_label.pack(pady=10)
        self.progress = ttk.Progressbar(self.root, length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.progress["maximum"] = self.time_left
        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Pause", command=self.pause_timer).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Resume", command=self.resume_timer).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="End", command=self.end_timer).grid(row=0, column=2, padx=5)
        ttk.Checkbutton(self.root, text="Play Background Music", variable=self.music_on, command=self.toggle_music).pack(pady=10)

    def format_time(self, seconds):
        return f"{seconds // 60:02}:{seconds % 60:02}"

    def update_timer(self):
        if self.timer_running and not self.paused and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=self.format_time(self.time_left))
            self.progress["value"] = 25 * 60 - self.time_left
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.timer_running = False
            self.timer_label.config(text="00:00")
            self.quote_label.config(text="Session Complete! Great job 🎉")
            #pygame.mixer.music.stop()

    def pause_timer(self):
        self.paused = True

    def resume_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
        self.paused = False

    def end_timer(self):
        self.timer_running = False
        self.time_left = 25 * 60
        self.timer_label.config(text=self.format_time(self.time_left))
        self.progress["value"] = 0
        self.quote_label.config(text=random.choice(self.quotes))
        #pygame.mixer.music.stop()

    '''def toggle_music(self):
        music_path = "background.mp3"
        if self.music_on.get():
            if os.path.exists(music_path):
                pygame.mixer.init()
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)
            else:
                self.quote_label.config(text="⚠️ Music file not found.")
        else:
            pygame.mixer.music.stop()'''
class SettingsPanel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("🛠️ Settings")
        self.geometry("420x540")
        self.configure(bg="#fdf6f0")

        style = ttk.Style(self)
        style.configure("TLabel", background="#fdf6f0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TCheckbutton", background="#fdf6f0", font=("Segoe UI", 10))
        style.configure("TRadiobutton", background="#fdf6f0", font=("Segoe UI", 10))

        ttk.Label(self, text="Customize Your Experience", font=("Segoe UI", 14, "bold")).pack(pady=10)

        section = ttk.LabelFrame(self, text="Blocked Apps/Sites", padding=10)
        section.pack(fill="x", padx=20, pady=10)
        self.blocked_entry = ttk.Entry(section, width=40)
        self.blocked_entry.insert(0, "Instagram, YouTube, Netflix")
        self.blocked_entry.pack(pady=5)
        ttk.Button(section, text="Save Block List", command=self.save_blocked).pack()

        section = ttk.LabelFrame(self, text="Intervention Style", padding=10)
        section.pack(fill="x", padx=20, pady=10)
        self.intervention_var = tk.StringVar(value="nudge")
        for style in ["nudge", "auto-close", "dim"]:
            ttk.Radiobutton(section, text=style.capitalize(), variable=self.intervention_var, value=style).pack(anchor="w")

        section = ttk.LabelFrame(self, text="Accessibility", padding=10)
        section.pack(fill="x", padx=20, pady=10)
        ttk.Label(section, text="Font Style:").pack(anchor="w")
        self.font_var = tk.StringVar(value="Segoe UI")
        ttk.Combobox(section, textvariable=self.font_var, values=["Segoe UI", "Arial", "Comic Sans", "OpenDyslexic"]).pack(fill="x", pady=5)
        self.color_mode = tk.BooleanVar()
        ttk.Checkbutton(section, text="Enable Neurodiverse Color Mode", variable=self.color_mode).pack(anchor="w", pady=5)

        section = ttk.LabelFrame(self, text="Language & Theme Preferences", padding=10)
        section.pack(fill="x", padx=20, pady=10)
        ttk.Label(section, text="Language:").pack(anchor="w")
        self.language_var = tk.StringVar(value="English")
        ttk.Combobox(section, textvariable=self.language_var, values=["English", "Hindi", "Marathi", "Spanish"]).pack(fill="x", pady=5)
        ttk.Label(section, text="Theme:").pack(anchor="w")
        self.theme_var = tk.StringVar(value="Light")
        ttk.Combobox(section, textvariable=self.theme_var, values=["Light", "Dark", "Pastel"]).pack(fill="x", pady=5)

        ttk.Button(self, text="Apply Settings", command=self.apply_settings).pack(pady=20)

    def save_blocked(self):
        print("Blocked apps/sites saved:", self.blocked_entry.get())

    def apply_settings(self):
        print("Intervention style:", self.intervention_var.get())
        print("Font:", self.font_var.get())
        print("Neurodiverse mode:", self.color_mode.get())
        print("Language:", self.language_var.get())
        print("Theme:", self.theme_var.get())
        self.destroy()
class GamificationPanel(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("🎮 Gamification & Rewards")
        self.geometry("440x540")
        self.configure(bg="#fdf6f0")

        style = ttk.Style(self)
        style.configure("TLabel", background="#fdf6f0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TProgressbar", thickness=20)

        ttk.Label(self, text="Your Progress & Achievements", font=("Segoe UI", 14, "bold")).pack(pady=10)

        badge_frame = ttk.LabelFrame(self, text="Badges Earned", padding=10)
        badge_frame.pack(fill="x", padx=20, pady=10)
        badges = [
            ("🎯 Focus Streak", "Completed 5 days in a row"),
            ("⏳ Deep Work", "1 hour uninterrupted"),
            ("🚫 Distraction Blocker", "Blocked 10 apps")
        ]
        for icon, desc in badges:
            ttk.Label(badge_frame, text=f"{icon} {desc}").pack(anchor="w", pady=2)

        xp_frame = ttk.LabelFrame(self, text="XP Progress", padding=10)
        xp_frame.pack(fill="x", padx=20, pady=10)
        ttk.Label(xp_frame, text="Level 3 — Productivity Ninja").pack(anchor="w")
        self.xp_bar = ttk.Progressbar(xp_frame, maximum=100, value=65)
        self.xp_bar.pack(fill="x", pady=5)
        ttk.Label(xp_frame, text="65 / 100 XP").pack(anchor="e")
        ttk.Label(xp_frame, text="+15 XP today").pack(anchor="e")

        leaderboard_frame = ttk.LabelFrame(self, text="Leaderboard", padding=10)
        leaderboard_frame.pack(fill="x", padx=20, pady=10)
        leaderboard = [("Swara", 320), ("Aarav", 290), ("Mira", 270)]
        for rank, (name, score) in enumerate(leaderboard, start=1):
            highlight = "⭐" if name == "Swara" else ""
            ttk.Label(leaderboard_frame, text=f"{rank}. {name} — {score} XP {highlight}").pack(anchor="w")

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=20)
class DistractionLogViewer(tk.Toplevel):
    def __init__(self, master, log_entries):
        super().__init__(master)
        self.title("🚫 Distraction Intervention Log")
        self.geometry("600x500")
        self.configure(bg="#fdf6f0")

        ttk.Label(self, text="Weekly Distraction Report", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        canvas = tk.Canvas(frame, bg="#fdf6f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, entry in enumerate(log_entries, start=1):
            ttk.Label(scroll_frame, text=f"{i}. {entry}", wraplength=540).pack(anchor="w", pady=4)

        ttk.Label(self, text="Summary", font=("Segoe UI", 12, "bold")).pack(pady=10)
        summary = self.generate_summary(log_entries)
        for line in summary:
            ttk.Label(self, text=line, wraplength=560).pack(anchor="w", padx=20)

        ttk.Button(self, text="Close", command=self.destroy).pack(pady=20)

    def generate_summary(self, entries):
        auto_close = sum("Auto-close" in e for e in entries)
        nudges = sum("Nudge" in e for e in entries)
        dimmed = sum("Dim" in e for e in entries)
        
    def generate_summary(self, entries):
        auto_close = sum("Auto-close" in e for e in entries)
        nudges = sum("Nudge" in e for e in entries)
        dimmed = sum("Dim" in e for e in entries)
        app_counts = {}
        for e in entries:
            app = e.split()[0]
            app_counts[app] = app_counts.get(app, 0) + 1
        most_common = max(app_counts, key=app_counts.get)
        return [
            f"• Total distractions detected: {len(entries)}",
            f"• Auto-closures executed: {auto_close}",
            f"• Nudges delivered: {nudges}",
            f"• Dim interventions: {dimmed}",
            f"• Most frequent distraction: {most_common} ({app_counts[most_common]} times)"
        ]
if __name__ == "__main__":
    root = tk.Tk()
    app = FocusApp(root)
    root.mainloop()

