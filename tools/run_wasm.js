const fs = require('fs');

async function main() {
    const core_wasm = require('../core_wasm/pkg/core_wasm.js');

    const inputData = fs.readFileSync(0, 'utf-8');
    const input = JSON.parse(inputData);

    const coords_json = JSON.stringify(input.coords);
    
    // Call the WASM function
    const result_json = core_wasm.compute_density_field_asymmetry(coords_json, input.s12, input.s21);
    
    console.log(result_json);
}

main().catch(console.error);
