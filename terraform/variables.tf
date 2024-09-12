variable "gcp_region" {
  type        = string
  default     = "us-central1"
  description = "GCP region"
}

variable "gcp_project_id" {
  type        = string
  description = "GCP project ID"
}

variable "registry_id" {
  type        = string
  default     = "exp-scalability-repo"
  description = "Artifact registry ID"
}

variable "get_incidents_service_name" {
  type        = string
  default     = "get-incidents"
  description = "Microservice name"
}

variable "modify_incidents_service_name" {
  type        = string
  default     = "modify-incidents"
  description = "Microservice name"
}


variable "database_name" {
  type        = string
  default     = "incidentsdb"
  description = "Firestore database name"
}

variable "api_id" {
  type        = string
  default     = "exp-scalability"
  description = "API Gateway API ID"
}

variable "service_account_name" {
  type        = string
  default     = "exp-scalability-sa"
  description = "Service account name"
}
