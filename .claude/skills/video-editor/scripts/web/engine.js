/* Shared short-video style engine (styles A–I). Used by the live preview page and by the
   headless final renderer. All drawing is in a 540x960 coordinate space; `scale` 2 gives 1080x1920.
   Source video = colour frame (left half) | person matte (right half), side by side. */
(function () {
const W = 540, H = 960;
const CJK_SERIF = '"Noto Serif SC","Noto Serif CJK SC",serif';
const CJK_SANS = '"Noto Sans SC","Noto Sans CJK SC",sans-serif';

/* ---------- helpers ---------- */
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const easeOut = x => 1 - (1 - clamp(x)) ** 3;
const easeIO = x => { x = clamp(x); return 3 * x * x - 2 * x * x * x; };
const backOut = (x, s = 1.9) => { x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1; };
function pop(t, t0, t1, dur = 0.28, o = 0.22) {
  if (t < t0 || t > t1) return [0, 0];
  const a = clamp((t - t0) / 0.12) * clamp((t1 - t) / o);
  return [backOut((t - t0) / dur) * (0.85 + 0.15 * clamp((t1 - t) / o)), a];
}
const fade = (t, t0, t1, i = 0.15, o = 0.15) => (t < t0 || t > t1) ? 0 : clamp((t - t0) / i) * clamp((t1 - t) / o);
const hex = h => { h = (h || '#ffffff').replace('#', ''); if (h.length === 3) h = h.split('').map(c => c + c).join(''); return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16) || 0); };
const rgb = (c, a = 1) => `rgba(${c.map(v => Math.round(clamp(v, 0, 255))).join(',')},${a})`;
const mix = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
const lum = c => 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
const isCJK = s => /[　-鿿＀-￯]/.test(s || '');
function rr(g, x, y, w, h, r) { g.beginPath(); g.roundRect(x, y, w, h, r); }
function within(g, x, y, s, a, rot, fn) {
  if (a <= 0.003 || s <= 0.01) return;
  g.save(); g.globalAlpha *= a; g.translate(x, y); if (rot) g.rotate(rot * Math.PI / 180); g.scale(s, s); fn(g); g.restore();
}
function chunks(txt) { // words for latin, 1–2 char groups for CJK
  txt = (txt || '').trim(); if (!txt) return [];
  if (isCJK(txt)) { const out = []; const s = [...txt.replace(/\s+/g, '')]; for (let i = 0; i < s.length; i += 2) out.push(s.slice(i, i + 2).join('')); return out; }
  return txt.split(/\s+/);
}
function hash(n) { const x = Math.sin(n * 127.1) * 43758.5453; return x - Math.floor(x); }

/* ---------- fonts ---------- */
const FONTS = {
  serif_black:       {name: '粗宋体', css: s => `900 ${s}px ${CJK_SERIF}`},
  serif_italic:      {name: '衬线斜体', css: s => `italic 700 ${s}px "VE Crimson",${CJK_SERIF}`, skewCJK: true},
  playfair_italic:   {name: 'Playfair 斜体', css: s => `italic 700 ${s}px "VE Playfair",${CJK_SERIF}`, skewCJK: true},
  sans_black:        {name: '粗黑体', css: s => `900 ${s}px ${CJK_SANS}`},
  montserrat:        {name: 'Montserrat', css: s => `900 ${s * 0.82}px "VE Montserrat",${CJK_SANS}`},
  montserrat_italic: {name: 'Montserrat 斜体', css: s => `italic 900 ${s * 0.82}px "VE Montserrat",${CJK_SANS}`, skewCJK: true},
  anton:             {name: 'Anton', css: s => `400 ${s}px "VE Anton",${CJK_SANS}`},
  mono:              {name: 'Space Mono', css: s => `700 ${s * 0.78}px "VE Mono",${CJK_SANS}`}
};
const UI = (w, s, cjkFirst) => `${w} ${s}px "VE Inter",${CJK_SANS}`;

/* draw a keyword with the chosen font; returns width */
function bigText(g, txt, x, y, o) {
  const f = FONTS[o.font] || FONTS.sans_black;
  g.save();
  g.font = f.css(o.size); g.textAlign = o.align || 'center'; g.textBaseline = 'middle';
  let w = g.measureText(txt).width;
  const fit = o.maxW ? Math.min(1, o.maxW / Math.max(1, w)) : 1;
  g.translate(x, y); g.scale(fit, fit);
  if (f.skewCJK && isCJK(txt)) g.transform(1, 0, -0.2, 1, 0, 0);
  if (o.glow) { g.shadowColor = rgb(o.glowColor || o.color, 0.95); g.shadowBlur = o.glowBlur || 26; }
  else if (o.shadow !== false) { g.shadowColor = 'rgba(0,0,0,.38)'; g.shadowBlur = 10; g.shadowOffsetY = 5; }
  if (o.stroke) { g.lineWidth = o.strokeW || 6; g.strokeStyle = o.strokeColor || '#1a1a1a'; g.lineJoin = 'round'; g.strokeText(txt, 0, 0); }
  g.fillStyle = typeof o.color === 'string' ? o.color : rgb(o.color);
  g.fillText(txt, 0, 0); if (o.glow) g.fillText(txt, 0, 0);
  g.restore();
  return w * fit;
}
function uiText(g, txt, x, y, size, color, o = {}) {
  g.save(); g.font = o.font || UI(o.w || 800, size); g.textAlign = o.align || 'center'; g.textBaseline = 'middle';
  if (o.shadow) { g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 8; g.shadowOffsetY = 3; }
  g.fillStyle = color; g.fillText(txt, x, y, o.maxW || 1e4); const w = Math.min(o.maxW || 1e4, g.measureText(txt).width); g.restore(); return w;
}

/* ---------- small graphics ---------- */
function icon(g, kind, s, col) {
  g.save(); g.strokeStyle = col; g.fillStyle = col; g.lineWidth = s / 12; g.lineCap = 'round'; g.lineJoin = 'round';
  const c = (x, y) => [x * s - s / 2, y * s - s / 2];
  g.beginPath();
  if (kind === 'pin') { g.arc(...c(.5, .38), s * .26, 0, Math.PI * 2); g.stroke(); g.beginPath(); g.moveTo(...c(.29, .52)); g.lineTo(...c(.5, .92)); g.lineTo(...c(.71, .52)); g.fill(); g.beginPath(); g.arc(...c(.5, .38), s * .09, 0, Math.PI * 2); g.fill(); }
  else if (kind === 'house') { [[.5,.12],[.9,.48],[.8,.48],[.8,.88],[.58,.88],[.58,.64],[.42,.64],[.42,.88],[.2,.88],[.2,.48],[.1,.48]].forEach((p, i) => i ? g.lineTo(...c(...p)) : g.moveTo(...c(...p))); g.closePath(); g.fill(); }
  else if (kind === 'search') { g.arc(...c(.42, .42), s * .26, 0, Math.PI * 2); g.stroke(); g.beginPath(); g.lineWidth = s / 8; g.moveTo(...c(.62, .62)); g.lineTo(...c(.86, .86)); g.stroke(); }
  else if (kind === 'gavel') { g.save(); g.translate(...c(.42, .34)); g.rotate(-0.7); g.fillRect(-s * .22, -s * .1, s * .44, s * .2); g.restore(); g.moveTo(...c(.45, .4)); g.lineTo(...c(.82, .8)); g.stroke(); g.fillRect(...c(.14, .84), s * .46, s * .08); }
  else if (kind === 'doc') { g.roundRect(...c(.24, .1), s * .52, s * .8, s * .06); g.stroke(); [.34, .5, .66].forEach(y => { g.beginPath(); g.moveTo(...c(.36, y)); g.lineTo(...c(.64, y)); g.stroke(); }); }
  else if (kind === 'check') { g.lineWidth = s / 8; g.moveTo(...c(.18, .52)); g.lineTo(...c(.42, .76)); g.lineTo(...c(.84, .26)); g.stroke(); }
  else if (kind === 'heart') { g.moveTo(0, s * .32); g.bezierCurveTo(-s * .55, -s * .05, -s * .25, -s * .48, 0, -s * .18); g.bezierCurveTo(s * .25, -s * .48, s * .55, -s * .05, 0, s * .32); g.fill(); }
  else if (kind === 'phone') { g.roundRect(...c(.3, .08), s * .4, s * .84, s * .08); g.stroke(); g.beginPath(); g.arc(...c(.5, .8), s * .04, 0, Math.PI * 2); g.fill(); }
  else { g.arc(0, 0, s * .38, 0, Math.PI * 2); g.stroke(); g.beginPath(); g.ellipse(0, 0, s * .16, s * .38, 0, 0, Math.PI * 2); g.stroke(); g.beginPath(); g.moveTo(-s * .38, 0); g.lineTo(s * .38, 0); g.stroke(); }
  g.restore();
}
function pill(g, txt, x, y, s, a, o = {}) {
  within(g, x, y, s, a, o.rot || 0, g => {
    const sz = o.size || 18; g.font = UI(o.w || 600, sz);
    const tw = g.measureText(txt).width, dot = o.dot !== false, w = tw + (dot ? 62 : 40), h = sz + 24;
    g.shadowColor = 'rgba(0,0,0,.22)'; g.shadowBlur = 12; g.shadowOffsetY = 5;
    rr(g, -w / 2, -h / 2, w, h, h / 2); g.fillStyle = o.bg || '#fff'; g.fill(); g.shadowColor = 'transparent';
    if (dot) { g.beginPath(); g.arc(-w / 2 + 23, 0, 8, 0, Math.PI * 2); g.fillStyle = o.dotColor || '#888'; g.fill(); }
    g.fillStyle = o.fg || '#181a16'; g.textBaseline = 'middle'; g.textAlign = 'left'; g.fillText(txt, -w / 2 + (dot ? 40 : 20), 1);
  });
}
function card(g, kind, label, w, h, A, o = {}) {
  g.shadowColor = 'rgba(0,0,0,.28)'; g.shadowBlur = 18; g.shadowOffsetY = 8;
  rr(g, -w / 2, -h / 2, w, h, o.r || 17); g.fillStyle = o.bg || 'rgba(255,255,255,.98)'; g.fill(); g.shadowColor = 'transparent';
  if (o.border) { g.strokeStyle = o.border; g.lineWidth = 1; g.stroke(); }
  g.beginPath(); g.arc(0, -h / 2 + 50, 33, 0, Math.PI * 2); g.fillStyle = rgb(A.c); g.fill();
  g.save(); g.translate(0, -h / 2 + 50); icon(g, kind, 38, lum(A.c) > 150 ? '#181a16' : '#ffffff'); g.restore();
  g.font = UI(800, 15); g.fillStyle = o.fg || '#181a16'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(label, 0, h / 2 - 28, w - 12);
}

