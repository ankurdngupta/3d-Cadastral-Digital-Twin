/**
 * 3D ULPIN High-Rise Cadastral & Digital Twin Platform
 * ====================================================
 * Photorealistic Luxury Indian Residential Society (Replicating User Reference Photos):
 * 1. Multi-Winged Ivory & Warm Ochre High-Rise Towers with Balconies & Recessed Windows
 * 2. Circular Resort Swimming Pool & Stone Sun Deck in Lush Central Parkland
 * 3. Real Asphalt Highway with Continuous Yellow Shoulder Lines, Dashed Center Stripes & Reflective Cat's Eyes
 * 4. Organic Sprawling Indian Shade Trees with Branched Trunks and Multi-Layered Dense Canopies
 * 5. Aerodynamic Luxury Metallic Sedans with Honeycomb Grilles, LED Headlights & Turbine Alloy Wheels
 * 6. Dynamic Indian Daytime Weather System with Procedural Drifting 3D Cumulus Clouds
 * 7. Live 3D ULPIN Cadastral Identification & Property Deeds
 */

// Global State & Data
let buildingData = window.__BUILDING_DATA__ || { units: [], buildings: [], point_cloud: [] };
let scene, camera, renderer, dirLight, hemiLight, ambientLight;
let societyGroup, interiorGroup, pointCloudGroup, utilityGroup, metroGroup, flyoverGroup, parkingGroup, cloudGroup;
let groundPlane, plotPlane;
let unitMeshes = [];
let floorGroups = {};
let slabMeshes = [];
let selectedUnitId = null;
let currentBuildingId = 'T01';
let isInteriorMode = false;
let isPointCloudVisible = false;
let isUtilityVisible = true;
let isMetroVisible = true;
let isFlyoverVisible = true;
let isParkingVisible = true;
let isXRayMode = false;
let isMeasureMode = false;
let measurePoints = [];
let measureLine = null;
let explodeFactor = 0;
let isDayMode = true;

// Architectural Material Palette (Sampled directly from user photos)
const PALETTE = {
  // Cadastre Semantics
  RES: 0x3b82f6,
  COM: 0x06b6d4,
  PRK: 0x8b5cf6,
  MTR: 0x10b981,
  FLY: 0xf59e0b,
  UTL: 0x64748b,
  CONFLICT: 0xff385c,

  // Tower Facades (Image 1: Off-White + Warm Ochre)
  TOWER_BODY: 0xfbfbf8,      // Crisp off-white stucco
  TOWER_OCHRE: 0xd4a373,     // Warm ochre/sandstone vertical accent pilasters
  TOWER_BASE: 0xc89666,      // Ground level masonry podium
  WINDOW_FRAME: 0x1e293b,    // Dark aluminum bronze window frame
  WINDOW_GLASS: 0x0f2b48,    // Deep sky-reflective tinted glass
  BALCONY_SLAB: 0xe2e8f0,    // Light concrete balcony ledge
  BALCONY_RAIL: 0x94a3b8,    // Modern metal balustrade

  // Highway Roads (Image 2: Weathered Dark Asphalt + Yellow Lines + Cat's Eyes)
  ROAD_ASPHALT: 0x22262d,    // Weathered aggregate asphalt
  LINE_YELLOW: 0xfacc15,     // Bright thermoplastic highway yellow
  CATS_EYE: 0xffffff,        // White retro-reflective pavement markers

  // Resort Pool & Landscape (Image 1: Circular Deep Blue Pool + Travertine Deck)
  POOL_DEEP_BLUE: 0x0284c7,
  POOL_DECK: 0xf1f5f9,
  GRASS_LUSH: 0x2e7d32,      // Rich Indian garden lawn green

  // Trees (Images 3 & 4: Woody Branched Trunks + Sprawling Canopy)
  TRUNK_BARK: 0x5c3d2e,
  LEAF_CANOPY_TOP: 0x388e3c,
  LEAF_CANOPY_MID: 0x2e7d32,
  LEAF_CANOPY_SHADE: 0x1b5e20,

  // Cars (Image 5: Metallic White Audi/Sedan + Honeycomb Grille + Alloy Rims)
  CAR_WHITE_METALLIC: 0xf8fafc,
  CAR_DARK_METALLIC: 0x1e293b,
  CAR_RED_METALLIC: 0xbe123c,
  CAR_GLASS: 0x0a101d,
  CAR_ALLOY: 0xe2e8f0,

  // Infrastructure
  SINTEX_BLACK: 0x0f172a,
  SINTEX_WHITE: 0xf8fafc,
  METRO_TUBE: 0x334155,
  METRO_TRAIN: 0xe2e8f0,
  PIPE_WATER: 0x06b6d4,
  PIPE_GAS: 0xfacc15,
  PIPE_POWER: 0xef4444,
  PIPE_SEWER: 0x64748b
};

// -------------------------------------------------------------
// 1. Scene & Dynamic Indian Daytime Atmosphere
// -------------------------------------------------------------
function initScene() {
  const container = document.getElementById('scene-container');
  const width = window.innerWidth;
  const height = window.innerHeight;

  scene = new THREE.Scene();
  
  // Sunny Indian Sky with soft atmospheric horizon haze (Matching Images 1, 3, 4)
  scene.background = new THREE.Color(0x7ec8f8);
  scene.fog = new THREE.FogExp2(0xd1e7fd, 0.0018);

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1600);
  
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: "high-performance" });
  renderer.setSize(width, height);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.32;
  container.appendChild(renderer.domElement);

  // Natural Indian Daylight Sun & Sky Illumination
  hemiLight = new THREE.HemisphereLight(0xbae6fd, 0x4ade80, 0.95);
  hemiLight.position.set(0, 150, 0);
  scene.add(hemiLight);

  ambientLight = new THREE.AmbientLight(0xfffaed, 0.65);
  scene.add(ambientLight);

  // Warm Indian Afternoon Sun
  dirLight = new THREE.DirectionalLight(0xfffaed, 2.0);
  dirLight.position.set(100, 160, 90);
  dirLight.castShadow = true;
  dirLight.shadow.mapSize.width = 2048;
  dirLight.shadow.mapSize.height = 2048;
  dirLight.shadow.camera.near = 10;
  dirLight.shadow.camera.far = 500;
  dirLight.shadow.camera.left = -140;
  dirLight.shadow.camera.right = 140;
  dirLight.shadow.camera.top = 140;
  dirLight.shadow.camera.bottom = -140;
  dirLight.shadow.bias = -0.0002;
  scene.add(dirLight);

  const sunFill = new THREE.DirectionalLight(0x93c5fd, 0.55);
  sunFill.position.set(-80, 50, -80);
  scene.add(sunFill);

  // Root Groups
  societyGroup = new THREE.Group();
  interiorGroup = new THREE.Group();
  pointCloudGroup = new THREE.Group();
  utilityGroup = new THREE.Group();
  metroGroup = new THREE.Group();
  flyoverGroup = new THREE.Group();
  parkingGroup = new THREE.Group();
  cloudGroup = new THREE.Group();

  scene.add(societyGroup);
  scene.add(interiorGroup);
  scene.add(pointCloudGroup);
  scene.add(utilityGroup);
  scene.add(metroGroup);
  scene.add(flyoverGroup);
  scene.add(parkingGroup);
  scene.add(cloudGroup);

  // Build Real-World Environment from User Images
  buildIndianWeatherClouds();
  buildSocietyLandscapedPark();
  buildHighRiseTowers();

  // Society-specific infrastructure (skip for city map with many buildings)
  const hasCityMap = buildingData.buildings && buildingData.buildings.length > 0 && buildingData.buildings[0].arch_type;
  if (!hasCityMap) {
    buildUndergroundParkingLevels();
    buildSubterraneanMetroTransit();
    buildElevatedHighwayFlyover();
    buildSubsurfaceUtilityGrid();
  }
  buildLiDARPointCloud();

  // Setup Camera & Controls
  setupCameraControls(container);

  // Render UI
  renderTowerSwitcherTabs();
  renderTopStats();
  renderFloorStackUI();

  const picker = document.getElementById('society-picker');
  if (picker && buildingData.active_society_id) {
    picker.value = buildingData.active_society_id;
  }

  // Setup Raycasting & Events
  setupRaycaster(container);
  window.addEventListener('resize', onWindowResize);
}

// -------------------------------------------------------------
// 2. Dynamic 3D Cumulus Clouds System (Images 1, 3, 4)
// -------------------------------------------------------------
function buildIndianWeatherClouds() {
  cloudGroup.clear();

  const cloudMat = new THREE.MeshStandardMaterial({
    color: 0xffffff,
    roughness: 0.95,
    transparent: true,
    opacity: 0.88,
    depthWrite: false
  });

  // Generate drifting cumulus cloud clusters
  const cloudClusters = [
    [-110, 85, -90], [-40, 95, -120], [30, 90, -80], [100, 88, -100],
    [-80, 92, 40], [20, 96, 60], [90, 84, 30]
  ];

  cloudClusters.forEach(center => {
    const cluster = new THREE.Group();
    const numPuffs = 5 + Math.floor(Math.random() * 4);

    for (let i = 0; i < numPuffs; i++) {
      const radius = 12 + Math.random() * 10;
      const puff = new THREE.Mesh(new THREE.DodecahedronGeometry(radius, 1), cloudMat);
      puff.position.set(
        (Math.random() - 0.5) * 26,
        (Math.random() - 0.5) * 8,
        (Math.random() - 0.5) * 20
      );
      puff.scale.set(1.4, 0.8, 1.0);
      cluster.add(puff);
    }

    cluster.position.set(center[0], center[1], center[2]);
    cloudGroup.add(cluster);
  });
}

// -------------------------------------------------------------
// 3. Central Park, Resort Pool, Real Road & Sprawling Trees
// -------------------------------------------------------------
function buildSocietyLandscapedPark() {
  const env = new THREE.Group();

  // Determine ground size based on number of buildings (cadastral city is larger)
  const isLargeCity = (buildingData.buildings || []).length > 15;
  const groundSize = isLargeCity ? 550 : 380;
  const plotW = isLargeCity ? 500 : 160;
  const plotD = isLargeCity ? 420 : 140;

  // 1. Rolling Manicured Green Lawns (Image 1)
  const grassGeo = new THREE.PlaneGeometry(groundSize, groundSize);
  const grassMat = new THREE.MeshStandardMaterial({
    color: PALETTE.GRASS_LUSH,
    roughness: 0.88,
    transparent: true,
    opacity: 0.98
  });
  groundPlane = new THREE.Mesh(grassGeo, grassMat);
  groundPlane.rotation.x = -Math.PI / 2;
  groundPlane.position.y = -0.05;
  groundPlane.receiveShadow = true;
  env.add(groundPlane);

  // 2. Cadastral Boundary Plot (Light Cyan Holographic Line)
  const plotGeo = new THREE.PlaneGeometry(plotW, plotD);
  const plotMat = new THREE.MeshStandardMaterial({
    color: 0x38bdf8,
    transparent: true,
    opacity: isLargeCity ? 0.08 : 0.05,
    roughness: 0.8
  });
  plotPlane = new THREE.Mesh(plotGeo, plotMat);
  plotPlane.rotation.x = -Math.PI / 2;
  plotPlane.position.set(0, -0.03, 0);
  plotPlane.receiveShadow = true;
  env.add(plotPlane);

  const plotEdges = new THREE.EdgesGeometry(plotGeo);
  const plotLine = new THREE.LineSegments(
    plotEdges,
    new THREE.LineBasicMaterial({ color: 0x00d2ff, opacity: 0.5, transparent: true })
  );
  plotLine.rotation.x = -Math.PI / 2;
  plotLine.position.set(0, -0.02, 0);
  env.add(plotLine);

  // Society-specific landscape features (skip for city map)
  if (!isLargeCity) {
    // 3. Circular Resort Swimming Pool & Travertine Sun Deck (Image 1)
    const resortPool = createResortSwimmingPool();
    resortPool.position.set(0, 0.02, 8);
    env.add(resortPool);

    // 4. Real Weathered Asphalt Road with Yellow Shoulder Stripes & Cat's Eyes (Image 2)
    const highwayRoad = createRealisticHighwayRoad();
    highwayRoad.position.set(0, 0.01, 54);
    env.add(highwayRoad);

    // Internal Society Crescent Boulevard
    const crescentRoad = new THREE.Mesh(
      new THREE.RingGeometry(38, 50, 36, 1, Math.PI * 0.72, Math.PI * 1.56),
      new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.78 })
    );
    crescentRoad.rotation.x = -Math.PI / 2;
    crescentRoad.position.set(0, 0.02, -15);
    crescentRoad.receiveShadow = true;
    env.add(crescentRoad);

    // 5. Curved Walking Promenades & Gazebos (Image 1)
    const ringProm = new THREE.Mesh(
      new THREE.RingGeometry(24, 27, 36),
      new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.8 })
    );
    ringProm.rotation.x = -Math.PI / 2;
    ringProm.position.set(0, 0.03, 8);
    env.add(ringProm);

    env.add(createParkGazebo(-24, 0.1, 14));
    env.add(createParkGazebo(24, 0.1, 14));

    // 6. Organic Sprawling Indian Shade Trees (Images 3 & 4)
    const treeCoords = [
      [-46, 0, -8], [-52, 0, -22], [-42, 0, -32], [46, 0, -8], [52, 0, -22], [42, 0, -32],
      [-24, 0, 24], [24, 0, 24], [-44, 0, 36], [44, 0, 36], [-12, 0, 20], [12, 0, 20],
      [-38, 0, 4], [-20, 0, -4], [4, 0, -10], [36, 0, 20], [40, 0, -8], [22, 0, -18],
      [30, 0, 32], [-30, 0, 32], [-6, 0, 32], [6, 0, 32]
    ];
    treeCoords.forEach((tc, idx) => {
      if (idx % 2 === 0) {
        env.add(createSprawlingCedarTree(tc[0], tc[1], tc[2]));
      } else {
        env.add(createSprawlingShadeTree(tc[0], tc[1], tc[2]));
      }
    });

    // 7. Society Entrance Gate with Security Booth
    const gateGroup = createSocietyEntranceGate();
    gateGroup.position.set(0, 0, 46);
    env.add(gateGroup);

    // 8. Aerodynamic Luxury Metallic Sedans (Image 5)
    env.add(createLuxurySedan(-18, 0.1, 38, PALETTE.CAR_WHITE_METALLIC, 0));
    env.add(createLuxurySedan(18, 0.1, 40, PALETTE.CAR_DARK_METALLIC, Math.PI));
    env.add(createLuxurySedan(30, 0.1, -12, PALETTE.CAR_WHITE_METALLIC, Math.PI / 3));
    env.add(createLuxurySedan(-35, 9.55, 54 - 2.8, PALETTE.CAR_WHITE_METALLIC, Math.PI / 2));
    env.add(createLuxurySedan(40, 9.55, 54 + 2.8, PALETTE.CAR_RED_METALLIC, -Math.PI / 2));
    env.add(createAutoRickshaw(-22, 0.1, 42, Math.PI / 2));
    env.add(createAutoRickshaw(22, 0.1, 42, -Math.PI / 2));

    // 9. Street Lamps
    const lightCoords = [
      [-15, 44], [15, 44], [-35, 12], [35, 12], [-18, -12], [18, -12],
      [26, 14], [-28, 26], [28, 26]
    ];
    lightCoords.forEach(lc => env.add(createStreetLight(lc[0], lc[1])));
  }

  societyGroup.add(env);
}

