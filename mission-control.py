#!/usr/bin/env python3
"""
🦾 Francois — Mission Control
Desktop-App zum Überwachen von Francois' Status.
Liest status.json und zeigt ein Live-Dashboard.
"""

import json
import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path
from datetime import datetime

STATUS_FILE = Path(__file__).parent / "status.json"
REFRESH_MS = 5000

# Colors
BG = "#0a0e1a"
CARD = "#131a2e"
BORDER = "#1e2a4a"
ACCENT = "#4fc3f7"
GREEN = "#66bb6a"
ORANGE = "#ffa726"
RED = "#ef5350"
TEXT = "#e0e6f0"
MUTED = "#7888a0"


class MissionControl(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🦾 Francois — Mission Control")
        self.configure(bg=BG)
        self.geometry("700x800")
        self.minsize(600, 700)

        # Fonts
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.heading_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        self.body_font = tkfont.Font(family="Segoe UI", size=10)
        self.small_font = tkfont.Font(family="Segoe UI", size=9)
        self.mono_font = tkfont.Font(family="Courier", size=9)
        self.task_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")

        self.build_ui()
        self.refresh()

    def build_ui(self):
        # Scrollable canvas
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.main_frame = tk.Frame(canvas, bg=BG)

        self.main_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        # Header
        header = tk.Frame(self.main_frame, bg=BG)
        header.pack(fill="x", pady=(0, 15))

        tk.Label(header, text="🦾 Francois", font=self.title_font,
                 bg=BG, fg=ACCENT).pack(side="left")

        self.status_label = tk.Label(header, text="● Online", font=self.heading_font,
                                      bg=BG, fg=GREEN)
        self.status_label.pack(side="right")

        # Separator
        tk.Frame(self.main_frame, bg=BORDER, height=1).pack(fill="x", pady=(0, 15))

        # Current Task Card
        self.task_card = self.make_card("📌 AKTUELLE AUFGABE")
        self.task_label = tk.Label(self.task_card, text="Lade...", font=self.task_font,
                                    bg=CARD, fg=ACCENT, wraplength=600, justify="left")
        self.task_label.pack(anchor="w")
        self.task_meta = tk.Label(self.task_card, text="", font=self.small_font,
                                   bg=CARD, fg=MUTED)
        self.task_meta.pack(anchor="w", pady=(5, 0))

        # System Info Card
        sys_card = self.make_card("🖥️ SYSTEM")
        self.sys_labels = {}
        for key, label in [("model", "Modell"), ("sandbox", "Sandbox"),
                           ("uptime", "Uptime"), ("lastUpdate", "Letztes Update")]:
            row = tk.Frame(sys_card, bg=CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, font=self.body_font, bg=CARD, fg=MUTED,
                     width=15, anchor="w").pack(side="left")
            val = tk.Label(row, text="—", font=self.body_font, bg=CARD, fg=TEXT, anchor="w")
            val.pack(side="left", fill="x")
            self.sys_labels[key] = val

        # Health Card
        health_card = self.make_card("💚 SYSTEM HEALTH")
        self.health_frame = tk.Frame(health_card, bg=CARD)
        self.health_frame.pack(fill="x")

        # Tools
        tk.Label(health_card, text="🧰 TOOLS", font=self.small_font,
                 bg=CARD, fg=MUTED).pack(anchor="w", pady=(10, 5))
        self.tools_frame = tk.Frame(health_card, bg=CARD)
        self.tools_frame.pack(fill="x")

        # Activity Card
        activity_card = self.make_card("📋 LETZTE AKTIVITÄTEN")
        self.activity_frame = tk.Frame(activity_card, bg=CARD)
        self.activity_frame.pack(fill="x")

        # Goals Card
        goals_card = self.make_card("🎯 ZIELE")
        self.goals_frame = tk.Frame(goals_card, bg=CARD)
        self.goals_frame.pack(fill="x")

        # Footer
        self.refresh_label = tk.Label(self.main_frame, text="Auto-refresh alle 5s",
                                       font=self.small_font, bg=BG, fg=MUTED)
        self.refresh_label.pack(pady=(10, 0))

    def make_card(self, title):
        outer = tk.Frame(self.main_frame, bg=BORDER, padx=1, pady=1)
        outer.pack(fill="x", pady=(0, 12))
        card = tk.Frame(outer, bg=CARD, padx=15, pady=12)
        card.pack(fill="x")
        tk.Label(card, text=title, font=self.small_font, bg=CARD, fg=MUTED).pack(anchor="w", pady=(0, 8))
        return card

    def refresh(self):
        try:
            data = json.loads(STATUS_FILE.read_text())
            self.render(data)
        except Exception as e:
            self.status_label.config(text="● Offline", fg=RED)
            self.task_label.config(text=f"Fehler: {e}")

        self.after(REFRESH_MS, self.refresh)

    def render(self, d):
        # Status
        if d.get("status") == "online":
            mood = d.get("mood", "")
            self.status_label.config(text=f"● Online {mood}", fg=GREEN)
        else:
            self.status_label.config(text="● Offline", fg=RED)

        # Task
        self.task_label.config(text=d.get("currentTask", "Nichts gerade"))
        ts = d.get("lastUpdate", "")
        try:
            t = datetime.fromisoformat(ts).strftime("%H:%M:%S")
            self.task_meta.config(text=f"Letztes Update: {t}")
        except:
            self.task_meta.config(text=f"Update: {ts}")

        # System
        self.sys_labels["model"].config(text=d.get("model", "—"))
        sb = "✅ Aktiv" if d.get("sandbox") else "❌ Aus"
        self.sys_labels["sandbox"].config(text=sb)
        self.sys_labels["uptime"].config(text=d.get("uptime", "—"))
        try:
            t = datetime.fromisoformat(ts).strftime("%d.%m.%Y %H:%M")
            self.sys_labels["lastUpdate"].config(text=t)
        except:
            self.sys_labels["lastUpdate"].config(text=ts)

        # Health
        for w in self.health_frame.winfo_children():
            w.destroy()
        health = d.get("systemHealth", {})
        row_frame = None
        for i, (k, v) in enumerate([(k, v) for k, v in health.items() if k != "tools"]):
            if i % 2 == 0:
                row_frame = tk.Frame(self.health_frame, bg=CARD)
                row_frame.pack(fill="x", pady=1)
            color = GREEN if v in ("ok", "active") else ORANGE if "TODO" in str(v) else GREEN
            item = tk.Frame(row_frame, bg=CARD)
            item.pack(side="left", fill="x", expand=True, anchor="w")
            tk.Label(item, text="●", font=self.small_font, bg=CARD, fg=color).pack(side="left")
            tk.Label(item, text=f" {k}: {v}", font=self.small_font,
                     bg=CARD, fg=TEXT).pack(side="left")

        # Tools
        for w in self.tools_frame.winfo_children():
            w.destroy()
        tools = health.get("tools", [])
        for t in tools:
            lbl = tk.Label(self.tools_frame, text=f" {t} ", font=self.mono_font,
                           bg="#0d1a2e", fg=ACCENT, padx=6, pady=2,
                           relief="solid", borderwidth=1)
            lbl.pack(side="left", padx=(0, 5), pady=2)

        # Activity
        for w in self.activity_frame.winfo_children():
            w.destroy()
        for a in d.get("recentActivity", []):
            row = tk.Frame(self.activity_frame, bg=CARD)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=a.get("time", ""), font=self.mono_font,
                     bg=CARD, fg=ACCENT, width=6, anchor="w").pack(side="left")
            tk.Label(row, text=a.get("action", ""), font=self.small_font,
                     bg=CARD, fg=TEXT, anchor="w").pack(side="left", fill="x")

        # Goals
        for w in self.goals_frame.winfo_children():
            w.destroy()
        for g in d.get("goals", []):
            tk.Label(self.goals_frame,
                     text=f'{g.get("icon", "")} {g.get("name", "")}',
                     font=self.body_font, bg=CARD, fg=TEXT,
                     anchor="w").pack(anchor="w", pady=1)

        # Refresh time
        self.refresh_label.config(
            text=f"Auto-refresh alle 5s · {datetime.now().strftime('%H:%M:%S')}")


if __name__ == "__main__":
    app = MissionControl()
    app.mainloop()
