importScripts('../../public/wasm/core_wasm.js');

let wasmInitPromise = null;

self.onmessage = async function(e) {
    const { type, data } = e.data;
    
    if (type === 'INIT') {
        try {
            wasmInitPromise = wasm_bindgen('../../public/wasm/core_wasm_bg.wasm');
            await wasmInitPromise;
            self.postMessage({ type: 'INIT_DONE' });
        } catch (err) {
            self.postMessage({ type: 'COMPUTE_ERROR', error: err.message });
        }
    } else if (type === 'COMPUTE_CHUNK') {
        try {
            if (!wasmInitPromise) throw new Error("WASM not initialized");
            await wasmInitPromise;
            
            const start = performance.now();
            const coordsStr = JSON.stringify(data.coords);
            
            // Core K3 Asymmetry
            const k3ResultStr = wasm_bindgen.compute_density_field_asymmetry(coordsStr, data.s12 || 1.6, data.s21 || 0.5);
            const k3Result = JSON.parse(k3ResultStr);

            // KD-Tree Nearest Neighbors
            const avgNeighborDist = wasm_bindgen.compute_nearest_neighbors_average(coordsStr);

            // Weak Lensing Shear Fields
            const shearResultStr = wasm_bindgen.compute_weak_lensing_shear_fields(coordsStr);
            const shearResult = JSON.parse(shearResultStr);

            const computeTime = performance.now() - start;
            
            self.postMessage({
                type: 'COMPUTE_DONE',
                result: { 
                    ...k3Result,
                    avg_neighbor_dist: avgNeighborDist,
                    shear: shearResult,
                    computeTime 
                }
            });
        } catch (error) {
            self.postMessage({ type: 'COMPUTE_ERROR', error: error.message });
        }
    }
};
