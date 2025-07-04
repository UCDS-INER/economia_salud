#!/usr/bin/env python3
"""
Script principal para ejecutar todo el pipeline de análisis de datos hospitalarios.
Este script ejecuta todos los pasos del procesamiento y análisis de manera ordenada.
"""

import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Agregar el directorio scripts al path para importar módulos
sys.path.append(str(Path(__file__).parent))

def run_step(step_name, script_path, description):
    """Ejecuta un paso del pipeline con logging detallado."""
    print(f"\n{'='*60}")
    print(f"🚀 EJECUTANDO: {step_name}")
    print(f"📝 Descripción: {description}")
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Ejecutar el script
        result = os.system(f"python {script_path}")
        
        if result == 0:
            end_time = time.time()
            duration = end_time - start_time
            print(f"\n✅ {step_name} completado exitosamente")
            print(f"⏱️  Duración: {duration:.2f} segundos")
            return True
        else:
            print(f"\n❌ Error en {step_name}")
            return False
            
    except Exception as e:
        print(f"\n❌ Excepción en {step_name}: {str(e)}")
        return False

def main():
    """Función principal que ejecuta todo el pipeline."""
    
    print("🏥 PROYECTO ECONOMÍA SALUD - PIPELINE COMPLETO")
    print("="*60)
    print(f"📅 Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🐍 Python version: {sys.version}")
    print("="*60)
    
    # Definir los pasos del pipeline
    pipeline_steps = [
        {
            "name": "Unión de Archivos CSV",
            "script": "scripts/data_processing/join.py",
            "description": "Combina los archivos CSV de diferentes períodos en un solo dataset"
        },
        {
            "name": "Estandarización de Expedientes",
            "script": "scripts/data_processing/standardize_expedients.py",
            "description": "Normaliza los expedientes y elimina duplicados por formato inconsistente"
        },
        {
            "name": "Generación de Resúmenes",
            "script": "scripts/data_processing/summarize.py",
            "description": "Genera resúmenes y comparaciones de los datos procesados"
        },
        {
            "name": "Análisis Exploratorio de Datos (EDA)",
            "script": "scripts/analysis/eda.py",
            "description": "Realiza análisis exploratorio completo de todos los datasets"
        },
        {
            "name": "Análisis IAN vs Expedientes",
            "script": "scripts/analysis/analyze_ian_vs_expedients.py",
            "description": "Analiza la distribución de pacientes por tipo de identificación"
        },
        {
            "name": "Análisis Detallado de Diferencias IAN-Expediente",
            "script": "scripts/analysis/analyze_ian_expedient_differences.py",
            "description": "Análisis profundo de las diferencias entre IAN y expedientes"
        },
        {
            "name": "Análisis de Diferencias de Costos",
            "script": "scripts/analysis/analyze_cost_differences.py",
            "description": "Analiza las diferencias de costos entre diferentes categorías"
        },
        {
            "name": "Análisis de Múltiples Expedientes",
            "script": "scripts/analysis/analyze_multiple_expedients.py",
            "description": "Identifica y analiza pacientes con múltiples expedientes"
        },
        {
            "name": "Análisis de Paciente Específico",
            "script": "scripts/analysis/analyze_specific_patient.py",
            "description": "Análisis detallado de un paciente específico como ejemplo"
        },
        {
            "name": "Análisis del Archivo de Resumen",
            "script": "scripts/analysis/analyze_summary_file.py",
            "description": "Analiza el archivo de resumen original y compara con el generado"
        }
    ]
    
    # Contadores para el resumen final
    successful_steps = 0
    failed_steps = 0
    total_start_time = time.time()
    
    # Ejecutar cada paso del pipeline
    for i, step in enumerate(pipeline_steps, 1):
        print(f"\n📋 Paso {i}/{len(pipeline_steps)}")
        
        if run_step(step["name"], step["script"], step["description"]):
            successful_steps += 1
        else:
            failed_steps += 1
            print(f"\n⚠️  ¿Deseas continuar con el siguiente paso? (s/n): ", end="")
            response = input().lower()
            if response != 's':
                print("🛑 Pipeline interrumpido por el usuario")
                break
    
    # Resumen final
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    
    print(f"\n{'='*60}")
    print("📊 RESUMEN FINAL DEL PIPELINE")
    print(f"{'='*60}")
    print(f"✅ Pasos exitosos: {successful_steps}")
    print(f"❌ Pasos fallidos: {failed_steps}")
    print(f"📈 Tasa de éxito: {(successful_steps/len(pipeline_steps)*100):.1f}%")
    print(f"⏱️  Tiempo total: {total_duration:.2f} segundos ({total_duration/60:.1f} minutos)")
    print(f"📅 Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_steps == 0:
        print("\n🎉 ¡Pipeline completado exitosamente!")
        print("📁 Los resultados están disponibles en la carpeta 'resultados/'")
        print("📖 Revisa el README.md para más información sobre los outputs")
    else:
        print(f"\n⚠️  Pipeline completado con {failed_steps} errores")
        print("🔍 Revisa los logs anteriores para identificar los problemas")
    
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 