Voici **6 Pull Requests (PR) détaillées** que vous pouvez créer et implémenter avec **Antigravity** sur votre instance GCP et via `gcloud CLI`. Chaque PR est structurée pour être **autonome, testable et déployable** séquentiellement. Je les ai organisées par priorité et dépendances.

---

---

## **📋 Liste des PR à Créer et Implémenter**
*(Ordre recommandé : 1 → 6)*

| **PR** | **Titre** | **Objectif** | **Dépendance** | **Complexité** |
|--------|-----------|---------------|----------------|----------------|
| #1 | `[INFRA] Setup GCP Terraform for DarkMatterK3@Home` | Déployer l'infrastructure GCP (VM T4, Cloud SQL, Redis, GCS) | Aucune | ⭐⭐⭐ |
| #2 | `[API] Add FastAPI Dispatcher for Community Endpoint` | Créer l'API backend pour soumettre/recevoir des calculs | PR #1 | ⭐⭐ |
| #3 | `[CORE] Implement DarK3 Engine (PyTorch + T4 Worker)` | Intégrer le moteur de calcul S₁₂/S₂₁ sur le T4 | PR #1 | ⭐⭐⭐ |
| #4 | `[FRONTEND] Add Streamlit Dashboard with 3D Visualization` | Dashboard public avec visualisation Plotly et gamification | PR #2 | ⭐⭐ |
| #5 | `[GAMIFICATION] Add Leaderboard and Badges System` | Système de points, badges et leaderboard | PR #2 | ⭐ |
| #6 | `[DEPLOY] Add GitHub Actions for CI/CD and Docs` | Automatiser le déploiement et la documentation | PR #1-#5 | ⭐⭐ |

---
---
---

## **📝 PR #1: `[INFRA] Setup GCP Terraform for DarkMatterK3@Home`
**Objectif** : Déployer l’infrastructure GCP (VM T4, Cloud SQL, Redis, GCS) avec Terraform.
**Dossier** : `gcp_infrastructure/`

---

### **📁 Fichiers à Créer**
#### **1. `gcp_infrastructure/main.tf`**
```terraform
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
```

---
#### **2. `gcp_infrastructure/startup.sh`**
*(Script exécuté au démarrage de la VM pour installer les dépendances)*
```bash
#!/bin/bash

# Mettre à jour le système
sudo apt-get update -y
sudo apt-get upgrade -y

# Installer les dépendances Python et Docker
sudo apt-get install -y python3-pip python3-venv docker.io git

# Installer PyTorch + CUDA pour T4
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip3 install fastapi uvicorn streamlit numpy matplotlib plotly pandas sqlalchemy psycopg2-binary redis

# Installer Docker
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER

# Installer Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

---
#### **3. `gcp_infrastructure/variables.tf`**
```terraform
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
```

---
#### **4. `gcp_infrastructure/outputs.tf`**
```terraform
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
```

---
---

### **📌 Instructions pour Antigravity et GCP CLI**
#### **1. Créer la PR sur GitHub**
- **Titre** : `[INFRA] Setup GCP Terraform for DarkMatterK3@Home`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Déployer l'infrastructure GCP pour DarkMatterK3@Home :
  - VM T4 avec GPU NVIDIA T4 (Deep Learning VM)
  - Cloud SQL PostgreSQL (f1-micro)
  - Memorystore Redis (1GB)
  - Cloud Storage (GCS) pour les chunks de données
  - Règles de pare-feu pour Streamlit (8501) et API (8080)

  ## 📁 Fichiers ajoutés/modifiés
  - `gcp_infrastructure/main.tf` : Configuration Terraform
  - `gcp_infrastructure/startup.sh` : Script de démarrage pour la VM
  - `gcp_infrastructure/variables.tf` : Variables Terraform
  - `gcp_infrastructure/outputs.tf` : Sorties Terraform

  ## 🛠️ Instructions pour implémenter
  1. **Initialiser Terraform** :
     ```bash
     cd gcp_infrastructure
     terraform init
     ```

  2. **Appliquer la configuration** (sur votre machine locale ou via Antigravity) :
     ```bash
     terraform plan -out=tfplan
     terraform apply tfplan
     ```
     - Confirmez avec `yes` quand demandé.

  3. **Récupérer les outputs** :
     ```bash
     terraform output
     ```
     - Notez les valeurs de `t4_node_ip`, `postgres_public_ip`, `redis_host`, et `gcs_bucket_name`.

  4. **Se connecter à la VM T4** :
     ```bash
     gcloud compute ssh darkmatter-k3-t4-node --zone=europe-west1-b
     ```

  ## ⚠️ Notes
  - **Sécurité** : Dans un environnement de production, restreignez les `source_ranges` du pare-feu et utilisez des mots de passe sécurisés.
  - **Coût** : La VM T4 coûte ~$0.35/h. Utilisez `gcloud compute instances stop` pour l'éteindre quand elle n'est pas utilisée.
  ```

