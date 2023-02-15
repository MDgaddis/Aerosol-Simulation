##/opt/homebrew/bin/python3.9
#!/usr/bin/env python3

import AvgAgentBackground as agent


def animate_single_people_move(frame_count, minutes_per_frame, rectangle_array, grid, sorted_pop):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     # Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(minutes_per_frame, grid)                  # Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)


def animate_single_people(frame_count, rectangle_array, grid):

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  # Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)


def virion_movement_german(frame_count, frames, rectangle_array, grid, ceiling_height, viab_vir, pop, pop_spawned, minutes_per_frame):
    filtered_virions = 0
    grid.spawn_people(frame_count, pop)

    for pi in pop:
        if pi.Spawned is False:
            if pi.arrival_time < frame_count:
                pi.Spawned = True
                pop_spawned.append(pi)
        if pi.Spawned is True and pi in pop_spawned:
            if pi.arrival_time + pi.time_stayed < frame_count:
                pi.Exiting = True
                pop_spawned.remove(pi)
                if pi.__class__ is agent.Susceptible:
                    pi.Prob_of_Infection()

    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)
        Cell.move_people(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:                     # Transfer transient states to active states and color cells last
        Cell.transient_states()
        Cell.cell_colors_virions(rectangle_array, ceiling_height, viab_vir)

    if frame_count == frames-1:  # check who became infected
        infect_count = 0
        for pi in pop:
            if pi.__class__ is agent.Infected_Pre_Infectious:
                infect_count += 1

        return infect_count


def animate_single_virions(frame_count, frames, rectangle_array, grid, ceiling_height, minutes_per_frame, viab_vir, sus_population):
    filtered_virions = 0
    # print(grid.cell_list[63].filtered_virions)
    # print(grid.cell_list[63].virions)
    # print(grid.cell_list[63].transient_vir)
    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_virions(rectangle_array, ceiling_height, viab_vir)

    if frame_count == frames:  # In Bus scenario, since no one enters or exits, when time is up check everyone for infection
        infect_count = 0
        for cell in grid.cell_list:
            for person in cell.population:
                if person.__class__ is agent.Susceptible:
                    person.Prob_of_Infection()
                    if person.__class__ is agent.Infected_Pre_Infectious:
                        cell.infected_count += 1
                        infect_count += 1
        print(infect_count/sus_population)


def animate_single_infected_move(frame_count, rectangle_array,grid,sorted_pop):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     ## Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_infected(rectangle_array)


def animate_single_infected(frame_count, rectangle_array, grid):
    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_infected(rectangle_array)


def animate_double_pi_move(frame_count, rectangle_array, rectangle_array2, grid, sorted_pop):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     ## Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_infected(rectangle_array2)


def animate_double_pi(frame_count, rectangle_array, rectangle_array2, grid):

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_infected(rectangle_array2)


def animate_double_pv_move(frame_count, rectangle_array, rectangle_array2, grid, sorted_pop, ceiling_height):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     ## Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_virions(rectangle_array2, ceiling_height)


def pv_movement_german(frame_count, frames, rectangle_array, rectangle_array2, grid, pop, ceiling_height, minutes_per_frame, viab_vir):
    filtered_virions = 0
    print(frame_count)
    grid.spawn_people(frame_count, pop)

    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:                     # Transfer transient states to active states and color cells last
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_virions(rectangle_array2, ceiling_height, frames)

    if frame_count == frames-1:  # check who became infected
        infect_count = 0
        for pi in pop:
            if pi.__class__ is agent.Infected_Pre_Infectious:
                infect_count += 1

        return infect_count


def animate_double_pv(frame_count, frames, rectangle_array, rectangle_array2, grid, ceiling_height):

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_virions(rectangle_array2, ceiling_height)


def animate_double_vi_move(frame_count, rectangle_array, rectangle_array2, grid, sorted_pop, ceiling_height):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     ## Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_virions(rectangle_array, ceiling_height)
        Cell.cell_colors_infected(rectangle_array2)


def animate_double_vi(frame_count, rectangle_array, rectangle_array2, grid, ceiling_height):
    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:
        Cell.transient_states()
        Cell.cell_colors_virions(rectangle_array, ceiling_height)
        Cell.cell_colors_infected(rectangle_array2)


def animate_all_move(frame_count, rectangle_array, rectangle_array2, rectangle_array3, rectangle_array4, grid, sorted_pop, ceiling_height):
    grid.spawn_people(frame_count, sorted_pop)

    for Cell in grid.cell_list:                     ## Do stuff with moving people 1st
        Cell.despawn_person(frame_count)
        Cell.move_people(grid)

    for Cell in grid.cell_list:                     ## Do stuff with moving virions 2nd
        Cell.spread_virions(grid)
        Cell.breathe_virions(grid)                  ## Spread them, then breathe them. Not sure, may end up putting at front

    for Cell in grid.cell_list:                     ## Transfer transient states to active states and color cells last
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_virions(rectangle_array2,ceiling_height)
        Cell.cell_colors_infected(rectangle_array3)
        Cell.cell_colors_people(rectangle_array4)


def animate_all(frame_count, frames, rectangle_array, rectangle_array2, rectangle_array3, rectangle_array4, grid, ceiling_height, ax, viab_vir, sus_population, inf_pop, minutes_per_frame):
    filtered_virions = 0

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:                     # Transfer transient states to active states and color cells last
        Cell.transient_states()
        Cell.cell_colors_people(rectangle_array)
        Cell.cell_colors_virions(rectangle_array2, ceiling_height, viab_vir)
        Cell.cell_colors_infected(rectangle_array3)

    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    if frame_count == frames:  # In Bus scenario, since no one enters or exits, when time is up check everyone for infection
        infect_count = 0
        for cell in grid.cell_list:
            for person in cell.population:
                if person.__class__ is agent.Infected:
                    cell.infected_count += 1
                    infect_count += 1
                if person.__class__ is agent.Susceptible:
                    person.Prob_of_Infection()
                    if person.__class__ is agent.Infected_Pre_Infectious:
                        cell.infected_count += 1
                        infect_count += 1
        grid.cell_color_pre_infected(ax)
        print(infect_count/(sus_population + inf_pop))


def all_headless(frame_count, frames, grid, viab_vir, cell_infect_count, overall_infect_count, sus_population, inf_pop, minutes_per_frame, cough, sneeze, talk):
    filtered_virions = 0

    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    # for cell in grid.vent_inlet_cells:
    #     filtered_virions += cell.virions*(1-(cell.filtration_percentage/100))
    #     cell.virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, cough, sneeze, talk, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:                     # Transfer transient states to active states and color cells last
        Cell.transient_states()

    if frame_count == frames-1:  # In Bus scenario, since no one enters or exits, when time is up check everyone for infection
        infect_count = 0
        for cell in grid.cell_list:
            for person in cell.population:
                if person.__class__ is agent.Infected:
                    cell.infected_count += 1
                    infect_count += 1
                if person.__class__ is agent.Susceptible:
                    person.Prob_of_Infection()
                    if person.__class__ is agent.Infected_Pre_Infectious:
                        cell.infected_count += 1
                        infect_count += 1
            cell_infect_count.append(cell.infected_count)
        overall_infect_count = infect_count/(sus_population + inf_pop)

    return overall_infect_count


def all_headless_movement_german(frame_count, frames, grid, viab_vir, pop, pop_spawned, minutes_per_frame):
    filtered_virions = 0
    grid.spawn_people(frame_count, pop)

    for pi in pop:
        if pi.Spawned is False:
            if pi.arrival_time < frame_count:
                pi.Spawned = True
                pop_spawned.append(pi)
        if pi.Spawned is True and pi in pop_spawned:
            if pi.arrival_time + pi.time_stayed < frame_count:
                pi.Exiting = True
                pop_spawned.remove(pi)
                if pi.__class__ is agent.Susceptible:
                    pi.Prob_of_Infection()

    print(pop_spawned)

    for Cell in grid.cell_list:
        Cell.breathe_virions(minutes_per_frame, grid)

    for Cell in grid.cell_list:
        Cell.flow_move_virions(grid)
        Cell.move_people(grid)

    for cell in grid.vent_inlet_cells:
        for adj in cell.adjacent_cells:
            filtered_virions += grid.cell_list[adj].virions*(1-(cell.filtration_percentage/100))
            grid.cell_list[adj].virions = 0

    for Cell in grid.vent_outlet_cells:
        Cell.return_filtered_virions(filtered_virions, frame_count, grid)

    for Cell in grid.cell_list:                     # Do stuff with moving virions 2nd
        Cell.spread_virions(grid, minutes_per_frame, viab_vir)

    for Cell in grid.cell_list:                     # Transfer transient states to active states and color cells last
        Cell.transient_states()

    if frame_count == frames-1:  # check who became infected
        infect_count = 0
        for pi in pop:
            if pi.__class__ is agent.Infected_Pre_Infectious:
                infect_count += 1

        return infect_count
