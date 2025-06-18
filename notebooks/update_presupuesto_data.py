#!/usr/bin/env python3
"""
Script de Actualización Automática de Datos del Presupuesto Público
Ejecuta el notebook y actualiza los datos en la aplicación Streamlit
"""

import subprocess
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def main():
    """
    Función principal para actualización de datos
    """
    print("🚀 INICIANDO ACTUALIZACIÓN DE DATOS DEL PRESUPUESTO PÚBLICO")
    print("=" * 60)
    
    # Rutas
    notebook_path = Path(__file__).parent / "04_Analisis_Presupuesto_Publico.ipynb"
    app_data_path = Path(__file__).parent.parent / "app" / "data" / "processed"
    
    try:
        # 1. Ejecutar notebook completo
        print("📓 1. EJECUTANDO NOTEBOOK...")
        result = subprocess.run([
            "jupyter", "nbconvert", 
            "--to", "notebook",
            "--execute",
            "--inplace",
            str(notebook_path)
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("   ✅ Notebook ejecutado exitosamente")
        else:
            print(f"   ❌ Error ejecutando notebook: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Timeout ejecutando notebook (>5 min)")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False
    
    # 2. Verificar archivos generados
    print("\n📂 2. VERIFICANDO ARCHIVOS GENERADOS...")
    
    required_files = [
        "resumen_ejecutivo.json",
        "presupuesto_chile_2024.csv",
        "ejecucion_presupuestaria_2024.csv",
        "transferencias_regionales_2024.csv",
        "top_ministerios.csv",
        "top_regiones.csv",
        "distribucion_sectores.csv",
        "metadatos.json"
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = app_data_path / file_name
        if file_path.exists():
            print(f"   ✅ {file_name}")
        else:
            print(f"   ❌ {file_name} - FALTANTE")
            missing_files.append(file_name)
    
    if missing_files:
        print(f"\n⚠️  ARCHIVOS FALTANTES: {len(missing_files)}")
        return False
    
    # 3. Validar integridad de datos
    print("\n🔍 3. VALIDANDO INTEGRIDAD DE DATOS...")
    
    try:
        # Cargar resumen ejecutivo
        with open(app_data_path / "resumen_ejecutivo.json", 'r') as f:
            resumen = json.load(f)
        
        # Verificar campos críticos
        required_fields = [
            'presupuesto_total', 'transferencias_totales', 
            'eficiencia_ejecucion', 'avance_promedio',
            'fecha_analisis'
        ]
        
        for field in required_fields:
            if field in resumen and resumen[field] is not None:
                print(f"   ✅ {field}: {resumen[field]}")
            else:
                print(f"   ❌ {field}: FALTANTE O NULL")
                return False
        
        # Verificar datasets principales
        datasets = [
            ("presupuesto", "presupuesto_chile_2024.csv"),
            ("ejecucion", "ejecucion_presupuestaria_2024.csv"),
            ("transferencias", "transferencias_regionales_2024.csv")
        ]
        
        for name, filename in datasets:
            df = pd.read_csv(app_data_path / filename)
            if len(df) > 0:
                print(f"   ✅ {name}: {len(df):,} registros")
            else:
                print(f"   ❌ {name}: Dataset vacío")
                return False
                
    except Exception as e:
        print(f"   ❌ Error validando datos: {e}")
        return False
    
    # 4. Actualizar timestamp
    print("\n⏰ 4. ACTUALIZANDO TIMESTAMP...")
    
    try:
        # Actualizar metadatos con timestamp actual
        with open(app_data_path / "metadatos.json", 'r') as f:
            metadatos = json.load(f)
        
        metadatos['fecha_actualizacion'] = datetime.now().isoformat()
        metadatos['ultima_ejecucion_exitosa'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(app_data_path / "metadatos.json", 'w') as f:
            json.dump(metadatos, f, indent=2)
        
        print(f"   ✅ Timestamp actualizado: {metadatos['ultima_ejecucion_exitosa']}")
        
    except Exception as e:
        print(f"   ⚠️ Error actualizando timestamp: {e}")
        # No es crítico, continuar
    
    # 5. Resumen final
    print("\n🎉 ACTUALIZACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"📊 Presupuesto total: ${resumen['presupuesto_total']:,.0f}")
    print(f"📈 Eficiencia ejecución: {resumen['eficiencia_ejecucion']:.1f}%")
    print(f"📅 Última actualización: {resumen['fecha_analisis']}")
    print(f"🗂️  Archivos generados: {len(required_files)}")
    print(f"🔗 Aplicación disponible en: http://localhost:8501/04_presupuesto_publico")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
