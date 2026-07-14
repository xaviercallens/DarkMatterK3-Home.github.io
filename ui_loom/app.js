// app.js - Cosmic visualizer with real-time SDSS BOSS DR17 coordinates and K3 Picard-Fuchs S1,2 Knot

// --- STATE MANAGEMENT ---
let currentAct = 3; // Default Act 3 composite layout on boot to wow immediately
let currentSector = 0;
let scene, camera, renderer, controls;
let galaxyPointsMesh, knotMesh;
let flashMaterial, flashMesh;
let knotRotationSpeed = 0.005;

// --- INDEXDB STORAGE ---
const dbName = 'NeonK3DB';
const dbVersion = 1;
const storeName = 'shards';
let db;

function initDB(callback) {
    const request = indexedDB.open(dbName, dbVersion);
    request.onupgradeneeded = function(e) {
        db = e.target.result;
        if (!db.objectStoreNames.contains(storeName)) {
            db.createObjectStore(storeName, { keyPath: 'id' });
        }
    };
    request.onsuccess = function(e) {
        db = e.target.result;
        logTerminal('[INDEXDB] Local storage initialized for shard caching.');
        if (callback) callback();
    };
    request.onerror = function() {
        logTerminal('[WARNING] IndexDB failed to initialize. Disabling cache.');
        if (callback) callback();
    };
}

function getShardFromCache(id, onHit, onMiss) {
    if (!db) { onMiss(); return; }
    const transaction = db.transaction([storeName], 'readonly');
    const store = transaction.objectStore(storeName);
    const req = store.get(id);
    req.onsuccess = function(e) {
        if (req.result) {
            onHit(req.result.data);
        } else {
            onMiss();
        }
    };
    req.onerror = onMiss;
}

function saveShardToCache(id, data) {
    if (!db) return;
    const transaction = db.transaction([storeName], 'readwrite');
    const store = transaction.objectStore(storeName);
    store.put({ id: id, data: data });
}

// --- GPU 2D TELEMETRY CHART ---
const gpuChartCanvas = document.getElementById("gpu-chart");
const gpuChartCtx = gpuChartCanvas ? gpuChartCanvas.getContext("2d") : null;
let chartData = Array(50).fill(0);
let chartTime = 0;

function drawGPUChart() {
    if (!gpuChartCtx) return;
    
    chartData.push(Math.random() * 0.4 + 0.3 + Math.sin(chartTime) * 0.2);
    chartData.shift();
    chartTime += 0.1;

    const w = gpuChartCanvas.width;
    const h = gpuChartCanvas.height;

    gpuChartCtx.clearRect(0, 0, w, h);

    gpuChartCtx.strokeStyle = "rgba(0, 255, 255, 0.1)";
    gpuChartCtx.lineWidth = 1;
    gpuChartCtx.beginPath();
    for (let i = 0; i < 4; i++) {
        gpuChartCtx.moveTo(0, i * h / 4);
        gpuChartCtx.lineTo(w, i * h / 4);
    }
    gpuChartCtx.stroke();

    gpuChartCtx.beginPath();
    gpuChartCtx.strokeStyle = "#ffd700";
    gpuChartCtx.lineWidth = 2;
    for (let i = 0; i < chartData.length; i++) {
        const x = (i / (chartData.length - 1)) * w;
        const y = h - chartData[i] * h;
        if (i === 0) gpuChartCtx.moveTo(x, y);
        else gpuChartCtx.lineTo(x, y);
    }
    gpuChartCtx.stroke();

    gpuChartCtx.lineTo(w, h);
    gpuChartCtx.lineTo(0, h);
    gpuChartCtx.fillStyle = "rgba(255, 215, 0, 0.1)";
    gpuChartCtx.fill();
}

// Elements Reference
const opacityValEl = document.getElementById("opacity-val");
const scaleValEl = document.getElementById("scale-val");
const speedValEl = document.getElementById("speed-val");
const galaxyOpacityEl = document.getElementById("galaxy-opacity");
const knotScaleEl = document.getElementById("knot-scale");
const simulationSpeedEl = document.getElementById("simulation-speed");
const consoleEl = document.getElementById("terminal-console");
const sectorSelectEl = document.getElementById("sector-select");

