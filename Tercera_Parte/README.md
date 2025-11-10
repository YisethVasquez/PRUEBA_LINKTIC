Este proyecto implementa un flujo de prueba End-to-End (E2E) para el sitio OpenCart (abstracta.us) utilizando **Selenium** con **Python** bajo el patrón de diseño **Page Object Model (POM)**.

## Requisitos Previos

* **Python 3.x** instalado.
* 
## Configuración del Entorno

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/YisethVasquez/PRUEBA_LINKTIC.git](https://github.com/YisethVasquez/PRUEBA_LINKTIC.git)
    cd selenium-pom-opencart
    ```

2.  **Crear y activar un entorno virtual (Recomendado):**
    ```bash
    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuración del Navegador:**
    * El proyecto utiliza **Chrome** por defecto.

## Configuración de Pruebas

Los datos de prueba (como `BASE_URL`, `FIRST_NAME`, `PASSWORD`) se encuentran en el archivo:
* `config/config.ini`

## Ejecución de la Prueba

El proyecto utiliza **Pytest** para la ejecución.

Para ejecutar el flujo de prueba completo (`test_e2e_flow.py`):

```bash
# Asegúrate de estar en el directorio raíz del proyecto (selenium-pom-opencart)
pytest tests/test_e2e_flow.py
