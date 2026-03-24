#!/usr/bin/env python3
import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def process_recruitment_data(excel_path):
    """Procesa el Excel de vacantes y devuelve un diccionario con los datos limpios."""
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"No se encontró el archivo: {excel_path}")

    # Leer hojas principales con los nombres reales
    df_vacantes = pd.read_excel(excel_path, sheet_name='Cubrimiento de vacantes')
    df_licencias = pd.read_excel(excel_path, sheet_name='Proximas licencias de maternida')

    # Limpieza de Vacantes
    df_vacantes = df_vacantes.dropna(subset=['CARGO']).copy()
    
    # Mapeo de columnas (normalización)
    column_map = {
        'psicologa': 'PSICOLOGA',
        'Fecha probable de ingreso': 'FECHA PROBABLE DE INGRESO',
        'Proceso': 'CIUDAD' # Usamos Proceso como ubicación si no hay CIUDAD específica
    }
    df_vacantes = df_vacantes.rename(columns=column_map)
    
    # Manejo de fechas
    df_vacantes['FECHA PROBABLE DE INGRESO'] = pd.to_datetime(df_vacantes['FECHA PROBABLE DE INGRESO'], errors='coerce')
    
    # Dashboard v3 usa 'FECHA DE SOLICITUD' para calcular antiguedad, pero si no existe, usamos la fecha actual - 1 día como placeholder
    df_vacantes['dias_antiguedad'] = 0 
    
    # Formatear fechas para JSON
    df_vacantes['FECHA PROBABLE DE INGRESO'] = df_vacantes['FECHA PROBABLE DE INGRESO'].dt.strftime('%b %d, %Y').fillna('-')
    df_vacantes['FECHA DE SOLICITUD'] = '-'

    # Asegurar que PSICOLOGA y CIUDAD existan
    if 'PSICOLOGA' not in df_vacantes.columns: df_vacantes['PSICOLOGA'] = '-'
    if 'CIUDAD' not in df_vacantes.columns: df_vacantes['CIUDAD'] = '-'

    # KPIs
    kpis = {
        "total_vacantes": len(df_vacantes),
        "activas": len(df_vacantes[df_vacantes['ESTADO'] != 'Seleccionado']),
        "completadas": len(df_vacantes[df_vacantes['ESTADO'] == 'Seleccionado']),
        "licencias": len(df_licencias),
        "criticas": 0
    }

    return {
        "kpis": kpis,
        "vacantes": df_vacantes.astype(str).replace('nan', '-').replace('NaT', '-').to_dict(orient='records'),
        "licencias": df_licencias.astype(str).replace('nan', '-').replace('NaT', '-').to_dict(orient='records'),
        "updated_at": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }

def generate_html(data, template_path, output_path):
    """Inyecta los datos en la plantilla HTML."""
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()

    # Inyectar JSON de datos
    json_data = json.dumps(data, ensure_ascii=False)
    final_html = html_template.replace('{{DASHBOARD_DATA}}', json_data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    ONEDRIVE_PATH = "/Users/santiagopinzon/Library/CloudStorage/OneDrive-CorporacionHospitalariaJuanCiudad/Dashboard Vacantes/Informe vacantes Auto Dashboard.xlsx"
    TEMPLATE_PATH = BASE_DIR / 'templates' / 'main.html'
    OUTPUT_PATH = BASE_DIR / 'index.html'

    print(f"[*] Procesando Excel en: {ONEDRIVE_PATH}")
    try:
        data = process_recruitment_data(ONEDRIVE_PATH)
        print(f"[*] Generando dashboard en: {OUTPUT_PATH}")
        generate_html(data, TEMPLATE_PATH, OUTPUT_PATH)
        print(f"[✓] Dashboard actualizado con éxito ({data['kpis']['total_vacantes']} vacantes).")
    except Exception as e:
        print(f"[!] Error: {e}")
