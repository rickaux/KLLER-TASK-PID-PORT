# kill_ports.py
import psutil
import socket
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

def find_listening_ports():
    conns = psutil.net_connections(kind='inet')
    port_map = {}
    for c in conns:
        if c.laddr and c.status in ('LISTEN','ESTABLISHED'):
            pid = c.pid
            port = c.laddr.port
            if pid:
                try:
                    p = psutil.Process(pid)
                    name = p.name()
                except Exception:
                    name = '?'
                port_map.setdefault((port,pid,name), []).append((c.raddr, c.status))
    return port_map

def refresh():
    tree.delete(*tree.get_children())
    for (port,pid,name),addrs in sorted(find_listening_ports().items()):
        tree.insert('', 'end', values=(port, pid, name, len(addrs)))

def kill_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Info","Pilih proses dulu")
        return
    for s in sel:
        port, pid, name, _ = tree.item(s, 'values')
        try:
            psutil.Process(int(pid)).kill()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal kill PID {pid}: {e}")
    refresh()

root = tk.Tk()
root.title("Port Killer — ArduxLab Tool")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(fill='both', expand=True, padx=8, pady=8)

cols = ('Port','PID','Process','Conns')
tree = ttk.Treeview(frame, columns=cols, show='headings', selectmode='extended')
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, anchor='w')
tree.pack(fill='both', expand=True)

btn_frame = tk.Frame(root)
btn_frame.pack(fill='x', padx=8, pady=6)
tk.Button(btn_frame, text="Refresh", command=refresh).pack(side='left')
tk.Button(btn_frame, text="Kill Selected", command=kill_selected).pack(side='left')

refresh()
root.mainloop()
