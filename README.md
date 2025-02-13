# reto_IM


# FastAPI con Docker, Swagger y Autenticación JWT

Esta aplicación es un ejemplo de API creada con FastAPI que utiliza autenticación con JWT. Incluye endpoints para obtener productos y un Dockerfile para empaquetarla en un contenedor.

## Estructura del Proyecto

La estructura del proyecto es similar a la siguiente:

- **Dockerfile:** Instrucciones para construir la imagen Docker.
- **requirements.txt:** Lista de dependencias del proyecto.
- **main.py:** Archivo principal con la configuración y los endpoints de la API.
- **products.py:** Módulo que contiene la lógica para obtener los productos.

## Construcción y Ejecución con Docker

### 1. Construir la imagen Docker

Desde el directorio raíz del proyecto (donde se encuentra el `Dockerfile`), ejecuta:

```bash
docker build -t fastapi_app .
```

```bash
docker run -p 8000:8000 fastapi_app
```

La aplicación estará disponible en: [http://localhost:8000](http://localhost:8000)

## Acceso a la Documentación Swagger

FastAPI genera automáticamente una interfaz de documentación Swagger. Para acceder a ella:

Abre tu navegador y visita: [http://localhost:8000/docs](http://localhost:8000/docs)

Desde esta interfaz podrás explorar y probar los endpoints de la API.

## Uso de la API con Postman

### 1. Obtener el Token Bearer

Realiza una petición POST al endpoint de autenticación:

- **URL:** `http://localhost:8000/auth/`
- **Método:** POST
- **Body:** Selecciona la opción `x-www-form-urlencoded` y agrega los siguientes campos:
    - `username`: admin
    - `password`: imagemaker

La respuesta será un JSON con el token de acceso, similar a:

```json
{
    "access_token": "tu_token_jwt_aqui",
    "token_type": "bearer"
}
```

### 2. Usar el Token en Otros Endpoints

Copia el valor del `access_token` obtenido.

En Postman, para cada petición a endpoints protegidos (por ejemplo, `/products` o `/products/products_id`):

- Ve a la pestaña `Authorization`.
- Selecciona el tipo `Bearer Token`.
- Pega el token en el campo correspondiente.

### Ejemplos de Peticiones

#### Obtener Productos:

Realiza una petición GET a:

```bash
http://localhost:8000/products
```

Puedes usar parámetros de consulta (`min_price` y `max_price`) según sea necesario.

#### Obtener Producto por ID:

Realiza una petición GET a:

```bash
http://localhost:8000/products/products_id?product_id=1
```

(Reemplaza `1` por el ID del producto que deseas consultar.)

## Pruebas Unitarias

Las pruebas unitarias están implementadas en el archivo `test_main.py` utilizando `pytest` y el `TestClient` de FastAPI. No es necesario tener la API ejecutándose en un servidor para correr las pruebas, ya que `TestClient` simula un servidor en memoria y ejecuta la aplicación internamente.

### Ejecutar las Pruebas

Asegúrate de tener instaladas las dependencias de desarrollo, incluyendo `pytest` (puedes agregarlas a tu `requirements.txt` o instalarlo de forma global):

```bash
pip install pytest
```

Ejecuta las pruebas desde la raíz del proyecto:

```bash
pytest
```
```