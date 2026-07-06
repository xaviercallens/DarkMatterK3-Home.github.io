// core_wasm/src/lib.rs
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct CosmologyParams {
    pub h0: f64,
    pub w0: f64,
    pub wa: f64,
    pub omega_m: f64,
    pub omega_de: f64,
}

#[derive(Serialize, Deserialize)]
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
    // Parse input coordinates
    let coords: Vec<GalaxyCoord> = match serde_json::from_str(coords_json) {
        Ok(v) => v,
        Err(_) => return "{\"status\": \"error\", \"message\": \"invalid json\"}".to_string(),
    };

    if coords.len() < 3 {
        return "{\"status\": \"insufficient_data\"}".to_string();
    }

    // Measure spatial asymmetry
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

    // 3:2 cosmic ratio checker
    let ratio_xy = if dev_y > 0.0 { dev_x / dev_y } else { 1.0 };
    let delta = (ratio_xy - 1.5).abs();
    let anomaly_score = 1.0 / (1.0 + delta);

    format!(
        "{{\"status\": \"success\", \"variance_ratio\": {:.4}, \"delta\": {:.4}, \"score\": {:.4}}}",
        ratio_xy, delta, anomaly_score
    )
}