/* ---------- engine ---------- */
function Engine(out, video, data, opts = {}) {
  const sc = opts.scale || 1;
  out.width = W * sc; out.height = H * sc;
  const octx = out.getContext('2d');
  const mk = (rf) => { const c = document.createElement('canvas'); c.width = W * sc; c.height = H * sc; const g = c.getContext('2d', rf ? {willReadFrequently: true} : undefined); g.setTransform(sc, 0, 0, sc, 0, 0); return [c, g]; };
  const [V, vctx] = mk(true), [P, pctx] = mk(true), [Mk, mctx] = mk(true);
  const [T1, t1] = mk(), [T2, t2] = mk(), [T3, t3] = mk(), [RB, rbctx] = mk(), [RF, rfctx] = mk();
  let noMask = false;
  const st = {};
  const E = {W, H, sc, st, data, V, P, T1, T2, T3, t1, t2, t3};

  E.acc = () => { const c = hex(st.accent); return {c, d: c.map(v => v * 0.7), l: mix(c, [255, 255, 255], 0.55), hex: st.accent}; };
  E.reset = g => { g.setTransform(sc, 0, 0, sc, 0, 0); g.globalAlpha = 1; g.filter = 'none'; g.globalCompositeOperation = 'source-over'; g.shadowColor = 'transparent'; };
  E.clear = g => { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, g.canvas.width, g.canvas.height); g.restore(); };
  E.Z = (g, z) => g.transform(z, 0, 0, z, E.fx * (1 - z), E.fy * (1 - z));
  E.frame = (g, o = {}) => { // draw video frame
    g.save(); if (o.z) E.Z(g, o.z); g.filter = o.filter || 'none';
    const pad = o.filter && o.filter.includes('blur') ? 16 : 0;
    g.drawImage(V, 0, 0, V.width, V.height, -pad, -pad, W + pad * 2, H + pad * 2); g.restore();
  };
  E.person = (g, o = {}) => {
    g.save(); if (o.z) E.Z(g, o.z); g.filter = o.filter || 'none';
    g.drawImage(noMask ? V : P, 0, 0, P.width, P.height, 0, 0, W, H); g.restore();
  };
  E.layer = (g, c, x = 0, y = 0, w = W, h = H) => g.drawImage(c, 0, 0, c.width, c.height, x, y, w, h);
  E.flash = (g, t, t0, dur = 0.25, col = '#fff') => { const a = fade(t, t0, t0 + dur, 0.04, dur - 0.04); if (a > 0) { g.save(); g.globalAlpha = a; g.fillStyle = col; g.fillRect(0, 0, W, H); g.restore(); } };
  E.rms = fi => (data.rms && data.rms[clamp(fi, 0, data.rms.length - 1)]) || 0.2;
  E.subtitle = (g, t, o = {}) => {
    const ev = E.ev(t, 'sub'); if (!ev || !st.subs) return;
    const words = chunks(ev.text); if (!words.length) return;
    const per = (ev.t1 - ev.t0) / words.length, k = Math.floor((t - ev.t0) / per);
    const grp = 4, start = Math.floor(k / grp) * grp, shown = words.slice(start, Math.min(words.length, start + grp));
    const sep = isCJK(ev.text) ? '' : ' ';
    g.save(); g.font = o.font || `900 ${o.size || 28}px ${CJK_SANS}`; g.textBaseline = 'middle';
    const full = shown.join(sep), fw = Math.min(480, g.measureText(full).width); let x = 270 - fw / 2;
    const sc2 = Math.min(1, 480 / Math.max(1, g.measureText(full).width));
    g.translate(270, o.y || 850); g.scale(sc2, sc2); g.translate(-270, 0); x = 270 - g.measureText(full).width / 2;
    shown.forEach((w, i) => {
      const cur = start + i === k;
      g.shadowColor = 'rgba(0,0,0,.7)'; g.shadowBlur = 10; g.shadowOffsetY = 3;
      g.fillStyle = cur && o.hi ? o.hi : (start + i > k ? 'rgba(255,255,255,.55)' : '#fff');
      g.textAlign = 'left'; g.fillText(w, x, 0); x += g.measureText(w + sep).width;
    });
    g.restore();
  };
  E.ev = (t, type) => (E.events || []).find(e => e.type === type && t >= e.t0 && t <= e.t1 + (e.tail || 0));
  E.evs = (type) => (E.events || []).filter(e => e.type === type);

  /* ribbon (style I) */
  E.ribbon = (t, cx, cy, prog, tail, p) => {
    E.clear(rbctx); E.clear(rfctx); if (prog - tail < 0.01) return;
    const A = E.acc(), N = 150, R = p.R || 215, top = cy + (p.top || -450), len = p.len || 1200, turns = p.turns || 1.35, wd = 48, ph = p.phase || 0;
    const pts = [], zs = [], ks = [], ws = [];
    for (let i = 0; i < N; i++) {
      const u = tail + (prog - tail) * i / (N - 1), phi = ph + u * turns * 2 * Math.PI + t * 0.55;
      pts.push([cx + R * Math.cos(phi) * (0.85 + 0.15 * Math.sin(u * 3)), top + u * len + 60 * Math.sin(phi)]);
      const z = Math.sin(phi), k = Math.cos(u * 9 + t * 1.3 + ph), ends = clamp((u - tail) / 0.06) * clamp((prog - u) / 0.06);
      zs.push(z); ks.push(k); ws.push(wd * (0.28 + 0.72 * Math.abs(k)) * (1 + 0.18 * z) * (0.25 + 0.75 * ends));
    }
    const L = [], R2 = [];
    for (let i = 0; i < N; i++) {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(N - 1, i + 1)];
      let tx = b[0] - a[0], ty = b[1] - a[1]; const n = Math.hypot(tx, ty) || 1; tx /= n; ty /= n;
      L.push([pts[i][0] - ty * ws[i] / 2, pts[i][1] + tx * ws[i] / 2]); R2.push([pts[i][0] + ty * ws[i] / 2, pts[i][1] - tx * ws[i] / 2]);
    }
    const ex = (P0, Q) => [Q[0] + (Q[0] - P0[0]) * 0.3, Q[1] + (Q[1] - P0[1]) * 0.3];
    for (let i = 0; i < N - 1; i++) {
      const light = 0.5 + 0.5 * ks[i], face = ks[i] >= 0, base = face ? A.c : A.l, hi = face ? A.l : [250, 252, 240];
      let c = mix(A.d, base, Math.min(1, light * 1.4)); c = mix(c, hi, Math.max(0, light - 0.75) * 3);
      const g = zs[i] > 0 ? rfctx : rbctx, l1 = ex(L[i], L[i + 1]), r1 = ex(R2[i], R2[i + 1]);
      g.fillStyle = rgb(c); g.beginPath(); g.moveTo(...L[i]); g.lineTo(...l1); g.lineTo(...r1); g.lineTo(...R2[i]); g.closePath(); g.fill();
    }
  };
  E.RB = RB; E.RF = RF;

  E.update = (t) => {
    E.t = t; E.fi = Math.floor(t * 30);
    const f = data.face || [[216, 341]], i = clamp(Math.floor(t * 2), 0, f.length - 1);
    let x = 0, y = 0, n = 0; for (let j = Math.max(0, i - 2); j < Math.min(f.length, i + 3); j++) { x += f[j][0]; y += f[j][1]; n++; }
    E.fx = x / n; E.fy = y / n;
    if (video.readyState >= 2) {
      const vw = video.videoWidth / 2, vh = video.videoHeight;
      vctx.save(); vctx.setTransform(1, 0, 0, 1, 0, 0); vctx.drawImage(video, 0, 0, vw, vh, 0, 0, V.width, V.height); vctx.restore();
      if (!noMask) {
        try {
          pctx.save(); pctx.setTransform(1, 0, 0, 1, 0, 0); pctx.drawImage(V, 0, 0); pctx.restore();
          mctx.save(); mctx.setTransform(1, 0, 0, 1, 0, 0); mctx.drawImage(video, vw, 0, vw, vh, 0, 0, Mk.width, Mk.height); mctx.restore();
          const pd = pctx.getImageData(0, 0, P.width, P.height), md = mctx.getImageData(0, 0, Mk.width, Mk.height).data, d = pd.data;
          for (let k = 3; k < d.length; k += 4) d[k] = md[k - 3];
          pctx.putImageData(pd, 0, 0);
        } catch (e) { noMask = true; }
      }
    }
  };
  E.draw = (t) => {
    E.update(t);
    const S = STYLES[st.style] || STYLES.I;
    E.reset(octx); E.clear(octx); octx.fillStyle = '#111'; octx.fillRect(0, 0, W, H);
    [t1, t2, t3].forEach(g => { E.reset(g); E.clear(g); });
    S.render(octx, t, E);
    E.reset(octx);
  };
  return E;
}

