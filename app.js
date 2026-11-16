// REGRESSION WEIGHT MATRIX
const MODEL_CONFIG = {
  intercept: 5.2,
  weights: {
    pm25: 1.15,
    pm10: 0.42,
    no2: 0.28,
    so2: 0.18,
    co: 9.50,
    temp: 0.12,
    humidity: -0.08
  }
};

// CPCB SPECIFICATION TIERS & ACTION SUGGESTIONS
const CPCB_TIERS = [
  {
    id: "Good",
    max: 50,
    label: "Good",
    color: "#10b981",
    mask: "No mask required",
    exercise: "Safe for all outdoor workouts",
    vent: "Open windows for fresh air ventilation",
    advisory: "Air quality is satisfactory. Pollution poses little or no risk to public health."
  },
  {
    id: "Satisfactory",
    max: 100,
    label: "Satisfactory",
    color: "#84cc16",
    mask: "Optional for sensitive persons",
    exercise: "Normal outdoor activity is fine",
    vent: "Natural ventilation is safe today",
    advisory: "Acceptable air quality. Minor discomfort possible for sensitive individuals."
  },
  {
    id: "Moderate",
    max: 200,
    label: "Moderate",
    color: "#eab308",
    mask: "Recommended for sensitive groups",
    exercise: "Take breaks during long outdoor runs",
    vent: "Close windows during heavy traffic hours",
    advisory: "May cause breathing discomfort to people with asthma, lung, or heart diseases."
  },
  {
    id: "Poor",
    max: 300,
    label: "Poor",
    color: "#f97316",
    mask: "Wear protective N95 mask outside",
    exercise: "Avoid intense outdoor exercise",
    vent: "Keep windows closed & use air purifiers",
    advisory: "Causes breathing discomfort to most people on prolonged exposure."
  },
  {
    id: "VeryPoor",
    max: 400,
    label: "Very Poor",
    color: "#ef4444",
    mask: "N95 mask mandatory outdoors",
    exercise: "Avoid outdoor morning runs/sports",
    vent: "Run air purifiers continuously indoors",
    advisory: "Risk of respiratory illness on prolonged exposure. Significant impact on vulnerable people."
  },
  {
    id: "Severe",
    max: Infinity,
    label: "Severe",
    color: "#dc2626",
    mask: "Mandatory N95 / Stay completely indoors",
    exercise: "Strictly avoid all outdoor activities",
    vent: "Seal windows & operate air cleaning units",
    advisory: "Emergency conditions. Serious health impact on healthy adults and vulnerable groups."
  }
];

// STATE REPOSITORY
let activeState = {
  pm25: 35.0,
  pm10: 70.0,
  no2: 24.0,
  so2: 12.0,
  co: 0.80,
  temp: 28.0,
  humidity: 55.0
};

// 1. THEME CONTROLLER
function setTheme(mode) {
  document.querySelectorAll('.theme-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.themeVal === mode);
  });

  if (mode === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  } else {
    document.documentElement.setAttribute('data-theme', mode);
  }
}

// 2. TAB CONTROLLER
function switchMode(mode) {
  document.querySelectorAll('.tab-pill').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.mode-view').forEach(view => view.classList.remove('active'));

  document.querySelector(`[onclick="switchMode('${mode}')"]`).classList.add('active');
  document.getElementById(`mode-${mode}`).classList.add('active');

  const presetsBar = document.getElementById('presetsBar');
  presetsBar.style.display = (mode === 'dataset') ? 'none' : 'flex';
}

// 3. PARAMETER SYNCHRONIZATION
function syncParam(key, val, origin) {
  const num = parseFloat(val) || 0;
  activeState[key] = num;

  if (origin === 'slider') {
    const disp = document.getElementById(`${key}_s_val`);
    if (disp) disp.textContent = num.toFixed(key === 'co' ? 2 : 1);
    const man = document.getElementById(key);
    if (man) man.value = num;
  } else if (origin === 'manual') {
    const sld = document.getElementById(`${key}_s`);
    if (sld) sld.value = num;
    const disp = document.getElementById(`${key}_s_val`);
    if (disp) disp.textContent = num.toFixed(key === 'co' ? 2 : 1);
  }

  evaluate();
}

