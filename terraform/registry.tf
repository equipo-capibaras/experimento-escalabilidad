resource "google_project_service" "artifact_registry" {
  service = "artifactregistry.googleapis.com"

  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "default" {
  location      = var.gcp_region
  repository_id = var.registry_id
  format        = "DOCKER"

  depends_on = [ google_project_service.artifact_registry ]
}
