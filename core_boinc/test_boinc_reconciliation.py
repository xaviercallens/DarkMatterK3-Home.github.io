# core_boinc/test_boinc_reconciliation.py
import os
import json
import unittest
from unittest.mock import patch, MagicMock
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core_boinc.boinc_bridge_daemon import reconcile_offline_ledger, synchronize_receipt_to_db

class TestBOEINCReconciliation(unittest.TestCase):
    def setUp(self):
        self.ledger_path = os.path.join(BASE_DIR, "core_boinc", "boinc_offline_ledger.json")
        # Ensure clean slate
        if os.path.exists(self.ledger_path):
            os.remove(self.ledger_path)
            
    def tearDown(self):
        if os.path.exists(self.ledger_path):
            os.remove(self.ledger_path)
            
    @patch("core_boinc.boinc_bridge_daemon.get_db_connection")
    @patch("core_boinc.boinc_bridge_daemon.get_redis_client")
    def test_reconcile_offline_ledger(self, mock_get_redis, mock_get_db):
        # 1. Create a mock offline ledger with a pending receipt
        test_wu_id = "boinc_wu_reconcile_test_999"
        mock_ledger_data = {
            test_wu_id: {
                "user_id": "test_boinc_worker",
                "metrics": {
                    "Galaxies": 5000,
                    "AsymmetryRatio": 1.25,
                    "Delta": 0.25,
                    "Score": 0.8,
                    "KnotDistance": 15.5,
                    "AlignmentScore": 85.0,
                    "ComputationTimeMs": 42.5,
                    "Status": "success"
                },
                "points_earned": 57,
                "synced_at": "2026-07-07T14:00:00.000000"
            }
        }
        
        with open(self.ledger_path, "w") as f:
            json.dump(mock_ledger_data, f)
            
        # 2. Mock DB connection and cursor behavior
        mock_conn = MagicMock()
        mock_get_db.return_value = mock_conn
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # User exists check -> Return something so we update, or None to create
        mock_cursor.fetchone.side_effect = [
            None,  # User does not exist check (for users table)
            None   # Job does not exist check (for jobs table)
        ]
        
        # Mock Redis client
        mock_redis_client = MagicMock()
        mock_get_redis.return_value = mock_redis_client
        
        # 3. Trigger reconciliation
        reconcile_offline_ledger()
        
        # 4. Assertions
        # Check that the DB connection was requested
        mock_get_db.assert_called()
        
        # Check that SQL INSERT was executed to register the user
        insert_user_call = False
        insert_job_call = False
        
        for call in mock_cursor.execute.call_args_list:
            sql = call[0][0]
            if "INSERT INTO users" in sql:
                insert_user_call = True
            if "INSERT INTO jobs" in sql:
                insert_job_call = True
                
        self.assertTrue(insert_user_call, "Failed to insert user into PostgreSQL.")
        self.assertTrue(insert_job_call, "Failed to insert job into PostgreSQL.")
        
        # Check that Redis leaderboard was updated
        mock_redis_client.zincrby.assert_called_with("leaderboard", 57, "test_boinc_worker")
        
        # Verify that ledger is now empty or removed since all items are reconciled
        self.assertFalse(os.path.exists(self.ledger_path), "Offline ledger file was not cleared after synchronization.")
        
        print("\n✅ Reconciliation test passed successfully! Offline-online synchronization verified.")

if __name__ == "__main__":
    unittest.main()
