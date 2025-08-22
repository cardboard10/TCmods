# tinker_town_pygame.py — Minimal city-builder with Pygame + stdlib only
# Run: python tinker_town_pygame.py
# Requires: pip install pygame

import sys
import json
import pygame

# -----------------------------
# Config
# -----------------------------
GRID_W = 20
GRID_H = 15
CELL = 32
SIDEBAR_W = 260
PADDING = 8
WINDOW_W = GRID_W * CELL + SIDEBAR_W + PADDING * 2
WINDOW_H = GRID_H * CELL + PADDING * 2
FPS = 60
TICK_MS = 1000  # economy tick (1s)

TOOLS = ["Road", "House", "Factory", "Park", "Bulldoze"]

COLORS = {
    "BG": (18, 18, 18),
    "GRID": (40, 40, 40),
    "Road": (120, 120, 120),
    "House": (76, 175, 80),
    "Factory": (191, 54, 12),
    "Park": (46, 125, 50),
    "Empty": (31, 31, 31),
    "Text": (230, 230, 230),
    "Dim": (170, 170, 170),
    "Accent": (255, 213, 79),
    "Bad": (229, 57, 53),
    "Good": (102, 187, 106),
    "Panel": (26, 26, 26),
    "Button": (36, 36, 36),
    "ButtonHover": (48, 48, 48),
    "ButtonActive": (60, 60, 60),
    "Outline": (80, 80, 80),
}

COST = {
    "Road": 10,
    "House": 100,
    "Factory": 300,
    "Park": 80,
    "Bulldoze": 0,
}

INCOME = {
    "Factory": 5,
    "Park": -1,
    # House handled conditionally (+2 if touching road)
}

SAVE_FILE = "tinker_save.json"


# -----------------------------
# Utilities
# -----------------------------
def clamp(v, a, b):
    return max(a, min(b, v))


