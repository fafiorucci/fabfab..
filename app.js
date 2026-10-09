'use strict';

const GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search';
const FORECAST_URL = 'https://api.open-meteo.com/v1/forecast';
const DEFAULT_PLACE = { name: 'Roma', admin1: 'Lazio', country: 'Italia', latitude: 41.8919, longitude: 12.5113 };

// Codici WMO -> [descrizione, icona giorno, icona notte]
const WMO = {
  0: ['Sereno', '☀️', '🌙'],
  1: ['Prevalentemente sereno', '🌤️', '🌙'],
  2: ['Parzialmente nuvoloso', '⛅', '☁️'],
  3: ['Coperto', '☁️', '☁️'],
  45: ['Nebbia', '🌫️', '🌫️'],
  48: ['Nebbia con brina', '🌫️', '🌫️'],
  51: ['Pioviggine leggera', '🌦️', '🌧️'],
  53: ['Pioviggine', '🌦️', '🌧️'],
  55: ['Pioviggine intensa', '🌧️', '🌧️'],
  56: ['Pioviggine gelata', '🌧️', '🌧️'],
  57: ['Pioviggine gelata intensa', '🌧️', '🌧️'],
  61: ['Pioggia leggera', '🌦️', '🌧️'],
  63: ['Pioggia', '🌧️', '🌧️'],
  65: ['Pioggia forte', '🌧️', '🌧️'],
  66: ['Pioggia gelata', '🌧️', '🌧️'],
  67: ['Pioggia gelata forte', '🌧️', '🌧️'],
  71: ['Neve leggera', '🌨️', '🌨️'],
  73: ['Neve', '🌨️', '🌨️'],
  75: ['Neve forte', '❄️', '❄️'],
  77: ['Granelli di neve', '🌨️', '🌨️'],
  80: ['Rovesci leggeri', '🌦️', '🌧️'],
  81: ['Rovesci', '🌧️', '🌧️'],
  82: ['Rovesci violenti', '⛈️', '⛈️'],
  85: ['Rovesci di neve', '🌨️', '🌨️'],
  86: ['Rovesci di neve forti', '❄️', '❄️'],
  95: ['Temporale', '⛈️', '⛈️'],
  96: ['Temporale con grandine', '⛈️', '⛈️'],
  99: ['Temporale con grandine forte', '⛈️', '⛈️'],
};

const state = {
  unit: loadPref('unit', 'celsius'),
  place: loadPref('place', DEFAULT_PLACE),
};

const $ = (id) => document.getElementById(id);

function loadPref(key, fallback) {
  try {
    const v = localStorage.getItem('studio-meteo:' + key);
    return v ? JSON.parse(v) : fallback;
  } catch { return fallback; }
}
function savePref(key, value) {
  try { localStorage.setItem('studio-meteo:' + key, JSON.stringify(value)); } catch { /* ignore */ }
}

function wmo(code, isDay = 1) {
  const w = WMO[code] || ['Sconosciuto', '❔', '❔'];
  return { desc: w[0], icon: isDay ? w[1] : w[2] };
}

const fmtTime = (iso) => iso.slice(11, 16);
const deg = (t) => `${Math.round(t)}°`;

function windDir(d) {
  const dirs = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO'];
  return dirs[Math.round(d / 45) % 8];
}

function placeLabel(p) {
  return [p.name, p.admin1 && p.admin1 !== p.name ? p.admin1 : null, p.country].filter(Boolean).join(', ');
}

function setStatus(msg, isError = false) {
  const el = $('status');
  el.textContent = msg || '';
  el.hidden = !msg;
  el.classList.toggle('error', isError);
}

// ---------- Dati ----------

async function fetchForecast(place) {
  const params = new URLSearchParams({
    latitude: place.latitude,
    longitude: place.longitude,
    timezone: 'auto',
    forecast_days: 7,
    temperature_unit: state.unit,
    wind_speed_unit: state.unit === 'fahrenheit' ? 'mph' : 'kmh',
    precipitation_unit: state.unit === 'fahrenheit' ? 'inch' : 'mm',
    current: 'temperature_2m,apparent_temperature,relative_humidity_2m,is_day,precipitation,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m',
    hourly: 'temperature_2m,precipitation_probability,weather_code,is_day',
    daily: 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,sunrise,sunset,uv_index_max',
  });
  const res = await fetch(`${FORECAST_URL}?${params}`);
  if (!res.ok) throw new Error(`Errore del servizio meteo (${res.status})`);
  return res.json();
}

