// Inject overlay form first (works even if 3D fails)
const root = document.getElementById("agri-3d-root");
if (!root) throw new Error("#agri-3d-root not found");

const mode = (window.__MODE__ || "login").toLowerCase();
const csrf = window.__CSRF__ || "";
const action = mode === "register"
  ? (window.__REGISTER_ACTION__ || "/auth/register")
  : (window.__LOGIN_ACTION__    || "/auth/login");

// Create overlay form immediately
const wrap = document.createElement("div");
wrap.className = "agri-center";
wrap.dir = "rtl";
wrap.innerHTML = `
  <form method="post" action="${action}" class="agri-card" id="agri-form">
    ${csrf ? `<input type="hidden" name="csrf_token" value="${csrf}">` : ""}
    ${mode === "register" ? `
      <h1>إنشاء حساب</h1>
      <p>أدخل بياناتك للبدء.</p>
      <div class="agri-stack">
        <input class="agri-input" name="name"           placeholder="الاسم الكامل" required />
        <input class="agri-input" name="username"       placeholder="اسم المستخدم" required autocomplete="username" />
        <input class="agri-input" name="email"          placeholder="البريد (اختياري)" type="email" />
        <input class="agri-input" name="date_of_birth"  placeholder="تاريخ الميلاد" type="date" />
        <input class="agri-input" name="farm_location"  placeholder="موقع المزرعة (اختياري)" />
        <input class="agri-input" name="contact_details"placeholder="وسيلة الاتصال (اختياري)" />
        <input class="agri-input" name="password"       placeholder="كلمة المرور" type="password" required autocomplete="new-password" />
        <input class="agri-input" name="confirm"        placeholder="تأكيد كلمة المرور" type="password" required autocomplete="new-password" />
        <button class="agri-btn" type="submit">تسجيل</button>
        <p style="text-align:center">عندك حساب؟ <a class="agri-link" href="/auth/login">تسجيل دخول</a></p>
      </div>
    ` : `
      <h1>تسجيل الدخول</h1>
      <p>مرحبًا بك، أدخل بياناتك.</p>
      <div class="agri-stack">
        <input class="agri-input" name="username" placeholder="اسم المستخدم" required autocomplete="username" />
        <input class="agri-input" name="password" placeholder="كلمة المرور" type="password" required autocomplete="current-password" />
        <button class="agri-btn" type="submit">دخول</button>
        <p style="text-align:center">ما عندك حساب؟ <a class="agri-link" href="/auth/register">إنشاء حساب</a></p>
      </div>
    `}
  </form>
  <div class="agri-vignette"></div>
`;
root.appendChild(wrap);

// Try to load 3D background; if it fails we keep the form alone
(async () => {
  try {
    const THREE = await import("https://unpkg.com/three@0.159.0/build/three.module.js");

    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog("#052e2b", 20, 80);

    const camera = new THREE.PerspectiveCamera(40, root.clientWidth / window.innerHeight, 0.1, 200);
    camera.position.set(0, 6, 14);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(root.clientWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
    renderer.shadowMap.enabled = true;
    root.prepend(renderer.domElement);

    const sun = new THREE.DirectionalLight(0xffffff, 1.2);
    sun.position.set(20, 20, 10);
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048;
    sun.shadow.mapSize.height = 2048;
    scene.add(sun);

    const hemi = new THREE.HemisphereLight(0xffffff, 0x0b2e29, 0.5);
    scene.add(hemi);

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(200, 200),
      new THREE.MeshStandardMaterial({ color: "#052e2b", roughness: 1 })
    );
    ground.receiveShadow = true;
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    const rowsGroup = new THREE.Group();
    for (let i = -60; i <= 60; i += 2.2) {
      const row = new THREE.Mesh(
        new THREE.PlaneGeometry(1.4, 80),
        new THREE.MeshStandardMaterial({ color: i % 4 === 0 ? "#065f46" : "#064e3b" })
      );
      row.receiveShadow = true;
      row.rotation.x = -Math.PI / 2.4;
      row.position.set(i * 0.25, 0.02, -80 * 0.2);
      rowsGroup.add(row);
    }
    scene.add(rowsGroup);

    const tractor = new THREE.Group();
    tractor.position.set(-18, 0.6, -2);
    tractor.rotation.y = Math.PI / 8;

    const body = new THREE.Mesh(
      new THREE.BoxGeometry(2.8, 0.8, 1.4),
      new THREE.MeshStandardMaterial({ color: "#65a30d", metalness:0.2, roughness:0.6 })
    );
    body.castShadow = true; body.position.y = 0.7; tractor.add(body);

    const cabin = new THREE.Mesh(
      new THREE.BoxGeometry(1.2, 0.9, 1),
      new THREE.MeshStandardMaterial({ color: "#84cc16", metalness:0.1, roughness:0.4 })
    );
    cabin.castShadow = true; cabin.position.set(0.5, 1.3, 0); tractor.add(cabin);

    function wheel(r=0.6, z=0.65){
      const m = new THREE.Mesh(
        new THREE.CylinderGeometry(r, r, 0.38, 24),
        new THREE.MeshStandardMaterial({ color:"#0f172a", roughness:0.9 })
      );
      m.castShadow = true; m.position.set(1.2, 0.45, z); m.rotation.z = Math.PI/2; return m;
    }
    function smallWheel(z=0.6){
      const m = new THREE.Mesh(
        new THREE.CylinderGeometry(0.45, 0.45, 0.3, 24),
        new THREE.MeshStandardMaterial({ color:"#111827", roughness:0.9 })
      );
      m.castShadow = true; m.position.set(-1.1, 0.4, z); m.rotation.z = Math.PI/2; return m;
    }
    const w1 = smallWheel(0.6), w2 = smallWheel(-0.6), w3 = wheel(0.6, 0.65), w4 = wheel(0.6, -0.65);
    tractor.add(w1, w2, w3, w4);

    const exhaust = new THREE.Mesh(
      new THREE.CylinderGeometry(0.05, 0.05, 0.7, 12),
      new THREE.MeshStandardMaterial({ color:"#1f2937", roughness:0.6 })
    );
    exhaust.castShadow = true; exhaust.position.set(-0.4, 1.3, 0.4); tractor.add(exhaust);

    scene.add(tractor);

    let t = 0;
    function animate(){
      requestAnimationFrame(animate);
      t += 0.016;
      tractor.position.x += 0.7 * 0.016;
      if (tractor.position.x > 18) tractor.position.x = -18;
      [w1, w2, w3, w4].forEach(w=> { if (w.rotation) w.rotation.y -= 4 * 0.016; });
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener("resize", () => {
      renderer.setSize(root.clientWidth, window.innerHeight);
      camera.aspect = root.clientWidth / window.innerHeight;
      camera.updateProjectionMatrix();
    });

    console.log("3D background initialized");
  } catch (err) {
    console.warn("3D init failed, showing form only:", err);
    // Keep a plain background so the form is still readable
    root.style.background = "#073530";
  }
})();