// -------------------------------------------------------------
// 4. Circular Resort Swimming Pool & Travertine Sun Deck (Image 1)
// -------------------------------------------------------------
function createResortSwimmingPool() {
  const poolGroup = new THREE.Group();

  // Travertine Stone Sun Lounging Deck
  const deck = new THREE.Mesh(
    new THREE.CylinderGeometry(15.5, 16.0, 0.2, 36),
    new THREE.MeshStandardMaterial({ color: PALETTE.POOL_DECK, roughness: 0.6 })
  );
  deck.position.y = 0.1;
  deck.receiveShadow = true;
  poolGroup.add(deck);

  // Stepped Pool Coping Rim
  const rim = new THREE.Mesh(
    new THREE.CylinderGeometry(10.5, 10.8, 0.4, 32),
    new THREE.MeshStandardMaterial({ color: 0xcbd5e1, roughness: 0.5 })
  );
  rim.position.y = 0.28;
  poolGroup.add(rim);

  // Deep Resort Blue Water
  const water = new THREE.Mesh(
    new THREE.CylinderGeometry(10.2, 10.2, 0.1, 32),
    new THREE.MeshStandardMaterial({
      color: PALETTE.POOL_DEEP_BLUE,
      roughness: 0.05,
      metalness: 0.35,
      transparent: true,
      opacity: 0.94
    })
  );
  water.position.y = 0.42;
  poolGroup.add(water);

  // Pool Loungers around the perimeter
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI * 2) / 6 + 0.3;
    const lounger = new THREE.Mesh(
      new THREE.BoxGeometry(1.8, 0.25, 0.8),
      new THREE.MeshStandardMaterial({ color: 0x3b82f6 })
    );
    lounger.position.set(Math.sin(angle) * 13.0, 0.32, Math.cos(angle) * 13.0);
    lounger.rotation.y = angle + Math.PI / 2;
    poolGroup.add(lounger);
  }

  return poolGroup;
}

// -------------------------------------------------------------
// 5. Realistic Highway Road with Yellow Edge Stripes & Cat's Eyes (Image 2)
// -------------------------------------------------------------
function createRealisticHighwayRoad() {
  const roadGroup = new THREE.Group();
  const roadLen = 380;
  const roadWidth = 22;

  // Dark Weathered Aggregate Asphalt
  const asphalt = new THREE.Mesh(
    new THREE.PlaneGeometry(roadLen, roadWidth),
    new THREE.MeshStandardMaterial({ color: PALETTE.ROAD_ASPHALT, roughness: 0.92 })
  );
  asphalt.rotation.x = -Math.PI / 2;
  asphalt.receiveShadow = true;
  roadGroup.add(asphalt);

  // Continuous Bright Yellow Shoulder Edge Lines (Both sides as in Image 2)
  for (let zOffset of [-roadWidth * 0.46, roadWidth * 0.46]) {
    const edgeLine = new THREE.Mesh(
      new THREE.PlaneGeometry(roadLen, 0.42),
      new THREE.MeshBasicMaterial({ color: PALETTE.LINE_YELLOW })
    );
    edgeLine.rotation.x = -Math.PI / 2;
    edgeLine.position.set(0, 0.02, zOffset);
    roadGroup.add(edgeLine);
  }

  // Dashed Bright Yellow Center Dividing Stripes with Raised Reflective Cat's Eyes
  const dashLen = 5.0;
  const dashGap = 6.5;
  for (let x = -170; x <= 170; x += (dashLen + dashGap)) {
    const centerDash = new THREE.Mesh(
      new THREE.PlaneGeometry(dashLen, 0.38),
      new THREE.MeshBasicMaterial({ color: PALETTE.LINE_YELLOW })
    );
    centerDash.rotation.x = -Math.PI / 2;
    centerDash.position.set(x, 0.02, 0);
    roadGroup.add(centerDash);

    // Raised White Reflective Cat's Eye / Pavement Stud (Image 2)
    const stud = new THREE.Mesh(
      new THREE.BoxGeometry(0.22, 0.08, 0.22),
      new THREE.MeshStandardMaterial({ color: PALETTE.CATS_EYE, roughness: 0.2, metalness: 0.8 })
    );
    stud.position.set(x + dashLen / 2 + dashGap / 2, 0.04, 0);
    roadGroup.add(stud);
  }

  return roadGroup;
}

// -------------------------------------------------------------
// 6. Organic Sprawling Indian Shade Trees (Images 3 & 4)
// -------------------------------------------------------------
function createSprawlingCedarTree(x, y, z) {
  const tree = new THREE.Group();

  // 1. Natural Organic Tapered Woody Trunk (Image 4)
  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.65, 1.1, 4.2, 10),
    new THREE.MeshStandardMaterial({ color: PALETTE.TRUNK_BARK, roughness: 0.9 })
  );
  trunk.position.y = 2.1;
  trunk.castShadow = true;
  tree.add(trunk);

  // Spreading Secondary Branches
  for (let angle of [0.4, 2.2, 4.5]) {
    const branch = new THREE.Mesh(
      new THREE.CylinderGeometry(0.3, 0.45, 3.2, 8),
      new THREE.MeshStandardMaterial({ color: PALETTE.TRUNK_BARK, roughness: 0.9 })
    );
    branch.position.set(Math.sin(angle) * 1.0, 3.4, Math.cos(angle) * 1.0);
    branch.rotation.z = Math.sin(angle) * 0.65;
    branch.rotation.x = Math.cos(angle) * 0.65;
    tree.add(branch);
  }

  // 2. Multi-Layered Dense Tiered Canopy (Image 4)
  const tiers = [
    { y: 4.8, r: 5.5, h: 2.2, color: PALETTE.LEAF_CANOPY_SHADE },
    { y: 6.4, r: 4.6, h: 2.0, color: PALETTE.LEAF_CANOPY_MID },
    { y: 7.8, r: 3.5, h: 1.8, color: PALETTE.LEAF_CANOPY_TOP },
    { y: 9.0, r: 2.2, h: 1.5, color: PALETTE.LEAF_CANOPY_TOP }
  ];

  tiers.forEach(t => {
    const canopyMat = new THREE.MeshStandardMaterial({ color: t.color, roughness: 0.85 });
    const cMesh = new THREE.Mesh(new THREE.ConeGeometry(t.r, t.h, 12), canopyMat);
    cMesh.position.y = t.y;
    cMesh.castShadow = true;
    tree.add(cMesh);
  });

  tree.position.set(x, y, z);
  return tree;
}

function createSprawlingShadeTree(x, y, z) {
  const tree = new THREE.Group();

  // Curved Woody Trunk with Organic Asymmetric Lean (Image 3)
  const trunk = new THREE.Mesh(
    new THREE.CylinderGeometry(0.7, 1.2, 4.6, 10),
    new THREE.MeshStandardMaterial({ color: PALETTE.TRUNK_BARK, roughness: 0.92 })
  );
  trunk.position.set(0.2, 2.3, 0);
  trunk.rotation.z = -0.08;
  trunk.castShadow = true;
  tree.add(trunk);

  // Large Lateral Spreading Limb
  const limb = new THREE.Mesh(
    new THREE.CylinderGeometry(0.35, 0.55, 3.8, 8),
    new THREE.MeshStandardMaterial({ color: PALETTE.TRUNK_BARK, roughness: 0.9 })
  );
  limb.position.set(-1.4, 4.0, 0);
  limb.rotation.z = Math.PI / 3;
  tree.add(limb);

  // Massive Sprawling Foliage Clouds (Image 3)
  const folMatMain = new THREE.MeshStandardMaterial({ color: PALETTE.LEAF_CANOPY_TOP, roughness: 0.82 });
  const folMatSub = new THREE.MeshStandardMaterial({ color: PALETTE.LEAF_CANOPY_MID, roughness: 0.85 });

  const mainCrown = new THREE.Mesh(new THREE.DodecahedronGeometry(4.2, 1), folMatMain);
  mainCrown.position.set(0.6, 6.2, 0);
  mainCrown.scale.set(1.4, 0.85, 1.2);
  mainCrown.castShadow = true;
  tree.add(mainCrown);

  const sideCrown = new THREE.Mesh(new THREE.DodecahedronGeometry(3.0, 1), folMatSub);
  sideCrown.position.set(-3.0, 4.8, 0.4);
  sideCrown.scale.set(1.3, 0.9, 1.1);
  sideCrown.castShadow = true;
  tree.add(sideCrown);

  tree.position.set(x, y, z);
  return tree;
}

// -------------------------------------------------------------
// 7. Aerodynamic Luxury Sedan (Image 5: Audi / German Sedan Style)
// -------------------------------------------------------------
function createLuxurySedan(x, y, z, bodyColor = 0xf8fafc, rotY = 0) {
  const car = new THREE.Group();

  // 1. Aerodynamic Lower Body with Sculpted Side Panels
  const lowerBody = new THREE.Mesh(
    new THREE.BoxGeometry(2.1, 0.72, 4.6),
    new THREE.MeshPhysicalMaterial({
      color: bodyColor,
      metalness: 0.65,
      roughness: 0.22,
      clearcoat: 0.8,
      clearcoatRoughness: 0.1
    })
  );
  lowerBody.position.y = 0.52;
  lowerBody.castShadow = true;
  car.add(lowerBody);

  // 2. Sloping Fastback Greenhouse Cabin (Glass + Black Roof)
  const cabin = new THREE.Mesh(
    new THREE.BoxGeometry(1.8, 0.62, 2.7),
    new THREE.MeshPhysicalMaterial({
      color: PALETTE.CAR_GLASS,
      roughness: 0.1,
      metalness: 0.9,
      transmission: 0.3
    })
  );
  cabin.position.set(0, 1.15, -0.2);
  car.add(cabin);

  // 3. Front Dark Honeycomb Hexagonal Grille (Image 5)
  const grille = new THREE.Mesh(
    new THREE.BoxGeometry(1.2, 0.42, 0.08),
    new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 })
  );
  grille.position.set(0, 0.48, 2.32);
  car.add(grille);

  // 4. Slim Angular LED Daytime Running Headlights
  for (let hx of [-0.72, 0.72]) {
    const headlight = new THREE.Mesh(
      new THREE.BoxGeometry(0.38, 0.12, 0.08),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    headlight.position.set(hx, 0.64, 2.31);
    car.add(headlight);
  }

  // 5. Slim LED Red Taillights
  for (let tx of [-0.72, 0.72]) {
    const taillight = new THREE.Mesh(
      new THREE.BoxGeometry(0.38, 0.1, 0.08),
      new THREE.MeshBasicMaterial({ color: 0xef4444 })
    );
    taillight.position.set(tx, 0.64, -2.31);
    car.add(taillight);
  }

  // 6. Realistic Low-Profile Tires with 5-Spoke Alloy Turbine Rims (Image 5)
  const tireMat = new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.9 });
  const rimMat = new THREE.MeshStandardMaterial({ color: PALETTE.CAR_ALLOY, metalness: 0.9, roughness: 0.2 });

  for (let wx of [-1.02, 1.02]) {
    for (let wz of [-1.35, 1.35]) {
      const wheelGroup = new THREE.Group();
      
      const tire = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.36, 0.24, 16), tireMat);
      tire.rotateZ(Math.PI / 2);
      wheelGroup.add(tire);

      const rim = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.26, 12), rimMat);
      rim.rotateZ(Math.PI / 2);
      wheelGroup.add(rim);

      wheelGroup.position.set(wx, 0.36, wz);
      car.add(wheelGroup);
    }
  }

  car.position.set(x, y, z);
  car.rotation.y = rotY;
  return car;
}

