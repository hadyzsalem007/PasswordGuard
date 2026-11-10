
import customtkinter as ctk
import re

# ==============================
# PASSGUARD V4.0 FINAL
# ==============================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1120"
CARD = "#151F32"
ACCENT = "#38BDF8"
GREEN = "#22C55E"
RED = "#EF4444"
YELLOW = "#F59E0B"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"

COMMON_PASSWORDS = {
    "password", "password123", "12345678",
    "123456789", "qwerty123", "admin123",
    "welcome123", "iloveyou"
}


class PassGuard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("PassGuard V4.0 | Password Security")
        self.geometry("850x760")
        self.minsize(700, 680)
        self.configure(fg_color=BG)

        self.show_password = False

        self.build_ui()

    # ==============================
    # USER INTERFACE
    # ==============================

    def build_ui(self):

        self.header = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        self.header.pack(fill="x", padx=35, pady=(25, 10))

        ctk.CTkLabel(
            self.header,
            text="PASSGUARD",
            font=("Arial", 32, "bold"),
            text_color=ACCENT
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.header,
            text="PASSWORD SECURITY ANALYZER  |  V4.0 FINAL",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(anchor="w", pady=(3, 0))

        self.main_card = ctk.CTkFrame(
            self,
            fg_color=CARD,
            corner_radius=18
        )
        self.main_card.pack(
            fill="both", expand=True,
            padx=35, pady=15
        )

        ctk.CTkLabel(
            self.main_card,
            text="Analyze Your Password",
            font=("Arial", 23, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            self.main_card,
            text="Enter your password to check its basic security properties.",
            font=("Arial", 12),
            text_color=MUTED
        ).pack(anchor="w", padx=25, pady=(0, 20))

        # Password input

        self.password_entry = ctk.CTkEntry(
            self.main_card,
            placeholder_text="Enter password...",
            height=45,
            show="*",
            font=("Arial", 14),
            corner_radius=10
        )
        self.password_entry.pack(
            fill="x", padx=25, pady=7
        )

        self.confirm_entry = ctk.CTkEntry(
            self.main_card,
            placeholder_text="Confirm password...",
            height=45,
            show="*",
            font=("Arial", 14),
            corner_radius=10
        )
        self.confirm_entry.pack(
            fill="x", padx=25, pady=7
        )

        self.show_var = ctk.BooleanVar(value=False)

        self.show_checkbox = ctk.CTkCheckBox(
            self.main_card,
            text="Show password",
            variable=self.show_var,
            command=self.toggle_password,
            font=("Arial", 12),
            text_color=MUTED
        )
        self.show_checkbox.pack(
            anchor="w", padx=25, pady=10
        )

        # Buttons

        self.button_frame = ctk.CTkFrame(
            self.main_card,
            fg_color="transparent"
        )
        self.button_frame.pack(
            fill="x", padx=25, pady=12
        )

        self.analyze_button = ctk.CTkButton(
            self.button_frame,
            text="ANALYZE PASSWORD",
            height=45,
            fg_color=ACCENT,
            hover_color="#0284C7",
            text_color="#07111F",
            font=("Arial", 14, "bold"),
            corner_radius=10,
            command=self.analyze
        )
        self.analyze_button.pack(
            side="left", fill="x", expand=True, padx=(0, 7)
        )

        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="CLEAR",
            height=45,
            width=100,
            fg_color="#334155",
            hover_color="#475569",
            font=("Arial", 13, "bold"),
            corner_radius=10,
            command=self.clear
        )
        self.clear_button.pack(side="right")

        # Results section

        self.results = ctk.CTkFrame(
            self.main_card,
            fg_color="#0F172A",
            corner_radius=14
        )
        self.results.pack(
            fill="both", expand=True,
            padx=25, pady=(10, 20)
        )

        ctk.CTkLabel(
            self.results,
            text="SECURITY ANALYSIS",
            font=("Arial", 15, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(18, 12))

        self.strength_label = ctk.CTkLabel(
            self.results,
            text="Waiting for analysis...",
            font=("Arial", 20, "bold"),
            text_color=MUTED
        )
        self.strength_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(
            self.results,
            text="Security Score: -- / 5",
            font=("Arial", 13),
            text_color=TEXT
        )
        self.score_label.pack(pady=5)

        self.progress = ctk.CTkProgressBar(
            self.results,
            height=12,
            progress_color=ACCENT
        )
        self.progress.pack(
            fill="x", padx=25, pady=12
        )
        self.progress.set(0)

        self.details_label = ctk.CTkLabel(
            self.results,
            text="",
            font=("Arial", 13),
            text_color=TEXT,
            justify="left"
        )
        self.details_label.pack(
            anchor="w", padx=25, pady=8
        )

        self.tips_label = ctk.CTkLabel(
            self.results,
            text="Your security recommendations will appear here.",
            font=("Arial", 12),
            text_color=MUTED,
            justify="left",
            wraplength=650
        )
        self.tips_label.pack(
            anchor="w", padx=25, pady=(8, 15)
        )

        # Footer

        ctk.CTkLabel(
            self,
            text="LOCAL ANALYSIS • NO PASSWORD STORAGE • PASSGUARD V4.0",
            font=("Arial", 10),
            text_color=MUTED
        ).pack(pady=(0, 15))

    # ==============================
    # SHOW / HIDE PASSWORD
    # ==============================

    def toggle_password(self):

        if self.show_var.get():
            self.password_entry.configure(show="")
            self.confirm_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")
            self.confirm_entry.configure(show="*")

    # ==============================
    # PASSWORD ANALYSIS
    # ==============================

    def analyze(self):

        password = self.password_entry.get()
        confirmation = self.confirm_entry.get()

        if not password:
            self.show_error("Password cannot be empty!")
            return

        if not confirmation:
            self.show_error("Please confirm your password!")
            return

        if password != confirmation:
            self.show_error("Passwords do not match!")
            return

        length = len(password)

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)

        common = password.lower() in COMMON_PASSWORDS

        score = 0

        if length >= 12:
            score += 1

        if has_upper:
            score += 1

        if has_lower:
            score += 1

        if has_digit:
            score += 1

        if has_symbol:
            score += 1

        # Basic strength classification

        if common or length < 8:
            strength = "WEAK"
            color = RED

        elif length >= 12 and score >= 4:
            strength = "STRONG"
            color = GREEN

        elif length >= 8 and score >= 3:
            strength = "MEDIUM"
            color = YELLOW

        else:
            strength = "WEAK"
            color = RED

        self.display_results(
            length,
            has_upper,
            has_lower,
            has_digit,
            has_symbol,
            score,
            strength,
            color,
            common
        )

    # ==============================
    # DISPLAY RESULTS
    # ==============================

    def display_results(
        self, length, upper, lower, digit,
        symbol, score, strength, color, common
    ):

        self.strength_label.configure(
            text=f"STRENGTH: {strength}",
            text_color=color
        )

        self.score_label.configure(
            text=f"Security Score: {score} / 5"
        )

        self.progress.set(score / 5)
        self.progress.configure(progress_color=color)

        details = (
            f"Password Length: {length} characters\n\n"
            f"{'✓' if length >= 12 else '✗'} Length: At least 12 characters\n"
            f"{'✓' if upper else '✗'} Uppercase letters\n"
            f"{'✓' if lower else '✗'} Lowercase letters\n"
            f"{'✓' if digit else '✗'} Numbers\n"
            f"{'✓' if symbol else '✗'} Special symbols"
        )

        self.details_label.configure(text=details)

        tips = []

        if common:
            tips.append("- This password matches a common password in our small local list.")

        if length < 12:
            tips.append("- Use a longer password (at least 12 characters).")

        if not upper:
            tips.append("- Consider adding uppercase letters.")

        if not lower:
            tips.append("- Consider adding lowercase letters.")

        if not digit:
            tips.append("- Consider adding numbers.")

        if not symbol:
            tips.append("- Consider adding special symbols.")

        if not tips:
            tips.append("- Your password meets all our basic checks.")

        tips_text = "\n".join(tips)

        self.tips_label.configure(
            text="SECURITY RECOMMENDATIONS\n\n" + tips_text,
            text_color=MUTED
        )

    # ==============================
    # ERROR DISPLAY
    # ==============================

    def show_error(self, message):

        self.strength_label.configure(
            text=message,
            text_color=RED
        )

        self.score_label.configure(
            text="Security Score: -- / 5"
        )

        self.progress.set(0)

        self.details_label.configure(text="")
        self.tips_label.configure(
            text="Please correct the input and try again."
        )

    # ==============================
    # CLEAR INPUTS
    # ==============================

    def clear(self):

        self.password_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")

        self.strength_label.configure(
            text="Waiting for analysis...",
            text_color=MUTED
        )

        self.score_label.configure(
            text="Security Score: -- / 5"
        )

        self.progress.set(0)
        self.details_label.configure(text="")
        self.tips_label.configure(
            text="Your security recommendations will appear here."
        )

        self.password_entry.focus()


# ==============================
# RUN APPLICATION
# ==============================

if __name__ == "__main__":

    app = PassGuard()
    app.mainloop()
