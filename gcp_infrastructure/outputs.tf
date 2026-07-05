output "gcs_bucket_name" {
  description = "Name of the GCS bucket for data chunks"
  value       = google_storage_bucket.data_chunks.name
}

output "postgres_instance_connection_name" {
  description = "The connection name of the Cloud SQL instance"
  value       = google_sql_database_instance.postgres_instance.connection_name
}

output "redis_host" {
  description = "The IP address of the Redis instance"
  value       = google_redis_instance.redis_cache.host
}

output "redis_port" {
  description = "The port of the Redis instance"
  value       = google_redis_instance.redis_cache.port
}

output "t4_worker_ip" {
  description = "The public IP address of the T4 GPU worker VM"
  value       = google_compute_instance.t4_worker.network_interface[0].access_config[0].nat_ip
}