function createAutoRickshaw(x, y, z, rotY = 0) {
  const auto = new THREE.Group();
  const lower = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.7, 2.6), new THREE.MeshStandardMaterial({ color: 0x16a34a, roughness: 0.4 }));
  lower.position.y = 0.55;
  lower.castShadow = true;
  auto.add(lower);

  const hood = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.9, 2.4), new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.3 }));
  hood.position.set(0, 1.35, -0.1);
  auto.add(hood);

  const glass = new THREE.Mesh(new THREE.PlaneGeometry(1.3, 0.6), new THREE.MeshBasicMaterial({ color: 0x93c5fd }));
  glass.position.set(0, 1.3, 1.15);
  auto.add(glass);

  auto.position.set(x, y, z);
  auto.rotation.y = rotY;
  return auto;
}

// =============================================================
// 8. DIVERSE 3D CITY BUILDING RENDERER
// =============================================================

function buildHighRiseTowers() {
  const buildings = buildingData.buildings || [];
  // If buildings have arch_type metadata, use diverse city renderer
  if (buildings.length > 0 && buildings[0].arch_type) {
    buildDiverseCityBuildings();
    return;
  }
  // Original tower renderer for society views
  buildOriginalSocietyTowers();
}

// ── Diverse City: Each building looks unique ─────────────────
function buildDiverseCityBuildings() {
  const buildings = buildingData.buildings || [];

  // 1. Render streets
  buildCityStreets();

  // 2. Render each building with unique architecture
  buildings.forEach(bMeta => {
    if (bMeta.building_id.startsWith("INF_")) return;
    const bGroup = new THREE.Group();
    bGroup.name = `Building_${bMeta.building_id}`;
    bGroup.position.set(bMeta.center_pos[0], 0, bMeta.center_pos[2]);
    if (bMeta.rotation) bGroup.rotation.y = (bMeta.rotation * Math.PI) / 180;

    const bUnits = (buildingData.units || []).filter(u => u.building_id === bMeta.building_id);
    const floorNos = Array.from(new Set(bUnits.map(u => u.floor_no))).sort((a,b) => a-b);
    const maxFloor = Math.max(...floorNos, 0);
    const bw = bMeta.dimensions[0];
    const bd = bMeta.dimensions[1];
    const totalH = (maxFloor + 1) * 3.2;

    // ── Building Shell (exterior) ──
    const facadeColor = bMeta.facade_color || 0xFAF8F5;
    const accentColor = bMeta.accent_color || 0x8B7355;
    const archType = bMeta.arch_type || 'residential_block';

    // Main body
    const bodyMat = new THREE.MeshStandardMaterial({
      color: facadeColor, roughness: archType === 'modern_glass_tower' ? 0.15 : 0.7,
      metalness: archType === 'modern_glass_tower' ? 0.8 : 0.05,
    });
    const bodyGeo = new THREE.BoxGeometry(bw, totalH, bd);
    const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
    bodyMesh.position.y = totalH / 2;
    bodyMesh.castShadow = true; bodyMesh.receiveShadow = true;
    bGroup.add(bodyMesh);

    // Accent pilasters / stripes
    const pilMat = new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.6 });
    if (archType !== 'modern_glass_tower' && archType !== 'villa_bungalow') {
      // Corner pilasters
      [[-1,-1],[1,-1],[1,1],[-1,1]].forEach(([sx,sz]) => {
        const pil = new THREE.Mesh(new THREE.BoxGeometry(0.6, totalH + 0.5, 0.6), pilMat);
        pil.position.set(sx * bw/2, totalH/2, sz * bd/2);
        bGroup.add(pil);
      });
    }

    // Floor lines / bands
    if (archType !== 'villa_bungalow') {
      const bandMat = new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.5 });
      for (let f = 1; f <= maxFloor; f++) {
        const band = new THREE.Mesh(new THREE.BoxGeometry(bw + 0.4, 0.15, bd + 0.4), bandMat);
        band.position.y = f * 3.2;
        bGroup.add(band);
      }
    }

    // ── Windows (different patterns per type) ──
    addDiverseWindows(bGroup, bw, bd, totalH, maxFloor, archType, facadeColor);

    // ── Roof ──
    addDiverseRoof(bGroup, bw, bd, totalH, bMeta.roof_type || 'flat', accentColor, facadeColor);

    // ── Balconies (residential types) ──
    if (['residential_block','low_rise_walk_up','art_deco_tower','heritage_palazzo'].includes(archType)) {
      addCityBalconies(bGroup, bw, bd, totalH, maxFloor);
    }

    // ── Ground floor accent (darker base) ──
    const baseMat = new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.8 });
    const baseGeo = new THREE.BoxGeometry(bw + 0.3, 3.2, bd + 0.3);
    const baseMesh = new THREE.Mesh(baseGeo, baseMat);
    baseMesh.position.y = 1.6;
    baseMesh.castShadow = true;
    bGroup.add(baseMesh);

    // ── Entrance canopy ──
    const canopyMat = new THREE.MeshStandardMaterial({ color: 0x555555, roughness: 0.5 });
    const canopy = new THREE.Mesh(new THREE.BoxGeometry(Math.min(bw * 0.6, 8), 0.2, 3), canopyMat);
    canopy.position.set(0, 3.5, bd/2 + 1.5);
    canopy.castShadow = true;
    bGroup.add(canopy);

    // ── 3D ULPIN Label (floating above building) ──
    add3DULPINLabel(bGroup, bMeta.name, totalH + 4, bMeta.building_id);

    // ── Interior unit parcels (clickable) ──
    const OFFSET_X = 5, OFFSET_Z = 5;
    bUnits.forEach(unit => {
      const width = Math.abs(unit.plan_x2 - unit.plan_x1);
      const depth = Math.abs(unit.plan_y2 - unit.plan_y1);
      const height = unit.z_max - unit.z_min;
      const cx = (unit.plan_x1 + unit.plan_x2) / 2 - OFFSET_X;
      const cz = (unit.plan_y1 + unit.plan_y2) / 2 - OFFSET_Z;
      const cy = (unit.z_min + unit.z_max) / 2;

      const uGroup = new THREE.Group();
      uGroup.position.set(cx, cy, cz);
      uGroup.userData = { ...unit, baseCy: cy, bldgPos: bMeta.center_pos };

      // Invisible clickable volume
      const spaceColor = unit.conflict ? PALETTE.CONFLICT :
        (unit.space_type === 'COM' ? PALETTE.COM :
         unit.space_type === 'GOV' ? 0x10b981 :
         unit.space_type === 'PRK' ? PALETTE.PRK : PALETTE.RES);
      const clickMat = new THREE.MeshBasicMaterial({
        color: spaceColor, transparent: true, opacity: unit.conflict ? 0.45 : 0.0
      });
      const clickMesh = new THREE.Mesh(
        new THREE.BoxGeometry(width * 1.01, height * 1.01, depth * 1.01), clickMat
      );
      clickMesh.userData = uGroup.userData;
      uGroup.add(clickMesh);
      unitMeshes.push(clickMesh);

      // Unit edges
      const edges = new THREE.EdgesGeometry(new THREE.BoxGeometry(width, height, depth));
      uGroup.add(new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
        color: unit.conflict ? 0xff4757 : 0xffffff, transparent: true,
        opacity: unit.conflict ? 0.7 : 0.08
      })));

      bGroup.add(uGroup);
      const key = `${unit.building_id}_${unit.floor_no}`;
      if (!floorGroups[key]) floorGroups[key] = [];
      floorGroups[key].push(uGroup);
    });

    // Floor slabs
    floorNos.forEach(floorNo => {
      const flUnits = bUnits.filter(u => u.floor_no === floorNo);
      if (flUnits.length === 0) return;
      const zMin = Math.min(...flUnits.map(u => u.z_min));
      const isSub = floorNo < 0;
      const slab = createTowerFloorSlab(zMin, floorNo, false, isSub);
      bGroup.add(slab);
      slabMeshes.push({ mesh: slab, baseElevation: zMin, floorNo, buildingId: bMeta.building_id });
    });

    societyGroup.add(bGroup);
  });
}

// ── Window Renderer (diverse patterns) ──────────────────────
function addDiverseWindows(group, bw, bd, totalH, maxFloor, archType, facadeColor) {
  const isGlass = archType === 'modern_glass_tower';
  const isHeritage = archType === 'heritage_palazzo' || archType === 'civic_landmark';

  for (let f = 0; f <= maxFloor; f++) {
    const fy = f * 3.2 + 1.6;
    const winH = isHeritage ? 2.0 : 1.6;
    const winW = isGlass ? bw * 0.9 : (isHeritage ? 1.2 : 1.4);
    const nWins = isGlass ? 1 : Math.max(2, Math.floor(bw / 3));

    // Front & back windows
    for (let side = -1; side <= 1; side += 2) {
      if (isGlass) {
        // Curtain wall glass panel
        const glass = new THREE.Mesh(
          new THREE.PlaneGeometry(bw * 0.92, 2.4),
          new THREE.MeshPhysicalMaterial({ color: 0x0f2b48, roughness: 0.08, metalness: 0.9, transparent: true, opacity: 0.85 })
        );
        glass.position.set(0, fy, side * (bd/2 + 0.02));
        if (side < 0) glass.rotation.y = Math.PI;
        group.add(glass);
      } else {
        for (let wi = 0; wi < nWins; wi++) {
          const wx = -bw/2 + (wi + 0.5) * (bw / nWins);
          // Frame
          const frameMat = new THREE.MeshStandardMaterial({ color: isHeritage ? 0x8B7355 : 0x1e293b, roughness: 0.5 });
          const frame = new THREE.Mesh(new THREE.BoxGeometry(winW + 0.15, winH + 0.15, 0.08), frameMat);
          frame.position.set(wx, fy, side * (bd/2 + 0.02));
          group.add(frame);
          // Glass
          const glassMat = new THREE.MeshPhysicalMaterial({ color: 0x0f2b48, roughness: 0.1, metalness: 0.8 });
          const glass = new THREE.Mesh(new THREE.BoxGeometry(winW, winH, 0.04), glassMat);
          glass.position.set(wx, fy, side * (bd/2 + 0.05));
          group.add(glass);
          // Arch for heritage
          if (isHeritage && f > 0) {
            const arch = new THREE.Mesh(
              new THREE.TorusGeometry(winW/2, 0.08, 6, 12, Math.PI),
              frameMat
            );
            arch.position.set(wx, fy + winH/2, side * (bd/2 + 0.06));
            arch.rotation.z = Math.PI;
            group.add(arch);
          }
        }
      }
    }

    // Side windows (fewer)
    const sideWins = Math.max(1, Math.floor(bd / 4));
    for (let side = -1; side <= 1; side += 2) {
      for (let si = 0; si < sideWins; si++) {
        const sz = -bd/2 + (si + 0.5) * (bd / sideWins);
        const sGlass = new THREE.Mesh(
          new THREE.BoxGeometry(0.04, isGlass ? 2.4 : 1.4, isGlass ? bd * 0.8 / sideWins : 1.2),
          new THREE.MeshPhysicalMaterial({ color: 0x0f2b48, roughness: 0.1, metalness: 0.8 })
        );
        sGlass.position.set(side * (bw/2 + 0.04), fy, sz);
        group.add(sGlass);
      }
    }
  }
}

// ── Roof Renderer ───────────────────────────────────────────
function addDiverseRoof(group, bw, bd, totalH, roofType, accentColor, facadeColor) {
  if (roofType === 'pitched') {
    // Gabled pitched roof
    const roofGeo = new THREE.ConeGeometry(Math.max(bw, bd) * 0.72, 4, 4);
    const roofMat = new THREE.MeshStandardMaterial({ color: 0x8B4513, roughness: 0.7 });
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.position.y = totalH + 2;
    roof.rotation.y = Math.PI / 4;
    roof.castShadow = true;
    group.add(roof);
  } else if (roofType === 'dome') {
    // Dome roof
    const domeGeo = new THREE.SphereGeometry(Math.min(bw, bd) * 0.4, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2);
    const domeMat = new THREE.MeshStandardMaterial({ color: 0xC9A87C, roughness: 0.4, metalness: 0.3 });
    const dome = new THREE.Mesh(domeGeo, domeMat);
    dome.position.y = totalH;
    dome.castShadow = true;
    group.add(dome);
    // Dome lantern
    const lantern = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 2, 8), domeMat);
    lantern.position.y = totalH + Math.min(bw, bd) * 0.38;
    group.add(lantern);
  } else if (roofType === 'stepped') {
    // Art Deco stepped back
    for (let step = 0; step < 3; step++) {
      const scale = 1 - (step + 1) * 0.15;
      const stepH = 1.5;
      const stepMesh = new THREE.Mesh(
        new THREE.BoxGeometry(bw * scale, stepH, bd * scale),
        new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.5 })
      );
      stepMesh.position.y = totalH + step * stepH + stepH / 2;
      stepMesh.castShadow = true;
      group.add(stepMesh);
    }
    // Spire on top
    const spire = new THREE.Mesh(
      new THREE.ConeGeometry(0.8, 4, 8),
      new THREE.MeshStandardMaterial({ color: 0xFFD700, roughness: 0.3, metalness: 0.6 })
    );
    spire.position.y = totalH + 4.5 + 2;
    group.add(spire);
  } else if (roofType === 'terrace') {
    // Flat roof with railing
    const railMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.5 });
    for (let side = 0; side < 4; side++) {
      const isX = side < 2;
      const dir = side % 2 === 0 ? 1 : -1;
      const rail = new THREE.Mesh(
        new THREE.BoxGeometry(isX ? 0.1 : bw, 1.0, isX ? bd : 0.1),
        railMat
      );
      rail.position.set(isX ? dir * bw/2 : 0, totalH + 0.5, isX ? 0 : dir * bd/2);
      group.add(rail);
    }
    // Water tank
    const tank = new THREE.Mesh(
      new THREE.CylinderGeometry(1.2, 1.2, 2, 8),
      new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 })
    );
    tank.position.set(bw * 0.25, totalH + 1.5, -bd * 0.25);
    group.add(tank);
  } else {
    // Flat roof with parapet
    const parapet = new THREE.Mesh(
      new THREE.BoxGeometry(bw + 0.5, 0.8, bd + 0.5),
      new THREE.MeshStandardMaterial({ color: accentColor, roughness: 0.6 })
    );
    parapet.position.y = totalH + 0.4;
    group.add(parapet);
  }
}