/* ---------- styles ---------- */
const STYLES = {};
const TL = (E, type) => E.evs(type)[0];

/* I — neon ribbon */
STYLES.I = {name: 'I 霓虹飘带', font: 'serif_italic', accent: '#D4F23A',
  render(o, t, E) {
    const A = E.acc(), st = E.st;
    const zev = E.events.filter(e => ['hook', 'cards', 'feature', 'outro'].includes(e.type) && t >= e.t0).pop();
    const ztar = {hook: 1, cards: 1.12, feature: 1, outro: 1.1}[zev ? zev.type : 'hook'];
    const z = zev ? 1 + (ztar - 1) * easeOut((t - zev.t0) / 0.18) + 0 : 1;
    const g = E.t1; // scene
    E.frame(g, {z, filter: 'blur(9px)'});
    const rib = E.events.find(e => (e.type === 'hook' || e.type === 'cards' || e.type === 'outro') && t >= e.t0 && t <= e.t1 + 0.6 && !(e.type === 'cards' && E.ev(t, 'hook')));
    let span = null;
    const h = TL(E, 'hook'), c = TL(E, 'cards'), ou = TL(E, 'outro');
    if (h && c && t >= h.t0 && t <= c.t1 + 0.6) span = [h.t0 - 0.6, c.t1, 1.1, 0, 1.35];
    else if (ou && t >= ou.t0 - 0.1 && t <= ou.t1 + 0.6) span = [ou.t0 - 0.1, ou.t1, 0.9, 2, 1.1];
    if (span) { const prog = easeOut((t - span[0]) / span[2]), tail = t > span[1] ? easeIO((t - span[1]) / 0.6) * prog : 0; E.ribbon(t, E.fx, E.fy, prog, tail, {phase: span[3], turns: span[4]}); g.drawImage(E.RB, 0, 0, E.RB.width, E.RB.height, 0, 0, W, H); }
    E.person(g, {z});
    if (span) { g.save(); g.shadowColor = 'rgba(0,0,0,.3)'; g.shadowBlur = 16; g.shadowOffsetY = 10; g.drawImage(E.RF, 0, 0, E.RF.width, E.RF.height, 0, 0, W, H); g.restore(); }
    // keyword in film strip
    const k = E.ev(t, 'hook');
    if (k) {
      const y = 615; let [s, a] = pop(t, k.t0, k.t1, 0.3);
      g.save(); g.font = FONTS[st.font].css(125); const tw = Math.min(430, g.measureText(k.big).width); g.restore();
      const sw = Math.min(500, tw + 80), sh = 130;
      within(g, 270, y, s, a * 0.97, -2, q => {
        q.shadowColor = 'rgba(0,0,0,.35)'; q.shadowBlur = 18; q.shadowOffsetY = 8;
        rr(q, -sw / 2, -sh / 2, sw, sh, 9); q.fillStyle = 'rgba(22,24,20,.94)'; q.fill(); q.shadowColor = 'transparent';
        q.save(); rr(q, -sw / 2 + 6, -sh / 2 + 29, sw - 12, sh - 58, 4); q.clip(); q.filter = 'blur(6px)'; q.drawImage(E.V, 0, E.V.height * .16, E.V.width, E.V.height * .31, -sw / 2, -sh / 2 + 29, sw, sh - 58); q.restore();
        q.fillStyle = '#ebebe1'; for (let x = -sw / 2 + 7; x < sw / 2 - 18; x += 20) { rr(q, x, -sh / 2 + 5, 11, 7, 2); q.fill(); rr(q, x, sh / 2 - 12, 11, 7, 2); q.fill(); }
      });
      [s, a] = pop(t, k.t0 + 0.08, k.t1, 0.3);
      within(g, 270, y + 4, s, a, -2, q => bigText(q, k.big, 0, 0, {font: st.font, size: 125, color: A.c, glow: st.glow, stroke: st.stroke, maxW: 430}));
      if (k.small) { [s, a] = pop(t, k.t0 + 0.25, k.t1); g.save(); g.font = UI(800, 29); const w2 = g.measureText(k.small).width; g.restore();
        within(g, 270 + sw / 2 - w2 / 2 - 10, y + sh / 2 + 22, s, a, 0, q => uiText(q, k.small, 0, 0, 29, '#fff', {shadow: true})); }
    }
    const cv = E.ev(t, 'cards');
    if (cv) {
      const kinds = ['pin', 'house', 'search'];
      cv.items.forEach((lab, j) => { const [s, a] = pop(t, cv.t0 + j * 0.14, cv.t1);
        within(g, 270 + (j - 1) * 130, 720 + Math.abs(j - 1) * 20 + 5 * Math.sin(t * 2.6 + j * 1.3), s, a, (j - 1) * -5, q => card(q, kinds[j % 3], lab, 115, 135, A)); });
      const [s, a] = pop(t, cv.t0 + 0.1, cv.t1); pill(g, cv.label, 270, 565, s, a, {dotColor: rgb(A.c)});
    }
    const ov = E.ev(t, 'outro');
    if (ov) {
      const [s, a] = pop(t, ov.t0, ov.t1), nb = 26, bw = 11, gap = 6, by = 780, x0 = 270 - nb * (bw + gap) / 2;
      g.save(); g.globalAlpha = a * 0.85; rr(g, x0 - 15, by - 47, nb * (bw + gap) + 24, 94, 18); g.fillStyle = '#161814'; g.fill();
      g.globalAlpha = a; g.fillStyle = rgb(A.c);
      for (let j = 0; j < nb; j++) { const r = E.rms(E.fi - Math.abs(j - 13)); const hh = (7 + 60 * r * (0.6 + 0.4 * Math.sin(j * 1.7 + t * 9) ** 2)) * s; rr(g, x0 + j * (bw + gap), by - hh / 2, bw, hh, 3); g.fill(); }
      g.restore();
      if (ov.cta) { const [s2, a2] = pop(t, ov.t0 + 0.3, ov.t1); pill(g, ov.cta, 270, 880, s2, a2, {dotColor: rgb(A.c)}); }
    }
    const fe = E.ev(t, 'feature');
    if (!fe) { o.drawImage(E.T1, 0, 0, E.T1.width, E.T1.height, 0, 0, W, H); E.subtitle(o, t); return; }
    // circle mode
    const kk = Math.min(easeIO((t - fe.t0) / 0.45), easeIO((fe.t1 - t) / 0.4)), ccx = 270, ccy = 360, rad = 700 + (165 - 700) * kk;
    o.fillStyle = '#eef0e6'; o.fillRect(0, 0, W, H);
    if (kk > 0.3) {
      const ka = clamp((kk - 0.3) / 0.7), prog = easeOut((t - fe.t0 - 0.3) / (fe.t1 - fe.t0 - 0.6));
      o.save(); o.globalAlpha = ka; o.strokeStyle = rgb(A.d); o.lineWidth = 5; o.beginPath(); o.arc(ccx, ccy, rad + 11, 0, 7); o.stroke();
      o.lineWidth = 1; o.globalAlpha = ka * 0.25; o.beginPath(); o.arc(ccx, ccy, rad + 59, 0, 7); o.stroke();
      o.globalAlpha = ka; o.lineWidth = 7; o.lineCap = 'round'; o.beginPath(); o.arc(ccx, ccy, rad + 59, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * prog); o.stroke();
      const ring = (fe.text || ' ') + ' • ', txt = ring.repeat(Math.max(1, Math.round(60 / Math.max(4, ring.length))));
      o.font = UI(800, 19); o.fillStyle = rgb(A.d); o.textAlign = 'center'; o.textBaseline = 'middle';
      const chars = [...txt], r2 = rad + 35, rot = -(t - fe.t0) * 0.38;
      chars.forEach((ch, i) => { const an = rot + i / chars.length * Math.PI * 2; o.save(); o.translate(ccx + r2 * Math.sin(an), ccy - r2 * Math.cos(an)); o.rotate(an); o.fillText(ch, 0, 0); o.restore(); });
      o.restore();
    }
    o.save(); o.beginPath(); o.arc(ccx, ccy, rad, 0, 7); o.clip(); o.drawImage(E.T1, 0, 0, E.T1.width, E.T1.height, (ccx - E.fx) * kk, (ccy - E.fy) * kk, W, H); o.restore();
    let [s, a] = pop(t, fe.t0 + 0.55, fe.t1 - 0.15); pill(o, fe.label || fe.text, ccx, 640, s, a, {dotColor: rgb(A.c)});
    ['gavel', 'doc', 'web'].forEach((kd, j) => { const [s2, a2] = pop(t, fe.t0 + 0.8 + j * 0.15, fe.t1 - 0.1);
      within(o, 270 + (j - 1) * 125, 760 + 4 * Math.sin(t * 3 + j), s2, a2, 0, q => card(q, kd, (fe.items || [])[j] || '', 105, 125, A)); });
    E.subtitle(o, t);
  }
};

