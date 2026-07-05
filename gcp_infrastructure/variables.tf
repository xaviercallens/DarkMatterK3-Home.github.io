variable "gcp_project_id" {
  description = "ID du projet GCP"
  type        = string
  default     = "YOUR_GCP_PROJECT_ID"  # À remplacer
}

variable "db_password" {
  description = "Mot de passe PostgreSQL"
  type        = string
  sensitive   = true
  default     = "YOUR_DB_PASSWORD"  # À remplacer
}
