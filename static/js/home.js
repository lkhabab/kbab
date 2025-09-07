// Minimal low-poly field using Three.js
(() => {
  const canvas = document.getElementById('farm3d');
  if (!canvas) return;
  const renderer = new THREE.WebGLRenderer({canvas, antialias:true});
  function resize() {
    renderer.setSize(canvas.clientWidth || window.innerWidth, canvas.clientHeight || window.innerHeight, false);
  }
  resize();
  window.addEventListener('resize', resize);

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x0a2f2b, 8, 40);
  const camera = new THREE.PerspectiveCamera(55, window.innerWidth/window.innerHeight, 0.1, 100);
  camera.position.set(0.6, 3.2, 7.5);

  const hemi = new THREE.HemisphereLight(0xbcd7cc, 0x0a2f2b, 0.8);
  scene.add(hemi);
  const dir = new THREE.DirectionalLight(0xffffff, 0.8);
  dir.position.set(4,6,3);
  scene.add(dir);

  // ground
  const g = new THREE.PlaneGeometry(60, 60, 1, 1);
  const m = new THREE.MeshStandardMaterial({color:0x0b5c50, roughness:0.9, metalness:0.05});
  const ground = new THREE.Mesh(g, m);
  ground.rotation.x = -Math.PI/2;
  scene.add(ground);

  // simple rows
  const rowMat = new THREE.MeshStandardMaterial({color:0x07443d, roughness:1});
  for(let i=-15;i<=15;i+=1.5){
    const r = new THREE.Mesh(new THREE.BoxGeometry(60, .06, .4), rowMat);
    r.position.set(0, 0.03, i);
    scene.add(r);
  }

  // trees
  const trunkMat = new THREE.MeshStandardMaterial({color:0x3c2f2f});
  const crownMat = new THREE.MeshStandardMaterial({color:0x2c7a3f, roughness:1});
  function addTree(x, z){
    const t = new THREE.Mesh(new THREE.CylinderGeometry(.07, .07, .6, 8), trunkMat);
    t.position.set(x, .3, z);
    scene.add(t);
    const c = new THREE.Mesh(new THREE.DodecahedronGeometry(.35, 0), crownMat);
    c.position.set(x, .8, z);
    scene.add(c);
  }
  for(let i=0;i<18;i++){
    addTree(-5 + Math.random()*10, -8 + Math.random()*16);
  }

  // animate
  const clock = new THREE.Clock();
  function loop(){
    requestAnimationFrame(loop);
    const t = clock.getElapsedTime();
    camera.position.x = Math.sin(t*0.15)*1.2;
    camera.lookAt(0,0,0);
    renderer.setSize(window.innerWidth, window.innerHeight, false);
    renderer.render(scene, camera);
  }
  loop();
})();
