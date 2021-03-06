#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 18:26:13 2017

@author: thinkpad

Defining the Grid class that contains all the cells
"""
import params
from cell import Cell

directions_vect = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


class Grid(object):
    """ Definig the Grid object
        The Grid is basically a matrix of Cells
    """
    def __init__(self):
        self.grid_size = params.grid_size

        self.grid = [[Cell(i, j) for j in range(params.grid_size[0])] \
                     for i in range(params.grid_size[1])]

        self.nests = []
        self.update_time = 0
        self.step = params.step

    def __getitem__(self, pos):
        
        """
        Returns the cell in pos
        """
        i, j = pos
        if (i*(self.grid_size[0]-i) >= 0) and ( j*(self.grid_size[1]-j) >= 0):
            return self.grid[i][j]

        raise NameError("Cell (%d,%d) out of bound"%(i,j))
        return None

    def access(self,pos,new_pos,has_food):
        
        try:
            reward = self.__getitem__([new_pos[0],new_pos[1]]).access(has_food)
            self.__getitem__(pos).count-=1
            self.__getitem__(new_pos).count+=1
            return new_pos, reward
        except:
            reward = self.__getitem__([pos[0],pos[1]]).access(has_food)            
            return pos,reward
        

    def get_state(self,pos,has_food):
        state = []
        for i in range(8):
            x0 = pos[0] + directions_vect[i][0]
            y0 = pos[1] + directions_vect[i][0]
            if (x0*(self.grid_size[0]-x0) >= 0) and ( y0*(self.grid_size[1]-y0) >= 0):
                state.append(self.grid[x0][y0].get_phero(has_food))
            else:
                state.append(-2)
        return state
    def load_grid(self, filename):
        """Loads the grid from filename
        the file contains lines in the format : int x, int y,cell_type
        """
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        for i in lines:
            i = i.replace("\n", "").split(",")
            self.grid[int(i[0])][int(i[1])].type = i[2].upper()
            if i[2] == "NEST":
                self.nests.append([int(n) for n in i[:2]])

    def save_grid(self, filename):
        """ Saves the grid from to memory to filename
        """
        file = open(filename, "w")
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid[i][j].type != "ROAD":
                    file.write(str(i)+","+str(j)+","+self.grid[i][j].type+"\n")
        file.close()

    def update(self):
        """ Iterates through all cells and updates them
        """
        self.update_time = (self.update_time+1)%self.step
        if self.update_time == 0:
            for row in self.grid:
                for cell in row:
                    cell.update()
    def draw(self, display):
        """ Draw all the grid's cells
        """
        for row in self.grid:
            for cell in row:
                cell.draw(display, params.block_size)
