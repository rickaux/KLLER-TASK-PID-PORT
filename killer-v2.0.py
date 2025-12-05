import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import winreg


# ============================================================
# SYSTEM THEME DETECT
# ============================================================
def get_system_theme():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "light" if value == 1 else "dark"
    except:
        return "light"


# ============================================================
# PALETTES (CUSTOMIZABLE)
# ============================================================
palette_light = {
    "bg": "#F5F6FA",
    "surface": "#FFFFFF",
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
    "text": "#1e1e24",
    "text_secondary": "#4f4f57",
    "border": "#D1D5DB",
}

palette_dark = {
    "bg": "#0d1117",
    "surface": "#161b22",
    "primary": "#238636",
    "primary_hover": "#2ea043",
    "text": "#c9d1d9",
    "text_secondary": "#8b949e",
    "border": "#30363d",
}

palette_custom = {
    "bg": "#1a1a1d",
    "surface": "#222226",
    "primary": "#9b5de5",
    "primary_hover": "#b97bff",
    "text": "#e3e3e8",
    "text_secondary": "#c0c0c7",
    "border": "#3a3a3f",
}


current_palette = palette_dark


# ============================================================
# APPLY PALETTE
# ============================================================
def apply_palette(root, pal):
    global current_palette
    current_palette = pal

    root.configure(bg=pal["bg"])

    for w in root.winfo_children():
        apply_to_widget(w, pal)


def apply_to_widget(widget, pal):
    cls = widget.winfo_class()

    if cls == "Frame":
        widget.configure(bg=pal["bg"])

    elif cls == "Label":
        widget.configure(bg=pal["bg"], fg=pal["text"])

    elif cls == "Button":
        widget.configure(
            bg=pal["primary"],
            fg=pal["text"],
            activebackground=pal["primary_hover"],
            activeforeground=pal["text"],
            bd=0,
            relief="flat",
            padx=10, pady=6,
            highlightthickness=0
        )

    elif cls == "Treeview":
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=pal["surface"],
            foreground=pal["text"],
            fieldbackground=pal["surface"],
            bordercolor=pal["border"],
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=pal["surface"],
            foreground=pal["text"],
            borderwidth=0
        )

    # recursive apply
    for child in widget.winfo_children():
        apply_to_widget(child, pal)


# ============================================================
# PORT LOGIC
# ============================================================
def find_listening_ports():
    conns = psutil.net_connections(kind="inet")
    result = []
    for c in conns:
        if not c.laddr or c.pid is None:
            continue
        if c.status in ("LISTEN", "ESTABLISHED"):
            try:
                name = psutil.Process(c.pid).name()
            except:
                name = "?"
            result.append((c.laddr.port, c.pid, name))
    return sorted(set(result))


def refresh():
    for i in tree.get_children():
        tree.delete(i)
    for port, pid, name in find_listening_ports():
        tree.insert("", "end", values=(port, pid, name))


def kill_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info", "Pilih proses dulu")
        return
    for s in sel:
        port, pid, name = tree.item(s, "values")
        try:
            psutil.Process(int(pid)).kill()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal kill PID {pid}: {e}")
    refresh()


# ============================================================
# UI MAIN
# ============================================================
root = tk.Tk()
root.title("ArduxLab Port Killer — Modern UI")
root.geometry("700x450")
root.minsize(700, 450)

apply_palette(root, palette_dark)


# NAVBAR ======================================================
navbar = tk.Frame(root, height=50, bg=current_palette["surface"])
navbar.pack(fill="x")

title = tk.Label(
    navbar, text="🔧 ArduxLab Port Killer", font=("Segoe UI", 14, "bold"),
    bg=current_palette["surface"], fg=current_palette["text"]
)
title.pack(side="left", padx=12)

# HAMBURGER MENU
def toggle_menu():
    if menu_frame.winfo_viewable():
        menu_frame.pack_forget()
    else:
        menu_frame.pack(fill="x")

hamb_btn = tk.Button(
    navbar, text="☰", command=toggle_menu,
    bg=current_palette["surface"], fg=current_palette["text"]
)
hamb_btn.pack(side="right", padx=8)


# MENU PANEL ==================================================
menu_frame = tk.Frame(root, bg=current_palette["surface"])
menu_frame.pack(fill="x")

tk.Button(menu_frame, text="Dark Mode", command=lambda: apply_palette(root, palette_dark)).pack(side="left", padx=6, pady=6)
tk.Button(menu_frame, text="Light Mode", command=lambda: apply_palette(root, palette_light)).pack(side="left", padx=6, pady=6)
tk.Button(menu_frame, text="Custom Mode", command=lambda: apply_palette(root, palette_custom)).pack(side="left", padx=6, pady=6)


# CONTENT AREA ===============================================
content = tk.Frame(root, bg=current_palette["bg"])
content.pack(fill="both", expand=True, padx=12, pady=12)

cols = ("Port", "PID", "Process")
tree = ttk.Treeview(content, columns=cols, show="headings")
for c in cols:
    tree.heading(c, text=c)
tree.pack(fill="both", expand=True)

btn_frame = tk.Frame(root, bg=current_palette["bg"])
btn_frame.pack(fill="x", pady=10)

tk.Button(btn_frame, text="Refresh", command=refresh).pack(side="left", padx=6)
tk.Button(btn_frame, text="Kill Selected", command=kill_selected).pack(side="left", padx=6)

refresh()
root.mainloop()