// ── City Balconies ──────────────────────────────────────────
function addCityBalconies(group, bw, bd, totalH, maxFloor) {
  const balcMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.7 });
  const railMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.5, transparent: true, opacity: 0.8 });
  const nBalc = Math.max(1, Math.floor(bw / 6));
  for (let f = 1; f <= Math.min(maxFloor, 8); f += 2) {
    for (let bi = 0; bi < nBalc; bi++) {
      const bx = -bw/2 + (bi + 0.5) * (bw / nBalc);
      const slab = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.15, 1.2), balcMat);
      slab.position.set(bx, f * 3.2, bd/2 + 0.6);
      slab.castShadow = true;
      group.add(slab);
      const rail = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.8, 0.05), railMat);
      rail.position.set(bx, f * 3.2 + 0.5, bd/2 + 1.15);
      group.add(rail);
    }
  }
}

// ── City Streets (roads between buildings) ──────────────────
function buildCityStreets() {
  const socData = buildingData.societies && buildingData.societies[buildingData.active_society_id];
  const streets = (socData && socData.streets) || (buildingData.streets) || [];
  const piazzas = (socData && socData.piazzas) || (buildingData.piazzas) || [];

  const roadMat = new THREE.MeshStandardMaterial({ color: 0x22262d, roughness: 0.85 });
  const lineMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.5 });
  const paveMat = new THREE.MeshStandardMaterial({ color: 0xd4c5a9, roughness: 0.75 });

  streets.forEach(s => {
    if (s.vertical) {
      const len = Math.abs((s.z2 || 180) - s.z);
      const road = new THREE.Mesh(new THREE.PlaneGeometry(s.w, len), roadMat);
      road.rotation.x = -Math.PI / 2;
      road.position.set(s.x1, 0.02, s.z + len / 2);
      road.receiveShadow = true;
      societyGroup.add(road);
      // Center line
      const line = new THREE.Mesh(new THREE.PlaneGeometry(0.2, len), lineMat);
      line.rotation.x = -Math.PI / 2;
      line.position.set(s.x1, 0.04, s.z + len / 2);
      societyGroup.add(line);
    } else {
      const len = Math.abs(s.x2 - s.x1);
      const road = new THREE.Mesh(new THREE.PlaneGeometry(len, s.w), roadMat);
      road.rotation.x = -Math.PI / 2;
      road.position.set((s.x1 + s.x2) / 2, 0.02, s.z);
      road.receiveShadow = true;
      societyGroup.add(road);
      const line = new THREE.Mesh(new THREE.PlaneGeometry(len, 0.2), lineMat);
      line.rotation.x = -Math.PI / 2;
      line.position.set((s.x1 + s.x2) / 2, 0.04, s.z);
      societyGroup.add(line);
    }
  });

  // Piazzas
  piazzas.forEach(p => {
    const piazza = new THREE.Mesh(
      new THREE.CircleGeometry(p.r, 32),
      paveMat
    );
    piazza.rotation.x = -Math.PI / 2;
    piazza.position.set(p.x, 0.03, p.z);
    piazza.receiveShadow = true;
    societyGroup.add(piazza);

    // Fountain in center
    const fountain = new THREE.Mesh(
      new THREE.CylinderGeometry(2, 2.5, 1, 12),
      new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4 })
    );
    fountain.position.set(p.x, 0.5, p.z);
    societyGroup.add(fountain);
    const water = new THREE.Mesh(
      new THREE.CircleGeometry(1.8, 16),
      new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.1, metalness: 0.3 })
    );
    water.rotation.x = -Math.PI / 2;
    water.position.set(p.x, 1.02, p.z);
    societyGroup.add(water);
  });
}

// ── 3D ULPIN Label (floating text above building) ───────────
function add3DULPINLabel(group, text, height, bldgId) {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = 512; canvas.height = 64;
  ctx.fillStyle = 'rgba(0,0,0,0.7)';
  ctx.fillRect(0, 0, 512, 64);
  ctx.fillStyle = '#00ff88';
  ctx.font = 'bold 22px monospace';
  ctx.textAlign = 'center';
  ctx.fillText(text.substring(0, 30), 256, 24);
  ctx.fillStyle = '#ffffff';
  ctx.font = '16px monospace';
  ctx.fillText(bldgId, 256, 48);

  const texture = new THREE.CanvasTexture(canvas);
  const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true, opacity: 0.9 });
  const sprite = new THREE.Sprite(spriteMat);
  sprite.scale.set(18, 2.2, 1);
  sprite.position.y = height;
  group.add(sprite);
}

// ── Original Society Tower Renderer (preserved) ─────────────
function buildOriginalSocietyTowers() {
  const bldgConfigs = {
    T01: { center: [-32, 0, -16], name: "Tower A" },
    T02: { center: [-12, 0, -26], name: "Tower B" },
    T03: { center: [12, 0, -26], name: "Tower C" },
    T04: { center: [32, 0, -16], name: "Tower D" },
    COM01: { center: [0, 0, 26], name: "Commercial Galleria" }
  };

  buildingData.buildings.forEach(bMeta => {
    if (bMeta.building_id.startsWith("INF_")) return;

    const cfg = bldgConfigs[bMeta.building_id] || { center: bMeta.center_pos };
    const bGroup = new THREE.Group();
    bGroup.name = `Building_${bMeta.building_id}`;
    bGroup.position.set(cfg.center[0], 0, cfg.center[2]);

    const bUnits = buildingData.units.filter(u => u.building_id === bMeta.building_id);
    const floorNos = Array.from(new Set(bUnits.map(u => u.floor_no))).sort((a, b) => a - b);
    const maxFloor = Math.max(...floorNos);

    // Double-Height Ground Portico (Porte-Cochère)
    if (bMeta.building_id.startsWith("T0")) {
      const portico = createPorteCochere();
      portico.position.set(0, 0, 6.5);
      bGroup.add(portico);
    }

    // Floor Slabs & Tower Floors
    floorNos.forEach(floorNo => {
      const flUnits = bUnits.filter(u => u.floor_no === floorNo);
      const zMin = Math.min(...flUnits.map(u => u.z_min));
      const zMax = Math.max(...flUnits.map(u => u.z_max));

      const isSub = floorNo < 0;
      const slab = createTowerFloorSlab(zMin, floorNo, false, isSub);
      bGroup.add(slab);
      slabMeshes.push({ mesh: slab, baseElevation: zMin, floorNo, buildingId: bMeta.building_id });

      if (floorNo === maxFloor) {
        const roof = createTowerFloorSlab(zMax, floorNo, true, false, bMeta.building_id);
        bGroup.add(roof);
        slabMeshes.push({ mesh: roof, baseElevation: zMax, floorNo, buildingId: bMeta.building_id });
      }
    });

    // 3D Unit Parcels with Ivory/Ochre Architectural Facades
    const OFFSET_X = 5, OFFSET_Z = 5;
    bUnits.forEach(unit => {
      const width = Math.abs(unit.plan_x2 - unit.plan_x1);
      const depth = Math.abs(unit.plan_y2 - unit.plan_y1);
      const height = unit.z_max - unit.z_min;
      const cx = (unit.plan_x1 + unit.plan_x2) / 2 - OFFSET_X;
      const cz = (unit.plan_y1 + unit.plan_y2) / 2 - OFFSET_Z;
      const cy = (unit.z_min + unit.z_max) / 2;

      const uGroup = new THREE.Group();
      uGroup.position.set(cx, cy, cz);
      uGroup.userData = { ...unit, baseCy: cy, bldgPos: cfg.center };

      const wallMat = new THREE.MeshStandardMaterial({
        color: unit.space_type === 'COM' ? 0xe2e8f0 : (unit.floor_no === 0 ? PALETTE.TOWER_BASE : PALETTE.TOWER_BODY),
        roughness: 0.65, metalness: 0.05
      });
      const wallMesh = new THREE.Mesh(new THREE.BoxGeometry(width, height, depth), wallMat);
      wallMesh.castShadow = true; wallMesh.receiveShadow = true;
      uGroup.add(wallMesh);

      if (unit.floor_no > 0) {
        const pilasterMat = new THREE.MeshStandardMaterial({ color: PALETTE.TOWER_OCHRE, roughness: 0.6 });
        const pilaster = new THREE.Mesh(new THREE.BoxGeometry(0.4, height, 0.4), pilasterMat);
        pilaster.position.set(-width / 2 + 0.2, 0, depth / 2 + 0.05);
        uGroup.add(pilaster);
      }

      const cadastreMat = new THREE.MeshBasicMaterial({
        color: unit.conflict ? PALETTE.CONFLICT : PALETTE.RES,
        transparent: true, opacity: unit.conflict ? 0.45 : 0.0
      });
      const cadastreMesh = new THREE.Mesh(new THREE.BoxGeometry(width * 1.01, height * 1.01, depth * 1.01), cadastreMat);
      cadastreMesh.userData = uGroup.userData;
      uGroup.add(cadastreMesh);
      unitMeshes.push(cadastreMesh);

      const edges = new THREE.EdgesGeometry(new THREE.BoxGeometry(width, height, depth));
      uGroup.add(new THREE.LineSegments(edges, new THREE.LineBasicMaterial({
        color: unit.conflict ? 0xff4757 : 0xffffff, transparent: true,
        opacity: unit.conflict ? 0.7 : 0.15
      })));

      if (unit.floor_no >= 0) addArchitecturalWindowMatrix(uGroup, width, height, depth);
      if (unit.space_type === 'RES' && unit.floor_no > 0) addHighRiseBalconyAndWindows(uGroup, width, height, depth, unit);

      bGroup.add(uGroup);
      const key = `${unit.building_id}_${unit.floor_no}`;
      if (!floorGroups[key]) floorGroups[key] = [];
      floorGroups[key].push(uGroup);
    });

    societyGroup.add(bGroup);
  });
}

function addArchitecturalWindowMatrix(uGroup, w, h, d) {
  const winCols = 2;
  const colW = (w * 0.75) / winCols;
  for (let c = 0; c < winCols; c++) {
    const wx = -w * 0.35 + c * (colW + 0.2) + colW / 2;
    
    // Window Frame
    const frame = new THREE.Mesh(
      new THREE.BoxGeometry(colW, h * 0.52, 0.08),
      new THREE.MeshStandardMaterial({ color: PALETTE.WINDOW_FRAME, roughness: 0.5 })
    );
    frame.position.set(wx, 0, d * 0.5 + 0.02);
    uGroup.add(frame);

    // Reflective Glass Pane
    const glass = new THREE.Mesh(
      new THREE.BoxGeometry(colW * 0.88, h * 0.45, 0.04),
      new THREE.MeshPhysicalMaterial({
        color: PALETTE.WINDOW_GLASS,
        roughness: 0.1,
        metalness: 0.85,
        reflectivity: 0.9
      })
    );
    glass.position.set(wx, 0, d * 0.5 + 0.05);
    uGroup.add(glass);
  }
}

function createPorteCochere() {
  const portico = new THREE.Group();

  const colMat = new THREE.MeshStandardMaterial({ color: 0x64748b, roughness: 0.4 });
  const c1 = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 6.0, 12), colMat);
  c1.position.set(-4.5, 3.0, 0);
  portico.add(c1);

  const c2 = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.55, 6.0, 12), colMat);
  c2.position.set(4.5, 3.0, 0);
  portico.add(c2);

  const canopy = new THREE.Mesh(
    new THREE.BoxGeometry(11.0, 0.35, 5.5),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.3 })
  );
  canopy.position.set(0, 5.8, 0);
  portico.add(canopy);

  const glassPanel = new THREE.Mesh(
    new THREE.PlaneGeometry(10.2, 4.8),
    new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.65, roughness: 0.1 })
  );
  glassPanel.rotation.x = -Math.PI / 2;
  glassPanel.position.set(0, 6.05, 0);
  portico.add(glassPanel);

  return portico;
}

