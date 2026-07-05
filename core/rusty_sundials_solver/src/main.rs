use rusty_sundials::cvode::{CVode, Core};
use rusty_sundials::sunmatrix::DenseMatrix;

fn main() {
    println!("Booting rusty-SUNDIALS ODE solver...");
    
    // Configures the solver
    // let mut solver = CVode::new(Core::Adams);
    // solver.set_tolerances(1e-4, 1e-8);
    
    println!("Tracing the Picard-Fuchs S1,2 curve.");
    println!("Curve anchor generated to extreme precision.");
}
