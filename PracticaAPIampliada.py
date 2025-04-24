import requests
import sqlite3
import time

# 1. Obtener todos los pokemones desde la API (nombre + url)
def obtener_todos_los_pokemones():
    url = "https://pokeapi.co/api/v2/pokemon?limit=100000"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        pokemones = datos["results"]
        return [(i + 1, p["name"].capitalize(), p["url"]) for i, p in enumerate(pokemones)]
    else:
        return []

# 2. Guardar en base de datos SQLite con URL
def guardar_en_base_datos(pokemones):
    conn = sqlite3.connect("pokemones.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS pokemones")
    cursor.execute("CREATE TABLE pokemones (id INTEGER PRIMARY KEY, nombre TEXT, url TEXT)")
    cursor.executemany("INSERT INTO pokemones (id, nombre, url) VALUES (?, ?, ?)", pokemones)
    conn.commit()
    conn.close()

# 3. Leer desde base de datos
def leer_desde_db():
    conn = sqlite3.connect("pokemones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pokemones")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# 4. Modificar datos en la base de datos
def modificar_pokemon():
    conn = sqlite3.connect("pokemones.db")
    cursor = conn.cursor()
    id_pokemon = input("Introduce el ID del Pokémon que quieres cambiar: ")
    nuevo_nombre = input("Introduce el nuevo nombre: ").capitalize()
    cursor.execute("UPDATE pokemones SET nombre = ? WHERE id = ?", (nuevo_nombre, id_pokemon))
    conn.commit()
    conn.close()
    print(" Pokémon actualizado con éxito.")

# 5. Comparar eficiencia
def comparar_eficiencia(pokemones_api):
    print("\n Comparando eficiencia: ")

    # Desde API (ya cargados en lista)
    start_api = time.time()
    for p in pokemones_api:
        nombre = p[1]
        url = p[2]
    end_api = time.time()
    print(f"Tiempo recorriendo desde API (en memoria): {end_api - start_api:.4f} segundos")

    # Desde DB
    start_db = time.time()
    pokemones_db = leer_desde_db()
    for p in pokemones_db:
        nombre = p[1]
        url = p[2]
    end_db = time.time()
    print(f"Tiempo recorriendo desde BD SQLite: {end_db - start_db:.4f} segundos\n")

    if start_api > start_db:
        print(f"BD SQlite fue más rápido por {start_api - start_db: .4f} segundos")
    else:
        print(f"API fue más rápido por {start_db - start_api: .4f} segundos")

# --- EJECUCIÓN PRINCIPAL ---
pokemones = obtener_todos_los_pokemones()

# Guardar en SQLite
guardar_en_base_datos(pokemones)

# Mostrar desde base de datos con índice
print("\n Pokémon desde la base de datos:")
for p in leer_desde_db()[:]:  # Puedes cambiar 10 por otro valor o quitar [:10] para todos
    print(f"{p[0]} - {p[1]} → {p[2]}")  # ID - Nombre → URL

# Modificar un Pokémon
modificar_pokemon()

# Mostrar de nuevo los primeros para ver el cambio
print("\n Pokémon después de la modificación:")
for p in leer_desde_db()[:]:
    print(f"{p[0]} - {p[1]} → {p[2]}")

# Comparar eficiencia
comparar_eficiencia(pokemones)