# ArduxLab-Port-Killer-Modern-UI
Tool Python berbasis **Tkinter + TTK** untuk menampilkan semua port yang sedang listening/established di Windows dan memudahkan untuk **kill process** yang terkait. Fokus pada **UI responsif** dengan fitur modern.

---

## Fitur

- Menampilkan semua port TCP/UDP yang aktif beserta PID dan nama proses.
- Filter/search **Port, PID, atau Process** secara real-time.
- Kill proses langsung dari UI dengan exception handling.
- Tema **Dark / Light / Custom**:
  - Custom theme pakai **color picker**.
  - Auto adjust text color agar kontras.
- **Responsive Treeview**: kolom menyesuaikan ukuran window.
- Shortcut keyboard:
  - `F5` → Refresh list
  - `Delete` → Kill selected process

---

## Struktur Project
```
KLLER TASK-PID-PORT/
├─ killer.py
├─ killer-v1.0.py
├─ killer-v2.0.py
├─ README.md
```

---

## Requirement

- Python 3.x  
- Modules: `psutil` (`pip install psutil`)  

**Install modules langsung via pip**:
```bash
pip install psutil
```

---

## Instalasi & Run

1. Clone atau download repo ini.
2. Pastikan Python environment aktif.
3. **Jika muncul error terkait Tcl/Tk**, set environment variable sesuai folder Python/Tk:

```bat
Contoh
set TCL_LIBRARY=C:\Users\LAPTOP-RYZE\AppData\Local\Programs\PhpWebStudy-Data\env\python\tcl\tcl8.6
set TK_LIBRARY=C:\Users\LAPTOP-RYZE\AppData\Local\Programs\PhpWebStudy-Data\env\python\tcl\tk8.6

harus disesuaikan folder dari tcl
set TCL_LIBRARY=C:\Users\LAPTOP-RYZE\AppData\Local\Programs\x\x
set TK_LIBRARY=C:\Users\LAPTOP-RYZE\AppData\Local\Programs\x\x
```

4. Jalankan script:
```bat
python kill.py
```

---

## Cara Penggunaan

1. Buka aplikasi, daftar port/pid/process akan muncul di tabel.
2. Gunakan tombol **Filter** untuk memilih Port, PID, atau Process.
3. Pilih item dari tabel untuk **kill** process/port.
4. Resize window, UI akan otomatis menyesuaikan.

---

## Known Issues / Catatan

- Filter/search port kadang tidak bekerja jika belum refresh → tekan `F5` atau klik tombol **Refresh**.
- Kill PID:
  - **NoSuchProcess** → PID sudah tidak ada.
  - **AccessDenied** → perlu jalankan Python sebagai Administrator untuk kill process tertentu.
- Custom theme:
  - Jika memilih warna terlalu terang/gelap, teks akan auto adjust.
- Tkinter/Ttk styling kadang berbeda di Windows → sudah diperbaiki dengan `ttk.Style(theme_use("clam"))`.
- Beberapa port system/protected mungkin tidak bisa di-kill walaupun PID muncul.
- Untuk **responsivitas maksimal**, jangan resize window terlalu ekstrem di resolusi sangat kecil.

---

## Lisensi

MIT License