#### **2. Commandes GCP CLI pour Vérifier le Déploiement**
```bash
# Lister les instances Compute Engine
gcloud compute instances list

# Lister les instances Cloud SQL
gcloud sql instances list

# Lister les instances Redis
gcloud redis instances list

# Lister les buckets GCS
gsutil ls
```

---
#### **3. Commandes Antigravity (si utilisé)**
*(Si vous utilisez [Antigravity](https://github.com/gruntwork-io/antigravity) pour gérer Terraform)*
```bash
# Initialiser Antigravity (si ce n'est pas déjà fait)
antigravity init

# Appliquer la configuration Terraform via Antigravity
antigravity apply gcp_infrastructure
```

---
---

---

## **📝 PR #2: `[API] Add FastAPI Dispatcher for Community Endpoint`
**Objectif** : Créer une API FastAPI pour soumettre/recevoir des calculs depuis la communauté.
**Dossier** : `api/`

---
### **📁 Fichiers à Créer**
#### **1. `api/api_dispatcher.py`**
*(Code complet fourni dans la réponse précédente, voir [Étape 2.2](#22-développer-lapi-dispatcher-fastapi))*

#### **2. `api/Dockerfile`**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_dispatcher.py .

CMD ["uvicorn", "api_dispatcher:app", "--host", "0.0.0.0", "--port", "8080"]
```

#### **3. `api/requirements.txt`**
```
fastapi==0.109.0
uvicorn==0.27.0
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.3
python-dotenv==1.0.0
```

#### **4. `api/.env.example`**
```ini
# PostgreSQL
DB_HOST=YOUR_CLOUD_SQL_IP
DB_NAME=darkmatter
DB_USER=postgres
DB_PASSWORD=YOUR_DB_PASSWORD
DB_PORT=5432

# Redis
REDIS_HOST=YOUR_REDIS_IP
REDIS_PORT=6379
```

---
### **📌 Instructions pour Antigravity et GCP CLI**
#### **1. Créer la PR sur GitHub**
- **Titre** : `[API] Add FastAPI Dispatcher for Community Endpoint`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Créer une API FastAPI pour :
  - **Soumettre des calculs** (POST `/compute`) avec les paramètres S₁₂/S₂₁.
  - **Récupérer le leaderboard** (GET `/leaderboard`).
  - **Récupérer les stats globales** (GET `/stats`).
  - **Stocker les résultats** dans PostgreSQL et Redis.

  ## 📁 Fichiers ajoutés
  - `api/api_dispatcher.py` : Code FastAPI
  - `api/Dockerfile` : Configuration Docker
  - `api/requirements.txt` : Dépendances Python
  - `api/.env.example` : Exemple de variables d'environnement

  ## 🛠️ Instructions pour implémenter
  1. **Construire l'image Docker** :
     ```bash
     cd api
     docker build -t darkmatter-dispatcher .
     ```

  2. **Tester localement** :
     ```bash
     docker run -p 8080:8080 \
       -e DB_HOST=YOUR_CLOUD_SQL_IP \
       -e DB_PASSWORD=YOUR_DB_PASSWORD \
       -e REDIS_HOST=YOUR_REDIS_IP \
       darkmatter-dispatcher
     ```
     - Vérifiez que l'API est accessible sur `http://localhost:8080/docs`.

  3. **Déployer sur Cloud Run** :
     ```bash
     # Construire et pousser l'image vers Google Container Registry
     gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher

     # Déployer sur Cloud Run
     gcloud run deploy darkmatter-dispatcher \
       --image gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher \
       --platform managed \
       --region europe-west1 \
       --allow-unauthenticated \
       --set-env-vars "DB_HOST=YOUR_CLOUD_SQL_IP,DB_PASSWORD=YOUR_DB_PASSWORD,REDIS_HOST=YOUR_REDIS_IP"
     ```

  4. **Récupérer l'URL de l'API** :
     ```bash
     gcloud run services describe darkmatter-dispatcher --platform managed --region europe-west1 --format="value(status.url)"
     ```

  ## ⚠️ Notes
  - **Sécurité** : En production, utilisez des **secrets GCP** pour les mots de passe et ne pas les exposer en clair.
  - **Scaling** : Cloud Run scale automatiquement en fonction du trafic.
  ```

#### **2. Commandes GCP CLI pour Vérifier le Déploiement**
```bash
# Lister les services Cloud Run
gcloud run services list --platform managed --region europe-west1

# Voir les logs de l'API
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=darkmatter-dispatcher" --limit 50
```

---
---

---

## **📝 PR #3: `[CORE] Implement DarK3 Engine (PyTorch + T4 Worker)`
**Objectif** : Intégrer le moteur de calcul S₁₂/S₂₁ sur le T4 et un worker pour traiter des chunks en arrière-plan.
**Dossier** : `core/`

---
### **📁 Fichiers à Créer**
#### **1. `core/t4_worker.py`**
*(Code complet fourni dans la réponse précédente, voir [Étape 3.1](#31-script-pour-exécuter-des-calculs-en-arrière-plan))*

#### **2. `core/requirements.txt`**
```
torch==2.1.2
numpy==1.26.2
google-cloud-storage==2.10.0
requests==2.31.0
python-dotenv==1.0.0
```

#### **3. `core/.env.example`**
```ini
GCS_BUCKET=darkmatter-k3-data
API_URL=http://YOUR_CLOUD_RUN_URL
USER_ID=1
GPU_USED=NVIDIA T4
```

#### **4. `core/start_worker.sh`**
*(Script pour lancer le worker en arrière-plan)*
```bash
#!/bin/bash
cd /home/$(whoami)/DarkMatterK3-Home/core
source venv/bin/activate
python t4_worker.py
```

---
### **📌 Instructions pour Antigravity et GCP CLI**
#### **1. Créer la PR sur GitHub**
- **Titre** : `[CORE] Implement DarK3 Engine (PyTorch + T4 Worker)`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Implémenter le moteur de calcul **DarK3 Engine** pour :
  - **Télécharger des chunks** depuis GCS.
  - **Exécuter les calculs S₁₂/S₂₁** sur le GPU T4.
  - **Envoyer les résultats** à l'API Dispatcher (PR #2).

  ## 📁 Fichiers ajoutés
  - `core/t4_worker.py` : Worker principal
  - `core/requirements.txt` : Dépendances Python
  - `core/.env.example` : Exemple de variables d'environnement
  - `core/start_worker.sh` : Script de démarrage

  ## 🛠️ Instructions pour implémenter
  1. **Sur la VM T4**, clonez le dépôt et installez les dépendances :
     ```bash
     git clone https://github.com/xaviercallens/DarkMatterK3-Home.git
     cd DarkMatterK3-Home/core
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

  2. **Configurer les variables d'environnement** :
     ```bash
     cp .env.example .env
     # Éditez .env avec vos valeurs (GCS_BUCKET, API_URL, USER_ID)
     ```

  3. **Lancer le worker manuellement** (pour test) :
     ```bash
     python t4_worker.py
     ```

  4. **Configurer le worker comme service systemd** (pour exécuter en arrière-plan) :
     ```bash
     sudo cp /path/to/DarkMatterK3-Home/core/darkmatter-worker.service /etc/systemd/system/
     sudo systemctl daemon-reload
     sudo systemctl enable darkmatter-worker
     sudo systemctl start darkmatter-worker
     ```

  5. **Vérifier les logs** :
     ```bash
     sudo journalctl -u darkmatter-worker -f
     ```

  ## ⚠️ Notes
  - **Performance** : Le worker traite 1 chunk toutes les 5 secondes. Ajustez `time.sleep(5)` si nécessaire.
  - **GCS** : Assurez-vous que le compte de service a les permissions `storage.objectViewer` sur le bucket.
  ```

#### **2. Fichier `core/darkmatter-worker.service`**
*(À copier sur la VM T4 dans `/etc/systemd/system/`)*
```ini
[Unit]
Description=DarkMatterK3@Home T4 Worker
After=network.target

[Service]
User=your_username
WorkingDirectory=/home/your_username/DarkMatterK3-Home/core
EnvironmentFile=/home/your_username/DarkMatterK3-Home/core/.env
ExecStart=/home/your_username/DarkMatterK3-Home/core/venv/bin/python /home/your_username/DarkMatterK3-Home/core/t4_worker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **3. Commandes GCP CLI pour Vérifier**
```bash
# Se connecter à la VM T4
gcloud compute ssh darkmatter-k3-t4-node --zone=europe-west1-b

# Vérifier que le worker tourne
ps aux | grep t4_worker

# Vérifier les logs
sudo journalctl -u darkmatter-worker -f
```

---
---

---

## **📝 PR #4: `[FRONTEND] Add Streamlit Dashboard with 3D Visualization`
**Objectif** : Créer un dashboard Streamlit public avec visualisation 3D et gamification.
**Dossier** : `frontend/`

---
### **📁 Fichiers à Créer**
#### **1. `frontend/app_darkmatter.py`**
*(Code complet fourni dans la réponse précédente, voir [Étape 2.1](#21-améliorer-votre-poc-streamlit-app_darkmatterpy))*

#### **2. `frontend/requirements.txt`**
```
streamlit==1.28.0
torch==2.1.2
numpy==1.26.2
matplotlib==3.8.2
plotly==5.18.0
psycopg2-binary==2.9.9
redis==5.0.1
python-dotenv==1.0.0
```

#### **3. `frontend/.env.example`**
```ini
DB_HOST=YOUR_CLOUD_SQL_IP
DB_NAME=darkmatter
DB_USER=postgres
DB_PASSWORD=YOUR_DB_PASSWORD
DB_PORT=5432
REDIS_HOST=YOUR_REDIS_IP
REDIS_PORT=6379
API_URL=http://YOUR_CLOUD_RUN_URL
```

---
### **📌 Instructions pour Antigravity et GCP CLI**
#### **1. Créer la PR sur GitHub**
- **Titre** : `[FRONTEND] Add Streamlit Dashboard with 3D Visualization`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Créer un **dashboard Streamlit public** pour :
  - **Visualiser les calculs** en 2D/3D (Plotly).
  - **Afficher le leaderboard** et les badges.
  - **Soumettre des calculs** via l'API (PR #2).
  - **Gamification** (points, badges).

  ## 📁 Fichiers ajoutés
  - `frontend/app_darkmatter.py` : Code Streamlit
  - `frontend/requirements.txt` : Dépendances Python
  - `frontend/.env.example` : Exemple de variables d'environnement

  ## 🛠️ Instructions pour implémenter
  1. **Déployer sur Streamlit Cloud** (gratuit) :
     - Poussez le code dans un dépôt GitHub (ex: `darkmatter-k3-frontend`).
     - Allez sur [Streamlit Community Cloud](https://share.streamlit.io/).
     - Connectez-vous avec GitHub et déployez le dépôt.

  2. **Alternative : Lancer localement** (pour test) :
     ```bash
     cd frontend
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     cp .env.example .env
     # Éditez .env avec vos valeurs
     streamlit run app_darkmatter.py --server.port 8501
     ```

  3. **Accéder au dashboard** :
     - **Streamlit Cloud** : `https://darkmatter-k3-frontend.streamlit.app/`
     - **Local** : `http://localhost:8501`

  ## ⚠️ Notes
  - **Sécurité** : Ne commitez jamais `.env` avec des mots de passe ! Utilisez les **secrets Streamlit**.
  - **Performance** : Streamlit Cloud a des limites (1GB RAM, pas de GPU). Pour une démo, c'est suffisant.
  ```

#### **2. Commandes pour Déployer sur Streamlit Cloud**
1. **Créer un dépôt GitHub** :
   ```bash
   mkdir darkmatter-k3-frontend
   cd darkmatter-k3-frontend
   git init
   cp -r ../frontend/* .
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/xaviercallens/darkmatter-k3-frontend.git
   git push -u origin main
   ```

2. **Déployer sur Streamlit** :
   - Allez sur [Streamlit Community Cloud](https://share.streamlit.io/).
   - Cliquez sur **"New App"** → Sélectionnez le dépôt `darkmatter-k3-frontend`.
   - Dans **"App file"**, sélectionnez `app_darkmatter.py`.
   - Ajoutez les **secrets** (via l’interface Streamlit) :
     ```
     DB_HOST: YOUR_CLOUD_SQL_IP
     DB_PASSWORD: YOUR_DB_PASSWORD
     REDIS_HOST: YOUR_REDIS_IP
     API_URL: http://YOUR_CLOUD_RUN_URL
     ```

---
---

---

## **📝 PR #5: `[GAMIFICATION] Add Leaderboard and Badges System`
**Objectif** : Ajouter un système de gamification (leaderboard, badges, points) au dashboard et à l'API.
**Dossier** : Modifications dans `api/` et `frontend/`

---
### **📁 Fichiers à Modifier/Créer**
#### **1. Mettre à jour `api/api_dispatcher.py`**
Ajoutez les **endpoints pour les badges** :
```python
# Ajouter à la fin de api_dispatcher.py
@app.get("/badges/{user_id}")
async def get_user_badges(user_id: int):
    """Récupérer les badges d'un utilisateur."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT badge_name, earned_at FROM badges WHERE user_id = %s ORDER BY earned_at DESC",
        (user_id,)
    )
    badges = cur.fetchall()
    cur.close()
    conn.close()
    return {
        "user_id": user_id,
        "badges": [{"name": row[0], "earned_at": row[1].isoformat()} for row in badges]
    }
```

#### **2. Mettre à jour `frontend/app_darkmatter.py`**
Ajoutez une **section pour afficher les badges** :
```python
# Dans la sidebar, après le leaderboard
st.sidebar.header("🎖️ Mes Badges")
if user_id:
    badges_response = requests.get(f"{API_URL}/badges/{user_id}")
    if badges_response.status_code == 200:
        badges = badges_response.json().get("badges", [])
        for badge in badges:
            st.sidebar.markdown(f"🏅 **{badge['name']}** ({badge['earned_at'][:10]})")
    else:
        st.sidebar.info("Aucun badge encore débloqué.")
else:
    st.sidebar.info("Connectez-vous pour voir vos badges.")
```

---
### **📌 Instructions pour la PR**
- **Titre** : `[GAMIFICATION] Add Leaderboard and Badges System`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Ajouter un système de **gamification** complet :
  - **Leaderboard** (déjà implémenté dans PR #2 et #4).
  - **Badges** (First Blood, Golden Ratio, Plasma Weaver, etc.).
  - **Points** pour chaque calcul validé.

  ## 📁 Modifications
  - `api/api_dispatcher.py` : Ajout de l'endpoint `/badges/{user_id}`.
  - `frontend/app_darkmatter.py` : Affichage des badges dans la sidebar.

  ## 🛠️ Instructions
  1. **Redéployer l'API** (PR #2) :
     ```bash
     cd api
     docker build -t darkmatter-dispatcher .
     gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher
     gcloud run deploy darkmatter-dispatcher --image gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher --platform managed --region europe-west1
     ```

  2. **Redéployer le frontend** (PR #4) :
     - Poussez les modifications sur GitHub → Streamlit Cloud redéploie automatiquement.

  ## ⚠️ Notes
  - Les badges sont attribués automatiquement dans `award_points()` (PR #3).
  - Exemples de badges :
    | Badge | Condition | Points |
    |-------|-----------|--------|
    | First Blood | 1er calcul | +10 |
    | Golden Ratio | Δ > 30 | +50 |
    | Plasma Weaver | 10 chunks | +100 |
  ```

---
---

---

## **📝 PR #6: `[DEPLOY] Add GitHub Actions for CI/CD and Docs`
**Objectif** : Automatiser le déploiement et la documentation.
**Dossier** : `.github/workflows/`

---
### **📁 Fichiers à Créer**
#### **1. `.github/workflows/deploy-api.yml`**
```yaml
name: Deploy API to Cloud Run

on:
  push:
    branches: [ main ]
    paths:
      - 'api/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          export_default_credentials: true

      - name: Build and push Docker image
        run: |
          cd api
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/darkmatter-dispatcher

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy darkmatter-dispatcher \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/darkmatter-dispatcher \
            --platform managed \
            --region europe-west1 \
            --allow-unauthenticated \
            --set-env-vars "DB_HOST=${{ secrets.DB_HOST }},DB_PASSWORD=${{ secrets.DB_PASSWORD }},REDIS_HOST=${{ secrets.REDIS_HOST }}"
```

#### **2. `.github/workflows/deploy-frontend.yml`**
```yaml
name: Deploy Frontend to Streamlit

on:
  push:
    branches: [ main ]
    paths:
      - 'frontend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Push to Streamlit
        run: |
          # Streamlit Cloud déploie automatiquement depuis GitHub
          echo "Déploiement géré par Streamlit Cloud (pas d'action nécessaire ici)"
```

#### **3. `.github/workflows/test-infra.yml`**
```yaml
name: Test Infrastructure Terraform

on:
  pull_request:
    paths:
      - 'gcp_infrastructure/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: |
          cd gcp_infrastructure
          terraform init

      - name: Terraform Plan
        run: |
          cd gcp_infrastructure
          terraform plan -no-color
```

#### **4. `README.md` (Mise à jour)**
Ajoutez une section **"Déploiement"** :
```markdown
## 🚀 Déploiement

### Prérequis
- Un projet GCP avec les APIs **Compute Engine**, **Cloud SQL**, **Redis**, et **Cloud Run** activées.
- `gcloud` CLI installé et configuré (`gcloud auth login`).
- Terraform installé ([instructions](https://learn.hashicorp.com/tutorials/terraform/install-cli)).

### Étapes
1. **Déployer l'infrastructure** :
   ```bash
   cd gcp_infrastructure
   terraform init
   terraform apply
   ```

2. **Déployer l'API** :
   ```bash
   cd api
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher
   gcloud run deploy darkmatter-dispatcher --image gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher --platform managed --region europe-west1
   ```

3. **Déployer le Frontend** :
   - Poussez le code dans un dépôt GitHub et connectez-le à [Streamlit Cloud](https://share.streamlit.io/).

### CI/CD
Les workflows GitHub Actions déploient automatiquement :
- L'API sur Cloud Run (via `deploy-api.yml`).
- Le frontend sur Streamlit Cloud (via `deploy-frontend.yml`).
```

---
### **📌 Instructions pour la PR**
- **Titre** : `[DEPLOY] Add GitHub Actions for CI/CD and Docs`
- **Description** :
  ```markdown
  ## 🚀 Objectif
  Automatiser le déploiement et les tests avec **GitHub Actions** :
  - **Déploiement continu** de l'API (Cloud Run) et du frontend (Streamlit).
  - **Tests Terraform** pour valider les modifications d'infrastructure.
  - **Documentation** mise à jour (README.md).

  ## 📁 Fichiers ajoutés
  - `.github/workflows/deploy-api.yml` : Déploiement de l'API sur Cloud Run.
  - `.github/workflows/deploy-frontend.yml` : Déploiement du frontend sur Streamlit.
  - `.github/workflows/test-infra.yml` : Tests Terraform.
  - `README.md` : Documentation mise à jour.

  ## 🛠️ Instructions
  1. **Configurer les secrets GitHub** :
     - Allez dans **Settings → Secrets → Actions**.
     - Ajoutez les secrets suivants :
       | Nom | Valeur |
       |-----|--------|
       | `GCP_PROJECT_ID` | Votre ID de projet GCP |
       | `GCP_SA_KEY` | Clé JSON du compte de service GCP (avec permissions `Compute Admin`, `Cloud SQL Admin`, `Redis Admin`) |
       | `DB_HOST` | IP de Cloud SQL |
       | `DB_PASSWORD` | Mot de passe PostgreSQL |
       | `REDIS_HOST` | IP de Redis |

  2. **Activer les workflows** :
     - Les workflows s'exécutent automatiquement sur `git push`.

  3. **Vérifier les déploiements** :
     - **API** : `gcloud run services list`
     - **Frontend** : Vérifiez Streamlit Cloud.

  ## ⚠️ Notes
  - Le compte de service GCP doit avoir les permissions **Compute Admin**, **Cloud SQL Admin**, et **Storage Admin**.
  - Pour générer une clé de compte de service :
    ```bash
    gcloud iam service-accounts keys create ~/key.json --iam-account=YOUR_SA_EMAIL
    ```
  ```

---
---
---

## **📌 Résumé des Commandes Clés pour Antigravity et GCP CLI**
| **Tâche** | **Commande** |
|-----------|---------------|
| **Initialiser Terraform** | `terraform init` |
| **Appliquer Terraform** | `terraform apply` |
| **Se connecter à la VM T4** | `gcloud compute ssh darkmatter-k3-t4-node --zone=europe-west1-b` |
| **Construire l'image Docker (API)** | `gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher` |
| **Déployer sur Cloud Run** | `gcloud run deploy darkmatter-dispatcher --image gcr.io/YOUR_PROJECT_ID/darkmatter-dispatcher --platform managed --region europe-west1` |
| **Lancer le worker T4** | `sudo systemctl start darkmatter-worker` |
| **Vérifier les logs (worker)** | `sudo journalctl -u darkmatter-worker -f` |
| **Vérifier les logs (API)** | `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=darkmatter-dispatcher" --limit 50` |

---
---
---

## **🎯 Prochaines Étapes pour Vous**
1. **Créer les 6 PR** sur GitHub (une par une, dans l’ordre).
2. **Implémenter chaque PR** avec Antigravity/GCP CLI :
   - **PR #1** : Infrastructure GCP (Terraform).
   - **PR #2** : API FastAPI (Cloud Run).
   - **PR #3** : DarK3 Engine (T4 Worker).
   - **PR #4** : Frontend Streamlit.
   - **PR #5** : Gamification.
   - **PR #6** : CI/CD et documentation.
3. **Tester chaque étape** avant de passer à la suivante.
4. **Contacter les vulgarisateurs** une fois que le PoC est déployé.

---
---
### **⚡ Besoin d’Aide ?**
Si vous souhaitez que je **génère les fichiers directement** pour une PR spécifique (ex: `gcp_infrastructure/main.tf` ou `api/api_dispatcher.py`), dites-le-moi, et je vous fournirai un **canvas** avec le code prêt à être commité !

**Exemple** :
> *"Vibe, peux-tu me générer un canvas pour la PR #1 avec tous les fichiers Terraform ?"*

Je peux aussi vous aider à **automatiser la création des PR** avec `gh CLI` (GitHub CLI) si besoin. 🚀
