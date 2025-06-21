import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Generar datos simulados para propiedades inmobiliarias en Chile
np.random.seed(42)

# Crear datos sintéticos
n_samples = 1000

# Características
comunas = ['Las Condes', 'Providencia', 'Ñuñoa', 'Santiago Centro', 'Vitacura', 
          'La Reina', 'Maipú', 'La Florida', 'Puente Alto', 'Conchalí', 
          'Huechuraba', 'Independencia', 'Recoleta', 'Macul', 'San Miguel']

tipos_propiedad = ['Casa', 'Departamento']

data = {
    'comuna': np.random.choice(comunas, n_samples),
    'tipo_propiedad': np.random.choice(tipos_propiedad, n_samples),
    'metros_totales': np.random.normal(120, 50, n_samples).clip(30, 300),
    'metros_construidos': np.random.normal(90, 40, n_samples).clip(25, 250),
    'dormitorios': np.random.randint(1, 6, n_samples),
    'banos': np.random.randint(1, 5, n_samples),
    'estacionamientos': np.random.randint(0, 4, n_samples),
    'antiguedad_anos': np.random.randint(0, 40, n_samples),
    'piso': np.random.randint(1, 25, n_samples),
    'orientacion': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Nororiente', 'Norponiente', 'Suroriente', 'Surponiente'], n_samples),
    'gastos_comunes': np.random.normal(120000, 50000, n_samples).clip(50000, 300000),
    'cercania_metro': np.random.choice([True, False], n_samples),
    'ascensor': np.random.choice([True, False], n_samples)
}

df = pd.DataFrame(data)

# Ajustar metros construidos para que sea siempre menor o igual a metros totales
df['metros_construidos'] = df.apply(lambda x: min(x['metros_construidos'], x['metros_totales']), axis=1)

# Poner piso en 1 para todas las casas
df.loc[df['tipo_propiedad'] == 'Casa', 'piso'] = 1

# Establecer ascensor a False para casas
df.loc[df['tipo_propiedad'] == 'Casa', 'ascensor'] = False

# Definir precios base por comuna (en millones de pesos chilenos)
precios_base = {
    'Las Condes': 5500,
    'Providencia': 5000,
    'Ñuñoa': 3500,
    'Santiago Centro': 3000,
    'Vitacura': 6000,
    'La Reina': 4500,
    'Maipú': 2000,
    'La Florida': 2200,
    'Puente Alto': 1800,
    'Conchalí': 1500,
    'Huechuraba': 2800,
    'Independencia': 2000,
    'Recoleta': 2200,
    'Macul': 2800,
    'San Miguel': 3000
}

# Generar precios según un modelo con ruido
def calcular_precio(row):
    precio_base = precios_base[row['comuna']]
    
    # Factor por tipo de propiedad
    factor_tipo = 1.1 if row['tipo_propiedad'] == 'Casa' else 1.0
    
    # Factor por tamaño
    factor_tamano = (row['metros_construidos'] / 100) * 1.2
    
    # Factor por dormitorios y baños
    factor_habitaciones = (row['dormitorios'] * 0.15) + (row['banos'] * 0.2)
    
    # Factor por estacionamientos
    factor_estacionamiento = 1 + (row['estacionamientos'] * 0.08)
    
    # Factor por antigüedad (disminuye con los años)
    factor_antiguedad = max(0.7, 1 - (row['antiguedad_anos'] * 0.01))
    
    # Factor por piso (para departamentos)
    factor_piso = 1 + (min(row['piso'], 15) * 0.01) if row['tipo_propiedad'] == 'Departamento' else 1
    
    # Factor por cercanía al metro
    factor_metro = 1.15 if row['cercania_metro'] else 1
    
    # Factor por ascensor
    factor_ascensor = 1.05 if row['ascensor'] else 1
    
    # Calcular precio en UF
    precio_uf = precio_base * factor_tipo * factor_tamano * factor_habitaciones * factor_estacionamiento * factor_antiguedad * factor_piso * factor_metro * factor_ascensor
    
    # Convertir UF a CLP (valor UF aproximado: 36,000 CLP)
    precio_clp = precio_uf * 36000
    
    # Añadir ruido aleatorio (±10%)
    ruido = np.random.uniform(0.9, 1.1)
    precio_final = precio_clp * ruido
    
    return round(precio_final, -3)  # Redondear a miles

# Calcular precios
df['precio'] = df.apply(calcular_precio, axis=1)

