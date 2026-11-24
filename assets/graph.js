/* graph.js — силовой граф Веротеки на чистом JS */
(function () {
  'use strict';
  var canvas = document.getElementById('g-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var card = document.getElementById('g-card');
  var searchInput = document.getElementById('g-search');
  var resetBtn = document.getElementById('g-reset');

  var axisCbs = {
    dvaita: document.getElementById('g-axis-dvaita'),
    advaita: document.getElementById('g-axis-advaita'),
    sunyata: document.getElementById('g-axis-sunyata')
  };
  var linksOnlyCb = document.getElementById('g-links-only');

  var DPR = Math.min(window.devicePixelRatio || 1, 2);
  var W = 0, H = 0;
  var nodes = [], links = [], byId = {};
  var hovered = null, selected = null, dragging = null;
  var cam = { x: 0, y: 0, scale: 1 };
  var alpha = 1;

  var KIND_COLOR = {
    'выделилась': '#4f46e5',
    'влияние': '#f59e0b',
    'раскол': '#ef4444',
    'ветка': '#10b981',
    'пантеон': '#8b5cf6',
    'бог принадлежит': '#a78bfa'
  };

  var SECTION_COLOR = {
    '01_basics': '#94a3b8',
    '02_world': '#2563eb',
    '03_ancient': '#b45309',
    '04_national': '#059669',
    '05_nrd': '#dc2626',
    '06_esoteric': '#7c3aed',
    '07_mysticism': '#0891b2',
    '08_skeptic': '#475569',
    '09_ref': '#a1a1aa',
    '10_pantheons': '#c026d3'
  };

  function resize() {
    var rect = canvas.getBoundingClientRect();
    W = rect.width; H = rect.height;
    canvas.width = Math.round(W * DPR);
    canvas.height = Math.round(H * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  }
  window.addEventListener('resize', resize);

  function radius(n) {
    if (n.section === '10_pantheons') return 5.5;
    if (n.section === '02_world' || n.section === '03_ancient' || n.section === '04_national') return 4.5;
    return 3;
  }

  function visibleNode(n) {
    if (!n.axis) return true;
    var cb = axisCbs[n.axis];
    return cb ? cb.checked : true;
  }

  fetch('graph-data.json').then(function (r) { return r.json(); }).then(function (data) {
    var rawNodes = data.nodes;
    var rawLinks = data.links;
    var deg = {};
    rawLinks.forEach(function (l) {
      deg[l.source] = (deg[l.source] || 0) + 1;
      deg[l.target] = (deg[l.target] || 0) + 1;
    });
    var hubs = {
      '02_world/abrahamic/abrahamic': 1, '02_world/abrahamic/judaism/judaism': 1,
      '02_world/abrahamic/christianity/christianity': 1, '02_world/abrahamic/islam/islam': 1,
      '02_world/dharmic/hinduism/hinduism': 1, '02_world/dharmic/buddhism/buddhism': 1,
      '03_ancient/graeco_roman/greek/greek': 1, '03_ancient/graeco_roman/roman/roman': 1,
      '03_ancient/near_east/egyptian/egyptian': 1, '03_ancient/near_east/mesopotamian/mesopotamian': 1,
      '03_ancient/european/norse/norse': 1, '03_ancient/european/slavic_tradition/slavic_tradition': 1,
      '02_world/iranian/zoroastrianism/zoroastrianism': 1,
      '10_pantheons/pantheons': 1
    };
    var keep = {};
    rawNodes.forEach(function (n) {
      if (deg[n.id] || hubs[n.id] || n.section === '10_pantheons') keep[n.id] = true;
    });
    nodes = rawNodes.filter(function (n) { return keep[n.id]; }).map(function (n) {
      var ang = Math.random() * Math.PI * 2;
      var r = 80 + Math.random() * 200;
      return {
        id: n.id, title: n.title, section: n.section, axis: n.axis, year: n.year, url: n.url,
        x: Math.cos(ang) * r, y: Math.sin(ang) * r, vx: 0, vy: 0,
        degree: deg[n.id] || 0
      };
    });
    byId = {};
    nodes.forEach(function (n) { byId[n.id] = n; });
    links = rawLinks.filter(function (l) { return byId[l.source] && byId[l.target]; })
      .map(function (l) { return { source: byId[l.source], target: byId[l.target], kind: l.kind }; });
    resize();
    requestAnimationFrame(tick);
  });

  function simulate() {
    var i, j, a, b, dx, dy, d2, d, f;
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      if (a === dragging) continue;
      a.vx *= 0.86; a.vy *= 0.86;
      for (j = i + 1; j < nodes.length; j++) {
        b = nodes[j];
        dx = b.x - a.x; dy = b.y - a.y;
        d2 = dx * dx + dy * dy;
        if (d2 < 1) { d2 = 1; }
        if (d2 > 90000) continue;
        d = Math.sqrt(d2);
        f = 900 / d2 * alpha;
        a.vx -= dx / d * f; a.vy -= dy / d * f;
        if (b !== dragging) { b.vx += dx / d * f; b.vy += dy / d * f; }
      }
      a.vx -= a.x * 0.0016 * alpha;
      a.vy -= a.y * 0.0016 * alpha;
    }
    for (i = 0; i < links.length; i++) {
      var l = links[i];
      a = l.source; b = l.target;
      dx = b.x - a.x; dy = b.y - a.y;
      d = Math.sqrt(dx * dx + dy * dy) || 1;
      var rest = l.kind === 'бог принадлежит' ? 46 : (l.kind === 'пантеон' ? 90 : 120);
      f = (d - rest) * 0.02 * alpha;
      dx /= d; dy /= d;
      if (a !== dragging) { a.vx += dx * f; a.vy += dy * f; }
      if (b !== dragging) { b.vx -= dx * f; b.vy -= dy * f; }
    }
    for (i = 0; i < nodes.length; i++) {
      a = nodes[i];
      if (a === dragging) continue;
      a.x += a.vx; a.y += a.vy;
    }
  }

  function worldToScreen(x, y) {
    return [(x + cam.x) * cam.scale + W / 2, (y + cam.y) * cam.scale + H / 2];
  }
  function screenToWorld(sx, sy) {
    return [(sx - W / 2) / cam.scale - cam.x, (sy - H / 2) / cam.scale - cam.y];
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    links.forEach(function (l) {
      if (!visibleNode(l.source) || !visibleNode(l.target)) return;
      var p1 = worldToScreen(l.source.x, l.source.y);
      var p2 = worldToScreen(l.target.x, l.target.y);
      var hl = (selected && (l.source === selected || l.target === selected)) ||
               (hovered && (l.source === hovered || l.target === hovered));
      ctx.beginPath();
      ctx.moveTo(p1[0], p1[1]);
      ctx.lineTo(p2[0], p2[1]);
      ctx.strokeStyle = KIND_COLOR[l.kind] || '#cbd5e1';
      ctx.globalAlpha = hl ? 0.95 : 0.28;
      ctx.lineWidth = hl ? 2.2 : 1.1;
      ctx.stroke();
      ctx.globalAlpha = 1;
    });
    nodes.forEach(function (n) {
      if (!visibleNode(n)) return;
      if (linksOnlyCb && linksOnlyCb.checked && !n.degree) return;
      var p = worldToScreen(n.x, n.y);
      var r = radius(n) * cam.scale;
      var col = SECTION_COLOR[n.section] || '#64748b';
      var isSel = n === selected, isHov = n === hovered;
      ctx.beginPath();
      ctx.arc(p[0], p[1], r + (isSel || isHov ? 2.5 : 0), 0, Math.PI * 2);
      ctx.fillStyle = col;
      ctx.globalAlpha = (n.section === '10_pantheons') ? 0.75 : 1;
      ctx.fill();
      ctx.globalAlpha = 1;
      if (isSel || isHov) {
        ctx.strokeStyle = '#111'; ctx.lineWidth = 2; ctx.stroke();
      }
      if (cam.scale > 0.75 || isSel || isHov || n.section === '10_pantheons') {
        if (r > 2.4 || isSel || isHov) {
          ctx.font = (isSel || isHov ? '600 ' : '') + '11px system-ui, sans-serif';
          ctx.fillStyle = isSel || isHov ? '#111' : '#334155';
          ctx.textAlign = 'center';
          ctx.fillText(n.title, p[0], p[1] - r - 5);
        }
      }
    });
  }

  function tick() {
    if (alpha > 0.02) { alpha *= 0.995; simulate(); }
    draw();
    requestAnimationFrame(tick);
  }

  function hitTest(sx, sy) {
    var best = null, bestD = 1e9;
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      if (!visibleNode(n)) continue;
      if (linksOnlyCb && linksOnlyCb.checked && !n.degree) continue;
      var p = worldToScreen(n.x, n.y);
      var dx = p[0] - sx, dy = p[1] - sy;
      var d = Math.sqrt(dx * dx + dy * dy);
      var r = radius(n) * cam.scale + 6;
      if (d < r && d < bestD) { bestD = d; best = n; }
    }
    return best;
  }

  var isPanning = false, panStart = null, moved = false;

  canvas.addEventListener('pointerdown', function (e) {
    var rect = canvas.getBoundingClientRect();
    var sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    var n = hitTest(sx, sy);
    moved = false;
    if (n) {
      dragging = n; alpha = Math.max(alpha, 0.3);
      try { canvas.setPointerCapture(e.pointerId); } catch (err) {}
    } else {
      isPanning = true;
      panStart = { x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y };
    }
  });

  canvas.addEventListener('pointermove', function (e) {
    var rect = canvas.getBoundingClientRect();
    var sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    if (dragging) {
      var w = screenToWorld(sx, sy);
      dragging.x = w[0]; dragging.y = w[1];
      dragging.vx = 0; dragging.vy = 0;
      alpha = Math.max(alpha, 0.25);
      moved = true;
    } else if (isPanning) {
      cam.x = panStart.cx + (e.clientX - panStart.x) / cam.scale;
      cam.y = panStart.cy + (e.clientY - panStart.y) / cam.scale;
      moved = true;
    } else {
      hovered = hitTest(sx, sy);
      canvas.style.cursor = hovered ? 'pointer' : 'grab';
    }
  });

  canvas.addEventListener('pointerup', function (e) {
    var rect = canvas.getBoundingClientRect();
    var sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    var target = dragging;
    dragging = null;
    isPanning = false;
    if (target && !moved) { showCard(target); return; }
    var n = hitTest(sx, sy);
    if (n) showCard(n);
  });

  canvas.addEventListener('wheel', function (e) {
    e.preventDefault();
    var rect = canvas.getBoundingClientRect();
    var sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    var before = screenToWorld(sx, sy);
    var factor = e.deltaY < 0 ? 1.12 : 1 / 1.12;
    cam.scale = Math.max(0.2, Math.min(4, cam.scale * factor));
    var after = screenToWorld(sx, sy);
    cam.x += after[0] - before[0];
    cam.y += after[1] - before[1];
  }, { passive: false });

  function esc(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function showCard(n) {
    selected = n;
    var incoming = links.filter(function (l) { return l.target === n && l.source !== n; });
    var outgoing = links.filter(function (l) { return l.source === n && l.target !== n; });
    var h = '<button id="g-close" style="position:absolute;top:8px;right:12px;background:none;border:none;font-size:1.3rem;cursor:pointer;color:var(--muted)" aria-label="Закрыть">×</button>';
    h += '<h2>' + esc(n.title) + '</h2>';
    var meta = [];
    if (n.axis) meta.push('ось: ' + esc(n.axis));
    if (n.year) meta.push(esc(n.year));
    if (meta.length) h += '<div class="g-meta">' + meta.join(' · ') + '</div>';
    h += '<a class="g-open" href="ru/' + esc(n.url) + '">Открыть статью →</a>';
    if (incoming.length) {
      h += '<div class="g-rel"><b>Из чего выделилась / что влияло:</b>';
      incoming.forEach(function (l) {
        h += '<a href="#" data-id="' + esc(l.source.id) + '">' + esc(l.source.title) + ' <span style="color:var(--muted);font-size:.8em">(' + esc(l.kind) + ')</span></a>';
      });
      h += '</div>';
    }
    if (outgoing.length) {
      h += '<div class="g-rel"><b>Что из неё вышло / на что повлияла:</b>';
      outgoing.forEach(function (l) {
        h += '<a href="#" data-id="' + esc(l.target.id) + '">' + esc(l.target.title) + ' <span style="color:var(--muted);font-size:.8em">(' + esc(l.kind) + ')</span></a>';
      });
      h += '</div>';
    }
    card.innerHTML = h;
    card.hidden = false;
    card.querySelector('#g-close').onclick = function () {
      card.hidden = true; selected = null;
    };
    Array.prototype.forEach.call(card.querySelectorAll('a[data-id]'), function (a) {
      a.onclick = function (ev) {
        ev.preventDefault();
        var t = byId[a.getAttribute('data-id')];
        if (t) {
          cam.x = -t.x; cam.y = -t.y;
          showCard(t);
        }
      };
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', function () {
      var q = searchInput.value.trim().toLowerCase();
      if (!q) { selected = null; return; }
      var found = nodes.filter(function (n) { return n.title.toLowerCase().indexOf(q) !== -1; });
      if (found.length) {
        selected = found[0];
        cam.x = -found[0].x; cam.y = -found[0].y; cam.scale = 1.6;
      }
    });
  }

  if (resetBtn) {
    resetBtn.onclick = function () {
      cam = { x: 0, y: 0, scale: 1 };
      alpha = 1;
      card.hidden = true; selected = null;
    };
  }

  Object.keys(axisCbs).forEach(function (k) {
    if (axisCbs[k]) axisCbs[k].onchange = function () { selected = null; };
  });
})();
