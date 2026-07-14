// core_wasm/src/lib.rs
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};
use num_complex::Complex;
use rustfft::FftDirection;

pub mod fft;
use fft::fftn_3d;

// Use wee_alloc as the global allocator to strictly bound WebAssembly memory footprint.
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[derive(Serialize, Deserialize)]
pub struct CosmologyParams {
    pub h0: f64,
    pub w0: f64,
    pub wa: f64,
    pub omega_m: f64,
    pub omega_de: f64,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct GalaxyCoord {
    pub x: f64,
    pub y: f64,
    pub z: f64,
}

#[wasm_bindgen]
pub fn compute_comoving_distance(z_val: f64, h0: f64, w0: f64, wa: f64, omega_m: f64, omega_de: f64) -> f64 {
    let steps = 100;
    let mut integrand_sum = 0.0;
    let dz = z_val / steps as f64;
    let c_light = 299792.458; // km/s

    for i in 0..steps {
        let zi = (i as f64) * dz;
        let f_de = ((1.0 + zi).powf(3.0 * (1.0 + w0 + wa))) * (-3.0 * wa * zi / (1.0 + zi)).exp();
        let e_z = (omega_m * (1.0 + zi).powi(3) + omega_de * f_de).sqrt();
        integrand_sum += 1.0 / e_z;
    }

    (c_light / h0) * integrand_sum * dz
}

#[wasm_bindgen]
pub fn solve_asymmetric_3_2_check(coords_json: &str) -> String {
    // Verifies whether clusters align with the S1,2 3:2 asymmetric ratio
    let coords: Vec<GalaxyCoord> = match serde_json::from_str(coords_json) {
        Ok(v) => v,
        Err(_) => return "{\"status\": \"error\", \"message\": \"invalid json\"}".to_string(),
    };

    if coords.len() < 3 {
        return "{\"status\": \"insufficient_data\"}".to_string();
    }

    let mut x_sum = 0.0;
    let mut y_sum = 0.0;
    let mut z_sum = 0.0;
    for c in &coords {
        x_sum += c.x;
        y_sum += c.y;
        z_sum += c.z;
    }
    let n = coords.len() as f64;
    let mean_x = x_sum / n;
    let mean_y = y_sum / n;
    let mean_z = z_sum / n;

    let mut var_x = 0.0;
    let mut var_y = 0.0;
    let mut var_z = 0.0;
    for c in &coords {
        var_x += (c.x - mean_x).powi(2);
        var_y += (c.y - mean_y).powi(2);
        var_z += (c.z - mean_z).powi(2);
    }

    let dev_x = (var_x / n).sqrt();
    let dev_y = (var_y / n).sqrt();
    let dev_z = (var_z / n).sqrt();

    let ratio_xy = if dev_y > 0.0 { dev_x / dev_y } else { 1.0 };
    let delta = (ratio_xy - 1.5).abs();
    let anomaly_score = 1.0 / (1.0 + delta);

    format!(
        "{{\"status\": \"success\", \"variance_ratio\": {:.4}, \"delta\": {:.4}, \"score\": {:.4}}}",
        ratio_xy, delta, anomaly_score
    )
}

#[wasm_bindgen]
pub fn compute_density_field_asymmetry(coords_json: &str, s12: f64, s21: f64) -> String {
    let coords: Vec<GalaxyCoord> = match serde_json::from_str(coords_json) {
        Ok(v) => v,
        Err(_) => return "{\"status\": \"error\", \"message\": \"invalid json\"}".to_string(),
    };

    if coords.len() == 0 {
        return "{\"status\": \"insufficient_data\"}".to_string();
    }

    let n = coords.len() as f64;
    let mut x_sum = 0.0;
    let mut y_sum = 0.0;
    let mut z_sum = 0.0;
    for c in &coords {
        x_sum += c.x;
        y_sum += c.y;
        z_sum += c.z;
    }
    let mean_x = x_sum / n;
    let mean_y = y_sum / n;
    let mean_z = z_sum / n;

    let mut max_val: f64 = 1.0;
    for c in &coords {
        let x_c = (c.x - mean_x).abs();
        if x_c > max_val { max_val = x_c; }
        let y_c = (c.y - mean_y).abs();
        if y_c > max_val { max_val = y_c; }
        let z_c = (c.z - mean_z).abs();
        if z_c > max_val { max_val = z_c; }
    }

    let grid_size: usize = 128;
    let mut grid = vec![Complex::new(0.0f32, 0.0f32); grid_size * grid_size * grid_size];

    let scale = (grid_size as f64 - 1.0) / (max_val * 2.0);

    for c in &coords {
        let mut ix = (((c.x - mean_x) + max_val) * scale) as i64;
        let mut iy = (((c.y - mean_y) + max_val) * scale) as i64;
        let mut iz = (((c.z - mean_z) + max_val) * scale) as i64;

        if ix < 0 { ix = 0; }
        if iy < 0 { iy = 0; }
        if iz < 0 { iz = 0; }
        if ix >= grid_size as i64 { ix = grid_size as i64 - 1; }
        if iy >= grid_size as i64 { iy = grid_size as i64 - 1; }
        if iz >= grid_size as i64 { iz = grid_size as i64 - 1; }

        let flat_idx = ix as usize * grid_size * grid_size + iy as usize * grid_size + iz as usize;
        grid[flat_idx].re += 1.0;
    }

    // Perform 3D FFT
    fftn_3d(&mut grid, grid_size, FftDirection::Forward);

    let exp_05 = Complex::new(0.0f32, 0.5f32).exp();
    let exp_m05 = Complex::new(0.0f32, -0.5f32).exp();

    let c_s12 = Complex::new(s12 as f32, 0.0);
    let c_s21 = Complex::new(s21 as f32, 0.0);

    for i in 0..grid.len() {
        let val = grid[i];
        let s12_field = val * c_s12 * exp_05;
        let s21_field = val * c_s21 * exp_m05;
        grid[i] = s12_field - s21_field;
    }

    // Perform 3D IFFT
    fftn_3d(&mut grid, grid_size, FftDirection::Inverse);

    // Because FFT and IFFT might lack normalization in rustfft, we must normalize IFFT by N^3
    let n3 = (grid_size * grid_size * grid_size) as f32;
    let mut sum_asymmetry = 0.0f32;
    let mut max_asymmetry = 0.0f32;

    for i in 0..grid.len() {
        let abs_val = grid[i].norm() / n3;
        sum_asymmetry += abs_val;
        if abs_val > max_asymmetry {
            max_asymmetry = abs_val;
        }
    }

    let mean_asymmetry = sum_asymmetry / n3;
    let delta = (s12 - s21).abs();

    format!(
        "{{\"status\": \"success\", \"mean_asymmetry\": {:.8}, \"max_asymmetry\": {:.8}, \"delta\": {:.8}}}",
        mean_asymmetry, max_asymmetry, delta
    )
}

// --- ARCHIVE 01 NEAREST NEIGHBOR SEARCH (KD-TREE OPTIMIZED) ---
struct KdNode {
    point: GalaxyCoord,
    left: Option<Box<KdNode>>,
    right: Option<Box<KdNode>>,
    axis: usize,
}

impl KdNode {
    fn build(mut points: Vec<GalaxyCoord>, depth: usize) -> Option<Box<Self>> {
        if points.is_empty() {
            return None;
        }

        let axis = depth % 3;
        points.sort_by(|a, b| {
            let val_a = if axis == 0 { a.x } else if axis == 1 { a.y } else { a.z };
            let val_b = if axis == 0 { b.x } else if axis == 1 { b.y } else { b.z };
            val_a.partial_cmp(&val_b).unwrap_or(std::cmp::Ordering::Equal)
        });

        let median = points.len() / 2;
        let mut left_points = points;
        let mut right_points = left_points.split_off(median);
        let median_point = right_points.remove(0);

        Some(Box::new(KdNode {
            point: median_point,
            left: KdNode::build(left_points, depth + 1),
            right: KdNode::build(right_points, depth + 1),
            axis,
        }))
    }