# Preparar datos para el modelo
X = pd.get_dummies(df.drop('precio', axis=1), drop_first=True)
y = df['precio']

# División entrenamiento/prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear modelos base
model1 = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

model2 = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', GradientBoostingRegressor(n_estimators=100, random_state=42))
])

model3 = Pipeline([
    ('scaler', StandardScaler()),
    ('regressor', LinearRegression())
])

# Entrenar modelos
model1.fit(X_train, y_train)
model2.fit(X_train, y_train)
model3.fit(X_train, y_train)

# Crear diccionario para almacenar el ensemble
ensemble_model = {
    'models': [model1, model2, model3],
    'weights': [0.5, 0.4, 0.1],  # Pesos para cada modelo
    'feature_names': list(X.columns),
    'comuna_mapping': {comuna: i for i, comuna in enumerate(comunas)},
    'tipo_propiedad_mapping': {tipo: i for i, tipo in enumerate(tipos_propiedad)},
    'orientacion_mapping': {orient: i for i, orient in enumerate(['Norte', 'Sur', 'Este', 'Oeste', 'Nororiente', 'Norponiente', 'Suroriente', 'Surponiente'])},
    'metadata': {
        'created_at': '2023-09-01',
        'version': '1.0.0',
        'metrics': {
            'r2_score': r2_score(y_test, model1.predict(X_test)),
            'mae': mean_absolute_error(y_test, model1.predict(X_test)),
            'rmse': np.sqrt(mean_squared_error(y_test, model1.predict(X_test)))
        }
    }
}

# Función para predecir con el ensemble
def predict(data, ensemble=ensemble_model):
    # Convertir a DataFrame si es un diccionario
    if isinstance(data, dict):
        data = pd.DataFrame([data])
    
    # Hacer one-hot encoding con las mismas columnas que el modelo
    X = pd.get_dummies(data, drop_first=True)
    
    # Asegurarse de que X tenga las mismas columnas que el modelo
    for col in ensemble['feature_names']:
        if col not in X.columns:
            X[col] = 0
    
    # Seleccionar y ordenar las columnas según el modelo
    X = X[ensemble['feature_names']]
    
    # Predecir con cada modelo y aplicar ponderación
    predictions = []
    for model, weight in zip(ensemble['models'], ensemble['weights']):
        pred = model.predict(X)
        predictions.append(pred * weight)
    
    # Combinar predicciones
    final_prediction = sum(predictions)
    
    return final_prediction

# Generar datos de tendencias para comunas
def generar_tendencias():
    tendencias = []
    for comuna in comunas:
        # Generar tendencia de precios para los últimos 12 meses
        for mes in range(1, 13):
            fecha = f"2023-{mes:02d}-01"
            # Simular tendencia con un patrón estacional y una tendencia general al alza
            factor_estacional = 1 + 0.03 * np.sin(mes * np.pi / 6)  # Patrón estacional
            factor_tendencia = 1 + 0.005 * mes  # Tendencia al alza
            
            # Precio base + ajuste estacional y de tendencia
            precio_base = precios_base[comuna] * 36000  # Convertir a CLP
            precio_promedio = precio_base * factor_estacional * factor_tendencia
            
            # Añadir variación por tipo de propiedad
            for tipo in tipos_propiedad:
                factor_tipo = 1.2 if tipo == 'Casa' else 1.0
                precio_tipo = precio_promedio * factor_tipo
                
                # Añadir ruido aleatorio
                precio_final = precio_tipo * np.random.uniform(0.95, 1.05)
                
                tendencias.append({
                    'fecha': fecha,
                    'comuna': comuna,
                    'tipo_propiedad': tipo,
                    'precio_promedio': round(precio_final, -3),
                    'variacion_mensual': round(np.random.uniform(-3.0, 5.0), 1),
                    'num_propiedades': int(np.random.uniform(10, 100))
                })
    
    return pd.DataFrame(tendencias)

# Generar y guardar tendencias
tendencias_df = generar_tendencias()
tendencias_df.to_csv('e:/repos/ds_portfolio/app/data/inmobiliario/tendencias.csv', index=False)

# Guardar el modelo ensemble
with open('e:/repos/ds_portfolio/app/data/modelos/modelo_ensemble.pkl', 'wb') as f:
    pickle.dump(ensemble_model, f)

# Guardar el dataset simulado
df.to_csv('e:/repos/ds_portfolio/app/data/inmobiliario/datos_propiedades.csv', index=False)

print("Modelo y datos guardados correctamente.")
