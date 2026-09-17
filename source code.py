import io
import os
import ssl
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import urllib.request
import zipfile

# --- CORE URLS (Siema chopaki) ---
CUSTOM_DATA_URL = "https://github.com/gorniczblazej9-lab/AIRAC/releases/download/xplane12/xplane_customdata_native_2609.zip"
XP11_URL = "https://github.com/gorniczblazej9-lab/AIRAC/releases/download/xplane12/xplane11_native_2609.zip"
XP12_URL = "https://github.com/gorniczblazej9-lab/AIRAC/releases/download/xplane12/xplane12_native_2609.zip"


class AiracInstallerApp(tk.Tk):

  def __init__(self):
    super().__init__()
    self.title("Navigraph AIRAC Setup Assistant")
    self.geometry("740x500")
    self.resizable(False, False)
    self.configure(bg="#090d16")

    self.selected_sim = None
    self.sim_path = tk.StringVar()

    self.setup_styles()
    self.create_main_menu()

  def setup_styles(self):
    self.style = ttk.Style(self)
    try:
      self.style.theme_use("clam")
    except Exception:
      pass

    # Premium Dark Theme Palette
    self.bg_color = "#090d16"
    self.card_bg = "#111827"
    self.card_hover = "#192338"
    self.accent_blue = "#0ea5e9"
    self.accent_hover = "#38bdf8"
    self.text_main = "#f8fafc"
    self.text_muted = "#64748b"
    self.success_green = "#10b981"

    self.style.configure("Main.TFrame", background=self.bg_color)
    self.style.configure("Card.TFrame", background=self.card_bg)

    self.style.configure(
        "Header.TLabel",
        background=self.bg_color,
        foreground=self.text_main,
        font=("Segoe UI", 20, "bold"),
    )
    self.style.configure(
        "SubHeader.TLabel",
        background=self.bg_color,
        foreground=self.text_muted,
        font=("Segoe UI", 9, "bold"),
    )
    self.style.configure(
        "Status.TLabel",
        background=self.bg_color,
        foreground=self.accent_blue,
        font=("Segoe UI", 10, "italic", "bold"),
    )

    self.style.configure(
        "Dark.TEntry",
        fieldbackground="#0b101d",
        foreground="#38bdf8",
        insertcolor="#ffffff",
        borderwidth=0,
    )

  def clear_window(self):
    for widget in self.winfo_children():
      widget.destroy()

  def create_main_menu(self):
    self.clear_window()

    main_frame = ttk.Frame(self, style="Main.TFrame", padding=45)
    main_frame.pack(fill="both", expand=True)

    # Status Banner Capsule
    banner = tk.Frame(
        main_frame,
        bg="#111827",
        highlightbackground="#1f293d",
        highlightthickness=1,
    )
    banner.pack(anchor="w", fill="x", pady=(0, 25), ipady=4)

    banner_inner = tk.Frame(banner, bg="#111827", padx=16, pady=10)
    banner_inner.pack(fill="both", expand=True)

    lbl_dot = tk.Label(
        banner_inner, text="●", bg="#111827", fg="#10b981", font=("Segoe UI", 10)
    )
    lbl_dot.pack(side="left", padx=(0, 8))

    lbl_status_text = tk.Label(
        banner_inner,
        text="SYSTEM READY   |   AIRAC CYCLE 2609 AVAILABLE",
        bg="#111827",
        fg="#f1f5f9",
        font=("Segoe UI", 9, "bold"),
    )
    lbl_status_text.pack(side="left")

    lbl_badge_right = tk.Label(
        banner_inner,
        text="SECURE INSTALLER",
        bg="#111827",
        fg="#0ea5e9",
        font=("Segoe UI", 8, "bold"),
    )
    lbl_badge_right.pack(side="right")

    # Titles
    lbl_title = ttk.Label(
        main_frame, text="Select Flight Simulator", style="Header.TLabel"
    )
    lbl_title.pack(anchor="w", pady=(0, 5))

    lbl_subtitle = ttk.Label(
        main_frame,
        text="CHOOSE YOUR TARGET PLATFORM TO START INSTALLATION",
        style="SubHeader.TLabel",
    )
    lbl_subtitle.pack(anchor="w", pady=(0, 30))

    # Cards Container
    cards_frame = ttk.Frame(main_frame, style="Main.TFrame")
    cards_frame.pack(fill="x", pady=10)

    self.create_sim_card(
        cards_frame,
        "X-Plane 11",
        "Legacy Native Database",
        lambda: self.setup_path_menu("X-Plane 11"),
    )
    self.create_sim_card(
        cards_frame,
        "X-Plane 12",
        "Next-Gen Avionics Pipeline",
        lambda: self.setup_path_menu("X-Plane 12"),
    )

    # Footer
    lbl_footer = tk.Label(
        main_frame,
        text="NAVIGRAPH NATIVE AIRAC DATASET • AUTOMATED WIZARD V2.6",
        bg="#090d16",
        fg="#1e293b",
        font=("Segoe UI", 8, "bold"),
    )
    lbl_footer.pack(side="bottom", anchor="w", pady=(15, 0))

  def create_sim_card(self, parent, title, subtitle, command):
    card = tk.Frame(
        parent, bg="#111827", highlightbackground="#1f293d", highlightthickness=1
    )
    card.pack(side="left", expand=True, fill="both", padx=10, ipady=10)

    inner = tk.Frame(card, bg="#111827", padx=20, pady=20)
    inner.pack(fill="both", expand=True)

    lbl_name = tk.Label(
        inner,
        text=title,
        bg="#111827",
        fg="#f8fafc",
        font=("Segoe UI", 16, "bold"),
    )
    lbl_name.pack(anchor="w", pady=(0, 4))

    lbl_sub = tk.Label(
        inner, text=subtitle, bg="#111827", fg="#64748b", font=("Segoe UI", 9)
    )
    lbl_sub.pack(anchor="w", pady=(0, 20))

    btn = tk.Button(
        inner,
        text="Select Platform →",
        bg="#0ea5e9",
        fg="#090d16",
        activebackground="#38bdf8",
        activeforeground="#090d16",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=command,
        padx=15,
        pady=8,
    )
    btn.pack(anchor="w")

    # Hover animations / color swaps
    def on_enter(e):
      card.config(highlightbackground="#0ea5e9")
      inner.config(bg="#162035")
      lbl_name.config(bg="#162035")
      lbl_sub.config(bg="#162035")

    def on_leave(e):
      card.config(highlightbackground="#1f293d")
      inner.config(bg="#111827")
      lbl_name.config(bg="#111827")
      lbl_sub.config(bg="#111827")

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    inner.bind("<Enter>", on_enter)
    inner.bind("<Leave>", on_leave)
    lbl_name.bind("<Enter>", on_enter)
    lbl_sub.bind("<Enter>", on_enter)

  def setup_path_menu(self, sim_name):
    self.selected_sim = sim_name
    self.clear_window()

    main_frame = ttk.Frame(self, style="Main.TFrame", padding=45)
    main_frame.pack(fill="both", expand=True)

    lbl_sim = ttk.Label(
        main_frame,
        text=f"Installation Path: {sim_name}",
        style="Header.TLabel",
    )
    lbl_sim.pack(anchor="w", pady=(0, 5))

    lbl_desc = ttk.Label(
        main_frame,
        text=(
            "SELECT THE ROOT FOLDER OF YOUR SIMULATOR (WHERE X-PLANE.EXE IS"
            " LOCATED):"
        ),
        style="SubHeader.TLabel",
    )
    lbl_desc.pack(anchor="w", pady=(0, 25))

    # Path Input Card
    card = tk.Frame(
        main_frame, bg="#111827", highlightbackground="#1f293d", highlightthickness=1
    )
    card.pack(fill="x", pady=10, ipady=5, ipadx=5)

    path_inner = tk.Frame(card, bg="#111827", padx=15, pady=15)
    path_inner.pack(fill="x")

    self.entry_path = ttk.Entry(
        path_inner,
        textvariable=self.sim_path,
        state="readonly",
        style="Dark.TEntry",
        font=("Segoe UI", 10, "bold"),
    )
    self.entry_path.pack(
        side="left", fill="x", expand=True, padx=(0, 15), ipady=8
    )

    btn_browse = tk.Button(
        path_inner,
        text="Browse...",
        bg="#1f293d",
        fg="#38bdf8",
        activebackground="#334155",
        activeforeground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.browse_directory,
        padx=15,
        pady=8,
    )
    btn_browse.pack(side="right")

    self.lbl_status = ttk.Label(
        main_frame,
        text="Status: Waiting for simulator directory selection...",
        style="Status.TLabel",
    )
    self.lbl_status.pack(anchor="w", pady=(25, 10))

    self.progress_bar = ttk.Progressbar(main_frame, mode="indeterminate")

    # Bottom Actions
    btn_frame = ttk.Frame(main_frame, style="Main.TFrame")
    btn_frame.pack(fill="x", side="bottom", pady=(25, 0))

    btn_back = tk.Button(
        btn_frame,
        text="← Back",
        bg="#111827",
        fg="#94a3b8",
        activebackground="#1f293d",
        activeforeground="#ffffff",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.create_main_menu,
        padx=20,
        pady=10,
    )
    btn_back.pack(side="left")

    self.btn_install = tk.Button(
        btn_frame,
        text="Install AIRAC",
        bg="#0ea5e9",
        fg="#090d16",
        activebackground="#38bdf8",
        activeforeground="#090d16",
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.start_installation,
        state=tk.DISABLED,
        padx=25,
        pady=10,
    )
    self.btn_install.pack(side="right")

  def browse_directory(self):
    directory = filedialog.askdirectory(
        title=f"Select Root Folder for {self.selected_sim}"
    )
    if directory:
      self.sim_path.set(directory)
      self.btn_install.config(state=tk.NORMAL, bg="#0ea5e9", cursor="hand2")
      self.lbl_status.config(
          text="Status: Directory verified. Ready to install.",
          foreground=self.success_green,
      )

  def start_installation(self):
    self.btn_install.config(state=tk.DISABLED, bg="#1f293d", fg="#64748b")
    self.progress_bar.pack(fill="x", pady=(0, 10))
    self.progress_bar.start(12)

    thread = threading.Thread(target=self.install_process)
    thread.daemon = True
    thread.start()

  def install_process(self):
    try:
      base_path = self.sim_path.get()
      custom_data_path = os.path.join(base_path, "Custom Data")
      gns430_path = os.path.join(custom_data_path, "GNS430")

      os.makedirs(gns430_path, exist_ok=True)

      self.update_status("Downloading GNS430 base dataset...")
      self.download_and_extract(CUSTOM_DATA_URL, gns430_path)

      sim_url = XP12_URL if self.selected_sim == "X-Plane 12" else XP11_URL
      self.update_status(f"Downloading native dataset for {self.selected_sim}...")
      self.download_and_extract(sim_url, custom_data_path)

      self.show_success_screen()

    except Exception as e:
      self.show_error(f"Installation Error:\n{str(e)}")

  def download_and_extract(self, url, extract_to):
    context = ssl._create_unverified_context()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "*/*",
        },
    )

    try:
      with urllib.request.urlopen(req, context=context) as response:
        content = response.read()
        zip_file = zipfile.ZipFile(io.BytesIO(content))
        zip_file.extractall(extract_to)
    except urllib.error.HTTPError as e:
      raise Exception(f"HTTP Error {e.code}: {e.reason}\nURL: {url}")
    except Exception as e:
      raise Exception(f"{str(e)}\nURL: {url}")

  def update_status(self, text):
    self.after(
        0, lambda: self.lbl_status.config(text=text, foreground="#0ea5e9")
    )

  def show_error(self, error_message):

    def gui_action():
      self.progress_bar.stop()
      self.progress_bar.pack_forget()
      messagebox.showerror("Installation Failed", error_message)
      self.lbl_status.config(
          text="Status: Installation aborted due to an error.",
          foreground="#ef4444",
      )
      self.btn_install.config(state=tk.NORMAL, bg="#0ea5e9", fg="#090d16")

    self.after(0, gui_action)

  def show_success_screen(self):

    def gui_action():
      self.progress_bar.stop()
      self.clear_window()

      main_frame = ttk.Frame(self, style="Main.TFrame", padding=45)
      main_frame.pack(fill="both", expand=True)

      lbl_success = ttk.Label(
          main_frame,
          text="Installation Successful!",
          style="Header.TLabel",
          foreground=self.success_green,
      )
      lbl_success.pack(anchor="w", pady=(20, 10))

      lbl_info = ttk.Label(
          main_frame,
          text=(
              "The Navigraph AIRAC cycle has been successfully downloaded,"
              " extracted, and installed into your Custom Data directory. Your"
              " navigation databases are now fully up to date."
          ),
          style="SubHeader.TLabel",
          justify="left",
      )
      lbl_info.pack(anchor="w", pady=(0, 40))

      btn_exit = tk.Button(
          main_frame,
          text="Finish & Close",
          bg="#0ea5e9",
          fg="#090d16",
          activebackground="#38bdf8",
          activeforeground="#090d16",
          font=("Segoe UI", 11, "bold"),
          relief="flat",
          cursor="hand2",
          command=self.destroy,
          padx=30,
          pady=12,
      )
      btn_exit.pack(anchor="w")

    self.after(0, gui_action)


if __name__ == "__main__":
  app = AiracInstallerApp()
  app.mainloop()