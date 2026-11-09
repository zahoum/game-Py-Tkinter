"""A small, gentle Tkinter game about finding little moments of light."""

import random
import tkinter as tk


WIDTH = 800
HEIGHT = 600
GOAL = 8
PLAYER_SPEED = 5

SKY_COLORS = ("#25334f", "#304663", "#46677c", "#70968d", "#d0a978")


class LittleLightGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("A Little Light")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(
            root, width=WIDTH, height=HEIGHT, bg=SKY_COLORS[0], highlightthickness=0
        )
        self.canvas.pack()

        self.keys: set[str] = set()
        self.lights: list[tuple[float, float]] = []
        self.collected = 0
        self.player_x = WIDTH / 2
        self.player_y = HEIGHT - 125
        self.playing = False
        self.finished = False
        self.after_id: str | None = None

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.canvas.bind("<Button-1>", self.on_click)
        self.draw_title_screen()

    def draw_landscape(self, progress: int = 0) -> None:
        color_index = min(progress // 2, len(SKY_COLORS) - 1)
        self.canvas.configure(bg=SKY_COLORS[color_index])

        # A few quiet stars remain in the sky as it brightens.
        star_random = random.Random(12)
        for _ in range(32):
            x = star_random.randint(18, WIDTH - 18)
            y = star_random.randint(24, 330)
            size = star_random.choice((1, 2, 3))
            self.canvas.create_oval(
                x - size, y - size, x + size, y + size,
                fill="#f3e8c8", outline="",
            )
        self.canvas.create_oval(-100, 400, 390, 740, fill="#293d4b", outline="")
        self.canvas.create_oval(280, 420, 900, 760, fill="#344b53", outline="")
        self.canvas.create_oval(510, 450, 900, 720, fill="#405858", outline="")

    def draw_title_screen(self) -> None:
        self.canvas.delete("all")
        self.draw_landscape()
        self.canvas.create_text(
            WIDTH / 2, 135, text="A Little Light",
            fill="#fff3d4", font=("Segoe UI", 38, "bold"),
        )
        self.canvas.create_text(
            WIDTH / 2, 198, text="A gentle game for cloudy days",
            fill="#e1e4dc", font=("Segoe UI", 16),
        )
        self.canvas.create_text(
            WIDTH / 2, 285,
            text="Gather little lights and watch the world grow warmer.\n"
            "There is no rush. Just take one small step at a time.",
            fill="#f1eee3", font=("Segoe UI", 14), justify="center",
        )
        self.draw_button("START A NEW WALK", WIDTH / 2, 390)
        self.canvas.create_text(
            WIDTH / 2, 470, text="Move with the arrow keys or WASD",
            fill="#d2dacf", font=("Segoe UI", 12),
        )
        self.canvas.create_text(
            WIDTH / 2, 530, text="You don't have to feel sunny to keep going.",
            fill="#e4d7bd", font=("Segoe UI", 12, "italic"),
        )

    def draw_button(self, label: str, x: float, y: float) -> None:
        self.canvas.create_rectangle(
            x - 125, y - 25, x + 125, y + 25,
            fill="#e5bd75", outline="#f8dfaa", width=2, tags="start_button",
        )
        self.canvas.create_text(
            x, y, text=label, fill="#273447", font=("Segoe UI", 12, "bold"),
            tags="start_button",
        )

    def start_game(self) -> None:
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.keys.clear()
        self.collected = 0
        self.player_x = WIDTH / 2
        self.player_y = HEIGHT - 125
        self.lights = [self.random_light() for _ in range(GOAL)]
        self.playing = True
        self.finished = False
        self.draw_game()
        self.tick()

    def random_light(self) -> tuple[float, float]:
        return (
            random.randint(45, WIDTH - 45),
            random.randint(100, HEIGHT - 190),
        )

    def draw_player(self) -> None:
        x, y = self.player_x, self.player_y
        self.canvas.create_oval(
            x - 25, y - 25, x + 25, y + 25,
            fill="#f4c96b", outline="#fff0b5", width=3,
        )
        self.canvas.create_oval(x - 9, y - 5, x - 5, y - 1, fill="#51443a", outline="")
        self.canvas.create_oval(x + 5, y - 5, x + 9, y - 1, fill="#51443a", outline="")
        self.canvas.create_arc(
            x - 8, y - 4, x + 8, y + 10, start=205, extent=130,
            style=tk.ARC, outline="#51443a", width=2,
        )

    def draw_game(self) -> None:
        self.canvas.delete("all")
        self.draw_landscape(self.collected)
        self.canvas.create_text(
            28, 27, anchor="w", text="LITTLE LIGHTS",
            fill="#fff2d6", font=("Segoe UI", 12, "bold"),
        )
        self.canvas.create_text(
            WIDTH - 28, 27, anchor="e",
            text=f"{self.collected} / {GOAL}",
            fill="#fff2d6", font=("Segoe UI", 12, "bold"),
        )
        self.canvas.create_rectangle(
            28, 48, 148, 57, fill="#41536a", outline="",
        )
        if self.collected:
            self.canvas.create_rectangle(
                28, 48, 28 + 120 * self.collected / GOAL, 57,
                fill="#f4c96b", outline="",
            )
        for x, y in self.lights:
            self.canvas.create_oval(
                x - 18, y - 18, x + 18, y + 18,
                fill="#f6d884", outline="#fff1bc", width=2,
            )
            self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5, fill="#fff8d7", outline="",
            )
        self.draw_player()
        self.canvas.create_text(
            WIDTH / 2, HEIGHT - 25, text="A small step is still a step.",
            fill="#e7dfc9", font=("Segoe UI", 12, "italic"),
        )

    def tick(self) -> None:
        if not self.playing:
            return

        dx = int("right" in self.keys or "d" in self.keys) - int(
            "left" in self.keys or "a" in self.keys
        )
        dy = int("down" in self.keys or "s" in self.keys) - int(
            "up" in self.keys or "w" in self.keys
        )
        # Keep diagonal movement at the same speed as horizontal movement.
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        self.player_x = min(WIDTH - 30, max(30, self.player_x + dx * PLAYER_SPEED))
        self.player_y = min(HEIGHT - 70, max(85, self.player_y + dy * PLAYER_SPEED))

        remaining: list[tuple[float, float]] = []
        for x, y in self.lights:
            if (self.player_x - x) ** 2 + (self.player_y - y) ** 2 < 38**2:
                self.collected += 1
            else:
                remaining.append((x, y))
        self.lights = remaining
        self.draw_game()

        if self.collected >= GOAL:
            self.playing = False
            self.finished = True
            self.draw_finish_screen()
            return
        self.after_id = self.root.after(30, self.tick)

    def draw_finish_screen(self) -> None:
        self.canvas.create_rectangle(
            115, 175, WIDTH - 115, 425,
            fill="#25334f", outline="#f2d18a", width=3,
        )
        self.canvas.create_text(
            WIDTH / 2, 230, text="You found your little lights.",
            fill="#fff0c8", font=("Segoe UI", 23, "bold"),
        )
        self.canvas.create_text(
            WIDTH / 2, 290,
            text="The sky can be cloudy and still hold stars.\n"
            "Thank you for taking this walk.",
            fill="#e5e7df", font=("Segoe UI", 14), justify="center",
        )
        self.draw_button("TAKE ANOTHER WALK", WIDTH / 2, 365)

    def on_key_press(self, event: tk.Event) -> None:
        key = event.keysym.lower()
        if key in {"left", "right", "up", "down", "w", "a", "s", "d"}:
            self.keys.add(key)
        elif key in {"return", "space"} and not self.playing:
            self.start_game()

    def on_key_release(self, event: tk.Event) -> None:
        self.keys.discard(event.keysym.lower())

    def on_click(self, event: tk.Event) -> None:
        if not self.playing and WIDTH / 2 - 130 <= event.x <= WIDTH / 2 + 130:
            if 350 <= event.y <= 420 or (self.finished and 330 <= event.y <= 400):
                self.start_game()


def main() -> None:
    root = tk.Tk()
    LittleLightGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()