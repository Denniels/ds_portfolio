"""
Script para regenerar el modelo inmobiliario con scikit-learn 1.7.0
Compatible con las últimas versiones de numpy y scikit-learn
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib
import json
import os

def generate_training_data():
    """Genera datos de entrenamiento realistas"""
    np.random.seed(42)
    n_samples = 2000
    
    # Características con distribuciones realistas
    comunas = ['Las Condes', 'Providencia', 'Ñuñoa', 'Santiago Centro', 
              'Vitacura', 'La Reina', 'Maipú', 'La Florida']
    
    data = {
        'comuna': np.random.choice(comunas, n_samples),
        'tipo_propiedad': np.random.choice(['Casa', 'Departamento'], n_samples),
        'metros_totales': np.random.normal(120, 40, n_samples).clip(30, 300),
        'metros_construidos': np.random.normal(100, 35, n_samples).clip(25, 250),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.exponential(10, n_samples).clip(0, 40),
        'piso': np.random.randint(1, 25, n_samples),
        'cercania_metro': np.random.choice([True, False], n_samples),
        'orientacion': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste'], n_samples)
    }
    
    # Asegurar que metros_construidos <= metros_totales
    data['metros_construidos'] = np.minimum(data['metros_construidos'], data['metros_totales'])
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Generar precios realistas en UF
    precios_base = {
        'Las Condes': 65,
        'Vitacura': 75,
        'Providencia': 55,
        'Ñuñoa': 45,
        'Santiago Centro': 40,
        'La Reina': 50,
        'Maipú': 35,
        'La Florida': 30
    }
    
    # Calcular precios
    precios = []
    for _, row in df.iterrows():
        precio_base = precios_base.get(row['comuna'], 40)
        precio = precio_base * row['metros_construidos']
        
        # Factores de ajuste
        if row['tipo_propiedad'] == 'Casa':
            precio *= 1.15  # +15% por ser casa
        
        precio *= (1 + 0.08 * row['dormitorios'])  # +8% por dormitorio
        precio *= (1 + 0.1 * row['banos'])         # +10% por baño
        precio *= (1 + 0.05 * row['estacionamientos'])  # +5% por estacionamiento
        
        # Depreciación por antigüedad
        precio *= (1 - min(0.5, row['antiguedad_anos'] * 0.01))  # máx 50% deprec
        
        # Ajustes adicionales
        if row['cercania_metro']:
            precio *= 1.1  # +10% por cercanía al metro
        
        if row['tipo_propiedad'] == 'Departamento':
            precio *= (1 + min(row['piso'] * 0.01, 0.15))  # hasta +15% por altura
        
        # Añadir variación aleatoria (±10%)
        precio *= np.random.uniform(0.9, 1.1)
        
        precios.append(precio)
    
    df['precio_uf'] = precios
    return df

def train_model(df):
    """Entrena el modelo con características seleccionadas"""
    # Seleccionar features para el modelo
    feature_cols = ['metros_totales', 'metros_construidos', 'dormitorios', 'banos',
                   'estacionamientos', 'antiguedad_anos', 'cercania_metro']
    
    # One-hot encoding para variables categóricas
    df_encoded = pd.get_dummies(df, columns=['comuna', 'tipo_propiedad', 'orientacion'])
    
    # Preparar X e y
    X = df_encoded.drop('precio_uf', axis=1)
    y = df_encoded['precio_uf']
    
    # Split train-test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Escalar features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelo
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluar modelo
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"\nMétricas del modelo:")
    print(f"R² Score: {r2:.4f}")
    print(f"MAE: {mae:.2f} UF")
    
    return model, scaler, X.columns.tolist()

def save_model_files(model, scaler, feature_names, version_info):
    """Guarda el modelo y archivos relacionados en todas las ubicaciones necesarias"""
    # Definir directorios donde guardar el modelo
    paths = [
        Path('app/models'),
        Path('app/data/processed'),
        Path('app/data/inmobiliario')
    ]
    
    # Información del modelo
    model_info = {
        'feature_names': feature_names,
        'n_features': len(feature_names),
        'version': version_info,
        'created_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo y scaler
        joblib.dump(model, path / 'modelo_inmobiliario.pkl', compress=3)
        joblib.dump(scaler, path / 'scaler_inmobiliario.pkl', compress=3)
        
        # Guardar información del modelo
        with open(path / 'model_info.json', 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2, ensure_ascii=False)
        
        print(f"\nArchivos guardados en {path}:")
        print(f"✓ modelo_inmobiliario.pkl")
        print(f"✓ scaler_inmobiliario.pkl")
        print(f"✓ model_info.json")

def main():
    """Función principal para regenerar el modelo"""
    print("\n🚀 Iniciando regeneración del modelo inmobiliario...")
    
    # Obtener versiones de las dependencias
    import sklearn
    version_info = {
        'scikit-learn': sklearn.__version__,
        'numpy': np.__version__,
        'pandas': pd.__version__,
        'joblib': joblib.__version__
    }
    
    print("\nVersiones de dependencias:")
    for pkg, ver in version_info.items():
        print(f"✓ {pkg}: {ver}")
    
    # Generar y preparar datos
    print("\n📊 Generando datos de entrenamiento...")
    df = generate_training_data()
    print(f"✓ Dataset generado: {len(df):,} registros")
    
    # Entrenar modelo
    print("\n🔄 Entrenando modelo...")
    model, scaler, feature_names = train_model(df)
    
    # Guardar archivos
    print("\n💾 Guardando archivos...")
    save_model_files(model, scaler, feature_names, version_info)
    
    print("\n✨ Proceso completado con éxito!")

if __name__ == "__main__":
    main()
