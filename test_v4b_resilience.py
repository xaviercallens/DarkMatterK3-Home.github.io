#!/usr/bin/env python3
"""
Unit Tests for V4B Resilience Infrastructure

Tests for:
- v4b_disk_monitor.py (disk space monitoring and cleanup)
- v4b_checkpoint.py (checkpoint/resume system)
"""

import unittest
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import sys
import os

# Add repo root to path
REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))


class TestDiskMonitor(unittest.TestCase):
    """Test disk space monitoring and cleanup."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = self.test_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_disk_usage_calculation(self):
        """Test disk usage calculation."""
        # Create test files
        test_file = Path(self.test_dir) / 'test.txt'
        test_file.write_text('x' * 1024)  # 1KB
        
        # Verify file size
        self.assertEqual(test_file.stat().st_size, 1024)
    
    def test_cleanup_targets_defined(self):
        """Test that cleanup targets are properly defined."""
        from v4b_disk_monitor import DiskMonitor
        
        monitor = DiskMonitor(self.repo_root)
        
        # Verify cleanup targets exist
        self.assertIsNotNone(monitor.CLEANUP_TARGETS)
        self.assertGreater(len(monitor.CLEANUP_TARGETS), 0)
        
        # Verify each target has name and size
        for target_name, keep_gb in monitor.CLEANUP_TARGETS:
            self.assertIsInstance(target_name, str)
            self.assertIsInstance(keep_gb, (int, float))
            self.assertGreater(keep_gb, 0)
    
    def test_thresholds_defined(self):
        """Test that disk thresholds are properly defined."""
        from v4b_disk_monitor import DiskMonitor
        
        monitor = DiskMonitor(self.repo_root)
        
        # Verify thresholds
        self.assertGreater(monitor.CRITICAL_THRESHOLD, 0)
        self.assertGreater(monitor.WARNING_THRESHOLD, monitor.CRITICAL_THRESHOLD)
        self.assertGreater(monitor.TARGET_FREE_SPACE, monitor.WARNING_THRESHOLD)
    
    def test_status_file_creation(self):
        """Test that status file is created."""
        from v4b_disk_monitor import DiskMonitor
        
        monitor = DiskMonitor(self.repo_root)
        
        # Create status file
        status = {
            'timestamp': datetime.utcnow().isoformat(),
            'drives': {'D:': {'free_gb': 100, 'total_gb': 1000, 'used_gb': 900, 'used_percent': 90}},
            'pipeline_safe': True,
            'warnings': [],
            'actions_taken': []
        }
        
        monitor._save_status(status)
        
        # Verify file was created
        self.assertTrue(monitor.status_file.exists())
        
        # Verify file contents
        with open(monitor.status_file, 'r') as f:
            loaded = json.load(f)
        
        self.assertEqual(loaded['pipeline_safe'], True)
        self.assertIn('D:', loaded['drives'])
    
    def test_cleanup_directory_logic(self):
        """Test cleanup directory logic."""
        from v4b_disk_monitor import DiskMonitor
        
        monitor = DiskMonitor(self.repo_root)
        
        # Create test directory with files
        test_dir = Path(self.test_dir) / 'test_cleanup'
        test_dir.mkdir()
        
        # Create files with different modification times
        for i in range(5):
            file_path = test_dir / f'file_{i}.txt'
            file_path.write_text('x' * 1024)  # 1KB each
        
        # Cleanup should keep at least keep_gb size
        freed = monitor._cleanup_directory(test_dir, keep_gb=0.001)  # Keep 1MB
        
        # Verify some files were removed
        remaining_files = list(test_dir.glob('*'))
        self.assertLess(len(remaining_files), 5)


class TestCheckpointManager(unittest.TestCase):
    """Test checkpoint management and resume system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = self.test_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_checkpoint_manager_initialization(self):
        """Test checkpoint manager initialization."""
        from v4b_checkpoint import CheckpointManager
        
        manager = CheckpointManager(self.repo_root)
        
        # Verify checkpoint directory created
        self.assertTrue(manager.checkpoint_dir.exists())
        self.assertEqual(manager.checkpoint_dir.name, 'checkpoints')
    
    def test_checkpoint_data_creation(self):
        """Test checkpoint data structure."""
        from v4b_checkpoint import CheckpointData
        
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        
        # Verify all fields
        self.assertEqual(checkpoint.phase, 'mock_calibration')
        self.assertEqual(checkpoint.sector_index, 5)
        self.assertEqual(checkpoint.mock_index, 3)
        self.assertEqual(checkpoint.progress_percent, 15.0)
        self.assertIsNone(checkpoint.error_message)
        self.assertEqual(checkpoint.retry_count, 0)
    
    def test_checkpoint_save_and_load(self):
        """Test saving and loading checkpoints."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Create and save checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=10,
            mock_index=5,
            status='in_progress',
            progress_percent=30.0,
            elapsed_seconds=7200,
            estimated_remaining_seconds=16800,
            last_successful_sector=10,
            last_successful_mock=5
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Load checkpoint
        loaded = manager.load_checkpoint()
        
        # Verify loaded checkpoint matches saved
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.phase, 'mock_calibration')
        self.assertEqual(loaded.sector_index, 10)
        self.assertEqual(loaded.mock_index, 5)
        self.assertEqual(loaded.progress_percent, 30.0)
    
    def test_resume_position_calculation(self):
        """Test resume position calculation."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save checkpoint at sector 15, mock 8
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=15,
            mock_index=8,
            status='in_progress',
            progress_percent=45.0,
            elapsed_seconds=16200,
            estimated_remaining_seconds=19800,
            last_successful_sector=15,
            last_successful_mock=8
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Get resume position
        sector, mock = manager.get_resume_position()
        
        # Should resume from next mock (8+1=9)
        self.assertEqual(sector, 15)
        self.assertEqual(mock, 9)
    
    def test_checkpoint_history(self):
        """Test checkpoint history tracking."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save multiple checkpoints
        for i in range(3):
            checkpoint = CheckpointData(
                timestamp=datetime.utcnow().isoformat(),
                phase='mock_calibration',
                sector_index=i,
                mock_index=0,
                status='in_progress',
                progress_percent=float(i * 10),
                elapsed_seconds=i * 1000,
                estimated_remaining_seconds=(35 - i) * 1000,
                last_successful_sector=i,
                last_successful_mock=0
            )
            manager.save_checkpoint(checkpoint)
        
        # Verify history file exists
        self.assertTrue(manager.history_file.exists())
        
        # Verify history has entries
        with open(manager.history_file, 'r') as f:
            lines = f.readlines()
        
        self.assertGreaterEqual(len(lines), 3)
    
    def test_checkpoint_integrity_verification(self):
        """Test checkpoint integrity verification."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save valid checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Verify integrity
        is_valid = manager.verify_checkpoint_integrity()
        self.assertTrue(is_valid)
    
    def test_mark_sector_complete(self):
        """Test marking sector as complete."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save initial checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Mark sector complete
        manager.mark_sector_complete(5, 9)
        
        # Load and verify
        loaded = manager.load_checkpoint()
        self.assertEqual(loaded.last_successful_sector, 5)
        self.assertEqual(loaded.last_successful_mock, 9)
        self.assertEqual(loaded.retry_count, 0)
    
    def test_mark_failed(self):
        """Test marking checkpoint as failed."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Mark as failed
        manager.mark_failed("GPU out of memory", retry_count=1)
        
        # Load and verify
        loaded = manager.load_checkpoint()
        self.assertEqual(loaded.status, 'failed')
        self.assertEqual(loaded.error_message, "GPU out of memory")
        self.assertEqual(loaded.retry_count, 1)
    
    def test_clear_checkpoint(self):
        """Test clearing checkpoint."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        
        manager.save_checkpoint(checkpoint)
        self.assertTrue(manager.current_checkpoint_file.exists())
        
        # Clear checkpoint
        manager.clear_checkpoint()
        self.assertFalse(manager.current_checkpoint_file.exists())
    
    def test_statistics_generation(self):
        """Test statistics generation from checkpoint history."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save multiple checkpoints
        for i in range(5):
            checkpoint = CheckpointData(
                timestamp=datetime.utcnow().isoformat(),
                phase='mock_calibration',
                sector_index=i,
                mock_index=0,
                status='completed' if i < 4 else 'in_progress',
                progress_percent=float(i * 20),
                elapsed_seconds=i * 1000,
                estimated_remaining_seconds=(35 - i) * 1000,
                last_successful_sector=i,
                last_successful_mock=0
            )
            manager.save_checkpoint(checkpoint)
        
        # Get statistics
        stats = manager.get_statistics()
        
        # Verify statistics
        self.assertGreater(stats['total_checkpoints'], 0)
        self.assertIn('phases', stats)


