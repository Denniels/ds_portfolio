# 🔄 Guía para Actualizar Streamlit Community Cloud

## ✅ Pasos para Forzar Actualización

### **1. Acceder al Dashboard de Streamlit Cloud**
1. Ve a: https://share.streamlit.io/
2. Inicia sesión con tu cuenta de GitHub
3. Busca tu aplicación "ds_portfolio"

### **2. Hacer Reboot Manual**
1. **Opción A: Desde el Dashboard**
   - Haz clic en los "..." (menú) de tu aplicación
   - Selecciona "Reboot"
   - Espera 2-3 minutos para el reinicio

2. **Opción B: Desde la App Desplegada**
   - Ve a tu app en el navegador
   - Haz clic en "Manage app" (esquina superior derecha)
   - Selecciona "Reboot app"

### **3. Verificar Variables de Entorno**
Asegúrate de que estas variables estén configuradas en Streamlit Cloud:

```
IS_STREAMLIT_CLOUD=true
ENVIRONMENT=production
```

### **4. Revisar Logs**
1. En el dashboard, haz clic en tu app
2. Ve a la pestaña "Logs"
3. Busca errores relacionados con:
   - Archivos CSS faltantes
   - Imports fallidos
   - Problemas de dependencias

### **5. Forzar Actualización de Caché**
Si el problema persiste:
1. Modifica ligeramente `requirements.txt`
2. Haz commit y push
3. Esto forzará una reconstrucción completa

## ⚠️ Problemas Comunes

### **CSS No Se Carga**
- Verifica que `style.min.css` existe
- Revisa rutas relativas en `main.py`
- Confirma que `IS_STREAMLIT_CLOUD=true`

### **Datos No Actualizados**
- Limpia caché de Streamlit con `st.cache_data.clear()`
- Verifica que archivos JSON estén en el repositorio
- Confirma que las rutas de datos sean correctas

### **Imports Fallidos**
- Revisa `requirements.txt` actualizado
- Confirma versiones de librerías compatibles
- Verifica que todos los módulos estén en el repo
