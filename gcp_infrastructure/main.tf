terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = "YOUR_GCP_PROJECT_ID"  # Remplacez par votre ID de projet GCP
  region  = "europe-west1"
  zone    = "europe-west1-b"
}

# --- VM T4 (Compute Node) ---
resource "google_compute_instance" "t4_node" {
  name         = "darkmatter-k3-t4-node"
  machine_type = "n1-standard-4"
  zone         = "europe-west1-b"

  boot_disk {
    initialize_params {
      image = "projects/deeplearning-platform/global/images/family/dlvm-cuda-118"  # Deep Learning VM avec CUDA 11.8
      size  = 100  # 100GB SSD
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Éphemère IP publique
    }
  }

  guest_accelerator {
    type  = "nvidia-tesla-t4"
    count = 1
  }

  metadata = {
    startup-script = file("startup.sh")  # Script de démarrage pour installer les dépendances
  }

  tags = ["darkmatter", "t4"]
}

# --- Cloud SQL (PostgreSQL) ---
resource "google_sql_database_instance" "postgres" {
  name             = "darkmatter-k3-db"
  database_version = "POSTGRES_15"
  region           = "europe-west1"

  settings {
    tier              = "f1-micro"  # Gratuit pour un usage léger
    disk_size         = 10          # 10GB SSD
    disk_type         = "PD_SSD"
    pricing_plan      = "PER_USE"
    activation_policy = "ALWAYS"

    ip_configuration {
      ipv4_enabled    = true
      authorized_networks {
        name  = "allow-public"
        value = "0.0.0.0/0"  # À restreindre en production !
      }
    }
  }
}

resource "google_sql_database" "darkmatter_db" {
  name     = "darkmatter"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "postgres_user" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres.name
  password = "YOUR_DB_PASSWORD"  # À remplacer par un mot de passe sécurisé
}

# --- Memorystore (Redis) ---
resource "google_redis_instance" "telemetry" {
  name           = "darkmatter-telemetry"
  tier           = "BASIC"
  memory_size_gb = 1
  region         = "europe-west1"
}

# --- Cloud Storage (GCS) ---
resource "google_storage_bucket" "data_bucket" {
  name          = "darkmatter-k3-data-${random_id.bucket_suffix.hex}"  # Nom unique
  location      = "EU"
  force_destroy = false

  versioning {
    enabled = true
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# --- Firewall Rules ---
resource "google_compute_firewall" "allow_http" {
  name    = "darkmatter-allow-http"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8501", "8080"]  # Streamlit, API, HTTP/HTTPS
  }

  source_ranges = ["0.0.0.0/0"]  # À restreindre en production
  target_tags   = ["darkmatter"]
}

# --- Outputs (Variables utiles pour les autres PR) ---
output "t4_node_ip" {
  value = google_compute_instance.t4_node.network_interface[0].access_config[0].nat_ip
}

output "postgres_public_ip" {
  value = google_sql_database_instance.postgres.public_ip_address
}

output "redis_host" {
  value = google_redis_instance.telemetry.host
}

output "gcs_bucket_name" {
  value = google_storage_bucket.data_bucket.name
}
