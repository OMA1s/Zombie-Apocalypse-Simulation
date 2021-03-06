"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7



class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        height = self.get_grid_height()
        width = self.get_grid_width()
        visited = poc_grid.Grid(height, width)
        distance_field = [[ height * width \
                           for dummy_col in range(width)] \
                             for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for item in self._zombie_list:
                boundary.enqueue(item)
        if entity_type == HUMAN:
            for item in self._human_list:
                boundary.enqueue(item)
        for cell in boundary:
            visited.set_full(cell[0],cell[1])
            distance_field[cell[0]][cell[1]] = 0
            
        while boundary:
            cell = boundary.dequeue()
            neighbors = visited.four_neighbors(cell[0],cell[1])
            for neighbor in neighbors:
                if visited.is_empty(neighbor[0],neighbor[1]) and self.is_empty(neighbor[0],neighbor[1]):
                    visited.set_full(neighbor[0], neighbor[1])
                    boundary.enqueue(neighbor)
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[cell[0]][cell[1]] +1
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        templ = []
        for human in self._human_list:
            neighbors = self.eight_neighbors(human[0],human[1])
            best_move = float('-inf')
            best_neighbor = human
            for neighbor in neighbors:
                if not self.is_empty(neighbor[0], neighbor[1]):
                    continue
                if (neighbor[0], neighbor[1]) in self._zombie_list:
                    continue
                move = zombie_distance_field[neighbor[0]][neighbor[1]]
                if move >= best_move:
                    best_move = move
                    best_neighbor = neighbor
            templ.append(best_neighbor)
        self._human_list = templ
            
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        templ = []
        for zombie in self._zombie_list:
            
            if (zombie[0],zombie[1]) in self._human_list:
                templ.append(zombie)
                continue
            neighbors = self.four_neighbors(zombie[0],zombie[1])
            best_move = float('inf')
            best_neighbor = zombie
            for neighbor in neighbors:
                if not self.is_empty(neighbor[0], neighbor[1]):
                    continue
                move = human_distance_field[neighbor[0]][neighbor[1]]
                if move <= best_move:
                    best_move = move
                    best_neighbor = neighbor
            templ.append(best_neighbor)
        self._zombie_list = templ

    
# Start up gui for simulation 

poc_zombie_gui.run_gui(Apocalypse(30, 40))
