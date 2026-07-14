// Phase 5 Gamification Logic
const API_BASE = "";

async function fetchLeaderboard() {
    try {
        const response = await fetch(API_BASE + '/leaderboard');
        const data = await response.json();
        const tbody = document.querySelector('#leaderboard-table tbody');
        if (tbody && Array.isArray(data)) {
            tbody.innerHTML = '';
            data.forEach((entry, index) => {
                let username = entry.user_id || entry.node || 'Anonymous Node';
                let score = entry.score !== undefined ? entry.score : (entry.points || 0);
                let colorClass = index === 0 ? "neon-cyan-text" : (index === 1 ? "neon-gold-text" : "");
                tbody.innerHTML += `<tr>
                    <td>${index + 1}</td>
                    <td class="${colorClass}">${username}</td>
                    <td>${entry.guild || 'Freelancer'}</td>
                    <td>${score.toLocaleString()}</td>
                </tr>`;
            });
        }
    } catch (e) {
        console.error("Error fetching leaderboard", e);
    }
}

async function fetchDiscoveries() {
    try {
        const response = await fetch(API_BASE + '/api/v1/discoveries');
        const data = await response.json();
        const container = document.querySelector('.discoveries-log');
        if (container && data.length > 0) {
            container.innerHTML = `<h3 style="color: var(--neon-gold); font-family: var(--font-mono); font-size: 11px; margin-bottom: 8px;">🏆 MAJORS COSMOLOGICAL DISCOVERIES</h3>`;
            data.slice(0, 3).forEach((disc, index) => {
                let colorBorder = index === 0 ? "rgba(255, 215, 0, 0.15)" : "rgba(255, 0, 127, 0.15)";
                let colorBg = index === 0 ? "rgba(255, 215, 0, 0.04)" : "rgba(255, 0, 127, 0.04)";
                let colorText = index === 0 ? "var(--neon-gold)" : "var(--neon-magenta)";
                
                container.innerHTML += `
                <div class="discovery-card" style="background: ${colorBg}; border: 1px solid ${colorBorder}; border-radius: 4px; padding: 10px; margin-bottom: 8px; font-family: var(--font-sans); font-size: 11px; line-height: 1.4;">
                    <strong style="color: ${colorText}; font-family: var(--font-mono); font-size: 10px; display: block; margin-bottom: 4px;">${index + 1}. ${disc.type} (Delta: ${disc.delta || disc.confidence_sigma || 0})</strong>
                    ${disc.description || disc.details || 'A profound anomaly detected in the cosmic web.'} <br>
                    <span style="opacity: 0.7; font-size: 9px;">Discovered by: ${disc.author || 'Anonymous'} | Sector: ${disc.sector_index || 'Unknown'}</span>
                </div>
                `;
            });
        }
    } catch (e) {
        console.error("Error fetching discoveries", e);
    }
}