async function searchPlaces(query, signal) {
  const params = new URLSearchParams({ name: query, count: 6, language: 'it', format: 'json' });
  const res = await fetch(`${GEO_URL}?${params}`, { signal });
  if (!res.ok) throw new Error('Ricerca non disponibile');
  const data = await res.json();
  return data.results || [];
}

async function load(place) {
  state.place = place;
  savePref('place', place);
  setStatus('Caricamento…');
  try {
    const data = await fetchForecast(place);
    render(data);
    setStatus('');
  } catch (err) {
    setStatus(err.message || 'Impossibile caricare i dati meteo.', true);
  }
}

// ---------- Render ----------

function render(data) {
  const { current: c, hourly: h, daily: d, current_units: u } = data;
  const w = wmo(c.weather_code, c.is_day);

  $('place').textContent = placeLabel(state.place);
  $('updated').textContent = `Aggiornato alle ${fmtTime(c.time)} (ora locale)`;
  $('cur-icon').textContent = w.icon;
  $('cur-temp').textContent = deg(c.temperature_2m);
  $('cur-desc').textContent = w.desc;
  $('cur-feels').textContent = deg(c.apparent_temperature);
  $('cur-hum').textContent = `${c.relative_humidity_2m}%`;
  $('cur-wind').textContent = `${Math.round(c.wind_speed_10m)} ${u.wind_speed_10m} ${windDir(c.wind_direction_10m)}`;
  $('cur-press').textContent = `${Math.round(c.pressure_msl)} hPa`;
  $('cur-prec').textContent = `${c.precipitation} ${u.precipitation}`;
  $('cur-uv').textContent = d.uv_index_max[0] != null ? d.uv_index_max[0].toFixed(1) : '—';
  $('cur-sunrise').textContent = fmtTime(d.sunrise[0]);
  $('cur-sunset').textContent = fmtTime(d.sunset[0]);
  document.title = `${deg(c.temperature_2m)} ${state.place.name} · Studio Meteo`;

  // Prossime 24 ore a partire dall'ora corrente
  const start = Math.max(0, h.time.findIndex((t) => t >= c.time.slice(0, 13)));
  const hours = h.time.slice(start, start + 24).map((t, i) => ({
    time: t,
    temp: h.temperature_2m[start + i],
    pop: h.precipitation_probability[start + i] ?? 0,
    code: h.weather_code[start + i],
    isDay: h.is_day[start + i],
  }));
  renderChart(hours);
  $('hourly-list').innerHTML = hours.map((x, i) => {
    const hw = wmo(x.code, x.isDay);
    return `<div class="hour" title="${hw.desc}">
      <div class="muted">${i === 0 ? 'Ora' : fmtTime(x.time)}</div>
      <span class="icon">${hw.icon}</span>
      <div class="t">${deg(x.temp)}</div>
      <div class="p">${x.pop >= 10 ? x.pop + '%' : ''}</div>
    </div>`;
  }).join('');

  // 7 giorni
  const lo = Math.min(...d.temperature_2m_min);
  const hi = Math.max(...d.temperature_2m_max);
  const span = hi - lo || 1;
  const dayFmt = new Intl.DateTimeFormat('it-IT', { weekday: 'short', day: 'numeric' });
  $('daily-list').innerHTML = d.time.map((t, i) => {
    const dw = wmo(d.weather_code[i]);
    const min = d.temperature_2m_min[i];
    const max = d.temperature_2m_max[i];
    const left = ((min - lo) / span) * 100;
    const width = Math.max(((max - min) / span) * 100, 3);
    const pop = d.precipitation_probability_max[i];
    const label = i === 0 ? 'Oggi' : dayFmt.format(new Date(t + 'T12:00'));
    return `<li title="${dw.desc}">
      <span class="day">${label}</span>
      <span class="icon">${dw.icon}</span>
      <span class="range">
        <span class="min">${deg(min)}</span>
        <span class="bar"><span style="left:${left}%;width:${width}%"></span></span>
        <span class="max">${deg(max)}</span>
      </span>
      <span class="rain">${pop != null && pop >= 10 ? '💧' + pop + '%' : ''}</span>
    </li>`;
  }).join('');

  $('current').hidden = false;
  $('hourly').hidden = false;
  $('daily').hidden = false;
}

