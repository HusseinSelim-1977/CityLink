/**
 * CityLink Studio-Grade 3D WebGL & Kinetic Engine
 * Inspired by Unseen Studio (unseen.co), Active Theory, and Awwwards SOTD
 * Powered by Three.js (r128) & Anime.js (v3.2.2) vendored locally in src/assets/vendor
 */

(function () {
  'use strict';

  let threeScene, threeCamera, threeRenderer, threeAnimationId;
  let cityGroup, transitLines = [], nexusOrb, pointLights = [];
  let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;
  let isSceneActive = false;
  let clock;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /**
   * Initialize Custom Magnetic Cursor
   */
  function initMagneticCursor() {
    if (prefersReducedMotion || document.querySelector('.custom-cursor-dot')) return;

    const dot = document.createElement('div');
    dot.className = 'custom-cursor-dot';
    const aura = document.createElement('div');
    aura.className = 'custom-cursor-aura';

    document.body.appendChild(dot);
    document.body.appendChild(aura);

    let cursorX = window.innerWidth / 2;
    let cursorY = window.innerHeight / 2;
    let targetCursorX = cursorX;
    let targetCursorY = cursorY;

    window.addEventListener('mousemove', (e) => {
      targetCursorX = e.clientX;
      targetCursorY = e.clientY;
      dot.style.left = `${e.clientX}px`;
      dot.style.top = `${e.clientY}px`;
    });

    function renderCursor() {
      cursorX += (targetCursorX - cursorX) * 0.18;
      cursorY += (targetCursorY - cursorY) * 0.18;
      aura.style.left = `${cursorX}px`;
      aura.style.top = `${cursorY}px`;
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Expand on interactive hover
    document.querySelectorAll('a, button, input, .Select-control, .bento-card').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        aura.style.width = '55px';
        aura.style.height = '55px';
        aura.style.borderColor = 'rgba(0, 242, 254, 0.8)';
        aura.style.background = 'rgba(0, 242, 254, 0.08)';
      });
      el.addEventListener('mouseleave', () => {
        aura.style.width = '36px';
        aura.style.height = '36px';
        aura.style.borderColor = 'rgba(0, 242, 254, 0.4)';
        aura.style.background = 'transparent';
      });
    });
  }

  /**
   * Card Mouse Spotlight Tracking
   */
  function initCardSpotlights() {
    document.querySelectorAll('.bento-card').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        card.style.setProperty('--mouse-x', `${x}px`);
        card.style.setProperty('--mouse-y', `${y}px`);
      });
    });
  }

  /**
   * Initialize Studio-Grade 3D Metropolitan Canvas
   */
  function initThreeCanvas() {
    const container = document.getElementById('three-canvas-container');
    if (!container || !window.THREE) return;

    // Clean existing
    if (isSceneActive && threeRenderer) {
      if (threeAnimationId) cancelAnimationFrame(threeAnimationId);
      container.innerHTML = '';
      isSceneActive = false;
    }

    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || 750;
    clock = new THREE.Clock();

    // 1. Scene & Perspective
    threeScene = new THREE.Scene();
    threeScene.fog = new THREE.FogExp2(0x05060A, 0.022);

    threeCamera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    threeCamera.position.set(0, 22, 50);
    threeCamera.lookAt(0, 4, 0);

    // 2. High-Precision Renderer
    threeRenderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    threeRenderer.setSize(width, height);
    threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    threeRenderer.toneMapping = THREE.ACESFilmicToneMapping;
    threeRenderer.toneMappingExposure = 1.35;
    container.appendChild(threeRenderer.domElement);

    // 3. Cinematic Studio Lighting
    const ambientLight = new THREE.AmbientLight(0x0F172A, 2.5);
    threeScene.add(ambientLight);

    const cyanSpot = new THREE.PointLight(0x00F2FE, 3.5, 90);
    cyanSpot.position.set(25, 30, 25);
    threeScene.add(cyanSpot);

    const violetSpot = new THREE.PointLight(0xA855F7, 3.0, 90);
    violetSpot.position.set(-25, 25, -15);
    threeScene.add(violetSpot);

    const coralSpot = new THREE.PointLight(0xFF6B6B, 2.0, 70);
    coralSpot.position.set(0, 15, 30);
    threeScene.add(coralSpot);

    cityGroup = new THREE.Group();

    // 4. Metropolitan Voxel High-Rise Skyscrapers
    const clusters = [
      { name: "Manhattan", x: -8, z: -2, count: 45, hMax: 22, color: 0xA855F7 },
      { name: "Brooklyn", x: 6, z: 8, count: 40, hMax: 16, color: 0x00F2FE },
      { name: "Queens", x: 14, z: -6, count: 32, hMax: 13, color: 0xFF6B6B },
      { name: "Bronx", x: -6, z: -18, count: 25, hMax: 11, color: 0xFBBF24 },
      { name: "Staten Island", x: -16, z: 18, count: 18, hMax: 7, color: 0x10B981 }
    ];

    const boxGeo = new THREE.BoxGeometry(1.2, 1, 1.2);

    clusters.forEach((cluster) => {
      for (let i = 0; i < cluster.count; i++) {
        const height = Math.random() * (cluster.hMax - 3) + 3;
        const mat = new THREE.MeshStandardMaterial({
          color: cluster.color,
          roughness: 0.2,
          metalness: 0.85,
          wireframe: false,
          emissive: cluster.color,
          emissiveIntensity: Math.random() > 0.65 ? 0.45 : 0.08
        });
        const mesh = new THREE.Mesh(boxGeo, mat);
        const offsetX = (Math.random() - 0.5) * 11;
        const offsetZ = (Math.random() - 0.5) * 11;
        mesh.position.set(cluster.x + offsetX, height / 2, cluster.z + offsetZ);
        mesh.scale.set(1, height, 1);
        cityGroup.add(mesh);
      }
    });

    // 5. Central Unseen-Style Liquid Nexus Core
    const sphereGeo = new THREE.IcosahedronGeometry(3.2, 32);
    const sphereMat = new THREE.MeshStandardMaterial({
      color: 0x00F2FE,
      roughness: 0.1,
      metalness: 0.9,
      wireframe: true,
      emissive: 0xA855F7,
      emissiveIntensity: 0.6
    });
    nexusOrb = new THREE.Mesh(sphereGeo, sphereMat);
    nexusOrb.position.set(0, 8, 0);
    cityGroup.add(nexusOrb);

    // 6. Glowing Kinetic Transit Splines & High-Speed Pulses
    transitLines = [];
    const splinePaths = [
      [new THREE.Vector3(-16, 2, 18), new THREE.Vector3(-8, 6, 8), new THREE.Vector3(0, 8, 0)],
      [new THREE.Vector3(0, 8, 0), new THREE.Vector3(6, 6, 8), new THREE.Vector3(14, 4, 12)],
      [new THREE.Vector3(0, 8, 0), new THREE.Vector3(-4, 7, -8), new THREE.Vector3(-6, 3, -18)],
      [new THREE.Vector3(0, 8, 0), new THREE.Vector3(8, 7, -3), new THREE.Vector3(14, 4, -6)]
    ];

    splinePaths.forEach((path) => {
      const curve = new THREE.CatmullRomCurve3(path);
      const points = curve.getPoints(70);
      const geom = new THREE.BufferGeometry().setFromPoints(points);
      const mat = new THREE.LineBasicMaterial({
        color: 0x00F2FE,
        transparent: true,
        opacity: 0.75,
        linewidth: 2
      });
      const line = new THREE.Line(geom, mat);
      cityGroup.add(line);

      // Pulse orb
      const pulseGeo = new THREE.SphereGeometry(0.55, 16, 16);
      const pulseMat = new THREE.MeshBasicMaterial({ color: 0xFFFFFF });
      const pulse = new THREE.Mesh(pulseGeo, pulseMat);
      cityGroup.add(pulse);

      transitLines.push({ curve, pulse, progress: Math.random() });
    });

    threeScene.add(cityGroup);
    isSceneActive = true;

    // Window Listeners
    window.addEventListener('resize', onWindowResize, false);
    window.addEventListener('mousemove', onMouseMove, false);

    animateThree();
  }

  function onWindowResize() {
    const container = document.getElementById('three-canvas-container');
    if (!container || !threeCamera || !threeRenderer) return;
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || 750;
    threeCamera.aspect = width / height;
    threeCamera.updateProjectionMatrix();
    threeRenderer.setSize(width, height);
  }

  function onMouseMove(event) {
    const halfW = window.innerWidth / 2;
    const halfH = window.innerHeight / 2;
    targetX = ((event.clientX - halfW) / halfW) * 7;
    targetY = -((event.clientY - halfH) / halfH) * 5;
  }

  function animateThree() {
    if (!isSceneActive) return;
    threeAnimationId = requestAnimationFrame(animateThree);

    const delta = clock.getDelta();
    const elapsedTime = clock.getElapsedTime();

    if (!prefersReducedMotion) {
      // Smooth camera dampening
      mouseX += (targetX - mouseX) * 0.06;
      mouseY += (targetY - mouseY) * 0.06;

      threeCamera.position.x = mouseX;
      threeCamera.position.y = 22 + mouseY * 0.7;
      threeCamera.lookAt(0, 4, 0);

      // Rotate city grid gently
      if (cityGroup) {
        cityGroup.rotation.y = elapsedTime * 0.06;
      }

      // Deform and pulse nexus orb
      if (nexusOrb) {
        nexusOrb.rotation.x = elapsedTime * 0.4;
        nexusOrb.rotation.y = elapsedTime * 0.6;
        const breath = 1.0 + Math.sin(elapsedTime * 3) * 0.08;
        nexusOrb.scale.set(breath, breath, breath);
      }

      // Transit pulse progression
      transitLines.forEach((item) => {
        item.progress += delta * 0.45;
        if (item.progress > 1.0) item.progress = 0.0;
        const point = item.curve.getPointAt(item.progress);
        item.pulse.position.copy(point);
      });
    }

    threeRenderer.render(threeScene, threeCamera);
  }

  /**
   * Anime.js KPI Number Rollups
   */
  function triggerKpiRollups() {
    if (!window.anime || prefersReducedMotion) return;

    const elements = document.querySelectorAll('.kpi-number-animate');
    elements.forEach((el) => {
      const rawVal = parseFloat(el.getAttribute('data-target-val') || '0');
      const isDecimal = el.getAttribute('data-is-decimal') === 'true';
      const obj = { val: 0 };

      window.anime({
        targets: obj,
        val: rawVal,
        round: isDecimal ? 10 : 1,
        easing: 'easeOutExpo',
        duration: 1800,
        update: function () {
          el.innerText = isDecimal ? obj.val.toFixed(1) : Math.round(obj.val).toLocaleString();
        }
      });
    });
  }

  function mountAll() {
    initMagneticCursor();
    initCardSpotlights();
    if (document.getElementById('three-canvas-container') && !isSceneActive) {
      initThreeCanvas();
    }
    triggerKpiRollups();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountAll);
  } else {
    setTimeout(mountAll, 200);
  }

  const observer = new MutationObserver(() => {
    const container = document.getElementById('three-canvas-container');
    if (container && !isSceneActive) {
      initThreeCanvas();
    } else if (!container && isSceneActive) {
      isSceneActive = false;
      if (threeAnimationId) cancelAnimationFrame(threeAnimationId);
    }
    initCardSpotlights();
    triggerKpiRollups();
  });

  observer.observe(document.body, { childList: true, subtree: true });

  window.CityLink = { initThreeCanvas, triggerKpiRollups, initMagneticCursor };
})();
