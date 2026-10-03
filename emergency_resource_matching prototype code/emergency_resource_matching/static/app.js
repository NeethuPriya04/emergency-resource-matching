let globalData = null;
let currentView = 'greedy';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('runBtn').addEventListener('click', triggerMatching);
    document.getElementById('tab-greedy').addEventListener('click', () => switchTab('greedy'));
    document.getElementById('tab-optimal').addEventListener('click', () => switchTab('optimal'));
});

async function triggerMatching() {
    const btn = document.getElementById('runBtn');
    btn.disabled = true;
    btn.innerText = 'Computing Matrices...';

    try {
        const res = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });

        if (!res.ok) throw new Error('HTTP ' + res.status);
        globalData = await res.json();

        document.getElementById('greedyTotalDist').innerText = globalData.greedy.total_distance + ' km';
        document.getElementById('greedyAvgDist').innerText = globalData.greedy.avg_distance + ' km';
        document.getElementById('optTotalDist').innerText = globalData.optimal.total_distance + ' km';
        document.getElementById('optAvgDist').innerText = globalData.optimal.avg_distance + ' km';

        renderTable();
        renderMap();
    } catch (err) {
        alert('Server Error: ' + err.message);
    } finally {
        btn.disabled = false;
        btn.innerText = '⚡ Execute DAA Algorithms';
    }
}

function switchTab(view) {
    currentView = view;
    document.getElementById('tab-greedy').classList.toggle('active', view === 'greedy');
    document.getElementById('tab-optimal').classList.toggle('active', view === 'optimal');
    renderTable();
    renderMap();
}

function renderTable() {
    if (!globalData) return;
    const data = globalData[currentView];
    const tbody = document.getElementById('matchTableBody');
    tbody.innerHTML = '';

    if (!data.matches || data.matches.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-secondary py-3">No matches produced.</td></tr>';
        return;
    }

    data.matches.forEach(m => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>#${m.step}</strong></td>
            <td>${m.incident_id}<br><small class="text-secondary">${m.incident_desc}</small></td>
            <td><span class="badge badge-urgency-${m.urgency}">Level ${m.urgency}</span></td>
            <td class="text-success fw-bold">${m.resource_name}</td>
            <td>${m.distance} km</td>
            <td><small class="text-info">${m.reason}</small></td>
        `;
        tbody.appendChild(tr);
    });
}

function renderMap() {
    if (!globalData) return;
    const canvas = document.getElementById('canvasMap');
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const scaleX = canvas.width / 70;
    const scaleY = canvas.height / 90;

    const data = globalData[currentView];
    ctx.lineWidth = 2;
    ctx.setLineDash([4, 4]);
    ctx.strokeStyle = currentView === 'greedy' ? '#38bdf8' : '#4ade80';

    data.matches.forEach(m => {
        const inc = globalData.incidents.find(i => i.id === m.incident_id);
        const res = globalData.resources.find(r => r.id === m.resource_id);
        if (inc && res) {
            ctx.beginPath();
            ctx.moveTo(inc.location[0] * scaleX, inc.location[1] * scaleY);
            ctx.lineTo(res.location[0] * scaleX, res.location[1] * scaleY);
            ctx.stroke();
        }
    });
    ctx.setLineDash([]);

    // Units (Green squares)
    globalData.resources.forEach(r => {
        ctx.fillStyle = '#22c55e';
        const x = r.location[0] * scaleX;
        const y = r.location[1] * scaleY;
        ctx.fillRect(x - 6, y - 6, 12, 12);
        ctx.fillStyle = '#94a3b8';
        ctx.font = '10px sans-serif';
        ctx.fillText(r.id, x + 8, y + 4);
    });

    // Incidents (Red circles)
    globalData.incidents.forEach(inc => {
        ctx.fillStyle = inc.urgency === 4 ? '#ef4444' : '#f97316';
        const x = inc.location[0] * scaleX;
        const y = inc.location[1] * scaleY;
        ctx.beginPath();
        ctx.arc(x, y, 4 + (inc.urgency * 2), 0, 2 * Math.PI);
        ctx.fill();
        ctx.fillStyle = '#f8fafc';
        ctx.font = '10px sans-serif';
        ctx.fillText(inc.id, x + 10, y + 4);
    });
}
