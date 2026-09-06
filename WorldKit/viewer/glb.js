/* WORLD KIT viewer — dependency-free glTF-binary (.glb) loader + WebGL renderer.
   No CDNs, no frameworks. Handles the subset of glTF 2.0 that the kit exports:
   triangle meshes, node hierarchies, PBR base colour factor/texture, emissive,
   alpha MASK/BLEND, embedded PNG images.                                      */
(function (global) {
  'use strict';

  /* ---------------------------------------------------------------- math */
  const M4 = {
    ident: () => new Float32Array([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]),
    mul: (a, b) => {                       // returns a*b (column-major, glTF order)
      const o = new Float32Array(16);
      for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
        let s = 0;
        for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k];
        o[c * 4 + r] = s;
      }
      return o;
    },
    fromTRS: (t, q, s) => {
      const [x, y, z, w] = q;
      const x2 = x + x, y2 = y + y, z2 = z + z;
      const xx = x * x2, xy = x * y2, xz = x * z2;
      const yy = y * y2, yz = y * z2, zz = z * z2;
      const wx = w * x2, wy = w * y2, wz = w * z2;
      return new Float32Array([
        (1 - (yy + zz)) * s[0], (xy + wz) * s[0], (xz - wy) * s[0], 0,
        (xy - wz) * s[1], (1 - (xx + zz)) * s[1], (yz + wx) * s[1], 0,
        (xz + wy) * s[2], (yz - wx) * s[2], (1 - (xx + yy)) * s[2], 0,
        t[0], t[1], t[2], 1]);
    },
    persp: (fovy, asp, n, f) => {
      const t = 1 / Math.tan(fovy / 2);
      return new Float32Array([t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) / (n - f), -1,
        0, 0, 2 * f * n / (n - f), 0]);
    },
    lookAt: (e, c, u) => {
      const z = norm([e[0] - c[0], e[1] - c[1], e[2] - c[2]]);
      const x = norm(cross(u, z)), y = cross(z, x);
      return new Float32Array([x[0], y[0], z[0], 0, x[1], y[1], z[1], 0, x[2], y[2], z[2], 0,
        -dot(x, e), -dot(y, e), -dot(z, e), 1]);
    },
    // inverse-transpose of the upper 3x3 — required for correct normals
    normalMat: (m) => {
      const a = m[0], b = m[1], c = m[2], d = m[4], e = m[5], f = m[6],
        g = m[8], h = m[9], i = m[10];
      const A = e * i - f * h, B = f * g - d * i, C = d * h - e * g;
      let det = a * A + b * B + c * C;
      if (!det) det = 1e-8;
      const id = 1 / det;
      // inverse = adj/det ; we then transpose it (so store row-major of inverse)
      return new Float32Array([
        A * id, B * id, C * id,
        (c * h - b * i) * id, (a * i - c * g) * id, (b * g - a * h) * id,
        (b * f - c * e) * id, (c * d - a * f) * id, (a * e - b * d) * id]);
    }
  };
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const norm = (a) => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  const xform = (m, p) => [
    m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12],
    m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13],
    m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14]];

  /* ------------------------------------------------------------ glb parse */
  const CSIZE = { 5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4 };
  const NCOMP = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4, MAT4: 16 };
  const CARR = { 5120: Int8Array, 5121: Uint8Array, 5122: Int16Array, 5123: Uint16Array, 5125: Uint32Array, 5126: Float32Array };

  function parseGLB(buf) {
    const dv = new DataView(buf);
    if (dv.getUint32(0, true) !== 0x46546C67) throw new Error('not a glb');
    let off = 12, json = null, bin = null;
    while (off < dv.byteLength) {
      const len = dv.getUint32(off, true), type = dv.getUint32(off + 4, true);
      const data = buf.slice(off + 8, off + 8 + len);
      if (type === 0x4E4F534A) json = JSON.parse(new TextDecoder().decode(data));
      else if (type === 0x004E4942) bin = data;
      off += 8 + len + ((4 - (len % 4)) % 4) * 0;
      off += (4 - (len % 4)) % 4;
    }
    return { json, bin };
  }

  function readAccessor(g, idx) {
    const acc = g.json.accessors[idx];
    const n = NCOMP[acc.type], cs = CSIZE[acc.componentType], Arr = CARR[acc.componentType];
    if (acc.bufferView === undefined) return new Arr(acc.count * n);
    const bv = g.json.bufferViews[acc.bufferView];
    const base = (bv.byteOffset || 0) + (acc.byteOffset || 0);
    const stride = bv.byteStride || 0;
    if (!stride || stride === n * cs) return new Arr(g.bin, base, acc.count * n);
    const out = new Arr(acc.count * n);                     // de-interleave
    for (let i = 0; i < acc.count; i++) {
      const src = new Arr(g.bin, base + i * stride, n);
      out.set(src, i * n);
    }
    return out;
  }

  /* -------------------------------------------------------------- shaders */
  const VS = `
attribute vec3 aPos; attribute vec3 aNrm; attribute vec2 aUV;
uniform mat4 uMVP, uModel; uniform mat3 uNrm;
varying vec3 vN; varying vec3 vW; varying vec2 vUV;
void main(){ vN = normalize(uNrm*aNrm); vW = (uModel*vec4(aPos,1.0)).xyz; vUV = aUV;
  gl_Position = uMVP*vec4(aPos,1.0); }`;
  const FS = `
precision highp float;
varying vec3 vN; varying vec3 vW; varying vec2 vUV;
uniform vec4 uBase; uniform vec3 uEmis; uniform float uHasTex, uAlphaCut, uWire, uRough, uMetal;
uniform sampler2D uTex; uniform vec3 uEye;
void main(){
  vec4 base = uBase;
  if (uHasTex > 0.5) base *= texture2D(uTex, vUV);
  if (uAlphaCut > 0.0 && base.a < uAlphaCut) discard;
  vec3 N = normalize(vN); vec3 V = normalize(uEye - vW);
  if (dot(N,V) < 0.0) N = -N;                       // treat kit meshes as 2-sided
  vec3 key = normalize(vec3(-0.45, 0.75, 0.55));
  vec3 rim = normalize(vec3(0.7, -0.5, 0.15));
  float kd = max(dot(N, key), 0.0), rd = max(dot(N, rim), 0.0);
  float sky = 0.5 + 0.5*N.y;
  vec3 amb = mix(vec3(0.045,0.05,0.075), vec3(0.16,0.185,0.24), sky);
  vec3 col = base.rgb * (amb + kd*vec3(1.06,0.98,0.86) + rd*vec3(0.16,0.2,0.32));
  vec3 H = normalize(key + V);
  float sp = pow(max(dot(N,H),0.0), mix(12.0, 90.0, 1.0-uRough)) * (0.12 + 0.5*uMetal) * (1.0-uRough);
  col += vec3(sp) + uEmis;
  col = pow(col, vec3(0.4545));                      // gamma
  if (uWire > 0.5) col = vec3(0.55, 0.85, 1.0);
  gl_FragColor = vec4(col, base.a);
}`;
  const LVS = `attribute vec3 aPos; attribute vec3 aCol; uniform mat4 uMVP;
varying vec3 vC; void main(){ vC=aCol; gl_Position=uMVP*vec4(aPos,1.0); }`;
  const LFS = `precision mediump float; varying vec3 vC; void main(){ gl_FragColor=vec4(vC,1.0); }`;

  function compile(gl, vs, fs) {
    const p = gl.createProgram();
    for (const [t, src] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) {
      const s = gl.createShader(t);
      gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      gl.attachShader(p, s);
    }
    gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    return p;
  }

  /* -------------------------------------------------------------- viewer */
  function Viewer(canvas) {
    const gl = canvas.getContext('webgl', { antialias: true, alpha: false });
    if (!gl) throw new Error('WebGL unavailable');
    const prog = compile(gl, VS, FS), lprog = compile(gl, LVS, LFS);
    const A = {
      pos: gl.getAttribLocation(prog, 'aPos'), nrm: gl.getAttribLocation(prog, 'aNrm'),
      uv: gl.getAttribLocation(prog, 'aUV')
    };
    const U = {};
    ['uMVP', 'uModel', 'uNrm', 'uBase', 'uEmis', 'uHasTex', 'uAlphaCut', 'uWire', 'uTex', 'uEye',
      'uRough', 'uMetal'].forEach(n => U[n] = gl.getUniformLocation(prog, n));
    const LA = { pos: gl.getAttribLocation(lprog, 'aPos'), col: gl.getAttribLocation(lprog, 'aCol') };
    const LU = { mvp: gl.getUniformLocation(lprog, 'uMVP') };

    gl.getExtension('OES_element_index_uint');
    gl.enable(gl.DEPTH_TEST);
    gl.clearColor(0.043, 0.055, 0.078, 1);

    const white = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, white);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
      new Uint8Array([255, 255, 255, 255]));

    const V = {
      gl, canvas, prims: [], bbox: null, spin: true, wire: false, grid: true,
      yaw: 0.9, pitch: 0.42, dist: 8, target: [0, 1, 0], fov: 38, lastT: 0, onstat: null
    };

    /* --- helper geometry: 1 m grid + origin axes ------------------------ */
    function buildGrid(extent) {
      const v = [], c = [];
      const n = Math.max(4, Math.ceil(extent));
      for (let i = -n; i <= n; i++) {
        const major = (i % 5 === 0), g = major ? 0.30 : 0.17, b = major ? 0.40 : 0.22;
        v.push(-n, 0, i, n, 0, i, i, 0, -n, i, 0, n);
        for (let k = 0; k < 4; k++) c.push(g * 0.8, g, b);
      }
      const L = 1.0;                                   // origin gizmo
      v.push(0, 0, 0, L, 0, 0); c.push(0.95, 0.32, 0.3, 0.95, 0.32, 0.3);
      v.push(0, 0, 0, 0, L, 0); c.push(0.45, 0.95, 0.4, 0.45, 0.95, 0.4);
      v.push(0, 0, 0, 0, 0, L); c.push(0.35, 0.6, 1.0, 0.35, 0.6, 1.0);
      const bp = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bp);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(v), gl.STATIC_DRAW);
      const bc = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bc);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(c), gl.STATIC_DRAW);
      V.grid_ = { bp, bc, count: v.length / 3 };
    }
    buildGrid(6);

    /* --- load ----------------------------------------------------------- */
    V.load = async function (url) {
      const buf = await (await fetch(url)).arrayBuffer();
      const g = parseGLB(buf);
      V.prims.forEach(p => {
        gl.deleteBuffer(p.pos); gl.deleteBuffer(p.nrm);
        if (p.uv) gl.deleteBuffer(p.uv); gl.deleteBuffer(p.idx);
      });
      V.prims = [];
      const j = g.json;

      // textures (embedded PNG in the BIN chunk)
      const texs = (j.textures || []).map(() => white);
      await Promise.all((j.textures || []).map(async (t, ti) => {
        const img = j.images[t.source];
        if (img.bufferView === undefined) return;
        const bv = j.bufferViews[img.bufferView];
        const blob = new Blob([new Uint8Array(g.bin, bv.byteOffset || 0, bv.byteLength)],
          { type: img.mimeType || 'image/png' });
        const bmp = await createImageBitmap(blob);
        const tex = gl.createTexture();
        gl.bindTexture(gl.TEXTURE_2D, tex);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, bmp);
        const pot = (x) => (x & (x - 1)) === 0;
        if (pot(bmp.width) && pot(bmp.height)) {
          gl.generateMipmap(gl.TEXTURE_2D);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
        } else {
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
          gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        }
        texs[ti] = tex;
      }));

      const lo = [1e9, 1e9, 1e9], hi = [-1e9, -1e9, -1e9];
      let tris = 0;
      const visit = (ni, parent) => {
        const n = j.nodes[ni];
        const local = n.matrix ? new Float32Array(n.matrix)
          : M4.fromTRS(n.translation || [0, 0, 0], n.rotation || [0, 0, 0, 1], n.scale || [1, 1, 1]);
        const world = M4.mul(parent, local);
        if (n.mesh !== undefined) {
          for (const pr of j.meshes[n.mesh].primitives) {
            if (pr.mode !== undefined && pr.mode !== 4) continue;
            const pos = readAccessor(g, pr.attributes.POSITION);
            const nrm = pr.attributes.NORMAL !== undefined ? readAccessor(g, pr.attributes.NORMAL)
              : new Float32Array(pos.length);
            const uv = pr.attributes.TEXCOORD_0 !== undefined ? readAccessor(g, pr.attributes.TEXCOORD_0) : null;
            const idx = pr.indices !== undefined ? readAccessor(g, pr.indices) : null;
            const acc = j.accessors[pr.attributes.POSITION];
            for (const corner of [[acc.min, acc.max]]) {
              for (let bit = 0; bit < 8; bit++) {
                const p = xform(world, [
                  (bit & 1 ? corner[1] : corner[0])[0],
                  (bit & 2 ? corner[1] : corner[0])[1],
                  (bit & 4 ? corner[1] : corner[0])[2]]);
                for (let k = 0; k < 3; k++) { lo[k] = Math.min(lo[k], p[k]); hi[k] = Math.max(hi[k], p[k]); }
              }
            }
            const mk = (data, Arr) => {
              const b = gl.createBuffer();
              gl.bindBuffer(gl.ARRAY_BUFFER, b);
              gl.bufferData(gl.ARRAY_BUFFER, Arr ? new Arr(data) : data, gl.STATIC_DRAW);
              return b;
            };
            const ib = gl.createBuffer();
            gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ib);
            const i32 = idx instanceof Uint32Array;
            gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
              idx || new Uint16Array([...Array(pos.length / 3).keys()]), gl.STATIC_DRAW);
            const mat = pr.material !== undefined ? j.materials[pr.material] : {};
            const pbr = mat.pbrMetallicRoughness || {};
            const count = idx ? idx.length : pos.length / 3;
            tris += count / 3;
            V.prims.push({
              pos: mk(pos), nrm: mk(nrm), uv: uv ? mk(uv) : null, idx: ib, count,
              itype: i32 ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT,
              world, nmat: M4.normalMat(world),
              base: pbr.baseColorFactor || [1, 1, 1, 1],
              rough: pbr.roughnessFactor !== undefined ? pbr.roughnessFactor : 0.85,
              metal: pbr.metallicFactor !== undefined ? pbr.metallicFactor : 0.0,
              emis: mat.emissiveFactor || [0, 0, 0],
              tex: pbr.baseColorTexture ? texs[pbr.baseColorTexture.index] : null,
              cut: mat.alphaMode === 'MASK' ? (mat.alphaCutoff !== undefined ? mat.alphaCutoff : 0.5) : 0,
              blend: mat.alphaMode === 'BLEND',
              name: mat.name || 'material'
            });
          }
        }
        (n.children || []).forEach(c => visit(c, world));
      };
      const scene = j.scenes[j.scene || 0];
      scene.nodes.forEach(n => visit(n, M4.ident()));

      V.bbox = { lo, hi };
      const size = [hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]];
      const r = Math.max(...size) || 1;
      V.target = [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2];
      V.dist = r * 1.85 + 0.6;
      buildGrid(Math.min(Math.max(r * 0.9, 3), 12));
      V.stats = { tris: Math.round(tris), prims: V.prims.length, mats: (j.materials || []).length, size };
      if (V.onstat) V.onstat(V.stats);
      return V.stats;
    };

    /* --- draw ----------------------------------------------------------- */
    function frame(t) {
      const dt = Math.min((t - V.lastT) / 1000 || 0, 0.05); V.lastT = t;
      if (V.spin) V.yaw += dt * 0.42;
      const w = canvas.clientWidth, h = canvas.clientHeight;
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      const eye = [
        V.target[0] + V.dist * Math.cos(V.pitch) * Math.sin(V.yaw),
        V.target[1] + V.dist * Math.sin(V.pitch),
        V.target[2] + V.dist * Math.cos(V.pitch) * Math.cos(V.yaw)];
      const view = M4.lookAt(eye, V.target, [0, 1, 0]);
      const proj = M4.persp(V.fov * Math.PI / 180, (canvas.width || 1) / (canvas.height || 1),
        0.05, 400);
      const vp = M4.mul(proj, view);

      if (V.grid) {                                    // grid + origin gizmo
        gl.useProgram(lprog);
        gl.uniformMatrix4fv(LU.mvp, false, vp);
        gl.bindBuffer(gl.ARRAY_BUFFER, V.grid_.bp);
        gl.enableVertexAttribArray(LA.pos); gl.vertexAttribPointer(LA.pos, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, V.grid_.bc);
        gl.enableVertexAttribArray(LA.col); gl.vertexAttribPointer(LA.col, 3, gl.FLOAT, false, 0, 0);
        gl.drawArrays(gl.LINES, 0, V.grid_.count);
      }

      gl.useProgram(prog);
      gl.uniform3fv(U.uEye, new Float32Array(eye));
      gl.uniform1i(U.uTex, 0);
      const order = V.prims.slice().sort((a, b) => (a.blend ? 1 : 0) - (b.blend ? 1 : 0));
      for (const p of order) {
        if (p.blend) { gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false); }
        else { gl.disable(gl.BLEND); gl.depthMask(true); }
        gl.uniformMatrix4fv(U.uMVP, false, M4.mul(vp, p.world));
        gl.uniformMatrix4fv(U.uModel, false, p.world);
        gl.uniformMatrix3fv(U.uNrm, false, p.nmat);
        gl.uniform4fv(U.uBase, new Float32Array(p.base));
        gl.uniform3fv(U.uEmis, new Float32Array(p.emis));
        gl.uniform1f(U.uRough, p.rough);
        gl.uniform1f(U.uMetal, p.metal);
        gl.uniform1f(U.uAlphaCut, p.cut);
        gl.uniform1f(U.uWire, V.wire ? 1 : 0);
        gl.uniform1f(U.uHasTex, p.tex ? 1 : 0);
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, p.tex || white);
        gl.bindBuffer(gl.ARRAY_BUFFER, p.pos);
        gl.enableVertexAttribArray(A.pos); gl.vertexAttribPointer(A.pos, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, p.nrm);
        gl.enableVertexAttribArray(A.nrm); gl.vertexAttribPointer(A.nrm, 3, gl.FLOAT, false, 0, 0);
        if (p.uv) {
          gl.bindBuffer(gl.ARRAY_BUFFER, p.uv);
          gl.enableVertexAttribArray(A.uv); gl.vertexAttribPointer(A.uv, 2, gl.FLOAT, false, 0, 0);
        } else { gl.disableVertexAttribArray(A.uv); gl.vertexAttrib2f(A.uv, 0, 0); }
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, p.idx);
        gl.drawElements(V.wire ? gl.LINE_STRIP : gl.TRIANGLES, p.count, p.itype, 0);
      }
      gl.depthMask(true);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);

    /* --- input ----------------------------------------------------------- */
    let drag = null;
    canvas.addEventListener('pointerdown', e => {
      drag = { x: e.clientX, y: e.clientY }; V.spin = false;
      canvas.setPointerCapture(e.pointerId);
      if (V.onspin) V.onspin(false);
    });
    canvas.addEventListener('pointermove', e => {
      if (!drag) return;
      V.yaw -= (e.clientX - drag.x) * 0.008;
      V.pitch = Math.max(-1.35, Math.min(1.45, V.pitch + (e.clientY - drag.y) * 0.006));
      drag = { x: e.clientX, y: e.clientY };
    });
    const stop = () => { drag = null; };
    canvas.addEventListener('pointerup', stop);
    canvas.addEventListener('pointercancel', stop);
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      V.dist = Math.max(0.4, Math.min(180, V.dist * (1 + Math.sign(e.deltaY) * 0.12)));
    }, { passive: false });

    return V;
  }

  /* ------------------------------------------------------- equirect pano */
  /* A real 360 viewer: one fullscreen triangle, and the fragment shader turns
     each pixel into a view ray and samples the equirectangular map. Yaw/pitch
     are camera angles, so the projection stays correct instead of sliding a
     flat image sideways.                                                    */
  const PANO_VS = `#version 300 es
  out vec2 vNdc;
  void main(){ vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2) * 2.0 - 1.0;
    vNdc = p; gl_Position = vec4(p, 0.0, 1.0); }`;

  const PANO_FS = `#version 300 es
  precision highp float;
  in vec2 vNdc; out vec4 outC;
  uniform sampler2D uTex; uniform vec2 uRes; uniform float uYaw, uPitch, uFov;
  const float PI = 3.14159265359;
  void main(){
    float asp = uRes.x / uRes.y;
    float t = tan(uFov * 0.5);
    vec3 d = normalize(vec3(vNdc.x * t * asp, vNdc.y * t, -1.0));
    float cy = cos(uYaw), sy = sin(uYaw), cp = cos(uPitch), sp = sin(uPitch);
    d = mat3(1.0, 0.0, 0.0, 0.0, cp, sp, 0.0, -sp, cp) * d;      // pitch
    d = mat3(cy, 0.0, -sy, 0.0, 1.0, 0.0, sy, 0.0, cy) * d;      // yaw
    vec2 uv = vec2(atan(d.x, -d.z) / (2.0 * PI) + 0.5, acos(clamp(d.y, -1.0, 1.0)) / PI);
    outC = texture(uTex, uv);
  }`;

  function Pano(canvas, url) {
    const gl = canvas.getContext('webgl2', { antialias: true });
    if (!gl) throw new Error('WebGL unavailable');
    const P = { yaw: 0.4, pitch: 0.0, fov: 1.15, drift: true, ready: false };
    const prog = gl.createProgram();
    for (const [t, src] of [[gl.VERTEX_SHADER, PANO_VS], [gl.FRAGMENT_SHADER, PANO_FS]]) {
      const sh = gl.createShader(t);
      gl.shaderSource(sh, src); gl.compileShader(sh);
      if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh));
      gl.attachShader(prog, sh);
    }
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    gl.useProgram(prog);
    const u = {};
    ['uTex', 'uRes', 'uYaw', 'uPitch', 'uFov'].forEach(n => u[n] = gl.getUniformLocation(prog, n));
    const vao = gl.createVertexArray();
    const tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE,
                  new Uint8Array([12, 16, 26, 255]));
    const im = new Image();
    im.onload = () => {
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, im);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.generateMipmap(gl.TEXTURE_2D);
      P.ready = true;
    };
    im.src = url;

    let drag = null;
    canvas.addEventListener('pointerdown', e => {
      drag = { x: e.clientX, y: e.clientY }; P.drift = false;
      canvas.setPointerCapture(e.pointerId);
    });
    const stop = () => { drag = null; };
    canvas.addEventListener('pointerup', stop);
    canvas.addEventListener('pointercancel', stop);
    canvas.addEventListener('pointermove', e => {
      if (!drag) return;
      P.yaw -= (e.clientX - drag.x) * 0.0032 * P.fov;
      P.pitch = Math.max(-1.45, Math.min(1.45, P.pitch - (e.clientY - drag.y) * 0.0032 * P.fov));
      drag = { x: e.clientX, y: e.clientY };
    });
    canvas.addEventListener('wheel', e => {
      e.preventDefault();
      P.fov = Math.max(0.35, Math.min(2.0, P.fov * (1 + Math.sign(e.deltaY) * 0.1)));
    }, { passive: false });
    canvas.addEventListener('dblclick', () => { P.drift = !P.drift; });

    function frame() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.max(1, (canvas.clientWidth * dpr) | 0);
      const h = Math.max(1, (canvas.clientHeight * dpr) | 0);
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      if (P.drift) P.yaw += 0.0006;
      gl.viewport(0, 0, w, h);
      gl.useProgram(prog);
      gl.bindVertexArray(vao);
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, tex);
      gl.uniform1i(u.uTex, 0);
      gl.uniform2f(u.uRes, w, h);
      gl.uniform1f(u.uYaw, P.yaw);
      gl.uniform1f(u.uPitch, P.pitch);
      gl.uniform1f(u.uFov, P.fov);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    return P;
  }

  global.WKViewer = { create: (c) => new Viewer(c), pano: (c, url) => Pano(c, url), parseGLB };
})(window);
