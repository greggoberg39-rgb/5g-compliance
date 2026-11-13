(function () {
  var root = document.getElementById("spectrum-widget");
  var dataNode = document.getElementById("spectrum-data");
  if (!root || !dataNode) return;
  var payload;
  try { payload = JSON.parse(dataNode.textContent); }
  catch (e) { return; }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  var STATES = payload.states || [];
  var TILES = payload.tiles || {};
  if (!STATES.length) return;
  root.hidden = false;

  var SCORE_MIN = 38;
  var SCORE_MAX = 93;
  var selected = "PA";
  var view = "map";
  var query = "";
  var sort = "protective";

  function colorForScore(score) {
    var t = (score - SCORE_MIN) / (SCORE_MAX - SCORE_MIN);
    if (t < 0) t = 0;
    if (t > 1) t = 1;
    // gold (contract-enforcing) -> slate-muted -> teal (consumer-protective)
    var stops = [
      [184, 134, 11],
      [171, 155, 107],
      [200, 206, 196],
      [90, 148, 140],
      [15, 118, 110]
    ];
    var x = t * (stops.length - 1);
    var i = Math.floor(x);
    if (i >= stops.length - 1) {
      var last = stops[stops.length - 1];
      return "rgb(" + last[0] + "," + last[1] + "," + last[2] + ")";
    }
    var f = x - i;
    var a = stops[i], b = stops[i + 1];
    var r = Math.round(a[0] + (b[0] - a[0]) * f);
    var g = Math.round(a[1] + (b[1] - a[1]) * f);
    var bl = Math.round(a[2] + (b[2] - a[2]) * f);
    return "rgb(" + r + "," + g + "," + bl + ")";
  }

  function byAb(ab) {
    for (var i = 0; i < STATES.length; i++) if (STATES[i].ab === ab) return STATES[i];
    return STATES[0];
  }

  function renderMetrics() {
    var pa = byAb("PA");
    var top = STATES.slice().sort(function (a, b) { return b.score - a.score || a.name.localeCompare(b.name); });
    var bot = STATES.slice().sort(function (a, b) { return a.score - b.score || a.name.localeCompare(b.name); });
    var t3 = top.slice(0, 3);
    var b3 = bot.slice(0, 3);
    var html = "";
    html += '<div class="metric-card"><div class="metric-value">#' + pa.rank + ' of ' + STATES.length + '</div><div class="metric-label">Pennsylvania</div><p>Score ' + pa.score.toFixed(1) + ', tied with Ohio, in the center band, on the left side of center</p></div>';
    html += '<div class="metric-card"><div class="metric-value">' + t3.map(function (s) { return s.ab; }).join(", ") + '</div><div class="metric-label">Most consumer-protective</div><p>' + t3.map(function (s) { return s.score.toFixed(1); }).join(", ") + ". New Mexico and Hawaii are immediately behind.</p></div>";
    html += '<div class="metric-card"><div class="metric-value">' + b3.map(function (s) { return s.ab; }).join(", ") + '</div><div class="metric-label">Most contract-enforcing</div><p>' + b3.map(function (s) { return s.score.toFixed(1); }).join(", ") + ". Weak private UDAP reach, thin remedies, or both.</p></div>";
    document.getElementById("spectrum-metrics").innerHTML = html;
  }

  function renderMap() {
    var cell = 36, gap = 4, cols = 12, rows = 8;
    var width = cols * (cell + gap) - gap;
    var height = rows * (cell + gap) - gap;
    var svg = '<svg viewBox="0 0 ' + width + ' ' + height + '" width="100%" height="' + height + '" role="img" aria-label="Tile map of the 50 states and D.C., colored from consumer-protective to sanctity of contract" style="aspect-ratio:' + width + '/' + height + ';height:auto">';
    STATES.forEach(function (row) {
      var at = TILES[row.ab];
      if (!at) return;
      var x = at[0] * (cell + gap);
      var y = at[1] * (cell + gap);
      var isSel = row.ab === selected;
      var isPA = row.ab === "PA";
      var stroke = isSel ? "#122033" : (isPA ? "#0f766e" : "#d8dee6");
      var sw = (isSel || isPA) ? 2 : 1;
      var weight = (isPA || isSel) ? 700 : 500;
      svg += '<g class="tile" data-ab="' + row.ab + '" tabindex="0" role="button" aria-label="' + row.name + '">';
      svg += '<title>' + esc(row.name) + ': rank ' + row.rank + ', score ' + row.score.toFixed(1) + '</title>';
      svg += '<rect x="' + x + '" y="' + y + '" width="' + cell + '" height="' + cell + '" rx="4" fill="#fff" stroke="' + stroke + '" stroke-width="' + sw + '"/>';
      svg += '<rect x="' + x + '" y="' + y + '" width="' + cell + '" height="5" rx="4" fill="' + colorForScore(row.score) + '"/>';
      svg += '<text x="' + (x + cell / 2) + '" y="' + (y + cell / 2 + 7) + '" text-anchor="middle" fill="#122033" font-size="11" font-weight="' + weight + '" font-family="system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif">' + row.ab + '</text>';
      svg += '</g>';
    });
    svg += '</svg>';
    var wrap = document.getElementById("spectrum-map");
    wrap.innerHTML = svg;
    wrap.querySelectorAll(".tile").forEach(function (g) {
      function pick() { selected = g.getAttribute("data-ab"); renderAll(); }
      g.addEventListener("click", pick);
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(); }
      });
    });
  }

  function renderBar() {
    var wrap = document.getElementById("spectrum-bar");
    var html = '<div class="spectrum-axis"><span>Consumer-protective</span><span>Sanctity of contract</span></div><div class="spectrum-chips">';
    STATES.forEach(function (row) {
      var isSel = row.ab === selected;
      var isPA = row.ab === "PA";
      var cls = "chip" + (isSel ? " sel" : "") + (isPA ? " pa" : "");
      html += '<button type="button" class="' + cls + '" data-ab="' + esc(row.ab) + '" title="' + esc(row.name) + ': ' + row.score.toFixed(1) + '">';
      html += '<span class="chip-swatch" style="background:' + colorForScore(row.score) + '"></span>';
      html += '<span class="chip-ab">' + row.ab + '</span></button>';
    });
    html += '</div>';
    wrap.innerHTML = html;
    wrap.querySelectorAll("button[data-ab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        selected = btn.getAttribute("data-ab");
        renderAll();
      });
    });
  }

  function renderProps() {
    var s = byAb(selected);
    var apl = s.apl || "No separate statute scored here (federal HOEPA still applies)";
    var rows = [
      ["Jurisdiction", s.name + " (" + s.ab + ")"],
      ["Rank", s.rank + " of " + STATES.length],
      ["Score", s.score.toFixed(1) + " / 100 · " + s.band],
      ["Key statute", s.statute + " (" + s.cite + ")"],
      ["Foreclosure", s.fc],
      ["State high-cost / APL law", apl],
      ["One-line note", s.note]
    ];
    var html = "";
    rows.forEach(function (pair) {
      html += "<div><dt>" + esc(pair[0]) + "</dt><dd>" + esc(pair[1]) + "</dd></div>";
    });
    document.getElementById("spectrum-props").innerHTML = html;
  }

  function filteredRows() {
    var q = query.trim().toLowerCase();
    var rows = STATES.filter(function (row) {
      if (!q) return true;
      return (row.name + " " + row.ab + " " + row.statute + " " + row.cite).toLowerCase().indexOf(q) >= 0;
    });
    if (sort === "sanctity") rows = rows.slice().sort(function (a, b) { return a.score - b.score || a.name.localeCompare(b.name); });
    else if (sort === "alpha") rows = rows.slice().sort(function (a, b) { return a.name.localeCompare(b.name); });
    else if (sort === "foreclosure") {
      var order = { Judicial: 0, Mixed: 1, Nonjudicial: 2 };
      rows = rows.slice().sort(function (a, b) { return order[a.fc] - order[b.fc] || b.score - a.score; });
    } else {
      rows = rows.slice().sort(function (a, b) { return a.rank - b.rank || a.name.localeCompare(b.name); });
    }
    return rows;
  }

  function renderTable() {
    var tbody = document.querySelector("#spectrum-table tbody");
    var rows = filteredRows();
    var html = "";
    rows.forEach(function (row) {
      var name = row.ab === "PA" ? row.name + " (focus)" : row.name;
      var trClass = row.ab === selected ? ' class="sel"' : (row.ab === "PA" ? ' class="pa"' : "");
      html += "<tr" + trClass + " data-ab=\"" + esc(row.ab) + "\">";
      html += '<td class="num">' + row.rank + "</td>";
      html += "<td>" + esc(name) + "</td>";
      html += '<td class="num">' + row.score.toFixed(1) + "</td>";
      html += "<td>" + esc(row.band) + "</td>";
      html += "<td>" + esc(row.statute + ". " + row.cite) + "</td>";
      html += "<td>" + esc(row.fc) + "</td>";
      html += "<td>" + esc(row.note) + "</td>";
      html += "</tr>";
    });
    tbody.innerHTML = html;
    tbody.querySelectorAll("tr").forEach(function (tr) {
      tr.addEventListener("click", function () {
        selected = tr.getAttribute("data-ab");
        renderAll();
      });
    });
  }

  function renderAll() {
    document.getElementById("spectrum-map").hidden = view !== "map";
    document.getElementById("spectrum-bar").hidden = view !== "spectrum";
    if (view === "map") renderMap();
    else renderBar();
    renderProps();
    renderTable();
  }

  document.querySelectorAll(".view-toggle button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      view = btn.getAttribute("data-view");
      document.querySelectorAll(".view-toggle button").forEach(function (b) { b.classList.toggle("on", b === btn); });
      renderAll();
    });
  });
  document.getElementById("spectrum-search").addEventListener("input", function (e) {
    query = e.target.value;
    renderTable();
  });
  document.getElementById("spectrum-sort").addEventListener("change", function (e) {
    sort = e.target.value;
    renderTable();
  });

  renderMetrics();
  renderAll();
})();
