#!/usr/bin/env python3
"""
Script para generar resumen de pacientes y comparar con el archivo de resumen original.
Suma los totales del archivo combinado y genera estadísticas comparables.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def main():
    # Definir las rutas de los archivos
    processed_path = Path("data/processed")
    raw_path = Path("data/raw")
    
    print("Iniciando proceso de generación de resumen...")
    
    # Leer el archivo combinado
    combined_file = processed_path / "resultados_pacientes_combinados.csv"
    if not combined_file.exists():
        print("Error: No se encontró el archivo combinado. Ejecuta primero join.py")
        return
    
    print("Leyendo archivo combinado...")
    df_combined = pd.read_csv(combined_file, low_memory=False)
    print(f"Registros leídos: {len(df_combined):,}")
    
    # Leer el archivo de resumen original
    summary_file = raw_path / "Resumen Pacientes 2024-2025.csv"
    if not summary_file.exists():
        print("Error: No se encontró el archivo de resumen original")
        return
    
    print("Leyendo archivo de resumen original...")
    df_summary = pd.read_csv(summary_file, low_memory=False)
    print(f"Registros en resumen original: {len(df_summary):,}")
    
    # Generar resumen del archivo combinado
    print("\nGenerando resumen del archivo combinado...")
    
    # Agrupar por paciente y expediente para obtener totales únicos
    summary_combined = df_combined.groupby(['paciente', 'n_expediente_hosp', 'ian_expediente_hosp']).agg({
        'fecha': ['min', 'max'],  # Primera y última fecha
        'cantidad': 'sum',        # Total de cantidad
        'costo_nivel_6': 'sum',   # Total costo nivel 6
        'monto_nivel_1': 'sum',   # Total monto nivel 1
        'monto_nivel_6': 'sum',   # Total monto nivel 6
        'archivo_origen': 'first' # Archivo de origen
    }).reset_index()
    
    # Renombrar columnas
    summary_combined.columns = [
        'paciente', 'n_expediente_hosp', 'ian_expediente_hosp',
        'fecha_inicio', 'fecha_fin', 'total_cantidad',
        'total_costo_nivel_6', 'total_monto_nivel_1', 'total_monto_nivel_6',
        'archivo_origen'
    ]
    
    # Convertir fechas
    summary_combined['fecha_inicio'] = pd.to_datetime(summary_combined['fecha_inicio'])
    summary_combined['fecha_fin'] = pd.to_datetime(summary_combined['fecha_fin'])
    
    # Calcular días de estancia
    summary_combined['dias_estancia'] = (summary_combined['fecha_fin'] - summary_combined['fecha_inicio']).dt.days + 1
    
    # Agregar información adicional
    summary_combined['total_registros'] = df_combined.groupby(['paciente', 'n_expediente_hosp', 'ian_expediente_hosp']).size().values
    
    # Ordenar por paciente
    summary_combined = summary_combined.sort_values('paciente')
    
    # Guardar resumen generado
    output_file = processed_path / "resumen_generado_2024_2025.csv"
    summary_combined.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"Resumen guardado en: {output_file}")
    print(f"Total de pacientes únicos en resumen generado: {len(summary_combined):,}")
    
    # Generar comparación
    print("\nGenerando comparación...")
    
    # Estadísticas del resumen generado
    stats_generated = {
        'total_pacientes': len(summary_combined),
        'total_costo_nivel_6': summary_combined['total_costo_nivel_6'].sum(),
        'total_monto_nivel_1': summary_combined['total_monto_nivel_1'].sum(),
        'total_monto_nivel_6': summary_combined['total_monto_nivel_6'].sum(),
        'promedio_dias_estancia': summary_combined['dias_estancia'].mean(),
        'total_registros': summary_combined['total_registros'].sum()
    }
    
    # Estadísticas del resumen original
    stats_original = {
        'total_pacientes': len(df_summary),
        'total_costo_nivel_6': df_summary['gasto_nivel_6'].sum() if 'gasto_nivel_6' in df_summary.columns else 0,
        'total_monto_nivel_1': df_summary['gasto_nivel_1'].sum() if 'gasto_nivel_1' in df_summary.columns else 0,
        'total_monto_nivel_6': df_summary['gasto_nivel_6'].sum() if 'gasto_nivel_6' in df_summary.columns else 0,
        'promedio_dias_estancia': df_summary['dias_hopit'].mean() if 'dias_hopit' in df_summary.columns else 0
    }
    
    # Crear DataFrame de comparación
    comparison_data = []
    for metric in ['total_pacientes', 'total_costo_nivel_6', 'total_monto_nivel_1', 'total_monto_nivel_6', 'promedio_dias_estancia']:
        comparison_data.append({
            'metrica': metric,
            'resumen_original': stats_original[metric],
            'resumen_generado': stats_generated[metric],
            'diferencia': stats_generated[metric] - stats_original[metric],
            'diferencia_porcentual': ((stats_generated[metric] - stats_original[metric]) / stats_original[metric] * 100) if stats_original[metric] != 0 else 0
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    # Guardar comparación
    comparison_file = processed_path / "comparacion_resumenes.csv"
    comparison_df.to_csv(comparison_file, index=False, encoding='utf-8')
    
    print(f"Comparación guardada en: {comparison_file}")
    
    # Mostrar resumen de la comparación
    print("\n" + "="*60)
    print("RESUMEN DE COMPARACIÓN")
    print("="*60)
    
    for _, row in comparison_df.iterrows():
        print(f"\n{row['metrica'].replace('_', ' ').title()}:")
        print(f"  Original: {row['resumen_original']:,.2f}")
        print(f"  Generado: {row['resumen_generado']:,.2f}")
        print(f"  Diferencia: {row['diferencia']:,.2f} ({row['diferencia_porcentual']:+.2f}%)")
    
    # Información adicional
    print(f"\nInformación adicional:")
    print(f"- Total de registros en archivo combinado: {len(df_combined):,}")
    print(f"- Total de registros únicos por paciente/expediente: {stats_generated['total_registros']:,}")
    print(f"- Promedio de registros por paciente: {stats_generated['total_registros'] / stats_generated['total_pacientes']:.2f}")

if __name__ == "__main__":
    main() 