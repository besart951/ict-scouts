from __future__ import annotations

from pathlib import Path

import pygame

from settings import GROUND_Y, OBSTACLE_HEIGHT, OBSTACLE_WIDTH, PLAYER_SPRITE_SIZE, SOUNDS_DIR, SPRITES_DIR, WINDOW_HEIGHT, WINDOW_WIDTH


class AssetStore:
    """Loads all images and sounds in one place."""

    def __init__(self, audio_enabled: bool) -> None:
        background_dir = SPRITES_DIR / "Backgrounds" / "Default"
        character_dir = SPRITES_DIR / "Characters" / "Default"
        tile_dir = SPRITES_DIR / "Tiles" / "Default"

        self.background = self._load_image(background_dir / "background_color_hills.png", (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clouds = self._load_image(background_dir / "background_clouds.png", (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.ground = self._load_image(tile_dir / "terrain_grass_block_top.png", (64, 64))

        self.player_idle = self._load_image(character_dir / "character_green_idle.png", PLAYER_SPRITE_SIZE)
        self.player_jump = self._load_image(character_dir / "character_green_jump.png", PLAYER_SPRITE_SIZE)
        self.player_walk_frames = (
            self._load_image(character_dir / "character_green_walk_a.png", PLAYER_SPRITE_SIZE),
            self._load_image(character_dir / "character_green_walk_b.png", PLAYER_SPRITE_SIZE),
        )

        self.obstacle = self._load_image(tile_dir / "cactus.png", (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.obstacle_small = self._load_image(tile_dir / "rock.png", (46, 34))

        self.jump_sound = self._load_sound(SOUNDS_DIR / "sfx_jump.ogg") if audio_enabled else None
        self.hit_sound = self._load_sound(SOUNDS_DIR / "sfx_hurt.ogg") if audio_enabled else None

        self.ground_rect = pygame.Rect(0, GROUND_Y, WINDOW_WIDTH, WINDOW_HEIGHT - GROUND_Y)

    def _load_image(self, path: Path, size: tuple[int, int]) -> pygame.Surface:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)

    def _load_sound(self, path: Path) -> pygame.mixer.Sound | None:
        try:
            sound = pygame.mixer.Sound(path)
        except pygame.error:
            return None

        sound.set_volume(0.35)
        return sound
