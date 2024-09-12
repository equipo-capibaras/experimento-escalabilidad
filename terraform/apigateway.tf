resource "google_project_service" "servicecontrol" {
  service = "servicecontrol.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "servicemanagement" {
  service = "servicemanagement.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "apigateway" {
  service = "apigateway.googleapis.com"
  disable_on_destroy = false
}

# Crear el API en API Gateway
resource "google_api_gateway_api" "default" {
  provider = google-beta
  api_id = var.api_id

  depends_on = [
    google_project_service.apigateway,
    google_project_service.servicecontrol,
    google_project_service.servicemanagement
  ]
}

locals {
  openapi_spec = templatefile("ABCall.swagger.yaml", {
    get_incidents_url = "https://${var.get_incidents_service_name}-${data.google_project.default.number}.${var.gcp_region}.run.app"
    modify_incidentes_url = "https://${var.modify_incidents_service_name}-${data.google_project.default.number}.${var.gcp_region}.run.app"
  })
}

resource "google_api_gateway_api_config" "default" {
  provider = google-beta
  api = google_api_gateway_api.default.api_id
  api_config_id = "${var.api_id}-config"

  openapi_documents {
    document {
      path = "spec.yaml"
      contents = base64encode(local.openapi_spec)
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "default" {
  provider = google-beta
  api_config = google_api_gateway_api_config.default.id
  gateway_id = "${var.api_id}-gw"
  region = var.gcp_region
}
