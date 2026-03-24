#!/usr/bin/env python3
import time
import subprocess
import os
import argparse
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class OneDriveHandler(FileSystemEventHandler):
    def __init__(self, excel_path, autopush=False):
        self.excel_path = os.path.abspath(excel_path)
        self.autopush = autopush
        self.last_run = 0.0
        self.cooldown = 10  # Evita múltiples disparos por guardados rápidos de OneDrive

    def on_modified(self, event):
        if event.is_directory or os.path.abspath(event.src_path) != self.excel_path:
            return
        
        current_time = time.time()
        if current_time - self.last_run > self.cooldown:
            self.last_run = current_time
            print(f"\n[!] Cambio detectado en OneDrive: {os.path.basename(self.excel_path)}")
            # Pequeña espera para que OneDrive libere el archivo
            time.sleep(2)
            self.run_sync()

    def run_sync(self):
        try:
            print("[*] Regenerando dashboard...")
            subprocess.run(["python3", "scripts/generate.py"], check=True)
            
            if self.autopush:
                print("[*] Subiendo a GitHub...")
                subprocess.run(["git", "add", "index.html"], check=True)
                subprocess.run(["git", "commit", "-m", "chore: auto-update dashboard from OneDrive"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("[✓] Web actualizada correctamente.")
        except Exception as e:
            print(f"[!] Error en la sincronización: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GWS Sync Monitor")
    parser.add_argument("--push", action="store_true", help="Habilitar subida automática a GitHub")
    args = parser.parse_args()

    ONEDRIVE_FILE = "/Users/santiagopinzon/Library/CloudStorage/OneDrive-CorporacionHospitalariaJuanCiudad/Dashboard Vacantes/Informe vacantes Auto Dashboard.xlsx"
    
    if not os.path.exists(ONEDRIVE_FILE):
        print(f"[!] Error: No se encuentra el archivo en {ONEDRIVE_FILE}")
        exit(1)

    watch_dir = os.path.dirname(ONEDRIVE_FILE)
    handler = OneDriveHandler(ONEDRIVE_FILE, autopush=args.push)
    observer = Observer()
    observer.schedule(handler, watch_dir, recursive=False)

    print(f"=== GWS Monitor Pro v1.0 ===")
    print(f"[*] Vigilando: {os.path.basename(ONEDRIVE_FILE)}")
    print(f"[*] Modo: {'Sync + Push' if args.push else 'Solo Local'}")
    print("[*] Presiona Ctrl+C para detener.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
