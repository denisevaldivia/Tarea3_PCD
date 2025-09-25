# **API DE USUARIOS - Tarea 3 PDC**
En este repositorio podremos encontrar una **API REST** con FastAPI que gestiona una base de datos de **usuarios**. La API cuenta con los 4 métodos principales para **crear, actualizar, obtener y eliminar** usuarios, todos estos métodos siendo validados por el método de **X-API-Key**.

## **Endpoints**
### `1. Crear usuario`
**POST** `/api/v1/users/`  
- **Descripción:** Crea un nuevo usuario en la base de datos.  
- **Body (JSON):**
```json
{
  "user_name": "Diana",
  "user_email": "diana@example.com",
  "age": 20,
  "ZIP": "12345",
  "recommendations": ["Hola"]
}
```
### `2. Obtener usuario por ID`
**GET** /api/v1/users/{user_id}
- **Descripción:** Recupera los datos de un usuario específico por su ID.

### `3. Actualizar usuario`
**PUT** /api/v1/users/{user_id}
- **Descripción:** Actualiza los datos de un usuario existente.
```json
{
  "user_name": "Pepe",
  "user_email": "diana@example.com",
  "age": 100,
  "ZIP": "12345",
  "recommendations": ["Hola"]
}
```
### 4. Eliminar usuario`
**DELETE** /api/v1/users/{user_id}
- **Descripción:** Elimina un usuario de la base de datos.

## **Ambiente y dependencias**
Este repo fue creado usando **UV** para el ambiente y las dependencias, para poder usar el código es necesario correr el siguiente código que instala las versiones de producción;
`uv pip install .`

## **Autenticación**
Todos los endpoints de la API están protegidos. Para poder acceder a ellos y a sus recursos es necesario crear un archivo `.env`.  
Puedes usar el archivo `.env.example` como guía para generar tu propio `.env`.  
La contraseña puede ser la que decidas.

## **Como correr la API**
Para poder correr la api, abrir la terminal y ejecutar la siguiente linea: `uv run fastapi main.py`.

