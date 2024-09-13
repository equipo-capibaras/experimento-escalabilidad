# Activar el servicio de Cloud Run
resource "google_project_service" "cloudrun" {
  service = "run.googleapis.com"
  disable_on_destroy = false
}

# Definir la política IAM para permitir la invocación
data "google_iam_policy" "default" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers"
    ]
  }
}

# Crear la instancia de Cloud Run para el microservicio "get_incidents"
resource "google_cloud_run_v2_service" "get_incidents" {
  name     = var.get_incidents_service_name
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
    service_account = google_service_account.default.email

    containers {
      name = "app"
      # Note: This is not the actual image of the service as container lifecycle is managed outside of terraform
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name  = "ENABLE_CLOUD_LOGGING"
        value = "1"
      }

      env {
        name  = "ENABLE_CLOUD_TRACE"
        value = "1"
      }

      startup_probe {
        http_get {
          path = "/ping"
        }
      }

      liveness_probe {
        http_get {
          path = "/ping"
        }
      }

      resources {
        cpu_idle = true
        startup_cpu_boost = true
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image
    ]
  }

  depends_on = [google_project_service.cloudrun]
}

# Crear la instancia de Cloud Run para el microservicio "modify_incidents"
resource "google_cloud_run_v2_service" "modify_incidents" {
  name     = var.modify_incidents_service_name
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
    service_account = google_service_account.default.email

    containers {
      name = "app"
      image = "us-docker.pkg.dev/cloudrun/container/hello"

      env {
        name  = "ENABLE_CLOUD_LOGGING"
        value = "1"
      }

      env {
        name  = "ENABLE_CLOUD_TRACE"
        value = "1"
      }

      startup_probe {
        http_get {
          path = "/ping"
        }
      }

      liveness_probe {
        http_get {
          path = "/ping"
        }
      }

      resources {
        cpu_idle = true
        startup_cpu_boost = true
      }
    }
  }

  lifecycle {
    ignore_changes = [
      client,
      client_version,
      template[0].containers[0].image
    ]
  }

  depends_on = [google_project_service.cloudrun]
}

# Políticas IAM para el servicio get_incidents
resource "google_cloud_run_v2_service_iam_policy" "get_incidents_policy" {
  project     = google_cloud_run_v2_service.get_incidents.project
  location    = google_cloud_run_v2_service.get_incidents.location
  name        = google_cloud_run_v2_service.get_incidents.name
  policy_data = data.google_iam_policy.default.policy_data
}

# Políticas IAM para el servicio modify_incidents
resource "google_cloud_run_v2_service_iam_policy" "modify_incidents_policy" {
  project     = google_cloud_run_v2_service.modify_incidents.project
  location    = google_cloud_run_v2_service.modify_incidents.location
  name        = google_cloud_run_v2_service.modify_incidents.name
  policy_data = data.google_iam_policy.default.policy_data
}
