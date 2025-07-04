#!/usr/bin/env python3
"""
Script para unir archivos CSV de resultados de pacientes.
Combina los archivos de diferentes períodos en un solo archivo procesado.
"""

import pandas as pd
import os
from pathlib import Path

def main():
    # Definir las rutas de los archivos
    base_path = Path("data/raw")
    output_path = Path("data/processed")
    
    # Lista de archivos a unir
    files_to_join = [
        "Resultados Pacientes Jan 2024 - Jul 2024.csv",
        "Resultados Pacientes Jan-Jun 2025.csv", 
        "Resultados Pacientes Jul 2024 - Ene 2025.csv"
    ]
    
    # Crear directorio de salida si no existe
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Lista para almacenar todos los DataFrames
    dataframes = []
    
    print("Iniciando proceso de unión de archivos CSV...")
    
    # Leer cada archivo
    for filename in files_to_join:
        file_path = base_path / filename
        if file_path.exists():
            print(f"Leyendo: {filename}")
            try:
                # Leer el CSV con encoding utf-8 y manejo de errores
                df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
                print(f"  - Filas leídas: {len(df)}")
                print(f"  - Columnas: {list(df.columns)}")
                
                # Agregar una columna para identificar el archivo de origen
                df['archivo_origen'] = filename
                
                dataframes.append(df)
                
            except Exception as e:
                print(f"Error leyendo {filename}: {e}")
                # Intentar con encoding diferente
                try:
                    df = pd.read_csv(file_path, encoding='latin-1', on_bad_lines='skip')
                    print(f"  - Filas leídas (latin-1): {len(df)}")
                    df['archivo_origen'] = filename
                    dataframes.append(df)
                except Exception as e2:
                    print(f"Error con encoding alternativo: {e2}")
        else:
            print(f"Archivo no encontrado: {filename}")
    
    if not dataframes:
        print("No se pudieron leer archivos. Verificar que los archivos existan.")
        return
    
    # Unir todos los DataFrames
    print("\nUniendo archivos...")
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    print(f"Total de filas combinadas: {len(combined_df)}")
    print(f"Total de columnas: {len(combined_df.columns)}")
    
    # Guardar el archivo combinado
    output_file = output_path / "resultados_pacientes_combinados.csv"
    combined_df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\nArchivo guardado exitosamente en: {output_file}")
    
    # Mostrar información adicional
    print("\nInformación del dataset combinado:")
    print(f"- Forma del dataset: {combined_df.shape}")
    print(f"- Columnas: {list(combined_df.columns)}")
    
    # Mostrar conteo por archivo de origen
    print("\nConteo por archivo de origen:")
    print(combined_df['archivo_origen'].value_counts())

if __name__ == "__main__":
    main()
