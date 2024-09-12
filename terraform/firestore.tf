resource "google_project_service" "firestore" {
  service = "firestore.googleapis.com"
  disable_on_destroy = false
}


resource "google_firestore_database" "default" {
  name                    = var.database_name
  location_id             = var.gcp_region
  type                    = "FIRESTORE_NATIVE"
  deletion_policy         = "DELETE"
  delete_protection_state = "DELETE_PROTECTION_DISABLED"

  depends_on = [ google_project_service.firestore ]
}

resource "google_project_iam_member" "firestore" {
  project = var.gcp_project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.default.email}"
}