    fn nearest_neighbor(&self, target: &GalaxyCoord, best: &mut (f64, Option<GalaxyCoord>)) {
        let dx = target.x - self.point.x;
        let dy = target.y - self.point.y;
        let dz = target.z - self.point.z;
        let dist_sq = dx*dx + dy*dy + dz*dz;

        // Skip absolute zero distance self-matches
        if dist_sq > 1e-9 && dist_sq < best.0 {
            best.0 = dist_sq;
            best.1 = Some(self.point.clone());
        }

        let axis_dist = if self.axis == 0 { target.x - self.point.x }
                        else if self.axis == 1 { target.y - self.point.y }
                        else { target.z - self.point.z };

        let (near, far) = if axis_dist < 0.0 {
            (&self.left, &self.right)
        } else {
            (&self.right, &self.left)
        };

        if let Some(ref node) = near {
            node.nearest_neighbor(target, best);
        }

        if axis_dist.powi(2) < best.0 {
            if let Some(ref node) = far {
                node.nearest_neighbor(target, best);
            }
        }
    }
}

#[wasm_bindgen]
pub fn compute_nearest_neighbors_average(coords_json: &str) -> f64 {
    let coords: Vec<GalaxyCoord> = match serde_json::from_str(coords_json) {
        Ok(v) => v,
        Err(_) => return -1.0,
    };

    if coords.len() < 2 {
        return 0.0;
    }

    let root = match KdNode::build(coords.clone(), 0) {
        Some(r) => r,
        None => return -1.0,
    };

    let mut total_distance = 0.0;
    for c in &coords {
        let mut best = (f64::INFINITY, None);
        root.nearest_neighbor(c, &mut best);
        if best.0 < f64::INFINITY {
            total_distance += best.0.sqrt();
        }
    }

    total_distance / (coords.len() as f64)
}

// --- ARCHIVE 02 WEAK GRAVITATIONAL LENSING SHEAR FIELDS ---
fn fft2d(data: &mut [Complex<f32>], n: usize, direction: FftDirection) {
    let mut planner = rustfft::FftPlanner::new();
    let fft = planner.plan_fft(n, direction);

    // Row pass
    for r in 0..n {
        let mut row = vec![Complex::new(0.0, 0.0); n];
        for c in 0..n {
            row[c] = data[r * n + c];
        }
        fft.process(&mut row);
        for c in 0..n {
            data[r * n + c] = row[c];
        }
    }

    // Col pass
    for c in 0..n {
        let mut col = vec![Complex::new(0.0, 0.0); n];
        for r in 0..n {
            col[r] = data[r * n + c];
        }
        fft.process(&mut col);
        for r in 0..n {
            data[r * n + c] = col[r];
        }
    }
}

#[wasm_bindgen]
pub fn compute_weak_lensing_shear_fields(coords_json: &str) -> String {
    let coords: Vec<GalaxyCoord> = match serde_json::from_str(coords_json) {
        Ok(v) => v,
        Err(_) => return "{\"status\": \"error\", \"message\": \"invalid json\"}".to_string(),
    };

    if coords.len() < 10 {
        return "{\"status\": \"insufficient_data\"}".to_string();
    }

    // Project coordinates to 2D Convergence grid kappa (X-Y plane)
    let grid_size = 128;
    let mut kappa = vec![Complex::new(0.0f32, 0.0f32); grid_size * grid_size];

    let mut x_min = f64::INFINITY;
    let mut x_max = f64::NEG_INFINITY;
    let mut y_min = f64::INFINITY;
    let mut y_max = f64::NEG_INFINITY;

    for c in &coords {
        if c.x < x_min { x_min = c.x; }
        if c.x > x_max { x_max = c.x; }
        if c.y < y_min { y_min = c.y; }
        if c.y > y_max { y_max = c.y; }
    }

    let x_span = if x_max > x_min { x_max - x_min } else { 1.0 };
    let y_span = if y_max > y_min { y_max - y_min } else { 1.0 };

    for c in &coords {
        let ix = (((c.x - x_min) / x_span) * (grid_size as f64 - 1.0)) as usize;
        let iy = (((c.y - y_min) / y_span) * (grid_size as f64 - 1.0)) as usize;
        let flat_idx = iy * grid_size + ix;
        kappa[flat_idx].re += 1.0;
    }

    // Forward 2D FFT to get Convergence in Fourier Space
    fft2d(&mut kappa, grid_size, FftDirection::Forward);

    let mut gamma1 = vec![Complex::new(0.0f32, 0.0f32); grid_size * grid_size];
    let mut gamma2 = vec![Complex::new(0.0f32, 0.0f32); grid_size * grid_size];

    for u in 0..grid_size {
        let kx = if u < grid_size / 2 { u as f32 } else { (u as i32 - grid_size as i32) as f32 };
        for v in 0..grid_size {
            let ky = if v < grid_size / 2 { v as f32 } else { (v as i32 - grid_size as i32) as f32 };
            let k_sq = kx*kx + ky*ky;
            let flat_idx = u * grid_size + v;

            if k_sq > 0.0 {
                let factor1 = (kx*kx - ky*ky) / k_sq;
                let factor2 = (2.0 * kx * ky) / k_sq;
                gamma1[flat_idx] = kappa[flat_idx] * factor1;
                gamma2[flat_idx] = kappa[flat_idx] * factor2;
            } else {
                gamma1[flat_idx] = Complex::new(0.0, 0.0);
                gamma2[flat_idx] = Complex::new(0.0, 0.0);
            }
        }
    }

    // Inverse 2D FFT
    fft2d(&mut gamma1, grid_size, FftDirection::Inverse);
    fft2d(&mut gamma2, grid_size, FftDirection::Inverse);

    let norm_factor = (grid_size * grid_size) as f32;
    let mut mean_shear_1 = 0.0;
    let mut mean_shear_2 = 0.0;
    let mut max_shear_1 = 0.0;
    let mut max_shear_2 = 0.0;

    for i in 0..(grid_size * grid_size) {
        let g1 = (gamma1[i].re / norm_factor).abs();
        let g2 = (gamma2[i].re / norm_factor).abs();

        mean_shear_1 += g1;
        mean_shear_2 += g2;

        if g1 > max_shear_1 { max_shear_1 = g1; }
        if g2 > max_shear_2 { max_shear_2 = g2; }
    }

    let n2 = (grid_size * grid_size) as f32;
    let mean_1 = mean_shear_1 / n2;
    let mean_2 = mean_shear_2 / n2;

    // Asymmetric lensing detection criteria to sweep for Chameleon Gravitino knots
    let has_chameleon_knot = (max_shear_1 > 5.0 * mean_1 && max_shear_2 > 5.0 * mean_2) 
        || (max_shear_1 > 10.0 * mean_1);

    format!(
        "{{\"status\": \"success\", \"mean_shear_1\": {:.8}, \"mean_shear_2\": {:.8}, \"max_shear_1\": {:.8}, \"max_shear_2\": {:.8}, \"has_chameleon_knot\": {}}}",
        mean_1, mean_2, max_shear_1, max_shear_2, has_chameleon_knot
    )
}