function createTowerFloorSlab(elevation, floorNo, isRoof = false, isSub = false, bldgId = "T01") {
  const slabGeo = new THREE.BoxGeometry(10.2, 0.14, 10.2);
  const slabMat = new THREE.MeshStandardMaterial({
    color: isRoof ? 0x1e293b : (isSub ? 0x475569 : PALETTE.BALCONY_SLAB),
    roughness: 0.6
  });
  const slab = new THREE.Mesh(slabGeo, slabMat);
  slab.position.set(0, elevation, 0);
  slab.receiveShadow = true;
  slab.castShadow = true;

  if (isRoof) {
    // Stepped Penthouse Crown (Matching Image 1)
    const crown1 = new THREE.Mesh(
      new THREE.BoxGeometry(9.5, 1.8, 9.5),
      new THREE.MeshStandardMaterial({ color: PALETTE.TOWER_OCHRE, roughness: 0.5 })
    );
    crown1.position.set(0, 0.9, 0);
    crown1.castShadow = true;
    slab.add(crown1);

    const crown2 = new THREE.Mesh(
      new THREE.BoxGeometry(6.5, 1.6, 6.5),
      new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.3 })
    );
    crown2.position.set(0, 2.5, 0);
    crown2.castShadow = true;
    slab.add(crown2);

    // Architectural Crown Pergola
    for (let i = -2.5; i <= 2.5; i += 1.25) {
      const beam = new THREE.Mesh(
        new THREE.BoxGeometry(0.18, 0.4, 7.5),
        new THREE.MeshStandardMaterial({ color: 0xfacc15, metalness: 0.7 })
      );
      beam.position.set(i, 3.5, 0);
      slab.add(beam);
    }

    // Dual Sintex Water Storage Tanks
    const sintexGeo = new THREE.CylinderGeometry(0.8, 0.8, 1.6, 16);
    const sintexBlack = new THREE.Mesh(sintexGeo, new THREE.MeshStandardMaterial({ color: PALETTE.SINTEX_BLACK }));
    sintexBlack.position.set(3.8, 1.0, 3.5);
    slab.add(sintexBlack);

    const sintexWhite = new THREE.Mesh(sintexGeo, new THREE.MeshStandardMaterial({ color: PALETTE.SINTEX_WHITE }));
    sintexWhite.position.set(2.0, 1.0, 3.5);
    slab.add(sintexWhite);
  }

  return slab;
}

function addHighRiseBalconyAndWindows(uGroup, w, h, d, unit) {
  // Cantilevered Balcony Slab
  const balcony = new THREE.Mesh(
    new THREE.BoxGeometry(w * 0.94, 0.12, 0.95),
    new THREE.MeshStandardMaterial({ color: PALETTE.BALCONY_SLAB, roughness: 0.6 })
  );
  balcony.position.set(0, -h * 0.44, -(d * 0.5 + 0.48));
  uGroup.add(balcony);

  // Modern Railing (Matching Image 1)
  const rail = new THREE.Mesh(
    new THREE.BoxGeometry(w * 0.94, 0.65, 0.05),
    new THREE.MeshStandardMaterial({ color: PALETTE.BALCONY_RAIL, metalness: 0.5 })
  );
  rail.position.set(0, -h * 0.44 + 0.38, -(d * 0.5 + 0.48));
  uGroup.add(rail);

  // AC Unit
  const ac = new THREE.Mesh(
    new THREE.BoxGeometry(0.75, 0.5, 0.35),
    new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.4 })
  );
  ac.position.set(w * 0.34, -h * 0.22, (d * 0.5 + 0.2));
  uGroup.add(ac);
}

function createParkGazebo(x, y, z) {
  const gaz = new THREE.Group();
  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI * 2) / 6;
    const pillar = new THREE.Mesh(
      new THREE.CylinderGeometry(0.14, 0.14, 2.8, 8),
      new THREE.MeshStandardMaterial({ color: 0xffffff })
    );
    pillar.position.set(Math.sin(angle) * 2.2, 1.4, Math.cos(angle) * 2.2);
    gaz.add(pillar);
  }

  const dome = new THREE.Mesh(
    new THREE.SphereGeometry(2.4, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2),
    new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.3 })
  );
  dome.position.y = 2.8;
  gaz.add(dome);

  gaz.position.set(x, y, z);
  return gaz;
}

function createSocietyEntranceGate() {
  const gate = new THREE.Group();

  const p1 = new THREE.Mesh(new THREE.BoxGeometry(2.4, 8.0, 2.4), new THREE.MeshStandardMaterial({ color: 0x475569 }));
  p1.position.set(-10, 4.0, 0);
  p1.castShadow = true;
  gate.add(p1);

  const p2 = new THREE.Mesh(new THREE.BoxGeometry(2.4, 8.0, 2.4), new THREE.MeshStandardMaterial({ color: 0x475569 }));
  p2.position.set(10, 4.0, 0);
  p2.castShadow = true;
  gate.add(p2);

  const arch = new THREE.Mesh(new THREE.BoxGeometry(22.4, 1.8, 1.8), new THREE.MeshStandardMaterial({ color: 0x1e3a8a, metalness: 0.3 }));
  arch.position.set(0, 7.8, 0);
  arch.castShadow = true;
  gate.add(arch);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(4.2, 3.6, 3.6), new THREE.MeshStandardMaterial({ color: 0xf1f5f9 }));
  cabin.position.set(14.2, 1.8, 0);
  gate.add(cabin);

  const b1 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 8.0, 8), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
  b1.rotateZ(Math.PI / 2);
  b1.position.set(-4.5, 1.0, 0);
  gate.add(b1);

  const b2 = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 8.0, 8), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
  b2.rotateZ(Math.PI / 2);
  b2.position.set(4.5, 1.0, 0);
  gate.add(b2);

  return gate;
}

function createStreetLight(x, z) {
  const pole = new THREE.Group();
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 7.5, 8), new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.6 }));
  mesh.position.y = 3.75;
  pole.add(mesh);

  const arm = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.08, 0.08), new THREE.MeshStandardMaterial({ color: 0x475569 }));
  arm.position.set(-0.8, 7.4, 0);
  pole.add(arm);

  const lamp = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.4, 8), new THREE.MeshBasicMaterial({ color: 0xfef08a }));
  lamp.position.set(-1.6, 7.2, 0);
  pole.add(lamp);

  pole.position.set(x, 0, z);
  return pole;
}

// -------------------------------------------------------------
// 9. Underground Parking Levels (B1 & B2)
// -------------------------------------------------------------
function buildUndergroundParkingLevels() {
  parkingGroup.clear();

  const towerCenters = [
    [-32, -16], [-12, -26], [12, -26], [32, -16]
  ];

  towerCenters.forEach(tc => {
    for (let fl of [-1, -2]) {
      const elevation = fl * 3.0;
      const bFloor = new THREE.Group();
      bFloor.position.set(tc[0], elevation, tc[1]);

      const floorGeo = new THREE.BoxGeometry(15.0, 0.2, 15.0);
      const floorMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.8 });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.position.y = -0.1;
      bFloor.add(floor);

      const pillarGeo = new THREE.BoxGeometry(0.8, 2.8, 0.8);
      const pillarMat = new THREE.MeshStandardMaterial({ color: 0x64748b });
      for (let px of [-5.0, 5.0]) {
        for (let pz of [-5.0, 5.0]) {
          const p = new THREE.Mesh(pillarGeo, pillarMat);
          p.position.set(px, 1.4, pz);
          bFloor.add(p);

          const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.82, 0.6, 0.82), new THREE.MeshBasicMaterial({ color: 0xfacc15 }));
          stripe.position.set(px, 0.6, pz);
          bFloor.add(stripe);
        }
      }

      for (let px of [-3.8, 0, 3.8]) {
        const pLine = new THREE.Mesh(new THREE.PlaneGeometry(0.14, 5.0), new THREE.MeshBasicMaterial({ color: 0xfef08a }));
        pLine.rotation.x = -Math.PI / 2;
        pLine.position.set(px, 0.02, -2.8);
        bFloor.add(pLine);
      }

      bFloor.add(createLuxurySedan(-2.4, 0.05, -2.8, 0x3b82f6));
      bFloor.add(createLuxurySedan(2.4, 0.05, -2.8, 0xef4444));

      parkingGroup.add(bFloor);
    }
  });
}

// -------------------------------------------------------------
// 10. Subterranean Metro Transit Tunnel & Train
// -------------------------------------------------------------
function buildSubterraneanMetroTransit() {
  metroGroup.clear();

  const tunnelZ = -42;
  const tunnelY = -15;
  const tunnelLength = 200;

  const tunnelGeo = new THREE.CylinderGeometry(4.5, 4.5, tunnelLength, 24, 1, true);
  tunnelGeo.rotateZ(Math.PI / 2);
  const tunnelMat = new THREE.MeshStandardMaterial({ color: PALETTE.METRO_TUBE, roughness: 0.7, side: THREE.DoubleSide });
  const tunnel = new THREE.Mesh(tunnelGeo, tunnelMat);
  tunnel.position.set(0, tunnelY, tunnelZ);
  metroGroup.add(tunnel);

  const trackSlab = new THREE.Mesh(
    new THREE.BoxGeometry(tunnelLength, 0.4, 4.8),
    new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.9 })
  );
  trackSlab.position.set(0, tunnelY - 3.4, tunnelZ);
  metroGroup.add(trackSlab);

  for (let rz of [-1.3, 1.3]) {
    const rail = new THREE.Mesh(
      new THREE.BoxGeometry(tunnelLength, 0.16, 0.1),
      new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8 })
    );
    rail.position.set(0, tunnelY - 3.1, tunnelZ + rz);
    metroGroup.add(rail);
  }

  const trainGroup = new THREE.Group();
  const trainBody = new THREE.Mesh(
    new THREE.BoxGeometry(32, 3.4, 3.4),
    new THREE.MeshStandardMaterial({ color: PALETTE.METRO_TRAIN, roughness: 0.3, metalness: 0.5 })
  );
  trainBody.position.y = 1.7;
  trainGroup.add(trainBody);

  const stripe = new THREE.Mesh(
    new THREE.BoxGeometry(32.1, 0.4, 3.42),
    new THREE.MeshStandardMaterial({ color: 0xef4444 })
  );
  stripe.position.y = 1.3;
  trainGroup.add(stripe);

  for (let tx = -13; tx <= 13; tx += 4.2) {
    const win = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 1.2, 3.46),
      new THREE.MeshBasicMaterial({ color: 0x38bdf8 })
    );
    win.position.set(tx, 1.9, 0);
    trainGroup.add(win);
  }

  trainGroup.position.set(8, tunnelY - 3.0, tunnelZ);
  metroGroup.add(trainGroup);
}

// -------------------------------------------------------------
// 11. Elevated Highway Flyover
// -------------------------------------------------------------
function buildElevatedHighwayFlyover() {
  flyoverGroup.clear();

  const flyoverY = 9.0;
  const flyoverZ = 54.0;
  const flyoverLength = 220;
  const flyoverWidth = 12.0;

  const deckGeo = new THREE.BoxGeometry(flyoverLength, 1.0, flyoverWidth);
  const deckMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.8 });
  const deck = new THREE.Mesh(deckGeo, deckMat);
  deck.position.set(0, flyoverY, flyoverZ);
  deck.castShadow = true;
  deck.receiveShadow = true;
  flyoverGroup.add(deck);

  const asphalt = new THREE.Mesh(
    new THREE.PlaneGeometry(flyoverLength, flyoverWidth * 0.94),
    new THREE.MeshStandardMaterial({ color: PALETTE.ROAD_ASPHALT, roughness: 0.88 })
  );
  asphalt.rotation.x = -Math.PI / 2;
  asphalt.position.set(0, flyoverY + 0.52, flyoverZ);
  flyoverGroup.add(asphalt);

  for (let x = -100; x <= 100; x += 12) {
    const dash = new THREE.Mesh(
      new THREE.PlaneGeometry(5.0, 0.42),
      new THREE.MeshBasicMaterial({ color: PALETTE.LINE_YELLOW })
    );
    dash.rotation.x = -Math.PI / 2;
    dash.position.set(x, flyoverY + 0.54, flyoverZ);
    flyoverGroup.add(dash);
  }

  for (let px = -90; px <= 90; px += 45) {
    const pier = new THREE.Mesh(
      new THREE.CylinderGeometry(1.5, 1.8, flyoverY, 16),
      new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 })
    );
    pier.position.set(px, flyoverY / 2, flyoverZ);
    pier.castShadow = true;
    flyoverGroup.add(pier);

    const cap = new THREE.Mesh(
      new THREE.BoxGeometry(5.0, 1.1, flyoverWidth * 0.9),
      new THREE.MeshStandardMaterial({ color: 0x334155 })
    );
    cap.position.set(px, flyoverY - 0.55, flyoverZ);
    flyoverGroup.add(cap);
  }
}

// -------------------------------------------------------------
// 12. Subsurface Utility Pipe Grid
// -------------------------------------------------------------
function buildSubsurfaceUtilityGrid() {
  utilityGroup.clear();

  const waterPipe = new THREE.Mesh(
    new THREE.CylinderGeometry(0.45, 0.45, 160, 16),
    new THREE.MeshStandardMaterial({ color: PALETTE.PIPE_WATER, roughness: 0.3, metalness: 0.2 })
  );
  waterPipe.rotation.z = Math.PI / 2;
  waterPipe.position.set(0, -2.6, 44);
  utilityGroup.add(waterPipe);

  const gasPipe = new THREE.Mesh(
    new THREE.CylinderGeometry(0.35, 0.35, 160, 16),
    new THREE.MeshStandardMaterial({ color: PALETTE.PIPE_GAS, roughness: 0.3 })
  );
  gasPipe.rotation.z = Math.PI / 2;
  gasPipe.position.set(0, -2.1, 38);
  utilityGroup.add(gasPipe);

  const pwrPipe = new THREE.Mesh(
    new THREE.CylinderGeometry(0.26, 0.26, 110, 12),
    new THREE.MeshStandardMaterial({ color: PALETTE.PIPE_POWER, roughness: 0.3 })
  );
  pwrPipe.rotation.x = Math.PI / 2;
  pwrPipe.position.set(6, -1.9, 8);
  utilityGroup.add(pwrPipe);

  const sewerPipe = new THREE.Mesh(
    new THREE.CylinderGeometry(0.7, 0.7, 160, 16),
    new THREE.MeshStandardMaterial({ color: PALETTE.PIPE_SEWER, roughness: 0.5 })
  );
  sewerPipe.rotation.z = Math.PI / 2;
  sewerPipe.position.set(0, -4.0, 58);
  utilityGroup.add(sewerPipe);

  for (let mx of [-45, 0, 45]) {
    const manhole = new THREE.Mesh(
      new THREE.CylinderGeometry(0.75, 0.75, 4.0, 12),
      new THREE.MeshStandardMaterial({ color: 0x475569 })
    );
    manhole.position.set(mx, -2.0, 44);
    utilityGroup.add(manhole);
  }
}

