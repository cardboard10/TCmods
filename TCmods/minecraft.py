# minimal_minecraft_pygame.py
# Requirements: Python 3.10+ and pygame
# pip install pygame
import sys, os, math, random, time
import pygame

# ---------- Config ----------
WIDTH, HEIGHT = 960, 540
FOV_DEG = 80
NEAR_PLANE = 0.05
FAR_PLANE = 100.0
MOUSE_SENS = 0.15
MOVE_SPEED = 6.0
FLY_MODE = True          # True = noclip fly; False = gravity/jump (basic)
GRAVITY = 18.0
JUMP_SPEED = 7.5
AIR_FRICTION = 0.90
WORLD_SEED = 1337
RENDER_RADIUS = 24        # Manhattan-ish radius in blocks around camera for rendering
BUILD_REACH = 6.0
FPS_CAP = 60

# Colors per block id
# 0=air, 1=grass, 2=dirt, 3=stone, 4=wood, 5=leaves
BLOCK_COLORS = {
    1: (100, 170, 80),
    2: (134, 96, 67),
    3: (128, 128, 128),
    4: (102, 81, 60),
    5: (64, 160, 64),
}
BLOCK_NAMES = {1: "Grass", 2: "Dirt", 3: "Stone", 4: "Wood", 5: "Leaves"}

# Face normals and order: +X, -X, +Y, -Y, +Z, -Z
FACE_DIRS = [
    (1, 0, 0),  (-1, 0, 0),
    (0, 1, 0),  (0, -1, 0),
    (0, 0, 1),  (0, 0, -1)
]

# Per-face brightness multiplier (approx. light)
FACE_BRIGHT = {
    (1,0,0): 0.85, (-1,0,0): 0.78,
    (0,1,0): 1.00, (0,-1,0): 0.65,
    (0,0,1): 0.90, (0,0,-1): 0.72,
}

# Sun light direction (world space, normalized)
SUN_DIR = (0.5, 1.0, 0.2)
SUN_LEN = math.sqrt(SUN_DIR[0]**2 + SUN_DIR[1]**2 + SUN_DIR[2]**2)
SUN = (SUN_DIR[0]/SUN_LEN, SUN_DIR[1]/SUN_LEN, SUN_DIR[2]/SUN_LEN)

# ---------- Math helpers ----------
def clamp(v, a, b): return a if v < a else b if v > b else v

def dot(a, b): return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def add(a, b): return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def mul(a, s): return (a[0]*s, a[1]*s, a[2]*s)

def length(v): return math.sqrt(dot(v, v))

def norm(v):
    l = length(v)
    if l == 0: return (0.0, 0.0, 0.0)
    return (v[0]/l, v[1]/l, v[2]/l)

# ---------- Camera transform ----------
class Camera:
    def __init__(self, pos=(0.0, 40.0, 0.0), yaw=0.0, pitch=0.0, fov_deg=FOV_DEG):
        self.x, self.y, self.z = pos
        self.yaw, self.pitch = yaw, pitch
        self.f = HEIGHT / (2 * math.tan(math.radians(fov_deg)*0.5))

    def dir_forward(self):
        cy, sy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
        cp, sp = math.cos(math.radians(self.pitch)), math.sin(math.radians(self.pitch))
        # Forward in world space given yaw, pitch
        return (sy*cp, -sp, cy*cp)

    def rotate_point(self, px, py, pz):
        # Transform world point into camera space
        # Translate
        x, y, z = px - self.x, py - self.y, pz - self.z
        # Yaw (around Y)
        cy, sy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
        xz = cy*x - sy*z
        zz = sy*x + cy*z
        # Pitch (around X)
        cp, sp = math.cos(math.radians(self.pitch)), math.sin(math.radians(self.pitch))
        y2 = cp*y - sp*zz
        z2 = sp*y + cp*zz
        return (xz, y2, z2)

    def project(self, x, y, z):
        if z <= NEAR_PLANE: return None
        sx = WIDTH*0.5 + (self.f * x) / z
        sy = HEIGHT*0.5 - (self.f * y) / z
        if sx < -1000 or sx > WIDTH+1000 or sy < -1000 or sy > HEIGHT+1000:
            # Let caller decide; we still return to enable coarse culling
            pass
        return (sx, sy)

