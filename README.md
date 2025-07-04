# Proyecto Economía Salud

Este proyecto contiene scripts para procesar y unir archivos CSV de resultados de pacientes.

## Configuración del Ambiente

1. **Crear ambiente virtual** (ya creado):
   ```bash
   python3 -m venv venv
   ```

2. **Activar el ambiente virtual**:
   ```bash
   source venv/bin/activate

## Estructura del Proyecto

```
economia-salud/
├── data/
│   ├── raw/                    # Archivos CSV originales
│   │   ├── Resultados Pacientes Jan 2024 - Jul 2024.csv
│   │   ├── Resultados Pacientes Jan-Jun 2025.csv
│   │   └── Resultados Pacientes Jul 2024 - Ene 2025.csv
│   └── processed/              # Archivos procesados
│       ├── resultados_pacientes_combinados.csv
│       ├── resultados_pacientes_estandarizados.csv
│       ├── resumen_generado_2024_2025.csv
│       └── comparacion_resumenes.csv
├── resultados/                 # Resultados de análisis
│   ├── eda_resultados.txt      # Análisis exploratorio detallado
│   ├── resumen_ejecutivo.txt   # Resumen ejecutivo
│   ├── analisis_multiples_expedientes.txt  # Análisis de múltiples expedientes
│   ├── pacientes_multiples_expedientes.csv # CSV con pacientes múltiples expedientes
│   ├── estandarizacion_expedientes.txt     # Análisis de estandarización
│   ├── resumen_estandarizacion.txt         # Resumen de estandarización
│   ├── analisis_archivo_resumen.txt        # Análisis del archivo de resumen
│   └── resumen_ejecutivo_archivo_resumen.txt # Resumen ejecutivo del archivo de resumen
├── scripts/
│   ├── join.py                 # Script para unir archivos CSV
│   ├── summarize.py            # Script para generar resumen y comparar
│   ├── eda.py                  # Script de análisis exploratorio de datos
│   ├── analyze_multiple_expedients.py  # Script para analizar múltiples expedientes
│   ├── standardize_expedients.py       # Script para estandarizar expedientes
│   └── analyze_summary_file.py         # Script para analizar archivo de resumen
├── venv/                       # Ambiente virtual de Python
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Este archivo
```

## Configuración del Ambiente

1. **Crear ambiente virtual** (ya creado):
   ```bash
   python3 -m venv venv
   ```

2. **Activar el ambiente virtual**:
   ```bash
   source venv/bin/activate
   ```

3. **Instalar dependencias** (ya instaladas):
   ```bash
   pip install -r requirements.txt
   ```

## Uso del Script

### Unir archivos CSV

Para unir los archivos de resultados de pacientes:

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/join.py
```

El script:
- Lee los tres archivos CSV de la carpeta `data/raw/`
- Los combina en un solo archivo
- Agrega una columna `archivo_origen` para identificar de dónde viene cada registro
- Guarda el resultado en `data/processed/resultados_pacientes_combinados.csv`

### Generar resumen y comparar

Para generar un resumen del archivo combinado y compararlo con el resumen original:

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/summarize.py
```

El script:
- Lee el archivo combinado y el resumen original
- Genera un resumen por paciente/expediente con totales
- Compara las estadísticas entre ambos archivos
- Guarda el resumen generado en `data/processed/resumen_generado_2024_2025.csv`
- Guarda la comparación en `data/processed/comparacion_resumenes.csv`

### Análisis Exploratorio de Datos (EDA)

Para realizar un análisis exploratorio completo de todos los datasets:

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/eda.py
```

El script:
- Analiza cada archivo individual de `data/raw/`
- Analiza el archivo combinado
- Genera estadísticas descriptivas detalladas
- Analiza valores faltantes, distribuciones y tendencias
- Guarda resultados en `resultados/eda_resultados.txt`
- Crea un resumen ejecutivo en `resultados/resumen_ejecutivo.txt`

### Análisis de Múltiples Expedientes

Para identificar y analizar pacientes con múltiples expedientes o IAN:

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/analyze_multiple_expedients.py
```

El script:
- Identifica pacientes con múltiples expedientes o IAN
- Analiza las diferencias entre métodos de conteo
- Proporciona ejemplos específicos de pacientes
- Genera recomendaciones para el conteo correcto
- Guarda análisis en `resultados/analisis_multiples_expedientes.txt`
- Crea CSV con pacientes múltiples expedientes

### Estandarización de Expedientes

Para estandarizar los expedientes eliminando el prefijo "000":

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/standardize_expedients.py
```

