
(function () {
  if (window.__bwDrip) return;
  window.__bwDrip = true;
  var mm = window.matchMedia;
  if (!mm || mm('(prefers-reduced-motion: reduce)').matches || !mm('(hover: hover) and (pointer: fine)').matches) return;

  var MAXW = 12, LIFE = 2.6;
  var VS = 'attribute vec2 a; varying vec2 v; void main() { v = vec2(a.x * 0.5 + 0.5, 0.5 - a.y * 0.5); gl_Position = vec4(a, 0.0, 1.0); }';
  var FS = [
    'precision mediump float;',
    'uniform sampler2D u_tex; uniform vec2 u_size; uniform vec4 u_map; uniform vec4 u_w[12]; uniform int u_n;',
    'varying vec2 v;',
    'void main() {',
    '  vec2 p = v * u_size; vec2 disp = vec2(0.0); float lit = 0.0;',
    '  for (int i = 0; i != 12; i++) {',
    '    if (i == u_n) break;',
    '    vec4 w = u_w[i]; vec2 d = p - w.xy; float r = length(d) + 0.0001;',
    '    float x = r - w.z * 230.0; float s = 14.0 + w.z * 36.0;',
    '    float env = exp(-x * x / (2.0 * s * s)) * exp(-w.z * 1.6) * min(1.0, w.z * 8.0);',
    '    float h = sin(x * 0.16) * env * w.w;',
    '    disp += d / r * h; lit += cos(x * 0.16) * env * w.w;',
    '  }',
    '  vec2 t = (p + disp) / u_size * u_map.xy + u_map.zw;',
    '  vec4 c = texture2D(u_tex, clamp(t, vec2(0.001), vec2(0.999)));',
    '  c.rgb += lit * 0.012;',
    '  gl_FragColor = vec4(c.rgb, 1.0);',
    '}'
  ].join(' ');

  var surfaces = [];
  // 3차 원본 홈(.st-key-home_top) 또는 4차 첫 화면(body.jv · 자비스 8장)
  function onHome() { return !!document.querySelector('.st-key-home_top, body.jv'); }

  function shader(gl, type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null;
  }
  function attach() {
    surfaces = surfaces.filter(function (s) {
      if (s.el.isConnected) return true;
      s.cv.remove();
      var x = s.gl.getExtension('WEBGL_lose_context'); if (x) x.loseContext();
      return false;
    });
    document.querySelectorAll('.bw-h-scene .photo, .bw-h-photo .img, .bw-h-pic').forEach(function (el) {
      if (el.hasAttribute('data-rip')) return;
      el.setAttribute('data-rip', '1');
      var band = el.tagName !== 'IMG';
      var src = band ? (el.style.backgroundImage.match(/url\(["']?([^"')]+)/) || [])[1] : (el.currentSrc || el.src);
      if (!src) return;
      var cv = document.createElement('canvas');
      cv.className = 'bw-rip';
      cv.setAttribute('aria-hidden', 'true');
      var gl = cv.getContext('webgl', { alpha: false, antialias: false });
      if (!gl) return;
      var vs = shader(gl, gl.VERTEX_SHADER, VS), fs = shader(gl, gl.FRAGMENT_SHADER, FS);
      if (!vs || !fs) return;
      var pr = gl.createProgram();
      gl.attachShader(pr, vs); gl.attachShader(pr, fs); gl.linkProgram(pr);
      if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
      gl.useProgram(pr);
      gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
      var la = gl.getAttribLocation(pr, 'a');
      gl.enableVertexAttribArray(la); gl.vertexAttribPointer(la, 2, gl.FLOAT, false, 0, 0);
      var s = { el: el, cv: cv, gl: gl, band: band, waves: [], on: false, ready: false,
                u: { size: gl.getUniformLocation(pr, 'u_size'), map: gl.getUniformLocation(pr, 'u_map'),
                     w: gl.getUniformLocation(pr, 'u_w'), n: gl.getUniformLocation(pr, 'u_n') } };
      var im = new Image();
      im.onload = function () {
        s.iw = im.naturalWidth; s.ih = im.naturalHeight;
        gl.bindTexture(gl.TEXTURE_2D, gl.createTexture());
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, im);
        s.ready = true;
      };
      im.src = src;
      cv.addEventListener('webglcontextlost', function () { s.ready = false; cv.remove(); });
      if (band) el.appendChild(cv); else el.insertAdjacentElement('afterend', cv);
      surfaces.push(s);
    });
  }

  // 화면 좌표 → 사진 상자 안 좌표. 히어로 사진은 천천히 커지는 중이라(scale · transform-origin, CSS 값을 그대로 읽는다) 그만큼 되돌린다
  function local(s, x, y) {
    var w = s.el.offsetWidth, h = s.el.offsetHeight, lx, ly;
    if (s.band) {
      var r = s.el.getBoundingClientRect(); lx = x - r.left; ly = y - r.top;
    } else {
      var cs = getComputedStyle(s.el), R = s.el.parentElement.getBoundingClientRect(), k = parseFloat(cs.scale) || 1;
      var o = cs.transformOrigin.split(' '), ox = parseFloat(o[0]) || 0, oy = parseFloat(o[1]) || 0;
      lx = (x - R.left - ox) / k + ox; ly = (y - R.top - oy) / k + oy;
    }
    var edge = s.band ? 0 : 0.22;   // 히어로 사진 왼쪽 22% 는 종이색으로 흐려지는 자리
    return { x: lx, y: ly, w: w, h: h, ok: w > 0 && lx >= w * edge && lx <= w && ly >= 0 && ly <= h };
  }
  function cover(s) {   // CSS cover 와 같은 자리 — 사진 띠는 스크롤 시차(--py)만큼 위아래로 밀려 있다
    var w = s.w, h = s.h, k = Math.max(w / s.iw, h / s.ih), dw = s.iw * k, dh = s.ih * k, py = 0.5;
    if (s.band) { var f = s.el.closest('[data-par]'); py = 0.5 + (parseFloat(f && f.style.getPropertyValue('--py')) || 0) * 0.4; }
    return [w / dw, h / dh, -(w - dw) * 0.5 / dw, -(h - dh) * py / dh];
  }
  function wave(s, x, y, amp) {
    if (!s.ready) return;
    s.waves.push({ x: x, y: y, t0: performance.now(), a: amp });
    if (s.waves.length > MAXW) s.waves.shift();
    if (!s.on) { s.on = true; requestAnimationFrame(function () { draw(s); }); }
  }
  var buf = new Float32Array(MAXW * 4);
  function draw(s) {
    var now = performance.now();
    s.waves = s.waves.filter(function (w) { return (now - w.t0) / 1000 < LIFE; });
    if (!s.waves.length || !s.el.isConnected || !s.ready) { s.on = false; s.cv.classList.remove('on'); return; }
    var gl = s.gl, cv = s.cv, dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    s.w = s.el.offsetWidth; s.h = s.el.offsetHeight;
    var W = Math.max(1, Math.round(s.w * dpr)), H = Math.max(1, Math.round(s.h * dpr));
    if (cv.width !== W || cv.height !== H) { cv.width = W; cv.height = H; }
    gl.viewport(0, 0, W, H);
    gl.uniform2f(s.u.size, s.w, s.h);
    gl.uniform4fv(s.u.map, cover(s));
    buf.fill(0);
    s.waves.forEach(function (w, i) { buf[i * 4] = w.x; buf[i * 4 + 1] = w.y; buf[i * 4 + 2] = (now - w.t0) / 1000; buf[i * 4 + 3] = w.a; });
    gl.uniform4fv(s.u.w, buf); gl.uniform1i(s.u.n, s.waves.length);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    if (!s.band) cv.style.scale = getComputedStyle(s.el).scale;
    cv.classList.add('on');
    requestAnimationFrame(function () { draw(s); });
  }
  function hit(x, y) {
    for (var i = 0; i != surfaces.length; i++) { var L = local(surfaces[i], x, y); if (L.ok) return { s: surfaces[i], L: L }; }
    return null;
  }

  // 방울: 커서 끝(핫스팟)에서 맺혀 → 늘어나 떨어지고 → 14px 아래에 닿는다
  function drop(x, y) {
    var d = document.createElement('i');
    d.className = 'bw-dropl'; d.style.left = x + 'px'; d.style.top = y + 'px';
    document.body.appendChild(d);
    setTimeout(function () { land(x, y + 14); }, 640);
    setTimeout(function () { d.remove(); }, 950);
  }
  function land(x, y) {
    if (!onHome()) return;
    attach();
    var h = hit(x, y);
    if (h) { wave(h.s, h.L.x, h.L.y, 11); return; }
    var r = document.createElement('i');
    r.className = 'bw-ring'; r.style.left = x + 'px'; r.style.top = y + 'px';
    document.body.appendChild(r);
    setTimeout(function () { r.remove(); }, 1400);
  }

  var last = { x: -1, y: -1 }, wake = { x: -1e4, y: -1e4, t: 0 }, idle = 0, rests = 0;
  function rest() {
    if (!onHome() || document.hidden || rests >= 4) return;
    attach();
    if (!hit(last.x, last.y)) return;
    rests += 1;
    drop(last.x, last.y);
    idle = setTimeout(rest, 1900);
  }
  document.addEventListener('mousemove', function (e) {
    if (!onHome()) return;
    last.x = e.clientX; last.y = e.clientY;
    clearTimeout(idle); rests = 0; idle = setTimeout(rest, 750);
    var now = performance.now();
    if (now - wake.t < 45 || Math.abs(e.clientX - wake.x) + Math.abs(e.clientY - wake.y) < 30) return;
    wake.x = e.clientX; wake.y = e.clientY; wake.t = now;
    attach();
    var h = hit(e.clientX, e.clientY);
    if (h) wave(h.s, h.L.x, h.L.y, 2.4);
  }, { passive: true });
  document.addEventListener('mousedown', function (e) {
    if (e.button === 0 && onHome()) drop(e.clientX, e.clientY);
  }, { passive: true });
  document.addEventListener('mouseleave', function () { clearTimeout(idle); });
})();
