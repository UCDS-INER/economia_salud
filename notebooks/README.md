# 📓 Notebooks - Economía Salud

Esta carpeta contiene los notebooks especializados para el análisis integral de datos hospitalarios. Cada notebook está diseñado para un aspecto específico del análisis, desde exploración básica hasta análisis temporal avanzado.

## 📋 Índice de Notebooks

### 🔍 Notebooks Exploratorios Principales

| Notebook | Estado | Descripción | Funcionalidades Clave |
|----------|--------|-------------|------------------------|
| **01_data_overview_professional.ipynb** | ✅ **Principal** | Análisis exploratorio completo y profesional | 14 celdas, métricas validadas, resumen ejecutivo |
| **02_outliers_analysis.ipynb** | ✅ **Completado** | Detección multidimensional de outliers | Métodos múltiples, categorización, rankings |
| **03_temporal_analysis_enhanced.ipynb** | ✅ **Completado** | Análisis temporal avanzado con visualizaciones | Heatmaps, distribuciones, correlaciones temporales |
| **03_temporal_analysis_complete.ipynb** | ✅ **Archivado** | Primera versión de análisis temporal | Base para versión mejorada |
| **01_data_overview.ipynb** | ✅ **Archivado** | Primera versión de análisis exploratorio | Análisis básico inicial |

---

## 📊 Análisis Detallado por Notebook

### 🏆 **01_data_overview_professional.ipynb**
**Notebook Principal - Análisis Exploratorio Completo**

**📈 Métricas Validadas:**
- **2,399,200 servicios hospitalarios** de **5,782 pacientes únicos**
- **$1,178,751,841** en costos totales analizados
- **Período:** 14 Junio 2023 - 31 Mayo 2025 (717 días)

**🔧 Estructura del Notebook (14 Celdas):**
1. **Header Corporativo** - Información del proyecto y contexto
2. **Configuración Profesional** - Setup del entorno con funciones helper
3. **Carga y Validación** - Datos con manejo robusto de errores
4. **Estadísticas Descriptivas** - Métricas principales del sistema
5. **Análisis por Origen** - Hospitalización (57.5%), Labs (25.9%), Urgencias (16.7%)
6. **Comparación IAN vs Expedientes** - Validación de flujo (99.98% consistencia)
7. **Perfiles de Pacientes** - Segmentación por complejidad
8. **Relación Cantidad vs Costo** - Análisis de eficiencia operativa
9. **Resumen Ejecutivo** - Insights y recomendaciones estratégicas

**💡 Insights Principales:**
- **Concentración de costos:** Top 10 pacientes = $42.1M (3.6% del total)
- **Eficiencia por origen:** Labs $619/unidad vs Hospitalización $58.65/unidad
- **Distribución:** 55.8% servicios unitarios vs 44.2% servicios múltiples
- **Variabilidad:** Coeficiente de variación costo/unidad = 770%

---

### 🔍 **02_outliers_analysis.ipynb**  
**Análisis Multidimensional de Outliers**

**🎯 Metodologías Implementadas:**
- **IQR (Interquartile Range)** - Método robusto clásico
- **Z-Score** - Detección paramétrica estándar  
- **Modified Z-Score** - Método resistente a outliers extremos

**📊 Dimensiones de Análisis:**
1. **Outliers por Costo Total de Pacientes**
   - Extreme: 89 pacientes con costos >$2.5M
   - Moderate: 145 pacientes ($500K-$2.5M)
   - Impacto: Top 1% representa 15% del costo total

2. **Outliers por Cantidad/Unidades**
   - Extreme: 847 cargos con >100 unidades
   - Concentración: 0.04% de cargos = servicios masivos
   - Patrón: Medicamentos y materiales quirúrgicos

3. **Outliers por Costo Unitario**
   - Extreme: 15,252 servicios con costo/unidad >$10K
   - Rango: $10K hasta $2.8M por unidad
   - Áreas: Procedimientos especializados

**🔧 Funciones Especializadas:**
```python
def detect_outliers_iqr(data, column, factor=1.5)
def detect_outliers_zscore(data, column, threshold=3)  
def detect_outliers_modified_zscore(data, column, threshold=3.5)
def categorize_outlier_severity(data, column)
def analyze_outliers_by_origin(data, outlier_method='iqr')
```

