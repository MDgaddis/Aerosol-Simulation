import Animate_2 as animate2
import Environment as env
import random
import matplotlib.pyplot as plt
import AvgAgentBackground as Agent
import matplotlib.patches as mpatch
from matplotlib import animation
import math
import numpy as np

## To run this code in terminal, use any of the Sim_Var methods as is. All numbers can be changed in the first Simulate method

def Simulate(cough, sneeze, talk, ACH=60, filter_percentage=0, version='p'):

    sus_population = 67
    infected_population = 1

    # Initial Counts
    # Virions = 0
    # count_Sus = 0
    # count_Inf_Pre = 0
    ceiling_height = 3  # meters

    # Population Lists
    sus_pop = [Agent.Susceptible() for i in range(sus_population)]
    inf_pop = [Agent.Infected() for j in range(infected_population)]
    total_pop = sus_pop + inf_pop
    sorted_pop = total_pop

    # Create Grid
    grid = env.Grid(12 + 2, 3 + 2, ceiling_height)
    grid.Create_Grid()

    # Set inlets at the back of bus (vents)
    # grid.set_inlet(1, filter_percentage)
    grid.set_inlet(2, filter_percentage)
    # grid.set_inlet(3, filter_percentage)
    # grid.set_inlet(37, filter_percentage)
    # Set inlets in the front middle of bus
    # grid.set_inlet(47, 20)
    # Set inlets 2 on each side (windows) may try at another time
    # grid.set_inlet(59,100)
    # grid.set_inlet(55,100)
    # grid.set_inlet(14,100)
    # grid.set_inlet(10,100)

    # Updated (vents at back of bus)
    grid.set_outlet(50, 50+1)
    grid.set_outlet(54, 54-1)
    grid.set_outlet(64, 64-1)
    grid.set_outlet(60, 60+1)
    # grid.set_outlet(59, 59-1)
    # grid.set_outlet(55, 55+1)
    grid.set_outlet(49, 49-1)
    grid.set_outlet(45, 45+1)
    grid.set_outlet(39, 39-1)
    grid.set_outlet(35, 35+1)
    grid.set_outlet(29, 29-1)
    grid.set_outlet(25, 25+1)
    grid.set_outlet(19, 19-1)
    grid.set_outlet(15, 15+1)
    grid.set_outlet(9, 9-1)
    grid.set_outlet(5, 5+1)

    # Create Paths
    grid.Check_Adjacency()
    grid.distance_to_inlets()
    max_distance = max(grid.distances_from_inlet)

    # Set population in seats (left side)
    grid.cell_list[61].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(1)])
    grid.cell_list[51].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[46].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[41].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[36].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[31].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[26].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[21].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[16].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[11].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])
    grid.cell_list[6].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(4)])

    # Set population in seats (right side)
    grid.cell_list[58].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(1)])
    grid.cell_list[53].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[48].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[43].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[38].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[33].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(2)])
    grid.cell_list[28].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(2)])
    grid.cell_list[23].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[18].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])
    grid.cell_list[13].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(2)])
    grid.cell_list[8].population.extend([sus_pop.pop(random.randint(0, len(sus_pop)-1)) for i in range(3)])

    # Set infected population
    grid.cell_list[36].population.append(random.choice(inf_pop))

    m = 0
    for i in grid.cell_list:
        if not i.wall:
            m += 1

    air_volume = (m*(grid.cell_height**2)*ceiling_height)*(10**3)  # m^3 to L
    ACM = ACH/60                                                   # air changes per minute

    viab_vir = 1  # Percentage of viable virions
    distances_to_inlet = []
    for cell in grid.cell_list:
        distances_to_inlet.append(cell.cells_from_vent)
    max_distance = max(distances_to_inlet)

    # Time
    minutes = 100  # minutes on bus
    frames_per_minute = (max_distance*ACM)  # since 1 frame = 1 tile, frames per minute
    minutes_per_frame = 1 / frames_per_minute
    frames = math.ceil(frames_per_minute*minutes)

    # Coughing, Sneezing, Talking Probs

    if version.lower() in ['p']:

        rectangle_array = []

        people = []
        cells = []

        fig, ax = plt.subplots()
        ax.set_xlim((0,grid.num_col))
        ax.set_ylim((0,grid.num_row))
        ax.set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col),1,1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col),1,1, color='b')
            ax.add_artist(a)
            rectangle_array.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_single_people(i, rectangle_array, grid), frames=range(frames+1), interval=1)
        anim.save('p_bus_output.gif', writer='ffmpeg')
        plt.close()

        for i in grid.cell_list:
            cells.append(i)
            people.append(i.population)

    elif version.lower() in ['v']:
        rectangle_array = []

        fig, ax = plt.subplots()
        ax.set_xlim((0, grid.num_col))
        ax.set_ylim((0, grid.num_row))
        ax.set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax.add_artist(a)
            rectangle_array.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_single_virions(i, frames, rectangle_array, grid, ceiling_height, minutes_per_frame, viab_vir, sus_population), frames=range(frames+1), interval=1)
        anim.save('v_bus_output.gif', writer='ffmpeg')
        plt.close()

    elif version.lower() in ['i']:
        rectangle_array = []
        fig, ax = plt.subplots()
        ax.set_xlim((0, grid.num_col))
        ax.set_ylim((0, grid.num_row))
        ax.set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax.add_artist(a)
            rectangle_array.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_single_infected(i, rectangle_array, grid, sorted_pop), frames=range(frames+1), interval=1)
        anim.save('i_bus_output.gif', writer='ffmpeg')
        plt.close()

    elif version.lower() in ['pv','vp']:

        rectangle_array = []
        rectangle_array2 = []

        fig, ax = plt.subplots(1,2)
        ax[0].set_xlim((0,grid.num_col))
        ax[0].set_ylim((0,grid.num_row))
        ax[0].set_aspect('equal')

        ax[1].set_xlim((0,grid.num_col))
        ax[1].set_ylim((0,grid.num_row))
        ax[1].set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[0].add_artist(a)
            rectangle_array.append(a)

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[1].add_artist(a)
            rectangle_array2.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_double_pv(i, rectangle_array, rectangle_array2, grid, sorted_pop,ceiling_height), frames=range(frames+1), interval=1)
        anim.save('p_v_bus_output.gif', writer='ffmpeg')
        plt.close()

    elif version.lower() in ['pi', 'ip']:

        rectangle_array = []
        rectangle_array2 = []

        fig, ax = plt.subplots(1, 2)
        ax[0].set_xlim((0, grid.num_col))
        ax[0].set_ylim((0, grid.num_row))
        ax[0].set_aspect('equal')

        ax[1].set_xlim((0, grid.num_col))
        ax[1].set_ylim((0, grid.num_row))
        ax[1].set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[0].add_artist(a)
            rectangle_array.append(a)

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[1].add_artist(a)
            rectangle_array2.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_double_pi(i, rectangle_array, rectangle_array2, grid, sorted_pop), frames=range(frames+1), interval=1)
        anim.save('p_i_bus_output.gif', writer='ffmpeg')
        plt.close()

    elif version.lower() in ['iv', 'vi']:

        rectangle_array = []
        rectangle_array2 = []

        fig, ax = plt.subplots(1,2)
        ax[0].set_xlim((0, grid.num_col))
        ax[0].set_ylim((0, grid.num_row))
        ax[0].set_aspect('equal')

        ax[1].set_xlim((0,grid.num_col))
        ax[1].set_ylim((0,grid.num_row))
        ax[1].set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[0].add_artist(a)
            rectangle_array.append(a)

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[1].add_artist(a)
            rectangle_array2.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_double_vi(i, rectangle_array, rectangle_array2, grid, sorted_pop, ceiling_height, viab_vir, sus_population), frames=range(frames+1), interval=1)
        anim.save('v_i_bus_output.gif', writer='ffmpeg')
        plt.close()

    elif version.lower() in ['a']:
        rectangle_array = []
        rectangle_array2 = []
        rectangle_array3 = []
        rectangle_array4 = []

        fig, ax = plt.subplots(2, 2)
        ax[0, 0].set_xlim((0, grid.num_col))
        ax[0, 0].set_ylim((0, grid.num_row))
        ax[0, 0].set_aspect('equal')

        ax[1, 0].set_xlim((0, grid.num_col))
        ax[1, 0].set_ylim((0, grid.num_row))
        ax[1, 0].set_aspect('equal')

        ax[0, 1].set_xlim((0, grid.num_col))
        ax[0, 1].set_ylim((0, grid.num_row))
        ax[0, 1].set_aspect('equal')

        ax[1, 1].set_xlim((0, grid.num_col))
        ax[1, 1].set_ylim((0, grid.num_row))
        ax[1, 1].set_aspect('equal')

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[0, 0].add_artist(a)
            rectangle_array.append(a)

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[1, 0].add_artist(a)
            rectangle_array2.append(a)

        for Cell in grid.cell_list:
            if Cell.wall:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='#000000')
            else:
                a = mpatch.Rectangle((Cell.name % grid.num_col, Cell.name // grid.num_col), 1, 1, color='b')
            ax[0, 1].add_artist(a)
            rectangle_array3.append(a)

        anim = animation.FuncAnimation(fig, lambda i: animate2.animate_all(i, frames, rectangle_array, rectangle_array2, rectangle_array3, rectangle_array4, grid, ceiling_height, ax, viab_vir, sus_population, infected_population,  minutes_per_frame), frames=range(frames+1), interval=1, repeat=False)
        anim.save('all_bus_output.mp4', writer='ffmpeg')
        # plt.close()

        return grid

    elif version.lower() in ['h']:  # headless
        cell_infect_count = []
        overall_infect_count = 0
        for i in range(frames):
            overall_infect_count = animate2.all_headless(i, frames, grid, viab_vir, cell_infect_count, overall_infect_count, sus_population, infected_population, minutes_per_frame, cough, sneeze, talk)

        return cell_infect_count, overall_infect_count


def Sim_Var_Inf(index=36): # Normal Simulation with varying infection rates, use this to get output with infection distribution
    loops = 10
    cell_infect_agg = np.zeros(shape=(loops, 70))
    overall_infect_avg = []
    for i in range(loops):
        cell_infect_count, overall_infect_count = Simulate(0, 0, 0, 60, 20, 'h')
        overall_infect_avg.append(overall_infect_count)
        cic = np.asarray(cell_infect_count)
        cell_infect_agg[i] = cic

    grid = env.Grid(12 + 2, 3 + 2, 1)
    grid.Create_Grid()

    fig, ax = plt.subplots()
    ax.set_xlim((0, grid.num_col))
    ax.set_ylim((0, grid.num_row))
    ax.set_aspect('equal')

    cell_infect_avg = np.mean(cell_infect_agg, axis=0)
    cell_avg = np.ndarray.flatten(cell_infect_avg)
    ovr_infect_avg = np.average(overall_infect_avg)
    print(ovr_infect_avg)

    for cell in grid.cell_list:
        cell.infected_count = round(cell_avg[cell.name], 2)

    grid.cell_color_pre_infected_single(ax, [grid.cell_list[index]])
    plt.savefig('Infection_Rates_60ACH_20Fil_Runs1000_IndCell36_BackFil4')


def Sim_Var_Cough(): # simulation for different cough probabilities per frame
    loops = 1000
    infection_percentages = []
    max_coughs = 21
    for k in range(max_coughs):
        print(k)
        overall_infect_avg = []
        for i in range(loops):
            print(i)
            cell_infect_count, overall_infect_count = Simulate(k/100, 0, 0, 60, 20, 'h')
            overall_infect_avg.append(overall_infect_count)
        ovr_infect_avg = np.average(overall_infect_avg)
        infection_percentages.append(ovr_infect_avg)

    x = range(max_coughs)
    plt.plot(x, infection_percentages)
    plt.xlabel('Number of Coughs')
    plt.ylabel('Infection Percentage')
    plt.title('Coughs Vs. Infections')
    plt.savefig('Sensitivity_Analysis_Bus_Variable_Cough')

def Sim_Var_Sneeze(): # simulation for different sneeze probabilities per frame
    loops = 1000
    infection_percentages = []
    max_sneezes = 11
    for k in range(max_sneezes):
        overall_infect_avg = []
        for i in range(loops):
            cell_infect_count, overall_infect_count = Simulate(0, k/100, 0, 60, 20, 'h')
            overall_infect_avg.append(overall_infect_count)
        ovr_infect_avg = np.average(overall_infect_avg)
        infection_percentages.append(ovr_infect_avg)

    x = range(max_sneezes)
    plt.plot(x, infection_percentages)
    plt.xlabel('Number of Sneezes')
    plt.ylabel('Infection Percentage')
    plt.title('Sneezes Vs. Infections')
    plt.savefig('Sensitivity_Analysis_Bus_Variable_Sneeze')

def Sim_Var_Talk(): # Simulation for different talk probabilities per frame
    loops = 1000
    infection_percentages = []
    talk_prob = 101
    for k in range(0, talk_prob, 5):
        overall_infect_avg = []
        for i in range(loops):
            cell_infect_count, overall_infect_count = Simulate(0, 0, k/100, 60, 20, 'h')
            overall_infect_avg.append(overall_infect_count)
        ovr_infect_avg = np.average(overall_infect_avg)
        infection_percentages.append(ovr_infect_avg)

    x = range(0, talk_prob, 5)
    plt.plot(x, infection_percentages)
    plt.xlabel('Minutes Spoken')
    plt.ylabel('Infection Percentage')
    plt.title('Minutes Spoken Vs. Infections')
    plt.savefig('Sensitivity_Analysis_Bus_Variable_Talk')



def Sim_Var_Filt(): # Simulation for differing filtration percentages
    loops = 1000
    fil_rate_max = 40
    infection_percentages = []
    for k in range(fil_rate_max):
        overall_infect_avg = []
        for i in range(loops):
            cell_infect_count, overall_infect_count = Simulate(.1, 0, 0, 60, k, 'h')
            overall_infect_avg.append(overall_infect_count)
        ovr_infect_avg = np.average(overall_infect_avg)
        infection_percentages.append(ovr_infect_avg)

    x = range(fil_rate_max)
    plt.plot(x, infection_percentages)
    plt.xlabel('Filtration')
    plt.ylabel('Infection Percentage')
    plt.title('Filtration Vs. Infections')
    plt.savefig('Sensitivity_Analysis_Bus_Variable_Filtration')


def Sim_Var_ACH():  # Simulation for different ACH values
    loops = 1000
    max_ACH = 60
    infection_percentages = []

    for k in range(4, max_ACH+1, 4):
        overall_infect_avg = []
        for i in range(loops):
            cell_infect_count, overall_infect_count = Simulate(.1, 0, 0, k, 20, 'h')
            overall_infect_avg.append(overall_infect_count)
        ovr_infect_avg = np.average(overall_infect_avg)
        infection_percentages.append(ovr_infect_avg)

    x = range(4, max_ACH+1, 4)
    plt.plot(x, infection_percentages)
    plt.xlabel('ACH')
    plt.ylabel('Infection Percentage')
    plt.title('ACH Vs. Infections')
    plt.savefig('Sensitivity_Analysis_Bus_Variable_ACH')

