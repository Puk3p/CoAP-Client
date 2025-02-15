import os
import tkinter as tk
import pygame
from PIL import Image, ImageTk


class DinoAnimation:
    def __init__(self, canvas, assets_path, x, y, scale=2, fps=10):  # Scale ajustabil
        self.canvas = canvas
        self.assets_path = assets_path
        self.x = x
        self.y = y
        self.scale = scale
        self.fps = fps

        pygame.init()
        pygame.display.set_mode((1, 1))

        sprite_sheet_path = os.path.join(self.assets_path, "redDino.png")
        if not os.path.exists(sprite_sheet_path):
            raise FileNotFoundError(f"Fișierul sprite sheet nu există: {sprite_sheet_path}")
        self.sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()

        self.frames = [self.get_sprite(i, 24, 24, self.scale) for i in range(24) if i != 16]

    def get_sprite(self, frame, width, height, scale):
        sprite = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        sprite.blit(self.sprite_sheet_image, (0, 0), (frame * width, 0, width, height))
        sprite = pygame.transform.scale(sprite, (width * scale, height * scale))
        return sprite

    def start_animation(self):
        self.current_frame = 0
        self.update_animation()

    def update_animation(self):
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)

        frame_image = pygame.image.tostring(frame, "RGBA")
        width, height = frame.get_size()
        pil_image = Image.frombytes("RGBA", (width, height), frame_image)

        pil_image = pil_image.convert("RGBA")
        data = pil_image.getdata()
        new_data = [
            (r, g, b, 0) if (r > 240 and g > 240 and b > 240) else (r, g, b, a)
            for (r, g, b, a) in data
        ]
        pil_image.putdata(new_data)

        photo_image = ImageTk.PhotoImage(pil_image)

        self.canvas.delete("all")
        self.canvas.create_image(self.x, self.y, image=photo_image, anchor="nw")
        self.canvas.image = photo_image

        self.canvas.after(int(1000 / self.fps), self.update_animation)