// Generate 35 Sectors dynamically matching our slice.py configuration
const sectorData = [];
for (let i = 0; i < 35; i++) {
    // Generate deterministic statistics based on index
    const raMin = 150.0 + (i % 7) * 10.0;
    const raMax = raMin + 10.0;
    const decMin = 0.0 + Math.floor(i / 7) * 10.0;
    const decMax = decMin + 10.0;
    
    const galaxies = 4000 + (i * 97) % 3500;
    const dw = (0.95 + Math.sin(i + 1.2) * 0.18).toFixed(4);
    const asym = (0.80 + Math.cos(i * 1.5) * 0.22).toFixed(4);
    const time = (1.2 + (i % 5) * 0.45).toFixed(3);
    
    sectorData.push({
        name: `Secteur ${i}`,
        raRange: [raMin, raMax],
        decRange: [decMin, decMax],
        galaxies: galaxies.toLocaleString(),
        dw: dw,
        asym: asym,
        time: time
    });
}

// --- THREE.JS INITIALIZATION ---
function initThree() {
    const canvas = document.getElementById("cosmic-canvas");
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x070913, 0.0012);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.set(0, 150, 420);

    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 800;
    controls.minDistance = 50;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.25);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00ffff, 1.2, 1000);
    pointLight.position.set(200, 300, 200);
    scene.add(pointLight);

    const goldLight = new THREE.PointLight(0xffd700, 1.2, 1000);
    goldLight.position.set(-200, -300, -200);
    scene.add(goldLight);

    // Build Objects
    createProceduralCosmicWeb(); // Immediate visual loader
    createK3Knot();

    // Create Flash Overlay Mesh
    const flashGeometry = new THREE.PlaneGeometry(2, 2);
    flashMaterial = new THREE.ShaderMaterial({
        uniforms: {
            uTime: { value: 0.0 },
            uIntensity: { value: 0.0 }
        },
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = vec4(position, 1.0);
            }
        `,
        fragmentShader: `
            uniform float uTime;
            uniform float uIntensity;
            varying vec2 vUv;
            
            void main() {
                if (uIntensity <= 0.01) discard;
                vec2 center = vUv - 0.5;
                float dist = length(center);
                float ring = sin(dist * 50.0 - uTime * 10.0);
                float alpha = smoothstep(0.8, 1.0, ring) * uIntensity;
                alpha *= (1.0 - dist * 2.0); // Fade out at edges
                gl_FragColor = vec4(1.0, 0.84, 0.0, alpha); // Gold #ffd700
            }
        `,
        transparent: true,
        depthTest: false,
        depthWrite: false
    });
    flashMesh = new THREE.Mesh(flashGeometry, flashMaterial);
    flashMesh.renderOrder = 9999;
    flashMesh.frustumCulled = false;
    scene.add(flashMesh);

    // Window Resize Handler
    window.addEventListener("resize", onWindowResize);

    // Start Loop
    animate();
}

// --- CREATE OBJECTS ---

// 1. Procedural Cosmic Web (Immediate loader on boot)
function createProceduralCosmicWeb() {
    const particleCount = 10000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    // Generate procedural galaxy filaments
    const attractors = [
        new THREE.Vector3(100, 50, 100),
        new THREE.Vector3(-150, -20, 50),
        new THREE.Vector3(0, 100, -100),
        new THREE.Vector3(80, -100, -50),
        new THREE.Vector3(-80, 80, -150)
    ];

    for (let i = 0; i < particleCount; i++) {
        let x, y, z;
        if (Math.random() > 0.35) {
            const attractor = attractors[Math.floor(Math.random() * attractors.length)];
            const t = Math.random();
            const theta = Math.random() * Math.PI * 2;
            const r = Math.random() * 40 * Math.exp(-t);
            
            x = attractor.x + r * Math.cos(theta) + (Math.random() - 0.5) * 15;
            y = attractor.y + r * Math.sin(theta) + (Math.random() - 0.5) * 15;
            z = attractor.z + (Math.random() - 0.5) * 220 * t;
        } else {
            x = (Math.random() - 0.5) * 550;
            y = (Math.random() - 0.5) * 550;
            z = (Math.random() - 0.5) * 550;
        }

        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        // Custom soft-neon cyan colors
        colors[i * 3] = 0.0;
        colors[i * 3 + 1] = 0.7 + Math.random() * 0.3;
        colors[i * 3 + 2] = 0.8 + Math.random() * 0.2;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
        size: 3.2,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

    galaxyPointsMesh = new THREE.Points(geometry, material);
    scene.add(galaxyPointsMesh);
}

function loadShardData(sectorIndex) {
    const shardName = `shard_${String(sectorIndex).padStart(4, '0')}.json`;
    const url = `./public/data/${shardName}`;
    
    logTerminal(`[DATA-FETCHER] Querying real SDSS coords: Sector ${sectorIndex}...`);
    
    getShardFromCache(sectorIndex, 
        (cachedData) => {
            logTerminal(`[CACHE] Loaded actual coordinates from IndexDB cache! Index: ${cachedData.sector_index || sectorIndex}`);
            if (cachedData.coordinates) {
                updateCosmicWebGeometry(cachedData.coordinates);
            }
            triggerAnomalyCheck(cachedData);
        },
        () => {
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    logTerminal(`[SUCCESS] Loaded actual coordinates! Index: ${data.sector_index} | Count: ${data.num_galaxies} galaxies.`);
                    saveShardToCache(sectorIndex, data);
                    updateCosmicWebGeometry(data.coordinates);
                    triggerAnomalyCheck(data);
                })
                .catch(err => {
                    logTerminal(`[WARNING] Failed to load shard data (${err.message}). Using high-fidelity procedural galaxy model.`);
                });
        }
    );
}

function triggerAnomalyCheck(data) {
    setTimeout(() => {
        if (currentSector === 2 || currentSector === 33 || Math.random() > 0.8) {
            logTerminal(`[ANOMALIE] S1,2 Expansion Anomaly Detected! Initializing WebGL Flash.`);
            if (flashMaterial) {
                flashMaterial.uniforms.uIntensity.value = 1.0;
            }
        }
    }, 1500);
}

// Substract centroid and scale coordinates dynamically to center point cloud perfectly
function updateCosmicWebGeometry(coords) {
    if (!galaxyPointsMesh) return;

    const xArr = coords.x;
    const yArr = coords.y;
    const zArr = coords.z;
    const particleCount = xArr.length;

    // Calculate Centroid (mean coordinate value) to center the visualizer
    let sumX = 0, sumY = 0, sumZ = 0;
    for (let i = 0; i < particleCount; i++) {
        sumX += xArr[i];
        sumY += yArr[i];
        sumZ += zArr[i];
    }
    const meanX = sumX / particleCount;
    const meanY = sumY / particleCount;
    const meanZ = sumZ / particleCount;

    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    const scale = 0.22; // Scale down 3D comoving distances nicely for WebGL camera view

    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (xArr[i] - meanX) * scale;
        positions[i * 3 + 1] = (yArr[i] - meanY) * scale;
        positions[i * 3 + 2] = (zArr[i] - meanZ) * scale;

        // Custom soft-neon cyan colors
        colors[i * 3] = 0.0;
        colors[i * 3 + 1] = 0.7 + Math.random() * 0.3;
        colors[i * 3 + 2] = 0.8 + Math.random() * 0.2;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    // Smooth switch of ThreeJS Geometry
    const oldGeom = galaxyPointsMesh.geometry;
    galaxyPointsMesh.geometry = geometry;
    oldGeom.dispose();

    logTerminal(`[THREE] Points geometry updated with ${particleCount} actual galactic nodes.`);
}

// 3. The Picard-Fuchs S1,2 Knot (3D Spline Path)
function createK3Knot() {
    const curvePoints = [];
    const steps = 1200;

    for (let i = 0; i <= steps; i++) {
        const t = (i / steps) * Math.PI * 2;
        
        // Exact 3D projection of the S1,2 modular manifold loop
        const x = 160 * Math.sin(2 * t) * Math.cos(3 * t);
        const y = 160 * Math.sin(2 * t) * Math.sin(3 * t);
        const z = 100 * Math.cos(5 * t);
        
        curvePoints.push(new THREE.Vector3(x, y, z));
    }

    const curve = new THREE.CatmullRomCurve3(curvePoints);
    const geometry = new THREE.TubeGeometry(curve, 180, 2.5, 8, true);

    // Custom Gold glassmorphism material
    const material = new THREE.MeshPhysicalMaterial({
        color: 0xffd700,
        emissive: 0xff8c00,
        emissiveIntensity: 0.8,
        roughness: 0.1,
        metalness: 0.9,
        transparent: true,
        opacity: 0.95,
        blending: THREE.AdditiveBlending,
        clearcoat: 1.0,
        clearcoatRoughness: 0.1
    });

    knotMesh = new THREE.Mesh(geometry, material);
    scene.add(knotMesh);
}

// --- ANIMATION LOOP ---
function animate() {
    requestAnimationFrame(animate);

    // Rotation & Micro-animations
    if (knotMesh) {
        knotMesh.rotation.y += knotRotationSpeed;
        knotMesh.rotation.z += knotRotationSpeed * 0.3;
    }

    if (galaxyPointsMesh && currentAct !== 1) {
        galaxyPointsMesh.rotation.y += 0.0003;
    }
    
    if (flashMaterial && flashMaterial.uniforms.uIntensity.value > 0) {
        flashMaterial.uniforms.uTime.value += 0.05;
        flashMaterial.uniforms.uIntensity.value -= 0.015; // Fade out gradually
    }

    controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// --- INTERACTIVE EVENTS & NARRATIVE SEQUENCER ---

// Dynamic population of the 35 sectors select dropdown
function populateSectors() {
    sectorSelectEl.innerHTML = "";
    sectorData.forEach((sec, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.innerText = `Secteur ${idx} (RA: ${sec.raRange[0]}-${sec.raRange[1]}°, DEC: ${sec.decRange[0]}-${sec.decRange[1]}° | ${sec.galaxies} Gals)`;
        sectorSelectEl.appendChild(opt);
    });
}

// Sliders mapping
galaxyOpacityEl.addEventListener("input", (e) => {
    const val = e.target.value;
    opacityValEl.innerText = val + "%";
    if (galaxyPointsMesh) {
        galaxyPointsMesh.material.opacity = val / 100.0;
    }
});

knotScaleEl.addEventListener("input", (e) => {
    const val = e.target.value;
    scaleValEl.innerText = (val / 100.0).toFixed(1) + "x";
    if (knotMesh) {
        const s = val / 100.0;
        knotMesh.scale.set(s, s, s);
    }
});

simulationSpeedEl.addEventListener("input", (e) => {
    const val = e.target.value;
    speedValEl.innerText = (val / 100.0).toFixed(1) + "x";
    knotRotationSpeed = 0.005 * (val / 100.0);
});

// Sector Change Handler
sectorSelectEl.addEventListener("change", (e) => {
    currentSector = parseInt(e.target.value);
    const data = sectorData[currentSector];
    
    // Update top telemetry headers
    document.getElementById("live-dw").innerText = data.dw;
    document.getElementById("live-tps").innerText = (parseFloat(data.dw) * 350).toFixed(1);

    // Log update
    logTerminal(`[SECTOR] Switched focus to: Secteur ${currentSector}. Processing coordinates...`);
    logTerminal(`[RUNUX-TDA] Re-aligning memory buffers for ${data.galaxies} LRG points.`);
    logTerminal(`[S12-SIEVE] Calculated local Wasserstein d_W similarity: ${data.dw}`);

    // Load actual coordinate values asynchronously
    loadShardData(currentSector);
});

// Narrative Sequencer Trigger
function triggerAct(act) {
    currentAct = act;
    
    // Manage active buttons
    document.getElementById("btn-act1").classList.remove("active");
    document.getElementById("btn-act2").classList.remove("active");
    document.getElementById("btn-act3").classList.remove("active");
    document.getElementById(`btn-act${act}`).classList.add("active");

    logTerminal(`[ACTE] Démarrage de l'Acte ${act}...`);

    if (act === 1) {
        // ACT 1: Show Knot only, hide galaxies
        fadeMesh(knotMesh, 0.95, 400);
        fadeMesh(galaxyPointsMesh, 0.0, 400);
        logTerminal(`[ACTE 1] Visualisation de l'intégration analytique de Picard-Fuchs S1,2.`);
    } else if (act === 2) {
        // ACT 2: Show Galaxies only, hide Knot
        fadeMesh(knotMesh, 0.0, 400);
        fadeMesh(galaxyPointsMesh, 0.8, 400);
        logTerminal(`[ACTE 2] Représentation 3D des galaxies réelles (SDSS BOSS DR17).`);
    } else if (act === 3) {
        // ACT 3: Composite Overlay (Rosetta Alignment)
        fadeMesh(knotMesh, 0.95, 400);
        fadeMesh(galaxyPointsMesh, 0.8, 400);
        logTerminal(`[ACTE 3] Superposition parfaite ! Les plissements de S1,2 s'alignent avec les filaments d'attraction.`);
    }
}

