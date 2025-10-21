from flask import Flask, Response

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Utah Teapot – Python All-in-One</title>
<style>
  html,body { margin:0; height:100%; overflow:hidden; background:#000; }
  #container { width:100%; height:100%; touch-action:none; }
  .ui {
    position: fixed; bottom:14px; left:50%; transform:translateX(-50%);
    background:rgba(0,0,0,0.55); padding:10px 18px; border-radius:12px;
    backdrop-filter:blur(6px); display:flex; gap:18px; align-items:center;
    color:white; font-family:sans-serif; z-index:10;
  }
  input[type="checkbox"] { transform:scale(1.3); }
</style>
</head>
<body>
<div id="container"></div>
<div class="ui">
  <label><input id="wire" type="checkbox"> Wireframe</label>
  <label><input id="autorotate" type="checkbox" checked> Rotate</label>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.158.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.158.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.158.0/examples/js/geometries/TeapotGeometry.js"></script>

<script>
const container = document.getElementById('container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101010);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 100);
camera.position.set(0, 1.5, 6);

const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;

const ambient = new THREE.AmbientLight(0x404040);
scene.add(ambient);
const keyLight = new THREE.DirectionalLight(0xffffff, 1.2);
keyLight.position.set(5,10,7);
keyLight.castShadow = true;
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x8888ff, 0.5);
fillLight.position.set(-4,2,-4);
scene.add(fillLight);

const floor = new THREE.Mesh(
  new THREE.PlaneGeometry(20,20),
  new THREE.MeshStandardMaterial({color:0x111111, roughness:0.85, metalness:0.05})
);
floor.rotation.x = -Math.PI/2;
floor.position.y = -1.5;
floor.receiveShadow = true;
scene.add(floor);

const teapotGeo = new THREE.TeapotGeometry(1,16,true,true,true,true,true);
const teapotMat = new THREE.MeshStandardMaterial({color:0xd2691e, metalness:0.5, roughness:0.3});
const teapot = new THREE.Mesh(teapotGeo, teapotMat);
teapot.position.y = -0.3;
teapot.castShadow = true;
scene.add(teapot);

const wireCheckbox = document.getElementById('wire');
const rotateCheckbox = document.getElementById('autorotate');
wireCheckbox.addEventListener('change', () => teapot.material.wireframe = wireCheckbox.checked);

window.addEventListener('keydown', e => {
  if(e.key==='w'||e.key==='W') wireCheckbox.checked = !wireCheckbox.checked;
  if(e.key==='r'||e.key==='R') rotateCheckbox.checked = !rotateCheckbox.checked;
});

function resize() {
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.position.z = window.innerWidth > window.innerHeight ? 5 : 6;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}
window.addEventListener('resize', resize);
window.addEventListener('orientationchange', () => setTimeout(resize,500));
resize();

function animate() {
  requestAnimationFrame(animate);
  if(rotateCheckbox.checked) teapot.rotation.y += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
animate();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return Response(HTML, mimetype='text/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