**📈 Categorización por Severidad:**
- **Extreme:** >Q3 + 3*IQR (Requires immediate attention)
- **Moderate:** Q3 + 1.5*IQR to Q3 + 3*IQR (Monitor closely)
- **Mild:** Q3 to Q3 + 1.5*IQR (Watch for patterns)
- **Normal:** ≤Q3 (Standard range)

---

### ⏰ **03_temporal_analysis_enhanced.ipynb**
**Análisis Temporal Avanzado con Visualizaciones Mejoradas**

**🎨 Visualizaciones Implementadas:**

**🔥 Heatmaps Temporales Especializados:**
- **Día de Semana vs Hora** - Patrones de actividad con intensidad horaria
- **Mes vs Día del Mes** - Distribución calendárica completa
- **Año vs Semana del Año** - Evolución semanal comparativa
- **Trimestre vs Mes** - Análisis estacional granular

**📊 Distribuciones Avanzadas:**
- **Histogramas con KDE** - Distribución de costos diarios con curvas de densidad
- **Boxplots Coloreados** - Variabilidad semanal con quartiles y outliers
- **Violin Plots** - Distribución mensual mostrando forma completa de datos
- **Matriz de Correlación** - Heatmap temporal con valores anotados

**🎯 Heatmaps Especializados por Servicios:**
- **Top 10 Servicios vs Mes** - Patrones estacionales normalizados
- **Áreas vs Trimestre** - Distribución trimestral por departamento
- **Servicios vs Día de Semana** - Patrones semanales de utilización
- **Áreas vs Hora del Día** - Intensidad horaria por departamento
- **Crecimiento Anual** - Tasas de crecimiento con valores anotados
- **Correlación entre Áreas** - Interdependencias departamentales

**📈 Análisis Integrado (12 Componentes):**
1. Tendencias principales con medias móviles suavizadas
2. Decomposición estacional con tendencias cuadráticas
3. Heatmap calendario de últimos 12 meses
4. Distribución por cuartiles evolutiva
5. Top 5 servicios y evolución temporal
6. Correlaciones temporales entre métricas clave
7. Volatilidad temporal con rolling windows
8. Distribución horaria en vista polar
9. Evolución por áreas normalizada estacionalmente
10. KPIs de performance con métricas dual-axis
11. Resumen estadístico anual como heatmap
12. Predicción básica para próximos 6 meses

**🌈 Mejoras Técnicas:**
- **Paletas profesionales** con gradientes especializados
- **Interpolación bilinear** para suavidad visual
- **Normalización apropiada** para comparaciones válidas
- **Colorbars informativos** con unidades claras
- **Anotaciones de valores** en celdas críticas

**📊 Insights Temporales Clave:**
- **Período Real:** 14 Jun 2023 - 31 May 2025 (717 días exactos)
- **Distribución:** 3.7% (2023) + 70.8% (2024) + 25.5% (2025)
- **Estacionalidad:** Q4 muestra picos de +15% vs promedio
- **Volatilidad:** CV temporal del 45% con control de picos
- **Correlación:** 0.85 entre servicios y costos temporalmente

---

### 📊 **03_temporal_analysis_complete.ipynb**
**Primera Versión Completa - Archivado**

**Estado:** ✅ Archivado (Base para versión mejorada)
**Propósito:** Desarrollo inicial del análisis temporal
**Contenido:** Análisis base con todas las granularidades temporales
**Evolución:** Mejorado hacia `03_temporal_analysis_enhanced.ipynb`

---

### 📈 **01_data_overview.ipynb**
**Primera Versión Exploratorio - Archivado**

**Estado:** ✅ Archivado (Reemplazado por versión profesional)
**Propósito:** Análisis exploratorio inicial y pruebas
**Contenido:** Exploración básica de datos y primeras métricas
**Evolución:** Evolucionó hacia `01_data_overview_professional.ipynb`

---

## 🔧 Configuración y Ejecución