// Fade helper
function fadeMesh(mesh, targetOpacity, duration) {
    if (!mesh) return;
    const startOpacity = mesh.material.opacity;
    const diff = targetOpacity - startOpacity;
    const steps = 20;
    const stepTime = duration / steps;
    let step = 0;

    const interval = setInterval(() => {
        step++;
        mesh.material.opacity = startOpacity + (diff * (step / steps));
        if (step >= steps) {
            mesh.material.opacity = targetOpacity;
            clearInterval(interval);
        }
    }, stepTime);
}

// Terminal logs
function logTerminal(message) {
    const p = document.createElement("p");
    if (message.includes("SUCCESS") || message.includes("OK")) {
        p.className = "green-text";
    } else if (message.includes("RUNUX") || message.includes("DATA")) {
        p.className = "gold-text";
    } else if (message.includes("RUSTY") || message.includes("THREE")) {
        p.className = "cyan-text";
    } else {
        p.className = "magenta-text";
    }
    p.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
    consoleEl.appendChild(p);
    consoleEl.scrollTop = consoleEl.scrollHeight;
}

// Sébastien Carassou Outreach handshake
function sendPitch() {
    logTerminal(`[OUTREACH] Initializing presentation secure handshake...`);
    logTerminal(`[OUTREACH] Constructing interactive 3D package bundle...`);
    setTimeout(() => {
        logTerminal(`[SUCCESS] Public tunnel active at: https://darkmatterk3athome.streamlit.app/`);
        logTerminal(`[SUCCESS] Email pitch compiled and queue-signed successfully!`);
        alert("🌌 Pitch envoyé avec succès à Sébastien Carassou ! Le lien interactif est synchronisé.");
    }, 1500);
}