function renderChart(hours) {
  const W = 720, H = 180, padX = 18, padTop = 26, padBottom = 24;
  const temps = hours.map((x) => x.temp);
  const tMin = Math.min(...temps), tMax = Math.max(...temps);
  const range = tMax - tMin || 1;
  const step = (W - padX * 2) / (hours.length - 1);
  const plotH = H - padTop - padBottom;
  const x = (i) => padX + i * step;
  const y = (t) => padTop + (1 - (t - tMin) / range) * plotH * 0.75;

  const line = hours.map((p, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(p.temp).toFixed(1)}`).join(' ');
  const area = `${line} L${x(hours.length - 1)},${H - padBottom} L${x(0)},${H - padBottom} Z`;
  const bars = hours.map((p, i) => {
    const bh = (p.pop / 100) * plotH * 0.5;
    return `<rect class="rain-bar" x="${x(i) - step * 0.3}" y="${H - padBottom - bh}" width="${step * 0.6}" height="${bh}"><title>${fmtTime(p.time)} · pioggia ${p.pop}%</title></rect>`;
  }).join('');
  const labels = hours.map((p, i) => i % 3 === 0
    ? `<text class="temp-label" x="${x(i)}" y="${y(p.temp) - 8}" text-anchor="middle">${deg(p.temp)}</text>
       <text x="${x(i)}" y="${H - 6}" text-anchor="middle">${fmtTime(p.time)}</text>`
    : '').join('');

  $('chart').innerHTML = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Andamento della temperatura e probabilità di pioggia nelle prossime 24 ore">
    <line class="grid" x1="${padX}" x2="${W - padX}" y1="${H - padBottom}" y2="${H - padBottom}"/>
    ${bars}
    <path class="temp-area" d="${area}"/>
    <path class="temp-line" d="${line}"/>
    ${labels}
  </svg>`;
}

// ---------- Ricerca ----------

let searchTimer = null;
let searchCtrl = null;
let results = [];
let activeIdx = -1;

function showSuggestions(list) {
  results = list;
  activeIdx = -1;
  const ul = $('suggestions');
  if (!list.length) {
    ul.innerHTML = '<li aria-disabled="true"><small>Nessun risultato</small></li>';
  } else {
    ul.innerHTML = list.map((p, i) => `<li role="option" data-i="${i}">${p.name} <small>${[p.admin1, p.country].filter(Boolean).join(', ')}</small></li>`).join('');
  }
  ul.hidden = false;
}

function hideSuggestions() {
  $('suggestions').hidden = true;
  activeIdx = -1;
}

function pick(i) {
  const p = results[i];
  if (!p) return;
  hideSuggestions();
  $('search-input').value = '';
  $('search-input').blur();
  load({ name: p.name, admin1: p.admin1, country: p.country, latitude: p.latitude, longitude: p.longitude });
}

$('search-input').addEventListener('input', (e) => {
  const q = e.target.value.trim();
  clearTimeout(searchTimer);
  if (q.length < 2) { hideSuggestions(); return; }
  searchTimer = setTimeout(async () => {
    searchCtrl?.abort();
    searchCtrl = new AbortController();
    try {
      showSuggestions(await searchPlaces(q, searchCtrl.signal));
    } catch (err) {
      if (err.name !== 'AbortError') setStatus(err.message, true);
    }
  }, 300);
});

$('search-input').addEventListener('keydown', (e) => {
  const ul = $('suggestions');
  if (ul.hidden || !results.length) return;
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    activeIdx = (activeIdx + (e.key === 'ArrowDown' ? 1 : -1) + results.length) % results.length;
    [...ul.children].forEach((li, i) => li.setAttribute('aria-selected', i === activeIdx));
  } else if (e.key === 'Escape') {
    hideSuggestions();
  }
});

$('search-form').addEventListener('submit', (e) => {
  e.preventDefault();
  if (results.length && !$('suggestions').hidden) pick(Math.max(activeIdx, 0));
});

$('suggestions').addEventListener('mousedown', (e) => {
  const li = e.target.closest('li[data-i]');
  if (li) { e.preventDefault(); pick(Number(li.dataset.i)); }
});

$('search-input').addEventListener('blur', () => setTimeout(hideSuggestions, 100));

// ---------- Posizione e unità ----------

$('geo-btn').addEventListener('click', () => {
  if (!navigator.geolocation) { setStatus('Geolocalizzazione non supportata.', true); return; }
  setStatus('Rilevamento posizione…');
  navigator.geolocation.getCurrentPosition(
    (pos) => load({
      name: 'La mia posizione',
      latitude: +pos.coords.latitude.toFixed(4),
      longitude: +pos.coords.longitude.toFixed(4),
    }),
    () => setStatus('Impossibile ottenere la posizione.', true),
    { timeout: 10000 },
  );
});

function updateUnitBtn() {
  $('unit-btn').textContent = state.unit === 'celsius' ? '°C' : '°F';
}

$('unit-btn').addEventListener('click', () => {
  state.unit = state.unit === 'celsius' ? 'fahrenheit' : 'celsius';
  savePref('unit', state.unit);
  updateUnitBtn();
  load(state.place);
});

updateUnitBtn();
load(state.place);
