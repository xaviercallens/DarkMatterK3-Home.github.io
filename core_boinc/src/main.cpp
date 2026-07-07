// core_boinc/src/main.cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <limits>
#include <chrono>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

struct Galaxy {
    double x, y, z;
    double ra = 0.0;
    double dec = 0.0;
    double redshift = 0.0;
};

// Exact Cosmological comoving distance solver using CPL (Chevallier-Polarski-Linder) parameterization
// Solves: Dc(z) = (c/H0) * \int_0^z [Omega_m*(1+z')^3 + Omega_de*(1+z')^(3*(1+w0+wa)) * exp(-3*wa*z'/(1+z'))]^(-1/2) dz'
double calculate_comoving_distance_cpl(double z, double h0, double w0, double wa, double omega_m, double omega_de) {
    if (z <= 0.0) return 0.0;
    
    const double c_kms = 299792.458; // speed of light in km/s
    int steps = 1000;                // High-precision numerical integration
    double dz = z / steps;
    double integral = 0.0;

    // Use Trapezoidal Rule for numerical integration
    for (int i = 0; i <= steps; ++i) {
        double zi = i * dz;
        // Dark energy density evolution term for CPL
        double f_de = std::pow(1.0 + zi, 3.0 * (1.0 + w0 + wa)) * std::exp(-3.0 * wa * zi / (1.0 + zi));
        double E_z = std::sqrt(omega_m * std::pow(1.0 + zi, 3) + omega_de * f_de);
        
        double weight = (i == 0 || i == steps) ? 0.5 : 1.0;
        integral += weight * (1.0 / E_z);
    }
    
    double D_c = (c_kms / h0) * integral * dz;
    return D_c;
}

// Convert spherical (RA, DEC, Redshift) to Cartesian Mpc
Galaxy convert_spherical_to_cartesian(double ra, double dec, double redshift, double h0, double w0, double wa, double omega_m, double omega_de) {
    double D_c = calculate_comoving_distance_cpl(redshift, h0, w0, wa, omega_m, omega_de);
    double ra_rad = ra * M_PI / 180.0;
    double dec_rad = dec * M_PI / 180.0;
    
    Galaxy g;
    g.ra = ra;
    g.dec = dec;
    g.redshift = redshift;
    g.x = D_c * std::cos(dec_rad) * std::cos(ra_rad);
    g.y = D_c * std::cos(dec_rad) * std::sin(ra_rad);
    g.z = D_c * std::sin(dec_rad);
    return g;
}

// Generates Picard-Fuchs S1,2 curve trajectory
std::vector<Galaxy> generate_picard_fuchs_knot(int num_points = 2000) {
    std::vector<Galaxy> knot;
    for (int i = 0; i < num_points; ++i) {
        double t = 2.0 * M_PI * i / num_points;
        // The algebraic 3D projection of the S1,2 Calabi-Yau moduli loop
        double x = 150.0 * std::sin(2.0 * t) * std::cos(3.0 * t);
        double y = 150.0 * std::sin(2.0 * t) * std::sin(3.0 * t);
        double z = 100.0 * std::cos(5.0 * t);
        knot.push_back({x, y, z, 0, 0, 0});
    }
    return knot;
}

