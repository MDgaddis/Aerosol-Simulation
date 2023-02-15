#!/usr/bin/env python3

import random
import matplotlib.patches as mpatch
import matplotlib.pyplot as plt
import AvgAgentBackground as Agent
import numpy as np


class Cell:
    def __init__(self, name):
        self.population = []
        self.virions = 0
        self.transient_population = []
        self.transient_vir = 0
        self.name = name
        self.adjacent_cells = []
        self.exit_done = False
        self.vent_done = False
        self.people_exit_cells = []
        self.cells_from_exit = 0
        self.wall = False
        self.version = ''
        self.move_prob = 0
        self.cells_from_vent = 0
        self.virion_exit_cells = []
        self.vent = 0
        self.vent_direction = 0
        self.filtered_virions = []
        self.direction = 0
        self.inlet = False
        self.filtration_percentage = 0
        self.frames_since_virion_movement = 0
        self.infected_count = 0

    def move_people(self, grid):
        total = []  # keep track of how much space we've delegated below if person =/= exiting
        for cell in self.adjacent_cells:
            if len(grid.cell_list[cell].population) + len(grid.cell_list[cell].transient_population) > 7:
                total.append(0)
            else:
                total.append(7 - len(grid.cell_list[cell].population) - len(grid.cell_list[cell].transient_population))

        if sum(total) == 0:
            pass
        else:
            csum = np.cumsum(total)  # cumulative sum for the prob distribution
            dist = list(range(1, max(csum) + 1))

        for person in self.population:
            if person.Exiting is True:
                if self.people_exit_cells:
                    d = random.choice(self.people_exit_cells)
                    grid.cell_list[d].transient_population.append(person)
                    person.marked_for_removal = True
                else:
                    person.marked_for_removal = True

            if not person.Exiting:
                a = random.random()
                b = len(list(filter(lambda x: x.marked_for_removal == False, self.population)))
                if sum(total) != 0:
                    csum = np.cumsum(total)  # cumulative sum for the prob distribution
                    c = random.choice(dist)
                    prob_list = [.6, .7, .8, .85, .9, .95,
                                 1]  # arbitrary movement distribution (whether to move or not depending on number of people)
                    if b > 6:
                        b = 6
                    if a > prob_list[b]:
                        pass
                    if a <= prob_list[b]:
                            if len(total) == 1:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 2:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 3:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 4:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                                elif csum[2] < c <= csum[3]:
                                    grid.cell_list[self.adjacent_cells[3]].transient_population.append(person)
                                    dist.remove(c)
                                    total[3] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 5:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                                elif csum[2] < c <= csum[3]:
                                    grid.cell_list[self.adjacent_cells[3]].transient_population.append(person)
                                    dist.remove(c)
                                    total[3] -= 1
                                    person.marked_for_removal = True
                                elif csum[3] < c <= csum[4]:
                                    grid.cell_list[self.adjacent_cells[4]].transient_population.append(person)
                                    dist.remove(c)
                                    total[4] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 6:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                                elif csum[2] < c <= csum[3]:
                                    grid.cell_list[self.adjacent_cells[3]].transient_population.append(person)
                                    dist.remove(c)
                                    total[3] -= 1
                                    person.marked_for_removal = True
                                elif csum[3] < c <= csum[4]:
                                    grid.cell_list[self.adjacent_cells[4]].transient_population.append(person)
                                    dist.remove(c)
                                    total[4] -= 1
                                    person.marked_for_removal = True
                                elif csum[4] < c <= csum[5]:
                                    grid.cell_list[self.adjacent_cells[5]].transient_population.append(person)
                                    dist.remove(c)
                                    total[5] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 7:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                                elif csum[2] < c <= csum[3]:
                                    grid.cell_list[self.adjacent_cells[3]].transient_population.append(person)
                                    dist.remove(c)
                                    total[3] -= 1
                                    person.marked_for_removal = True
                                elif csum[3] < c <= csum[4]:
                                    grid.cell_list[self.adjacent_cells[4]].transient_population.append(person)
                                    dist.remove(c)
                                    total[4] -= 1
                                    person.marked_for_removal = True
                                elif csum[4] < c <= csum[5]:
                                    grid.cell_list[self.adjacent_cells[5]].transient_population.append(person)
                                    dist.remove(c)
                                    total[5] -= 1
                                    person.marked_for_removal = True
                                elif csum[5] < c <= csum[6]:
                                    grid.cell_list[self.adjacent_cells[6]].transient_population.append(person)
                                    dist.remove(c)
                                    total[6] -= 1
                                    person.marked_for_removal = True
                            elif len(total) == 8:
                                if c <= csum[0]:
                                    grid.cell_list[self.adjacent_cells[0]].transient_population.append(person)
                                    dist.remove(c)
                                    total[0] -= 1
                                    person.marked_for_removal = True
                                elif csum[0] < c <= csum[1]:
                                    grid.cell_list[self.adjacent_cells[1]].transient_population.append(person)
                                    dist.remove(c)
                                    total[1] -= 1
                                    person.marked_for_removal = True
                                elif csum[1] < c <= csum[2]:
                                    grid.cell_list[self.adjacent_cells[2]].transient_population.append(person)
                                    dist.remove(c)
                                    total[2] -= 1
                                    person.marked_for_removal = True
                                elif csum[2] < c <= csum[3]:
                                    grid.cell_list[self.adjacent_cells[3]].transient_population.append(person)
                                    dist.remove(c)
                                    total[3] -= 1
                                    person.marked_for_removal = True
                                elif csum[3] < c <= csum[4]:
                                    grid.cell_list[self.adjacent_cells[4]].transient_population.append(person)
                                    dist.remove(c)
                                    total[4] -= 1
                                    person.marked_for_removal = True
                                elif csum[4] < c <= csum[5]:
                                    grid.cell_list[self.adjacent_cells[5]].transient_population.append(person)
                                    dist.remove(c)
                                    total[5] -= 1
                                    person.marked_for_removal = True
                                elif csum[5] < c <= csum[6]:
                                    grid.cell_list[self.adjacent_cells[6]].transient_population.append(person)
                                    dist.remove(c)
                                    total[6] -= 1
                                    person.marked_for_removal = True
                                elif csum[6] < c <= csum[7]:
                                    grid.cell_list[self.adjacent_cells[7]].transient_population.append(person)
                                    dist.remove(c)
                                    total[7] -= 1
                                    person.marked_for_removal = True
                else:
                    pass

        self.population = list(filter(lambda x: x.marked_for_removal is False, self.population))

    def flow_move_virions(self, grid):

        if self.cells_from_vent > 1:
            d = random.choice(self.virion_exit_cells)
            # if self.name % grid.num_col != d % grid.num_col and self.name // grid.num_col != d // grid.num_col:
            #     grid.cell_list[d].transient_vir += .7*self.virions
            #     i = set(self.adjacent_cells)
            #     d1 = set(grid.cell_list[d].adjacent_cells)
            #     d2 = list(i.intersection(d1))
            #     d3 = len(d2)
            #     for cell in d2:
            #         grid.cell_list[cell].transient_vir += (.3/d3)*self.virions
            # else:
            grid.cell_list[d].transient_vir += self.virions
            self.virions = 0

    def transient_states(self):
        for person in self.transient_population:
            person.marked_for_removal = False
        self.population += self.transient_population
        self.transient_population = []
        self.virions += self.transient_vir
        self.transient_vir = 0

    def despawn_person(self, frame_count):
        for person in self.population:
            if person.arrival_time + person.Time_Stayed - (self.cells_from_exit + 5) < frame_count:
                person.Exiting = True

    def cell_colors_people(self, rectangle_array):
        colors_list = ['#FFFFFF', '#FFbaba', '#FF7b7b', '#ff5252', '#ff0000', '#a70000', '#960000', '#530000']
        b = len(self.population) + len(self.transient_population)
        if not self.wall:
            rectangle_array[self.name].set(color=colors_list[b if b < 7 else 7])

        return rectangle_array

    def cell_colors_virions(self, rectangle_array, ceiling_height, frames):
        colors_list = ['#FFFFFF', '#e0e5ff', '#bac5fe', '#8ea0fe', '#5773ff', '#2548ff', '#0e35ff',
                       '#0029ff']  # 0, 12.5, 25, 37.5, 50, 62.5, 75, 90, 90+ %chance of infection in 1 minute.

        b = self.virions / (ceiling_height * 100)  # virions/L breathed in

        if not self.wall:
            if (b/frames) <= 10:
                rectangle_array[self.name].set(color=colors_list[0])
            if 10 < (b/frames) <= 20:
                rectangle_array[self.name].set(color=colors_list[1])
            if 20 < (b/frames) <= 30:
                rectangle_array[self.name].set(color=colors_list[2])
            if 30 < (b/frames) <= 40:
                rectangle_array[self.name].set(color=colors_list[3])
            if 40 < (b/frames) <= 50:
                rectangle_array[self.name].set(color=colors_list[4])
            if 60 < (b/frames) <= 70:
                rectangle_array[self.name].set(color=colors_list[5])
            if 70 < (b/frames) <= 80:
                rectangle_array[self.name].set(color=colors_list[6])
            if (b/frames) > 80:
                rectangle_array[self.name].set(color=colors_list[7])

        return rectangle_array

    def cell_colors_infected(self, rectangle_array):
        colors_list = ['#FFFFFF', '#000000']
        infected_population = [person for person in self.population if person.__class__ is Agent.Infected]
        b = len(infected_population)
        if not self.wall:
            rectangle_array[self.name].set(color=colors_list[b if b < 2 else 1])

        return rectangle_array

    def spread_virions(self, grid, cough, sneeze, talk, minutes_per_frame=1, viab_vir=.01):
        # move coughing in 3 meters in face direction / large droplets 1.5~
        # move sneezing 6 meters in face direction / large droplets 3~
        # infected = (person for person in self.population if person.__class__ is Agent.Infected)

        # Reason for this loop: the "infected" bit above makes you loop
        # over everyone in the cell to filter out the infected people---
        # then you loop over those people a second time to do stuff.
        # Save yourself some work by just looping over people once, and if they're infected, do stuff.
        for p in self.population:
            if p.__class__ is Agent.Infected:
                face = random.choices(population=[-1, 1, -grid.num_col, grid.num_col], weights=[0, 0, 0, 1], k=1)
                p.face_direction = face[0]
                # Not super beautiful and there's probably a sleek way to do this in two lines, but I'm tired and it's not slow.
                # One pretty cute option at the cost of a small bit of memory is to precompute every cells north, west, etc. cells and store them in appropriate lists, then below just take the 8 first elements of whatever.
                if p.face_direction == -1:
                    extent = self.name % grid.num_col  # Can only go as far left as our current colum
                elif p.face_direction == 1:
                    extent = grid.num_col - 1 - (
                                self.name % grid.num_col)  # Can only go as far right as the remaining columns
                elif p.face_direction == -grid.num_col:
                    extent = self.name // grid.num_col  # Can only go as far down as the current row
                elif p.face_direction == grid.num_col:
                    extent = grid.num_row - 1 - (
                                self.name // grid.num_col)  # Can only go as far up as the remaining rows

                # Also not sure if you want to skip a=1 and b=1? The cell right in front of them.

                a1 = random.random()
                b1 = random.random()
                c1 = random.random()

                if sneeze > a1:
                    for a in range(min(6, extent)):
                        if extent >= 6:
                            if a == 4 or 5:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.131/2)*p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 2 or 3:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.167/2)*p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 0 or 1:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.702/2)*p.Sneeze(minutes_per_frame, viab_vir)
                        if extent == 5:
                            if a == 4:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += .131 * p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 2 or 3:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.167/2)*p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 0 or 1:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.702/2)*p.Sneeze(minutes_per_frame, viab_vir)
                        elif extent == 4:
                            if a == 2 or 3:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.167/2)*p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 0 or 1:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.702/2)*p.Sneeze(minutes_per_frame, viab_vir)
                        elif extent == 3:
                            if a == 2:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.167 + .131)*p.Sneeze(minutes_per_frame, viab_vir)
                            if a == 0 or 1:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (.702/2)*p.Sneeze(minutes_per_frame, viab_vir)
                        elif extent == 2:
                            if a == 0 or 1:
                                grid.cell_list[self.name + (a * p.face_direction)].transient_vir += (1/2)*p.Sneeze(minutes_per_frame, viab_vir)
                        elif extent == 1:
                            grid.cell_list[self.name + (a * p.face_direction)].transient_vir += p.Sneeze(minutes_per_frame, viab_vir)

                if cough > b1:
                    for b in range(min(4, extent)):
                        if extent >= 4:
                            if b == 2 or 3:
                                grid.cell_list[self.name + (b * p.face_direction)].transient_vir += (.192/2)*p.Cough(minutes_per_frame, viab_vir)
                            if b == 0 or 1:
                                grid.cell_list[self.name + (b * p.face_direction)].transient_vir += (.808/2)*p.Cough(minutes_per_frame, viab_vir)
                        elif extent == 3:
                            if b == 2:
                                grid.cell_list[self.name + (b * p.face_direction)].transient_vir += .192 * p.Cough(minutes_per_frame, viab_vir)
                            if b == 0 or 1:
                                grid.cell_list[self.name + (b * p.face_direction)].transient_vir += (.808/2)*p.Cough(minutes_per_frame, viab_vir)
                        elif extent == 2:
                            if b == 0 or 1:
                                grid.cell_list[self.name + (b * p.face_direction)].transient_vir += (1/2)*p.Cough(minutes_per_frame, viab_vir)
                        elif extent == 1:
                            grid.cell_list[self.name + (b * p.face_direction)].transient_vir += p.Cough(minutes_per_frame, viab_vir)

                if talk > c1:
                    for c in range(min(2, extent)):
                        if extent >= 2:
                            grid.cell_list[self.name + (c * p.face_direction)].transient_vir += (1/2)*p.Talk(minutes_per_frame, viab_vir)
                        if extent == 1:
                            grid.cell_list[self.name + (c * p.face_direction)].transient_vir += p.Talk(minutes_per_frame, viab_vir)

                grid.cell_list[self.name].transient_vir += p.Breathe(minutes_per_frame, viab_vir)

    def breathe_virions(self, minutes_per_frame, grid):
        # Each person breathes in equal amount of virions.
        # Volume of air-pillar around cell: 1m x 1m x ceiling height
        # 1 m^3 = 1000 L

        air_pillar = grid.cell_height * (10 ** 3)  # Liters
        vir_per_liter = self.virions / air_pillar

        for p in self.population:
            p.breathe_in(vir_per_liter, minutes_per_frame)

    def return_filtered_virions(self, fil_virions, frame_count, grid):
        self.filtered_virions.append(fil_virions / len(grid.vent_outlet_cells))
        distance = 2
        # below = (self.name // grid.num_col)
        # above = grid.num_row - below
        # left = (self.name % grid.num_col)
        # right = grid.num_col - left

        if self.vent_direction is self.name + 1:  # vent direction is to the right
            for a in range(distance):
                grid.cell_list[self.name + 1 + a].transient_vir += (1/2)*(self.filtered_virions[frame_count-1])
        if self.vent_direction is self.name - 1:  # vent direction to the left
            for a in range(distance):
                grid.cell_list[self.name - 1 - a].transient_vir += (1/2)*(self.filtered_virions[frame_count-1])
        if self.vent_direction is self.name + grid.num_col:  # vent direction up
            for a in range(distance):
                grid.cell_list[self.name + grid.num_col + a].transient_vir += (self.filtered_virions[frame_count - 1])
        if self.vent_direction is self.name - grid.num_col:  # vent direction down
            for a in range(distance):
                grid.cell_list[self.name - grid.num_col + a].transient_vir += (self.filtered_virions[frame_count - 1])
        if self.vent_direction == 0:
            b = len(self.adjacent_cells)
            for cell in self.adjacent_cells:
                grid.cell_list[cell].transient_vir += (self.filtered_virions[frame_count - 1])/b


