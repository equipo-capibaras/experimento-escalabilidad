resource "google_project_service" "cloudtrace" {
  service = "cloudtrace.googleapis.com"

  disable_on_destroy = false
}

resource "google_project_iam_member" "cloudtrace" {
  project = var.gcp_project_id
  role    = "roles/cloudtrace.agent"
  member  = "serviceAccount:${google_service_account.default.email}"

  depends_on = [ google_project_service.cloudtrace ]
}
