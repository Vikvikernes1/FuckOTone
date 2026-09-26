"""Small cross-platform Tkinter clicker.

Run with: python main.py
"""

from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageDraw, ImageSequence, ImageTk


ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
WORLD_PATH = ROOT / "world.png"
FUCK_PATH = ROOT / "fuck.gif"
FURRY_PATH = ROOT / "furry.png"


class ClickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Вопрос жизни")
        self.geometry("980x700")
        self.minsize(700, 500)
        self.configure(bg="#11131c")
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.world = Image.open(WORLD_PATH).convert("RGBA")
        self.fuck_frames = self.load_gif_frames()
        self.furry = Image.open(FURRY_PATH).convert("RGBA")
        self.animation_id = None
        self.fuck_frame_index = 0
        self.current_photo = None
        self.show_menu()

    def clear(self):
        if self.animation_id is not None:
            self.after_cancel(self.animation_id)
            self.animation_id = None
        for child in self.winfo_children():
            child.destroy()

    @staticmethod
    def load_gif_frames():
        frames = []
        with Image.open(FUCK_PATH) as gif:
            for frame in ImageSequence.Iterator(gif):
                duration = frame.info.get("duration", 50)
                frames.append((frame.convert("RGBA"), max(20, duration)))
        return frames

    def show_menu(self):
        self.clear()
        wrapper = tk.Frame(self, bg="#11131c")
        wrapper.pack(expand=True, fill="both", padx=30, pady=30)

        tk.Label(
            wrapper,
            text="В каком институте учился?",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#11131c",
        ).pack(pady=(80, 45))

        buttons = tk.Frame(wrapper, bg="#11131c")
        buttons.pack()
        self.make_button(buttons, "МИЭТ", self.show_miet, "#c33c54").pack(
            side="left", padx=12
        )
        self.make_button(
            buttons, "ЛЮБОЙ ДРУГОЙ", self.show_world, "#3478d4"
        ).pack(side="left", padx=12)

        tk.Label(
            wrapper,
            text="Выбери вариант",
            font=("Arial", 12),
            fg="#8d93a8",
            bg="#11131c",
        ).pack(pady=35)

    @staticmethod
    def make_button(parent, text, command, color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 15, "bold"),
            fg="white",
            bg=color,
            activebackground="#ffffff",
            activeforeground="#11131c",
            relief="flat",
            cursor="hand2",
            padx=24,
            pady=15,
            bd=0,
        )

    def make_view(self):
        self.clear()
        self.canvas = tk.Canvas(self, bg="#08090d", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both")
        bottom = tk.Frame(self, bg="#11131c")
        bottom.pack(fill="x")
        self.make_button(bottom, "← В меню", self.show_menu, "#303747").pack(
            pady=10
        )

    @staticmethod
    def fit(image, width, height):
        ratio = min(width / image.width, height / image.height)
        size = (max(1, int(image.width * ratio)), max(1, int(image.height * ratio)))
        return image.resize(size, Image.Resampling.LANCZOS)

    def show_world(self):
        self.make_view()
        self.bind("<Configure>", self.redraw)
        self.redraw()

    def redraw(self, _event=None):
        if not hasattr(self, "canvas"):
            return
        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        if width < 10 or height < 10:
            return
        image = self.fit(self.world, width, height)
        canvas_image = Image.new("RGBA", (width, height), "#08090d")
        canvas_image.alpha_composite(image, ((width - image.width) // 2, (height - image.height) // 2))
        self.current_photo = ImageTk.PhotoImage(canvas_image)
        self.canvas.delete("all")
        self.canvas.create_image(width // 2, height // 2, image=self.current_photo)

    def show_miet(self):
        self.make_view()
        self.bind("<Configure>", self.render_miet)
        self.fuck_frame_index = 0
        self.play_miet_frame()

    def render_miet(self, _event=None):
        if not hasattr(self, "canvas"):
            return
        width = max(1, self.canvas.winfo_width())
        height = max(1, self.canvas.winfo_height())
        if width < 10 or height < 10:
            return

        base = self.fit(self.fuck_frames[self.fuck_frame_index][0], width, height)
        scene = Image.new("RGBA", (width, height), "#08090d")
        base_x = (width - base.width) // 2
        base_y = (height - base.height) // 2
        scene.alpha_composite(base, (base_x, base_y))

        # Replace the original face with the supplied furry reference.
        face = self.furry.crop((55, 120, 810, 850))
        face_size = int(min(width, height) * 0.265)
        face = face.resize((face_size, face_size), Image.Resampling.LANCZOS)
        mask = Image.new("L", face.size, 0)
        ImageDraw.Draw(mask).ellipse((2, 2, face.width - 2, face.height - 2), fill=255)
        face.putalpha(mask)
        face_x = width // 2 - face.width // 2
        face_y = height // 2 - int(face.height * 0.73)
        scene.alpha_composite(face, (face_x, face_y))

        self.current_photo = ImageTk.PhotoImage(scene)
        self.canvas.delete("all")
        self.canvas.create_image(width // 2, height // 2, image=self.current_photo)

    def play_miet_frame(self):
        if not hasattr(self, "canvas") or not self.winfo_exists():
            return
        self.render_miet()
        _, duration = self.fuck_frames[self.fuck_frame_index]
        self.fuck_frame_index = (self.fuck_frame_index + 1) % len(self.fuck_frames)
        self.animation_id = self.after(duration, self.play_miet_frame)


if __name__ == "__main__":
    try:
        ClickerApp().mainloop()
    except FileNotFoundError as error:
        messagebox.showerror("Не найден файл", str(error))
