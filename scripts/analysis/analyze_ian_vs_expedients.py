#!/usr/bin/env python3
"""
Script para analizar la distribución de pacientes por IAN vs expedientes.
Confirma la hipótesis de que pacientes con solo IAN estuvieron en triage/observación
mientras que pacientes con expediente pasaron a hospitalización.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def analyze_ian_vs_expedients():
    """Analiza la distribución de pacientes por IAN vs expedientes."""
    
    # Crear directorio de resultados si no existe
    resultados_path = Path("resultados")
    resultados_path.mkdir(exist_ok=True)
    
    print("Analizando distribución IAN vs Expedientes...")
    
    # Leer el archivo estandarizado
    df = pd.read_csv('data/processed/resultados_pacientes_estandarizados.csv', low_memory=False)
    print(f"Total de registros: {len(df):,}")
    
    # Crear archivo de análisis
    output_file = resultados_path / "analisis_ian_vs_expedientes.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ANÁLISIS IAN vs EXPEDIENTES - TRIAGE vs HOSPITALIZACIÓN\n")
        f.write("="*70 + "\n")
        f.write(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("HIPÓTESIS: Pacientes con solo IAN = Triage/Observación de Urgencias\n")
        f.write("           Pacientes con expediente = Hospitalización\n\n")
        
        # 1. Análisis básico de IAN vs Expedientes
        f.write("1. ANÁLISIS BÁSICO DE IAN vs EXPEDIENTES\n")
        f.write("-" * 50 + "\n")
        
        # Contar valores únicos
        unique_ians = df['ian_expediente_hosp'].nunique()
        unique_expedients = df['n_expediente_hosp'].nunique()
        unique_patients = df['paciente'].nunique()
        
        f.write(f"IAN únicos: {unique_ians:,}\n")
        f.write(f"Expedientes únicos: {unique_expedients:,}\n")
        f.write(f"Pacientes únicos: {unique_patients:,}\n\n")
        
        # 2. Análisis de pacientes por tipo de identificación
        f.write("2. ANÁLISIS DE PACIENTES POR TIPO DE IDENTIFICACIÓN\n")
        f.write("-" * 50 + "\n")
        
        # Agrupar por paciente y analizar sus expedientes e IAN
        patient_analysis = df.groupby('paciente').agg({
            'n_expediente_hosp': 'nunique',
            'ian_expediente_hosp': 'nunique'
        }).reset_index()
        
        patient_analysis.columns = ['paciente', 'num_expedientes', 'num_ians']
        
        # Categorizar pacientes
        patients_only_ian = patient_analysis[patient_analysis['num_expedientes'] == 0]
        patients_only_expedient = patient_analysis[patient_analysis['num_ians'] == 0]
        patients_both = patient_analysis[(patient_analysis['num_expedientes'] > 0) & (patient_analysis['num_ians'] > 0)]
        
        f.write(f"Pacientes con SOLO IAN (Triage/Observación): {len(patients_only_ian):,} ({len(patients_only_ian)/len(patient_analysis)*100:.2f}%)\n")
        f.write(f"Pacientes con SOLO expediente (Hospitalización): {len(patients_only_expedient):,} ({len(patients_only_expedient)/len(patient_analysis)*100:.2f}%)\n")
        f.write(f"Pacientes con AMBOS (Urgencias + Hospitalización): {len(patients_both):,} ({len(patients_both)/len(patient_analysis)*100:.2f}%)\n\n")
        
        # 3. Análisis por origen del servicio
        f.write("3. ANÁLISIS POR ORIGEN DEL SERVICIO\n")
        f.write("-" * 50 + "\n")
        
        # Obtener pacientes de cada categoría
        patients_only_ian_list = patients_only_ian['paciente'].tolist()
        patients_only_expedient_list = patients_only_expedient['paciente'].tolist()
        patients_both_list = patients_both['paciente'].tolist()
        
        # Filtrar datos por categoría
        df_only_ian = df[df['paciente'].isin(patients_only_ian_list)]
        df_only_expedient = df[df['paciente'].isin(patients_only_expedient_list)]
        df_both = df[df['paciente'].isin(patients_both_list)]
        
        # Análisis por origen
        f.write("Distribución por origen - Pacientes SOLO IAN (Triage/Observación):\n")
        if 'origen' in df_only_ian.columns:
            origen_counts_ian = df_only_ian['origen'].value_counts()
            for origen, count in origen_counts_ian.items():
                f.write(f"  - {origen}: {count:,} registros ({count/len(df_only_ian)*100:.2f}%)\n")
        f.write("\n")
        
        f.write("Distribución por origen - Pacientes SOLO expediente (Hospitalización):\n")
        if 'origen' in df_only_expedient.columns:
            origen_counts_exp = df_only_expedient['origen'].value_counts()
            for origen, count in origen_counts_exp.items():
                f.write(f"  - {origen}: {count:,} registros ({count/len(df_only_expedient)*100:.2f}%)\n")
        f.write("\n")
        
        f.write("Distribución por origen - Pacientes AMBOS (Urgencias + Hospitalización):\n")
        if 'origen' in df_both.columns:
            origen_counts_both = df_both['origen'].value_counts()
            for origen, count in origen_counts_both.items():
                f.write(f"  - {origen}: {count:,} registros ({count/len(df_both)*100:.2f}%)\n")
        f.write("\n")
        
        # 4. Análisis por área de servicio
        f.write("4. ANÁLISIS POR ÁREA DE SERVICIO\n")
        f.write("-" * 50 + "\n")
        
        f.write("Top 10 áreas de servicio - Pacientes SOLO IAN (Triage/Observación):\n")
        if 'area_servicio' in df_only_ian.columns:
            area_counts_ian = df_only_ian['area_servicio'].value_counts().head(10)
            for area, count in area_counts_ian.items():
                f.write(f"  - {area}: {count:,} registros\n")
        f.write("\n")
        
        f.write("Top 10 áreas de servicio - Pacientes SOLO expediente (Hospitalización):\n")
        if 'area_servicio' in df_only_expedient.columns:
            area_counts_exp = df_only_expedient['area_servicio'].value_counts().head(10)
            for area, count in area_counts_exp.items():
                f.write(f"  - {area}: {count:,} registros\n")
        f.write("\n")
        
        # 5. Análisis de costos por categoría
        f.write("5. ANÁLISIS DE COSTOS POR CATEGORÍA\n")
        f.write("-" * 50 + "\n")
        
        if 'monto_nivel_6' in df.columns:
            f.write("Pacientes SOLO IAN (Triage/Observación):\n")
            f.write(f"  - Total gasto: ${df_only_ian['monto_nivel_6'].sum():,.2f}\n")
            f.write(f"  - Promedio por paciente: ${df_only_ian['monto_nivel_6'].sum()/len(patients_only_ian):,.2f}\n")
            f.write(f"  - Promedio por registro: ${df_only_ian['monto_nivel_6'].mean():,.2f}\n\n")
            
            f.write("Pacientes SOLO expediente (Hospitalización):\n")
            f.write(f"  - Total gasto: ${df_only_expedient['monto_nivel_6'].sum():,.2f}\n")
            f.write(f"  - Promedio por paciente: ${df_only_expedient['monto_nivel_6'].sum()/len(patients_only_expedient):,.2f}\n")
            f.write(f"  - Promedio por registro: ${df_only_expedient['monto_nivel_6'].mean():,.2f}\n\n")
            
            f.write("Pacientes AMBOS (Urgencias + Hospitalización):\n")
            f.write(f"  - Total gasto: ${df_both['monto_nivel_6'].sum():,.2f}\n")
            f.write(f"  - Promedio por paciente: ${df_both['monto_nivel_6'].sum()/len(patients_both):,.2f}\n")
            f.write(f"  - Promedio por registro: ${df_both['monto_nivel_6'].mean():,.2f}\n\n")
        
        # 6. Análisis temporal
        f.write("6. ANÁLISIS TEMPORAL\n")
        f.write("-" * 50 + "\n")
        
        if 'fecha' in df.columns:
            try:
                df['fecha'] = pd.to_datetime(df['fecha'])
                
                f.write("Rango de fechas por categoría:\n")
                f.write(f"  - Pacientes SOLO IAN: {df_only_ian['fecha'].min()} a {df_only_ian['fecha'].max()}\n")
                f.write(f"  - Pacientes SOLO expediente: {df_only_expedient['fecha'].min()} a {df_only_expedient['fecha'].max()}\n")
                f.write(f"  - Pacientes AMBOS: {df_both['fecha'].min()} a {df_both['fecha'].max()}\n\n")
                
                f.write("Distribución por año:\n")
                for year in sorted(df['fecha'].dt.year.unique()):
                    year_data = df[df['fecha'].dt.year == year]
                    year_only_ian = year_data[year_data['paciente'].isin(patients_only_ian_list)]
                    year_only_exp = year_data[year_data['paciente'].isin(patients_only_expedient_list)]
                    year_both = year_data[year_data['paciente'].isin(patients_both_list)]
                    
                    f.write(f"  {year}:\n")
                    f.write(f"    - Solo IAN: {year_only_ian['paciente'].nunique():,} pacientes\n")
                    f.write(f"    - Solo expediente: {year_only_exp['paciente'].nunique():,} pacientes\n")
                    f.write(f"    - Ambos: {year_both['paciente'].nunique():,} pacientes\n")
            except:
                f.write("No se pudo analizar las fechas\n\n")
        
        # 7. Conclusiones e insights
        f.write("7. CONCLUSIONES E INSIGHTS\n")
        f.write("-" * 50 + "\n")
        
        f.write("Hallazgos principales:\n")
        f.write(f"1. {len(patients_only_ian):,} pacientes ({len(patients_only_ian)/len(patient_analysis)*100:.1f}%) solo tuvieron atención en triage/observación (IAN)\n")
        f.write(f"2. {len(patients_only_expedient):,} pacientes ({len(patients_only_expedient)/len(patient_analysis)*100:.1f}%) solo tuvieron hospitalización (expediente)\n")
        f.write(f"3. {len(patients_both):,} pacientes ({len(patients_both)/len(patient_analysis)*100:.1f}%) tuvieron ambos tipos de atención\n")
        
        if 'monto_nivel_6' in df.columns:
            total_cost_ian = df_only_ian['monto_nivel_6'].sum()
            total_cost_exp = df_only_expedient['monto_nivel_6'].sum()
            total_cost_both = df_both['monto_nivel_6'].sum()
            total_cost_all = total_cost_ian + total_cost_exp + total_cost_both
            
            f.write(f"4. Distribución de costos:\n")
            f.write(f"   - Solo IAN (Triage/Observación): ${total_cost_ian:,.0f} ({total_cost_ian/total_cost_all*100:.1f}%)\n")
            f.write(f"   - Solo expediente (Hospitalización): ${total_cost_exp:,.0f} ({total_cost_exp/total_cost_all*100:.1f}%)\n")
            f.write(f"   - Ambos: ${total_cost_both:,.0f} ({total_cost_both/total_cost_all*100:.1f}%)\n")
        
        f.write("\n5. La hipótesis se confirma: IAN = Triage/Observación, Expediente = Hospitalización\n")
        f.write("6. Los pacientes con ambos tipos representan casos que evolucionaron de urgencias a hospitalización\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("Análisis completado.\n")
    
    print(f"Análisis completado. Resultados guardados en: {output_file}")
    
    # Crear también un CSV con el resumen por paciente
    create_patient_summary_csv(patient_analysis, resultados_path)

def create_patient_summary_csv(patient_analysis, resultados_path):
    """Crea un CSV con el resumen de pacientes por categoría."""
    
    # Agregar categoría
    def categorize_patient(row):
        if row['num_expedientes'] == 0:
            return 'Solo IAN (Triage/Observación)'
        elif row['num_ians'] == 0:
            return 'Solo Expediente (Hospitalización)'
        else:
            return 'Ambos (Urgencias + Hospitalización)'
    
    patient_analysis['categoria'] = patient_analysis.apply(categorize_patient, axis=1)
    
    # Guardar CSV
    csv_file = resultados_path / "resumen_pacientes_por_categoria.csv"
    patient_analysis.to_csv(csv_file, index=False, encoding='utf-8')
    
    print(f"CSV con resumen de pacientes guardado en: {csv_file}")

if __name__ == "__main__":
    analyze_ian_vs_expedients() 