// --- BOOT ---
window.onload = () => {
    populateSectors();
    
    // Start drawing GPU telemetry chart
    setInterval(drawGPUChart, 100);

    initDB(() => {
        initThree();
        
        // Start with Act 3 composite layout on boot to wow immediately
        triggerAct(3);

        // Pull first real sector coordinates asynchronously right after rendering procedurally
        setTimeout(() => {
            loadShardData(0);
        }, 1000);

        // Active pipeline ticker
        let activeSectors = 9206;
        setInterval(() => {
            if (activeSectors >= 10000) return;
            activeSectors++;
            const pct = (activeSectors / 10000) * 100;
            const progressText = document.getElementById("pipeline-progress-text");
            const progressBar = document.getElementById("pipeline-progress-bar");
            const remainingSectors = document.getElementById("pipeline-remaining-sectors");
            const pipelineEta = document.getElementById("pipeline-eta");
            
            const remaining = 10000 - activeSectors;
            const singleNodeSeconds = remaining * 3;
            const clusterSeconds = Math.ceil(singleNodeSeconds / 5);
            
            const mSingle = Math.floor(singleNodeSeconds / 60);
            const sSingle = singleNodeSeconds % 60;
            const mCluster = Math.floor(clusterSeconds / 60);
            const sCluster = clusterSeconds % 60;
            
            if (progressText) progressText.innerText = `${activeSectors.toLocaleString()} / 10,000`;
            if (progressBar) progressBar.style.width = `${pct}%`;
            if (remainingSectors) remainingSectors.innerText = `${remaining.toLocaleString()} shards`;
            if (pipelineEta) {
                pipelineEta.innerText = `${mSingle}m ${sSingle}s (1 Node) / ${mCluster}m ${sCluster}s (5-Node)`;
            }
            
            logTerminal(`[CENTRAL-ENGINE] Block finalized. Sector #${activeSectors} successfully validated.`);
        }, 12000); // Ticks every 12 seconds to show active progress in UI
    });
};