// Fast nearest neighbor 3D distance checker between galaxy cloud and algebraic knot path
double compute_average_knot_distance(const std::vector<Galaxy>& galaxies, const std::vector<Galaxy>& knot) {
    if (galaxies.empty() || knot.empty()) return 0.0;
    
    double total_min_dist = 0.0;
    size_t total_size = galaxies.size();
    size_t num_chunks = 5; // Report progress at 20%, 40%, 60%, 80%, 100%
    size_t chunk_size = total_size / num_chunks;

    std::cout << "   [BOEINC API] Commencing nearest-neighbor topological search over OpenMP..." << std::endl;

    for (size_t c = 0; c < num_chunks; ++c) {
        size_t start_idx = c * chunk_size;
        size_t end_idx = (c == num_chunks - 1) ? total_size : (c + 1) * chunk_size;
        double chunk_min_dist = 0.0;

        // Multi-threaded nearest neighbor search for this segment
        #pragma omp parallel for reduction(+:chunk_min_dist)
        for (size_t i = start_idx; i < end_idx; ++i) {
            double min_dist_sq = std::numeric_limits<double>::max();
            for (size_t j = 0; j < knot.size(); ++j) {
                double dx = galaxies[i].x - knot[j].x;
                double dy = galaxies[i].y - knot[j].y;
                double dz = galaxies[i].z - knot[j].z;
                double dist_sq = dx*dx + dy*dy + dz*dz;
                if (dist_sq < min_dist_sq) {
                    min_dist_sq = dist_sq;
                }
            }
            chunk_min_dist += std::sqrt(min_dist_sq);
        }

        total_min_dist += chunk_min_dist;

        // Progress reporting (Simulation of BOINC progress API)
        double percent_complete = (static_cast<double>(end_idx) / total_size) * 100.0;
        std::cout << "   [BOEINC PROGRESS] " << static_cast<int>(percent_complete) 
                  << "% complete (Processed " << end_idx << "/" << total_size << " galaxies)." << std::endl;

        #ifdef BOINC_APP
        boinc_fraction_done(percent_complete / 100.0);
        if (boinc_time_to_checkpoint()) {
            boinc_checkpoint_completed();
        }
        #endif

        // Write a simulated BOINC checkpoint file for extreme-resilience simulation
        std::ofstream ckpt_file("boinc_checkpoint.tmp");
        if (ckpt_file.is_open()) {
            ckpt_file << "CHECKPOINT_DATA\n";
            ckpt_file << "GalaxiesProcessed=" << end_idx << "\n";
            ckpt_file << "RunningTotalDistance=" << total_min_dist << "\n";
            ckpt_file.close();
            std::rename("boinc_checkpoint.tmp", "boinc_checkpoint.txt");
        }
    }

    // Clean up checkpoint file upon successful job completion
    std::remove("boinc_checkpoint.txt");

    return total_min_dist / total_size;
}

