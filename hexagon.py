import math, pygame
from typing import Tuple, List

TILE = (56,93,56)
HIGHLIGHTEDTILE = (82,97,82)
DESTROYEDTILE = (0,0,0)

class Hexagon:
    
    radius: int = 30
    position: tuple([float, float])
    center: tuple([float, float])
    colour = TILE
    highlight = HIGHLIGHTEDTILE
    destroyed: int = 0
    has_mouse: int = 0
    minimal_radius: float = math.sqrt(3) * radius / 2
    
    def __init__(self, x, y, destroyed) -> None:
        center_coordinates = x, y + self.radius
        self.position = x, y
        self.center = center_coordinates
        self.destroyed = destroyed
        self.vertices = self.compute_vertices()
        if destroyed == 1:
            self.colour = DESTROYEDTILE
        
    def compute_vertices(self) -> List[Tuple[float, float]]:
        x, y = self.position
        half_radius = self.radius / 2
        minimal_radius = self.minimal_radius
        return [
            (x,y),
            (x - minimal_radius, y + half_radius),
            (x - minimal_radius, y + self.radius + half_radius),
            (x, y + 2 * self.radius),
            (x + minimal_radius, y + self.radius + half_radius),
            (x + minimal_radius, y + half_radius)
        ]
    
    def destroy_hex(self) -> None:
        self.destroyed = 1
    
    def inside_point(self, cursor_x, cursor_y) -> bool:
        return math.dist( (cursor_x, cursor_y), self.center ) < self.minimal_radius
    
    def update_highlight(self, coursor_x, coursor_y) -> None:
        if self.inside_point(coursor_x, coursor_y) == False:
            self.colour = TILE
        if self.inside_point(coursor_x, coursor_y) and self.has_mouse == 0:
            self.colour = HIGHLIGHTEDTILE
    
    def render(self, screen) -> None:
        if self.destroyed == 0:
            pygame.draw.polygon(screen, self.colour, self.vertices)
            pygame.draw.polygon(screen, DESTROYEDTILE, self.vertices, 1)
        else:
            pygame.draw.polygon(screen, DESTROYEDTILE, self.vertices)