### Prerrequisitos
```bash
# Instalar dependencias
pip install pandas numpy matplotlib seaborn plotly scipy jupyter

# O usar requirements del proyecto
pip install -r ../requirements.txt
```

### Ejecutar Notebooks
```bash
# Desde directorio raíz del proyecto
jupyter notebook notebooks/exploratory/

# O ejecutar específicamente
jupyter notebook notebooks/exploratory/01_data_overview_professional.ipynb
```

### Orden Recomendado de Ejecución
1. **01_data_overview_professional.ipynb** - Comenzar con análisis general
2. **02_outliers_analysis.ipynb** - Profundizar en detección de anomalías  
3. **03_temporal_analysis_enhanced.ipynb** - Analizar patrones temporales

---

## 📁 Estructura de Directorios

```
notebooks/
├── exploratory/                    # Notebooks principales ✅
│   ├── 01_data_overview_professional.ipynb    # 🏆 Principal
│   ├── 02_outliers_analysis.ipynb             # 🔍 Outliers  
│   ├── 03_temporal_analysis_enhanced.ipynb    # ⏰ Temporal
│   ├── 03_temporal_analysis_complete.ipynb    # 📊 Archivado
│   └── 01_data_overview.ipynb                 # 📈 Archivado
├── validation/                     # Notebooks de validación 📋
├── templates/                      # Templates para futuros análisis 📋
└── README.md                       # Esta documentación ✅
```

---

## 🎯 Próximos Notebooks Planificados

### 📋 **En Desarrollo**
- **04_patient_segmentation.ipynb** - Clustering de pacientes por patrones
- **05_service_area_analysis.ipynb** - Benchmarking por áreas de servicio
- **06_temporal_outliers.ipynb** - Outliers estacionales y anomalías

### 📋 **Planificados**
- **07_predictive_models.ipynb** - Modelos de forecasting y alertas
- **08_cost_optimization.ipynb** - Análisis de optimización de costos
- **09_dashboard_preparation.ipynb** - Preparación de datos para dashboard

---

## 📊 Métricas de Desarrollo

### Notebooks Completados
- **Total:** 5 notebooks desarrollados
- **Principales:** 3 notebooks operativos  
- **Archivados:** 2 notebooks (base para evolución)
- **Celdas totales:** 50+ celdas especializadas
- **Líneas de código:** 3,000+ líneas documentadas

### Funcionalidades Implementadas
- ✅ **Análisis exploratorio completo** con validación de datos
- ✅ **Detección multimétodo de outliers** con categorización
- ✅ **Análisis temporal avanzado** con 12 componentes integrados
- ✅ **Visualizaciones profesionales** con heatmaps y distribuciones
- ✅ **Correlaciones temporales** y análisis de volatilidad
- ✅ **Predicción básica** para forecasting

### Cobertura de Análisis
- **Datos procesados:** 2.4M registros (100%)
- **Pacientes analizados:** 5,782 únicos (100%)
- **Período temporal:** 717 días completos (100%)
- **Áreas de servicio:** Todas incluidas y analizadas
- **Descripciones de servicios:** +1000 categorizadas

---

## 💡 Tips para Desarrollo

### Mejores Prácticas
- **Documentar celdas** con markdown explicativo
- **Usar funciones reutilizables** para análisis complejos
- **Validar datos** antes de análisis profundos
- **Mantener notebooks limpios** eliminando outputs innecesarios
- **Versionar cambios importantes** en archivos separados

### Convenciones de Nomenclatura
- **01_**, **02_**, **03_** - Orden de ejecución recomendado
- **_professional** - Versión mejorada/final
- **_enhanced** - Versión con mejoras visuales
- **_complete** - Versión completa pero archivada

### Estructura de Celdas Recomendada
1. **Título y descripción** (Markdown)
2. **Imports y configuración** (Code)
3. **Carga de datos** (Code)
4. **Análisis específico** (Code + Markdown)
5. **Visualizaciones** (Code)
6. **Interpretación** (Markdown)
7. **Conclusiones** (Markdown)

---

**🚀 Notebooks desarrollados para análisis hospitalario integral**

**📧 Soporte técnico:** [economia.salud@iner.gob.mx](mailto:economia.salud@iner.gob.mx) 