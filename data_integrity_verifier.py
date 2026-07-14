#!/usr/bin/env python3
"""
Data Integrity Verifier for Euclid Q1 Data
Ensures real data sources are used and creates cryptographic verification tokens
"""

import json
import hashlib
import hmac
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid

class DataIntegrityVerifier:
    """Manages data source verification and integrity tokens."""
    
    # Real data source identifiers
    REAL_SOURCES = {
        'EUCLID_Q1': 'Euclid Q1 Mission Data (2024-2025)',
        'SDSS_BOSS_DR17': 'SDSS BOSS DR17 Spectroscopic Survey',
        'GAIA_DR3': 'Gaia Data Release 3',
        'PANSTARRS': 'Pan-STARRS Survey',
        'WISE': 'WISE All-Sky Survey'
    }
    
    SYNTHETIC_SOURCES = {
        'SIMULATION': 'Synthetic/Simulated Data',
        'FALLBACK': 'Fallback Physical Model',
        'MOCK': 'Mock Data for Testing'
    }
    
    def __init__(self, repo_root: str = None):
        """Initialize verifier."""
        if repo_root is None:
            repo_root = Path(__file__).parent
        else:
            repo_root = Path(repo_root)
        
        self.repo_root = repo_root
        self.verification_log = repo_root / 'logs' / 'data_integrity_verification.log'
        self.verification_tokens_file = repo_root / 'logs' / 'data_verification_tokens.json'
        self.data_manifest = repo_root / 'DATA_MANIFEST.json'
        
        self.verification_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Secret key for HMAC (should be environment variable in production)
        self.secret_key = b"euclid_q1_verification_key_2026"
    
    def generate_verification_token(self, data_entry: Dict) -> str:
        """Generate cryptographic verification token for data entry."""
        # Create deterministic hash of data content
        data_str = json.dumps(data_entry, sort_keys=True)
        content_hash = hashlib.sha256(data_str.encode()).hexdigest()
        
        # Create HMAC signature
        signature = hmac.new(
            self.secret_key,
            content_hash.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Combine for verification token
        token = f"VERIFY-{content_hash[:16]}-{signature[:16]}"
        return token
    
    def generate_data_integrity_token(self, discoveries: List[Dict]) -> Dict:
        """Generate comprehensive data integrity token for all discoveries."""
        timestamp = datetime.utcnow().isoformat()
        token_id = str(uuid.uuid4())
        
        # Analyze data sources
        source_analysis = self._analyze_sources(discoveries)
        
        # Create integrity manifest
        integrity_data = {
            'token_id': token_id,
            'timestamp': timestamp,
            'total_discoveries': len(discoveries),
            'source_analysis': source_analysis,
            'real_data_count': source_analysis['real_data_count'],
            'synthetic_data_count': source_analysis['synthetic_data_count'],
            'data_quality_score': source_analysis['quality_score'],
            'verification_status': 'VERIFIED' if source_analysis['real_data_count'] > 0 else 'SYNTHETIC_ONLY'
        }
        
        # Generate token
        token = self.generate_verification_token(integrity_data)
        integrity_data['integrity_token'] = token
        
        return integrity_data
    
    def _analyze_sources(self, discoveries: List[Dict]) -> Dict:
        """Analyze data sources in discoveries."""
        real_count = 0
        synthetic_count = 0
        source_breakdown = {}
        
        for discovery in discoveries:
            source = discovery.get('source', 'Unknown')
            
            # Categorize source
            is_real = False
            for real_key in self.REAL_SOURCES.keys():
                if real_key in source:
                    is_real = True
                    break
            
            if is_real:
                real_count += 1
            else:
                synthetic_count += 1
            
            # Track breakdown
            if source not in source_breakdown:
                source_breakdown[source] = 0
            source_breakdown[source] += 1
        
        # Calculate quality score (0-100)
        total = real_count + synthetic_count
        quality_score = (real_count / total * 100) if total > 0 else 0
        
        return {
            'real_data_count': real_count,
            'synthetic_data_count': synthetic_count,
            'total_count': total,
            'quality_score': round(quality_score, 2),
            'source_breakdown': source_breakdown,
            'real_percentage': round((real_count / total * 100), 2) if total > 0 else 0
        }
    
    def verify_discovery_integrity(self, discovery: Dict) -> Tuple[bool, str]:
        """Verify integrity of individual discovery."""
        required_fields = [
            'id', 'timestamp', 'sector_index', 'ra_min', 'ra_max',
            'dec_min', 'dec_max', 'num_galaxies', 'delta', 'source'
        ]
        
        # Check required fields
        missing_fields = [f for f in required_fields if f not in discovery]
        if missing_fields:
            return False, f"Missing fields: {missing_fields}"
        
        # Verify data types
        try:
            float(discovery['delta'])
            int(discovery['num_galaxies'])
            int(discovery['sector_index'])
        except (ValueError, TypeError):
            return False, "Invalid data types"
        
        # Check source authenticity
        source = discovery.get('source', '')
        is_real = any(real_key in source for real_key in self.REAL_SOURCES.keys())
        
        if not is_real:
            # Check if it's at least a known synthetic source
            is_synthetic = any(syn_key in source for syn_key in self.SYNTHETIC_SOURCES.keys())
            if not is_synthetic:
                return False, f"Unknown data source: {source}"
        
        return True, "Valid"
    
    def create_data_manifest(self, discoveries: List[Dict]) -> Dict:
        """Create comprehensive data manifest with verification."""
        manifest = {
            'manifest_id': str(uuid.uuid4()),
            'created_at': datetime.utcnow().isoformat(),
            'total_discoveries': len(discoveries),
            'discoveries': []
        }
        
        for discovery in discoveries:
            is_valid, message = self.verify_discovery_integrity(discovery)
            
            discovery_entry = {
                'id': discovery.get('id'),
                'source': discovery.get('source'),
                'timestamp': discovery.get('timestamp'),
                'valid': is_valid,
                'verification_message': message,
                'verification_token': self.generate_verification_token(discovery)
            }
            
            manifest['discoveries'].append(discovery_entry)
        
        # Generate manifest token
        manifest_token = self.generate_verification_token(manifest)
        manifest['manifest_token'] = manifest_token
        
        return manifest
    
    def log_verification(self, message: str, level: str = 'INFO'):
        """Log verification event."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        try:
            with open(self.verification_log, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        except:
            pass
    
    def save_verification_tokens(self, integrity_token: Dict, manifest: Dict):
        """Save verification tokens to file."""
        tokens = {
            'integrity_token': integrity_token,
            'manifest': manifest,
            'saved_at': datetime.utcnow().isoformat()
        }
        
        try:
            with open(self.verification_tokens_file, 'w', encoding='utf-8') as f:
                json.dump(tokens, f, indent=2, ensure_ascii=False)
            self.log_verification(f"Verification tokens saved to {self.verification_tokens_file}")
        except Exception as e:
            self.log_verification(f"Error saving verification tokens: {e}", 'ERROR')
    
    def generate_verification_report(self, discoveries: List[Dict]) -> str:
        """Generate comprehensive verification report."""
        integrity_token = self.generate_data_integrity_token(discoveries)
        manifest = self.create_data_manifest(discoveries)
        
        # Save tokens
        self.save_verification_tokens(integrity_token, manifest)
        
        # Generate report
        report = f"""
================================================================================
DATA INTEGRITY VERIFICATION REPORT
================================================================================
Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

INTEGRITY TOKEN
================================================================================
Token ID: {integrity_token['token_id']}
Verification Token: {integrity_token['integrity_token']}
Status: {integrity_token['verification_status']}

DATA SOURCE ANALYSIS
================================================================================
Total Discoveries: {integrity_token['total_discoveries']}
Real Data Count: {integrity_token['source_analysis']['real_data_count']}
Synthetic Data Count: {integrity_token['source_analysis']['synthetic_data_count']}
Real Data Percentage: {integrity_token['source_analysis']['real_percentage']}%
Data Quality Score: {integrity_token['source_analysis']['quality_score']}/100

SOURCE BREAKDOWN
================================================================================
"""
        
        for source, count in integrity_token['source_analysis']['source_breakdown'].items():
            percentage = (count / integrity_token['total_discoveries'] * 100)
            report += f"  {source}: {count} ({percentage:.1f}%)\n"
        
        report += f"""
MANIFEST VERIFICATION
================================================================================
Manifest ID: {manifest['manifest_id']}
Manifest Token: {manifest['manifest_token']}
Total Entries: {manifest['total_discoveries']}

DISCOVERY VERIFICATION STATUS
================================================================================
"""
        
        valid_count = sum(1 for d in manifest['discoveries'] if d['valid'])
        invalid_count = len(manifest['discoveries']) - valid_count
        
        report += f"Valid Discoveries: {valid_count}/{len(manifest['discoveries'])}\n"
        report += f"Invalid Discoveries: {invalid_count}/{len(manifest['discoveries'])}\n"
        
        if invalid_count > 0:
            report += "\nInvalid Discoveries:\n"
            for discovery in manifest['discoveries']:
                if not discovery['valid']:
                    report += f"  - {discovery['id']}: {discovery['verification_message']}\n"
        
        report += f"""
REAL DATA SOURCE VERIFICATION
================================================================================
"""
        
        # Check for real data sources
        real_sources_found = set()
        for discovery in discoveries:
            source = discovery.get('source', '')
            for real_key, real_name in self.REAL_SOURCES.items():
                if real_key in source:
                    real_sources_found.add(real_name)
        
        if real_sources_found:
            report += "Real Data Sources Detected:\n"
            for source in real_sources_found:
                report += f"  ✓ {source}\n"
        else:
            report += "WARNING: No real data sources detected!\n"
            report += "All data appears to be synthetic or fallback models.\n"
        
        report += f"""
RECOMMENDATIONS
================================================================================
"""
        
        if integrity_token['source_analysis']['real_percentage'] < 50:
            report += "⚠ WARNING: Less than 50% real data detected\n"
            report += "  Action: Ensure Euclid Q1 data extraction is properly configured\n"
        
        if invalid_count > 0:
            report += "⚠ WARNING: Invalid discoveries detected\n"
            report += "  Action: Review and fix invalid discovery entries\n"
        
        if integrity_token['source_analysis']['real_percentage'] == 0:
            report += "⚠ CRITICAL: No real data sources detected\n"
            report += "  Action: Implement real Euclid Q1 data extraction immediately\n"
        
        report += f"""
VERIFICATION FILES
================================================================================
Verification Log: {self.verification_log}
Verification Tokens: {self.verification_tokens_file}
Data Manifest: {self.data_manifest}

================================================================================
"""
        
        return report


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Integrity Verifier')
    parser.add_argument('--discoveries', type=str, default='discoveries.json',
                       help='Path to discoveries.json file')
    parser.add_argument('--report', type=str, default='logs/data_integrity_report.txt',
                       help='Output report file')
    
    args = parser.parse_args()
    
    # Load discoveries
    discoveries_path = Path(args.discoveries)
    if not discoveries_path.exists():
        print(f"Error: {discoveries_path} not found")
        return
    
    try:
        with open(discoveries_path, 'r', encoding='utf-8') as f:
            discoveries = json.load(f)
    except Exception as e:
        print(f"Error loading discoveries: {e}")
        return
    
    # Generate verification
    verifier = DataIntegrityVerifier()
    report = verifier.generate_verification_report(discoveries)
    
    # Print and save report
    print(report)
    
    try:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\nReport saved to: {report_path}")
    except Exception as e:
        print(f"Error saving report: {e}")


if __name__ == '__main__':
    main()
