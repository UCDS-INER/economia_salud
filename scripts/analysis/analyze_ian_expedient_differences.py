#!/usr/bin/env python3
"""
Script para analizar las diferencias específicas entre IAN y expedientes.
Como todos los pacientes tienen ambos, analizamos cuándo y cómo se usan.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def analyze_ian_expedient_differences():
    """Analiza las diferencias específicas entre IAN y expedientes."""
    
    # Crear directorio de resultados si no existe
    resultados_path = Path("resultados")
    resultados_path.mkdir(exist_ok=True)
    
    print("Analizando diferencias específicas entre IAN y expedientes...")
    
    # Leer el archivo estandarizado
    df = pd.read_csv('data/processed/resultados_pacientes_estandarizados.csv', low_memory=False)
    print(f"Total de registros: {len(df):,}")
    
    # Crear archivo de análisis
    output_file = resultados_path / "analisis_diferencias_ian_expediente.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS DETALLADO: DIFERENCIAS ENTRE IAN Y EXPEDIENTES\n")
        f.write("="*70 + "\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("INSIGHT: Todos los pacientes tienen tanto IAN como expediente.\n")
        f.write("Análisis: Cuándo y cómo se usan cada uno en el flujo de atención.\n\n")
        
        # 1. Análisis de valores únicos
        f.write("1. ANÁLISIS DE VALORES ÚNICOS\n")
        f.write("-" * 50 + "\n")
        
        unique_ians = df['ian_expediente_hosp'].nunique()
        unique_expedients = df['n_expediente_hosp'].nunique()
        
        f.write(f"IAN únicos: {unique_ians:,}\n")
        f.write(f"Expedientes únicos: {unique_expedients:,}\n")
        f.write(f"Registros totales: {len(df):,}\n\n")
        
        # 2. Análisis de cuándo IAN = Expediente
        f.write("2. ANÁLISIS: ¿CUÁNDO IAN = EXPEDIENTE?\n")
        f.write("-" * 50 + "\n")
        
        # Casos donde IAN es igual al expediente
        ian_equals_expedient = df[df['ian_expediente_hosp'] == df['n_expediente_hosp']]
        ian_different_expedient = df[df['ian_expediente_hosp'] != df['n_expediente_hosp']]
        
        f.write(f"Registros donde IAN = Expediente: {len(ian_equals_expedient):,} ({len(ian_equals_expedient)/len(df)*100:.2f}%)\n")
        f.write(f"Registros donde IAN ≠ Expediente: {len(ian_different_expedient):,} ({len(ian_different_expedient)/len(df)*100:.2f}%)\n\n")
        
        # 3. Análisis por origen cuando IAN = Expediente
        f.write("3. ANÁLISIS POR ORIGEN - CUANDO IAN = EXPEDIENTE\n")
        f.write("-" * 50 + "\n")
        
        if 'origen' in ian_equals_expedient.columns:
            origen_counts_equal = ian_equals_expedient['origen'].value_counts()
            f.write("Distribución por origen cuando IAN = Expediente:\n")
            for origen, count in origen_counts_equal.items():
                f.write(f"  - {origen}: {count:,} registros ({count/len(ian_equals_expedient)*100:.2f}%)\n")
        f.write("\n")
        
        # 4. Análisis por origen cuando IAN ≠ Expediente
        f.write("4. ANÁLISIS POR ORIGEN - CUANDO IAN ≠ EXPEDIENTE\n")
        f.write("-" * 50 + "\n")
        
        if 'origen' in ian_different_expedient.columns:
            origen_counts_diff = ian_different_expedient['origen'].value_counts()
            f.write("Distribución por origen cuando IAN ≠ Expediente:\n")
            for origen, count in origen_counts_diff.items():
                f.write(f"  - {origen}: {count:,} registros ({count/len(ian_different_expedient)*100:.2f}%)\n")
        f.write("\n")
        
        # 5. Análisis de patrones en expedientes
        f.write("5. ANÁLISIS DE PATRONES EN EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Expedientes que empiezan con "000"
        expedients_with_000 = df[df['n_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        expedients_without_000 = df[~df['n_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        
        f.write(f"Expedientes que empiezan con '000': {len(expedients_with_000):,} ({len(expedients_with_000)/len(df)*100:.2f}%)\n")
        f.write(f"Expedientes sin '000': {len(expedients_without_000):,} ({len(expedients_without_000)/len(df)*100:.2f}%)\n\n")
        
        # 6. Análisis de patrones en IAN
        f.write("6. ANÁLISIS DE PATRONES EN IAN\n")
        f.write("-" * 50 + "\n")
        
        # IAN que empiezan con "000"
        ian_with_000 = df[df['ian_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        ian_without_000 = df[~df['ian_expediente_hosp'].astype(str).str.startswith('000', na=False)]
        
        f.write(f"IAN que empiezan con '000': {len(ian_with_000):,} ({len(ian_with_000)/len(df)*100:.2f}%)\n")
        f.write(f"IAN sin '000': {len(ian_without_000):,} ({len(ian_without_000)/len(df)*100:.2f}%)\n\n")
        
        # 7. Análisis de casos específicos
        f.write("7. ANÁLISIS DE CASOS ESPECÍFICOS\n")
        f.write("-" * 50 + "\n")
        
        # Tomar algunos ejemplos de cada caso
        f.write("Ejemplos donde IAN = Expediente:\n")
        sample_equal = ian_equals_expedient.head(5)
        for _, row in sample_equal.iterrows():
            f.write(f"  - Paciente {row['paciente']}: IAN={row['ian_expediente_hosp']}, Expediente={row['n_expediente_hosp']}, Origen={row.get('origen', 'N/A')}\n")
        f.write("\n")
        
        f.write("Ejemplos donde IAN ≠ Expediente:\n")
        sample_diff = ian_different_expedient.head(5)
        for _, row in sample_diff.iterrows():
            f.write(f"  - Paciente {row['paciente']}: IAN={row['ian_expediente_hosp']}, Expediente={row['n_expediente_hosp']}, Origen={row.get('origen', 'N/A')}\n")
        f.write("\n")
        
        # 8. Análisis por área de servicio
        f.write("8. ANÁLISIS POR ÁREA DE SERVICIO\n")
        f.write("-" * 50 + "\n")
        
        f.write("Top 10 áreas cuando IAN = Expediente:\n")
        if 'area_servicio' in ian_equals_expedient.columns:
            area_counts_equal = ian_equals_expedient['area_servicio'].value_counts().head(10)
            for area, count in area_counts_equal.items():
                f.write(f"  - {area}: {count:,} registros\n")
        f.write("\n")
        
        f.write("Top 10 áreas cuando IAN ≠ Expediente:\n")
        if 'area_servicio' in ian_different_expedient.columns:
            area_counts_diff = ian_different_expedient['area_servicio'].value_counts().head(10)
            for area, count in area_counts_diff.items():
                f.write(f"  - {area}: {count:,} registros\n")
        f.write("\n")
        
        # 9. Análisis de costos
        f.write("9. ANÁLISIS DE COSTOS\n")
        f.write("-" * 50 + "\n")
        
        if 'monto_nivel_6' in df.columns:
            f.write("Cuando IAN = Expediente:\n")
            f.write(f"  - Total gasto: ${ian_equals_expedient['monto_nivel_6'].sum():,.2f}\n")
            f.write(f"  - Promedio por registro: ${ian_equals_expedient['monto_nivel_6'].mean():,.2f}\n\n")
            
            f.write("Cuando IAN ≠ Expediente:\n")
            f.write(f"  - Total gasto: ${ian_different_expedient['monto_nivel_6'].sum():,.2f}\n")
            f.write(f"  - Promedio por registro: ${ian_different_expedient['monto_nivel_6'].mean():,.2f}\n\n")
        
        # 10. Análisis temporal
        f.write("10. ANÁLISIS TEMPORAL\n")
        f.write("-" * 50 + "\n")
        
        if 'fecha' in df.columns:
            try:
                df['fecha'] = pd.to_datetime(df['fecha'])
                
                f.write("Rango de fechas:\n")
                f.write(f"  - IAN = Expediente: {ian_equals_expedient['fecha'].min()} a {ian_equals_expedient['fecha'].max()}\n")
                f.write(f"  - IAN ≠ Expediente: {ian_different_expedient['fecha'].min()} a {ian_different_expedient['fecha'].max()}\n\n")
                
                f.write("Distribución por año:\n")
                for year in sorted(df['fecha'].dt.year.unique()):
                    year_data = df[df['fecha'].dt.year == year]
                    year_equal = year_data[year_data['ian_expediente_hosp'] == year_data['n_expediente_hosp']]
                    year_diff = year_data[year_data['ian_expediente_hosp'] != year_data['n_expediente_hosp']]
                    
                    f.write(f"  {year}:\n")
                    f.write(f"    - IAN = Expediente: {len(year_equal):,} registros\n")
                    f.write(f"    - IAN ≠ Expediente: {len(year_diff):,} registros\n")
            except:
                f.write("No se pudo analizar las fechas\n\n")
        
        # 11. Conclusiones e insights
        f.write("11. CONCLUSIONES E INSIGHTS\n")
        f.write("-" * 50 + "\n")
        
        f.write("Hallazgos principales:\n")
        f.write(f"1. {len(ian_equals_expedient):,} registros ({len(ian_equals_expedient)/len(df)*100:.1f}%) tienen IAN = Expediente\n")
        f.write(f"2. {len(ian_different_expedient):,} registros ({len(ian_different_expedient)/len(df)*100:.1f}%) tienen IAN ≠ Expediente\n")
        
        if 'origen' in df.columns:
            # Análisis por origen
            urgencias_equal = len(ian_equals_expedient[ian_equals_expedient['origen'] == 'Urgencias'])
            urgencias_diff = len(ian_different_expedient[ian_different_expedient['origen'] == 'Urgencias'])
            
            f.write(f"3. En Urgencias:\n")
            f.write(f"   - IAN = Expediente: {urgencias_equal:,} registros\n")
            f.write(f"   - IAN ≠ Expediente: {urgencias_diff:,} registros\n")
        
        f.write("\n4. Interpretación:\n")
        f.write("   - IAN = Expediente: Casos donde el paciente fue directamente hospitalizado\n")
        f.write("   - IAN ≠ Expediente: Casos donde el paciente pasó por triage/observación antes de hospitalización\n")
        f.write("   - El IAN puede ser el identificador inicial en triage\n")
        f.write("   - El expediente se genera cuando se confirma la hospitalización\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("Análisis completado.\n")
    
    print(f"Análisis completado. Resultados guardados en: {output_file}")
    
    # Crear también un CSV con el resumen
    create_difference_summary_csv(df, resultados_path)

def create_difference_summary_csv(df, resultados_path):
    """Crea un CSV con el resumen de diferencias."""
    
    # Crear resumen por paciente
    patient_summary = df.groupby('paciente').agg({
        'ian_expediente_hosp': 'first',
        'n_expediente_hosp': 'first',
        'origen': lambda x: list(x.unique()),
        'monto_nivel_6': 'sum'
    }).reset_index()
    
    # Agregar columna de diferencia
    patient_summary['ian_equals_expedient'] = patient_summary['ian_expediente_hosp'] == patient_summary['n_expediente_hosp']
    patient_summary['categoria'] = patient_summary['ian_equals_expedient'].map({
        True: 'IAN = Expediente (Hospitalización directa)',
        False: 'IAN ≠ Expediente (Triage + Hospitalización)'
    })
    
    # Guardar CSV
    csv_file = resultados_path / "resumen_diferencias_ian_expediente.csv"
    patient_summary.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"CSV con resumen de diferencias guardado en: {csv_file}")

if __name__ == "__main__":
    analyze_ian_expedient_differences() 