import os
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import messagebox, ttk

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None


class MasterLevelPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Master Level Pro v2.0")
        self.root.geometry("520x760")
        self.root.minsize(500, 700)
        self.last_saved_pdf = None

        self.languages = {
            "English": {
                "app_title": "Master Level Pro",
                "subtitle": "Precision Shim Calculator",
                "select_lang": "Language",
                "m_no": "Machine/Job No",
                "op": "Operator Name",
                "err": "Error Reading (mm)",
                "len": "Level Length (mm)",
                "dist": "Shim Distance (mm)",
                "calc": "Calculate",
                "reset": "Reset",
                "save": "Save PDF",
                "show": "Open PDF",
                "res": "Shim Thickness",
                "status_ready": "Ready",
                "status_calculated": "Calculation completed",
                "status_reset": "Form reset",
                "err_invalid": "Please enter valid numeric values.",
                "err_zero": "Level Length cannot be zero.",
                "err_pdf_missing": "fpdf2 is not installed. Run: pip install fpdf2",
                "saved": "PDF saved successfully",
                "file_missing": "No saved PDF found.",
                "report_title": "LEVELING INSPECTION REPORT",
                "date": "Date",
                "machine": "Machine/Job No",
                "operator": "Operator",
                "level_length": "Level Length",
                "error_reading": "Error Reading",
                "total_distance": "Total Distance",
                "result": "RESULT SHIM THICKNESS",
            },
            "Hindi": {
                "app_title": "मास्टर लेवल प्रो",
                "subtitle": "प्रिसिजन शिम कैलकुलेटर",
                "select_lang": "भाषा",
                "m_no": "मशीन/जॉब नंबर",
                "op": "ऑपरेटर नाम",
                "err": "रीडिंग त्रुटि (mm)",
                "len": "लेवल लंबाई (mm)",
                "dist": "शिम दूरी (mm)",
                "calc": "गणना करें",
                "reset": "रीसेट",
                "save": "PDF सेव करें",
                "show": "PDF खोलें",
                "res": "शिम मोटाई",
                "status_ready": "तैयार",
                "status_calculated": "गणना पूरी हुई",
                "status_reset": "फ़ॉर्म रीसेट हुआ",
                "err_invalid": "कृपया सही संख्यात्मक मान भरें।",
                "err_zero": "लेवल लंबाई शून्य नहीं हो सकती।",
                "err_pdf_missing": "fpdf2 इंस्टॉल नहीं है। कमांड चलाएँ: pip install fpdf2",
                "saved": "PDF सफलतापूर्वक सेव हुआ",
                "file_missing": "कोई सेव किया हुआ PDF नहीं मिला।",
                "report_title": "लेवलिंग निरीक्षण रिपोर्ट",
                "date": "तारीख",
                "machine": "मशीन/जॉब नंबर",
                "operator": "ऑपरेटर",
                "level_length": "लेवल लंबाई",
                "error_reading": "रीडिंग त्रुटि",
                "total_distance": "कुल दूरी",
                "result": "परिणाम शिम मोटाई",
            },
        }

        self._build_style()
        self._build_ui()
        self.update_labels()

    def _build_style(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

        self.style.configure("Page.TFrame", background="#f4f6f9")
        self.style.configure("Card.TFrame", background="white")
        self.style.configure("Title.TLabel", background="#f4f6f9", foreground="#1f2937", font=("Segoe UI", 20, "bold"))
        self.style.configure("SubTitle.TLabel", background="#f4f6f9", foreground="#4b5563", font=("Segoe UI", 10))
        self.style.configure("FieldLabel.TLabel", background="white", foreground="#111827", font=("Segoe UI", 10, "bold"))
        self.style.configure("Status.TLabel", background="#f4f6f9", foreground="#334155", font=("Segoe UI", 10))
        self.style.configure("ResultLabel.TLabel", background="white", foreground="#0f172a", font=("Segoe UI", 12, "bold"))
        self.style.configure("ResultValue.TLabel", background="#eef2ff", foreground="#4338ca", font=("Segoe UI", 30, "bold"), anchor="center")
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

    def _build_ui(self):
        self.main = ttk.Frame(self.root, style="Page.TFrame", padding=16)
        self.main.pack(fill="both", expand=True)

        ttk.Label(self.main, text="Master Level Pro", style="Title.TLabel").pack(anchor="w")
        self.lbl_subtitle = ttk.Label(self.main, text="", style="SubTitle.TLabel")
        self.lbl_subtitle.pack(anchor="w", pady=(0, 12))

        topbar = ttk.Frame(self.main, style="Page.TFrame")
        topbar.pack(fill="x", pady=(0, 8))

        self.lbl_lang = ttk.Label(topbar, text="", style="Status.TLabel")
        self.lbl_lang.pack(side="left")

        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(topbar, textvariable=self.lang_var, values=list(self.languages.keys()), state="readonly", width=14)
        self.lang_combo.pack(side="left", padx=8)
        self.lang_combo.bind("<<ComboboxSelected>>", self.update_labels)

        form_card = ttk.Frame(self.main, style="Card.TFrame", padding=14)
        form_card.pack(fill="x", pady=(0, 10))

        self.fields = {}
        for row, key in enumerate(["m_no", "op", "err", "len", "dist"]):
            lbl = ttk.Label(form_card, text="", style="FieldLabel.TLabel")
            lbl.grid(row=row, column=0, sticky="w", pady=6)
            self.fields[f"{key}_lbl"] = lbl

            ent = ttk.Entry(form_card, font=("Segoe UI", 10))
            ent.grid(row=row, column=1, sticky="ew", pady=6, padx=(10, 0))
            self.fields[f"{key}_ent"] = ent

        form_card.columnconfigure(1, weight=1)

        action_row = ttk.Frame(self.main, style="Page.TFrame")
        action_row.pack(fill="x", pady=6)

        self.btn_calc = ttk.Button(action_row, text="", command=self.calculate, style="Accent.TButton")
        self.btn_calc.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_reset = ttk.Button(action_row, text="", command=self.reset)
        self.btn_reset.pack(side="left", fill="x", expand=True, padx=(6, 0))

        pdf_row = ttk.Frame(self.main, style="Page.TFrame")
        pdf_row.pack(fill="x", pady=6)

        self.btn_save = ttk.Button(pdf_row, text="", command=self.save_pdf)
        self.btn_save.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_show = ttk.Button(pdf_row, text="", command=self.show_pdf, state="disabled")
        self.btn_show.pack(side="left", fill="x", expand=True, padx=(6, 0))

        result_card = ttk.Frame(self.main, style="Card.TFrame", padding=14)
        result_card.pack(fill="both", expand=True, pady=(10, 6))

        self.lbl_res = ttk.Label(result_card, text="", style="ResultLabel.TLabel")
        self.lbl_res.pack(anchor="w")

        self.res_val = ttk.Label(result_card, text="0.000 mm", style="ResultValue.TLabel")
        self.res_val.pack(fill="x", pady=8, ipady=16)

        formula = ttk.Label(
            result_card,
            text="Formula: shim = (error × distance) / level length",
            style="SubTitle.TLabel",
            background="white",
        )
        formula.pack(anchor="w", pady=(8, 0))

        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.main, textvariable=self.status_var, style="Status.TLabel")
        self.status_bar.pack(anchor="w", pady=(8, 0))

    def t(self, key):
        return self.languages[self.lang_var.get()][key]

    def update_labels(self, event=None):
        self.root.title(f"{self.t('app_title')} v2.0")
        self.lbl_subtitle.config(text=self.t("subtitle"))
        self.lbl_lang.config(text=f"{self.t('select_lang')}: ")

        for key in ["m_no", "op", "err", "len", "dist"]:
            self.fields[f"{key}_lbl"].config(text=self.t(key))

        self.btn_calc.config(text=self.t("calc"))
        self.btn_reset.config(text=self.t("reset"))
        self.btn_save.config(text=self.t("save"))
        self.btn_show.config(text=self.t("show"))
        self.lbl_res.config(text=self.t("res"))
        self.status_var.set(self.t("status_ready"))

    def calculate(self):
        try:
            e = float(self.fields["err_ent"].get().strip())
            l = float(self.fields["len_ent"].get().strip())
            d = float(self.fields["dist_ent"].get().strip())

            if l == 0:
                messagebox.showerror("Error", self.t("err_zero"))
                return

            value = (e * d) / l
            self.res_val.config(text=f"{value:.3f} mm")
            self.status_var.set(self.t("status_calculated"))
        except ValueError:
            messagebox.showerror("Error", self.t("err_invalid"))

    def save_pdf(self):
        if FPDF is None:
            messagebox.showerror("Error", self.t("err_pdf_missing"))
            return

        res = self.res_val.cget("text")
        if res == "0.000 mm":
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt=self.t("report_title"), ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"{self.t('date')}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            pdf.cell(200, 10, txt=f"{self.t('machine')}: {self.fields['m_no_ent'].get().strip()}", ln=True)
            pdf.cell(200, 10, txt=f"{self.t('operator')}: {self.fields['op_ent'].get().strip()}", ln=True)
            pdf.ln(5)
            pdf.cell(200, 10, txt=f"{self.t('level_length')}: {self.fields['len_ent'].get().strip()} mm", ln=True)
            pdf.cell(200, 10, txt=f"{self.t('error_reading')}: {self.fields['err_ent'].get().strip()} mm", ln=True)
            pdf.cell(200, 10, txt=f"{self.t('total_distance')}: {self.fields['dist_ent'].get().strip()} mm", ln=True)
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 15, txt=f"{self.t('result')}: {res}", ln=True)

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.last_saved_pdf = os.path.abspath(f"Report_{ts}.pdf")
            pdf.output(self.last_saved_pdf)
            self.btn_show.config(state="normal")
            messagebox.showinfo("Success", f"{self.t('saved')}\n{self.last_saved_pdf}")
        except Exception as exc:
            messagebox.showerror("Error", f"PDF Error: {exc}")

    def show_pdf(self):
        if self.last_saved_pdf and os.path.exists(self.last_saved_pdf):
            try:
                webbrowser.open(f"file://{self.last_saved_pdf}")
            except Exception:
                messagebox.showinfo("Note", self.last_saved_pdf)
        else:
            messagebox.showwarning("Warning", self.t("file_missing"))

    def reset(self):
        for key in ["m_no", "op", "err", "len", "dist"]:
            self.fields[f"{key}_ent"].delete(0, tk.END)
        self.res_val.config(text="0.000 mm")
        self.btn_show.config(state="disabled")
        self.status_var.set(self.t("status_reset"))


if __name__ == "__main__":
    root = tk.Tk()
    app = MasterLevelPro(root)
    root.mainloop()