/* A — AI interface demo */
STYLES.A = {name: 'A AI 界面', font: 'montserrat', accent: '#D4F23A',
  render(o, t, E) {
    const A = E.acc(), st = E.st, g = E.t1;
    // stage: dark + vertical light bars
    o.fillStyle = '#101214'; o.fillRect(0, 0, W, H);
    for (let i = 0; i < 14; i++) { const x = i * 40 + 10, gr = o.createLinearGradient(x, 0, x + 40, 0); gr.addColorStop(0, 'rgba(120,150,170,0)'); gr.addColorStop(.5, `rgba(120,150,170,${0.10 + 0.08 * Math.sin(i * 1.7 + t * .6)})`); gr.addColorStop(1, 'rgba(120,150,170,0)'); o.fillStyle = gr; o.fillRect(x, 0, 40, H); }
    // scene with text behind person
    const fe = E.ev(t, 'feature');
    E.frame(g, {});
    const k = E.ev(t, 'hook');
    if (k) { const [s, a] = pop(t, k.t0 + 0.2, k.t1, 0.35); within(g, 270, 150, s, a, 0, q => bigText(q, k.big, 0, 0, {font: st.font, size: 150, color: A.c, glow: true, glowBlur: 30, stroke: st.stroke, maxW: 500})); }
    E.person(g, {});
    E.subtitle(g, t, {y: 800});
    // card
    let cs = 0.72, cy = 520;
    if (fe) { const kz = Math.min(easeOut((t - fe.t0) / 0.35), easeIO((fe.t1 - t) / 0.3)); cs += 0.08 * kz; cy -= 30 * kz; }
    const cw = W * cs, ch = H * cs, shake = fe ? Math.max(0, 1 - (t - fe.t0) / 0.25) * 6 * Math.sin(t * 90) : 0;
    o.save(); o.shadowColor = 'rgba(0,0,0,.55)'; o.shadowBlur = 30; rr(o, 270 - cw / 2 + shake, cy - ch / 2, cw, ch, 22); o.fillStyle = '#000'; o.fill(); o.clip();
    o.drawImage(E.T1, 0, 0, E.T1.width, E.T1.height, 270 - cw / 2 + shake, cy - ch / 2, cw, ch); o.restore();
    o.save(); rr(o, 270 - cw / 2, cy - ch / 2, cw, ch, 22); o.strokeStyle = 'rgba(255,255,255,.18)'; o.lineWidth = 1.5; o.stroke(); o.restore();
    // comment bubble hook
    if (k) { const [s, a] = pop(t, k.t0, k.t1 + 0.2);
      within(o, 270, 92, s, a, 0, q => { q.font = UI(800, 20); const tw = q.measureText(k.label || '').width, w = tw + 90, h = 58;
        q.shadowColor = 'rgba(0,0,0,.4)'; q.shadowBlur = 16; rr(q, -w / 2, -h / 2, w, h, h / 2); q.fillStyle = '#e9ecef'; q.fill(); q.shadowColor = 'transparent';
        q.beginPath(); q.arc(-w / 2 + 30, 0, 15, 0, 7); q.fillStyle = '#9aa1a8'; q.fill();
        uiText(q, 'some_user · 2m', -w / 2 + 54, -11, 11, '#6c737a', {align: 'left', w: 500}); uiText(q, k.label || '', -w / 2 + 54, 9, 20, '#111', {align: 'left'}); }); }
    // checklist
    const cv = E.ev(t, 'cards');
    if (cv) cv.items.forEach((lab, j) => { const [s, a] = pop(t, cv.t0 + j * 0.35, cv.t1);
      within(o, 270, 660 + j * 62, s, a, 0, q => { const w = 330, h = 50; q.shadowColor = 'rgba(0,0,0,.45)'; q.shadowBlur = 14; rr(q, -w / 2, -h / 2, w, h, 12); q.fillStyle = 'rgba(30,33,37,.95)'; q.fill(); q.shadowColor = 'transparent';
        q.beginPath(); q.arc(-w / 2 + 28, 0, 13, 0, 7); q.fillStyle = rgb(A.c); q.fill(); q.save(); q.translate(-w / 2 + 28, 0); icon(q, 'check', 20, '#111'); q.restore();
        uiText(q, lab, -w / 2 + 54, 1, 19, '#f1f3f5', {align: 'left'}); }); });
    // command typing
    if (fe) { const a = fade(t, fe.t0, fe.t1);
      o.save(); o.globalAlpha = a; const w = 440, h = 64, y = 880; rr(o, 270 - w / 2, y - h / 2, w, h, 14); o.fillStyle = '#1b1e22'; o.fill(); o.strokeStyle = 'rgba(255,255,255,.12)'; o.stroke();
      ['#ff5f57', '#febc2e', '#28c840'].forEach((c, i) => { o.beginPath(); o.arc(270 - w / 2 + 18 + i * 14, y - 18, 4, 0, 7); o.fillStyle = c; o.fill(); });
      const cmd = '/effects ' + (fe.text || ''), n = Math.floor(clamp((t - fe.t0 - 0.2) / 1.2) * [...cmd].length);
      const shown = [...cmd].slice(0, n).join('') + ((Math.floor(t * 3) % 2) ? '▍' : ' ');
      uiText(o, shown, 270 - w / 2 + 20, y + 8, 21, rgb(A.c), {align: 'left', font: `700 21px "VE Mono",${CJK_SANS}`}); o.restore(); }
    // CTA button with click
    const ov = E.ev(t, 'outro');
    if (ov) { const [s, a] = pop(t, ov.t0, ov.t1), saved = t > ov.t0 + 1.2;
      within(o, 270, 880, s * (saved && t < ov.t0 + 1.35 ? 0.94 : 1), a, 0, q => { const w = 300, h = 64; rr(q, -w / 2, -h / 2, w, h, 32); q.fillStyle = saved ? '#2b2f34' : rgb(A.c); q.fill();
        uiText(q, saved ? '✓ Saved' : (ov.cta || 'Comment EDIT') + '  ▸', 0, 1, 21, saved ? '#fff' : '#111'); });
      const cx = 270 + 60 + 60 * (1 - easeOut((t - ov.t0 - 0.4) / 0.7)), cyy = 900 + 50 * (1 - easeOut((t - ov.t0 - 0.4) / 0.7));
      if (t > ov.t0 + 0.4) { o.save(); o.globalAlpha = a; o.fillStyle = '#fff'; o.strokeStyle = '#111'; o.lineWidth = 1.5; o.beginPath(); o.moveTo(cx, cyy); o.lineTo(cx, cyy + 24); o.lineTo(cx + 7, cyy + 18); o.lineTo(cx + 15, cyy + 20); o.closePath(); o.fill(); o.stroke(); o.restore(); }
    }
  }
};

