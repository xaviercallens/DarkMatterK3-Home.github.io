#!/usr/bin/env python3
"""Astronomy Discovery Analyzer - K3 Surface Discoveries from Astrophysical Perspective."""

import json
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import statistics
import numpy as np

def calculate_k3_resonance_mass(delta, base_mass_ev=1.83e-21, coupling_k=0.048):
    """
    Calculates the effective extra-dimensional Kaluza-Klein resonance mass (in eV) 
    based on the geometric resonance model (cf. Tsai et al., 2026).
    Uses the empirical K3 asymmetry (Delta) as the geometric warping parameter.
    """
    # The larger the asymmetry (Delta), the tighter the geometric pinching,
    # leading to an exponentially higher resonance frequency (mass).
    warping_factor = np.exp(coupling_k * delta)
    
    # Effective Mass calculation based on K3 geometric resonance
    m_res = base_mass_ev * warping_factor
    
    return m_res

class AstronomyClass(Enum):
    """Astronomy classification of K3 surface discoveries."""
    DARK_MATTER_HALO = "DARK_MATTER_HALO"           # Galactic halo structure
    GALAXY_CLUSTER = "GALAXY_CLUSTER"               # Galaxy cluster detection
    COSMIC_FILAMENT = "COSMIC_FILAMENT"             # Large-scale filament
    VOID_BOUNDARY = "VOID_BOUNDARY"                 # Void edge detection
    GALAXY_GROUP = "GALAXY_GROUP"                   # Small galaxy group
    SUPERMASSIVE_BH_REGION = "SUPERMASSIVE_BH"      # Supermassive black hole region
    MERGER_SIGNATURE = "MERGER_SIGNATURE"           # Galaxy merger evidence
    LENSING_REGION = "LENSING_REGION"               # Gravitational lensing
    QUASAR_ENVIRONMENT = "QUASAR_ENVIRONMENT"       # Quasar host region
    ACTIVE_GALACTIC_NUCLEI = "ACTIVE_GALACTIC_NUCLEI" # AGN region
    STAR_FORMING_REGION = "STAR_FORMING_REGION"     # Star formation hotspot
    DWARF_GALAXY_CLUSTER = "DWARF_GALAXY_CLUSTER"   # Dwarf galaxy concentration
    SATELLITE_SYSTEM = "SATELLITE_SYSTEM"           # Satellite galaxy system
    TIDAL_DISRUPTION = "TIDAL_DISRUPTION"           # Tidal disruption evidence
    REDSHIFT_ANOMALY = "REDSHIFT_ANOMALY"           # Unusual redshift distribution

class AstronomySignificance(Enum):
    """Astrophysical significance levels."""
    EXCEPTIONAL = "EXCEPTIONAL"     # Rare, potentially new discovery
    MAJOR = "MAJOR"                 # Significant astrophysical feature
    NOTABLE = "NOTABLE"             # Important for cosmology
    INTERESTING = "INTERESTING"     # Worth detailed study
    STANDARD = "STANDARD"           # Normal cosmological feature

@dataclass
class AstronomyDiscovery:
    """Astronomy-focused discovery analysis."""
    discovery_id: str
    timestamp: str
    sector_index: int
    ra_min: float
    ra_max: float
    dec_min: float
    dec_max: float
    num_galaxies: int
    max_asymmetry: float
    mean_asymmetry: float
    s12_value: float
    wasserstein_distance: float
    astronomy_class: AstronomyClass
    significance: AstronomySignificance
    astrophysical_interpretation: str
    scientific_implications: str
    observational_recommendations: str
    related_phenomena: List[str] = None
    estimated_redshift_range: str = ""
    estimated_mass: str = ""
    
    def to_dict(self):
        """Convert to dictionary."""
        data = asdict(self)
        data['astronomy_class'] = self.astronomy_class.value
        data['significance'] = self.significance.value
        data['related_phenomena'] = self.related_phenomena or []
        return data

