from __future__ import annotations

import pygame


class Obstacle:
    """A thing the player should jump over."""

    def __init__(self, x: int, y: int, image: pygame.Surface, speed: float) -> None:
        self.image = image
        self.speed = speed
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.passed_player = False

    def update(self, dt: float) -> None:
        self.rect.x -= int(self.speed * dt)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def is_off_screen(self) -> bool:
        return self.rect.right < 0