/* B — editorial serif */
STYLES.B = {name: 'B 杂志衬线', font: 'playfair_italic', accent: '#445A3F',
  render(o, t, E) {
    const A = E.acc(), st = E.st, cream = '#F8F5DC';
    E.frame(o, {z: 1 + 0.04 * clamp(t / 11)});
    const k = E.ev(t, 'hook');
    if (k) { // numbered squares + title
      for (let i = 0; i < 3; i++) { const [s, a] = pop(t, k.t0 + i * 0.15, k.t1);
        within(o, 60, 230 + i * 58, s, a, 0, q => { q.fillStyle = rgb(A.c); q.fillRect(-20, -20, 40, 40); uiText(q, String(i + 1), 0, 1, 20, cream, {font: `700 20px "VE Playfair",serif`}); }); }
      const la = fade(t, k.t0 + 0.4, k.t1); o.save(); o.globalAlpha = la; o.strokeStyle = cream; o.lineWidth = 1.2; o.beginPath(); o.moveTo(82, 230); o.lineTo(82 + 60 * easeOut((t - k.t0 - 0.4) / 0.4), 230); o.stroke(); o.restore();
      const words = chunks(k.big); let x = 160;
      o.save(); o.font = FONTS[st.font].css(62); const tw = o.measureText(k.big).width; o.restore();
      const [s, a] = [1, fade(t, k.t0 + 0.45, k.t1)];
      within(o, 150 + Math.min(360, tw) / 2, 232 - 8 * (1 - easeOut((t - k.t0 - 0.45) / 0.4)), s, a, 0, q => bigText(q, k.big, 0, 0, {font: st.font, size: 62, color: cream, glow: st.glow, glowColor: hex(cream), stroke: st.stroke, maxW: 360}));
      if (k.small) uiText(o, k.small, 152, 280, 22, cream, {align: 'left', font: `italic 400 22px "VE Playfair",${CJK_SERIF}`, shadow: true});
    }
    const cv = E.ev(t, 'cards');
    if (cv) cv.items.forEach((w, j) => { const t0 = cv.t0 + j * 0.7, a = fade(t, t0, cv.t1), u = easeOut((t - t0) / 0.45);
      if (a <= 0) return; o.save(); o.globalAlpha = a; o.filter = `blur(${(1 - u) * 4}px)`;
      const y = 560 + j * 78 + (1 - u) * 14, big = j === 1;
      if (big) bigText(o, w, 270, y, {font: st.font, size: 70, color: u < 0.6 ? 'rgba(248,245,220,.55)' : cream, maxW: 440, glow: st.glow, glowColor: hex(cream)});
      else uiText(o, w, 270, y, 38, u < 0.6 ? 'rgba(248,245,220,.55)' : cream, {font: `700 38px "VE Playfair",${CJK_SERIF}`, shadow: true, maxW: 460});
      o.restore(); });
    const fe = E.ev(t, 'feature');
    if (fe) { const mid = fe.t0 + (fe.t1 - fe.t0) * 0.5;
      if (t < mid) { const a = fade(t, fe.t0, mid, 0.12, 0.08); o.save(); o.globalAlpha = a; o.fillStyle = rgb(A.c); o.fillRect(0, 0, W, H);
        const u = easeOut((t - fe.t0) / 0.6); o.save(); o.beginPath(); o.rect(0, 0, W, 620); o.clip();
        const gr = o.createLinearGradient(0, 330, 0, 600); gr.addColorStop(0, cream); gr.addColorStop(1, 'rgba(248,245,220,0)');
        o.fillStyle = gr; o.font = `900 300px "VE Playfair",serif`; o.textAlign = 'center'; o.textBaseline = 'alphabetic'; o.fillText('01', 270, 600 + (1 - u) * 200); o.restore();
        chunks(fe.text).forEach((w, i, arr) => { const aa = fade(t, fe.t0 + 0.4 + i * 0.12, mid); o.globalAlpha = a * aa; });
        o.globalAlpha = a * fade(t, fe.t0 + 0.4, mid); uiText(o, fe.text || '', 270, 700, 40, cream, {font: `italic 700 40px "VE Playfair",${CJK_SERIF}`, maxW: 470}); o.restore(); }
      else { const a = fade(t, mid, fe.t1, 0.08, 0.15); o.save(); o.globalAlpha = a; o.fillStyle = cream; o.fillRect(0, 0, W, H);
        uiText(o, '“', 270, 360, 120, rgb(A.c), {font: `900 120px "VE Playfair",serif`}); uiText(o, fe.quote || '', 270, 470, 36, rgb(A.c), {font: `italic 700 36px "VE Playfair",${CJK_SERIF}`, maxW: 460}); o.restore(); }
    }
    const ov = E.ev(t, 'outro');
    if (ov) { const a = fade(t, ov.t0, ov.t1); o.save(); o.globalAlpha = a * 0.55; const gr = o.createLinearGradient(0, 640, 0, 960); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(1, 'rgba(20,28,18,1)'); o.fillStyle = gr; o.fillRect(0, 640, W, 320); o.restore();
      o.save(); o.globalAlpha = a; uiText(o, 'Comment', 270, 770, 26, cream, {font: `italic 400 26px "VE Playfair",serif`});
      bigText(o, ov.cta || 'edit', 270, 825, {font: st.font, size: 64, color: cream, maxW: 460, glow: st.glow, glowColor: hex(cream)}); o.restore(); }
    E.subtitle(o, t, {font: `700 28px "VE Playfair",${CJK_SERIF}`});
  }
};

/* C — premium before/after */
STYLES.C = {name: 'C 高端对比', font: 'montserrat', accent: '#5FE0C8',
  render(o, t, E) {
    const A = E.acc(), st = E.st, g = E.t1, navy = '#0d1b2e';
    o.fillStyle = navy; o.fillRect(0, 0, W, H);
    const gl = o.createLinearGradient(0, 0, W, H); gl.addColorStop(0, 'rgba(95,224,200,.12)'); gl.addColorStop(1, 'rgba(95,224,200,0)'); o.fillStyle = gl; o.fillRect(0, 0, W, H);
    // FINAL scene: darkened bg + vignette, person normal
    E.frame(g, {filter: 'brightness(.62)'});
    const vg = g.createRadialGradient(270, 420, 120, 270, 480, 620); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,10,25,.75)'); g.fillStyle = vg; g.fillRect(0, 0, W, H);
    E.person(g, {});
    const k = E.ev(t, 'hook');
    if (k) { if (k.small) { const a = fade(t, k.t0, k.t1); g.save(); g.globalAlpha = a; uiText(g, k.small, 270, 590, 30, '#fff', {font: `300 30px "VE Montserrat",${CJK_SANS}`, shadow: true}); g.restore(); }
      const u = easeOut((t - k.t0 - 0.2) / 0.5), a = fade(t, k.t0 + 0.2, k.t1);
      g.save(); g.globalAlpha = a; g.beginPath(); g.rect(0, 600, W * u, 120); g.clip(); bigText(g, k.big, 270, 655, {font: st.font, size: 92, color: A.c, glow: st.glow, stroke: st.stroke, maxW: 480}); g.restore();
      g.save(); g.globalAlpha = a; g.shadowColor = rgb(A.c); g.shadowBlur = 16; g.fillStyle = rgb(A.c); rr(g, 270 - 150 * u, 712, 300 * u, 6, 3); g.fill(); g.restore(); }
    const cv = E.ev(t, 'cards');
    if (cv) cv.items.forEach((lab, j) => { const [s, a] = pop(t, cv.t0 + j * 0.25, cv.t1); const y = 640 + j * 82 + (1 - easeOut((t - cv.t0 - j * 0.25) / 0.4)) * 40;
      within(g, 270, y, 1, a, 0, q => { const w = 400, h = 66; rr(q, -w / 2, -h / 2, w, h, 16); q.fillStyle = 'rgba(255,255,255,.14)'; q.fill(); q.strokeStyle = 'rgba(255,255,255,.35)'; q.lineWidth = 1; q.stroke();
        q.beginPath(); q.arc(-w / 2 + 34, 0, 19, 0, 7); q.fillStyle = rgb(A.c); q.fill(); q.save(); q.translate(-w / 2 + 34, 0); icon(q, ['search', 'doc', 'gavel'][j % 3], 22, navy); q.restore();
        uiText(q, lab, -w / 2 + 66, 1, 22, '#fff', {align: 'left', font: `900 22px "VE Montserrat",${CJK_SANS}`}); }); });
    E.subtitle(g, t);
    // layout: raw card + final card
    const fe = E.ev(t, 'feature');
    o.save(); o.translate(92, 250); o.rotate(-4 * Math.PI / 180); rr(o, -70, -124, 140, 248, 14); o.fillStyle = '#000'; o.fill(); o.clip(); o.filter = 'saturate(.6) brightness(.9)'; o.drawImage(E.V, 0, 0, E.V.width, E.V.height, -70, -124, 140, 248); o.restore();
    pill(o, 'NO EDIT', 92, 395, 1, 1, {size: 13, bg: 'rgba(255,255,255,.12)', fg: '#dfe7ef', dot: false});
    const fx = 195, fy = 130, fw = 320, fh = 569;
    o.save(); o.shadowColor = 'rgba(95,224,200,.35)'; o.shadowBlur = 40; rr(o, fx, fy, fw, fh, 22); o.fillStyle = '#000'; o.fill(); o.restore();
    o.save(); rr(o, fx, fy, fw, fh, 22); o.clip(); o.drawImage(E.T1, 0, 0, E.T1.width, E.T1.height, fx, fy, fw, fh); o.restore();
    pill(o, 'FINAL', fx + 40, fy + 26, 1, 1, {size: 12, bg: rgb(A.c), fg: navy, dot: false});
    uiText(o, 'PREMIUM PERCEPTION', 270, 80, 15, 'rgba(255,255,255,.85)', {font: `300 15px "VE Montserrat",sans-serif`});
    // big readable copy under cards
    if (k) { const a = fade(t, k.t0 + 0.3, k.t1); o.save(); o.globalAlpha = a; bigText(o, k.big, 270, 790, {font: st.font, size: 64, color: '#fff', maxW: 470, glow: st.glow, glowColor: A.c}); o.restore(); }
    if (cv) { const a = fade(t, cv.t0, cv.t1); o.save(); o.globalAlpha = a; uiText(o, cv.label || '', 270, 790, 30, rgb(A.c), {font: `900 30px "VE Montserrat",${CJK_SANS}`, maxW: 470}); o.restore(); }
    if (fe) { const a = fade(t, fe.t0, fe.t1, 0.1, 0.12); o.save(); o.globalAlpha = a; const gr = o.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, rgb(A.l)); gr.addColorStop(1, '#ffffff'); o.fillStyle = gr; o.fillRect(0, 0, W, H);
      const u = easeOut((t - fe.t0) / 0.5); uiText(o, '1', 270, 340 + (1 - u) * 40, 260, navy, {font: `900 260px "VE Montserrat",sans-serif`});
      uiText(o, fe.text || '', 270, 560, 34, navy, {font: `300 34px "VE Montserrat",${CJK_SANS}`, maxW: 470});
      bigText(o, fe.label || '', 270, 625, {font: st.font, size: 64, color: navy, shadow: false, maxW: 470}); o.restore(); }
    const ov = E.ev(t, 'outro');
    if (ov) { E.flash(o, t, ov.t0, 0.25); const [s, a] = pop(t, ov.t0 + 0.15, ov.t1);
      within(o, 270, 800, s, a, 0, q => { const w = 400, h = 92; rr(q, -w / 2, -h / 2, w, h, 20); q.fillStyle = 'rgba(255,255,255,.95)'; q.fill();
        uiText(q, 'COMMENT', 0, -18, 14, '#53606c', {font: `300 14px "VE Montserrat",sans-serif`}); uiText(q, ov.cta || '', 0, 14, 30, navy, {font: `900 30px "VE Montserrat",${CJK_SANS}`, maxW: 360}); }); }
  }
};

