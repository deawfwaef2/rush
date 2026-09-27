/* Virtual clock for frame-exact capture of the game (promo videos).
   Injected BEFORE the page scripts (Playwright add_init_script). Replaces the page's notion of time:
   performance.now, requestAnimationFrame, setTimeout/setInterval all run on a virtual clock that only
   advances when the capture script calls __VT.step(ms). Math.random is seeded, so a take is repeatable.
   Placeholder __SEED__ is replaced by capture.py. */
(function () {
  var seed = (__SEED__ >>> 0) || 1;
  function mb(a) {                                // mulberry32
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  // two streams: SIM (game logic) and RENDER (switched on at drawBackground by capture.py).
  // Drawing never consumes the sim stream -> the battle is identical at any resolution / camera / viewport.
  var sim = mb(seed), rnd = mb((seed * 7919 + 13) >>> 0);
  Math.random = sim;
  var now = 1000;                                   // virtual ms
  var EPOCH = 1790000000000;                        // virtual wall clock (Date.now) - morale decay etc. stay deterministic
  performance.now = function () { return now; };
  Date.now = function () { return EPOCH + Math.round(now); };
  var raf = [], rafId = 0, timers = [], tId = 0;
  window.requestAnimationFrame = function (cb) { rafId++; raf.push({ id: rafId, cb: cb }); return rafId; };
  window.cancelAnimationFrame = function (id) { raf = raf.filter(function (r) { return r.id !== id; }); };
  function addT(fn, ms, args, iv) { tId++; ms = Math.max(0, +ms || 0); timers.push({ id: tId, t: now + (iv ? Math.max(1, ms) : ms), fn: fn, args: args, iv: iv ? Math.max(1, ms) : 0, seq: tId }); return tId; }
  window.setTimeout = function (fn, ms) { return addT(fn, ms, Array.prototype.slice.call(arguments, 2), false); };
  window.setInterval = function (fn, ms) { return addT(fn, ms, Array.prototype.slice.call(arguments, 2), true); };
  window.clearTimeout = window.clearInterval = function (id) { timers = timers.filter(function (x) { return x.id !== id; }); };
  var errs = [];
  function call(f, a) { Math.random = sim; try { if (typeof f === "function") f.apply(window, a || []); else (0, eval)(String(f)); } catch (e) { if (errs.length < 50) errs.push(String(e && e.stack || e)); } }
  window.__VT = {
    get now() { return now; },
    errs: errs, sim: sim, rnd: rnd, EPOCH: EPOCH,
    pre: null,                                      // optional per-frame hook (director), called before the frame
    step: function (ms) {
      var target = now + ms;
      for (var guard = 0; guard < 5000; guard++) {  // fire due timers in time order
        var best = null;
        for (var i = 0; i < timers.length; i++) { var x = timers[i]; if (x.t <= target && (!best || x.t < best.t || (x.t === best.t && x.seq < best.seq))) best = x; }
        if (!best) break;
        if (best.t > now) now = best.t;
        if (best.iv) { best.t += best.iv; } else { timers = timers.filter(function (y) { return y !== best; }); }
        call(best.fn, best.args);
      }
      now = target;
      if (this.pre) call(this.pre, [now]);
      var q = raf; raf = [];
      for (var j = 0; j < q.length; j++) call(q[j].cb, [now]);
      Math.random = sim;                            // evaluate() calls between frames are game logic too
    },
    run: function (ms, dt) { dt = dt || 50; for (var t = 0; t < ms; t += dt) this.step(dt); }
  };
})();