def touches_road(world, x, y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
            if world[ny][nx] == "Road":
                return True
    return False


# -----------------------------
# Game
# -----------------------------
class TinkerTown:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Tinker Town (Pygame)")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 22)
        self.font_big = pygame.font.SysFont(None, 28)

        self.world = [["Empty" for _ in range(GRID_W)] for _ in range(GRID_H)]
        self.money = 500
        self.day = 0
        self.current_tool = "Road"

        # Sidebar tool button rects
        self.tool_rects = {}
        self._layout_sidebar()

        # Economy tick event
        self.TICK_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TICK_EVENT, TICK_MS)

        # Flash effects: list of (x, y, until_ms, color)
        self.flashes = []

        # Income pulse feedback
        self.pulse_until = 0
        self.pulse_color = COLORS["Text"]

        # Pre-render grid lines
        self.grid_surface = self._make_grid_surface()

    def _make_grid_surface(self):
        surf = pygame.Surface((GRID_W * CELL, GRID_H * CELL), pygame.SRCALPHA)
        for x in range(GRID_W + 1):
            xx = x * CELL
            pygame.draw.line(surf, COLORS["GRID"], (xx, 0), (xx, GRID_H * CELL))
        for y in range(GRID_H + 1):
            yy = y * CELL
            pygame.draw.line(surf, COLORS["GRID"], (0, yy), (GRID_W * CELL, yy))
        return surf

    def _layout_sidebar(self):
        x0 = PADDING + GRID_W * CELL + PADDING
        y0 = PADDING
        panel = pygame.Rect(x0, y0, SIDEBAR_W, GRID_H * CELL)
        self.sidebar_rect = panel

        # Tool buttons stacked
        btn_w = SIDEBAR_W - 2 * 12
        btn_h = 34
        y = y0 + 120
        self.tool_rects.clear()
        for idx, tool in enumerate(TOOLS):
            rect = pygame.Rect(x0 + 12, y, btn_w, btn_h)
            self.tool_rects[tool] = rect
            y += btn_h + 8

    def save(self):
        data = {
            "world": self.world,
            "money": self.money,
            "day": self.day,
            "tool": self.current_tool,
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)

    def load(self):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            w = data.get("world")
            if isinstance(w, list) and len(w) == GRID_H and len(w[0]) == GRID_W:
                self.world = w
            self.money = int(data.get("money", self.money))
            self.day = int(data.get("day", self.day))
            tool = data.get("tool", self.current_tool)
            if tool in TOOLS:
                self.current_tool = tool
        except Exception:
            pass  # ignore malformed files

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            now = pygame.time.get_ticks()
            self.handle_events(now)
            self.update(now, dt)
            self.draw(now)

    def handle_events(self, now):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                elif event.key == pygame.K_1:
                    self.current_tool = TOOLS[0]
                elif event.key == pygame.K_2:
                    self.current_tool = TOOLS[1]
                elif event.key == pygame.K_3:
                    self.current_tool = TOOLS[2]
                elif event.key == pygame.K_4:
                    self.current_tool = TOOLS[3]
                elif event.key == pygame.K_5:
                    self.current_tool = TOOLS[4]
                elif event.key == pygame.K_s:
                    self.save()
                elif event.key == pygame.K_l:
                    self.load()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Sidebar clicks
                for tool, rect in self.tool_rects.items():
                    if rect.collidepoint(mx, my):
                        self.current_tool = tool
                        break
                else:
                    # Grid click
                    gx, gy = self.screen_to_grid(mx, my)
                    if 0 <= gx < GRID_W and 0 <= gy < GRID_H:
                        self.place_tile(gx, gy)

            if event.type == self.TICK_EVENT:
                self.economy_tick(now)

    def screen_to_grid(self, mx, my):
        gx = (mx - PADDING) // CELL
        gy = (my - PADDING) // CELL
        return int(gx), int(gy)

    def place_tile(self, x, y):
        tool = self.current_tool
        if tool == "Bulldoze":
            if self.world[y][x] != "Empty":
                self.world[y][x] = "Empty"
            return

        if self.world[y][x] == tool:
            return

        cost = COST[tool]
        if self.money < cost:
            self.flash_cell(x, y, COLORS["Bad"], duration=180)
            return

        self.money -= cost
        self.world[y][x] = tool

    def flash_cell(self, x, y, color, duration=150):
        until = pygame.time.get_ticks() + duration
        self.flashes.append((x, y, until, color))

    def economy_tick(self, now):
        income = 0
        for y in range(GRID_H):
            for x in range(GRID_W):
                t = self.world[y][x]
                if t == "House":
                    if touches_road(self.world, x, y):
                        income += 2
                elif t == "Factory":
                    income += INCOME["Factory"]
                elif t == "Park":
                    income += INCOME["Park"]

        self.money += income
        self.day += 1

        if income != 0:
            self.pulse_color = COLORS["Good"] if income > 0 else COLORS["Bad"]
            self.pulse_until = now + 160

    def update(self, now, dt):
        # Clear expired flashes
        self.flashes = [f for f in self.flashes if f[2] > now]

    def draw(self, now):
        self.screen.fill(COLORS["BG"])

        # Grid area
        grid_x = PADDING
        grid_y = PADDING
        grid_w = GRID_W * CELL
        grid_h = GRID_H * CELL
        grid_rect = pygame.Rect(grid_x, grid_y, grid_w, grid_h)

        # Grid background
        pygame.draw.rect(self.screen, COLORS["Empty"], grid_rect)

        # Tiles
        for y in range(GRID_H):
            for x in range(GRID_W):
                t = self.world[y][x]
                if t != "Empty":
                    self.draw_tile(grid_x, grid_y, x, y, t)

        # Flashes
        for x, y, until, color in self.flashes:
            x0 = grid_x + x * CELL
            y0 = grid_y + y * CELL
            pygame.draw.rect(self.screen, color, (x0, y0, CELL, CELL), width=3, border_radius=4)

        # Grid lines overlay
        self.screen.blit(self.grid_surface, (grid_x, grid_y))

        # Sidebar
        self.draw_sidebar(now)

        # Top HUD
        self.draw_hud(now)

        pygame.display.flip()

    def draw_tile(self, gx, gy, x, y, t):
        x0 = gx + x * CELL
        y0 = gy + y * CELL
        rect = pygame.Rect(x0 + 1, y0 + 1, CELL - 2, CELL - 2)
        color = COLORS[t]
        pygame.draw.rect(self.screen, color, rect, border_radius=5)

        label = {"House": "H", "Factory": "F", "Park": "P"}.get(t, "")
        if label:
            txt = self.font.render(label, True, (255, 255, 255))
            tr = txt.get_rect(center=rect.center)
            self.screen.blit(txt, tr)

        if t == "Road":
            # simple road line
            pygame.draw.line(self.screen, (180, 180, 180), (rect.left + 6, rect.centery), (rect.right - 6, rect.centery), 4)
            pygame.draw.line(self.screen, (160, 160, 160), (rect.centerx, rect.top + 6), (rect.centerx, rect.bottom - 6), 4)

    def draw_sidebar(self, now):
        pygame.draw.rect(self.screen, COLORS["Panel"], self.sidebar_rect, border_radius=8)
        x0, y0, w, h = self.sidebar_rect
        # Title
        title = self.font_big.render("Tools", True, COLORS["Text"])
        self.screen.blit(title, (x0 + 12, y0 + 12))

        rules_title = self.font.render("Rules", True, COLORS["Dim"])
        self.screen.blit(rules_title, (x0 + 12, y0 + 52))
        rules_lines = [
            "• House: +2 if next to a road",
            "• Factory: +5",
            "• Park: -1 upkeep",
            "• Bulldoze is free",
        ]
        yy = y0 + 72
        for line in rules_lines:
            txt = self.font.render(line, True, COLORS["Dim"])
            self.screen.blit(txt, (x0 + 12, yy))
            yy += 18

        # Buttons
        mx, my = pygame.mouse.get_pos()
        for tool in TOOLS:
            rect = self.tool_rects[tool]
            hovered = rect.collidepoint(mx, my)
            active = tool == self.current_tool
            base = COLORS["ButtonActive"] if active else (COLORS["ButtonHover"] if hovered else COLORS["Button"])
            pygame.draw.rect(self.screen, base, rect, border_radius=6)
            pygame.draw.rect(self.screen, COLORS["Outline"], rect, width=1, border_radius=6)

            label = f"{tool}   ${COST[tool]}" if tool != "Bulldoze" else "Bulldoze"
            txt = self.font.render(label, True, COLORS["Text"])
            self.screen.blit(txt, (rect.x + 10, rect.y + 8))

    def draw_hud(self, now):
        # Money / Day header
        top_bar = pygame.Rect(PADDING, WINDOW_H - PADDING - 28, GRID_W * CELL, 28)
        pygame.draw.rect(self.screen, COLORS["Panel"], top_bar, border_radius=6)

        money_color = COLORS["Bad"] if self.money < 0 else COLORS["Text"]
        money_txt = self.font_big.render(f"Money: ${self.money}", True, money_color)
        day_color = COLORS["Text"]
        if now < self.pulse_until:
            day_color = self.pulse_color
        day_txt = self.font_big.render(f"Day: {self.day}", True, day_color)

        self.screen.blit(money_txt, (top_bar.x + 10, top_bar.y + 4))
        self.screen.blit(day_txt, (top_bar.right - day_txt.get_width() - 10, top_bar.y + 4))


if __name__ == "__main__":
    TinkerTown().run()
