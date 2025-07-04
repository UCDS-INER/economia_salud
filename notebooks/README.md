# 📓 Notebooks de Análisis y Validación

Esta carpeta contiene Jupyter notebooks para análisis interactivo, validación de insights y pruebas antes de implementar funcionalidades en el dashboard.

## 🎯 Propósito

- **Análisis exploratorio interactivo** de los datos
- **Validación de insights** antes de implementación
- **Pruebas de visualizaciones** y gráficos
- **Experimentación** con nuevas métricas
- **Documentación** de hallazgos importantes

## 📁 Estructura Recomendada

```
notebooks/
├── 📊 exploratory/
│   ├── 01_data_overview.ipynb          # Vista general de los datos
│   ├── 02_ian_vs_expedients_validation.ipynb  # Validación de insights IAN
│   ├── 03_cost_analysis_deep_dive.ipynb       # Análisis profundo de costos
│   └── 04_temporal_analysis.ipynb             # Análisis temporal
├── 🔍 validation/
│   ├── 01_standardization_validation.ipynb    # Validar estandarización
│   ├── 02_data_quality_check.ipynb            # Verificar calidad de datos
│   └── 03_insights_validation.ipynb           # Validar insights principales
├── 📈 visualizations/
│   ├── 01_dashboard_mockups.ipynb             # Mockups de visualizaciones
│   ├── 02_interactive_charts.ipynb            # Gráficos interactivos
│   └── 03_report_templates.ipynb              # Plantillas de reportes
├── 🧪 experiments/
│   ├── 01_new_metrics.ipynb                   # Experimentar nuevas métricas
│   ├── 02_ml_models.ipynb                     # Modelos de ML (futuro)
│   └── 03_optimization_ideas.ipynb            # Ideas de optimización
└── 📋 templates/
    ├── analysis_template.ipynb                # Plantilla para nuevos análisis
    └── validation_template.ipynb              # Plantilla para validaciones
```

## 🚀 Cómo Usar

### 1. Configuración del Entorno

```bash
# Instalar Jupyter si no está instalado
pip install jupyter notebook

# O usar JupyterLab (recomendado)
pip install jupyterlab

# Activar el entorno virtual
source venv/bin/activate

# Iniciar Jupyter
jupyter lab
# o
jupyter notebook
```

### 2. Convenciones de Nomenclatura

- **Prefijos numéricos:** Para orden de ejecución
- **Nombres descriptivos:** Que indiquen el propósito
- **Sufijos:** `_validation`, `_experiment`, `_template`

### 3. Estructura de un Notebook

```python
# 1. Imports y configuración
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Configuración de visualización
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# 3. Carga de datos
df = pd.read_csv('../data/processed/resultados_pacientes_estandarizados.csv')

# 4. Análisis exploratorio
# ... código de análisis ...

# 5. Visualizaciones
# ... código de gráficos ...

# 6. Conclusiones e insights
# ... markdown con hallazgos ...
```

## 📊 Datos Disponibles

### Archivos Principales
- `../data/processed/resultados_pacientes_estandarizados.csv` - Datos principales
- `../data/processed/resultados_pacientes_combinados.csv` - Datos combinados
- `../data/processed/resumen_generado_2024_2025.csv` - Resúmenes

### Variables Clave
- `paciente` - ID del paciente
- `ian_expediente_hosp` - Identificador IAN
- `n_expediente_hosp` - Número de expediente
- `origen` - Origen del servicio (Urgencias, Hospitalización, Laboratorios)
- `area_servicio` - Área específica del servicio
- `monto_nivel_6` - Costo del servicio
- `fecha` - Fecha de atención

## 🔍 Insights a Validar

### 1. Flujo IAN vs Expedientes
- Confirmar que IAN = Triage/Observación
- Confirmar que Expediente = Hospitalización
- Analizar casos donde IAN = Expediente

### 2. Análisis de Costos
- Distribución por origen de servicio
- Costos promedio por paciente
- Identificar outliers y patrones

### 3. Análisis Temporal
- Tendencias por mes/año
- Estacionalidad en la atención
- Patrones de flujo temporal

### 4. Calidad de Datos
- Valores faltantes
- Inconsistencias en formatos
- Duplicados y anomalías

## 📝 Mejores Prácticas

### 1. Documentación
- **Títulos claros** en cada celda
- **Explicaciones** de lo que se está haciendo
- **Conclusiones** al final de cada análisis

### 2. Código
- **Funciones reutilizables** para análisis comunes
- **Configuración consistente** de visualizaciones
- **Manejo de errores** apropiado

### 3. Organización
- **Celdas pequeñas** y enfocadas
- **Separación clara** entre análisis y visualización
- **Comentarios** explicativos

### 4. Versionado
- **Commits regulares** de notebooks importantes
- **Nombres descriptivos** para commits
- **Documentación** de cambios importantes

## 🎨 Templates Disponibles

### analysis_template.ipynb
- Estructura básica para análisis exploratorio
- Configuración de imports y visualización
- Secciones predefinidas para diferentes tipos de análisis

### validation_template.ipynb
- Estructura para validar insights específicos
- Métricas de validación predefinidas
- Formato para reportar hallazgos

## 📈 Próximos Pasos

1. **Crear notebooks de validación** para insights principales
2. **Experimentar con visualizaciones** para el dashboard
3. **Validar métricas** antes de implementar en la API
4. **Documentar hallazgos** importantes para el equipo

---

## 📞 Notas

- **Backup regular:** Los notebooks pueden ser grandes, hacer backup frecuente
- **Colaboración:** Usar comentarios para explicar decisiones importantes
- **Iteración:** Los notebooks son para experimentar, no para código final
- **Documentación:** Exportar hallazgos importantes al README principal 