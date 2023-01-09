import math, pygame
from typing import Tuple, List

TILE = (56,93,56)
HIGHLIGHTEDTILE = (82,97,82)
DESTROYEDTILE = (0,0,0)

class Hexagon:
    '''
    A class to represent a Hexagon, or a tile from the board.
    
    ```
    
    Attributes
    ``````````
    radius : int
        always equal to 30
    position : tuple([float, float])
        the coordinates of the point at the top of the hexagon
    center : tuple([float, float])
        the coordinates of the center of the hexagon
    colour : tuple([int,int,int])
        the RGB values of the default colour of the hexagon
    highlight : tuple([int,int,int])
        the RGB values of the colour the hexagon is when highlighted
    destroyed : int
        stores wether or not the hexagon is destroyed
    has_mouse : int
        stores wether or not the mouse is currently on top of the hexagon
    minimal_radius : float
        the distance from the center of the hexagon to any of its edges
        
    Methods
    ```````
    compute_vertices():
        returns the coordinates of all the points of the hexagon, in order up, up-left, down-left, down, down-right, up-right
        
    destroy_hex():
        sets the destroyed attribute to 1
        
    inside_point(coursor_x, coursor_y):
        checks wether the given coordinates are inside of the hexagon
        
    update_higlight(coursor_x, coursor_y):
        checks wether the given coordinates are inside the hexagon; 
        if they are not it returns to normal colour, but if they are and the hexagon does not have the mouse on top of it, it becomes highlighted.
        
    render(screen):
        paints the hexagon on the screen; if it is destroyed it will be black.
    '''
    
    radius: int = 30
    position: tuple([float, float])
    center: tuple([float, float])
    colour = TILE
    highlight = HIGHLIGHTEDTILE
    destroyed: int = 0
    has_mouse: int = 0
    minimal_radius: float = math.sqrt(3) * radius / 2
    
    def __init__(self, x, y, destroyed) -> None:
        '''
        Initializes all the values needed for the hexagon.
        
        :param x: x coordinate of the top of the hexagon
        :param y: y coordinate of the top of the hexagon
        :param destroyed: wether or not the given hexagon is destroyed
        '''
        center_coordinates = x, y + self.radius
        self.position = x, y
        self.center = center_coordinates
        self.destroyed = destroyed
        self.vertices = self.compute_vertices()
        if destroyed == 1:
            self.colour = DESTROYEDTILE
        
    def compute_vertices(self) -> List[Tuple[float, float]]:
        '''
        Returns the coordinates of all the points of the hexagon, in order up, up-left, down-left, down, down-right, up-right
        
        :return: a tuple of 6 elements, each the coordinates of a vertice of the hexagon
        '''
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
        '''
        Sets the destroyed attribute of the hexagon to 1
        '''
        self.destroyed = 1
    
    def inside_point(self, coursor_x, coursor_y) -> bool:
        '''
        Checks wether the given coordinates are inside of the hexagon
        
        If the distance from the center of the hexagon to the coordinates is smaller than the minimal radius the point with the given coordinates is within the hexagon
        
        :param coursor_x: x coordinate of the point
        :param coursor_y: y coordinate of the point
        :return: wether or not the point is within the hexagon
        '''
        return math.dist( (coursor_x, coursor_y), self.center ) < self.minimal_radius
    
    def update_highlight(self, coursor_x, coursor_y) -> None:
        '''
        Checks wether the given coordinates are inside the hexagon; 
        If they are not it returns to normal colour, but if they are and the hexagon does not have the mouse on top of it, it becomes highlighted.
        
        :param coursor_x: x coordinate of the point
        :param coursor_y: y coordinate of the point
        '''
        if self.inside_point(coursor_x, coursor_y) == False:
            self.colour = TILE
        if self.inside_point(coursor_x, coursor_y) and self.has_mouse == 0:
            self.colour = HIGHLIGHTEDTILE
    
    def render(self, screen) -> None:
        '''
        Paints the hexagon on the screen; if it is destroyed it will be black.
        
        :param screen: the screen used by Pygame to paint on
        '''
        if self.destroyed == 0:
            pygame.draw.polygon(screen, self.colour, self.vertices)
            pygame.draw.polygon(screen, DESTROYEDTILE, self.vertices, 1)
        else:
            pygame.draw.polygon(screen, DESTROYEDTILE, self.vertices)
