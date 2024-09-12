resource "google_project_service" "iam" {
  service = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_service_account" "default" {
  account_id   = var.service_account_name
  display_name = "Scalability experiment service account"
  depends_on   = [google_project_service.iam]
}