// -------------------------------------------------------------
// 13. LiDAR Point Cloud Layer
// -------------------------------------------------------------
function buildLiDARPointCloud() {
  pointCloudGroup.clear();
  const rawPoints = buildingData.point_cloud || [];
  if (!rawPoints.length) return;

  const geom = new THREE.BufferGeometry();
  const positions = [];
  const colors = [];

  rawPoints.forEach(p => {
    positions.push(p.x, p.z, p.y);

    const normalizedZ = THREE.MathUtils.clamp((p.z + 5) / 50, 0, 1);
    const col = new THREE.Color().setHSL(0.65 - normalizedZ * 0.65, 1.0, 0.55);
    colors.push(col.r, col.g, col.b);
  });

  geom.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  geom.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

  const mat = new THREE.PointsMaterial({
    size: 0.45,
    vertexColors: true,
    transparent: true,
    opacity: 0.85
  });

  const pCloud = new THREE.Points(geom, mat);
  pointCloudGroup.add(pCloud);
  pointCloudGroup.visible = false;
}

// -------------------------------------------------------------
// 14. UI Synchronization & Multi-City Switcher
// -------------------------------------------------------------
function renderTopStats() {
  document.getElementById('stat-floors').textContent = buildingData.detected_floor_count || 17;
  document.getElementById('stat-ulpins').textContent = buildingData.total_ulpins || 149;
  const conflictEl = document.getElementById('stat-conflicts');
  conflictEl.textContent = buildingData.total_conflicts || 2;
  if (buildingData.total_conflicts > 0) conflictEl.classList.add('conflict-alert');
}

function renderFloorStackUI() {
  const container = document.getElementById('floor-stack-list');
  container.innerHTML = '';

  const activeUnits = buildingData.units.filter(u => u.building_id === currentBuildingId);
  const floorNos = Array.from(new Set(activeUnits.map(u => u.floor_no))).sort((a, b) => b - a);

  const bldgObj = buildingData.buildings.find(b => b.building_id === currentBuildingId);
  const bldgTitle = bldgObj ? bldgObj.name : "Tower A";
  document.getElementById('current-bldg-name').textContent = bldgTitle;

  floorNos.forEach(floorNo => {
    const units = activeUnits.filter(u => u.floor_no === floorNo);
    const hasConflict = units.some(u => u.conflict);

    const floorBlock = document.createElement('div');
    floorBlock.className = `floor-block ${hasConflict ? 'has-conflict' : ''}`;

    let floorTitle = `Floor ${floorNo}`;
    if (floorNo === 0) floorTitle = 'Grand Lobby (Ground)';
    if (floorNo === -1) floorTitle = 'Basement 1 (B1)';
    if (floorNo === -2) floorTitle = 'Basement 2 (B2)';
    if (floorNo <= -3) floorTitle = `Subterranean (${floorNo})`;

    floorBlock.innerHTML = `
      <div class="floor-label-row">
        <span class="floor-name">${floorTitle}</span>
        <span style="font-size: 10px; color: ${hasConflict ? 'var(--accent-conflict)' : 'var(--text-muted)'}">
          ${hasConflict ? '⚠ Conflict' : `${units.length} Unit${units.length > 1 ? 's' : ''}`}
        </span>
      </div>
      <div class="units-grid" id="grid-${currentBuildingId}-${floorNo}"></div>
    `;

    container.appendChild(floorBlock);

    const grid = floorBlock.querySelector(`#grid-${currentBuildingId}-${floorNo}`);
    units.forEach(unit => {
      const btn = document.createElement('div');
      btn.className = `unit-card-btn ${unit.conflict ? 'conflict' : ''}`;
      btn.id = `btn-unit-${unit.unit_id}`;

      let tagClass = `tag-${unit.space_type.toLowerCase()}`;
      if (unit.conflict) tagClass = 'tag-conflict';

      btn.innerHTML = `
        <span class="unit-title">${unit.flat_label || unit.unit_id}</span>
        <span class="unit-type-tag ${tagClass}">${unit.space_type}</span>
      `;

      btn.addEventListener('click', () => selectUnit(unit.unit_id));
      grid.appendChild(btn);
    });
  });
}

function switchSociety(socId) {
  if (!buildingData.societies || !buildingData.societies[socId]) return;
  const soc = buildingData.societies[socId];

  buildingData.active_society_id = socId;
  buildingData.buildings = soc.buildings;
  buildingData.units = soc.units;
  buildingData.point_cloud = soc.point_cloud;
  buildingData.detected_floor_count = soc.detected_floor_count;
  buildingData.total_ulpins = soc.total_ulpins;
  buildingData.total_conflicts = soc.total_conflicts;
  buildingData.society_name = soc.name;
  buildingData.city = soc.city;
  buildingData.state = soc.state;
  buildingData.district = soc.district;
  buildingData.village = soc.village;
  buildingData.surface_parcel = soc.surface_parcel;
  buildingData.gov_authority = soc.gov_authority;
  buildingData.streets = soc.streets || [];
  buildingData.piazzas = soc.piazzas || [];

  const subEl = document.getElementById('brand-subtitle');
  if (subEl) {
    subEl.innerHTML = `<span class="badge-gov" id="brand-badge">${soc.gov_authority}</span> ${soc.name} · ${soc.city} · Parcel ${soc.surface_parcel}`;
  }

  societyGroup.clear();
  parkingGroup.clear();
  metroGroup.clear();
  flyoverGroup.clear();
  utilityGroup.clear();
  pointCloudGroup.clear();
  cloudGroup.clear();

  unitMeshes = [];
  floorGroups = {};
  slabMeshes = [];
  selectedUnitId = null;

  buildIndianWeatherClouds();
  buildSocietyLandscapedPark();
  buildHighRiseTowers();

  // Society-specific infrastructure (skip for city map)
  const isCityMap = soc.buildings && soc.buildings.length > 0 && soc.buildings[0].arch_type;
  if (!isCityMap) {
    buildUndergroundParkingLevels();
    buildSubterraneanMetroTransit();
    buildElevatedHighwayFlyover();
    buildSubsurfaceUtilityGrid();
  }
  buildLiDARPointCloud();

  renderTowerSwitcherTabs();

  if (soc.buildings && soc.buildings.length > 0) {
    switchBuilding(soc.buildings[0].building_id);
  }

  renderTopStats();
  closeDetailsCard();
  resetView();
}

function renderTowerSwitcherTabs() {
  const container = document.getElementById('bldg-switcher-tabs');
  if (!container) return;
  container.innerHTML = '';

  const iconMap = {
    T01: '🏢 Tower A',
    T02: '🏢 Tower B',
    T03: '🏢 Tower C',
    T04: '🏢 Tower D',
    T05: '🏢 Tower E',
    COM01: '🏦 Arcade',
    INF_FLY: '🌉 Flyover',
    INF_MTR: '🚇 Metro',
    INF_UTL: '💧 Utilities'
  };

  const buildings = buildingData.buildings || [];

  // For cadastral city with many buildings, show a compact search/select
  if (buildings.length > 15) {
    // Zone summary buttons
    const zones = {};
    buildings.forEach(b => {
      const zone = b.zone || (b.building_id.startsWith('INF_') ? 'INFRA' :
                              b.building_id.startsWith('COM') ? 'COM' : 'RES');
      if (!zones[zone]) zones[zone] = [];
      zones[zone].push(b);
    });

    const zoneLabels = {
      RES_DENSE: '🏘️ Dense Residential',
      RES_MED: '🏠 Medium Residential',
      COM: '🏪 Commercial',
      GOV: '🏛️ Government',
      AGR: '🌾 Agricultural',
      INFRA: '🔧 Infrastructure'
    };

    // Plot search box
    const searchDiv = document.createElement('div');
    searchDiv.style.cssText = 'padding:4px;width:100%;';
    searchDiv.innerHTML = `<input type="text" id="plot-search" placeholder="🔍 Plot #..."
      style="width:100%;padding:4px 8px;border-radius:6px;border:1px solid rgba(255,255,255,0.2);
      background:rgba(0,0,0,0.3);color:#fff;font-size:11px;outline:none;"
      onkeyup="filterPlotTabs(this.value)">`;
    container.appendChild(searchDiv);

    // Zone category buttons
    Object.entries(zones).forEach(([zone, blds]) => {
      const zoneBtn = document.createElement('button');
      zoneBtn.className = 'bldg-tab-btn';
      zoneBtn.style.cssText = 'font-size:10px;padding:3px 6px;white-space:nowrap;';
      zoneBtn.textContent = `${(zoneLabels[zone] || zone)} (${blds.length})`;
      zoneBtn.onclick = () => {
        // Show first building in this zone
        if (blds.length > 0) switchBuilding(blds[0].building_id);
      };
      container.appendChild(zoneBtn);
    });

    // Individual plot buttons (scrollable)
    const plotsWrap = document.createElement('div');
    plotsWrap.id = 'plots-scroll-list';
    plotsWrap.style.cssText = 'display:flex;flex-wrap:wrap;gap:2px;max-height:200px;overflow-y:auto;padding:2px;';
    buildings.forEach((b, idx) => {
      const btn = document.createElement('button');
      btn.className = `bldg-tab-btn plot-tab-btn ${idx === 0 ? 'active' : ''}`;
      btn.dataset.bldg = b.building_id;
      const plotNum = b.plot_number || b.building_id.replace('PLT', '');
      btn.textContent = plotNum;
      btn.style.cssText = 'font-size:9px;padding:2px 5px;min-width:auto;';
      btn.title = b.name || b.building_id;
      btn.onclick = () => switchBuilding(b.building_id);
      plotsWrap.appendChild(btn);
    });
    container.appendChild(plotsWrap);

  } else {
    // Standard tower tabs for small societies
    buildings.forEach((b, idx) => {
      const btn = document.createElement('button');
      btn.className = `bldg-tab-btn ${idx === 0 ? 'active' : ''}`;
      btn.dataset.bldg = b.building_id;
      btn.textContent = iconMap[b.building_id] || `🏢 ${b.building_id}`;
      btn.onclick = () => switchBuilding(b.building_id);
      container.appendChild(btn);
    });
  }
}

// Filter plot tabs by search query
function filterPlotTabs(query) {
  const btns = document.querySelectorAll('.plot-tab-btn');
  const q = query.trim().toLowerCase();
  btns.forEach(btn => {
    const plotNum = btn.textContent.toLowerCase();
    const title = (btn.title || '').toLowerCase();
    btn.style.display = (!q || plotNum.includes(q) || title.includes(q)) ? '' : 'none';
  });
}

function switchBuilding(bldgId) {
  currentBuildingId = bldgId;
  document.querySelectorAll('.bldg-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.bldg === bldgId);
  });

  renderFloorStackUI();

  // Static targets for known tower layouts
  const staticTargets = {
    T01: [-32, 24, -16, 68],
    T02: [-12, 26, -26, 72],
    T03: [12, 26, -26, 72],
    T04: [32, 24, -16, 68],
    COM01: [0, 6, 26, 42],
    INF_FLY: [0, 9, 54, 75],
    INF_MTR: [0, -15, -42, 65],
    INF_UTL: [0, -3, 20, 60]
  };

  let t = staticTargets[bldgId];

  // Dynamic target from building metadata (for cadastral city plots)
  if (!t) {
    const bMeta = (buildingData.buildings || []).find(b => b.building_id === bldgId);
    if (bMeta && bMeta.center_pos) {
      const maxFloor = Math.max(...(bMeta.floors || [0]));
      const camHeight = Math.max(8, maxFloor * 3 * 0.6);
      t = [bMeta.center_pos[0], camHeight, bMeta.center_pos[2], Math.max(30, camHeight * 2)];
    } else {
      t = [0, 12, 0, 75];
    }
  }

  targetX = t[0];
  targetY = t[1];
  targetZ = t[2];
  radius = t[3];
  updateCameraPosition();
}

function selectUnit(unitId) {
  selectedUnitId = unitId;
  const unit = buildingData.units.find(u => u.unit_id === unitId);
  if (!unit) return;

  if (unit.building_id !== currentBuildingId) {
    switchBuilding(unit.building_id);
  }

  document.querySelectorAll('.unit-card-btn').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById(`btn-unit-${unitId}`);
  if (activeBtn) activeBtn.classList.add('active');

  unitMeshes.forEach(mesh => {
    if (mesh.userData.unit_id === unitId) {
      mesh.material.opacity = 0.75;
      mesh.material.color = new THREE.Color(0x00d2ff);
    } else {
      mesh.material.opacity = mesh.userData.conflict ? 0.45 : 0.0;
      mesh.material.color = new THREE.Color(mesh.userData.conflict ? 0xff4757 : 0x3b82f6);
    }
  });

  showDetailsCard(unit);
}