/* D — listicle */
STYLES.D = {name: 'D 清单教学', font: 'sans_black', accent: '#FFD84D',
  render(o, t, E) {
    const A = E.acc(), st = E.st;
    const looks = ['none', 'sepia(.5) saturate(1.3) brightness(1.05)', 'hue-rotate(190deg) saturate(.7) brightness(.95)', 'contrast(1.35) brightness(.85)', 'grayscale(1) contrast(1.2)', 'brightness(.7) saturate(1.4)', 'hue-rotate(320deg) saturate(1.2)'];
    const cv = E.ev(t, 'cards'), fe = E.ev(t, 'feature');
    let li = -1; if (cv || fe) { const s0 = (cv || fe).t0; li = Math.floor((t - TL(E, 'cards').t0) / 0.8); }
    const filt = li >= 0 ? looks[(li % (looks.length - 1)) + 1] : 'none';
    E.frame(o, {filter: filt});
    if (li >= 0 && ((t - TL(E, 'cards').t0) % 0.8) < 0.06) E.flash(o, ((t - TL(E, 'cards').t0) % 0.8), 0, 0.06, 'rgba(255,255,255,.5)');
    // list top-left
    const items = (TL(E, 'feature') || {}).items || [];
    const k = E.ev(t, 'hook');
    const showList = t >= (TL(E, 'hook') || {t0: 0}).t0;
    if (showList) {
      const title = (TL(E, 'hook') || {}).big || '';
      const a = fade(t, (TL(E, 'hook') || {t0: 0}).t0, 99);
      o.save(); o.globalAlpha = a; o.fillStyle = 'rgba(0,0,0,.42)'; rr(o, 14, 64, 150, 52 + items.length * 28, 12); o.fill();
      uiText(o, title, 26, 88, 20, '#fff', {align: 'left', font: FONTS[st.font].css(20), maxW: 130});
      const cur = li >= 0 ? li % items.length : -1;
      items.forEach((it, i) => { const on = i === cur, done = li >= 0 && (li >= items.length || i < cur);
        uiText(o, `${i + 1}. ${it}`, 26, 122 + i * 28, on ? 17 : 14, on ? rgb(A.c) : (done ? '#fff' : 'rgba(255,255,255,.55)'), {align: 'left', w: on ? 800 : 600, maxW: 130, shadow: true}); });
      o.restore();
    }
    // reference mini window
    if (li >= 0) { const a = fade(t, TL(E, 'cards').t0, (fe || cv).t1);
      o.save(); o.globalAlpha = a; rr(o, 18, 640, 150, 200, 12); o.fillStyle = '#000'; o.fill(); o.save(); o.clip(); o.filter = filt + ' blur(1px)'; o.drawImage(E.V, 0, E.V.height * .2, E.V.width, E.V.height * .5, 18 - 30, 640, 210, 200); o.restore();
      uiText(o, '参考 · ' + (items[li % Math.max(1, items.length)] || ''), 93, 828, 12, '#fff', {shadow: true, maxW: 140}); o.restore(); }
    if (k && !showList) {}
    const ov = E.ev(t, 'outro');
    if (ov) { const word = (ov.cta || '').toUpperCase(), n = Math.floor(clamp((t - ov.t0 - 0.2) / 0.8) * [...word].length);
      o.save(); o.globalAlpha = fade(t, ov.t0, ov.t1); o.fillStyle = 'rgba(0,0,0,.45)'; o.fillRect(0, 700, W, 140);
      uiText(o, 'comment', 270, 735, 20, '#fff', {w: 500});
      const shown = [...word].slice(0, n).join(''); bigText(o, shown + ((Math.floor(t * 3) % 2) ? '|' : ' '), 270, 790, {font: st.font, size: 60, color: A.c, maxW: 470, glow: st.glow, stroke: st.stroke}); o.restore(); }
    E.subtitle(o, t, {y: 880, size: 24});
  }
};

/* E — minimal talking head */
STYLES.E = {name: 'E 极简口播', font: 'sans_black', accent: '#FFD84D',
  render(o, t, E) {
    const A = E.acc(), st = E.st;
    const z = Math.floor(t / 2.5) % 2 ? 1.1 : 1.0;
    E.frame(o, {z});
    const k = E.ev(t, 'hook');
    if (k) { const [s, a] = pop(t, k.t0, k.t1); within(o, 270, 700, s, a, 0, q => bigText(q, k.big, 0, 0, {font: st.font, size: 88, color: A.c, glow: st.glow, stroke: st.stroke, maxW: 480})); if (k.small) uiText(o, k.small, 270, 640, 28, '#fff', {shadow: true}); }
    const cv = E.ev(t, 'cards');
    if (cv) { const n = cv.items.length, per = (cv.t1 - cv.t0) / n, j = clamp(Math.floor((t - cv.t0) / per), 0, n - 1), [s, a] = pop(t, cv.t0 + j * per, cv.t0 + (j + 1) * per - 0.05, 0.22, 0.08);
      within(o, 270, 720, s, a, 0, q => bigText(q, cv.items[j], 0, 0, {font: st.font, size: 72, color: '#fff', glow: st.glow, glowColor: A.c, stroke: st.stroke, maxW: 480})); }
    const fe = E.ev(t, 'feature');
    if (fe) { // B-roll style inset card
      const [s, a] = pop(t, fe.t0, fe.t1); within(o, 270, 330, s, a, -3, q => { rr(q, -150, -100, 300, 200, 16); q.fillStyle = '#fff'; q.fill(); q.save(); rr(q, -142, -92, 284, 184, 12); q.clip(); q.filter = 'saturate(1.1)'; q.drawImage(E.V, 0, E.V.height * .25, E.V.width, E.V.height * .35, -142, -92, 284, 184); q.restore(); });
      const a2 = fade(t, fe.t0 + 0.2, fe.t1); o.save(); o.globalAlpha = a2; bigText(o, fe.text || '', 270, 470, {font: st.font, size: 52, color: '#fff', glow: st.glow, glowColor: A.c, stroke: st.stroke, maxW: 470}); o.restore(); }
    const ov = E.ev(t, 'outro');
    if (ov) { const [s, a] = pop(t, ov.t0, ov.t1); within(o, 270, 780, s, a, 0, q => { const w = 420, h = 80; rr(q, -w / 2, -h / 2, w, h, 40); q.fillStyle = rgb(A.c); q.fill(); uiText(q, ov.cta || '', 0, 1, 30, lum(A.c) > 150 ? '#111' : '#fff', {font: FONTS[st.font].css(34), maxW: 380}); }); }
    const sv = st.subs; st.subs = true; E.subtitle(o, t, {y: 860, hi: rgb(A.c)}); st.subs = sv;
  }
};