# ---------- World generation (value noise + simple biome) ----------
class World:
    def __init__(self, seed=WORLD_SEED):
        self.seed = seed
        self.blocks = {}  # (x,y,z) -> block_id (omit air)
        self.rng = random.Random(seed)
        self._perm = list(range(256))
        self.rng.shuffle(self._perm)
        self._perm += self._perm

    def hash(self, x, z):
        # Deterministic pseudo-random based on integer lattice
        return self._perm[(x + self._perm[z & 255]) & 255] / 255.0

    def smoothstep(self, t):
        return t*t*(3 - 2*t)

    def value_noise2d(self, x, z, freq=1.0):
        # Value noise on integer lattice with bilinear interpolation
        x *= freq
        z *= freq
        xi, zi = math.floor(x), math.floor(z)
        xf, zf = x - xi, z - zi
        h00 = self.hash(xi,   zi)
        h10 = self.hash(xi+1, zi)
        h01 = self.hash(xi,   zi+1)
        h11 = self.hash(xi+1, zi+1)
        u, v = self.smoothstep(xf), self.smoothstep(zf)
        x1 = h00*(1-u) + h10*u
        x2 = h01*(1-u) + h11*u
        return x1*(1-v) + x2*v

    def fbm(self, x, z, octaves=5, lacunarity=2.0, gain=0.5):
        amp, freq, total = 1.0, 0.01, 0.0
        for _ in range(octaves):
            total += amp * self.value_noise2d(x, z, freq)
            amp *= gain
            freq *= lacunarity
        return total

    def height_at(self, x, z):
        base = 32
        hills = self.fbm(x, z, octaves=5)  # ~0..something
        h = base + int(hills * 18)  # scale elevation
        return max(8, min(80, h))

    def ensure_column(self, x, z):
        # Generate a vertical column if not present
        # Only generate if empty at surface; cheap guard
        top_y = self.height_at(x, z)
        key = (x, top_y, z)
        if key in self.blocks:  # already generated/modified
            return
        # Terrain layering
        for y in range(0, top_y - 4):
            self.blocks[(x, y, z)] = 3  # stone
        for y in range(top_y - 4, top_y - 1):
            self.blocks[(x, y, z)] = 2  # dirt
        self.blocks[(x, top_y - 1, z)] = 1  # grass
        # Occasional tree on grass
        rng_val = self.hash(x*13, z*17)
        if rng_val > 0.86 and top_y < 70:
            self._plant_tree(x, top_y, z)

    def _plant_tree(self, x, y, z):
        h = 4 + int(self.hash(x*7, z*9)*2)
        # trunk
        for i in range(h):
            self.blocks[(x, y+i, z)] = 4
        # leaves cube
        r = 2
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                for dz in range(-r, r+1):
                    if abs(dx)+abs(dy)+abs(dz) > 4: continue
                    self.blocks[(x+dx, y+h-1+dy, z+dz)] = 5

    def get_block(self, x, y, z):
        return self.blocks.get((x, y, z), 0)

    def set_block(self, x, y, z, bid):
        if bid == 0:
            self.blocks.pop((x, y, z), None)
        else:
            self.blocks[(x, y, z)] = bid

    def populate_region(self, cx, cz, radius):
        # Generate columns within radius around (cx,cz)
        for dx in range(-radius, radius+1):
            for dz in range(-radius, radius+1):
                if abs(dx) + abs(dz) > radius: continue
                self.ensure_column(cx+dx, cz+dz)

# ---------- Rendering ----------
# Cube vertices relative to (x,y,z)
CUBE_VERTS = [
    (0,0,0),(1,0,0),(1,1,0),(0,1,0),  # back z
    (0,0,1),(1,0,1),(1,1,1),(0,1,1)   # front z
]
# Faces as quads of indices into CUBE_VERTS and their normals
FACES = [
    ([1,5,6,2], (1,0,0)),   # +X
    ([4,0,3,7], (-1,0,0)),  # -X
    ([3,2,6,7], (0,1,0)),   # +Y
    ([0,1,5,4], (0,-1,0)),  # -Y
    ([5,4,7,6], (0,0,1)),   # +Z
    ([0,1,2,3], (0,0,-1)),  # -Z
]

def shade_color(base_rgb, normal):
    # Combine face brightness and simple directional light
    fb = FACE_BRIGHT[normal]
    n = normal
    ld = max(0.0, dot(norm(n), SUN))
    # Mix: base ambient + directional
    k = clamp(0.35 + 0.65*ld, 0.2, 1.0) * fb
    r = int(clamp(base_rgb[0]*k, 0, 255))
    g = int(clamp(base_rgb[1]*k, 0, 255))
    b = int(clamp(base_rgb[2]*k, 0, 255))
    return (r,g,b)

