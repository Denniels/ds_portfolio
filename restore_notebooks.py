# Script para restaurar los notebooks desde el respaldo
import shutil
from pathlib import Path
import json
import os

def main():
    # Definir rutas
    base_dir = Path(".")
    backup_dir = base_dir / "temp_backup"
    notebooks_dir = base_dir / "notebooks"
    
    # Asegurar que existe el directorio de notebooks
    notebooks_dir.mkdir(exist_ok=True)
    
    # Lista de notebooks a restaurar
    notebooks = [
        "01_Analisis_Emisiones_CO2_Chile.ipynb",
        "02_Analisis_Calidad_Del_Agua.ipynb",
        "03_Analisis_BigQuery_Demografia.ipynb",
        "04_Analisis_Presupuesto_Publico.ipynb"
    ]
    
    # Restaurar cada notebook
    for notebook in notebooks:
        src_path = backup_dir / "notebooks" / notebook
        dst_path = notebooks_dir / notebook
        
        if src_path.exists():
            print(f"Restaurando notebook: {notebook}")
            shutil.copy2(str(src_path), str(dst_path))
        else:
            print(f"No se encontró el archivo de respaldo para {notebook}")
    
    # Restaurar archivos JSON necesarios para el pipeline
    app_data_dir = base_dir / "app" / "data"
    backup_app_data_dir = backup_dir / "app" / "data"
    
    # Crear directorios necesarios
    for subdir in ["cache", "feedback", "processed", "raw"]:
        (app_data_dir / subdir).mkdir(exist_ok=True, parents=True)
    
    # Restaurar archivo de comentarios si existe
    feedback_file = backup_app_data_dir / "feedback" / "comments.json"
    if feedback_file.exists():
        print("Restaurando archivo de comentarios")
        target_dir = app_data_dir / "feedback"
        target_dir.mkdir(exist_ok=True)
        shutil.copy2(str(feedback_file), str(target_dir / "comments.json"))
    else:
        # Crear un archivo vacío de comentarios si no existe
        comments_file = app_data_dir / "feedback" / "comments.json"
        if not comments_file.exists():
            print("Creando archivo de comentarios vacío")
            with open(str(comments_file), 'w') as f:
                json.dump([], f)
    
    # Restaurar archivo de servicios si existe
    servicios_file = backup_dir / "data" / "servicios.json"
    if servicios_file.exists():
        print("Restaurando archivo de servicios")
        target_dir = base_dir / "data"
        target_dir.mkdir(exist_ok=True)
        shutil.copy2(str(servicios_file), str(target_dir / "servicios.json"))
    
    print("Restauración completada!")

if __name__ == "__main__":
    main()
