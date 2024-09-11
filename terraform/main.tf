provider "google" {
  project = var.project_id
  region  = var.region
}

# Crear la cuenta de servicio para Cloud Run con acceso a Firestore y Secret Manager
resource "google_service_account" "cloud_run_service_account" {
  account_id   = "exp-escalabilidad-sa"
  display_name = "Cloud Run Service Account"
}

# Asignar roles a la cuenta de servicio
resource "google_project_iam_member" "firestore_role" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

resource "google_project_iam_member" "secretmanager_role" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}

# Crear el servicio de Cloud Run
resource "google_cloud_run_service" "default" {
  name     = "exp-escalabilidad-cr"
  location = var.region

  template {
    spec {
      containers {
        image = var.docker_image_url

        env {
          name  = "GOOGLE_CLOUD_PROJECT"
          value = var.project_id
        }
      }
      service_account_name = google_service_account.cloud_run_service_account.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Configurar Firestore
resource "google_firestore_index" "incident_collection_index" {
  collection = var.firestore_collection_name
  fields {
    field_path = "__name__"
    order      = "ASCENDING"
  }
}

# Outputs importantes
output "cloud_run_url" {
  value = google_cloud_run_service.default.status[0].url
}
