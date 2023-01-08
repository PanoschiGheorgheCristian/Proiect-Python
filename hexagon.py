import math, pygame
from typing import Tuple, List

class Hexagon:
    
    radius: int = 26
    position: tuple([float, float])
    colour = (56,93,56)
    highlight = (82,97,82)
    destroyed: int = 0
    minimal_radius: float = math.sqrt(3) * radius / 2
    
    def __init__(self, x, y, destroyed) -> None:
        coordinates = x,y
        self.position = coordinates
        self.destroyed = destroyed
        self.vertices = self.compute_vertices()
        
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
    
    def render(self, screen) -> None:
        pygame.draw.polygon(screen, self.colour, self.vertices)
        pygame.draw.polygon(screen, (0,0,0), self.vertices, 1)
