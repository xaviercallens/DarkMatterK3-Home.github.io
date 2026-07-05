#!/usr/bin/env python3
"""
🌌 DarkMatterK3@Home — Checkpoint & System Backup Manager
==============================================================================
Provides automated, timestamped backups of cosmological state files
(checkpoint_run.pt and pipeline_runs.json), list capabilities, and
safe restoration with auto-rollback security.
==============================================================================
"""

import os
import shutil
import json
import torch
from datetime import datetime

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
PIPELINE_FILE = os.path.join(BASE_DIR, "pipeline_runs.json")
CHECKPOINT_FILE = os.path.join(BASE_DIR, "checkpoint_run.pt")

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)

def get_file_metadata(file_path):
    """Returns basic file metadata if it exists, else None."""
    if not os.path.exists(file_path):
        return None
    stat = os.stat(file_path)
    return {
        "size_bytes": stat.st_size,
        "size_kb": round(stat.st_size / 1024, 2),
        "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
    }

def get_active_system_status():
    """Aggregates the status of current active simulation files."""
    pipeline_meta = get_file_metadata(PIPELINE_FILE)
    checkpoint_meta = get_file_metadata(CHECKPOINT_FILE)
    
    # Try to read some info from current pipeline json
    run_count = 0
    latest_asymmetry = "N/A"
    latest_run_time = "N/A"
    
    if pipeline_meta:
        try:
            with open(PIPELINE_FILE, "r") as f:
                data = json.load(f)
                run_count = len(data)
                if data:
                    latest_asymmetry = data[-1].get("mean_asymmetry", "N/A")
                    latest_run_time = data[-1].get("timestamp", "N/A")
        except Exception:
            pass
            
    # Try to read info from checkpoint file
    checkpoint_galaxies = 0
    if checkpoint_meta:
        try:
            cp = torch.load(CHECKPOINT_FILE, map_location='cpu', weights_only=False)
            checkpoint_galaxies = len(cp.get("ra", []))
        except Exception:
            pass

    return {
        "pipeline": {
            "exists": pipeline_meta is not None,
            "meta": pipeline_meta,
            "run_count": run_count,
            "latest_asymmetry": latest_asymmetry,
            "latest_run_time": latest_run_time
        },
        "checkpoint": {
            "exists": checkpoint_meta is not None,
            "meta": checkpoint_meta,
            "galaxy_count": checkpoint_galaxies
        }
    }

