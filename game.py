# ============================================================
# FILE: game.py
# ============================================================
"""
Main game loop and state management.
"""
import pygame
import sys
from board import Board
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FLIP_DELAY,
    WHITE, BLACK, BLUE, RED, GREEN, GRAY
)


class MemoryGame:
    """
    The main Memory Card Matching Game class.
    """
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Memory Card Matching Game")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_card = pygame.font.Font(None, 48)
        
        self.board = Board()
        self.running = True
        self.flip_timer = 0
        self.waiting_for_flip = False
        self.game_over = False
        self.game_won = False
        
        # Score tracking
        self.moves = 0
        self.start_time = pygame.time.get_ticks()
        
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over or self.game_won:
                    # Click to restart
                    if self._is_restart_clicked(event.pos):
                        self.reset_game()
                else:
                    # Handle card click
                    if self.board.handle_click(event.pos):
                        self.moves += 1
                        # Check if we need to check for a match
                        if len(self.board.selected_cards) == 2:
                            self.waiting_for_flip = True
                            self.flip_timer = pygame.time.get_ticks()
                            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def _is_restart_clicked(self, pos):
        """Check if the restart button was clicked."""
        # Simple restart area check
        if SCREEN_WIDTH // 2 - 100 < pos[0] < SCREEN_WIDTH // 2 + 100:
            if SCREEN_HEIGHT // 2 + 50 < pos[1] < SCREEN_HEIGHT // 2 + 100:
                return True
        return False
                    
    def update(self):
        """Update game state."""
        # Handle match checking after delay
        if self.waiting_for_flip:
            current_time = pygame.time.get_ticks()
            if current_time - self.flip_timer > FLIP_DELAY:
                # Check match
                if len(self.board.selected_cards) == 2:
                    if self.board.check_match():
                        # Match found
                        pass
                    else:
                        # No match - flip back
                        self.board.flip_back()
                self.waiting_for_flip = False
                
        # Check if game is complete
        if self.board.is_game_complete() and not self.game_won:
            self.game_won = True
            self.game_over = True
            
        # Update game time if not over
        if not self.game_over:
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            
    def render(self):
        """Render all game elements."""
        self.screen.fill(WHITE)
        
        # Draw title and info
        self._draw_header()
        
        # Draw the board
        self.board.draw(self.screen, self.font_card)
        
        # Draw game over / win screen
        if self.game_over:
            self._draw_game_over()
            
        # Draw instructions
        self._draw_footer()
        
        pygame.display.flip()
        
    def _draw_header(self):
        """Draw the game header with stats."""
        # Title
        title = self.font_medium.render("Memory Match", True, BLACK)
        self.screen.blit(title, (20, 10))
        
        # Stats
        moves_text = self.font_small.render(f"Moves: {self.moves}", True, BLACK)
        self.screen.blit(moves_text, (20, 60))
        
        # Timer
        if not self.game_over:
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            timer_text = self.font_small.render(
                f"Time: {minutes:02d}:{seconds:02d}", True, BLACK
            )
        else:
            timer_text = self.font_small.render(
                f"Final Time: {self.elapsed_time // 60:02d}:{self.elapsed_time % 60:02d}", 
                True, BLACK
            )
        self.screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))
        
        # Pairs matched
        pairs_text = self.font_small.render(
            f"Pairs: {self.board.matched_pairs}/{self.board.total_pairs}", 
            True, BLACK
        )
        self.screen.blit(pairs_text, (SCREEN_WIDTH - 200, 50))
        
        # Restart hint
        restart_hint = self.font_small.render("Press 'R' to restart", True, GRAY)
        self.screen.blit(restart_hint, (SCREEN_WIDTH - 220, SCREEN_HEIGHT - 30))
        
    def _draw_footer(self):
        """Draw footer instructions."""
        if not self.game_over:
            footer = self.font_small.render(
                "Click cards to flip | Match all pairs to win!", 
                True, GRAY
            )
            footer_rect = footer.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
            self.screen.blit(footer, footer_rect)
            
    def _draw_game_over(self):
        """Draw the game over overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        if self.game_won:
            text = "🎉 You Win! 🎉"
            color = GREEN
            subtext = f"Completed in {self.moves} moves!"
        else:
            text = "Game Over"
            color = RED
            subtext = "Better luck next time!"
            
        # Main text
        game_over_text = self.font_large.render(text, True, color)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Subtext
        sub_text = self.font_medium.render(subtext, True, WHITE)
        sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(sub_text, sub_rect)
        
        # Restart button
        button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 100, 
            SCREEN_HEIGHT // 2 + 40, 
            200, 50
        )
        pygame.draw.rect(self.screen, BLUE, button_rect, border_radius=10)
        pygame.draw.rect(self.screen, WHITE, button_rect, 3, border_radius=10)
        
        button_text = self.font_medium.render("Play Again", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
    def reset_game(self):
        """Reset the game to initial state."""
        self.board.reset()
        self.moves = 0
        self.game_over = False
        self.game_won = False
        self.waiting_for_flip = False
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        self.flip_timer = 0
        
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
