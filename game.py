from __future__ import annotations

import random

import pygame

from asset_store import AssetStore
from obstacle import Obstacle
from player import Player
from settings import FPS, GROUND_Y, HUD_PANEL_COLOR, HUD_TEXT_COLOR, OBSTACLE_DISTANCE_MAX, OBSTACLE_DISTANCE_MIN, OBSTACLE_SPEED, PLAYER_X, TITLE, WIN_PANEL_COLOR, WIN_TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    """Owns the window and the whole runner game."""

    def __init__(self) -> None:
        pygame.init()
        self.audio_enabled = self._try_enable_audio()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 34)
        self.big_font = pygame.font.Font(None, 68)
        self.assets = AssetStore(self.audio_enabled)
        self.random = random.Random()
        self.running = True
        self._reset_game()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()

        pygame.quit()

    def _reset_game(self) -> None:
        self.player = Player(PLAYER_X, self.assets)
        self.obstacles: list[Obstacle] = []
        self.spawn_timer = 1.5
        self.score = 0
        self.game_over = False

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self._reset_game()

    def _update(self, dt: float) -> None:
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        jump_pressed = bool(keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w])

        if self.player.update(dt, jump_pressed):
            self._play_sound(self.assets.jump_sound)

        self._update_obstacles(dt)

        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(self.player.rect):
                self.game_over = True
                self._play_sound(self.assets.hit_sound)
                break

    def _draw(self) -> None:
        self.screen.blit(self.assets.background, (0, 0))
        self.screen.blit(self.assets.clouds, (0, 0))
        self._draw_ground()
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        self.player.draw(self.screen)
        self._draw_hud()

        if self.game_over:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_hud(self) -> None:
        panel = pygame.Surface((WINDOW_WIDTH, 74), pygame.SRCALPHA)
        panel.fill((*HUD_PANEL_COLOR, 210))
        self.screen.blit(panel, (0, 0))

        score_text = f"Punkte: {self.score}"
        mission_text = "Springe über Kakteen und Steine."

        self.screen.blit(self.font.render(score_text, True, HUD_TEXT_COLOR), (20, 14))
        self.screen.blit(self.font.render(mission_text, True, HUD_TEXT_COLOR), (20, 40))

    def _draw_game_over(self) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(WIN_PANEL_COLOR)
        self.screen.blit(overlay, (0, 0))

        line_one = self.big_font.render("Game Over", True, WIN_TEXT_COLOR)
        line_two = self.font.render("Druecke R fuer einen neuen Start.", True, WIN_TEXT_COLOR)

        line_one_rect = line_one.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        line_two_rect = line_two.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 32))

        self.screen.blit(line_one, line_one_rect)
        self.screen.blit(line_two, line_two_rect)

    def _play_sound(self, sound: pygame.mixer.Sound | None) -> None:
        if sound is not None:
            sound.play()

    def _draw_ground(self) -> None:
        for x in range(0, WINDOW_WIDTH, self.assets.ground.get_width()):
            self.screen.blit(self.assets.ground, (x, GROUND_Y))

    def _update_obstacles(self, dt: float) -> None:
        self.spawn_timer -= dt
        if self.spawn_timer <= 0.0:
            self._spawn_obstacle()

        for obstacle in self.obstacles:
            obstacle.update(dt)
            if not obstacle.passed_player and obstacle.rect.right < self.player.rect.left:
                obstacle.passed_player = True
                self.score += 1

        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.is_off_screen()]

    def _spawn_obstacle(self) -> None:
        image = self.assets.obstacle
        y = GROUND_Y
        if self.random.random() < 0.35:
            image = self.assets.obstacle_small
            y = GROUND_Y + 2

        x = WINDOW_WIDTH + 40
        self.obstacles.append(Obstacle(x, y, image, OBSTACLE_SPEED))
        distance = self.random.randint(OBSTACLE_DISTANCE_MIN, OBSTACLE_DISTANCE_MAX)
        self.spawn_timer = distance / OBSTACLE_SPEED

    def _try_enable_audio(self) -> bool:
        try:
            pygame.mixer.init()
        except pygame.error:
            return False

        return True
