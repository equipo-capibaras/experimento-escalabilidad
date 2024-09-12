terraform {
  required_providers {
    google = {
      version = "~> 6.1.0"
    }

    google-beta = {
      version = "~> 6.1.0"
    }
  }
}

terraform {
  backend "gcs" {
    prefix = "exp-scalability/state"
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

provider "google-beta" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