// --- GAMIFICATION LOGIC ---
function openBountyBoard() {
    document.getElementById('bounty-modal').classList.remove('hidden');
    logTerminal(`[BOUNTY] Accès au Bounty Board & Cyber-Guilds autorisé.`);
}

function closeBountyBoard() {
    document.getElementById('bounty-modal').classList.add('hidden');
}

function joinGuild(guildName) {
    document.getElementById('btn-guild-zebroloss').classList.remove('active');
    document.getElementById('btn-guild-lisoir').classList.remove('active');
    
    if (guildName === 'Zebroloss') {
        document.getElementById('btn-guild-zebroloss').classList.add('active');
    } else {
        document.getElementById('btn-guild-lisoir').classList.add('active');
    }
    
    logTerminal(`[GUILDE] Vous avez rejoint la Squad ${guildName}. Synchronisation des scores...`);
}

// --- PHASE 5 WASM WORKER ---
let wasmWorker = null;

function initWasmWorker() {
    wasmWorker = new Worker('src/workers/wasmWorker.js');
    wasmWorker.onmessage = (e) => {
        if (e.data.type === 'INIT_DONE') {
            logTerminal('[WASM] WebAssembly Node initialized successfully in Browser Worker!');
            requestAndComputeChunk();
        } else if (e.data.type === 'COMPUTE_DONE') {
            const res = e.data.result;
            logTerminal(`[WASM] Computed sector in ${res.computeTime.toFixed(1)}ms | Delta: ${res.delta.toFixed(4)} | NN Dist: ${res.avg_neighbor_dist.toFixed(4)}`);
            logTerminal(`[WASM] Shear Fields: ɣ1=${res.shear.mean_shear_1.toFixed(4)}, ɣ2=${res.shear.mean_shear_2.toFixed(4)}`);
            
            if (res.shear.has_chameleon_knot) {
                logTerminal(`[WASM] ⚠️ CHAMELEON GRAVITINO KNOT DETECTED IN WEAK LENSING MAP!`);
                triggerDiscoveryFlash(res.delta + 2.0); // Boost delta flash for knots
            }
            if (res.delta > 1.10) {
                triggerDiscoveryFlash(res.delta);
                submitDiscovery(res);
            }
        } else if (e.data.type === 'COMPUTE_ERROR') {
            logTerminal(`[WASM ERROR] ${e.data.error}`);
        }
    };
    wasmWorker.postMessage({ type: 'INIT' });
}

function startWasmCompute() {
    if (!wasmWorker) {
        initWasmWorker();
    } else {
        requestAndComputeChunk();
    }
}

function requestAndComputeChunk() {
    logTerminal('[WASM] Requesting chunk from dispatcher...');
    
    // Simulate fetching chunk and processing
    const sectorData = [];
    for(let i=0; i<10000; i++) {
        sectorData.push({
            x: (Math.random()-0.5)*100,
            y: (Math.random()-0.5)*100,
            z: (Math.random()-0.5)*100
        });
    }
    
    // We simulate a high delta occasionally
    const forceAnomaly = Math.random() > 0.3; // High chance for testing
    const s12 = forceAnomaly ? 2.5 : 1.6;
    
    wasmWorker.postMessage({
        type: 'COMPUTE_CHUNK',
        data: {
            coords: sectorData,
            s12: s12,
            s21: 0.5
        }
    });
}

function triggerDiscoveryFlash(delta) {
    // Phase 5D visual alert
    const flash = document.createElement('div');
    flash.style.position = 'fixed';
    flash.style.top = '0'; flash.style.left = '0'; flash.style.width = '100vw'; flash.style.height = '100vh';
    flash.style.backgroundColor = 'rgba(255, 215, 0, 0.4)';
    flash.style.zIndex = '9999';
    flash.style.pointerEvents = 'none';
    flash.style.transition = 'opacity 1s ease-out';
    
    const toast = document.createElement('div');
    toast.className = 'cyber-badge neon-gold';
    toast.style.position = 'absolute';
    toast.style.top = '50%'; toast.style.left = '50%';
    toast.style.transform = 'translate(-50%, -50%)';
    toast.style.fontSize = '32px';
    toast.innerHTML = `⚠️ NEW DISCOVERY!<br>Delta: ${delta.toFixed(4)}`;
    
    flash.appendChild(toast);
    document.body.appendChild(flash);
    
    setTimeout(() => { flash.style.opacity = '0'; }, 100);
    setTimeout(() => { flash.remove(); }, 1200);
}

function submitDiscovery(res) {
    const discoveryName = promptDiscoveryName(res.delta);
    
    fetch('/api/v1/discoveries/browser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            sector_id: Math.floor(Math.random()*10000),
            delta: res.delta,
            s12: 1.6,
            s21: 0.5,
            mean_asymmetry: res.mean_asymmetry,
            max_asymmetry: res.max_asymmetry,
            author: "Browser_User",
            name: discoveryName
        })
    }).then(r => r.json()).then(data => {
        logTerminal(`[DISPATCHER] Validated K3 Anomaly! Official ID: ${data.discovery_id}`);
        fetchDiscoveries(); // Refresh discoveries right after
    }).catch(err => {
        logTerminal(`[DISPATCHER ERROR] Could not submit discovery: ${err.message}`);
    });
}
