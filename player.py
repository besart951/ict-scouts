from __future__ import annotations

import pygame

from asset_store import AssetStore
from settings import GRAVITY, GROUND_Y, JUMP_SPEED, PLAYER_HEIGHT, PLAYER_WIDTH, WALK_ANIMATION_SPEED


class Player:
    """The runner that can jump."""

    def __init__(self, x: int, assets: AssetStore) -> None:
        self.assets = assets
        self.position = pygame.Vector2(x, GROUND_Y - PLAYER_HEIGHT)
        self.velocity = pygame.Vector2()
        self.rect = pygame.Rect(
            round(self.position.x),
            round(self.position.y),
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
        )
        self.on_ground = True
        self.walk_frame = 0
        self.walk_timer = 0.0
        self.jump_was_pressed = False

    def update(self, dt: float, jump_pressed: bool) -> bool:
        jumped = False
        if jump_pressed and not self.jump_was_pressed and self.on_ground:
            self.velocity.y = JUMP_SPEED
            self.on_ground = False
            jumped = True

        self.jump_was_pressed = jump_pressed
        self._update_walk_animation(dt)

        self.velocity.y += GRAVITY * dt
        self.position.y += self.velocity.y * dt
        floor_y = GROUND_Y - PLAYER_HEIGHT

        if self.position.y >= floor_y:
            self.position.y = floor_y
            self.velocity.y = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

        self.rect.y = round(self.position.y)

        return jumped

    def draw(self, surface: pygame.Surface) -> None:
        sprite = self._current_sprite()
        draw_rect = sprite.get_rect(midbottom=(self.rect.centerx, self.rect.bottom + 6))
        surface.blit(sprite, draw_rect)

    def _current_sprite(self) -> pygame.Surface:
        if not self.on_ground:
            return self.assets.player_jump

        return self.assets.player_walk_frames[self.walk_frame]

    def _update_walk_animation(self, dt: float) -> None:
        self.walk_timer += dt
        if self.walk_timer < 1 / WALK_ANIMATION_SPEED:
            return

        self.walk_timer = 0.0
        self.walk_frame = (self.walk_frame + 1) % len(self.assets.player_walk_frames)
