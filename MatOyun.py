import random
import sys
import time
import tkinter as tk
from tkinter import messagebox, ttk


class MatematikOyunu:

    def __init__(self, root):
        self.root = root
        self.root.title("Matematik Zeka & Hafıza Oyunu")
        self.root.geometry("900x750")

        self.puan = 0
        self.rekor_puan = 0

        self.is_dark_mode = False
        self.colors = {
            "light": {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "card_bg": "#ffffff",
                "btn_bg": "#e0e0e0",
            },
            "dark": {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "card_bg": "#2d2d2d",
                "btn_bg": "#3d3d3d",
            },
        }

        self.kalan_hak = 0
        self.kalan_sure = 0
        self.timer_job = None
        self.animasyon_jobs = []
        self.soru_parcalari = []
        self.dogru_cevap = 0
        self.animasyon_index = 0
        self.cevap_verilebilir = False

        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        self.btn_theme = tk.Button(
            self.top_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme,
            font=("Arial", 10, "bold"),
        )
        self.btn_theme.pack(side="left")

        self.lbl_rekor = tk.Label(
            self.top_frame,
            text=f"🏆 Rekor: {self.rekor_puan}",
            font=("Arial", 12, "bold"),
            fg="#d97706",
        )
        self.lbl_rekor.pack(side="right")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        self.tab_oyun = tk.Frame(self.notebook)
        self.tab_carpim = tk.Frame(self.notebook)

        self.notebook.add(self.tab_oyun, text="🎮 Oyuna Başla")
        self.notebook.add(self.tab_carpim, text="📊 100x100 Çarpım Tablosu")

        self.setup_tab_oyun()
        self.setup_tab_carpim()

    def setup_tab_oyun(self):
        self.frame_ayarlar = tk.LabelFrame(
            self.tab_oyun, text=" Ayarlar ", font=("Arial", 11, "bold")
        )
        self.frame_ayarlar.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.frame_ayarlar, text="Deneme Hakkı:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.spin_hak = tk.Spinbox(self.frame_ayarlar, from_=1, to=10, width=5)
        self.spin_hak.delete(0, "end")
        self.spin_hak.insert(0, "3")
        self.spin_hak.grid(row=0, column=1, sticky="e", pady=2)

        tk.Label(self.frame_ayarlar, text="Süre Sınırı (sn):").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.spin_sure = tk.Spinbox(self.frame_ayarlar, from_=5, to=120, width=5)
        self.spin_sure.delete(0, "end")
        self.spin_sure.insert(0, "30")
        self.spin_sure.grid(row=1, column=1, sticky="e", pady=2)

        tk.Label(self.frame_ayarlar, text="Öğe Görünme Süresi (ms):").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.spin_belirme = tk.Spinbox(
            self.frame_ayarlar, from_=200, to=3000, increment=100, width=5
        )
        self.spin_belirme.delete(0, "end")
        self.spin_belirme.insert(0, "600")
        self.spin_belirme.grid(row=2, column=1, sticky="e", pady=2)

        tk.Label(self.frame_ayarlar, text="Minimum Sayı:").grid(
            row=3, column=0, sticky="w", pady=2
        )
        self.spin_min = tk.Spinbox(
            self.frame_ayarlar, from_=-500, to=500, width=5
        )
        self.spin_min.delete(0, "end")
        self.spin_min.insert(0, "1")
        self.spin_min.grid(row=3, column=1, sticky="e", pady=2)

        tk.Label(self.frame_ayarlar, text="Maksimum Sayı:").grid(
            row=4, column=0, sticky="w", pady=2
        )
        self.spin_aralik = tk.Spinbox(
            self.frame_ayarlar, from_=-500, to=1000, increment=5, width=5
        )
        self.spin_aralik.delete(0, "end")
        self.spin_aralik.insert(0, "20")
        self.spin_aralik.grid(row=4, column=1, sticky="e", pady=2)

        tk.Label(self.frame_ayarlar, text="Operatörler:").grid(
            row=5, column=0, sticky="w", pady=2
        )
        self.var_topla = tk.BooleanVar(value=True)
        self.var_cikar = tk.BooleanVar(value=True)
        self.var_carp = tk.BooleanVar(value=False)
        self.var_bol = tk.BooleanVar(value=False)
        self.var_us = tk.BooleanVar(value=False)

        frame_ops = tk.Frame(self.frame_ayarlar)
        frame_ops.grid(row=5, column=1, sticky="e")
        tk.Checkbutton(frame_ops, text="+", variable=self.var_topla).pack(
            side="left"
        )
        tk.Checkbutton(frame_ops, text="-", variable=self.var_cikar).pack(
            side="left"
        )
        tk.Checkbutton(frame_ops, text="x", variable=self.var_carp).pack(side="left")
        tk.Checkbutton(frame_ops, text="/", variable=self.var_bol).pack(side="left")
        tk.Checkbutton(frame_ops, text="^", variable=self.var_us).pack(side="left")

        tk.Label(self.frame_ayarlar, text="İşlem Basamağı:").grid(
            row=6, column=0, sticky="w", pady=2
        )
        self.spin_basamak = tk.Spinbox(self.frame_ayarlar, from_=1, to=6, width=5)
        self.spin_basamak.delete(0, "end")
        self.spin_basamak.insert(0, "2")
        self.spin_basamak.grid(row=6, column=1, sticky="e", pady=2)

        self.btn_baslat = tk.Button(
            self.frame_ayarlar,
            text="🚀 Oyunu Başlat",
            command=self.oyun_baslat,
            font=("Arial", 11, "bold"),
            bg="#22c55e",
            fg="white",
        )
        self.btn_baslat.grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")

        self.lbl_bilgi = tk.Label(
            self.frame_ayarlar, text="Hazırsan Başlat'a bas!", font=("Arial", 9)
        )
        self.lbl_bilgi.grid(row=8, column=0, columnspan=2)

        self.frame_ekran = tk.Frame(self.tab_oyun, bd=2, relief="groove")
        self.frame_ekran.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_status = tk.Label(
            self.frame_ekran,
            text="Hak: - | Süre: - | Puan: 0",
            font=("Arial", 11, "bold"),
        )
        self.lbl_status.pack(pady=10)

        self.lbl_animasyon = tk.Label(
            self.frame_ekran, text="?", font=("Arial", 42, "bold")
        )
        self.lbl_animasyon.pack(expand=True)

        frame_cevap = tk.Frame(self.frame_ekran)
        frame_cevap.pack(pady=20)

        tk.Label(frame_cevap, text="Cevap: ", font=("Arial", 12)).pack(side="left")
        self.entry_cevap = tk.Entry(
            frame_cevap, font=("Arial", 14), width=12, state="disabled"
        )
        self.entry_cevap.pack(side="left", padx=5)
        self.entry_cevap.bind("<Return>", lambda e: self.cevap_kontrol())

        self.btn_gonder = tk.Button(
            frame_cevap,
            text="Gönder",
            command=self.cevap_kontrol,
            state="disabled",
            font=("Arial", 10, "bold"),
        )
        self.btn_gonder.pack(side="left")

    def setup_tab_carpim(self):
        lbl_baslik = tk.Label(
            self.tab_carpim,
            text="1'den 100'e Kadar Tüm Sayıların Çarpım Matrisi (100x100)",
            font=("Arial", 11, "bold"),
        )
        lbl_baslik.pack(pady=5)

        frame_text = tk.Frame(self.tab_carpim)
        frame_text.pack(fill="both", expand=True, padx=10, pady=5)

        self.txt_carpim = tk.Text(
            frame_text, font=("Consolas", 10), wrap="none"
        )
        scrollbar_y = ttk.Scrollbar(
            frame_text, orient="vertical", command=self.txt_carpim.yview
        )
        scrollbar_x = ttk.Scrollbar(
            frame_text, orient="horizontal", command=self.txt_carpim.xview
        )

        self.txt_carpim.configure(
            yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set
        )

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.txt_carpim.pack(side="left", fill="both", expand=True)

        self.tam_carpim_tablosu_olustur()

    def tam_carpim_tablosu_olustur(self):
        self.txt_carpim.delete("1.0", tk.END)

        baslik = "Çarpı |" + "".join([f"{i:6d}" for i in range(1, 101)]) + "\n"
        self.txt_carpim.insert(tk.END, baslik)
        self.txt_carpim.insert(
            tk.END, "-" * len(baslik) + "\n"
        )

        for i in range(1, 101):
            satir_metni = f"{i:5d} |"
            for j in range(1, 101):
                carpim = i * j
                satir_metni += f"{carpim:6d}"
            self.txt_carpim.insert(tk.END, satir_metni + "\n")

    def zorluk_puan_hesapla(self):
        puan = 10
        belirme_ms = int(self.spin_belirme.get())
        min_val = int(self.spin_min.get())
        max_val = int(self.spin_aralik.get())
        basamak = int(self.spin_basamak.get())

        puan += max(0, (1500 - belirme_ms) // 100) * 5
        puan += ((max_val - min_val) // 10) * 2
        puan += basamak * 15

        if min_val < 0:
            puan += 20

        if self.var_carp.get():
            puan += 10
        if self.var_bol.get():
            puan += 15
        if self.var_us.get():
            puan += 20

        return puan

    def animasyonlari_temizle(self):
        for jid in self.animasyon_jobs:
            self.root.after_cancel(jid)
        self.animasyon_jobs.clear()

    def oyun_baslat(self):
        ops = []
        if self.var_topla.get():
            ops.append("+")
        if self.var_cikar.get():
            ops.append("-")
        if self.var_carp.get():
            ops.append("x")
        if self.var_bol.get():
            ops.append("/")
        if self.var_us.get():
            ops.append("^")

        if not ops:
            messagebox.showwarning(
                "Uyarı", "Lütfen en az bir operatör seçiniz!"
            )
            return

        try:
            min_v = int(self.spin_min.get())
            max_v = int(self.spin_aralik.get())
            if min_v >= max_v:
                messagebox.showerror(
                    "Hata", "Minimum sayı maksimum sayıdan küçük olmalıdır!"
                )
                return
        except ValueError:
            return

        self.animasyonlari_temizle()
        self.kalan_hak = int(self.spin_hak.get())
        self.kalan_sure = int(self.spin_sure.get())
        self.puan = 0

        self.btn_baslat.config(state="disabled")
        self.lbl_bilgi.config(text="Oyun Başladı! Dikkatlice izle...")

        self.sureyi_baslat()
        self.yeni_soru_hazirla()

    def sureyi_baslat(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)

        def guncelle():
            if self.kalan_sure > 0:
                self.kalan_sure -= 1
                self.update_status()
                self.timer_job = self.root.after(1000, guncelle)
            else:
                self.oyun_bitti("Süre Doldu!")

        self.timer_job = self.root.after(1000, guncelle)

    def update_status(self):
        self.lbl_status.config(
            text=f"Hak: {self.kalan_hak} | Süre: {self.kalan_sure}s | Puan: {self.puan}"
        )

    def yeni_soru_hazirla(self):
        if self.kalan_hak <= 0:
            self.oyun_bitti("Hakkınız Bitti!")
            return

        self.animasyonlari_temizle()
        self.cevap_verilebilir = False

        ops = []
        if self.var_topla.get():
            ops.append("+")
        if self.var_cikar.get():
            ops.append("-")
        if self.var_carp.get():
            ops.append("x")
        if self.var_bol.get():
            ops.append("/")
        if self.var_us.get():
            ops.append("^")

        min_val = int(self.spin_min.get())
        max_val = int(self.spin_aralik.get())
        basamak_sayisi = int(self.spin_basamak.get())

        self.soru_parcalari = []
        ilk_sayi = random.randint(min_val, max_val)
        self.soru_parcalari.append(str(ilk_sayi))

        hesaplama_str = str(ilk_sayi)

        for _ in range(basamak_sayisi - 1):
            op = random.choice(ops)

            if op == "/":
                anlik_deger = int(eval(hesaplama_str))
                bolenler = [
                    i for i in range(1, max(2, abs(anlik_deger) + 1)) if anlik_deger % i == 0
                ]
                if not bolenler:
                    bolenler = [1]
                sayi = random.choice(bolenler)
                if random.choice([True, False]) and sayi != 0:
                    sayi = -sayi

                hesaplama_str += f" // {sayi}"
                gorsel_op = "/"

            elif op == "^":
                sayi = random.randint(1, 3)
                hesaplama_str += f" ** {sayi}"
                gorsel_op = "^"

            elif op == "x":
                sayi = random.randint(min(1, min_val), max(5, max_val // 2))
                if sayi == 0:
                    sayi = 1
                hesaplama_str += f" * {sayi}"
                gorsel_op = "x"

            elif op == "+":
                sayi = random.randint(min_val, max_val)
                hesaplama_str += f" + {sayi}"
                gorsel_op = "+"

            else:
                sayi = random.randint(min_val, max_val)
                hesaplama_str += f" - {sayi}"
                gorsel_op = "-"

            self.soru_parcalari.append(gorsel_op)
            self.soru_parcalari.append(str(sayi))

        try:
            self.dogru_cevap = int(eval(hesaplama_str))
        except Exception:
            self.dogru_cevap = ilk_sayi

        self.entry_cevap.config(state="disabled")
        self.btn_gonder.config(state="disabled")
        self.animasyon_index = 0
        self.animasyon_adim_calistir()

    def animasyon_adim_calistir(self):
        ms = int(self.spin_belirme.get())

        if self.animasyon_index < len(self.soru_parcalari):
            parca = self.soru_parcalari[self.animasyon_index]

            renk = (
                "#2563eb"
                if parca.isdigit() or (parca.startswith("-") and parca[1:].isdigit())
                else "#dc2626"
            )
            self.lbl_animasyon.config(text=parca, fg=renk)

            self.animasyon_index += 1

            def ara_bosluk():
                self.lbl_animasyon.config(text="")
                jid = self.root.after(200, self.animasyon_adim_calistir)
                self.animasyon_jobs.append(jid)

            jid2 = self.root.after(ms, ara_bosluk)
            self.animasyon_jobs.append(jid2)
        else:
            self.lbl_animasyon.config(text="?", fg="#888888")
            self.entry_cevap.config(state="normal")
            self.btn_gonder.config(state="normal")
            self.entry_cevap.delete(0, tk.END)
            self.entry_cevap.focus()
            self.cevap_verilebilir = True
            self.lbl_bilgi.config(text="Cevabını gir ve gönder!", fg="black")

    def cevap_kontrol(self):
        if not self.cevap_verilebilir:
            return

        try:
            tahmin = int(self.entry_cevap.get().strip())
        except ValueError:
            return

        self.cevap_verilebilir = False
        self.entry_cevap.config(state="disabled")
        self.btn_gonder.config(state="disabled")

        if tahmin == self.dogru_cevap:
            kazanilacak_puan = self.zorluk_puan_hesapla()
            self.puan += kazanilacak_puan
            self.lbl_bilgi.config(
                text=f"Doğru! (+{kazanilacak_puan} Puan)", fg="green"
            )
        else:
            self.kalan_hak -= 1
            self.lbl_bilgi.config(
                text=f"Yanlış! Doğru cevap: {self.dogru_cevap}", fg="red"
            )

        self.update_status()

        if self.kalan_hak > 0:
            jid = self.root.after(1200, self.yeni_soru_hazirla)
            self.animasyon_jobs.append(jid)
        else:
            self.oyun_bitti("Hakkınız Bitti!")

    def oyun_bitti(self, mesaj):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.animasyonlari_temizle()

        self.cevap_verilebilir = False
        self.entry_cevap.config(state="disabled")
        self.btn_gonder.config(state="disabled")
        self.btn_baslat.config(state="normal")

        if self.puan > self.rekor_puan:
            self.rekor_puan = self.puan
            self.lbl_rekor.config(text=f"🏆 Rekor: {self.rekor_puan}")
            rek_mesaj = "\n🎉 TEBRİKLER! YENİ REKOR!"
        else:
            rek_mesaj = ""

        messagebox.showinfo(
            "Oyun Bitti",
            f"{mesaj}\nToplam Puanınız: {self.puan}{rek_mesaj}",
        )
        self.lbl_animasyon.config(text="?", fg="#888888")
        self.lbl_bilgi.config(text="Oyun Bitti. Yeniden başlayabilirsiniz.")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        mode = "dark" if self.is_dark_mode else "light"
        theme = self.colors[mode]

        self.root.config(bg=theme["bg"])
        self.top_frame.config(bg=theme["bg"])
        self.tab_oyun.config(bg=theme["bg"])
        self.tab_carpim.config(bg=theme["bg"])
        self.frame_ekran.config(bg=theme["card_bg"])
        self.lbl_status.config(bg=theme["card_bg"], fg=theme["fg"])

        self.btn_theme.config(
            text="☀️ Light Mode" if self.is_dark_mode else "🌙 Dark Mode"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = MatematikOyunu(root)
    root.mainloop()