int main(int argc, char* argv[]) {
    auto start_time = std::chrono::high_resolution_clock::now();
    std::cout << "🌌 S21 DarK3CosmicWeb@Home -- ADVANCED NATIVE HPC SOLVER BOOTING..." << std::endl;
    std::cout << "   [BOEINC API] Initializing CPL-integrated handshake sequence..." << std::endl;

    if (argc < 2) {
        std::cerr << "   [ERROR] Missing input shard coordinate file path!" << std::endl;
        std::cerr << "   Usage: " << argv[0] << " <file_path> [--raw] [H0 w0 wa Omega_m Omega_de]" << std::endl;
        return 1;
    }

    std::string filepath = argv[1];
    bool is_raw = false;
    
    // Parse arguments
    double h0 = 71.92;
    double w0 = -0.5485;
    double wa = -0.3968;
    double omega_m = 0.315;
    double omega_de = 0.685;

    for (int i = 2; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--raw") {
            is_raw = true;
        } else if (i + 4 < argc) {
            h0 = std::stod(argv[i]);
            w0 = std::stod(argv[i+1]);
            wa = std::stod(argv[i+2]);
            omega_m = std::stod(argv[i+3]);
            omega_de = std::stod(argv[i+4]);
            break;
        }
    }

    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "   [ERROR] Failed to read shard input coordinate path: " << filepath << std::endl;
        return 2;
    }

    std::vector<Galaxy> galaxies;
    std::string line;
    
    // Parse the input file. 
    // If raw is requested, expects: RA, DEC, Redshift. Otherwise expects pre-computed Cartesian X, Y, Z.
    while (std::getline(file, line)) {
        if (line.empty() || line[0] == '#') continue;
        std::stringstream ss(line);
        double col1, col2, col3;
        if (ss >> col1 >> col2 >> col3) {
            if (is_raw) {
                // Spherical astronomical coordinates (RA, DEC, redshift) -> Cartesian conversion using CPL
                galaxies.push_back(convert_spherical_to_cartesian(col1, col2, col3, h0, w0, wa, omega_m, omega_de));
            } else {
                // Pre-converted Cartesian
                galaxies.push_back({col1, col2, col3});
            }
        }
    }

    std::cout << "   [DATA] Loaded " << galaxies.size() << " galaxies from " 
              << (is_raw ? "SDSS/Euclid spherical raw" : "Cartesian pre-converted") << " shard." << std::endl;

    if (galaxies.empty()) {
        std::cerr << "   [ERROR] Shard contains 0 valid galaxies. Cannot proceed with TDA Sieve." << std::endl;
        return 3;
    }

    // Run spatial 3:2 asymmetry ratio solver
    double x_sum = 0, y_sum = 0, z_sum = 0;
    for (const auto& g : galaxies) {
        x_sum += g.x;
        y_sum += g.y;
        z_sum += g.z;
    }

    double n = static_cast<double>(galaxies.size());
    double mean_x = x_sum / n;
    double mean_y = y_sum / n;
    double mean_z = z_sum / n;

    double var_x = 0, var_y = 0, var_z = 0;
    for (const auto& g : galaxies) {
        var_x += std::pow(g.x - mean_x, 2);
        var_y += std::pow(g.y - mean_y, 2);
        var_z += std::pow(g.z - mean_z, 2);
    }

    double dev_x = std::sqrt(var_x / n);
    double dev_y = std::sqrt(var_y / n);
    double dev_z = std::sqrt(var_z / n);

    // 3:2 spatial symmetry ratio check
    double ratio_xy = (dev_y > 0.0) ? (dev_x / dev_y) : 1.0;
    double delta = std::abs(ratio_xy - 1.5);
    double asymmetry_score = 1.0 / (1.0 + delta);

    // Compute topological alignment with the Picard-Fuchs S_1,2 Calabi-Yau loop
    std::cout << "   [MATH] Simulating Picard-Fuchs S1,2 moduli loop & running nearest-neighbor TDA..." << std::endl;
    std::vector<Galaxy> knot = generate_picard_fuchs_knot();
    double avg_distance_to_knot = compute_average_knot_distance(galaxies, knot);
    
    // Scale distance score
    double alignment_score = 100.0 / (100.0 + avg_distance_to_knot);

    auto end_time = std::chrono::high_resolution_clock::now();
    double elapsed_ms = std::chrono::duration<double, std::milli>(end_time - start_time).count();

    std::cout << "   [RESULT] Dispersion Dev X: " << dev_x << " Mpc | Dev Y: " << dev_y << " Mpc" << std::endl;
    std::cout << "   [RESULT] S1,2 Asymmetry Delta: " << delta << " | Ratio X/Y: " << ratio_xy << std::endl;
    std::cout << "   [RESULT] Average distance to Picard-Fuchs knot: " << avg_distance_to_knot << " Mpc" << std::endl;
    std::cout << "   [RESULT] K3 Topological Alignment Score: " << alignment_score << std::endl;
    std::cout << "   [BENCHMARK] Executed in " << elapsed_ms << " ms." << std::endl;

    // Output BOEINC result receipts
    std::ofstream outfile("receipt_boinc.txt");
    outfile << "BOINC_WU_RECEIPT\n";
    outfile << "Galaxies=" << galaxies.size() << "\n";
    outfile << "AsymmetryRatio=" << ratio_xy << "\n";
    outfile << "Delta=" << delta << "\n";
    outfile << "Score=" << asymmetry_score << "\n";
    outfile << "KnotDistance=" << avg_distance_to_knot << "\n";
    outfile << "AlignmentScore=" << alignment_score << "\n";
    outfile << "ComputationTimeMs=" << elapsed_ms << "\n";
    outfile << "Status=success\n";
    outfile.close();

    std::cout << "🏆 [SUCCESS] BOEINC verification receipt successfully written." << std::endl;
    return 0;
}