/* F — kinetic type on white */
STYLES.F = {name: 'F 动态排版', font: 'mono', accent: '#D4FF00',
  render(o, t, E) {
    const A = E.acc(), st = E.st, ink = '#232323';
    o.fillStyle = '#f7f7f5'; o.fillRect(0, 0, W, H);
    const fe = E.ev(t, 'feature');
    // person, scaled down, on white
    const ps = fe ? 0.7 : 0.86, px = fe ? 340 : 270;
    o.save(); o.translate(px, H + 30); o.scale(ps, ps); o.translate(-E.fx, -H); o.shadowColor = 'rgba(0,0,0,.12)'; o.shadowBlur = 30; o.shadowOffsetY = 20; E.person(o, {}); o.restore();
    { const gr = o.createLinearGradient(0, 800, 0, H); gr.addColorStop(0, 'rgba(247,247,245,0)'); gr.addColorStop(1, 'rgba(247,247,245,1)'); o.fillStyle = gr; o.fillRect(0, 800, W, 160); }
    const k = E.ev(t, 'hook');
    if (k) { const word = k.big || '', dec = clamp((t - k.t0) / 0.8), chars = [...word], glyphs = 'abcdefghijklmnopqrstuvwxyz#?%&*';
      const shown = chars.map((c, i) => (i / chars.length < dec || c === ' ') ? c : glyphs[Math.floor(hash(i + Math.floor(t * 20)) * glyphs.length)]).join('');
      const a = fade(t, k.t0, k.t1, 0.05, 0.1); o.save(); o.globalAlpha = a;
      const w = bigText(o, shown, 270, 170, {font: st.font, size: 92, color: ink, shadow: false, glow: st.glow, glowColor: A.c, stroke: st.stroke, maxW: 440});
      const bx = w / 2 + 22, by = 62, L = 22; o.strokeStyle = rgb(A.d); o.lineWidth = 5; o.lineCap = 'square';
      [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(([sx, sy]) => { o.beginPath(); o.moveTo(270 + sx * bx, 170 + sy * by - sy * L); o.lineTo(270 + sx * bx, 170 + sy * by); o.lineTo(270 + sx * bx - sx * L, 170 + sy * by); o.stroke(); });
      if (dec >= 1) { o.fillStyle = rgb(A.d); o.beginPath(); o.arc(270 + w / 2 + 8, 200, 7, 0, 7); o.fill(); }
      o.restore();
      if (k.small) { const [s, a2] = pop(t, k.t0 + 0.6, k.t1); within(o, 150, 80, s, a2, -8, q => { q.font = `700 26px "VE Mono",${CJK_SANS}`; const tw = q.measureText(k.small).width; q.fillStyle = rgb(A.c); q.fillRect(-tw / 2 - 12, -20, tw + 24, 40); uiText(q, k.small, 0, 1, 26, '#111', {font: `700 26px "VE Mono",${CJK_SANS}`}); }); }
    }
    const cv = E.ev(t, 'cards');
    if (cv) [0, 1].forEach(j => { const [s, a] = pop(t, cv.t0 + j * 0.35, cv.t1), win = j === 1;
      within(o, 150 + j * 240, 190, s, a, j ? 4 : -4, q => { const w = 200, h = 120; rr(q, -w / 2, -h / 2, w, h, 6); q.fillStyle = win ? rgb(A.c) : '#fff'; q.fill(); q.strokeStyle = ink; q.lineWidth = 2; q.stroke();
        q.save(); q.translate(0, -18); if (win) icon(q, 'heart', 36, ink); else { q.strokeStyle = ink; q.lineWidth = 3; q.beginPath(); q.moveTo(0, 11); q.bezierCurveTo(-20, -2, -9, -17, 0, -6); q.bezierCurveTo(9, -17, 20, -2, 0, 11); q.stroke(); } q.restore();
        uiText(q, cv.items[j] || '', 0, 32, 18, ink, {font: `700 18px "VE Mono",${CJK_SANS}`, maxW: 180}); }); });
    if (fe) { // picker wheel
      const list = fe.items || [], n = list.length, u = clamp((t - fe.t0 - 0.3) / (fe.t1 - fe.t0 - 0.8)) * (n - 1), cur = Math.round(u);
      const a = fade(t, fe.t0, fe.t1); o.save(); o.globalAlpha = a;
      uiText(o, fe.text || '', 40, 250, 30, ink, {align: 'left', font: `700 30px "VE Mono",${CJK_SANS}`, maxW: 460});
      list.forEach((it, i) => { const d = i - u, y = 420 + d * 56, on = i === cur; if (Math.abs(d) > 2.4) return;
        o.globalAlpha = a * (1 - Math.abs(d) * 0.3); uiText(o, it, 70, y, on ? 34 : 24, on ? ink : '#9a9a96', {align: 'left', font: `700 ${on ? 34 : 24}px "VE Mono",${CJK_SANS}`, maxW: 300}); });
      o.globalAlpha = a; o.fillStyle = rgb(A.d); o.beginPath(); o.moveTo(40, 410); o.lineTo(56, 420); o.lineTo(40, 430); o.fill(); o.restore();
      const pb = clamp((t - fe.t0) / 0.6); if (pb < 1) { o.save(); for (let i = 0; i < 40; i++) { const an = hash(i) * 7, r = 40 + pb * 260 * hash(i + 9); o.globalAlpha = 1 - pb; o.shadowColor = rgb(A.c); o.shadowBlur = 10; o.fillStyle = rgb(A.c); o.fillRect(E.fx + Math.cos(an) * r, E.fy - 40 + Math.sin(an) * r, 10, 10); } o.restore(); }
    }
    const ov = E.ev(t, 'outro');
    if (ov) { const a = fade(t, ov.t0, ov.t1, 0.12, 0.1); o.save(); o.globalAlpha = a; o.fillStyle = '#fafaf8'; o.fillRect(0, 0, W, H);
      const u = easeOut((t - ov.t0) / 0.4); uiText(o, ov.brand || '', 250, 470, 46, ink, {font: `700 46px "VE Mono",${CJK_SANS}`, maxW: 300});
      within(o, 380, 520, u, 1, -7, q => { q.font = `700 30px "VE Mono",${CJK_SANS}`; const tw = q.measureText(ov.cta || '').width; q.fillStyle = rgb(A.c); q.fillRect(-tw / 2 - 12, -22, tw + 24, 44); uiText(q, ov.cta || '', 0, 1, 30, '#111', {font: `700 30px "VE Mono",${CJK_SANS}`}); }); o.restore(); }
    E.subtitle(o, t, {font: `700 26px "VE Mono",${CJK_SANS}`, y: 880});
    // subtitles on white need dark text
  }
};

/* G — warm studio showcase (scale in / out) */
STYLES.G = {name: 'G 暖色套框', font: 'montserrat_italic', accent: '#B4552F',
  render(o, t, E) {
    const A = E.acc(), st = E.st, g = E.t1;
    const h = TL(E, 'hook'), sIn = (h ? h.t1 : 1.8) - 0.2;
    // inner scene
    const fe = E.ev(t, 'feature');
    const iz = fe ? 1 + 0.12 * easeIO((t - fe.t0) / (fe.t1 - fe.t0)) : 1;
    E.frame(g, {z: iz});
    const k = E.ev(t, 'hook');
    if (k) { const word = k.big || '', n = Math.ceil(clamp((t - k.t0) / 0.7) * [...word].length);
      const a = fade(t, k.t0, k.t1 + 0.3); g.save(); g.globalAlpha = a;
      if (k.small) uiText(g, k.small, 110, 48, 26, '#fff', {align: 'left', font: `italic 300 26px "VE Montserrat",${CJK_SANS}`, shadow: true});
      bigText(g, [...word].slice(0, n).join(''), 270, 112, {font: st.font, size: 120, color: A.c, glow: st.glow, stroke: st.stroke, maxW: 480});
      for (let i = 0; i < 14; i++) { const x = 40 + hash(i) * 460, y = 40 + hash(i + 3) * 150, s2 = 6 + hash(i + 7) * 10; if (hash(i + 11) < n / Math.max(1, word.length)) { g.fillStyle = rgb(A.c, 0.8); g.fillRect(x, y, s2, s2); } }
      g.restore(); }
    E.person(g, {z: iz});
    const cv = E.ev(t, 'cards');
    if (cv) cv.items.forEach((lab, j) => { const [s, a] = pop(t, cv.t0 + j * 0.3, cv.t1);
      within(g, [95, 450, 455][j], [600, 560, 790][j], s, a, [-6, 5, 3][j], q => { q.shadowColor = 'rgba(0,0,0,.3)'; q.shadowBlur = 14; q.shadowOffsetY = 6; q.fillStyle = '#fff'; q.fillRect(-80, -66, 160, 150); q.shadowColor = 'transparent';
        q.save(); q.beginPath(); q.rect(-72, -58, 144, 108); q.clip(); q.filter = ['sepia(.4)', 'saturate(1.3)', 'grayscale(1)'][j]; q.drawImage(E.V, 0, E.V.height * (.15 + j * .15), E.V.width, E.V.height * .3, -100, -58, 200, 108); q.restore();
        uiText(q, lab, 0, 67, 16, '#3a2a20', {font: `italic 900 16px "VE Montserrat",${CJK_SANS}`, maxW: 150}); }); });
    if (fe) { const u = clamp((t - fe.t0) / 0.9); g.save(); g.strokeStyle = '#fff'; g.lineWidth = 6; g.lineCap = 'round'; g.shadowColor = 'rgba(0,0,0,.25)'; g.shadowBlur = 8; g.beginPath();
      for (let i = 0; i <= 60 * u; i++) { const yy = -20 + i * 17, xx = 270 + 160 * Math.sin(i * 0.22 + 1); i ? g.lineTo(xx, yy) : g.moveTo(xx, yy); } g.stroke(); g.restore();
      const a = fade(t, fe.t0 + 0.3, fe.t1); g.save(); g.globalAlpha = a; bigText(g, fe.text || '', 270, 740, {font: st.font, size: 80, color: '#fff', glow: st.glow, glowColor: A.c, stroke: st.stroke, maxW: 480}); g.restore(); }
    E.subtitle(g, t);
    // stage + scale animation
    const k2 = easeOut((t - sIn) / 0.3), cs = 1 - 0.34 * k2, cw = W * cs, ch = H * cs, cx = 270 + 40 * k2, cy = 480 - 10 * k2;
    o.fillStyle = '#e9e7e2'; o.fillRect(0, 0, W, H);
    if (k2 > 0) { o.save(); o.globalAlpha = k2; o.translate(108, 330); o.rotate(-5 * Math.PI / 180); o.shadowColor = 'rgba(0,0,0,.2)'; o.shadowBlur = 12; rr(o, -78, -138, 156, 276, 14); o.fillStyle = '#000'; o.fill(); o.shadowColor = 'transparent'; o.clip(); o.filter = 'grayscale(1)'; o.drawImage(E.V, 0, 0, E.V.width, E.V.height, -78, -138, 156, 276); o.restore();
      o.save(); o.globalAlpha = k2; pill(o, 'Raw footage', 108, 490, 1, 1, {size: 13, dot: false, bg: '#fff'}); o.restore(); }
    o.save(); o.shadowColor = `rgba(0,0,0,${0.3 * k2})`; o.shadowBlur = 30 * k2; o.shadowOffsetY = 14 * k2; rr(o, cx - cw / 2, cy - ch / 2, cw, ch, 26 * k2); o.fillStyle = '#000'; o.fill(); o.restore();
    o.save(); rr(o, cx - cw / 2, cy - ch / 2, cw, ch, 26 * k2); o.clip(); o.drawImage(E.T1, 0, 0, E.T1.width, E.T1.height, cx - cw / 2, cy - ch / 2, cw, ch); o.restore();
    if (k2 > 0) { const badge = (TL(E, 'cards') || {}).label || ''; o.save(); o.globalAlpha = k2; pill(o, badge, cx, cy - ch / 2 - 2, 1, 1, {size: 15, bg: '#1f1b18', fg: '#fff', dotColor: rgb(A.c)});
      const ov0 = TL(E, 'outro'); uiText(o, ov0 ? ov0.ctaLine : '', 270, 905, 18, '#2e2925', {w: 600, maxW: 500}); o.restore(); }
    const ov = E.ev(t, 'outro');
    if (ov) { const [s, a] = pop(t, ov.t0 + 0.2, ov.t1, 0.35); within(o, 400, 640, s, a, 4, q => { q.shadowColor = 'rgba(0,0,0,.3)'; q.shadowBlur = 18; q.fillStyle = '#fff'; q.fillRect(-95, -125, 190, 250); q.shadowColor = 'transparent'; q.save(); q.beginPath(); q.rect(-85, -115, 170, 200); q.clip(); q.drawImage(E.V, E.V.width * .15, E.V.height * .2, E.V.width * .7, E.V.height * .5, -85, -115, 170, 200); q.restore(); uiText(q, ov.cta || '', 0, 106, 18, rgb(A.d), {font: `italic 900 18px "VE Montserrat",${CJK_SANS}`, maxW: 170}); }); }
  }
};

/* H — high-density effects, text behind person */
STYLES.H = {name: 'H 高密度特效', font: 'anton', accent: '#FF7A1A',
  render(o, t, E) {
    const A = E.acc(), st = E.st, blue = [47, 107, 255], g = E.t1;
    const fe = E.ev(t, 'feature'), bw = fe && t < fe.t0 + 1.4;
    const z = 1.04 + 0.03 * Math.sin(t * 0.8);
    E.frame(o, {z, filter: bw ? 'grayscale(1) contrast(1.1)' : 'none'});
    // behind-person layer drawn on o, then person over
    const behind = [], front = [];
    const k = E.ev(t, 'hook');
    if (k) { const mid = k.t0 + (k.t1 - k.t0) * 0.5;
      if (t < mid) front.push(q => { const a = fade(t, k.t0, mid); q.globalAlpha = a; if (k.small) uiText(q, k.small, 270, 560, 30, '#fff', {shadow: true, w: 800}); uiText(q, k.label || '', 270, 605, 40, rgb(A.c), {shadow: true, w: 800, maxW: 480}); bigText(q, (k.big || '').toUpperCase(), 270, 675, {font: st.font, size: 100, color: rgb(blue), glow: st.glow, stroke: st.stroke, maxW: 480}); });
      else behind.push(q => { const [s, a] = pop(t, mid, k.t1); within(q, 270, 175, s, a, 0, r => bigText(r, (k.big || '').toUpperCase(), 0, 0, {font: st.font, size: 230, color: '#141414', shadow: false, glow: st.glow, glowColor: A.c, maxW: 520})); }); }
    const cv = E.ev(t, 'cards');
    if (cv) { const mid = cv.t0 + 1.0;
      if (t < mid) { const u = easeOut((t - cv.t0) / 0.35); behind.push(q => { q.fillStyle = rgb(A.c); q.beginPath(); q.arc(270, 300, 700 * u, 0, 7); q.fill(); if (u > 0.6) bigText(q, cv.num || '10', 270, 190, {font: st.font, size: 330, color: '#fff', shadow: false, maxW: 520}); }); }
      else { const v = Math.round(easeOut((t - mid) / 1.3) * (cv.count || 450000));
        front.push(q => { const [s, a] = pop(t, mid, cv.t1); within(q, 270, 640, s, a, 0, r => bigText(r, v.toLocaleString('en-US'), 0, 0, {font: st.font, size: 110, color: '#fff', glow: true, glowColor: A.c, maxW: 500}));
          within(q, 270, 715, 1, a, 0, r => uiText(r, cv.label || '', 0, 0, 30, rgb(A.c), {shadow: true, w: 800, maxW: 480}));
          for (let i = 0; i < 9; i++) { const tt = (t - mid - i * 0.15); if (tt < 0) continue; const p = (tt % 1.4) / 1.4; q.save(); q.globalAlpha = a * (1 - p); q.translate(380 + 50 * Math.sin(i * 2 + p * 4), 640 - p * 300); icon(q, 'heart', 30 + hash(i) * 14, '#ff3b5c'); q.restore(); }
          [[150, 150, -6], [390, 140, 5]].forEach(([x, y, r], i) => { const [s2, a2] = pop(t, mid + i * 0.15, cv.t1); within(q, x, y, s2, a2, r, w => { w.shadowColor = 'rgba(0,0,0,.4)'; w.shadowBlur = 12; w.fillStyle = '#fff'; w.fillRect(-62, -100, 124, 200); w.shadowColor = 'transparent'; w.save(); w.beginPath(); w.rect(-57, -95, 114, 170); w.clip(); w.filter = i ? 'hue-rotate(40deg)' : 'saturate(1.3)'; w.drawImage(E.V, 0, 0, E.V.width, E.V.height, -57, -95, 114, 203); w.restore(); uiText(w, '▶ ' + (i ? '1.2M' : '450K'), 0, 88, 13, '#111', {w: 800}); }); }); }); } }
    if (fe) { const m1 = fe.t0 + 1.4, m2 = fe.t0 + 2.2;
      if (t < m1) front.push(q => { const a = fade(t, fe.t0, m1, 0.1, 0.05); q.globalAlpha = a; const it = fe.items || []; bigText(q, (it[0] || '').toUpperCase(), 270, 620, {font: st.font, size: 92, color: rgb(A.c), maxW: 480}); bigText(q, (it[1] || '').toUpperCase(), 270, 715, {font: st.font, size: 92, color: rgb(blue), maxW: 480}); });
      else if (t < m2) behind.push(q => { const [s, a] = pop(t, m1, m2); within(q, 270, 175, s, a, 0, r => bigText(r, (fe.text || '').toUpperCase(), 0, 0, {font: st.font, size: 210, color: '#141414', shadow: false, glow: st.glow, glowColor: A.c, maxW: 520})); });
      else { const words = chunks(fe.quote || ''), per = (fe.t1 - m2 - 0.25) / Math.max(1, words.length), j = clamp(Math.floor((t - m2 - 0.25) / per), 0, words.length - 1);
        if (t > m2 + 0.25) front.push(q => uiText(q, words[j] || '', 270, 690, 44, '#fff', {shadow: true, w: 800})); } }
    const ov = E.ev(t, 'outro');
    if (ov) { const mid = ov.t0 + 1.3;
      if (t < mid) front.push(q => { const [s, a] = pop(t, ov.t0, mid); within(q, 400, 560, s, a, 0, r => { const w = 230, h = 92; r.shadowColor = 'rgba(0,0,0,.35)'; r.shadowBlur = 16; rr(r, -w / 2, -h / 2, w, h, 22); r.fillStyle = 'rgba(255,255,255,.96)'; r.fill(); r.shadowColor = 'transparent';
        r.save(); r.beginPath(); r.arc(-w / 2 + 40, 0, 26, 0, 7); r.clip(); r.drawImage(E.V, E.V.width * .25, E.V.height * .2, E.V.width * .5, E.V.height * .3, -w / 2 + 14, -26, 52, 52); r.restore();
        uiText(r, ov.brand || '', -w / 2 + 76, -14, 16, '#111', {align: 'left', w: 800, maxW: 100}); uiText(r, ov.phone || '', -w / 2 + 76, 12, 14, '#555', {align: 'left', w: 600, maxW: 100});
        r.beginPath(); r.arc(w / 2 - 30, 0, 20, 0, 7); r.fillStyle = '#22c55e'; r.fill(); r.save(); r.translate(w / 2 - 30, 0); r.rotate(-0.6); icon(r, 'phone', 22, '#fff'); r.restore(); }); });
      else { behind.push(q => { const u = easeOut((t - mid) / 0.3); bigText(q, 'DM ME', 270 - (1 - u) * 400, 175, {font: st.font, size: 190, color: '#141414', shadow: false, maxW: 520}); });
        front.push(q => { const [s, a] = pop(t, mid + 0.2, ov.t1); within(q, 270, 680, s, a, 0, r => bigText(r, (ov.cta || '').toUpperCase(), 0, 0, {font: st.font, size: 120, color: '#fff', glow: st.glow, glowColor: A.c, stroke: st.stroke, maxW: 480})); }); } }
    behind.forEach(f => { o.save(); f(o); o.restore(); });
    E.person(o, {z, filter: bw ? 'grayscale(1) contrast(1.1)' : 'none'});
    front.forEach(f => { o.save(); f(o); o.restore(); });
    if (fe) { E.flash(o, t, fe.t0 + 2.1, 0.22); }
    if (cv) { const d = t - cv.t0; if (d > 0.95 && d < 1.2) { o.save(); o.globalAlpha = 0.6 * (1 - (d - 0.95) / 0.25); o.filter = 'blur(6px)'; E.frame(o, {}); o.restore(); } }
    E.subtitle(o, t);
  }
};

/* ---------- events ---------- */
// build preview events from editable texts (11.3s clip); the final renderer passes its own list
function previewEvents(tx) {
  return [
    {type: 'hook', t0: 0.6, t1: 2.5, big: tx.big, small: tx.small, label: tx.pill},
    {type: 'cards', t0: 2.8, t1: 5.4, items: [tx.c0, tx.c1, tx.c2], label: tx.pill, num: '10', count: 450000},
    {type: 'feature', t0: 5.6, t1: 8.8, text: tx.ring, label: tx.big, items: [tx.c0, tx.c1, tx.c2, tx.small], quote: tx.sub},
    {type: 'outro', t0: 8.9, t1: 11.3, cta: tx.cta, brand: tx.brand, phone: tx.phone, ctaLine: `Follow & comment “${tx.cta}”`},
    {type: 'sub', t0: 0.3, t1: 11.2, text: tx.sub}
  ];
}

window.VE = {Engine, STYLES, FONTS, previewEvents, W, H};
})();
