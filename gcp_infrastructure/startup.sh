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
