import requests
from faker import Faker
import csv


# Define la URL de tu endpoint de creación de documentos
url = "https://exp-scalability-gw-1vp12yav.uc.gateway.dev/v1/incidents"

# Archivo donde se guardarán los IDs
output_file = "ids.csv"

# Crea una instancia de Faker
fake = Faker()

# Abre el archivo en modo escritura y prepara para escribir en formato CSV
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    # Ejecuta 90 peticiones
    for i in range(90):
        try:
            # Genera una descripción aleatoria utilizando Faker
            descripcion = fake.sentence()  # Genera una oración aleatoria

            # Datos de ejemplo para la creación de un documento con descripción aleatoria
            data = {"mensaje": descripcion}

            # Realiza la petición POST
            response = requests.post(url, json=data)

            # Verifica que la petición fue exitosa
            if response.status_code == 201:
                # Extrae el ID del documento del JSON de respuesta
                document_id = response.json().get("id")
                print(f"Documento creado con ID: {document_id}")

                # Guarda el ID y la descripción en el archivo CSV
                writer.writerow([document_id])
            else:
                print(f"Error en la creación: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error en la solicitud: {e}")

print(f"IDs guardados en {output_file}")