class TestCheckpointedLoop(unittest.TestCase):
    """Test checkpointed loop helper."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = self.test_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_checkpointed_loop_initialization(self):
        """Test checkpointed loop initialization."""
        from v4b_checkpoint import CheckpointManager, CheckpointedLoop
        
        manager = CheckpointManager(self.repo_root)
        loop = CheckpointedLoop(manager, 'mock_calibration', total_sectors=35)
        
        # Verify initialization
        self.assertEqual(loop.phase, 'mock_calibration')
        self.assertEqual(loop.total_sectors, 35)
        self.assertIsNone(loop.start_time)
    
    def test_checkpointed_loop_resume(self):
        """Test checkpointed loop resume position."""
        from v4b_checkpoint import CheckpointManager, CheckpointedLoop, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save checkpoint
        checkpoint = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=10,
            mock_index=5,
            status='in_progress',
            progress_percent=30.0,
            elapsed_seconds=7200,
            estimated_remaining_seconds=16800,
            last_successful_sector=10,
            last_successful_mock=5
        )
        
        manager.save_checkpoint(checkpoint)
        
        # Create loop and get resume position
        loop = CheckpointedLoop(manager, 'mock_calibration')
        sector, mock = loop.get_resume_position()
        
        # Should resume from next mock
        self.assertEqual(sector, 10)
        self.assertEqual(mock, 6)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = self.test_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_checkpoint_with_missing_fields(self):
        """Test checkpoint loading with missing fields."""
        from v4b_checkpoint import CheckpointManager
        
        manager = CheckpointManager(self.repo_root)
        
        # Create checkpoint file with missing fields
        incomplete_checkpoint = {
            'timestamp': datetime.utcnow().isoformat(),
            'phase': 'mock_calibration',
            'sector_index': 5
            # Missing required fields
        }
        
        with open(manager.current_checkpoint_file, 'w') as f:
            json.dump(incomplete_checkpoint, f)
        
        # Try to load - should handle gracefully
        try:
            checkpoint = manager.load_checkpoint()
            # Either returns None or raises exception (both acceptable)
        except (KeyError, ValueError):
            # Expected for incomplete checkpoint
            pass
    
    def test_checkpoint_with_corrupted_json(self):
        """Test checkpoint loading with corrupted JSON."""
        from v4b_checkpoint import CheckpointManager
        
        manager = CheckpointManager(self.repo_root)
        
        # Create corrupted checkpoint file
        with open(manager.current_checkpoint_file, 'w') as f:
            f.write('{ invalid json }')
        
        # Try to load - should handle gracefully
        try:
            checkpoint = manager.load_checkpoint()
            # Should return None or handle error
        except (json.JSONDecodeError, ValueError):
            # Expected for corrupted JSON
            pass
    
    def test_disk_monitor_with_zero_disk_space(self):
        """Test disk monitor behavior with zero disk space."""
        from v4b_disk_monitor import DiskMonitor
        
        monitor = DiskMonitor(self.repo_root)
        
        # Test threshold comparison with zero
        self.assertFalse(0 >= monitor.CRITICAL_THRESHOLD)
        self.assertTrue(monitor.CRITICAL_THRESHOLD > 0)
    
    def test_checkpoint_resume_with_no_checkpoint(self):
        """Test resume position with no checkpoint file."""
        from v4b_checkpoint import CheckpointManager
        
        manager = CheckpointManager(self.repo_root)
        
        # Get resume position without saving checkpoint
        sector, mock = manager.get_resume_position()
        
        # Should return (0, 0) for fresh start
        self.assertEqual(sector, 0)
        self.assertEqual(mock, 0)


class TestIntegration(unittest.TestCase):
    """Integration tests for checkpoint and disk monitor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.repo_root = self.test_dir
    
    def tearDown(self):
        """Clean up test fixtures."""
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_full_checkpoint_workflow(self):
        """Test full checkpoint workflow: save, load, resume, mark complete."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Step 1: Save initial checkpoint
        checkpoint1 = CheckpointData(
            timestamp=datetime.utcnow().isoformat(),
            phase='mock_calibration',
            sector_index=5,
            mock_index=3,
            status='in_progress',
            progress_percent=15.0,
            elapsed_seconds=3600,
            estimated_remaining_seconds=20400,
            last_successful_sector=5,
            last_successful_mock=3
        )
        manager.save_checkpoint(checkpoint1)
        
        # Step 2: Load checkpoint
        loaded1 = manager.load_checkpoint()
        self.assertEqual(loaded1.sector_index, 5)
        
        # Step 3: Get resume position
        sector, mock = manager.get_resume_position()
        self.assertEqual(sector, 5)
        self.assertEqual(mock, 4)
        
        # Step 4: Mark sector complete
        manager.mark_sector_complete(5, 9)
        
        # Step 5: Load updated checkpoint
        loaded2 = manager.load_checkpoint()
        self.assertEqual(loaded2.last_successful_mock, 9)
        
        # Step 6: Get new resume position
        sector, mock = manager.get_resume_position()
        self.assertEqual(sector, 5)
        self.assertEqual(mock, 10)
    
    def test_checkpoint_history_tracking(self):
        """Test that checkpoint history is properly tracked."""
        from v4b_checkpoint import CheckpointManager, CheckpointData
        
        manager = CheckpointManager(self.repo_root)
        
        # Save checkpoints for multiple sectors
        for sector in range(3):
            for mock in range(2):
                checkpoint = CheckpointData(
                    timestamp=datetime.utcnow().isoformat(),
                    phase='mock_calibration',
                    sector_index=sector,
                    mock_index=mock,
                    status='in_progress',
                    progress_percent=float((sector * 2 + mock) * 5),
                    elapsed_seconds=(sector * 2 + mock) * 100,
                    estimated_remaining_seconds=(35 * 2 - sector * 2 - mock) * 100,
                    last_successful_sector=sector,
                    last_successful_mock=mock
                )
                manager.save_checkpoint(checkpoint)
        
        # Verify history
        stats = manager.get_statistics()
        self.assertGreater(stats['total_checkpoints'], 0)


if __name__ == '__main__':
    unittest.main()