// 4. QUICK PRESETS
const PRESETS = {
  clean: { pm25: 12.0, pm10: 25.0, no2: 8.0, so2: 4.0, co: 0.35, temp: 21.0, humidity: 62.0 },
  urban: { pm25: 48.0, pm10: 105.0, no2: 32.0, so2: 14.0, co: 1.10, temp: 31.0, humidity: 48.0 },
  smog:  { pm25: 230.0, pm10: 380.0, no2: 88.0, so2: 42.0, co: 4.20, temp: 18.0, humidity: 78.0 }
};

function loadPreset(key) {
  const p = PRESETS[key];
  if (!p) return;
  for (const [k, v] of Object.entries(p)) {
    syncParam(k, v, 'slider');
  }
}

// 5. CORE EVALUATION ENGINE
function evaluate() {
  const c = {
    pm25: activeState.pm25 * MODEL_CONFIG.weights.pm25,
    pm10: activeState.pm10 * MODEL_CONFIG.weights.pm10,
    no2: activeState.no2 * MODEL_CONFIG.weights.no2,
    so2: activeState.so2 * MODEL_CONFIG.weights.so2,
    co: activeState.co * MODEL_CONFIG.weights.co
  };

  const weatherEffect = (activeState.temp * MODEL_CONFIG.weights.temp) + 
                        (activeState.humidity * MODEL_CONFIG.weights.humidity);

  const rawAQI = MODEL_CONFIG.intercept + c.pm25 + c.pm10 + c.no2 + c.so2 + c.co + weatherEffect;
  const aqi = Math.max(1, Math.round(rawAQI));

  // Determine CPCB Tier
  const tier = CPCB_TIERS.find(t => aqi <= t.max);

  // Dominant Pollutant
  let maxWeight = -1;
  let dominant = "PM2.5";
  const labels = { pm25: "PM2.5", pm10: "PM10", no2: "NO₂", so2: "SO₂", co: "CO" };
  for (const [k, v] of Object.entries(c)) {
    if (v > maxWeight) { maxWeight = v; dominant = labels[k]; }
  }

  updateDashboard(aqi, tier, dominant);
}

// 6. DASHBOARD & SUGGESTIONS UPDATER
function updateDashboard(aqi, tier, dominant) {
  // Numeric Readout
  document.getElementById('aqiNumber').textContent = aqi;
  
  const badge = document.getElementById('catBadge');
  badge.textContent = tier.label;
  badge.style.backgroundColor = tier.color;
  badge.style.color = (tier.label === "Severe") ? "#ffffff" : "#0f172a";

  // Arc Fill (Gauge path length = 289)
  const clamped = Math.min(500, aqi);
  const arcOffset = 289 - (clamped / 500) * 289;
  const fillArc = document.getElementById('gaugeProgress');
  fillArc.style.strokeDashoffset = arcOffset;
  fillArc.style.stroke = tier.color;

  // Spectrum Cursor
  const pctPos = Math.min(100, Math.max(0, (clamped / 500) * 100));
  document.getElementById('spectrumCursor').style.left = `${pctPos}%`;

  // Dominant Tag
  document.getElementById('dominantBadge').textContent = `Main: ${dominant}`;

  // Smart Suggestions Update
  document.getElementById('suggMask').textContent = tier.mask;
  document.getElementById('suggExercise').textContent = tier.exercise;
  document.getElementById('suggVent').textContent = tier.vent;

  // Health Advisory Banner
  document.getElementById('advisoryDot').style.backgroundColor = tier.color;
  document.getElementById('advisoryHeading').textContent = `${tier.label} Air Quality`;
  document.getElementById('advisoryBody').textContent = tier.advisory;

  // Highlight Active Card in 2x3 Matrix
  document.querySelectorAll('.cat-card').forEach(card => card.classList.remove('active'));
  const activeCard = document.getElementById(`card-${tier.id}`);
  if (activeCard) activeCard.classList.add('active');
}