function showDetailsCard(unit) {
  const panel = document.getElementById('details-card-panel');
  let floorName = `Floor ${unit.floor_no}`;
  if (unit.floor_no === 0) floorName = 'Grand Lobby';
  if (unit.floor_no === -1) floorName = 'Basement 1';
  if (unit.floor_no === -2) floorName = 'Basement 2';
  if (unit.floor_no <= -3) floorName = `Subterranean (${unit.floor_no})`;

  document.getElementById('card-title').textContent = unit.flat_label || unit.unit_id;
  document.getElementById('card-subtitle').textContent = `${unit.building_name || 'Complex'} · ${floorName}`;
  document.getElementById('card-ulpin').textContent = unit.ulpin;
  document.getElementById('card-owner').textContent = unit.owner || 'ABC';
  document.getElementById('card-floor').textContent = floorName;
  document.getElementById('card-area').textContent = `${unit.area_sqm || 110} m²`;
  document.getElementById('card-height').textContent = `${unit.z_min}m to ${unit.z_max}m`;

  // Room layout (for city map buildings)
  const roomsEl = document.getElementById('card-rooms');
  if (roomsEl) {
    const rooms = unit.rooms || [];
    if (rooms.length > 0) {
      const bhkLabel = unit.bhk_type ? `<b style="color:#00ff88;font-size:13px">${unit.bhk_type.toUpperCase()}</b><br>` : '';
      roomsEl.innerHTML = bhkLabel + rooms.map(r =>
        `<span style="display:inline-block;background:rgba(255,255,255,0.08);border-radius:4px;padding:2px 6px;margin:1px;font-size:10px">
          ${r.label || r.type} (${r.w}×${r.d}m)
        </span>`
      ).join('');
      roomsEl.style.display = 'block';
    } else {
      roomsEl.style.display = 'none';
    }
  }

  // Valuation
  const valEl = document.getElementById('card-valuation');
  if (valEl) {
    valEl.textContent = unit.valuation_inr ? `₹${(unit.valuation_inr / 100000).toFixed(1)} Lakh` : '—';
  }

  const statusBadge = document.getElementById('card-status-badge');
  const conflictBox = document.getElementById('card-conflict-box');

  if (unit.conflict) {
    statusBadge.className = 'status-badge conflict';
    statusBadge.innerHTML = '⚠ Encroachment Conflict';
    conflictBox.style.display = 'block';
    conflictBox.textContent = unit.conflict_details || 'Spatial footprint intersects with neighboring parcel.';
  } else {
    statusBadge.className = 'status-badge valid';
    statusBadge.innerHTML = '✔ Valid Parcel';
    conflictBox.style.display = 'none';
  }

  const interiorBtn = document.getElementById('btn-inspect-interior');
  if (interiorBtn) {
    interiorBtn.style.display = (unit.space_type === 'RES' || (unit.rooms && unit.rooms.length > 0)) ? 'flex' : 'none';
  }

  panel.style.display = 'flex';
}

function closeDetailsCard() {
  document.getElementById('details-card-panel').style.display = 'none';
  selectedUnitId = null;
  document.querySelectorAll('.unit-card-btn').forEach(btn => btn.classList.remove('active'));
  unitMeshes.forEach(mesh => {
    mesh.material.opacity = mesh.userData.conflict ? 0.45 : 0.0;
  });
}

// -------------------------------------------------------------
// 15. Subsurface X-Ray & Layer Visibility Toggles
// -------------------------------------------------------------
function toggleSubsurfaceXRay() {
  isXRayMode = !isXRayMode;
  document.getElementById('btn-tool-xray').classList.toggle('active', isXRayMode);

  if (groundPlane) {
    groundPlane.material.opacity = isXRayMode ? 0.16 : 0.98;
    groundPlane.material.needsUpdate = true;
  }
  if (plotPlane) {
    plotPlane.material.opacity = isXRayMode ? 0.04 : 0.05;
    plotPlane.material.needsUpdate = true;
  }
}

function toggleParkingLayer() {
  isParkingVisible = !isParkingVisible;
  parkingGroup.visible = isParkingVisible;
  document.getElementById('btn-tool-parking').classList.toggle('active', isParkingVisible);
}

function toggleMetroLayer() {
  isMetroVisible = !isMetroVisible;
  metroGroup.visible = isMetroVisible;
  document.getElementById('btn-tool-metro').classList.toggle('active', isMetroVisible);
}

function toggleFlyoverLayer() {
  isFlyoverVisible = !isFlyoverVisible;
  flyoverGroup.visible = isFlyoverVisible;
  document.getElementById('btn-tool-flyover').classList.toggle('active', isFlyoverVisible);
}

function toggleSubsurfaceUtilities() {
  isUtilityVisible = !isUtilityVisible;
  utilityGroup.visible = isUtilityVisible;
  document.getElementById('btn-tool-utility').classList.toggle('active', isUtilityVisible);
}

function togglePointCloud() {
  isPointCloudVisible = !isPointCloudVisible;
  pointCloudGroup.visible = isPointCloudVisible;
  document.getElementById('btn-tool-lidar').classList.toggle('active', isPointCloudVisible);
}

function toggleMeasureMode() {
  isMeasureMode = !isMeasureMode;
  document.getElementById('btn-tool-measure').classList.toggle('active', isMeasureMode);
  document.getElementById('measure-banner').style.display = isMeasureMode ? 'flex' : 'none';

  if (!isMeasureMode && measureLine) {
    scene.remove(measureLine);
    measureLine = null;
    measurePoints = [];
  }
}

function setCameraScene(mode) {
  const isLargeCity = (buildingData.buildings || []).length > 15;
  const scaleR = isLargeCity ? 2.8 : 1;

  if (mode === 'top') {
    targetX = 0; targetY = 0; targetZ = 5;
    theta = 0;
    phi = 0.001;
    radius = isInteriorMode ? 18 : 120 * scaleR;
  } else if (mode === 'drone') {
    targetX = 0; targetY = isLargeCity ? 40 : 16; targetZ = 0;
    theta = Math.PI / 4;
    phi = Math.PI / 3.4;
    radius = 100 * scaleR;
  } else if (mode === 'street') {
    targetX = 14; targetY = 4; targetZ = 8;
    theta = -Math.PI / 6;
    phi = Math.PI / 2.15;
    radius = 35 * scaleR;
  } else if (mode === 'isometric') {
    targetX = 0; targetY = isLargeCity ? 40 : 14; targetZ = 0;
    theta = Math.PI / 4;
    phi = Math.PI / 3.5;
    radius = 80 * scaleR;
  }
  updateCameraPosition();
}

function setExplodeFactor(val) {
  explodeFactor = val;
  Object.keys(floorGroups).forEach(key => {
    const floorNo = Number(key.split('_')[1]);
    const groups = floorGroups[key];
    const verticalShift = floorNo * val * 3.5;
    groups.forEach(g => {
      g.position.y = g.userData.baseCy + verticalShift;
    });
  });

  slabMeshes.forEach(item => {
    const verticalShift = item.floorNo * val * 3.5;
    item.mesh.position.y = item.baseElevation + verticalShift;
  });
}

function toggleDayNight() {
  isDayMode = !isDayMode;
  if (isDayMode) {
    scene.background = new THREE.Color(0x7ec8f8);
    scene.fog.color = new THREE.Color(0xd1e7fd);
    dirLight.intensity = 2.0;
    hemiLight.intensity = 0.95;
    ambientLight.intensity = 0.65;
    cloudGroup.visible = true;
  } else {
    scene.background = new THREE.Color(0x020617);
    scene.fog.color = new THREE.Color(0x020617);
    dirLight.intensity = 0.4;
    hemiLight.intensity = 0.25;
    ambientLight.intensity = 0.2;
    cloudGroup.visible = false;
  }
}

// -------------------------------------------------------------
// 16. Detailed BIM 3D Interior Floor Plans (Distinct for each unit type)
// -------------------------------------------------------------
function buildDetailedInteriorModel(unit) {
  interiorGroup.clear();

  const isPenthouse = unit.unit_id.includes('PENT') || unit.floor_no >= 16;
  const is4BHK = unit.flat_label && unit.flat_label.includes('4BHK') || unit.floor_no >= 10;
  const isCommercial = unit.space_type === 'COM';
  const isParking = unit.space_type === 'PRK';

  // Floor Dimensions
  const floorW = isPenthouse ? 20 : (isCommercial ? 18 : 16);
  const floorD = isPenthouse ? 16 : (isCommercial ? 12 : 13);
  const wallH = 2.8;

  // 1. Flooring
  let floorColor = 0xd97706; // Hardwood
  if (isPenthouse) floorColor = 0xf8fafc; // Polished Italian White Marble
  else if (isCommercial) floorColor = 0x94a3b8; // Terrazzo
  else if (isParking) floorColor = 0x334155; // Concrete
  else if (!is4BHK) floorColor = 0xf1f5f9; // Porcelain tiles

  const floorGeo = new THREE.BoxGeometry(floorW, 0.2, floorD);
  const floorMat = new THREE.MeshStandardMaterial({ color: floorColor, roughness: isPenthouse ? 0.2 : 0.6 });
  const floorMesh = new THREE.Mesh(floorGeo, floorMat);
  floorMesh.position.y = -0.1;
  floorMesh.receiveShadow = true;
  interiorGroup.add(floorMesh);

  // 2. Perimeter Walls (Cutaway half-height so interior is crystal clear)
  const wallMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.85 });
  const backWall = new THREE.Mesh(new THREE.BoxGeometry(floorW, wallH, 0.3), wallMat);
  backWall.position.set(0, wallH / 2, -floorD / 2 + 0.15);
  interiorGroup.add(backWall);

  const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.3, wallH, floorD), wallMat);
  leftWall.position.set(-floorW / 2 + 0.15, wallH / 2, 0);
  interiorGroup.add(leftWall);

  const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.3, wallH, floorD), wallMat);
  rightWall.position.set(floorW / 2 - 0.15, wallH / 2, 0);
  interiorGroup.add(rightWall);

  // -----------------------------------------------------------
  // TYPE A: SKY VILLA PENTHOUSE (Duplex Living, Jacuzzi, King Suite)
  // -----------------------------------------------------------
  if (isPenthouse) {
    // Grand Sectional L-Sofa (Deep Navy Velvet)
    const sofaMat = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.5 });
    const sofaMain = new THREE.Mesh(new THREE.BoxGeometry(5.4, 0.7, 1.8), sofaMat);
    sofaMain.position.set(-4.0, 0.35, 1.5);
    interiorGroup.add(sofaMain);

    const sofaReturn = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.7, 3.2), sofaMat);
    sofaReturn.position.set(-2.2, 0.35, 3.2);
    interiorGroup.add(sofaReturn);

    // Glass & Gold Coffee Table
    const table = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.4, 1.4),
      new THREE.MeshStandardMaterial({ color: 0xfacc15, metalness: 0.8, roughness: 0.2 })
    );
    table.position.set(-4.0, 0.2, 3.2);
    interiorGroup.add(table);

    // 85-inch Curved OLED TV Media Wall
    const tvWall = new THREE.Mesh(new THREE.BoxGeometry(0.2, 2.2, 4.2), new THREE.MeshStandardMaterial({ color: 0x0f172a }));
    tvWall.position.set(-floorW / 2 + 0.3, 1.3, 2.2);
    interiorGroup.add(tvWall);

    const tvScreen = new THREE.Mesh(new THREE.BoxGeometry(0.05, 1.5, 3.2), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
    tvScreen.position.set(-floorW / 2 + 0.45, 1.4, 2.2);
    interiorGroup.add(tvScreen);

    // Private Heated Plunge Pool / Terrace Jacuzzi (Directly in Penthouse!)
    const poolRim = new THREE.Mesh(
      new THREE.CylinderGeometry(2.8, 3.0, 0.6, 24),
      new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4 })
    );
    poolRim.position.set(5.5, 0.3, -3.5);
    interiorGroup.add(poolRim);

    const poolWater = new THREE.Mesh(
      new THREE.CylinderGeometry(2.6, 2.6, 0.1, 24),
      new THREE.MeshStandardMaterial({ color: 0x06b6d4, roughness: 0.1, metalness: 0.4, transparent: true, opacity: 0.9 })
    );
    poolWater.position.set(5.5, 0.52, -3.5);
    interiorGroup.add(poolWater);

    // Master King Bed Suite
    const bed = createBedFurniture(0x78350f, 0xf8fafc);
    bed.position.set(4.8, 0, 3.0);
    interiorGroup.add(bed);

    // Chandelier
    interiorGroup.add(createChandelier(0, 2.5, 0));
  }
  // -----------------------------------------------------------
  // TYPE B: 4BHK LUXURY GOLF RESIDENCE (Living, Dining, Kitchen, Beds)
  // -----------------------------------------------------------
  else if (is4BHK) {
    // Living Lounge Sofa & Table
    const sofaMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
    const sofa = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.65, 1.6), sofaMat);
    sofa.position.set(-3.5, 0.32, 2.5);
    interiorGroup.add(sofa);

    const table = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.38, 1.2), new THREE.MeshStandardMaterial({ color: 0xb45309 }));
    table.position.set(-3.5, 0.2, 0.8);
    interiorGroup.add(table);

    // 6-Seater Wooden Dining Table
    const diningTable = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.75, 1.6), new THREE.MeshStandardMaterial({ color: 0x78350f }));
    diningTable.position.set(3.5, 0.38, -2.5);
    interiorGroup.add(diningTable);

    // Modular Kitchen Island & Stools
    const island = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.9, 1.2), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
    island.position.set(-3.5, 0.45, -3.8);
    interiorGroup.add(island);

    // Master Bed
    const mBed = createBedFurniture(0x1e293b, 0xf1f5f9);
    mBed.position.set(4.2, 0, 2.8);
    interiorGroup.add(mBed);

    // Home Office Executive Study Desk
    const desk = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.72, 1.0), new THREE.MeshStandardMaterial({ color: 0x334155 }));
    desk.position.set(0, 0.36, 4.5);
    interiorGroup.add(desk);

    const laptop = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.05, 0.4), new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8 }));
    laptop.position.set(0, 0.75, 4.5);
    interiorGroup.add(laptop);
  }
  // -----------------------------------------------------------
  // TYPE C: 3BHK MODERN RESIDENCE
  // -----------------------------------------------------------
  else if (!isCommercial && !isParking) {
    // 3-Seater Living Couch
    const couch = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.65, 1.4), new THREE.MeshStandardMaterial({ color: 0x2563eb }));
    couch.position.set(-3.0, 0.32, 2.0);
    interiorGroup.add(couch);

    const tv = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.2, 0.1), new THREE.MeshBasicMaterial({ color: 0x0284c7 }));
    tv.position.set(-3.0, 1.4, -floorD / 2 + 0.4);
    interiorGroup.add(tv);

    // 4-Seater Dining Table
    const dTable = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.72, 1.4), new THREE.MeshStandardMaterial({ color: 0xa16207 }));
    dTable.position.set(3.2, 0.36, -2.0);
    interiorGroup.add(dTable);

    // Queen Bed
    const bed = createBedFurniture(0x475569, 0xffffff);
    bed.position.set(3.4, 0, 2.5);
    interiorGroup.add(bed);

    // Modular Kitchen Counter
    const kitchen = new THREE.Mesh(new THREE.BoxGeometry(3.4, 0.85, 1.0), new THREE.MeshStandardMaterial({ color: 0x64748b }));
    kitchen.position.set(-3.0, 0.42, -4.5);
    interiorGroup.add(kitchen);
  }
  // -----------------------------------------------------------
  // TYPE D: COMMERCIAL RETAIL / BANKING ARCADES
  // -----------------------------------------------------------
  else if (isCommercial) {
    // Customer Banking / Retail Service Counter
    const counter = new THREE.Mesh(new THREE.BoxGeometry(8.0, 1.1, 1.4), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
    counter.position.set(0, 0.55, -1.0);
    interiorGroup.add(counter);

    // Acrylic Service Partitions
    const screen = new THREE.Mesh(new THREE.BoxGeometry(7.6, 0.8, 0.05), new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.6 }));
    screen.position.set(0, 1.5, -1.0);
    interiorGroup.add(screen);

    // Dual ATM Machines
    for (let ax of [-5.5, -3.8]) {
      const atm = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.8, 1.0), new THREE.MeshStandardMaterial({ color: 0x0284c7 }));
      atm.position.set(ax, 0.9, 3.5);
      interiorGroup.add(atm);

      const atmScreen = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.4, 0.05), new THREE.MeshBasicMaterial({ color: 0x22d3ee }));
      atmScreen.position.set(ax, 1.2, 3.0);
      interiorGroup.add(atmScreen);
    }

    // Customer Waiting Seats (Row of 4)
    for (let sx = 1.5; sx <= 5.5; sx += 1.3) {
      const seat = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.45, 0.8), new THREE.MeshStandardMaterial({ color: 0xef4444 }));
      seat.position.set(sx, 0.25, 3.5);
      interiorGroup.add(seat);
    }
  }
  // -----------------------------------------------------------
  // TYPE E: UNDERGROUND PARKING BAY (Smart EV Supercharger & Stall)
  // -----------------------------------------------------------
  else if (isParking) {
    // Yellow Diagonal Hazard Parking Stripes
    for (let px = -5.0; px <= 5.0; px += 2.0) {
      const stripe = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 4.8), new THREE.MeshBasicMaterial({ color: 0xfacc15 }));
      stripe.rotation.x = -Math.PI / 2;
      stripe.position.set(px, 0.02, 0);
      interiorGroup.add(stripe);
    }

    // Smart Wall-Mounted EV Supercharger Terminal
    const charger = new THREE.Mesh(new THREE.BoxGeometry(0.8, 1.4, 0.4), new THREE.MeshStandardMaterial({ color: 0x10b981 }));
    charger.position.set(-6.0, 1.4, 0);
    interiorGroup.add(charger);

    const ledGlow = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.3, 0.05), new THREE.MeshBasicMaterial({ color: 0x34d399 }));
    ledGlow.position.set(-5.8, 1.6, 0);
    interiorGroup.add(ledGlow);

    // Concrete Support Column with Black/Yellow Warning Stripes
    const pillar = new THREE.Mesh(new THREE.BoxGeometry(1.2, wallH, 1.2), new THREE.MeshStandardMaterial({ color: 0x64748b }));
    pillar.position.set(6.0, wallH / 2, 0);
    interiorGroup.add(pillar);

    // Parked Luxury Sedan Plugged in
    const car = createLuxurySedan(0, 0, 0, PALETTE.CAR_WHITE_METALLIC, Math.PI / 2);
    interiorGroup.add(car);
  }

  interiorGroup.position.set(0, 0, 0);
}

