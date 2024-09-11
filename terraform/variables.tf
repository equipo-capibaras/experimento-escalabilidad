variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region for deployment"
  type        = string
  default     = "us-central1"
}

variable "docker_image_url" {
  description = "URL of the Docker image to deploy in Cloud Run"
  type        = string
}

variable "firestore_collection_name" {
  description = "Firestore collection name to create if it doesn't exist"
  type        = string
  default     = "incidents"
}