El script:
- Identifica expedientes con prefijo "000" (19.89% del total)
- Elimina el prefijo para estandarizar el formato
- Reduce expedientes únicos de 6,156 a 5,782 (-374)
- Elimina completamente los pacientes con múltiples expedientes por formato inconsistente
- Guarda dataset estandarizado en `data/processed/resultados_pacientes_estandarizados.csv`
- Genera análisis detallado en `resultados/estandarizacion_expedientes.txt`

### Análisis del Archivo de Resumen

Para analizar el archivo de resumen original y compararlo con los datos procesados:

```bash
# Activar el ambiente virtual
source venv/bin/activate

# Ejecutar el script
python scripts/analyze_summary_file.py
```

El script:
- Analiza la estructura del archivo de resumen original (53 columnas)
- Compara métricas con los datos procesados
- Identifica diferencias en conteos y gastos
- Genera análisis detallado en `resultados/analisis_archivo_resumen.txt`
- Crea resumen ejecutivo en `resultados/resumen_ejecutivo_archivo_resumen.txt`

### Resultados

#### Archivo Combinado
- **2,399,200 registros** en total
- **17 columnas** incluyendo la nueva columna de origen
- Distribución por archivo:
  - Jan 2024 - Jul 2024: 868,182 registros
  - Jul 2024 - Ene 2025: 838,138 registros  
  - Jan-Jun 2025: 692,880 registros

#### Resumen Generado
- **6,156 pacientes únicos** identificados
- **Promedio de 389.73 registros por paciente**
- **Total de gastos calculados** por paciente/expediente

#### Comparación con Resumen Original
- **Resumen original**: 7,028 pacientes
- **Resumen generado**: 6,156 pacientes
- **Diferencia**: -872 pacientes (-12.41%)
- **Montos nivel 6**: Muy similares (diferencia < 0.01%)
- **Días de estancia**: Diferencia significativa (142% más en generado)

#### Hallazgos del EDA
- **Distribución por origen**: Hospitalización (56%), Laboratorios (26%), Urgencias (18%)
- **Áreas de servicio principales**: Medicamentos (22%), Material Quirúrgico (17%), Materiales e Insumos (13%)
- **Valores faltantes**: 75% en `id_registro_urg`, 25% en `id_registro_admision`
- **Rango de fechas**: Enero 2024 a Junio 2025
- **Promedio de registros por paciente**: 387-415 según el período

#### Análisis de Múltiples Expedientes
- **Pacientes con múltiples expedientes**: 374 (6.47% del total)
- **Diferencia en conteo**: +374 pacientes al considerar expediente + IAN
- **Patrón identificado**: Expedientes con y sin prefijo "000" (ej: "217382" vs "000217382")
- **Impacto en registros**: 12.7% de todos los registros corresponden a pacientes con múltiples expedientes
- **Recomendación**: Usar paciente + expediente + IAN para conteo preciso

#### Estandarización de Expedientes
- **Expedientes estandarizados**: 477,245 (19.89% del total)
- **Reducción de expedientes únicos**: 6,156 → 5,782 (-374)
- **Eliminación de duplicados**: 0 pacientes con múltiples expedientes después de estandarización
- **Formato final**: Todos los expedientes sin prefijo "000"
- **Dataset limpio**: `resultados_pacientes_estandarizados.csv` listo para análisis

#### Análisis del Archivo de Resumen Original
- **Registros en resumen**: 7,028 (vs 2,399,200 en datos procesados)
- **Pacientes únicos**: 5,782 (idéntico a datos procesados)
- **Columnas disponibles**: 53 (información detallada de urgencias y hospitalización)
- **Gastos nivel 6**: $1,178.7M (diferencia < 0.001% con datos procesados)
- **Pacientes con múltiples registros**: 882 pacientes (1,246 registros duplicados)
- **Naturaleza del archivo**: Resumen consolidado por episodio de atención

## Columnas del Dataset

- `paciente`: ID del paciente
- `id_registro_admision`: ID de registro de admisión
- `id_registro_urg`: ID de registro de urgencias
- `origen`: Origen del servicio
- `fecha`: Fecha del servicio
- `cantidad`: Cantidad del servicio
- `clave`: Clave del servicio
- `descripcion`: Descripción del servicio
- `area_servicio`: Área de servicio
- `nivel`: Nivel de atención
- `costo_nivel_6`: Costo nivel 6
- `monto_nivel_1`: Monto nivel 1
- `monto_nivel_6`: Monto nivel 6
- `n_expediente_hosp`: Número de expediente hospitalario
- `ian_expediente_hosp`: IAN del expediente hospitalario
- `fecha_egreso_general`: Fecha de egreso general
- `archivo_origen`: Archivo de origen (agregado por el script)

## Dependencias

- `pandas >= 2.3.0`: Para manipulación de datos
- `numpy >= 1.23.2`: Para operaciones numéricas 