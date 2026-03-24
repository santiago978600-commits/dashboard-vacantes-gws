# Dashboard de Vacantes - GWS

Panel interactivo para visualización de vacantes y reclutamiento.

## Actualización Automática

El dashboard se actualiza automáticamente cuando se modifica el archivo Excel en la carpeta `data/`.

### Para actualizar el dashboard:

1. Edita el archivo `data/Informe vacantes Auto.xlsx`
2. Haz commit y push a GitHub:
   ```bash
   git add data/"Informe vacantes Auto.xlsx"
   git commit -m "Actualizar datos de vacantes"
   git push
   ```
3. El dashboard se actualizará automáticamente en 1-2 minutos.

### Monitoreo Automático desde OneDrive (Recomendado)

Si quieres que el dashboard se actualice **solo** cada vez que guardas el archivo Excel en tu **OneDrive/SharePoint**:

1. Asegúrate de tener el archivo sincronizado en tu Mac.
2. La ruta configurada actualmente es:
   `/Users/santiagopinzon/Library/CloudStorage/OneDrive-CorporacionHospitalariaJuanCiudad/Dashboard Vacantes/Informe vacantes Auto Dashboard.xlsx`
3. Ejecuta el script de monitoreo con auto-push habilitado:
   ```bash
   python3 scripts/watch_excel.py --push
   ```
4. ¡Listo! Cualquier cambio realizado en OneDrive (por ti o por tu equipo) disparará la actualización automática del dashboard público.

## URL del Dashboard

El dashboard está disponible en:
```
https://santiago978600-commits.github.io/dashboard-vacantes-gws/dashboard_vacantes.html
```

## Estructura del Proyecto

```
├── data/
│   └── Informe vacantes Auto.xlsx  # Archivo de datos
├── scripts/
│   └── generate_dashboard.py       # Script de generación
├── .github/
│   └── workflows/
│       └── update-dashboard.yml    # Flujo de automatización
├── dashboard_vacantes.html         # Dashboard generado
└── README.md
```

## Funcionalidades

- **KPIs**: Planta autorizada, vacantes activas, congeladas, cobertura, licencias de maternidad
- **Gráficos**: Estado de vacantes, carga por psicóloga, vacantes por proceso
- **Tabla interactiva**: Filtros por estado, proceso, psicóloga y búsqueda
- **Sección maternidad**: Fechas probables de parto y días restantes