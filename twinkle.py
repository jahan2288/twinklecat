import tkinter as tk
import threading
import random
import time

class TwinkleCat:
    def __init__(self, root):
        self.root = root
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg='skyblue')

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(self.root, width=self.screen_width, height=self.screen_height, bg='skyblue', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # State flags
        self.running = True
        self.blinking = True
        self.tail_direction = 1
        self.tail_angle = 0
        self.cat_moving = False
        self.sleeping = False
        self.night_mode = False
        self.follow_mouse = False
        self.leg_position = 0  # Toggle leg positions

        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height - 250

        self.draw_background()
        self.add_buttons()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.draw_cat()

        threading.Thread(target=self.animate_blinking, daemon=True).start()
        threading.Thread(target=self.animate_tail, daemon=True).start()
        threading.Thread(target=self.move_cat, daemon=True).start()

    def add_buttons(self):
        self.run_btn = tk.Button(self.root, text="Run", command=self.start_moving, bg='green', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(70, 30, window=self.run_btn)

        self.stop_btn = tk.Button(self.root, text="Stop", command=self.stop_moving, bg='orange', fg='black', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(160, 30, window=self.stop_btn)

        self.blink_btn = tk.Button(self.root, text="Stop Blinking", command=self.toggle_blinking, bg='purple', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(280, 30, window=self.blink_btn)

        self.sleep_btn = tk.Button(self.root, text="Sleep Mode", command=self.toggle_sleep, bg='blue', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(410, 30, window=self.sleep_btn)

        self.bg_btn = tk.Button(self.root, text="Switch to Night", command=self.toggle_background, bg='black', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(550, 30, window=self.bg_btn)

        self.follow_btn = tk.Button(self.root, text="Follow Mouse", command=self.toggle_follow_mouse, bg='teal', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(700, 30, window=self.follow_btn)

        self.puzzle_btn = tk.Button(self.root, text="Puzzle Game", command=self.show_puzzle, bg='darkorange', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(850, 30, window=self.puzzle_btn)

        self.close_btn = tk.Button(self.root, text="✕", command=self.close, bg='red', fg='white', font=('Arial', 12, 'bold'), relief='flat')
        self.canvas.create_window(self.screen_width - 30, 30, window=self.close_btn)

    def draw_background(self):
        self.canvas.delete("bg")
        color = 'midnightblue' if self.night_mode else 'skyblue'
        grass_color = '#003300' if self.night_mode else 'lightgreen'
        road_color = '#222' if self.night_mode else 'gray'
        stripe_color = 'lightyellow' if self.night_mode else 'white'

        self.canvas.configure(bg=color)
        self.canvas.create_rectangle(0, self.screen_height - 300, self.screen_width, self.screen_height, fill=grass_color, outline='', tags='bg')
        self.canvas.create_rectangle(0, self.screen_height - 180, self.screen_width, self.screen_height - 80, fill=road_color, outline='', tags='bg')
        for x in range(0, self.screen_width, 80):
            self.canvas.create_rectangle(x, self.screen_height - 130, x + 40, self.screen_height - 120, fill=stripe_color, outline='', tags='bg')

    def draw_cat(self):
        self.canvas.delete("cat")

        if self.sleeping:
            self.canvas.create_oval(self.center_x - 100, self.center_y, self.center_x + 100, self.center_y + 140,
                                    fill='orange', outline='black', tags="cat")
            self.canvas.create_text(self.center_x, self.center_y - 50, text="💤", font=("Arial", 30), tags="cat")
            return

        self.canvas.create_oval(self.center_x - 100, self.center_y, self.center_x + 100, self.center_y + 180,
                                fill='orange', outline='black', tags="cat")
        self.canvas.create_oval(self.center_x - 120, self.center_y - 200, self.center_x + 120, self.center_y,
                                fill='orange', outline='black', tags="cat")

        self.canvas.create_polygon(self.center_x - 120, self.center_y - 160, self.center_x - 80, self.center_y - 300,
                                   self.center_x - 40, self.center_y - 160, fill='orange', outline='black', tags="cat")
        self.canvas.create_polygon(self.center_x + 40, self.center_y - 160, self.center_x + 80, self.center_y - 300,
                                   self.center_x + 120, self.center_y - 160, fill='orange', outline='black', tags="cat")

        self.eye1 = self.canvas.create_oval(self.center_x - 40, self.center_y - 130, self.center_x - 10, self.center_y - 90,
                                            fill='black', tags="cat")
        self.eye2 = self.canvas.create_oval(self.center_x + 10, self.center_y - 130, self.center_x + 40, self.center_y - 90,
                                            fill='black', tags="cat")

        self.mouth = self.canvas.create_arc(self.center_x - 20, self.center_y - 60, self.center_x + 20, self.center_y - 20,
                                            start=0, extent=-180, style='arc', tags="cat")

        for offset in [-15, 0, 15]:
            self.canvas.create_line(self.center_x - 80, self.center_y - 90 + offset,
                                    self.center_x - 40, self.center_y - 90 + offset, tags="cat")
            self.canvas.create_line(self.center_x + 40, self.center_y - 90 + offset,
                                    self.center_x + 80, self.center_y - 90 + offset, tags="cat")

        paw_offset = 20 if self.leg_position else 0
        self.canvas.create_oval(self.center_x - 60, self.center_y + 160 + paw_offset, self.center_x - 20, self.center_y + 200 + paw_offset,
                                fill='orange', outline='black', tags="cat")
        self.canvas.create_oval(self.center_x + 20, self.center_y + 160 - paw_offset, self.center_x + 60, self.center_y + 200 - paw_offset,
                                fill='orange', outline='black', tags="cat")

        self.canvas.create_line(self.center_x + 90, self.center_y + 50,
                                self.center_x + 140 + self.tail_angle, self.center_y + 40,
                                self.center_x + 180 + self.tail_angle, self.center_y + 80,
                                smooth=True, width=10, fill='orange', tags="cat")

    def animate_blinking(self):
        while self.running:
            if self.blinking and not self.sleeping:
                self.canvas.itemconfig(self.eye1, fill='lightblue')
                self.canvas.itemconfig(self.eye2, fill='lightblue')
                time.sleep(0.2)
                self.canvas.itemconfig(self.eye1, fill='black')
                self.canvas.itemconfig(self.eye2, fill='black')
            time.sleep(4)

    def animate_tail(self):
        while self.running:
            if not self.sleeping:
                self.tail_angle += self.tail_direction * 3
                if abs(self.tail_angle) > 20:
                    self.tail_direction *= -1
                self.draw_cat()
            time.sleep(0.2)

    def move_cat(self):
        while self.running:
            if self.cat_moving and not self.sleeping:
                dx = random.choice([-30, 0, 30])
                new_x = self.center_x + dx
                if 150 < new_x < self.screen_width - 150:
                    self.center_x = new_x
                self.leg_position ^= 1
                self.draw_cat()
                time.sleep(0.3)

            elif self.follow_mouse and not self.sleeping:
                x, y = self.canvas.winfo_pointerxy()
                self.center_x += (x - self.center_x) // 10
                self.center_y += (y - self.center_y) // 10
                self.leg_position ^= 1
                self.draw_cat()
                time.sleep(0.1)

            elif not self.follow_mouse and hasattr(self, 'original_x') and not self.sleeping:
                if abs(self.center_x - self.original_x) > 5 or abs(self.center_y - self.original_y) > 5:
                    self.center_x += (self.original_x - self.center_x) // 10
                    self.center_y += (self.original_y - self.center_y) // 10
                    self.leg_position ^= 1
                    self.draw_cat()
                    time.sleep(0.1)
                else:
                    time.sleep(0.3)
            else:
                time.sleep(0.3)

    def on_mouse_move(self, event):
        if self.follow_mouse:
            self.mouse_x, self.mouse_y = event.x, event.y

    def on_click(self, event):
        if not self.sleeping:
            self.canvas.itemconfig(self.mouth, extent=180)
            self.root.after(1000, lambda: self.canvas.itemconfig(self.mouth, extent=-180))

    def start_moving(self):
        self.cat_moving = True

    def stop_moving(self):
        self.cat_moving = False

    def toggle_blinking(self):
        self.blinking = not self.blinking
        self.blink_btn.config(text="Start Blinking" if not self.blinking else "Stop Blinking")

    def toggle_sleep(self):
        self.sleeping = not self.sleeping
        self.sleep_btn.config(text="Wake Up" if self.sleeping else "Sleep Mode")
        self.draw_cat()

    def toggle_background(self):
        self.night_mode = not self.night_mode
        self.bg_btn.config(text="Switch to Day" if self.night_mode else "Switch to Night")
        self.draw_background()

    def toggle_follow_mouse(self):
        self.follow_mouse = not self.follow_mouse
        self.follow_btn.config(text="Stop Follow" if self.follow_mouse else "Follow Mouse")
        if self.follow_mouse:
            self.original_x = self.center_x
            self.original_y = self.center_y

    def show_puzzle(self):
        puzzle_window = tk.Toplevel(self.root)
        puzzle_window.title("Sliding Puzzle")
        puzzle_window.geometry("300x350")
        puzzle_window.resizable(False, False)

        frame = tk.Frame(puzzle_window)
        frame.pack(pady=10)

        self.tiles = list(range(1, 9)) + [None]
        random.shuffle(self.tiles)

        def draw_tiles():
            for widget in frame.winfo_children():
                widget.destroy()
            for i, val in enumerate(self.tiles):
                btn = tk.Button(frame, text=str(val) if val else "", font=('Arial', 20), width=4, height=2,
                                state='normal' if val else 'disabled')
                btn.grid(row=i//3, column=i%3)
                btn.config(command=lambda i=i: move_tile(i))

        def move_tile(index):
            empty_index = self.tiles.index(None)
            neighbors = [index - 1, index + 1, index - 3, index + 3]
            if empty_index in neighbors and (
                (abs(index - empty_index) == 1 and index // 3 == empty_index // 3) or abs(index - empty_index) == 3):
                self.tiles[empty_index], self.tiles[index] = self.tiles[index], None
                draw_tiles()
                if self.tiles == list(range(1, 9)) + [None]:
                    tk.Label(puzzle_window, text="🎉 You Win!", font=("Arial", 16, "bold"), fg='green').pack(pady=10)

        draw_tiles()

    def close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TwinkleCat(root)
    root.mainloop()