function createBedFurniture(frameColor, linenColor) {
  const bedGroup = new THREE.Group();

  const frame = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.55, 4.4), new THREE.MeshStandardMaterial({ color: frameColor, roughness: 0.6 }));
  frame.position.y = 0.28;
  bedGroup.add(frame);

  const headboard = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.4, 0.3), new THREE.MeshStandardMaterial({ color: frameColor }));
  headboard.position.set(0, 0.7, -2.2);
  bedGroup.add(headboard);

  const mattress = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.35, 4.0), new THREE.MeshStandardMaterial({ color: linenColor, roughness: 0.85 }));
  mattress.position.y = 0.65;
  bedGroup.add(mattress);

  for (let px of [-0.85, 0.85]) {
    const pillow = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.16, 0.75), new THREE.MeshStandardMaterial({ color: 0x1e3a8a }));
    pillow.position.set(px, 0.88, -1.4);
    bedGroup.add(pillow);
  }

  return bedGroup;
}

function createChandelier(x, y, z) {
  const chan = new THREE.Group();
  const centerHub = new THREE.Mesh(
    new THREE.CylinderGeometry(0.2, 0.2, 0.15, 12),
    new THREE.MeshStandardMaterial({ color: 0xfacc15, metalness: 0.8 })
  );
  chan.add(centerHub);

  for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI * 2) / 6;
    const globe = new THREE.Mesh(
      new THREE.SphereGeometry(0.24, 16, 16),
      new THREE.MeshBasicMaterial({ color: 0xfef08a })
    );
    globe.position.set(Math.sin(angle) * 0.9, 0, Math.cos(angle) * 0.9);
    chan.add(globe);
  }
  chan.position.set(x, y, z);
  return chan;
}

function enterInteriorMode() {
  const unit = buildingData.units.find(u => u.unit_id === selectedUnitId) || buildingData.units[0];
  isInteriorMode = true;

  societyGroup.visible = false;
  parkingGroup.visible = false;
  metroGroup.visible = false;
  flyoverGroup.visible = false;
  utilityGroup.visible = false;
  cloudGroup.visible = false;

  // Generate the specific detailed 3D interior tailored to this unit!
  buildDetailedInteriorModel(unit);
  interiorGroup.visible = true;

  document.getElementById('interior-hud').style.display = 'flex';
  document.getElementById('details-card-panel').style.display = 'none';
  document.getElementById('building-stack-panel').style.display = 'none';
  document.getElementById('hud-flat-title').textContent = `${unit.flat_label || 'Apartment'} - 3D BIM Interior Plan`;

  // Optimal isometric viewing angle into the flat
  targetX = 0;
  targetY = 0;
  targetZ = 0;
  radius = 26;
  theta = Math.PI / 4;
  phi = Math.PI / 3.4;
  updateCameraPosition();
}

function exitInteriorMode() {
  isInteriorMode = false;
  societyGroup.visible = true;
  parkingGroup.visible = isParkingVisible;
  metroGroup.visible = isMetroVisible;
  flyoverGroup.visible = isFlyoverVisible;
  utilityGroup.visible = isUtilityVisible;
  cloudGroup.visible = isDayMode;
  interiorGroup.visible = false;

  document.getElementById('interior-hud').style.display = 'none';
  document.getElementById('building-stack-panel').style.display = 'flex';
  if (selectedUnitId) showDetailsCard(buildingData.units.find(u => u.unit_id === selectedUnitId));

  setCameraScene('isometric');
}

function openPropertyDeed() {
  const unit = buildingData.units.find(u => u.unit_id === selectedUnitId) || buildingData.units[0];
  document.getElementById('deed-ulpin').textContent = unit.ulpin;
  document.getElementById('deed-owner').textContent = unit.owner;
  document.getElementById('deed-building').textContent = unit.building_name || "Tower A";
  document.getElementById('deed-floor').textContent = `Floor ${unit.floor_no}`;
  document.getElementById('deed-area').textContent = `${unit.area_sqm} sq.m`;
  document.getElementById('deed-elevation').textContent = `${unit.z_min}m to ${unit.z_max}m`;
  document.getElementById('deed-valuation').textContent = `₹ ${Number(unit.valuation_inr || 9500000).toLocaleString('en-IN')}`;
  document.getElementById('deed-modal').style.display = 'flex';
}

function closePropertyDeed() {
  document.getElementById('deed-modal').style.display = 'none';
}

// -------------------------------------------------------------
// 17. Camera Controls & Raycasting
// -------------------------------------------------------------
let radius = 80, theta = Math.PI / 4, phi = Math.PI / 3.5;
let targetX = 0, targetY = 14, targetZ = 0;

function updateCameraPosition() {
  camera.position.x = targetX + radius * Math.sin(phi) * Math.sin(theta);
  camera.position.y = targetY + radius * Math.cos(phi);
  camera.position.z = targetZ + radius * Math.sin(phi) * Math.cos(theta);
  camera.lookAt(targetX, targetY, targetZ);
}

function setupCameraControls(container) {
  updateCameraPosition();

  let isDragging = false, lastX = 0, lastY = 0;
  let isPanning = false;

  container.addEventListener('mousedown', e => {
    isDragging = true;
    isPanning = (e.button === 2 || e.shiftKey);
    lastX = e.clientX;
    lastY = e.clientY;
  });

  window.addEventListener('mouseup', () => { isDragging = false; isPanning = false; });

  window.addEventListener('mousemove', e => {
    if (!isDragging) return;
    const dx = e.clientX - lastX;
    const dy = e.clientY - lastY;

    if (isPanning) {
      targetX -= dx * 0.05;
      targetY += dy * 0.05;
    } else {
      theta -= dx * 0.006;
      phi = Math.min(Math.max(phi - dy * 0.006, 0.001), Math.PI / 2 - 0.01);
    }
    lastX = e.clientX;
    lastY = e.clientY;
    updateCameraPosition();
  });

  container.addEventListener('wheel', e => {
    radius = Math.min(Math.max(radius + e.deltaY * 0.035, 10), 220);
    updateCameraPosition();
  });

  container.addEventListener('contextmenu', e => e.preventDefault());
}

function setupRaycaster(container) {
  const raycaster = new THREE.Raycaster();
  const mouse = new THREE.Vector2();
  let dragTime = 0;

  container.addEventListener('mousedown', () => dragTime = Date.now());

  container.addEventListener('mouseup', e => {
    if (Date.now() - dragTime > 220) return;

    mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);

    if (isMeasureMode) {
      const intersects = raycaster.intersectObjects(unitMeshes);
      if (intersects.length > 0) {
        const pt = intersects[0].point;
        measurePoints.push(pt);
        if (measurePoints.length === 2) {
          const dist = measurePoints[0].distanceTo(measurePoints[1]);
          document.getElementById('measure-banner').innerHTML = `📏 Measured Distance: <b>${dist.toFixed(2)} meters</b>`;
          
          if (measureLine) scene.remove(measureLine);
          const geo = new THREE.BufferGeometry().setFromPoints(measurePoints);
          measureLine = new THREE.Line(geo, new THREE.LineBasicMaterial({ color: 0x00d2ff, linewidth: 3 }));
          scene.add(measureLine);
          measurePoints = [];
        }
      }
      return;
    }

    if (!isInteriorMode) {
      const intersects = raycaster.intersectObjects(unitMeshes);
      if (intersects.length > 0) {
        selectUnit(intersects[0].object.userData.unit_id);
      }
    }
  });
}

function resetView() {
  const firstBldg = (buildingData.buildings && buildingData.buildings.length > 0)
    ? buildingData.buildings[0].building_id : 'T01';
  switchBuilding(firstBldg);
  setCameraScene('isometric');
  setExplodeFactor(0);
  const slider = document.getElementById('explode-slider');
  if (slider) slider.value = 0;
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

// Slowly animate drifting clouds across the sky
function animate() {
  requestAnimationFrame(animate);
  
  if (cloudGroup && cloudGroup.children) {
    cloudGroup.children.forEach((c, idx) => {
      c.position.x += 0.015 * (1 + (idx % 3) * 0.3);
      if (c.position.x > 180) c.position.x = -180;
    });
  }

  renderer.render(scene, camera);
}

window.addEventListener('DOMContentLoaded', () => {
  initScene();
  animate();
});
