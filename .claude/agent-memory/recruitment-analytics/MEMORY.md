# Memoria del Agente - Analisis de Vacantes GWS

## Estructura del Archivo de Vacantes
Archivo principal: `Informe vacantes Auto.xlsx`

### Hojas del archivo:
1. **Cubrimiento de vacantes** - Hoja principal con vacantes activas
2. **Proximas licencias de maternida** - Registro de licencias maternidad proximas
3. **Hoja2** - Hoja vacia/secundaria

### Columnas principales (Cubrimiento de vacantes):
- `Proceso` - Area/Departamento (ej: ENFERMERIA, CLINICAS QUIRURGICAS, etc.)
- `CARGO` - Nombre del cargo
- `Planta Autorizada` - Total posiciones autorizadas
- `VACANTES / TIEMPOS` - Numero de vacantes activas
- `CONGELADAS/ TIEMPOS` - Vacantes pausadas
- `TIPO DE VINCULACION` - FIJO, OBRA O LABOR
- `ESTADO` - Estado del proceso: Reclutamiento, Entrevista, En proceso, Seleccionado, Congelado, En revision, Convocatoria Interna
- `EN PROCESO` - Cantidad de candidatos en proceso
- `Fecha probable de ingreso` - Fecha estimada de ingreso
- `OBSERVACIONES` - Notas adicionales
- `SALARIO` - Salario del cargo
- `psicologa` - Nombre de la psicologa asignada (natalia, lady, susana, carolina, yulieth)

### Metricas clave (datos de referencia):
- Total Planta Autorizada: ~4,870 posiciones
- Total Vacantes Activas: ~227 posiciones
- Cobertura: ~95.3%
- Procesos con mas vacantes: ENFERMERIA, SERVICIO FARMACEUTICO, MANTENIMIENTO
- Psicologas principales: Carolina, Susana, Natalia, Lady, Yulieth

### Preferencias de visualizacion:
- Dashboard HTML con Chart.js
- Colores por estado: Reclutamiento (amarillo), Entrevista (azul), En proceso (morado), Seleccionado (verde), Congelado (rojo)
- Graficos: Dona para estados, barras horizontales por psicologa, barras apiladas por proceso

## Notas importantes:
- Archivo Excel tiene validacion de datos que genera warning en openpyxl (ignorar)
- Campo `psicologa` requiere limpieza (espacios, mayusculas)
- Algunos campos de fecha tienen valores invalidos (1900-01-01)