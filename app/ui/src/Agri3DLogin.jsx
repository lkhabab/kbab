import React, { useEffect, useRef, useState } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

export default function AgriGeziraLogin() {
  const mountRef = useRef(null);
  const tractorRef = useRef(null);
  const wheelLRef = useRef(null);
  const wheelRRef = useRef(null);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Helpers
    const sizes = () => ({ width: container.clientWidth, height: container.clientHeight });

    // Scene
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog("#082f2b", 20, 80);

    // Camera
    const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 200);
    camera.position.set(8, 8, 14);
    scene.add(camera);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    const { width, height } = sizes();
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Lights (مظللة)
    const hemi = new THREE.HemisphereLight("#cfe7db", "#0a2f2b", 0.8);
    scene.add(hemi);

    const dir = new THREE.DirectionalLight("#fff7dd", 1.2);
    dir.position.set(12, 18, 8);
    dir.castShadow = true;
    dir.shadow.mapSize.set(1024, 1024);
    dir.shadow.camera.near = 1;
    dir.shadow.camera.far = 60;
    dir.shadow.camera.left = -20;
    dir.shadow.camera.right = 20;
    dir.shadow.camera.top = 20;
    dir.shadow.camera.bottom = -20;
    scene.add(dir);

    // Background color (في حال لا يوجد HDR)
    renderer.setClearColor("#0b3b36", 1);

    // Ground
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(120, 120),
      new THREE.MeshStandardMaterial({ color: "#0b5c50", roughness: 1 })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    // Group for fields & canals
    const land = new THREE.Group();
    scene.add(land);

    // Fields (شبكة مربعات بدرجات خضراء)
    const fieldColors = [0x2e7d32, 0x388e3c, 0x43a047, 0x4caf50, 0x2e7d32];
    const fieldSize = 2;
    const grid = 12; // نصف عدد المربعات بالاتجاه
    for (let x = -grid; x <= grid; x++) {
      for (let z = -grid; z <= grid; z++) {
        // اترك مسارات القنوات كل بضعة خلايا
        if (x % 4 === 0 || z % 4 === 0) continue;

        const color = fieldColors[Math.floor(Math.random() * fieldColors.length)];
        const patch = new THREE.Mesh(
          new THREE.PlaneGeometry(fieldSize * 0.95, fieldSize * 0.95),
          new THREE.MeshStandardMaterial({ color, roughness: 0.95, metalness: 0.02 })
        );
        patch.rotation.x = -Math.PI / 2;
        patch.position.set(x * fieldSize, 0.002, z * fieldSize);
        patch.receiveShadow = true;
        land.add(patch);
      }
    }

    // Canals (قنوات ري طويلة متعامدة)
    function makeCanal(length, width, x, z, rotY = 0) {
      const grp = new THREE.Group();
      grp.position.set(x, 0.003, z);
      grp.rotation.y = rotY;

      const water = new THREE.Mesh(
        new THREE.PlaneGeometry(length, width),
        new THREE.MeshStandardMaterial({
          color: 0x1e88e5,
          roughness: 0.25,
          metalness: 0.6,
          transparent: true,
          opacity: 0.95,
          envMapIntensity: 1.0,
        })
      );
      water.rotation.x = -Math.PI / 2;
      water.receiveShadow = true;
      grp.add(water);

      const bankMat = new THREE.MeshStandardMaterial({ color: 0xc2b280, roughness: 1 });
      const bankL = new THREE.Mesh(new THREE.BoxGeometry(length, 0.25, 0.2), bankMat);
      bankL.position.set(0, 0.13, width / 2);
      bankL.receiveShadow = bankL.castShadow = true;

      const bankR = bankL.clone();
      bankR.position.z = -width / 2;

      grp.add(bankL, bankR);
      scene.add(grp);
    }
    // قنوات أفقية ورأسية
    makeCanal(110, 1.2, 0, 0, 0);            // أفقي
    makeCanal(110, 1.2, 0, 0, Math.PI / 2);  // رأسي

    // Date palms (نخيل)
    function makePalm() {
      const palm = new THREE.Group();

      const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.12, 0.22, 2.2, 8),
        new THREE.MeshStandardMaterial({ color: 0x8d5524, roughness: 1 })
      );
      trunk.position.y = 1.1;
      trunk.castShadow = trunk.receiveShadow = true;
      palm.add(trunk);

      for (let i = 0; i < 7; i++) {
        const leaf = new THREE.Mesh(
          new THREE.ConeGeometry(0.7, 1.3, 8),
          new THREE.MeshStandardMaterial({ color: 0x0f7a50, roughness: 0.8 })
        );
        leaf.position.y = 2.1;
        leaf.rotation.z = Math.PI / 2;
        leaf.rotation.y = (i / 7) * Math.PI * 2;
        leaf.castShadow = true;
        palm.add(leaf);
      }
      return palm;
    }

    // وزّع نخيل على ضفاف القنوات
    const palms = new THREE.Group();
    for (let i = -8; i <= 8; i += 2) {
      const p1 = makePalm();
      p1.position.set(i * 2, 0, 0.9);
      const p2 = makePalm();
      p2.position.set(i * 2, 0, -0.9);

      const p3 = makePalm();
      p3.position.set(0.9, 0, i * 2);
      const p4 = makePalm();
      p4.position.set(-0.9, 0, i * 2);

      palms.add(p1, p2, p3, p4);
    }
    scene.add(palms);

    // Tractor (جرار بسيط Low-poly)
    const tractor = new THREE.Group();
    tractorRef.current = tractor;
    tractor.position.set(-10, 0, 3);
    scene.add(tractor);

    const body = new THREE.Mesh(
      new THREE.BoxGeometry(1.8, 0.6, 0.9),
      new THREE.MeshStandardMaterial({ color: 0x2e7d32, roughness: 0.6 })
    );
    body.position.y = 0.45;
    body.castShadow = body.receiveShadow = true;
    tractor.add(body);

    const cabin = new THREE.Mesh(
      new THREE.BoxGeometry(0.8, 0.7, 0.7),
      new THREE.MeshStandardMaterial({ color: 0x43a047, roughness: 0.6 })
    );
    cabin.position.set(0.4, 1, 0);
    cabin.castShadow = cabin.receiveShadow = true;
    tractor.add(cabin);

    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.8 });
    const wheelL = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.25, 18), wheelMat);
    wheelLRef.current = wheelL;
    wheelL.rotation.z = Math.PI / 2;
    wheelL.position.set(-0.5, 0.25, 0.48);
    wheelL.castShadow = wheelL.receiveShadow = true;

    const wheelR = wheelL.clone();
    wheelRRef.current = wheelR;
    wheelR.position.z = -0.48;

    const wheelFrontL = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.2, 16), wheelMat);
    wheelFrontL.rotation.z = Math.PI / 2;
    wheelFrontL.position.set(0.8, 0.25, 0.42);
    wheelFrontL.castShadow = wheelFrontL.receiveShadow = true;

    const wheelFrontR = wheelFrontL.clone();
    wheelFrontR.position.z = -0.42;

    tractor.add(wheelL, wheelR, wheelFrontL, wheelFrontR);

    // Controls (للنظر حول المشهد - غير ضرورية للمستخدم)
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0.6, 0);
    controls.enableDamping = true;
    controls.enableZoom = false;
    controls.enablePan = false;

    // Animate
    const clock = new THREE.Clock();
    let raf = 0;

    const animate = () => {
      const t = clock.getElapsedTime();

      // مشي الجرار على صف الحقول
      if (tractorRef.current) {
        const span = 40; // الطول
        const speed = 1.6; // السرعة
        const x = ((t * speed) % span) - span / 2; // -20..20
        tractorRef.current.position.x = x;
        tractorRef.current.position.z = 3;

        // دوران العجلات
        if (wheelLRef.current) wheelLRef.current.rotation.x = t * 8;
        if (wheelRRef.current) wheelRRef.current.rotation.x = t * 8;
      }

      controls.update();
      renderer.render(scene, camera);
      raf = requestAnimationFrame(animate);
    };
    animate();

    // Resize
    const onResize = () => {
      const s = sizes();
      camera.aspect = s.width / s.height;
      camera.updateProjectionMatrix();
      renderer.setSize(s.width, s.height);
    };
    window.addEventListener("resize", onResize);

    // Cleanup
    return () => {
      window.removeEventListener("resize", onResize);
      cancelAnimationFrame(raf);
      controls.dispose();
      renderer.dispose();
      if (renderer.domElement.parentNode) {
        renderer.domElement.parentNode.removeChild(renderer.domElement);
      }
      scene.traverse((o) => {
        if (o.geometry) o.geometry.dispose?.();
        if (o.material) {
          if (Array.isArray(o.material)) o.material.forEach((m) => m.dispose?.());
          else o.material.dispose?.();
        }
      });
    };
  }, []);

  const onSubmit = (e) => {
    e.preventDefault();
    alert(`مرحبًا ${username}! تم تسجيل الدخول 🌾`);
  };

  return (
    <div style={{ position: "relative", width: "100vw", height: "100vh" }}>
      {/* Canvas Mount */}
      <div ref={mountRef} style={{ width: "100%", height: "100%" }} />

      {/* Login Card (Glassmorphism) */}
      <div
        style={{
          position: "absolute",
          inset: "0",
          display: "grid",
          placeItems: "center",
          pointerEvents: "none",
        }}
      >
        <form
          onSubmit={onSubmit}
          style={{
            pointerEvents: "auto",
            width: 360,
            maxWidth: "92vw",
            background: "rgba(255,255,255,0.9)",
            border: "1px solid rgba(255,255,255,0.5)",
            borderRadius: 18,
            padding: 22,
            boxShadow: "0 16px 40px rgba(0,0,0,.20)",
            backdropFilter: "blur(10px)",
            fontFamily: "Tajawal, system-ui, sans-serif",
            textAlign: "center",
          }}
        >
          <h2 style={{ margin: 0, marginBottom: 8, color: "#1b5e20", fontWeight: 800 }}>
            تسجيل الدخول
          </h2>
          <p style={{ marginTop: 0, marginBottom: 18, color: "#2e7d32" }}>
            مرحبًا بك! أدخل بياناتك للمتابعة إلى لوحة المزارع.
          </p>

          <label style={{ display: "block", textAlign: "right", marginBottom: 6, color: "#1b5e20" }}>
            اسم المستخدم
          </label>
          <input
            type="text"
            required
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="farmer123"
            style={{
              width: "100%",
              padding: "10px 12px",
              borderRadius: 12,
              border: "2px solid #81c784",
              marginBottom: 12,
              textAlign: "right",
              outline: "none",
            }}
          />

          <label style={{ display: "block", textAlign: "right", marginBottom: 6, color: "#1b5e20" }}>
            كلمة المرور
          </label>
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="••••••••"
            style={{
              width: "100%",
              padding: "10px 12px",
              borderRadius: 12,
              border: "2px solid #81c784",
              marginBottom: 12,
              textAlign: "right",
              outline: "none",
            }}
          />

          <div style={{ textAlign: "right", marginBottom: 8 }}>
            <label style={{ display: "inline-flex", alignItems: "center", gap: 8, color: "#1b5e20" }}>
              <input type="checkbox" style={{ accentColor: "#43a047" }} />
              تذكّرني
            </label>
          </div>

          <button
            type="submit"
            style={{
              width: "100%",
              padding: 12,
              border: 0,
              borderRadius: 14,
              fontWeight: 800,
              color: "#03271f",
              background: "#34d399",
              boxShadow: "0 10px 24px rgba(16,185,129,.4)",
              cursor: "pointer",
            }}
          >
            دخول
          </button>

          <p style={{ fontSize: 14, color: "#1b5e20", marginTop: 12 }}>
            ما عندك حساب؟{" "}
            <a href="/auth/register" style={{ color: "#004d40", textDecoration: "underline" }}>
              إنشاء حساب
            </a>
          </p>
        </form>
      </div>
    </div>
  );
}