async function fetchUserProgress() {
    try {
        const userRes = await fetch(API_BASE + '/users/Browser_User');
        const userData = await userRes.json();
        
        let badges = [];
        try {
            const badgeRes = await fetch(API_BASE + '/badges/Browser_User');
            badges = await badgeRes.json();
        } catch (be) {
            console.warn("Could not load real user badges, fallback activated:", be);
        }
        
        // Calculate dynamic progress
        const chunks = userData.chunks_processed || 0;
        const score = userData.score || 0;
        
        const hasFirstBlood = Array.isArray(badges) && badges.some(b => b.badge_name === "First Blood" || b.name === "First Blood");
        const hasGoldenRatio = Array.isArray(badges) && badges.some(b => b.badge_name === "Golden Ratio" || b.name === "Golden Ratio");
        const hasPlasmaWeaver = Array.isArray(badges) && badges.some(b => b.badge_name === "Plasma Weaver" || b.name === "Plasma Weaver");
        
        const quests = [
            { name: "First Blood", desc: "Process your first galaxy chunk.", progress: chunks >= 1 ? 100 : 0, goal: 100 },
            { name: "Cosmic Cartographer", desc: "Process 10 sector chunks.", progress: Math.min(Math.round((chunks / 10) * 100), 100), goal: 100 },
            { name: "Anomaly Hunter", desc: "Achieve score >= 100 points.", progress: Math.min(Math.round((score / 100) * 100), 100), goal: 100 },
            { name: "Callens Theory", desc: "Examine Sector 99 to validate Callens Theory and name ALIXE.", progress: (typeof currentSector !== "undefined" && currentSector === 35) ? 100 : 0, goal: 100 }
        ];
        
        const questsContainer = document.getElementById('quests-container');
        if (questsContainer) {
            questsContainer.innerHTML = '';
            quests.forEach(q => {
                let isDone = q.progress >= q.goal;
                let color = isDone ? "var(--neon-cyan)" : "var(--neon-magenta)";
                questsContainer.innerHTML += `
                <div style="background: rgba(0,0,0,0.4); border: 1px solid rgba(0,255,255,0.1); padding: 10px; margin-bottom: 10px; border-radius: 4px;">
                    <div style="display:flex; justify-content: space-between; font-family: var(--font-mono); font-size: 10px; margin-bottom: 5px;">
                        <strong style="color: ${color}">${q.name} ${isDone ? '✓' : ''}</strong>
                        <span>${q.progress}%</span>
                    </div>
                    <p style="font-family: var(--font-sans); font-size: 9px; opacity: 0.8; margin-bottom: 5px;">${q.desc}</p>
                    <div class="progress-bar-bg" style="background: rgba(255,255,255,0.1); height: 4px; border-radius: 2px;">
                        <div style="background: ${color}; width: ${q.progress}%; height: 100%;"></div>
                    </div>
                </div>
                `;
            });
        }
        
        // Dynamically unlock visual badges in achievements panel!
        const badgesContainer = document.getElementById('badges-container');
        if (badgesContainer) {
            badgesContainer.innerHTML = '';
            const badgeList = [
                { name: "First Blood", color: "#00ffff", active: hasFirstBlood, svg: `<path d="M50 15 L85 80 L15 80 Z" fill="rgba(0, 255, 255, ${hasFirstBlood ? 0.4 : 0.05})" stroke="#00ffff" stroke-width="${hasFirstBlood ? 4 : 1}"/>` },
                { name: "Golden Ratio", color: "#ffd700", active: hasGoldenRatio, svg: `<rect x="30" y="30" width="40" height="40" fill="rgba(255, 215, 0, ${hasGoldenRatio ? 0.4 : 0.05})" stroke="#ffd700" stroke-width="${hasGoldenRatio ? 4 : 1}" transform="rotate(45 50 50)"/>` },
                { name: "Plasma Weaver", color: "#ff007f", active: hasPlasmaWeaver, svg: `<path d="M20 50 Q50 20 80 50 T20 50" fill="rgba(255, 0, 127, ${hasPlasmaWeaver ? 0.4 : 0.05})" stroke="#ff007f" stroke-width="${hasPlasmaWeaver ? 4 : 1}"/>` }
            ];
            badgeList.forEach(b => {
                let grayscale = b.active ? "" : "filter: grayscale(100%); opacity: 0.3;";
                badgesContainer.innerHTML += `
                <div class="badge" style="text-align: center; ${grayscale}" title="${b.name}: ${b.active ? 'UNLOCKED' : 'LOCKED'}">
                    <svg width="60" height="60" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" stroke="${b.color}" stroke-width="2" fill="none" stroke-dasharray="${b.active ? 'none' : '5,5'}"/>
                        ${b.svg}
                    </svg>
                    <div class="badge-title" style="font-family: var(--font-mono); font-size: 10px; margin-top: 5px; color: ${b.color};">${b.name}</div>
                </div>
                `;
            });
        }
    } catch (e) {
        console.error("Error fetching user progress and stats", e);
    }
}

function promptDiscoveryName(delta) {
    const name = prompt("High Delta Anomaly found! Name your discovery:", "The Cosmic Eye");
    if (name) {
        if (typeof logTerminal === "function") {
            logTerminal(`[DISCOVERY] You named anomaly: ${name}`);
        }
        return name;
    }
    return "Unnamed Anomaly";
}

setInterval(() => {
    fetchLeaderboard();
    fetchDiscoveries();
    fetchUserProgress();
}, 8000); // refresh every 8s

document.addEventListener("DOMContentLoaded", () => {
    fetchLeaderboard();
    fetchDiscoveries();
    fetchUserProgress();
});
