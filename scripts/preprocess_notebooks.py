import os
import json
import time
import psutil
import nbformat
import pandas as pd
from pathlib import Path
from datetime import datetime
from PIL import Image
import io
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessing.log'),
        logging.StreamHandler()
    ]
)

class ResourceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.start_cpu_percent = psutil.cpu_percent()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
    def get_usage(self):
        end_time = time.time()
        end_cpu_percent = psutil.cpu_percent()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        return {
            'duration_seconds': end_time - self.start_time,
            'cpu_percent': end_cpu_percent,
            'memory_mb': end_memory - self.start_memory
        }

class NotebookPreprocessor:
    def __init__(self, notebooks_dir, output_dir):
        self.notebooks_dir = Path(notebooks_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.resource_usage = []
        
    def process_notebook(self, notebook_path):
        monitor = ResourceMonitor()
        notebook_name = notebook_path.stem
        logging.info(f"Procesando notebook: {notebook_name}")
        
        # Crear directorio para los resultados de este notebook
        output_notebook_dir = self.output_dir / notebook_name
        output_notebook_dir.mkdir(parents=True, exist_ok=True)
        
        try:            # Leer notebook con codificación UTF-8
            with open(notebook_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
            
            # Extraer y procesar resultados
            results = self._extract_results(nb)
            
            # Guardar resultados procesados
            self._save_results(results, output_notebook_dir)
            
            # Registrar uso de recursos
            usage = monitor.get_usage()
            usage['notebook'] = notebook_name
            self.resource_usage.append(usage)
            
            logging.info(f"Notebook {notebook_name} procesado exitosamente")
            
        except Exception as e:
            logging.error(f"Error procesando {notebook_name}: {str(e)}")
            raise
    
    def _extract_results(self, notebook):
        results = {
            'dataframes': {},
            'figures': {},
            'metadata': {
                'processed_at': datetime.now().isoformat()
            }
        }
        
        for cell in notebook.cells:
            if cell.cell_type == 'code' and hasattr(cell, 'outputs'):
                for output in cell.outputs:
                    # Procesar DataFrames
                    if 'data' in output and 'text/html' in output.data and 'DataFrame' in output.data['text/html']:
                        df_name = f"df_{len(results['dataframes'])}"
                        results['dataframes'][df_name] = output.data['text/html']
                    
                    # Procesar imágenes
                    if 'data' in output and any(k for k in output.data.keys() if k.startswith('image/')):
                        img_name = f"fig_{len(results['figures'])}"
                        for k in output.data.keys():
                            if k.startswith('image/'):
                                results['figures'][img_name] = {
                                    'data': output.data[k],
                                    'format': k.split('/')[-1]
                                }
        
        return results
    
    def _save_results(self, results, output_dir):
        # Guardar DataFrames como CSV/JSON optimizados
        for df_name, df_html in results['dataframes'].items():
            df_path = output_dir / f"{df_name}.csv.gz"
            # Aquí deberías convertir el HTML a DataFrame y guardarlo
            # pd.DataFrame(...).to_csv(df_path, compression='gzip')
        
        # Guardar figuras optimizadas
        for fig_name, fig_data in results['figures'].items():
            fig_path = output_dir / f"{fig_name}.webp"
            # Convertir y optimizar imagen
            # img = Image.open(io.BytesIO(fig_data['data']))
            # img.save(fig_path, 'WEBP', quality=85, optimize=True)
        
        # Guardar metadata
        meta_path = output_dir / 'metadata.json'
        with open(meta_path, 'w') as f:
            json.dump(results['metadata'], f)
    
    def save_resource_report(self):
        report_path = self.output_dir / 'resource_usage.json'
        with open(report_path, 'w') as f:
            json.dump({
                'resource_usage': self.resource_usage,
                'summary': {
                    'total_duration': sum(u['duration_seconds'] for u in self.resource_usage),
                    'avg_cpu_percent': sum(u['cpu_percent'] for u in self.resource_usage) / len(self.resource_usage),
                    'total_memory_mb': sum(u['memory_mb'] for u in self.resource_usage),
                }
            }, f, indent=2)

def main():
    notebooks_dir = Path('notebooks')
    output_dir = Path('app/data/preprocessed')
    
    processor = NotebookPreprocessor(notebooks_dir, output_dir)
    
    # Procesar cada notebook
    for notebook_path in notebooks_dir.glob('0[1-4]_*.ipynb'):
        processor.process_notebook(notebook_path)
    
    # Guardar reporte de uso de recursos
    processor.save_resource_report()
    
    logging.info("Preprocesamiento completado exitosamente")

if __name__ == '__main__':
    main()
