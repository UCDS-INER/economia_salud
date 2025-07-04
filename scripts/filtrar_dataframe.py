#!/usr/bin/env python3
"""
Script para demostrar diferentes formas de filtrar un DataFrame para valores específicos
"""

import pandas as pd
import numpy as np

def cargar_datos_ejemplo():
    """Carga datos de ejemplo o crea un DataFrame de muestra"""
    try:
        # Intentar cargar datos reales
        df = pd.read_csv('../data/processed/resumen_generado_2024_2025.csv')
        print(f"✅ Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
        print(f"Columnas disponibles: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"⚠️ No se pudieron cargar los datos reales: {e}")
        print("Creando DataFrame de ejemplo...")
        
        # Crear DataFrame de ejemplo
        np.random.seed(42)
        data = {
            'paciente_id': range(1, 101),
            'nombre': [f'Paciente_{i}' for i in range(1, 101)],
            'edad': np.random.randint(18, 85, 100),
            'genero': np.random.choice(['M', 'F'], 100),
            'diagnostico': np.random.choice(['Diabetes', 'Hipertensión', 'Cardiopatía', 'Cáncer'], 100),
            'costo_total': np.random.uniform(1000, 50000, 100).round(2),
            'fecha_ingreso': pd.date_range('2024-01-01', periods=100, freq='D'),
            'estado': np.random.choice(['Activo', 'Inactivo', 'Alta'], 100)
        }
        df = pd.DataFrame(data)
        print(f"✅ DataFrame de ejemplo creado: {len(df)} filas")
        return df

def filtrar_por_valor_exacto(df, columna, valor):
    """
    Filtra el DataFrame por un valor exacto en una columna específica
    
    Args:
        df: DataFrame a filtrar
        columna: Nombre de la columna
        valor: Valor específico a buscar
    
    Returns:
        DataFrame filtrado
    """
    print(f"\n🔍 Filtrando por {columna} = {valor}")
    
    # Método 1: Usando operador de igualdad
    df_filtrado = df[df[columna] == valor]
    
    # Método 2: Usando query (más legible)
    # df_filtrado = df.query(f"{columna} == '{valor}'")
    
    print(f"Resultados encontrados: {len(df_filtrado)} filas")
    return df_filtrado

def filtrar_por_multiples_valores(df, columna, valores):
    """
    Filtra el DataFrame por múltiples valores en una columna
    
    Args:
        df: DataFrame a filtrar
        columna: Nombre de la columna
        valores: Lista de valores a buscar
    
    Returns:
        DataFrame filtrado
    """
    print(f"\n🔍 Filtrando por {columna} en {valores}")
    
    # Método 1: Usando isin()
    df_filtrado = df[df[columna].isin(valores)]
    
    # Método 2: Usando query
    # valores_str = "', '".join(valores)
    # df_filtrado = df.query(f"{columna} in ['{valores_str}']")
    
    print(f"Resultados encontrados: {len(df_filtrado)} filas")
    return df_filtrado

def filtrar_por_rango(df, columna, valor_min, valor_max):
    """
    Filtra el DataFrame por un rango de valores
    
    Args:
        df: DataFrame a filtrar
        columna: Nombre de la columna
        valor_min: Valor mínimo (inclusive)
        valor_max: Valor máximo (inclusive)
    
    Returns:
        DataFrame filtrado
    """
    print(f"\n🔍 Filtrando por {columna} entre {valor_min} y {valor_max}")
    
    # Método 1: Usando operadores de comparación
    df_filtrado = df[(df[columna] >= valor_min) & (df[columna] <= valor_max)]
    
    # Método 2: Usando query
    # df_filtrado = df.query(f"{columna} >= {valor_min} and {columna} <= {valor_max}")
    
    # Método 3: Usando between()
    # df_filtrado = df[df[columna].between(valor_min, valor_max)]
    
    print(f"Resultados encontrados: {len(df_filtrado)} filas")
    return df_filtrado

def filtrar_por_condiciones_complejas(df):
    """
    Ejemplo de filtrado con múltiples condiciones
    
    Args:
        df: DataFrame a filtrar
    
    Returns:
        DataFrame filtrado
    """
    print(f"\n🔍 Filtrando con condiciones complejas")
    
    # Ejemplo: Pacientes activos con costo > 20000 y edad > 50
    df_filtrado = df[
        (df['estado'] == 'Activo') & 
        (df['costo_total'] > 20000) & 
        (df['edad'] > 50)
    ]
    
    # Alternativa usando query
    # df_filtrado = df.query("estado == 'Activo' and costo_total > 20000 and edad > 50")
    
    print(f"Resultados encontrados: {len(df_filtrado)} filas")
    return df_filtrado

def filtrar_por_texto_parcial(df, columna, texto):
    """
    Filtra el DataFrame por texto parcial (contiene)
    
    Args:
        df: DataFrame a filtrar
        columna: Nombre de la columna
        texto: Texto a buscar
    
    Returns:
        DataFrame filtrado
    """
    print(f"\n🔍 Filtrando por {columna} que contenga '{texto}'")
    
    # Método 1: Usando str.contains()
    df_filtrado = df[df[columna].str.contains(texto, case=False, na=False)]
    
    # Método 2: Usando query con str.contains
    # df_filtrado = df.query(f"{columna}.str.contains('{texto}', case=False, na=False)")
    
    print(f"Resultados encontrados: {len(df_filtrado)} filas")
    return df_filtrado

def mostrar_ejemplos_filtrado(df):
    """Muestra ejemplos prácticos de filtrado"""
    print("\n" + "="*60)
    print("EJEMPLOS DE FILTRADO DE DATAFRAME")
    print("="*60)
    
    # 1. Filtrar por valor exacto
    print("\n1️⃣ FILTRADO POR VALOR EXACTO")
    pacientes_activos = filtrar_por_valor_exacto(df, 'estado', 'Activo')
    if len(pacientes_activos) > 0:
        print(pacientes_activos.head())
    
    # 2. Filtrar por múltiples valores
    print("\n2️⃣ FILTRADO POR MÚLTIPLES VALORES")
    diagnosticos_especificos = filtrar_por_multiples_valores(df, 'diagnostico', ['Diabetes', 'Hipertensión'])
    if len(diagnosticos_especificos) > 0:
        print(diagnosticos_especificos.head())
    
    # 3. Filtrar por rango
    print("\n3️⃣ FILTRADO POR RANGO")
    pacientes_edad_media = filtrar_por_rango(df, 'edad', 40, 60)
    if len(pacientes_edad_media) > 0:
        print(pacientes_edad_media.head())
    
    # 4. Filtrar por costo alto
    print("\n4️⃣ FILTRADO POR COSTO ALTO")
    pacientes_costo_alto = filtrar_por_rango(df, 'costo_total', 30000, 50000)
    if len(pacientes_costo_alto) > 0:
        print(pacientes_costo_alto.head())
    
    # 5. Filtrar por texto parcial
    print("\n5️⃣ FILTRADO POR TEXTO PARCIAL")
    pacientes_diabetes = filtrar_por_texto_parcial(df, 'diagnostico', 'diabetes')
    if len(pacientes_diabetes) > 0:
        print(pacientes_diabetes.head())
    
    # 6. Condiciones complejas
    print("\n6️⃣ FILTRADO CON CONDICIONES COMPLEJAS")
    pacientes_complejos = filtrar_por_condiciones_complejas(df)
    if len(pacientes_complejos) > 0:
        print(pacientes_complejos.head())

def main():
    """Función principal"""
    print("🚀 Iniciando script de filtrado de DataFrame")
    
    # Cargar datos
    df = cargar_datos_ejemplo()
    
    # Mostrar información básica
    print(f"\n📊 Información del DataFrame:")
    print(f"Dimensiones: {df.shape}")
    print(f"Tipos de datos:")
    print(df.dtypes)
    
    # Mostrar primeras filas
    print(f"\n👀 Primeras 5 filas:")
    print(df.head())
    
    # Mostrar ejemplos de filtrado
    mostrar_ejemplos_filtrado(df)
    
    print("\n✅ Script completado!")
    print("\n💡 TIPS ADICIONALES:")
    print("- Usa .query() para filtros más legibles")
    print("- Usa .between() para rangos")
    print("- Usa .str.contains() para búsqueda de texto")
    print("- Usa .isin() para múltiples valores")
    print("- Combina condiciones con & (AND) y | (OR)")

if __name__ == "__main__":
    main() 