class AstronomyDiscoveryAnalyzer:
    """Analyze K3 surface discoveries from astronomy perspective."""
    
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.discoveries_file = self.repo_root / "discoveries.json"
        self.astronomy_file = self.repo_root / "astronomy_discoveries.json"
        self.astronomy_log = self.repo_root / "logs" / "astronomy_analysis.log"
        self.discoveries = []
        self.astronomy_discoveries = []
        self.load_data()
    
    def load_data(self):
        """Load existing discoveries."""
        if self.discoveries_file.exists():
            try:
                with open(self.discoveries_file, 'r') as f:
                    data = json.load(f)
                    self.discoveries = data if isinstance(data, list) else [data]
            except Exception:
                self.discoveries = []
        
        if self.astronomy_file.exists():
            try:
                with open(self.astronomy_file, 'r') as f:
                    data = json.load(f)
                    self.astronomy_discoveries = data if isinstance(data, list) else [data]
            except Exception:
                self.astronomy_discoveries = []
    
    def classify_astronomy(self, discovery: Dict) -> tuple:
        """Classify discovery from astronomy perspective."""
        asymmetry = discovery.get('max_asymmetry', 0)
        s12 = discovery.get('s12', 0)
        num_galaxies = discovery.get('num_galaxies', 0)
        wasserstein = discovery.get('wasserstein_distance', 0)
        
        # Classification logic based on astrophysical signatures
        
        # Dark Matter Halo
        if asymmetry > 100 and num_galaxies > 30000 and s12 > 1.5:
            return (AstronomyClass.DARK_MATTER_HALO, AstronomySignificance.MAJOR)
        
        # Galaxy Cluster
        if num_galaxies > 40000 and asymmetry > 80 and s12 > 1.3:
            return (AstronomyClass.GALAXY_CLUSTER, AstronomySignificance.MAJOR)
        
        # Cosmic Filament
        if 1.3 < s12 <= 1.8 and asymmetry > 50:
            return (AstronomyClass.COSMIC_FILAMENT, AstronomySignificance.NOTABLE)
        
        # Void Boundary
        if asymmetry < 20 and num_galaxies < 15000 and wasserstein > 0.3:
            return (AstronomyClass.VOID_BOUNDARY, AstronomySignificance.NOTABLE)
        
        # Galaxy Group
        if 5000 < num_galaxies < 20000 and 30 < asymmetry < 80:
            return (AstronomyClass.GALAXY_GROUP, AstronomySignificance.INTERESTING)
        
        # Supermassive Black Hole Region
        if asymmetry > 120 and s12 > 2.0:
            return (AstronomyClass.SUPERMASSIVE_BH_REGION, AstronomySignificance.EXCEPTIONAL)
        
        # Merger Signature
        if asymmetry > 90 and wasserstein > 0.4 and s12 > 1.6:
            return (AstronomyClass.MERGER_SIGNATURE, AstronomySignificance.MAJOR)
        
        # Gravitational Lensing Region
        if wasserstein > 0.5 and asymmetry > 70:
            return (AstronomyClass.LENSING_REGION, AstronomySignificance.NOTABLE)
        
        # Quasar Environment
        if asymmetry > 100 and s12 > 1.9:
            return (AstronomyClass.QUASAR_ENVIRONMENT, AstronomySignificance.MAJOR)
        
        # Active Galactic Nuclei
        if asymmetry > 80 and s12 > 1.7:
            return (AstronomyClass.ACTIVE_GALACTIC_NUCLEI, AstronomySignificance.MAJOR)
        
        # Star Forming Region
        if asymmetry > 60 and num_galaxies > 25000 and s12 < 1.5:
            return (AstronomyClass.STAR_FORMING_REGION, AstronomySignificance.INTERESTING)
        
        # Dwarf Galaxy Cluster
        if 10000 < num_galaxies < 25000 and asymmetry > 40:
            return (AstronomyClass.DWARF_GALAXY_CLUSTER, AstronomySignificance.INTERESTING)
        
        # Satellite System
        if num_galaxies < 10000 and asymmetry > 50:
            return (AstronomyClass.SATELLITE_SYSTEM, AstronomySignificance.INTERESTING)
        
        # Tidal Disruption
        if asymmetry > 110 and wasserstein > 0.45:
            return (AstronomyClass.TIDAL_DISRUPTION, AstronomySignificance.MAJOR)
        
        # Redshift Anomaly
        if wasserstein > 0.6:
            return (AstronomyClass.REDSHIFT_ANOMALY, AstronomySignificance.NOTABLE)
        
        # Default
        return (AstronomyClass.GALAXY_GROUP, AstronomySignificance.STANDARD)
    
    def get_astrophysical_interpretation(self, discovery: Dict, 
                                        astronomy_class: AstronomyClass) -> str:
        """Get astrophysical interpretation."""
        asymmetry = discovery.get('max_asymmetry', 0)
        s12 = discovery.get('s12', 0)
        num_galaxies = discovery.get('num_galaxies', 0)
        
        interpretations = {
            AstronomyClass.DARK_MATTER_HALO: 
                f"Massive dark matter halo with {num_galaxies:,} galaxies. "
                f"Asymmetry {asymmetry:.1f} indicates significant gravitational potential well. "
                f"Likely host to galaxy cluster or massive elliptical galaxy.",
            
            AstronomyClass.GALAXY_CLUSTER:
                f"Galaxy cluster containing {num_galaxies:,} members. "
                f"S12={s12:.2f} indicates strong gravitational binding. "
                f"Potential Abell cluster or similar structure.",
            
            AstronomyClass.COSMIC_FILAMENT:
                f"Cosmic filament structure with S12={s12:.2f}. "
                f"Part of large-scale structure web. Contains {num_galaxies:,} galaxies. "
                f"Connects galaxy clusters in cosmic web.",
            
            AstronomyClass.VOID_BOUNDARY:
                f"Void boundary region with low galaxy density ({num_galaxies:,} galaxies). "
                f"Marks edge of cosmic void. Asymmetry {asymmetry:.1f} indicates density gradient.",
            
            AstronomyClass.GALAXY_GROUP:
                f"Galaxy group with {num_galaxies:,} members. "
                f"Moderate asymmetry ({asymmetry:.1f}) suggests ongoing interactions. "
                f"Typical Local Group analog.",
            
            AstronomyClass.SUPERMASSIVE_BH_REGION:
                f"Region with supermassive black hole signature. "
                f"Extreme asymmetry ({asymmetry:.1f}) and S12={s12:.2f}. "
                f"Likely AGN or quasar host galaxy.",
            
            AstronomyClass.MERGER_SIGNATURE:
                f"Galaxy merger signature detected. Asymmetry {asymmetry:.1f} and "
                f"Wasserstein distance indicate disturbed morphology. "
                f"{num_galaxies:,} galaxies in merger system.",
            
            AstronomyClass.LENSING_REGION:
                f"Gravitational lensing region. High Wasserstein distance indicates "
                f"strong mass concentration. Asymmetry {asymmetry:.1f} suggests lens mass.",
            
            AstronomyClass.QUASAR_ENVIRONMENT:
                f"Quasar host region. Extreme asymmetry ({asymmetry:.1f}) and S12={s12:.2f}. "
                f"Surrounded by {num_galaxies:,} galaxies. Likely high-redshift quasar.",
            
            AstronomyClass.ACTIVE_GALACTIC_NUCLEI:
                f"Active galactic nuclei region. S12={s12:.2f} indicates active accretion. "
                f"Asymmetry {asymmetry:.1f} suggests ongoing nuclear activity.",
            
            AstronomyClass.STAR_FORMING_REGION:
                f"Star-forming region with {num_galaxies:,} galaxies. "
                f"Asymmetry {asymmetry:.1f} indicates active star formation. "
                f"High stellar mass density.",
            
            AstronomyClass.DWARF_GALAXY_CLUSTER:
                f"Dwarf galaxy cluster with {num_galaxies:,} members. "
                f"Asymmetry {asymmetry:.1f} indicates gravitational interactions. "
                f"Potential satellite system.",
            
            AstronomyClass.SATELLITE_SYSTEM:
                f"Satellite galaxy system with {num_galaxies:,} members. "
                f"Asymmetry {asymmetry:.1f} suggests tidal interaction with primary. "
                f"Analog of Magellanic Clouds.",
            
            AstronomyClass.TIDAL_DISRUPTION:
                f"Tidal disruption event signature. Extreme asymmetry ({asymmetry:.1f}). "
                f"Galaxy being disrupted by gravitational interaction. "
                f"Rare and scientifically valuable.",
            
            AstronomyClass.REDSHIFT_ANOMALY:
                f"Unusual redshift distribution detected. Wasserstein distance indicates "
                f"anomalous galaxy population. May indicate selection effect or new physics.",
        }
        
        return interpretations.get(astronomy_class, "Unknown astrophysical feature")
    
    def get_scientific_implications(self, discovery: Dict, 
                                   astronomy_class: AstronomyClass) -> str:
        """Get scientific implications."""
        implications = {
            AstronomyClass.DARK_MATTER_HALO:
                "Constrains dark matter distribution models. Tests ΛCDM predictions. "
                "Provides mass function data for structure formation.",
            
            AstronomyClass.GALAXY_CLUSTER:
                "Tests cosmological simulations. Constrains cluster mass-richness relation. "
                "Important for dark energy studies via cluster abundance.",
            
            AstronomyClass.COSMIC_FILAMENT:
                "Maps large-scale structure. Tests structure formation theory. "
                "Constrains matter power spectrum.",
            
            AstronomyClass.VOID_BOUNDARY:
                "Probes void properties. Tests structure formation predictions. "
                "Constrains void size distribution.",
            
            AstronomyClass.GALAXY_GROUP:
                "Tests galaxy formation in group environments. "
                "Constrains environmental effects on galaxy evolution.",
            
            AstronomyClass.SUPERMASSIVE_BH_REGION:
                "Tests black hole-galaxy coevolution. Constrains black hole mass function. "
                "Important for understanding galaxy formation.",
            
            AstronomyClass.MERGER_SIGNATURE:
                "Tests merger-driven galaxy evolution. Constrains merger rates. "
                "Important for understanding morphology-density relation.",
            
            AstronomyClass.LENSING_REGION:
                "Tests gravitational lensing predictions. Constrains mass distribution. "
                "Useful for dark matter mapping.",
            
            AstronomyClass.QUASAR_ENVIRONMENT:
                "Tests quasar-environment connection. Constrains quasar clustering. "
                "Important for high-redshift universe studies.",
            
            AstronomyClass.ACTIVE_GALACTIC_NUCLEI:
                "Tests AGN feedback models. Constrains AGN duty cycle. "
                "Important for galaxy evolution.",
            
            AstronomyClass.STAR_FORMING_REGION:
                "Tests star formation in dense environments. Constrains star formation rate. "
                "Important for understanding cosmic star formation history.",
            
            AstronomyClass.DWARF_GALAXY_CLUSTER:
                "Tests dwarf galaxy formation. Constrains satellite galaxy abundance. "
                "Tests missing satellites problem.",
            
            AstronomyClass.SATELLITE_SYSTEM:
                "Tests satellite galaxy survival. Constrains tidal disruption timescales. "
                "Important for understanding halo substructure.",
            
            AstronomyClass.TIDAL_DISRUPTION:
                "Rare event. Tests tidal disruption theory. "
                "Important for understanding galaxy interactions.",
            
            AstronomyClass.REDSHIFT_ANOMALY:
                "May indicate new physics or systematic effects. "
                "Requires detailed investigation. Potential discovery.",
        }
        
        return implications.get(astronomy_class, "Unknown scientific implications")
    
    def get_observational_recommendations(self, discovery: Dict,
                                         astronomy_class: AstronomyClass) -> str:
        """Get observational follow-up recommendations."""
        recommendations = {
            AstronomyClass.DARK_MATTER_HALO:
                "Follow-up: High-resolution imaging (HST/JWST). Spectroscopy for kinematics. "
                "X-ray observations (Chandra/XMM) for hot gas. Weak lensing analysis.",
            
            AstronomyClass.GALAXY_CLUSTER:
                "Follow-up: Multi-wavelength imaging. Spectroscopic redshift survey. "
                "X-ray observations for temperature/mass. Sunyaev-Zeldovich observations.",
            
            AstronomyClass.COSMIC_FILAMENT:
                "Follow-up: Spectroscopic survey along filament. Mapping gas distribution. "
                "X-ray observations. Comparison with simulations.",
            
            AstronomyClass.VOID_BOUNDARY:
                "Follow-up: Detailed spectroscopy of boundary galaxies. "
                "Measure void properties. Compare with void simulations.",
            
            AstronomyClass.GALAXY_GROUP:
                "Follow-up: Spectroscopic survey of members. Kinematic analysis. "
                "X-ray observations for hot gas.",
            
            AstronomyClass.SUPERMASSIVE_BH_REGION:
                "Follow-up: High-resolution imaging. Spectroscopy for black hole mass. "
                "X-ray observations. Variability monitoring.",
            
            AstronomyClass.MERGER_SIGNATURE:
                "Follow-up: Detailed morphological analysis. Spectroscopy for kinematics. "
                "Simulation comparison. Monitor for tidal features.",
            
            AstronomyClass.LENSING_REGION:
                "Follow-up: Lens modeling. Search for lensed sources. "
                "High-resolution imaging. Spectroscopy for mass distribution.",
            
            AstronomyClass.QUASAR_ENVIRONMENT:
                "Follow-up: Spectroscopic confirmation. Redshift measurement. "
                "Imaging of host galaxy. Search for companion galaxies.",
            
            AstronomyClass.ACTIVE_GALACTIC_NUCLEI:
                "Follow-up: Multi-wavelength observations. Variability monitoring. "
                "Spectroscopy for black hole mass. X-ray observations.",
            
            AstronomyClass.STAR_FORMING_REGION:
                "Follow-up: UV/optical imaging. Infrared observations for dust. "
                "Spectroscopy for star formation rate. Molecular gas observations.",
            
            AstronomyClass.DWARF_GALAXY_CLUSTER:
                "Follow-up: Spectroscopic survey. Kinematic analysis. "
                "Search for dark matter. Compare with simulations.",
            
            AstronomyClass.SATELLITE_SYSTEM:
                "Follow-up: Detailed kinematics. Tidal disruption signatures. "
                "Stellar populations. Comparison with models.",
            
            AstronomyClass.TIDAL_DISRUPTION:
                "Follow-up: URGENT - Detailed observations. Spectroscopy. "
                "Monitor evolution. Compare with tidal disruption models.",
            
            AstronomyClass.REDSHIFT_ANOMALY:
                "Follow-up: Spectroscopic confirmation. Check for systematic effects. "
                "Detailed analysis. Compare with other surveys.",
        }
        
        return recommendations.get(astronomy_class, "Standard follow-up observations recommended")
    
    def analyze_discovery(self, discovery: Dict) -> AstronomyDiscovery:
        """Analyze discovery from astronomy perspective."""
        astronomy_class, significance = self.classify_astronomy(discovery)
        
        astro_discovery = AstronomyDiscovery(
            discovery_id=discovery.get('id', 'UNKNOWN'),
            timestamp=datetime.now().isoformat(),
            sector_index=discovery.get('sector_index', 0),
            ra_min=discovery.get('ra_min', 0),
            ra_max=discovery.get('ra_max', 0),
            dec_min=discovery.get('dec_min', 0),
            dec_max=discovery.get('dec_max', 0),
            num_galaxies=discovery.get('num_galaxies', 0),
            max_asymmetry=discovery.get('max_asymmetry', 0),
            mean_asymmetry=discovery.get('mean_asymmetry', 0),
            s12_value=discovery.get('s12', 0),
            wasserstein_distance=discovery.get('wasserstein_distance', 0),
            astronomy_class=astronomy_class,
            significance=significance,
            astrophysical_interpretation=self.get_astrophysical_interpretation(discovery, astronomy_class),
            scientific_implications=self.get_scientific_implications(discovery, astronomy_class),
            observational_recommendations=self.get_observational_recommendations(discovery, astronomy_class),
            estimated_redshift_range=self._estimate_redshift(discovery),
            estimated_mass=self._estimate_mass(discovery)
        )
        
        return astro_discovery
    
    def _estimate_redshift(self, discovery: Dict) -> str:
        """Estimate redshift range based on properties."""
        asymmetry = discovery.get('max_asymmetry', 0)
        num_galaxies = discovery.get('num_galaxies', 0)
        
        if asymmetry > 100 and num_galaxies > 30000:
            return "z ~ 0.1-0.3 (nearby massive cluster)"
        elif num_galaxies > 20000:
            return "z ~ 0.05-0.2 (nearby group/cluster)"
        elif asymmetry > 80:
            return "z ~ 0.1-0.5 (intermediate distance)"
        else:
            return "z ~ 0.0-0.1 (local universe)"
    
    def _estimate_mass(self, discovery: Dict) -> str:
        """Estimate mass based on properties."""
        num_galaxies = discovery.get('num_galaxies', 0)
        asymmetry = discovery.get('max_asymmetry', 0)
        
        # Calculate Kaluza-Klein resonance mass
        kk_mass = calculate_k3_resonance_mass(asymmetry)
        kk_str = f" [KK Res: {kk_mass:.2e} eV]"
        
        # Rough mass estimation
        if num_galaxies > 40000 and asymmetry > 100:
            return f"M ~ 10^15 M_sun (massive cluster){kk_str}"
        elif num_galaxies > 20000:
            return f"M ~ 10^14 M_sun (group/small cluster){kk_str}"
        elif num_galaxies > 10000:
            return f"M ~ 10^13 M_sun (group){kk_str}"
        else:
            return f"M ~ 10^12 M_sun (dwarf/satellite){kk_str}"
    
    def process_all_discoveries(self):
        """Process all discoveries with astronomy analysis."""
        for discovery in self.discoveries:
            astro_discovery = self.analyze_discovery(discovery)
            self.astronomy_discoveries.append(astro_discovery.to_dict())
            self._log_discovery(astro_discovery)
        
        self.save_astronomy_discoveries()
    
    def _log_discovery(self, discovery: AstronomyDiscovery):
        """Log astronomy discovery."""
        try:
            self.astronomy_log.parent.mkdir(parents=True, exist_ok=True)
            with open(self.astronomy_log, 'a') as f:
                f.write(f"\n[{discovery.timestamp}] {discovery.discovery_id}\n")
                f.write(f"  Class: {discovery.astronomy_class.value}\n")
                f.write(f"  Significance: {discovery.significance.value}\n")
                f.write(f"  Interpretation: {discovery.astrophysical_interpretation[:100]}...\n")
                f.write(f"  Redshift: {discovery.estimated_redshift_range}\n")
                f.write(f"  Mass: {discovery.estimated_mass}\n")
        except Exception as e:
            print(f"[ASTRONOMY] Logging error: {e}")
    
    def save_astronomy_discoveries(self):
        """Save astronomy discoveries to JSON."""
        try:
            with open(self.astronomy_file, 'w') as f:
                json.dump(self.astronomy_discoveries, f, indent=2)
        except Exception as e:
            print(f"[ASTRONOMY] Save error: {e}")
    
    def get_summary(self) -> Dict:
        """Get astronomy discovery summary."""
        summary = {
            'total_discoveries': len(self.astronomy_discoveries),
            'by_class': {},
            'by_significance': {},
            'exceptional_count': 0,
            'major_count': 0,
            'notable_count': 0
        }
        
        for disc in self.astronomy_discoveries:
            astro_class = disc.get('astronomy_class')
            significance = disc.get('significance')
            
            summary['by_class'][astro_class] = summary['by_class'].get(astro_class, 0) + 1
            summary['by_significance'][significance] = summary['by_significance'].get(significance, 0) + 1
            
            if significance == 'EXCEPTIONAL':
                summary['exceptional_count'] += 1
            elif significance == 'MAJOR':
                summary['major_count'] += 1
            elif significance == 'NOTABLE':
                summary['notable_count'] += 1
        
        return summary

if __name__ == "__main__":
    repo_root = "D:\\xdev\\DarkMatterK3@Home\\DarkMatterK3-Home.github.io"
    analyzer = AstronomyDiscoveryAnalyzer(repo_root)
    analyzer.process_all_discoveries()
    
    summary = analyzer.get_summary()
    print(f"\n[ASTRONOMY] Analysis Complete")
    print(f"  Total Discoveries: {summary['total_discoveries']}")
    print(f"  Exceptional: {summary['exceptional_count']}")
    print(f"  Major: {summary['major_count']}")
    print(f"  Notable: {summary['notable_count']}")

    # Example for Top Discovery: K3-DISC-0003
    delta_0003 = 47.0
    mass_0003 = calculate_k3_resonance_mass(delta_0003)
    print(f"\n[KALUZA-KLEIN] Example Prediction")
    print(f"  KK Resonance Mass at Supercluster Node 0003: {mass_0003:.2e} eV")
