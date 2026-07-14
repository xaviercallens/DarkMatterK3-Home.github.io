use num_complex::Complex;
use rustfft::{FftPlanner, FftDirection};
use std::sync::Arc;

pub fn fftn_3d(data: &mut [Complex<f32>], n: usize, direction: FftDirection) {
    let mut planner = FftPlanner::new();
    let fft = planner.plan_fft(n, direction);

    // X-pass
    for y in 0..n {
        for z in 0..n {
            let mut row = vec![Complex::new(0.0, 0.0); n];
            for x in 0..n {
                row[x] = data[x * n * n + y * n + z];
            }
            fft.process(&mut row);
            for x in 0..n {
                data[x * n * n + y * n + z] = row[x];
            }
        }
    }

    // Y-pass
    for x in 0..n {
        for z in 0..n {
            let mut row = vec![Complex::new(0.0, 0.0); n];
            for y in 0..n {
                row[y] = data[x * n * n + y * n + z];
            }
            fft.process(&mut row);
            for y in 0..n {
                data[x * n * n + y * n + z] = row[y];
            }
        }
    }

    // Z-pass
    for x in 0..n {
        for y in 0..n {
            let mut row = vec![Complex::new(0.0, 0.0); n];
            for z in 0..n {
                row[z] = data[x * n * n + y * n + z];
            }
            fft.process(&mut row);
            for z in 0..n {
                data[x * n * n + y * n + z] = row[z];
            }
        }
    }
}