def render_world(screen, cam, world, cx, cz):
    # Gather faces to draw
    faces_to_draw = []
    minx, maxx = int(cam.x - RENDER_RADIUS), int(cam.x + RENDER_RADIUS)
    miny, maxy = -2, 96
    minz, maxz = int(cam.z - RENDER_RADIUS), int(cam.z + RENDER_RADIUS)

    # Ensure terrain generated around camera
    world.populate_region(int(round(cam.x)), int(round(cam.z)), RENDER_RADIUS)

    for x in range(minx, maxx+1):
        for z in range(minz, maxz+1):
            # Cheap skip: if column empty assume generated lazily by populate_region
            # We still iterate to skip drawing empty columns quickly
            # Determine approximate surface to limit y scanning
            top_y = world.height_at(x, z)
            y_lo = max(miny, top_y - 20)
            y_hi = min(maxy, top_y + 8)
            for y in range(y_lo, y_hi):
                bid = world.get_block(x, y, z)
                if bid == 0: continue
                base_col = BLOCK_COLORS.get(bid, (200,200,200))

                # For each face, if neighbor is air, draw
                for idxs, nrm in FACES:
                    nx, ny, nz = nrm
                    if world.get_block(x+nx, y+ny, z+nz) != 0:
                        continue  # occluded
                    # Transform vertices
                    pts_cam = []
                    zsum = 0.0
                    skip = False
                    for vid in idxs:
                        vx, vy, vz = CUBE_VERTS[vid]
                        wx, wy, wz = x+vx, y+vy, z+vz
                        cxp, cyp, czp = cam.rotate_point(wx, wy, wz)
                        if czp <= NEAR_PLANE:
                            skip = True
                            break
                        zsum += czp
                        proj = cam.project(cxp, cyp, czp)
                        if proj is None:
                            skip = True
                            break
                        pts_cam.append(proj)
                    if skip or len(pts_cam) != 4:
                        continue
                    # Back-face culling in camera space:
                    # Two triangles; compute signed area to infer winding
                    ax, ay = pts_cam[0]
                    bx, by = pts_cam[1]
                    cxp2, cyp2 = pts_cam[2]
                    area = (bx-ax)*(cyp2-ay) - (by-ay)*(cxp2-ax)
                    if area >= 0:  # screen-space backface (assuming right-handed)
                        pass  # Allow; since we skipped occluded faces already

                    depth = zsum / 4.0
                    col = shade_color(base_col, nrm)
                    faces_to_draw.append((depth, pts_cam, col))

    # Depth sort far to near
    faces_to_draw.sort(key=lambda f: -f[0])

    # Draw
    for depth, pts, col in faces_to_draw:
        pygame.draw.polygon(screen, col, pts)

# ---------- Picking (3D DDA voxel traversal) ----------
def raycast_voxels(world, origin, direction, max_dist=BUILD_REACH):
    ox, oy, oz = origin
    dx, dy, dz = direction
    # Start voxel
    x, y, z = math.floor(ox), math.floor(oy), math.floor(oz)

    # Handle zero components
    def inv(v): return 1e30 if abs(v) < 1e-8 else 1.0/v

    stepX = 1 if dx > 0 else -1
    stepY = 1 if dy > 0 else -1
    stepZ = 1 if dz > 0 else -1

    tDeltaX = abs(inv(dx))
    tDeltaY = abs(inv(dy))
    tDeltaZ = abs(inv(dz))

    # Distance to the first voxel boundary
    def first_t(o, d, i, step):
        # Boundary at i if step<0 else i+1
        boundary = i + (1 if step > 0 else 0)
        return (boundary - o) / (d if abs(d) > 1e-8 else 1e-8)

    tMaxX = first_t(ox, dx, x, stepX)
    tMaxY = first_t(oy, dy, y, stepY)
    tMaxZ = first_t(oz, dz, z, stepZ)

    prev = (x, y, z)
    face = (0, 0, 0)
    t = 0.0
    while t <= max_dist:
        # Check block
        bid = world.get_block(x, y, z)
        if bid != 0:
            return (x, y, z, face, t)
        # Step
        if tMaxX < tMaxY:
            if tMaxX < tMaxZ:
                x += stepX
                t = tMaxX
                tMaxX += tDeltaX
                face = (-stepX, 0, 0)
            else:
                z += stepZ
                t = tMaxZ
                tMaxZ += tDeltaZ
                face = (0, 0, -stepZ)
        else:
            if tMaxY < tMaxZ:
                y += stepY
                t = tMaxY
                tMaxY += tDeltaY
                face = (0, -stepY, 0)
            else:
                z += stepZ
                t = tMaxZ
                tMaxZ += tDeltaZ
                face = (0, 0, -stepZ)
    return None

