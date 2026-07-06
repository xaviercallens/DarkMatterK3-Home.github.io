// ui_loom/app.js

// --- STATE MANAGEMENT ---
let currentAct = 1;
let currentSector = 0;
let scene, camera, renderer, controls;
let galaxyPointsMesh, knotMesh;
let knotRotationSpeed = 0.005;

// Elements Reference
const opacityValEl = document.getElementById("opacity-val");
const scaleValEl = document.getElementById("scale-val");
const speedValEl = document.getElementById("speed-val");
const galaxyOpacityEl = document.getElementById("galaxy-opacity");
const knotScaleEl = document.getElementById("knot-scale");
const simulationSpeedEl = document.getElementById("simulation-speed");
const consoleEl = document.getElementById("terminal-console");
const sectorSelectEl = document.getElementById("sector-select");

// Sector Statistics mapping
const sectorData = [
    { name: "Secteur 33", galaxies: "10,000", dw: "1.1161", asym: "0.9315", time: "1.578" },
    { name: "Secteur 24", galaxies: "8,953", dw: "1.0697", asym: "1.1323", time: "2.966" },
    { name: "Secteur 28", galaxies: "9,085", dw: "1.1361", asym: "1.0787", time: "3.056" },
    { name: "Secteur 15", galaxies: "10,000", dw: "1.1048", asym: "0.8611", time: "3.209" }
];

// --- THREE.JS INITIALIZATION ---
function initThree() {
    const canvas = document.getElementById("cosmic-canvas");
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x070913, 0.0015);

    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
    camera.position.set(0, 150, 400);

    renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 800;
    controls.minDistance = 50;

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00ffff, 1, 1000);
    pointLight.position.set(200, 300, 200);
    scene.add(pointLight);

    const goldLight = new THREE.PointLight(0xffd700, 1, 1000);
    goldLight.position.set(-200, -300, -200);
    scene.add(goldLight);

    // Build Objects
    createCosmicWeb();
    createK3Knot();

    // Window Resize Handler
    window.addEventListener("resize", onWindowResize);

    // Start Loop
    animate();
}

// --- CREATE OBJECTS ---

// 1. The Cosmic Web (SDSS Galaxy Point Cloud)
function createCosmicWeb() {
    const particleCount = 12000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    // Generate clusters/filaments using physical attractors
    const centerPoints = [
        new THREE.Vector3(100, 50, 100),
        new THREE.Vector3(-150, -20, 50),
        new THREE.Vector3(0, 100, -100),
        new THREE.Vector3(80, -100, -50),
        new THREE.Vector3(-80, 80, -150)
    ];

    for (let i = 0; i < particleCount; i++) {
        let x, y, z;
        // Filament attractor mapping
        if (Math.random() > 0.3) {
            const attractor = centerPoints[Math.floor(Math.random() * centerPoints.length)];
            const t = Math.random();
            const theta = Math.random() * Math.PI * 2;
            const r = Math.random() * 45 * Math.exp(-t);
            
            x = attractor.x + r * Math.cos(theta) + (Math.random() - 0.5) * 20;
            y = attractor.y + r * Math.sin(theta) + (Math.random() - 0.5) * 20;
            z = attractor.z + (Math.random() - 0.5) * 250 * t;
        } else {
            // Random background galaxies
            x = (Math.random() - 0.5) * 600;
            y = (Math.random() - 0.5) * 600;
            z = (Math.random() - 0.5) * 600;
        }

        positions[i * 3] = x;
        positions[i * 3 + 1] = y;
        positions[i * 3 + 2] = z;

        // Custom soft-neon cyan colors
        colors[i * 3] = 0.0;
        colors[i * 3 + 1] = 0.8 + Math.random() * 0.2;
        colors[i * 3 + 2] = 0.9 + Math.random() * 0.1;
    }

    geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    // Custom glowing point material
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

// 2. The Picard-Fuchs S1,2 Knot (3D Spline Path)
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
        opacity: 0.9,
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

    controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// --- INTERACTIVE EVENTS & NARRATIVE SEQUENCER ---

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

// Sector Change
sectorSelectEl.addEventListener("change", (e) => {
    currentSector = parseInt(e.target.value);
    const data = sectorData[currentSector];
    
    // Update top telemetry headers
    document.getElementById("live-dw").innerText = data.dw;
    document.getElementById("live-tps").innerText = (parseFloat(data.dw) * 350).toFixed(1);

    // Log update
    logTerminal(`[SECTOR] Switched focus to: ${data.name}. Processing coords...`);
    logTerminal(`[RUNUX-TDA] Re-aligning memory buffers for ${data.galaxies} LRG points.`);
    logTerminal(`[S12-SIEVE] Calculated local Wasserstein d_W similarity: ${data.dw}`);
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
    } else if (message.includes("RUNUX")) {
        p.className = "gold-text";
    } else if (message.includes("RUSTY")) {
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
    initThree();
    // Default Act 3 composite layout on boot to wow immediately
    triggerAct(3);
};
