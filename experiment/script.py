import requests
from faker import Faker
import csv
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('URL')

output_file = "ids.csv"

fake = Faker()

token = os.getenv('TOKEN')

with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)

    for i in range(100):
        try:
            name = fake.name()
            descripcion = fake.sentence()

            data = {
                "name": name,
                "description": descripcion,
                "email": "juan.rodriguez@example.com",
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                document_id = response.json().get("id")
                print(f"Documento creado con ID: {document_id}")

                writer.writerow([document_id])
            else:
                print(f"Error en la creación: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error en la solicitud: {e}")

print(f"IDs guardados en {output_file}")
