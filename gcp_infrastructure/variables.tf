variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy resources into"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The GCP zone for the Compute Engine VM"
  type        = string
  default     = "us-central1-a"
}

variable "db_password" {
  description = "Password for the Cloud SQL PostgreSQL instance"
  type        = string
  sensitive   = true
}

variable "t4_machine_type" {
  description = "Machine type for the T4 GPU VM"
  type        = string
  default     = "n1-standard-4"
}
