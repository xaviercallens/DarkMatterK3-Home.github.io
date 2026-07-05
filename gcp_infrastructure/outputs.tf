output "t4_node_external_ip" {
  description = "IP externe de la VM T4"
  value       = google_compute_instance.t4_node.network_interface[0].access_config[0].nat_ip
}

output "postgres_connection_string" {
  description = "Chaîne de connexion PostgreSQL"
  value       = "postgresql://postgres:${var.db_password}@${google_sql_database_instance.postgres.public_ip_address}/darkmatter"
  sensitive   = true
}

output "redis_connection_string" {
  description = "Chaîne de connexion Redis"
  value       = "redis://${google_redis_instance.telemetry.host}:6379"
}
