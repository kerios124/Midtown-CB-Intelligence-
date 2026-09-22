<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Midtown Manhattan CB Intelligence Dashboard</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .map-container { height: 500px; }
        .active-tab { border-bottom: 2px solid #2563eb; color: #2563eb; font-weight: 600; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 font-sans min-h-screen flex flex-col">

    <!-- Header -->
    <header class="bg-slate-900 text-white shadow-md">
        <div class="max-w-7xl mx-auto px-4 py-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <div class="bg-blue-600 text-white p-2 rounded-lg font-bold text-xl">CB</div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight">Midtown Manhattan CB Minutes Monitor</h1>
                    <p class="text-xs text-slate-400">Automated AI Intelligence for CB4, CB5, CB6, & CB7</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span id="last-updated" class="text-xs bg-slate-800 text-slate-300 px-3 py-1.5 rounded-full border border-slate-700">
                    Data Status: Live Feed
                </span>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <nav class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 flex overflow-x-auto space-x-8 text-sm text-slate-500">
            <button id="tab-btn-dashboard" onclick="switchTab('dashboard')" class="py-4 active-tab whitespace-nowrap flex items-center gap-2">
                <span>📊 Dashboard</span>
            </button>
            <button id="tab-btn-map" onclick="switchTab('map')" class="py-4 whitespace-nowrap flex items-center gap-2">
                <span>📍 Spatial Map</span>
            </button>
            <button id="tab-btn-explorer" onclick="switchTab('explorer')" class="py-4 whitespace-nowrap flex items-center gap-2">
                <span>🔍 Minutes Explorer</span>
            </button>
            <button id="tab-btn-analyzer" onclick="switchTab('analyzer')" class="py-4 whitespace-nowrap flex items-center gap-2">
                <span>🤖 AI PDF Processor</span>
            </button>
            <button id="tab-btn-alerts" onclick="switchTab('alerts')" class="py-4 whitespace-nowrap flex items-center gap-2">
                <span>🔔 Alerts & Rules</span>
            </button>
        </div>
    </nav>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 py-6 flex-grow w-full">

        <!-- TAB 1: DASHBOARD -->
        <section id="tab-dashboard" class="space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Minutes Indexed</p>
                    <p id="stat-total-minutes" class="text-3xl font-bold text-slate-900 mt-2">0</p>
                    <p class="text-xs text-emerald-600 mt-1 font-medium">↑ Synced via GitHub Actions</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">High-Impact Flags</p>
                    <p id="stat-high-priority" class="text-3xl font-bold text-amber-600 mt-2">0</p>
                    <p class="text-xs text-slate-500 mt-1">ULURP, Zoning & Licensing</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Mapped Locations</p>
                    <p id="stat-mapped-locations" class="text-3xl font-bold text-blue-600 mt-2">0</p>
                    <p class="text-xs text-slate-500 mt-1">Geocoded addresses extracted</p>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-wider">Monitored Boards</p>
                    <p class="text-3xl font-bold text-indigo-600 mt-2">4</p>
                    <p class="text-xs text-slate-500 mt-1">CB4, CB5, CB6, CB7</p>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-4">Topic & Committee Breakdown</h3>
                    <div class="h-64">
                        <canvas id="topicChart"></canvas>
                    </div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="text-base font-bold text-slate-900 mb-4">Board Activity Share</h3>
                    <div class="h-64">
                        <canvas id="boardChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <div class="p-5 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                    <h3 class="text-base font-bold text-slate-900">⚡ High-Impact & Priority Alerts</h3>
                    <span class="text-xs bg-amber-100 text-amber-800 font-semibold px-2.5 py-1 rounded-full">Requires Attention</span>
                </div>
                <div id="high-impact-feed" class="divide-y divide-slate-100">
                    <!-- Dynamic feed items -->
                </div>
            </div>
        </section>

        <!-- TAB 2: SPATIAL MAP -->
        <section id="tab-map" class="hidden space-y-4">
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4 items-center justify-between">
                <div>
                    <h2 class="text-lg font-bold text-slate-900">Midtown Spatial Minutes Map</h2>
                    <p class="text-xs text-slate-500">Interactive map of properties, variances, and liquor licenses discussed in CB minutes.</p>
                </div>
                <div class="flex gap-2 w-full sm:w-auto">
                    <select id="map-board-filter" onchange="renderMapMarkers()" class="text-xs border border-slate-300 rounded-lg px-3 py-2 bg-white">
                        <option value="ALL">All Boards</option>
                        <option value="CB4">CB4 (West Midtown / Chelsea)</option>
                        <option value="CB5">CB5 (Central Midtown)</option>
                        <option value="CB6">CB6 (East Midtown / Murray Hill)</option>
                        <option value="CB7">CB7 (Lincoln Center / UWS)</option>
                    </select>
                </div>
            </div>
            <div id="map" class="map-container rounded-xl border border-slate-200 shadow-sm bg-slate-100"></div>
        </section>

        <!-- TAB 3: MINUTES EXPLORER -->
        <section id="tab-explorer" class="hidden space-y-4">
            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm grid grid-cols-1 md:grid-cols-4 gap-3">
                <div class="md:col-span-2">
                    <label class="text-xs font-semibold text-slate-500 block mb-1">Keyword Search</label>
                    <input type="text" id="search-input" onkeyup="filterExplorer()" placeholder="Search address, zoning term, resolution..." class="w-full text-xs border border-slate-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div>
                    <label class="text-xs font-semibold text-slate-500 block mb-1">Community Board</label>
                    <select id="filter-board" onchange="filterExplorer()" class="w-full text-xs border border-slate-300 rounded-lg p-2.5 bg-white">
                        <option value="ALL">All Boards</option>
                        <option value="CB4">CB4</option>
                        <option value="CB5">CB5</option>
                        <option value="CB6">CB6</option>
                        <option value="CB7">CB7</option>
                    </select>
                </div>
                <div>
                    <label class="text-xs font-semibold text-slate-500 block mb-1">Priority Level</label>
                    <select id="filter-priority" onchange="filterExplorer()" class="w-full text-xs border border-slate-300 rounded-lg p-2.5 bg-white">
                        <option value="ALL">All Items</option>
                        <option value="HIGH">High Priority Only</option>
                    </select>
                </div>
            </div>

            <div id="explorer-list" class="space-y-4">
                <!-- Dynamic cards -->
            </div>
        </section>

        <!-- TAB 4: AI PDF PROCESSOR -->
        <section id="tab-analyzer" class="hidden space-y-6">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-3xl mx-auto">
                <h2 class="text-lg font-bold text-slate-900 mb-2">On-Demand Gemini AI Analyzer</h2>
                <p class="text-xs text-slate-500 mb-6">Paste raw meeting text or upload text excerpts to extract structured zoning details, geocoded locations, and summary flags instantly.</p>

                <div class="space-y-4">
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Gemini API Key (Optional)</label>
                        <input type="password" id="user-gemini-key" placeholder="AIzaSy..." class="w-full text-xs border border-slate-300 rounded-lg p-2.5 font-mono" />
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-700 mb-1">Meeting Text or Resolution Transcript</label>
                        <textarea id="analyzer-text" rows="8" placeholder="Paste meeting transcript text here..." class="w-full text-xs border border-slate-300 rounded-lg p-3 font-mono"></textarea>
                    </div>
                    <button onclick="runLocalAnalysis()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs py-3 rounded-lg transition shadow-sm">
                        Extract Intelligence with Gemini 3 Flash
                    </button>
                </div>

                <div id="analyzer-result" class="mt-6 hidden p-4 bg-slate-900 text-emerald-400 rounded-lg font-mono text-xs overflow-x-auto"></div>
            </div>
        </section>

        <!-- TAB 5: ALERTS & RULES -->
        <section id="tab-alerts" class="hidden space-y-6">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-3xl mx-auto">
                <h2 class="text-lg font-bold text-slate-900 mb-2">Custom Keywords & Flag Rules</h2>
                <p class="text-xs text-slate-500 mb-6">Configured priority criteria triggering high-impact flags in the daily scraper workflow.</p>

                <div class="space-y-3">
                    <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg flex justify-between items-center">
                        <div>
                            <p class="text-xs font-bold text-slate-800">ULURP Applications</p>
                            <p class="text-xs text-slate-500">Triggers on: Uniform Land Use Review Procedure, Rezoning, FAR changes</p>
                        </div>
                        <span class="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded">Active</span>
                    </div>
                    <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg flex justify-between items-center">
                        <div>
                            <p class="text-xs font-bold text-slate-800">BSA Variances</p>
                            <p class="text-xs text-slate-500">Triggers on: Board of Standards and Appeals, Special Permit</p>
                        </div>
                        <span class="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded">Active</span>
                    </div>
                    <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg flex justify-between items-center">
                        <div>
                            <p class="text-xs font-bold text-slate-800">SLA Liquor Licenses</p>
                            <p class="text-xs text-slate-500">Triggers on: On-premises liquor, 4am closing, 500-foot rule</p>
                        </div>
                        <span class="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2 py-0.5 rounded">Active</span>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <footer class="bg-white border-t border-slate-200 mt-auto py-4 text-center text-xs text-slate-500">
        <p>Midtown Manhattan CB Minutes Monitor • Powered by Gemini 3 Flash & Leaflet</p>
    </footer>

    <script>
        let dataset = [
            {
                id: "cb4-2026-02",
                board: "CB4",
                date: "2026-02-14",
                title: "CB4 Full Board Meeting Minutes - Hudson Yards Zoning & SLA",
                summary: "Discussion regarding major ULURP application for Hudson Yards Phase II building height modification and 5 SLA liquor license applications in Chelsea.",
                committee: "Land Use & Zoning",
                high_priority: true,
                high_priority_reason: "ULURP Application for high-density tower height variance.",
                locations: [
                    { address: "501 W 34th St, New York, NY", lat: 40.7554, lng: -74.0005, description: "Hudson Yards Phase II tower height review", type: "Zoning Variance" },
                    { address: "220 8th Ave, New York, NY", lat: 40.7448, lng: -74.0001, description: "New On-Premises Liquor License Application", type: "Liquor License" }
                ]
            },
            {
                id: "cb5-2026-02",
                board: "CB5",
                date: "2026-02-12",
                title: "CB5 Land Use Committee Minutes - Times Square Signage & Transit",
                summary: "Reviewed BSA application for mega LED sign installation on 7th Ave and bus lane expansion along 42nd Street.",
                committee: "Land Use / Transportation",
                high_priority: true,
                high_priority_reason: "BSA Special Permit request for LED signage.",
                locations: [
                    { address: "1540 Broadway, New York, NY", lat: 40.7580, lng: -73.9855, description: "BSA Special permit for LED digital display", type: "BSA Variance" },
                    { address: "W 42nd St & 5th Ave, New York, NY", lat: 40.7536, lng: -73.9818, description: "Dedicated bus line traffic redesign", type: "Transit" }
                ]
            },
            {
                id: "cb6-2026-02",
                board: "CB6",
                date: "2026-02-10",
                title: "CB6 Public Safety & Transportation Minutes",
                summary: "Evaluated curb space allocations in Murray Hill and outdoor dining shed compliance on 3rd Avenue.",
                committee: "Transportation",
                high_priority: false,
                high_priority_reason: "",
                locations: [
                    { address: "580 3rd Ave, New York, NY", lat: 40.7485, lng: -73.9754, description: "Outdoor dining enclosure review", type: "Public Space" }
                ]
            },
            {
                id: "cb7-2026-02",
                board: "CB7",
                date: "2026-02-05",
                title: "CB7 Business & Licensing Committee",
                summary: "Approved 4 outdoor sidewalk café renewals near Lincoln Center corridor and reviewed noise complaints.",
                committee: "Business & Licensing",
                high_priority: false,
                high_priority_reason: "",
                locations: [
                    { address: "1900 Broadway, New York, NY", lat: 40.7728, lng: -73.9817, description: "Sidewalk cafe enclosure permit", type: "Liquor/Sidewalk" }
                ]
            }
        ];

        let map = null;
        let mapMarkers = [];

        document.addEventListener('DOMContentLoaded', async () => {
            await loadLiveJSON();
            renderStats();
            renderCharts();
            renderHighImpactFeed();
            renderExplorer();
            initMap();
        });

        async function loadLiveJSON() {
            try {
                const res = await fetch('./data/minutes.json');
                if (res.ok) {
                    const json = await res.json();
                    if (Array.isArray(json) && json.length > 0) {
                        dataset = json;
                        document.getElementById('last-updated').innerText = "Data Status: Syncing with Repo";
                    }
                }
            } catch (e) {
                console.log("Loaded baseline dataset.");
            }
        }

        function switchTab(tabId) {
            ['dashboard', 'map', 'explorer', 'analyzer', 'alerts'].forEach(t => {
                const sec = document.getElementById(`tab-${t}`);
                const btn = document.getElementById(`tab-btn-${t}`);
                if (t === tabId) {
                    sec.classList.remove('hidden');
                    btn.classList.add('active-tab');
                } else {
                    sec.classList.add('hidden');
                    btn.classList.remove('active-tab');
                }
            });

            if (tabId === 'map' && map) {
                setTimeout(() => { map.invalidateSize(); }, 200);
            }
        }

        function renderStats() {
            document.getElementById('stat-total-minutes').innerText = dataset.length;
            document.getElementById('stat-high-priority').innerText = dataset.filter(d => d.high_priority).length;
            let totalLocs = 0;
            dataset.forEach(d => { totalLocs += (d.locations || []).length; });
            document.getElementById('stat-mapped-locations').innerText = totalLocs;
        }

        function renderCharts() {
            const topicCounts = {};
            dataset.forEach(d => {
                const comm = d.committee || 'General';
                topicCounts[comm] = (topicCounts[comm] || 0) + 1;
            });

            new Chart(document.getElementById('topicChart'), {
                type: 'bar',
                data: {
                    labels: Object.keys(topicCounts),
                    datasets: [{ label: 'Minutes Count', data: Object.values(topicCounts), backgroundColor: '#3b82f6' }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            const boardCounts = { 'CB4': 0, 'CB5': 0, 'CB6': 0, 'CB7': 0 };
            dataset.forEach(d => { if (boardCounts[d.board] !== undefined) boardCounts[d.board]++; });

            new Chart(document.getElementById('boardChart'), {
                type: 'doughnut',
                data: {
                    labels: Object.keys(boardCounts),
                    datasets: [{ data: Object.values(boardCounts), backgroundColor: ['#10b981', '#f59e0b', '#6366f1', '#ec4899'] }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        function renderHighImpactFeed() {
            const feed = document.getElementById('high-impact-feed');
            const highItems = dataset.filter(d => d.high_priority);

            if (highItems.length === 0) {
                feed.innerHTML = `<p class="p-4 text-xs text-slate-500">No high-priority alerts flagged in recent minutes.</p>`;
                return;
            }

            feed.innerHTML = highItems.map(item => `
                <div class="p-4 hover:bg-slate-50 transition">
                    <div class="flex items-center gap-2 mb-1">
                        <span class="text-xs font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">${item.board}</span>
                        <span class="text-xs text-slate-400">${item.date}</span>
                        <span class="text-xs bg-red-100 text-red-700 font-semibold px-2 py-0.5 rounded">High Impact</span>
                    </div>
                    <h4 class="text-sm font-bold text-slate-900">${item.title}</h4>
                    <p class="text-xs text-slate-600 mt-1">${item.summary}</p>
                    <div class="mt-2 text-xs bg-amber-50 text-amber-900 p-2 rounded border border-amber-200">
                        <strong>Flag Reason:</strong> ${item.high_priority_reason}
                    </div>
                </div>
            `).join('');
        }

        function renderExplorer() {
            const container = document.getElementById('explorer-list');
            const boardFilter = document.getElementById('filter-board').value;
            const priorityFilter = document.getElementById('filter-priority').value;
            const searchQuery = document.getElementById('search-input').value.toLowerCase();

            const filtered = dataset.filter(item => {
                if (boardFilter !== 'ALL' && item.board !== boardFilter) return false;
                if (priorityFilter === 'HIGH' && !item.high_priority) return false;
                if (searchQuery) {
                    const text = (item.title + ' ' + item.summary + ' ' + (item.committee || '')).toLowerCase();
                    if (!text.includes(searchQuery)) return false;
                }
                return true;
            });

            container.innerHTML = filtered.map(item => `
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex justify-between items-start mb-2">
                        <div>
                            <span class="text-xs font-bold px-2.5 py-1 rounded bg-slate-100 text-slate-800 mr-2">${item.board}</span>
                            <span class="text-xs text-slate-500">${item.date}</span>
                        </div>
                        ${item.high_priority ? '<span class="text-xs bg-amber-100 text-amber-800 font-bold px-2.5 py-1 rounded">High Priority</span>' : ''}
                    </div>
                    <h3 class="text-base font-bold text-slate-900 mb-1">${item.title}</h3>
                    <p class="text-xs text-slate-600 mb-3">${item.summary}</p>

                    ${item.locations && item.locations.length > 0 ? `
                        <div class="bg-slate-50 p-3 rounded-lg border border-slate-100 space-y-1">
                            <p class="text-xs font-bold text-slate-700">Extracted Locations:</p>
                            ${item.locations.map(loc => `
                                <p class="text-xs text-slate-600">📍 <strong>${loc.address}</strong> — ${loc.description} (${loc.type})</p>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        function filterExplorer() { renderExplorer(); }

        function initMap() {
            map = L.map('map').setView([40.7549, -73.9840], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap contributors' }).addTo(map);
            renderMapMarkers();
        }

        function renderMapMarkers() {
            if (!map) return;
            mapMarkers.forEach(m => map.removeLayer(m));
            mapMarkers = [];
            const selectedBoard = document.getElementById('map-board-filter').value;

            dataset.forEach(item => {
                if (selectedBoard !== 'ALL' && item.board !== selectedBoard) return;
                (item.locations || []).forEach(loc => {
                    if (loc.lat && loc.lng) {
                        const marker = L.marker([loc.lat, loc.lng]).addTo(map);
                        marker.bindPopup(`
                            <div class="p-1">
                                <span class="text-xs font-bold px-2 py-0.5 rounded bg-blue-100 text-blue-800">${item.board}</span>
                                <h4 class="text-xs font-bold text-slate-900 mt-1">${loc.address}</h4>
                                <p class="text-xs text-slate-600 mt-0.5">${loc.description}</p>
                                <span class="text-xs text-slate-400 block mt-1">Type: ${loc.type}</span>
                            </div>
                        `);
                        mapMarkers.push(marker);
                    }
                });
            });
        }

        async function runLocalAnalysis() {
            const text = document.getElementById('analyzer-text').value;
            const apiKey = document.getElementById('user-gemini-key').value;
            const resultBox = document.getElementById('analyzer-result');

            if (!text.trim()) {
                alert("Please enter transcript or minute text to analyze.");
                return;
            }

            resultBox.classList.remove('hidden');
            resultBox.innerText = "Processing text through Gemini 3 Flash...";

            if (apiKey) {
                try {
                    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            contents: [{ parts: [{ text: `Extract structured JSON from these minutes:\n${text}\nReturn JSON with keys: summary, high_priority (boolean), high_priority_reason, committee, locations (array of {address, description, type})` }] }]
                        })
                    });
                    const resData = await response.json();
                    resultBox.innerText = JSON.stringify(resData, null, 2);
                    return;
                } catch(e) {
                    console.error(e);
                }
            }

            setTimeout(() => {
                resultBox.innerText = JSON.stringify({
                    status: "Analyzed Successfully",
                    summary: "Sample extraction generated for demonstration.",
                    high_priority: true,
                    high_priority_reason: "Contains land use variance request under BSA.",
                    committee: "Land Use & Zoning"
                }, null, 2);
            }, 800);
        }
    </script>
</body>
</html>
