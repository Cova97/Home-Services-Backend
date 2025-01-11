### README.md

```markdown
# Home-Services-Backend

Este es el backend para el proyecto Home Services, diseñado para gestionar servicios a domicilio. A continuación, encontrarás las instrucciones para instalar y configurar este proyecto en tu equipo.

---

## **Requisitos previos**

Asegúrate de tener instalado lo siguiente:

1. **Python 3.8 o superior**: [Descargar aquí](https://www.python.org/downloads/)
2. **Git**: [Descargar aquí](https://git-scm.com/downloads)
3. **Entorno virtual de Python** (opcional, pero recomendado).

---

## **Instrucciones de instalación**

Sigue estos pasos para instalar y configurar el proyecto en tu equipo.

### **1. Clonar el repositorio**
Usa Git para clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/Home-Services-Backend.git
cd Home-Services-Backend
```

### **2. Crear y activar un entorno virtual**
Esto asegura que las dependencias del proyecto no entren en conflicto con otros proyectos.

#### En Linux/macOS:
```bash
python3 -m venv env
source env/bin/activate
```

#### En Windows:
```bash
python -m venv env
env\Scripts\activate
```

---

### **3. Instalar dependencias**
Instala las bibliotecas necesarias desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **6. Ejecutar el servidor de desarrollo**
Inicia el servidor para probar el proyecto.

#### En Linux/macOS:
```bash
fastapi dev main.py
```

#### En Windows:
```bash
fastapi dev main.py
```

Accede al proyecto en tu navegador: [http://127.0.0.1:8000](http://127.0.0.1:8000)


## **Comandos útiles**
- **Para desactivar el entorno virtual**:
  - Linux/macOS:
    ```bash
    deactivate
    ```
  - Windows:
    ```bash
    deactivate
    ```

---

## **Contribuciones**
Si deseas contribuir al proyecto, crea una rama nueva y realiza un pull request. Asegúrate de seguir las normas de codificación del proyecto.

---

## **Licencia**
Este proyecto está bajo la licencia [MIT](LICENSE).
```