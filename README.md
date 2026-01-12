# 🐊 Cert-Fix (PKI & Security Orchestrator)

> **"Democratizing Tier 3 solutions for Tier 1 Support."**

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-CertUtil-FFD43B?style=for-the-badge&logo=python&logoColor=blue" />
  <img src="https://img.shields.io/badge/Security-PKI_Repair-43B02A?style=for-the-badge&logo=security&logoColor=white" />
</div>

---

### 📋 The Problem (Diagnosis)
During a critical update cycle with **SEFAZ (Brazilian Tax Authority)**, hundreds of A3 Digital Certificates failed to communicate due to a "Broken Chain of Trust" and legacy TLS protocol mismatches.

* **Volume:** ~100 high-priority tickets per day escalation to Engineering.
* **Bottleneck:** The manual fix required advanced Registry manipulation (`regedit`) and Root CA injection via CLI (`certutil`), procedures that Tier 1 support agents were forbidden or afraid to execute due to risk.
* **Business Impact:** Clients unable to issue invoices (NF-e).

### 🛠️ The Solution (The Automation)
**Auto-CertFix** is a "One-Click Repair" GUI that orchestrates the entire remediation process. It safely executes elevated commands to repair the Windows CryptoAPI environment without requiring technical expertise from the agent.

**Capabilities:**
* ✅ **Chain Repair:** Automates `InstaladorCadeias.exe` (ACBR solution) installation.
* ✅ **Registry Hardening:** Applies `3_CryptoFix.reg` to fix TLS 1.2/SSL protocols.
* ✅ **Root CA Injection:** Uses `certutil` to forcibly inject missing ICP-Brasil Root Certificates into the Windows Trust Store.
* ✅ **Safety Wrapper:** Runs with elevated privileges via `ctypes` and provides real-time logging.

---

### 💻 Technical Implementation

The tool uses Python `subprocess` to bridge the gap between UI and System Shell.

**Workflow Logic:**
1.  **Check Environment:** Validates Admin privileges.
2.  **Phase 1 (Base):** Installs the base certificate chain executable.
3.  **Phase 2 (Crypto):** Edits Registry keys to force correct Protocol negotiation (SEFAZ requirement).
4.  **Phase 3 (Trust):** Loops through `.cer` assets and commits them to the `Root` store.

### How to Run

1.  **Dependencies:**
    ```bash
    pip install customtkinter
    ```
2.  **Assets Required:**
    * *Note: This repo contains the source code. To function, the following assets must be in the root folder:*
    * `InstaladorCadeias_1.0.2.0.exe`
    * `3_CryptoFix.reg`
    * `Raiz-icp-brasil v10.cer`
    * `ac soluti ssl ev.cer`

3.  **Execution:**
    ```bash
    python main.py
    ```

---

### ⚠️ Security Disclaimer
*This tool performs changes to the Windows Registry and System Root Store. It is intended for enterprise troubleshooting of specific ICP-Brasil scenarios. Use with caution.*

---

**Author:** Rafael Cavalheiro
*QA Automation Engineer & Tier 3 Support Lead*