// 7. DATASET CSV HANDLER
function processCSVFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    const text = e.target.result;
    const lines = text.split(/\r?\n/).filter(l => l.trim().length > 0);
    if (lines.length < 2) return alert("Dataset has insufficient rows.");

    const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
    const idx = {
      pm25: headers.findIndex(h => h.includes("pm2")),
      pm10: headers.findIndex(h => h.includes("pm10")),
      no2: headers.findIndex(h => h.includes("no2")),
      so2: headers.findIndex(h => h.includes("so2")),
      co: headers.findIndex(h => h.includes("co")),
      temp: headers.findIndex(h => h.includes("temp")),
      humidity: headers.findIndex(h => h.includes("hum"))
    };

    let total = 0, count = 0;
    let sum = { pm25: 0, pm10: 0, no2: 0, so2: 0, co: 0, temp: 0, humidity: 0 };

    for (let i = 1; i < lines.length; i++) {
      const cols = lines[i].split(',').map(c => parseFloat(c.trim()));
      if (cols.some(isNaN)) continue;

      const row = {
        pm25: idx.pm25 !== -1 ? cols[idx.pm25] : 30,
        pm10: idx.pm10 !== -1 ? cols[idx.pm10] : 60,
        no2: idx.no2 !== -1 ? cols[idx.no2] : 20,
        so2: idx.so2 !== -1 ? cols[idx.so2] : 10,
        co: idx.co !== -1 ? cols[idx.co] : 0.8,
        temp: idx.temp !== -1 ? cols[idx.temp] : 25,
        humidity: idx.humidity !== -1 ? cols[idx.humidity] : 50
      };

      total += (row.pm25 * 1.15 + row.pm10 * 0.42 + row.no2 * 0.28 + row.so2 * 0.18 + row.co * 9.5);
      count++;
      for (const k of Object.keys(sum)) sum[k] += row[k];
    }

    if (count === 0) return alert("Could not parse numeric rows.");

    document.getElementById('batchStats').style.display = 'grid';
    document.getElementById('bCount').textContent = count;
    document.getElementById('bMean').textContent = Math.round(total / count);
    document.getElementById('bDom').textContent = "PM2.5";

    for (const k of Object.keys(sum)) {
      syncParam(k, (sum[k] / count), 'slider');
    }
  };
  reader.readAsText(file);
}

function downloadTemplateCSV() {
  const content = `PM2.5,PM10,NO2,SO2,CO,Temperature,Humidity
18.5,35.0,12.0,6.0,0.45,22.0,65.0
42.0,90.0,28.0,14.0,0.90,30.0,52.0
85.0,160.0,45.0,22.0,1.80,34.0,40.0
190.0,310.0,72.0,38.0,3.50,19.0,75.0`;
  const blob = new Blob([content], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'aqi_sample_dataset.csv';
  a.click();
}

// 8. CLIPBOARD REPORT
function copyReport() {
  const aqi = document.getElementById('aqiNumber').textContent;
  const cat = document.getElementById('catBadge').textContent;
  const dom = document.getElementById('dominantBadge').textContent;
  const adv = document.getElementById('advisoryBody').textContent;

  const text = `--- AIR QUALITY ASSESSMENT REPORT ---
Predicted AQI: ${aqi} (${cat})
${dom}
Parameters:
- PM2.5: ${activeState.pm25.toFixed(1)} µg/m³
- PM10: ${activeState.pm10.toFixed(1)} µg/m³
- NO2: ${activeState.no2.toFixed(1)} µg/m³
- SO2: ${activeState.so2.toFixed(1)} µg/m³
- CO: ${activeState.co.toFixed(2)} mg/m³
- Temp/Humidity: ${activeState.temp.toFixed(1)}°C / ${activeState.humidity.toFixed(1)}%
Health Advisory: ${adv}`;

  navigator.clipboard.writeText(text).then(() => {
    const btn = document.getElementById('btnCopyReport');
    btn.innerHTML = `<span>Copied!</span>`;
    setTimeout(() => {
      btn.innerHTML = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><span>Copy</span>`;
    }, 1800);
  });
}

// INITIALIZE
window.addEventListener("DOMContentLoaded", () => {
  setTheme('dark');
  evaluate();
});