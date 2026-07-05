terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# ------------------------------------------------------------------------------
# 1. Cloud Storage (GCS) - "The Vault"
# ------------------------------------------------------------------------------

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "data_chunks" {
  name          = "darkmatter-chunks-${random_id.bucket_suffix.hex}"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  cors {
    origin          = ["*"]
    method          = ["GET", "HEAD", "OPTIONS"]
    response_header = ["*"]
    max_age_seconds = 3600
  }
}

# ------------------------------------------------------------------------------
# 2. Cloud SQL (PostgreSQL) - "The Ledger"
# ------------------------------------------------------------------------------

resource "google_sql_database_instance" "postgres_instance" {
  name             = "darkmatter-ledger-${random_id.bucket_suffix.hex}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro" # Small tier for PoC, scale up in production
    
    ip_configuration {
      ipv4_enabled = true
      # In production, use private IP and VPC peering
    }
  }
  
  deletion_protection = false # Set to true in production
}

resource "google_sql_database" "darkmatter_db" {
  name     = "darkmatter"
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_sql_user" "db_user" {
  name     = "dm_admin"
  instance = google_sql_database_instance.postgres_instance.name
  password = var.db_password
}

# ------------------------------------------------------------------------------
# 3. Memorystore (Redis) - Telemetry & Cache
# ------------------------------------------------------------------------------

resource "google_redis_instance" "redis_cache" {
  name           = "darkmatter-redis-${random_id.bucket_suffix.hex}"
  tier           = "BASIC" # Scale to STANDARD_HA for production
  memory_size_gb = 1
  region         = var.region

  redis_version = "REDIS_6_X"
}

# ------------------------------------------------------------------------------
# 4. Compute Engine (VM with NVIDIA T4 GPU) - Backend Worker
# ------------------------------------------------------------------------------

resource "google_compute_instance" "t4_worker" {
  name         = "darkmatter-t4-worker"
  machine_type = var.t4_machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      # Use a Deep Learning VM image which comes with NVIDIA drivers pre-installed
      image = "projects/deeplearning-platform-release/global/images/family/common-cu113-debian-11"
      size  = 100
      type  = "pd-ssd"
    }
  }

  guest_accelerator {
    type  = "nvidia-tesla-t4"
    count = 1
  }

  scheduling {
    on_host_maintenance = "TERMINATE" # Required for VMs with GPUs
    automatic_restart   = true
  }

  network_interface {
    network = "default"
    access_config {
      # Ephemeral public IP
    }
  }

  metadata = {
    install-nvidia-driver = "True"
  }

  tags = ["allow-ssh", "darkmatter-node"]
}
