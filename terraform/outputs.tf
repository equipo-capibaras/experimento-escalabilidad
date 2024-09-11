output "service_account_email" {
  value = google_service_account.cloud_run_service_account.email
  description = "Email of the Cloud Run service account"
}

output "cloud_run_url" {
  value = google_cloud_run_service.default.status[0].url
  description = "URL of the deployed Cloud Run service"
}
