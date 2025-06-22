"""
Script para crear un modelo con la estructura de nodos exacta requerida
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import struct

class CompatibleRandomForestRegressor(RandomForestRegressor):
    """Versión modificada de RandomForestRegressor con estructura de nodos compatible"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _make_compatible_structure(self, estimator):
        """Convierte la estructura del árbol al formato esperado"""
        tree = estimator.tree_
        
        n_nodes = tree.node_count
        children_left = tree.children_left
        children_right = tree.children_right
        feature = tree.feature
        threshold = tree.threshold
        impurity = tree.impurity
        n_node_samples = tree.n_node_samples
        weighted_n_node_samples = tree.weighted_n_node_samples
        
        # Crear array con la estructura exacta requerida
        dtype = np.dtype({
            'names': [
                'left_child', 'right_child', 'feature', 'threshold',
                'impurity', 'n_node_samples', 'weighted_n_node_samples',
                'missing_go_to_left'
            ],
            'formats': ['<i8', '<i8', '<i8', '<f8', '<f8', '<i8', '<f8', 'u1'],
            'offsets': [0, 8, 16, 24, 32, 40, 48, 56],
            'itemsize': 64
        })
        
        nodes = np.zeros(n_nodes, dtype=dtype)
        
        # Llenar el array con los valores
        nodes['left_child'] = children_left
        nodes['right_child'] = children_right
        nodes['feature'] = feature
        nodes['threshold'] = threshold
        nodes['impurity'] = impurity
        nodes['n_node_samples'] = n_node_samples
        nodes['weighted_n_node_samples'] = weighted_n_node_samples
        nodes['missing_go_to_left'] = np.ones(n_nodes, dtype=np.uint8)  # Default a True
        
        return nodes
    
    def fit(self, X, y, **kwargs):
        """Entrena el modelo y convierte la estructura de nodos"""
        super().fit(X, y, **kwargs)
        
        # Convertir la estructura de cada árbol
        for estimator in self.estimators_:
            tree = estimator.tree_
            compatible_nodes = self._make_compatible_structure(estimator)
            # Reemplazar la estructura de nodos
            tree.__setattr__('nodes', compatible_nodes)
        
        return self

def create_and_save_model():
    """Crea y guarda el modelo con la estructura compatible"""
    print("🔄 Creando conjunto de datos de entrenamiento...")
    
    # Generar datos de entrenamiento realistas
    np.random.seed(42)
    n_samples = 1000
    
    # Features con distribuciones realistas para el mercado inmobiliario chileno
    data = {
        'metros_totales': np.random.normal(120, 40, n_samples).clip(30, 300),
        'metros_construidos': np.random.normal(100, 35, n_samples).clip(25, 250),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.exponential(10, n_samples).clip(0, 40),
        'indice_ubicacion': np.random.normal(50, 15, n_samples).clip(20, 100)
    }
    
    X = pd.DataFrame(data)
    
    # Generar precios realistas en UF
    precio_base = data['indice_ubicacion'] * 2
    y = (
        precio_base * X['metros_construidos'] * 0.8 +
        X['dormitorios'] * 500 +
        X['banos'] * 300 +
        X['estacionamientos'] * 200 -
        X['antiguedad_anos'] * 15 +
        np.random.normal(0, 500, n_samples)
    ).clip(1000, 20000)
    
    print("✓ Datos de entrenamiento generados")
    
    # Preparar datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("🔄 Entrenando modelo compatible...")
    
    # Crear y entrenar modelo compatible
    model = CompatibleRandomForestRegressor(
        n_estimators=50,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_scaled, y)
    print("✓ Modelo entrenado exitosamente")
    
    # Guardar modelo y scaler
    save_paths = [
        Path('app/models'),
        Path('app/data/processed'),
        Path('app/data/inmobiliario')
    ]
    
    print("🔄 Guardando modelo y scaler...")
    
    for path in save_paths:
        path.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo
        model_path = path / 'modelo_inmobiliario.pkl'
        scaler_path = path / 'scaler_inmobiliario.pkl'
        
        joblib.dump(model, model_path, compress=3)
        joblib.dump(scaler, scaler_path, compress=3)
        
        print(f"✓ Modelo guardado en: {model_path}")
        print(f"✓ Scaler guardado en: {scaler_path}")
    
    # Verificar estructura
    print("\n🔍 Verificando estructura del modelo...")
    for estimator in model.estimators_:
        nodes = estimator.tree_.nodes
        dtype_names = nodes.dtype.names
        if 'missing_go_to_left' in dtype_names:
            print("✓ Estructura de nodos correcta verificada")
            print(f"✓ Campos presentes: {dtype_names}")
        else:
            print("❌ Error: Estructura de nodos incorrecta")
    
    return model, scaler

if __name__ == "__main__":
    print("\n🚀 Iniciando creación de modelo compatible...\n")
    model, scaler = create_and_save_model()
    print("\n✨ Proceso completado con éxito!")