def create_backup(label="manual"):
    """
    Creates a timestamped backup copy of pipeline_runs.json and checkpoint_run.pt.
    Saves a metadata.json alongside them containing physics indicators.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}_{label}"
    target_dir = os.path.join(BACKUP_DIR, backup_name)
    os.makedirs(target_dir, exist_ok=True)
    
    status = get_active_system_status()
    
    # Copy files
    pipeline_copied = False
    checkpoint_copied = False
    
    if os.path.exists(PIPELINE_FILE):
        shutil.copy2(PIPELINE_FILE, os.path.join(target_dir, "pipeline_runs.json"))
        pipeline_copied = True
        
    if os.path.exists(CHECKPOINT_FILE):
        shutil.copy2(CHECKPOINT_FILE, os.path.join(target_dir, "checkpoint_run.pt"))
        checkpoint_copied = True
        
    if not pipeline_copied and not checkpoint_copied:
        # Clean up empty directory if nothing was copied
        os.rmdir(target_dir)
        return False, "Aucun fichier d'état actif trouvé à sauvegarder.", None
        
    # Write metadata descriptor
    metadata = {
        "backup_name": backup_name,
        "timestamp": datetime.now().isoformat(),
        "label": label,
        "run_count": status["pipeline"]["run_count"],
        "latest_asymmetry": status["pipeline"]["latest_asymmetry"],
        "galaxy_count": status["checkpoint"]["galaxy_count"],
        "files": {
            "pipeline_runs.json": get_file_metadata(os.path.join(target_dir, "pipeline_runs.json")),
            "checkpoint_run.pt": get_file_metadata(os.path.join(target_dir, "checkpoint_run.pt"))
        }
    }
    
    with open(os.path.join(target_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    return True, f"Sauvegarde réussie : {backup_name}", metadata

def list_backups():
    """Scans the backups directory and returns parsed metadata of all backups sorted chronologically."""
    backups = []
    if not os.path.exists(BACKUP_DIR):
        return []
        
    for entry in os.listdir(BACKUP_DIR):
        entry_path = os.path.join(BACKUP_DIR, entry)
        if os.path.isdir(entry_path):
            meta_path = os.path.join(entry_path, "metadata.json")
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, "r") as f:
                        meta = json.load(f)
                    backups.append(meta)
                except Exception:
                    # Fallback metadata if file corrupted
                    backups.append({
                        "backup_name": entry,
                        "timestamp": "Inconnu",
                        "label": "corrompu",
                        "run_count": 0,
                        "latest_asymmetry": "N/A",
                        "galaxy_count": 0
                    })
            else:
                # Undescribed folder (might be standard backup without meta)
                backups.append({
                    "backup_name": entry,
                    "timestamp": entry.split("_")[1] if len(entry.split("_")) > 1 else "Inconnu",
                    "label": entry.split("_")[-1] if len(entry.split("_")) > 2 else "inconnu",
                    "run_count": 0,
                    "latest_asymmetry": "N/A",
                    "galaxy_count": 0
                })
                
    # Sort by timestamp descending (newest first)
    backups.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return backups

def restore_backup(backup_name):
    """
    Restores pipeline_runs.json and checkpoint_run.pt from the specified backup folder.
    Creates a pre-restore backup first as an automatic rollback safety net.
    """
    source_dir = os.path.join(BACKUP_DIR, backup_name)
    if not os.path.exists(source_dir):
        return False, f"La sauvegarde spécifiée '{backup_name}' n'existe pas."
        
    # 1. Create a safety roll-back backup of the current state
    success, msg, safety_meta = create_backup(label="pre_restore_safety")
    if not success:
        print(f"[Avertissement] Échec de la création de la sauvegarde de sécurité : {msg}. Poursuite forcée...")

    # 2. Perform restoration
    pipeline_src = os.path.join(source_dir, "pipeline_runs.json")
    checkpoint_src = os.path.join(source_dir, "checkpoint_run.pt")
    
    restored_files = []
    
    try:
        if os.path.exists(pipeline_src):
            shutil.copy2(pipeline_src, PIPELINE_FILE)
            restored_files.append("pipeline_runs.json")
        else:
            # If backup has no pipeline runs, remove current to match backup state
            if os.path.exists(PIPELINE_FILE):
                os.remove(PIPELINE_FILE)
                
        if os.path.exists(checkpoint_src):
            shutil.copy2(checkpoint_src, CHECKPOINT_FILE)
            restored_files.append("checkpoint_run.pt")
        else:
            # If backup has no physics checkpoint, remove current to match
            if os.path.exists(CHECKPOINT_FILE):
                os.remove(CHECKPOINT_FILE)
                
        return True, f"Restauration réussie depuis '{backup_name}'. Fichiers restaurés: {', '.join(restored_files)}", safety_meta
    except Exception as e:
        # 3. Rollback from the safety backup if anything breaks during copying!
        if safety_meta:
            print(f"[RESTAURATION ÉCHOUÉE] Tentative de rollback de sécurité...")
            safety_dir = os.path.join(BACKUP_DIR, safety_meta["backup_name"])
            if os.path.exists(os.path.join(safety_dir, "pipeline_runs.json")):
                shutil.copy2(os.path.join(safety_dir, "pipeline_runs.json"), PIPELINE_FILE)
            if os.path.exists(os.path.join(safety_dir, "checkpoint_run.pt")):
                shutil.copy2(os.path.join(safety_dir, "checkpoint_run.pt"), CHECKPOINT_FILE)
            return False, f"La restauration a échoué: {e}. L'état initial du système a été restauré pour des raisons de sécurité."
        return False, f"La restauration a échoué: {e}. Aucun rollback possible car la sauvegarde de sécurité n'a pas pu être construite."

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("🌌 DarkMatterK3 - Gestionnaire de Sauvegardes")
        print("Usage: ./checkpoint_manager.py [backup | list | restore | status]")
        print("  backup [label]    Créer une sauvegarde (label optionnel)")
        print("  list              Lister toutes les sauvegardes")
        print("  restore [nom]     Restaurer une sauvegarde spécifique")
        print("  status            Afficher l'état du système actif")
        sys.exit(0)
        
    cmd = sys.argv[1]
    if cmd == "backup":
        label = sys.argv[2] if len(sys.argv) > 2 else "manual"
        success, msg, meta = create_backup(label)
        print(msg)
        if success:
            print(json.dumps(meta, indent=2))
            
    elif cmd == "list":
        backups = list_backups()
        print(f"Trouvé {len(backups)} sauvegardes :")
        for b in backups:
            print(f"- {b['backup_name']} | Label: {b['label']} | Galaxies: {b['galaxy_count']} | Runs: {b['run_count']} | Asymétrie: {b['latest_asymmetry']}")
            
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("Erreur: Spécifiez le nom du dossier de sauvegarde à restaurer.")
            sys.exit(1)
        backup_name = sys.argv[2]
        success, msg, safety = restore_backup(backup_name)
        print(msg)
        if success and safety:
            print(f"Une copie de sécurité de l'ancien état a été archivée sous : {safety['backup_name']}")
            
    elif cmd == "status":
        print(json.dumps(get_active_system_status(), indent=2))
        
    else:
        print(f"Commande inconnue: {cmd}")
