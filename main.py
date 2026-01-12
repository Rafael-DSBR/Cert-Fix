"""
PROJECT: Auto-CertFix (PKI Orchestrator)
AUTHOR: Rafael Cavalheiro
DESCRIPTION: 
    Automates the repair of Broken Chain of Trust (ICP-Brasil) and 
    TLS/SSL Registry fixes for A3 Certificates communicating with SEFAZ.
    Built to offload Tier 3 tasks to Tier 1 support.
"""

import customtkinter as ctk
import subprocess
import ctypes
import sys
import os
import time
import threading

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run_command(cmd_list):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        process = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo,
            text=True,
            encoding='cp850'
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except Exception as e:
        return -1, "", str(e)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AutoCertFix(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Auto-CertFix | Enterprise Solutions")
        self.geometry("680x600")
        self.resizable(False, False)

        try:
            self.iconbitmap(resource_path("jacare.ico"))
        except: pass

        # === ESTILO VISUAL ===
        
        # Cabeçalho Compacto
        self.lbl_title = ctk.CTkLabel(self, text="Auto-CertFix Enterprise", font=("Roboto", 22, "bold"))
        self.lbl_title.pack(pady=(15, 0))
        
        self.lbl_desc = ctk.CTkLabel(self, text="Orquestrador de Segurança e PKI", font=("Roboto", 12), text_color="gray")
        self.lbl_desc.pack(pady=(0, 10))

        # Área de Log
        self.frame_log = ctk.CTkFrame(self, fg_color="#181818")
        self.frame_log.pack(pady=5, padx=15, fill="both", expand=True)

        self.textbox_log = ctk.CTkTextbox(
            self.frame_log, 
            font=("Roboto Medium", 13),
            fg_color="#181818",
            text_color="#E0E0E0",
            activate_scrollbars=True
        )
        self.textbox_log.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- CONFIGURAÇÃO DE CORES (TAGS) ---
        self.textbox_log.tag_config("GREEN", foreground="#00E676") # Verde Neon
        self.textbox_log.tag_config("RED", foreground="#FF1744")   # Vermelho Alerta
        self.textbox_log.tag_config("YELLOW", foreground="#FFEA00") # Amarelo Aviso
        self.textbox_log.tag_config("CYAN", foreground="#00B0FF")   # Azul Processo
        self.textbox_log.tag_config("HEADER", foreground="#FFFFFF") # Branco Puro

        self.textbox_log.insert("0.0", "Sistema pronto para operação.\n")

        # Barra de Progresso
        self.progress = ctk.CTkProgressBar(self, height=8, progress_color="#00E676")
        self.progress.pack(pady=(5, 10), padx=30, fill="x")
        self.progress.set(0)

        # Botão Ação
        self.btn_run = ctk.CTkButton(self, text="INICIAR REPARO", command=self.start_thread, height=45, font=("Roboto", 14, "bold"), fg_color="#2980b9", hover_color="#3498db")
        self.btn_run.pack(pady=15, padx=40, fill="x")

    def log(self, msg, type="INFO"):
        icon = ""
        tag = ""
        
        if type == "HEADER":
            self.textbox_log.insert("end", "\n" + msg + "\n", "HEADER")
            self.textbox_log.see("end")
            return

        if type == "SUCCESS":
            icon = "✔ "
            tag = "GREEN"
        elif type == "WARN":
            icon = "⚠ "
            tag = "YELLOW"
        elif type == "ERROR":
            icon = "✖ "
            tag = "RED"
        elif type == "PROCESS":
            icon = "➜ "
            tag = "CYAN"
        
        self.textbox_log.insert("end", icon, tag)
        self.textbox_log.insert("end", msg + "\n")
        self.textbox_log.see("end")

    def start_thread(self):
        self.textbox_log.delete("0.0", "end")
        self.btn_run.configure(state="disabled", text="PROCESSANDO...")
        threading.Thread(target=self.run_logic, daemon=True).start()

    def run_logic(self):
        files = {
            "exe_cadeias": resource_path("InstaladorCadeias_1.0.2.0.exe"),
            "reg_crypto": resource_path("3_CryptoFix.reg"),
            "cer_raiz": resource_path("Raiz-icp-brasil v10.cer"),
            "cer_soluti": resource_path("ac soluti ssl ev.cer")
        }

        self.log("DIAGNÓSTICO INICIAL", "HEADER")
        self.progress.set(0.1)
        time.sleep(0.5)

        # FASE 1
        self.log("Instalação de Cadeias Base", "HEADER")
        
        if os.path.exists(files["exe_cadeias"]):
            self.log("Executando pacote instalador", "PROCESS")
            time.sleep(0.5)
            try:
                subprocess.run([files["exe_cadeias"], "/S"], check=True) 
                self.log("Pacote base instalado", "SUCCESS")
            except Exception:
                self.log("Alerta na instalação base (Verificar manual)", "WARN")
        else:
            self.log("Pacote base não localizado", "WARN")

        self.progress.set(0.4)

        # FASE 2
        self.log("Segurança e Criptografia", "HEADER")
        
        if os.path.exists(files["reg_crypto"]):
            self.log("Ajustando protocolos TLS/SSL", "PROCESS")
            time.sleep(0.5)
            code, out, err = run_command(["regedit", "/s", files["reg_crypto"]])
            if code == 0:
                self.log("Registro otimizado", "SUCCESS")
            else:
                self.log(f"Falha no registro: {err}", "ERROR")
        
        self.progress.set(0.6)

        # FASE 3
        self.log("Injeção de Certificados", "HEADER")
        certs = [files["cer_raiz"], files["cer_soluti"]]
        for cert in certs:
            if os.path.exists(cert):
                nome = os.path.basename(cert)
                self.log(f"Instalando: {nome}", "PROCESS")
                time.sleep(0.3)
                
                code, out, err = run_command(["certutil", "-addstore", "-f", "Root", cert])
                
                if code == 0:
                    self.log(f"Certificado validado: {nome}", "SUCCESS")
                else:
                    self.log(f"Erro ao instalar {nome}", "ERROR")
            else:
                self.log(f"Arquivo ausente: {os.path.basename(cert)}", "WARN")

        self.progress.set(1.0)
        
        self.log("CONCLUSÃO", "HEADER")
        self.log("Otimização finalizada com sucesso", "SUCCESS")
        self.log("Reinicie o computador para aplicar", "WARN")
        
        self.btn_run.configure(state="normal", text="INICIAR REPARO")
        try: ctypes.windll.user32.MessageBeep(0x40) 
        except: pass

if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        app = AutoCertFix()
        app.mainloop()