# ---------- Main loop ----------
def main():
    pygame.init()
    pygame.display.set_caption("Minimal Minecraft - Pygame")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    cam = Camera(pos=(0.0, 50.0, 0.0), yaw=45.0, pitch=-15.0)
    world = World(WORLD_SEED)

    vel = [0.0, 0.0, 0.0]
    on_ground = False
    selected_block = 1  # start with grass

    last_time = time.time()
    running = True
    while running:
        dt = clock.tick(FPS_CAP) / 1000.0
        dt = min(dt, 0.05)

        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    selected_block = (event.key - pygame.K_0)
                elif event.key == pygame.K_f:
                    # Toggle fly mode
                    global FLY_MODE
                    FLY_MODE = not FLY_MODE
                    vel[1] = 0.0
                elif event.key == pygame.K_r:
                    # Reset position to spawn
                    cam.x, cam.y, cam.z = 0.0, 60.0, 0.0
                    vel = [0.0, 0.0, 0.0]
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.rel
                cam.yaw = (cam.yaw + mx * MOUSE_SENS) % 360
                cam.pitch = clamp(cam.pitch - my * MOUSE_SENS, -89.5, 89.5)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Raycast from camera
                fwd = cam.dir_forward()
                hit = raycast_voxels(world, (cam.x, cam.y, cam.z), fwd, BUILD_REACH)
                if event.button == 1:  # break
                    if hit:
                        hx, hy, hz, face, dist = hit
                        world.set_block(hx, hy, hz, 0)
                elif event.button == 3:  # place
                    if hit:
                        hx, hy, hz, face, dist = hit
                        px, py, pz = hx + face[0], hy + face[1], hz + face[2]
                        # do not place inside camera position
                        if length(sub((px+0.5,py+0.5,pz+0.5),(cam.x,cam.y,cam.z))) > 1.0:
                            world.set_block(px, py, pz, selected_block)

        # Movement
        keys = pygame.key.get_pressed()
        ax = az = ay = 0.0
        speed = MOVE_SPEED
        if keys[pygame.K_LCTRL] or keys[pygame.K_c]:
            speed *= 1.8
        if keys[pygame.K_LSHIFT]:
            speed *= 0.7

        # Strafe directions based on yaw
        yaw_rad = math.radians(cam.yaw)
        siny, cosy = math.sin(yaw_rad), math.cos(yaw_rad)
        forward = (siny, 0.0, cosy)
        right = (cosy, 0.0, -siny)

        if keys[pygame.K_w]:
            ax += forward[0] * speed
            az += forward[2] * speed
        if keys[pygame.K_s]:
            ax -= forward[0] * speed
            az -= forward[2] * speed
        if keys[pygame.K_a]:
            ax -= right[0] * speed
            az -= right[2] * speed
        if keys[pygame.K_d]:
            ax += right[0] * speed
            az += right[2] * speed

        if FLY_MODE:
            if keys[pygame.K_SPACE]: ay += speed
            if keys[pygame.K_LSHIFT]: ay -= speed
            vel[0] = vel[0]*AIR_FRICTION + ax * dt
            vel[1] = vel[1]*AIR_FRICTION + ay * dt
            vel[2] = vel[2]*AIR_FRICTION + az * dt
            cam.x += vel[0]
            cam.y += vel[1]
            cam.z += vel[2]
        else:
            # Basic ground physics without collision against blocks for simplicity
            if keys[pygame.K_SPACE] and on_ground:
                vel[1] = JUMP_SPEED
                on_ground = False
            vel[0] = vel[0]*AIR_FRICTION + ax * dt
            vel[2] = vel[2]*AIR_FRICTION + az * dt
            vel[1] -= GRAVITY * dt
            cam.x += vel[0]
            cam.z += vel[2]
            cam.y += vel[1]
            terrain_y = world.height_at(int(round(cam.x)), int(round(cam.z))) + 1.0
            if cam.y < terrain_y:
                cam.y = terrain_y
                vel[1] = 0.0
                on_ground = True
            else:
                on_ground = False

        # Draw
        screen.fill((140, 190, 255))  # sky
        # Simple horizon ground fill far away
        pygame.draw.rect(screen, (90, 160, 90), (0, HEIGHT*0.55, WIDTH, HEIGHT*0.45))

        render_world(screen, cam, world, int(cam.x), int(cam.z))

        # Crosshair
        cx, cy = WIDTH//2, HEIGHT//2
        pygame.draw.line(screen, (0,0,0), (cx-8, cy), (cx+8, cy), 3)
        pygame.draw.line(screen, (0,0,0), (cx, cy-8), (cx, cy+8), 3)
        pygame.draw.line(screen, (255,255,255), (cx-8, cy), (cx+8, cy), 1)
        pygame.draw.line(screen, (255,255,255), (cx, cy-8), (cx, cy+8), 1)

        # HUD
        fps = int(clock.get_fps())
        font = pygame.font.SysFont(None, 18)
        text = font.render(f"FPS {fps}  Pos({cam.x:.1f},{cam.y:.1f},{cam.z:.1f})  Yaw {cam.yaw:.1f}  Pitch {cam.pitch:.1f}  Block [{selected_block}:{BLOCK_NAMES.get(selected_block,'?')}]", True, (0,0,0))
        screen.blit(text, (10, 10))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise
