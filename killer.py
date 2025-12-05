# kill_ports_with_filter.py
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import psutil
import winreg

# -------------------------
# System theme detect
# -------------------------
def get_system_theme():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        return "light" if value == 1 else "dark"
    except:
        return "dark"

# -------------------------
# Palettes
# -------------------------
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

# -------------------------
# UI
# -------------------------
root = tk.Tk()
root.title("ArduxLab Port Killer — Modern UI")
root.geometry("780x520")
root.minsize(620, 420)
style = ttk.Style(root)

# -------------------------
# Styling helpers
# -------------------------
def style_widgets(pal):
    style.theme_use("clam")
    style.configure(
        "Custom.Treeview",
        background=pal["surface"],
        foreground=pal["text"],
        fieldbackground=pal["surface"],
        bordercolor=pal["border"],
        borderwidth=0,
        rowheight=24
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=pal["surface"],
        foreground=pal["text"],
        relief="flat"
    )
    style.configure(
        "Custom.TButton",
        background=pal["primary"],
        foreground=pal["text"],
        relief="flat",
        padding=6
    )
    style.map("Custom.TButton",
              background=[('active', pal["primary_hover"])])
    style.configure("Custom.TCombobox",
                    fieldbackground=pal["surface"],
                    background=pal["surface"],
                    foreground=pal["text"])
    style.map("Custom.TCombobox",
              fieldbackground=[('readonly', pal["surface"])])

def apply_to_widget_recursive(widget, pal):
    cls = widget.winfo_class()
    if cls in ("Frame", "Labelframe"):
        widget.configure(bg=pal["bg"])
    elif cls == "Label":
        widget.configure(bg=pal["bg"], fg=pal["text"])
    elif cls == "Button":
        widget.configure(bg=pal["primary"], fg=pal["text"],
                         activebackground=pal["primary_hover"],
                         activeforeground=pal["text"],
                         bd=0, relief="flat")
    elif cls == "Entry":
        widget.configure(bg=pal["surface"], fg=pal["text"], insertbackground=pal["text"])
    for child in widget.winfo_children():
        apply_to_widget_recursive(child, pal)

def apply_palette(root, pal):
    global current_palette
    current_palette = pal
    root.configure(bg=pal["bg"])
    style_widgets(pal)
    for w in root.winfo_children():
        apply_to_widget_recursive(w, pal)

# -------------------------
# Port logic + filter
# -------------------------
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
    return sorted(list(set(result)), key=lambda x: (x[0], x[1]))

def apply_filter(text, rows, filter_type="All"):
    t = (text or "").strip().lower()
    if not t:
        return rows
    out = []
    for port, pid, name in rows:
        if filter_type == "Port" and t in str(port).lower():
            out.append((port, pid, name))
        elif filter_type == "PID" and t in str(pid).lower():
            out.append((port, pid, name))
        elif filter_type == "Process" and t in name.lower():
            out.append((port, pid, name))
        elif filter_type == "All":
            if t in str(port).lower() or t in str(pid).lower() or t in name.lower():
                out.append((port, pid, name))
    return out

def refresh():
    rows = find_listening_ports()
    rows = apply_filter(search_var.get(), rows, filter_var.get())
    tree_delete_all()
    for port, pid, name in rows:
        tree.insert("", "end", values=(port, pid, name))
    adjust_columns()

def tree_delete_all():
    for i in tree.get_children():
        tree.delete(i)

def kill_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info", "Pilih proses dulu")
        return
    for s in sel:
        port, pid, name = tree.item(s, "values")
        try:
            psutil.Process(int(pid)).kill()
        except psutil.NoSuchProcess:
            messagebox.showwarning("Warning", f"PID {pid} tidak ditemukan")
        except psutil.AccessDenied:
            messagebox.showerror("Error", f"Permission denied untuk PID {pid}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal kill PID {pid}: {e}")
    refresh()

# -------------------------
# UI Layout
# -------------------------
navbar = tk.Frame(root, height=56)
navbar.pack(side="top", fill="x")
navbar.pack_propagate(False)

title_lbl = tk.Label(navbar, text="🔧 ArduxLab Port Killer", font=("Segoe UI", 13, "bold"))
title_lbl.pack(side="left", padx=12)

menu_frame = tk.Frame(navbar)
def toggle_menu():
    if menu_frame.winfo_ismapped():
        menu_frame.pack_forget()
    else:
        menu_frame.pack(side="bottom", fill="x", padx=6, pady=(6,6))

hamb_btn = tk.Button(navbar, text="☰", command=toggle_menu, relief="flat")
hamb_btn.pack(side="right", padx=8, pady=6)

search_var = tk.StringVar()
search_entry = ttk.Entry(navbar, textvariable=search_var, width=20)
search_entry.pack(side="right", padx=8, pady=10)

filter_var = tk.StringVar(value="All")
filter_combo = ttk.Combobox(navbar, textvariable=filter_var, values=["All","Port","PID","Process"], width=10, state="readonly")
filter_combo.pack(side="right", padx=6, pady=10)

search_lbl = tk.Label(navbar, text="Search:", font=("Segoe UI", 10))
search_lbl.pack(side="right", pady=10)

search_entry.bind("<KeyRelease>", lambda e: refresh())
filter_combo.bind("<<ComboboxSelected>>", lambda e: refresh())

def create_menu_buttons(frame):
    for i in range(3):
        frame.grid_columnconfigure(i, weight=1)
    dark_btn = tk.Button(frame, text="Dark Mode", command=lambda: apply_palette(root, palette_dark))
    light_btn = tk.Button(frame, text="Light Mode", command=lambda: apply_palette(root, palette_light))
    custom_btn = tk.Button(frame, text="Custom Mode", command=pick_custom_color)
    dark_btn.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
    light_btn.grid(row=0, column=1, sticky="ew", padx=4, pady=4)
    custom_btn.grid(row=0, column=2, sticky="ew", padx=4, pady=4)

def pick_custom_color():
    color_code = colorchooser.askcolor(title="Pick Custom Color")[1]
    if color_code:
        pal = palette_custom.copy()
        pal["bg"] = color_code
        pal["surface"] = color_code
        pal["text"] = "#000000" if sum(int(color_code[i:i+2],16) for i in (1,3,5)) > 382 else "#e3e3e8"
        apply_palette(root, pal)

create_menu_buttons(menu_frame)

content = tk.Frame(root)
content.pack(fill="both", expand=True, padx=12, pady=(8,12))

tv_frame = tk.Frame(content)
tv_frame.pack(fill="both", expand=True)

cols = ("Port", "PID", "Process")
tree = ttk.Treeview(tv_frame, columns=cols, show="headings", style="Custom.Treeview")
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor="w")
vsb = ttk.Scrollbar(tv_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)

ctrl_frame = tk.Frame(root, height=48)
ctrl_frame.pack(side="bottom", fill="x")
ctrl_frame.pack_propagate(False)

refresh_btn = ttk.Button(ctrl_frame, text="Refresh", style="Custom.TButton", command=refresh)
refresh_btn.pack(side="left", padx=10, pady=8, expand=True, fill="x")
kill_btn = ttk.Button(ctrl_frame, text="Kill Selected", style="Custom.TButton", command=kill_selected)
kill_btn.pack(side="left", padx=6, pady=8, expand=True, fill="x")

# -------------------------
# Responsive helpers
# -------------------------
def _adjust_columns():
    total = tree.winfo_width() or tv_frame.winfo_width() or 600
    tree.column("Port", width=int(total * 0.15))
    tree.column("PID", width=int(total * 0.15))
    tree.column("Process", width=int(total * 0.70))

def adjust_columns(event=None):
    root.after_idle(_adjust_columns)

tree.bind("<Configure>", adjust_columns)
root.bind("<Configure>", lambda e: adjust_columns())

# -------------------------
# Init theme & load
# -------------------------
sys_theme = get_system_theme()
apply_palette(root, palette_dark if sys_theme == "dark" else palette_light)
refresh()

# Keyboard shortcuts
root.bind("<F5>", lambda e: refresh())
root.bind("<Delete>", lambda e: kill_selected())

root.mainloop()