class Grid:
    def __init__(self, num_row=100, num_col=100, cell_height=1):
        self.cell_list = []
        self.cell_height = cell_height  # meters
        self.num_col = num_col
        self.num_row = num_row
        self.Number_Cells = num_col * num_row
        self.cell_names = []
        self.spawn_cells = []
        self.vent_outlet_cells = []
        self.vent_inlet_cells = []
        self.distances_from_inlet = []

    def Create_Grid(self, *doors):
        for i in range(self.Number_Cells):
            cell = Cell(i)
            self.cell_list.append(cell)
            if not (i % self.num_col) * ((i + 1) % self.num_col) * ((i // self.num_col) - self.num_row + 1) * (
                    i // self.num_col):  # think of them as roots for inner_col/outer_col/outer/inner/row (call jakob)
                cell.wall = True
        # for door in doors:
        #     self.spawn_cells.append(door)

    def cell_color_pre_infected(self, ax):
        for Cell in self.cell_list:
            if not Cell.wall:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, edgecolor='#FFFFFF')
                ax[1, 1].add_artist(a)
                cx, cy = a.get_xy()
                cy = cy + a.get_height() / 2.0
                cx = cx + a.get_width() / 2.0
                ax[1, 1].annotate(str(Cell.infected_count), (cx, cy), color='w', weight='bold', fontsize=6, ha='center', va='center')
            else:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, color='#000000',
                                      edgecolor='#FFFFFF')
                ax[1, 1].add_artist(a)

    def cell_color_pre_infected_single(self, ax, index_cells=[]):
        for Cell in self.cell_list:
            if not Cell.wall and Cell not in index_cells:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, edgecolor='#FFFFFF')
                ax.add_artist(a)
                cx, cy = a.get_xy()
                cy = cy + a.get_height() / 2.0
                cx = cx + a.get_width() / 2.0
                ax.annotate(str(Cell.infected_count), (cx, cy), color='w', weight='bold', fontsize=6, ha='center', va='center')
            else:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, color='#000000',
                                      edgecolor='#FFFFFF')
                ax.add_artist(a)
            if Cell in index_cells:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, edgecolor='#FFFFFF', facecolor='#8b0000')
                ax.add_artist(a)
                cx, cy = a.get_xy()
                cy = cy + a.get_height() / 2.0
                cx = cx + a.get_width() / 2.0
                ax.annotate(str(Cell.infected_count), (cx, cy), color='w', weight='bold', fontsize=6, ha='center', va='center')

    def Show_Grid(self):
        fig, ax = plt.subplots()

        for Cell in self.cell_list:
            if not Cell.wall:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, edgecolor='#FFFFFF')
                ax.add_artist(a)
            else:
                a = mpatch.Rectangle((Cell.name % self.num_col, Cell.name // self.num_col), 1, 1, color='#000000',
                                      edgecolor='#FFFFFF')
                ax.add_artist(a)
            cx, cy = a.get_xy()
            cy = cy + a.get_height() / 2.0
            cx = cx + a.get_width() / 2.0
            ax.annotate(str(Cell.name), (cx, cy), color='w', weight='bold', fontsize=6, ha='center', va='center')

        ax.set_xlim((0, self.num_col))
        ax.set_ylim((0, self.num_row))
        ax.set_aspect('equal')
        plt.show()

    def Check_Adjacency(self):
        for Cell in self.cell_list:
            if Cell.name + self.num_col < self.Number_Cells:
                Cell.adjacent_cells.append(Cell.name + self.num_col)        #up

            if Cell.name - self.num_col >= 0:
                Cell.adjacent_cells.append(Cell.name - self.num_col)        #down

            if (Cell.name + 1) % self.num_col != 0 and Cell.name + 1 < self.Number_Cells:
                Cell.adjacent_cells.append(Cell.name + 1)                   #right

            if Cell.name % self.num_col != 0:
                Cell.adjacent_cells.append(Cell.name - 1)                   #left

            # Experimental 8 way movement

            if (Cell.name % self.num_col) != 0 and Cell.name + self.num_col - 1 < self.Number_Cells: # and not self.cell_list[Cell.name + self.num_col - 1].wall:
                Cell.adjacent_cells.append(Cell.name + self.num_col - 1)  # up and left

            if ((Cell.name + 1) % self.num_col) != 0 and Cell.name + self.num_col + 1 < self.Number_Cells: #and not self.cell_list[ Cell.name + self.num_col + 1].wall
                Cell.adjacent_cells.append(Cell.name + self.num_col + 1)  # up and right

            if (Cell.name % self.num_col) and Cell.name - self.num_col - 1 >= 0: #and not self.cell_list[Cell.name - self.num_col - 1].wall
                Cell.adjacent_cells.append(Cell.name - self.num_col - 1)  # down and left

            if ((Cell.name + 1) % self.num_col) != 0 and Cell.name - self.num_col + 1 >= 0: # and not self.cell_list[Cell.name - self.num_col - 1].wall:
                Cell.adjacent_cells.append(Cell.name - self.num_col + 1)  # down and right

    def leave_path(self):
        active_cells = [self.cell_list[i] for i in self.spawn_cells]
        cells_from_exit1 = -1
        while len(active_cells) > 0:
            cells_from_exit1 += 1
            for cell in tuple(active_cells):
                cell.cells_from_exit = cells_from_exit1
                add_exit_cells = [self.cell_list[i] for i in cell.adjacent_cells]
                for c in add_exit_cells:
                    if c.exit_done is False and c not in active_cells:
                        active_cells.append(c)
                    if c.exit_done:
                        cell.people_exit_cells.append(c.name)
                    cell.exit_done = True
                active_cells = list(filter(lambda x: x.exit_done is False, active_cells))

    def distance_to_inlets(self):
        active_cells = [self.cell_list[i.name] for i in self.vent_inlet_cells]
        cells_from_vent1 = -1
        while len(active_cells) > 0:
            cells_from_vent1 += 1  # set the cells from nearest inlet to be 0
            for cell in tuple(active_cells):  # reset all cells in cell_list to not be completed, for start of new vent
                cell.cells_from_vent = cells_from_vent1
                self.distances_from_inlet.append(cells_from_vent1)
                add_exit_cells = [self.cell_list[i] for i in cell.adjacent_cells]
                for c in add_exit_cells:
                    if not c.wall:
                        if c.vent_done is False and c not in active_cells:
                            active_cells.append(c)
                        if c.vent_done and c.cells_from_vent < cell.cells_from_vent:
                            cell.virion_exit_cells.append(c.name)
                cell.vent_done = True
                active_cells = list(filter(lambda x: x.vent_done is False, active_cells))

    def spawn_people(self, frame_count, sorted_population):
        while sorted_population and sorted_population[0].arrival_time < frame_count:
            spawn_tile = random.choice(self.spawn_cells)
            sorted_population[0].face_direction = (spawn_tile - random.choice(self.cell_list[spawn_tile].adjacent_cells))
            sorted_population[0].Spawned = True
            self.cell_list[spawn_tile].transient_population.append(sorted_population[0])
            sorted_population.pop(0)

    def set_inlet(self, cell_number, filter_percentage):
        self.vent_inlet_cells.append(self.cell_list[cell_number])
        self.cell_list[cell_number].filtration_percentage = filter_percentage
        self.cell_list[cell_number].inlet = True

    def set_outlet(self, cell_number, flow_direction):
        self.vent_outlet_cells.append(self.cell_list[cell_number])
        self.cell_list[cell_number].vent_direction = flow_direction

    def filter_virions(self):
        pre_filtered_virions = 0
        print(pre_filtered_virions)
        for cell in self.vent_inlet_cells:
            for adj in cell.adjacent_cells:
                pre_filtered_virions += self.cell_list[adj].virions*(1-cell.filtration_percentage)
                self.cell_list[adj].virions = 0
        print(pre_filtered_virions)
        return pre_filtered_virions

