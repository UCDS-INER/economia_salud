#!/usr/bin/env python3
"""
Script de test para verificar la configuración del proyecto.
Verifica dependencias, estructura de carpetas y archivos necesarios.
"""

import sys
import os
from pathlib import Path

def test_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NO INSTALADO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Paquetes faltantes: {', '.join(missing_packages)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def test_directory_structure():
    """Verifica que la estructura de directorios esté correcta."""
    print("\n📁 Verificando estructura de directorios...")
    
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/database',
        'scripts/data_processing',
        'scripts/analysis',
        'scripts/utils',
        'resultados/reports',
        'resultados/insights',
        'resultados/visualizations',
        'docs/architecture',
        'docs/api',
        'docs/user_guides'
    ]
    
    missing_dirs = []
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} - NO EXISTE")
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"\n⚠️  Directorios faltantes: {', '.join(missing_dirs)}")
        print("💡 Ejecuta: mkdir -p " + " ".join(missing_dirs))
        return False
    
    print("✅ Estructura de directorios correcta")
    return True

def test_data_files():
    """Verifica que los archivos de datos necesarios existan."""
    print("\n📊 Verificando archivos de datos...")
    
    # Verificar archivos raw (opcionales, pueden no existir)
    raw_files = [
        'data/raw/Resultados Pacientes Jan 2024 - Jul 2024.csv',
        'data/raw/Resultados Pacientes Jan-Jun 2025.csv',
        'data/raw/Resultados Pacientes Jul 2024 - Ene 2025.csv'
    ]
    
    raw_files_exist = 0
    for file_path in raw_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
            raw_files_exist += 1
        else:
            print(f"  ⚠️  {file_path} - NO EXISTE (opcional)")
    
    if raw_files_exist == 0:
        print("⚠️  No se encontraron archivos de datos raw")
        print("💡 Coloca los archivos CSV en data/raw/ para ejecutar el análisis")
    
    # Verificar archivos procesados (opcionales, se generan durante el análisis)
    processed_files = [
        'data/processed/resultados_pacientes_combinados.csv',
        'data/processed/resultados_pacientes_estandarizados.csv'
    ]
    
    for file_path in processed_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  {file_path} - NO EXISTE (se genera durante el análisis)")
    
    return True

def test_scripts():
    """Verifica que los scripts principales existan."""
    print("\n🔧 Verificando scripts principales...")
    
    required_scripts = [
        'scripts/data_processing/join.py',
        'scripts/data_processing/standardize_expedients.py',
        'scripts/data_processing/summarize.py',
        'scripts/analysis/eda.py',
        'scripts/analysis/analyze_ian_vs_expedients.py',
        'scripts/analysis/analyze_ian_expedient_differences.py',
        'scripts/run_complete_analysis.py'
    ]
    
    missing_scripts = []
    
    for script_path in required_scripts:
        if Path(script_path).exists():
            print(f"  ✅ {script_path}")
        else:
            print(f"  ❌ {script_path} - NO EXISTE")
            missing_scripts.append(script_path)
    
    if missing_scripts:
        print(f"\n⚠️  Scripts faltantes: {', '.join(missing_scripts)}")
        return False
    
    print("✅ Scripts principales encontrados")
    return True

def test_python_version():
    """Verifica la versión de Python."""
    print("\n🐍 Verificando versión de Python...")
    
    version = sys.version_info
    print(f"  Versión actual: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("  ✅ Versión de Python compatible")
        return True
    else:
        print("  ❌ Se requiere Python 3.8 o superior")
        return False

def main():
    """Función principal del test."""
    print("🧪 TEST DE CONFIGURACIÓN DEL PROYECTO")
    print("="*50)
    
    tests = [
        ("Versión de Python", test_python_version),
        ("Dependencias", test_dependencies),
        ("Estructura de directorios", test_directory_structure),
        ("Archivos de datos", test_data_files),
        ("Scripts principales", test_scripts)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Error en {test_name}: {str(e)}")
    
    print("\n" + "="*50)
    print("📊 RESUMEN DE TESTS")
    print(f"✅ Tests pasados: {passed_tests}/{total_tests}")
    print(f"📈 Tasa de éxito: {(passed_tests/total_tests*100):.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡Configuración correcta!")
        print("🚀 Puedes ejecutar: python scripts/run_complete_analysis.py")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} problemas encontrados")
        print("🔧 Revisa los mensajes anteriores para solucionarlos")
    
    print("="*50)

if __name__ == "__main__":
    main() 