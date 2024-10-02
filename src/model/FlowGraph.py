from Edge import Edge
from Employee import Employee
from Shift import Shift
from Vertex import Vertex
from Preference import Preference
from datetime import datetime


class FlowGraph:
    
    source = Vertex(purpose = 0)
    sink = Vertex(purpose = 7)

    # could add a start_date variable, so one can make the schedule from a day in the future
    def __init__(self, shifts: list[Shift], employees: list[Employee]):
        self.shifts = shifts
        self.employees = employees
        
    
def generate_graph(flow_graph, start_date):

        # initializes day, day of week and month. Used to relate to calendar
        day = start_date.day
        day_of_week = start_date.weekday
        month = start_date.month

        shared_nodes = [] # nodes denoting time_of_day/department/exp_lvl

        # I make the final columns of the graph for each day
        for day in range(56):
            daily_shared_nodes = []

            # I encode the departments as 0: labor, 1: maternity
            # the time of day is 0: day, 1: evening, 2: night
            for dep in range(2): # department loop
                for time in range(3): # time of day loop
                    # this node signifies the 2nd last layer: dep_time
                    layer_6_node = Vertex(department=1, time_of_day=0, purpose= 6)
                    # link it to the sink
                    add_edge(layer_6_node, flow_graph.sink, 6*8)

                    for exp in range(2): # experience level loop
                        layer_5_node = Vertex(department=dep, time_of_day=time, experience=exp+1, purpose= 5) 
                        add_edge(layer_5_node, layer_6_node, (6-exp)*8)

                        # add to the array for the day after all the links between the final part of the graph are connected
                        # TODO Concern: don't think the edge made in exp=2 is visible, from the perspective of the edge where exp=1, in the final graph 
                        daily_shared_nodes.append(layer_5_node)

            # after making the array containing combinations i link it to the overall array
            shared_nodes.append(daily_shared_nodes)


        # make employee nodes + edges
        for e in flow_graph.employees:
            emp_node = Vertex(purpose = 1, employee = e)
            add_edge(flow_graph.source, emp_node, 8*e.weekly_hrs)

            # for the first day there are no intermediate nodes so they are defined here
            day_node = Vertex(day = 0, purpose= 2)
            add_edge(emp_node, day_node, 12)

            # define the list for intermediate nodes which the shifts are to be linked
            next_intermediate_nodes = [Vertex(purpose=3), Vertex(purpose=3), Vertex(purpose=3)]

            for s in flow_graph.shifts:
                shift_node = Vertex(day= 0, shift= s, purpose=4)
                add_edge(day_node, shift_node, s.calc_hours()+4)
                
                exp_lvl = e.exp_level
                # link to the correct node(s)
                # TODO this can be made into a function for reproducability
                # TODO should actually just be combined with the for loop
                # Since someone might have the first day of scheduling off, all days follow same pattern
                match s.start_time:
                    case 7:
                        for dep in len(e.departments): # for loop in case employee is in multiple departments
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1], 8)
                            
                            # adds the 4 hours extra from a 12 hour shift to the evening
                            if s.calc_hours == 12:
                                # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 4, lower_bound=4)

                            # add the edge the the node representing the 11 hour break
                        add_edge(shift_node, next_intermediate_nodes[0], 4, lower_bound=4, must_take=True)

                    case 15:
                        for dep in len(e.departments):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 8)

                        add_edge(shift_node, next_intermediate_nodes[1], 4, lower_bound=4, must_take=True)

                    case 19:
                        for dep in len(e.departments):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+4], 8)

                            # adds the 4 hours extra from a 12 hour shift to the evening
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            
                        add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)

                    case 23:
                        for dep in len(e.departments):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+4], 8)
                        add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)


            # make the graph for each day for the employee "e"
            for day in range(1, 56):
                # This should start with a works_day(day) function for checking whether they should be off on this day
                # TODO remember to also account for the intermediate nodes so they are reset
                # if not(works_day()): last_day_off = True; continue
                day_node = Vertex(day = day, purpose= 2)
                add_edge(emp_node, day_node, 12)
                prev_intermediate_nodes = next_intermediate_nodes # have to define the intermediate nodes here, as they are to be used in current day and next day
                next_intermediate_nodes =  [Vertex(purpose=3), Vertex(purpose=3), Vertex(purpose=3)]

                # add edges from day to intermediate nodes
                # if not(last_day_off):
                for i in range(3):
                    add_edge(day_node, next_intermediate_nodes[i])
                

                for s in flow_graph.shifts:
                    shift_node = Vertex(day= day, shift= s, purpose=4)
                    # TODO here it should lead to the solution where day is linked directly (e.g. situation above for loop with day 0)
                    # if last_day_off:
                    # add_edge(day_node, shift_node, s.calc_hours()+4)
                    
                    exp_lvl = e.exp_level
                    # link to the correct node(s)
                    match s.start_time:
                        case 7:
                            # if not(last_day_off):
                            add_edge(prev_intermediate_nodes[0], shift_node, 12)
                            for dep in len(e.departments): # for loop in case employee is in multiple departments
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1], 8)
                                
                                # adds the 4 hours extra from a 12 hour shift to the evening
                                if s.calc_hours == 12:
                                    # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                    # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                    add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            add_edge(shift_node, next_intermediate_nodes[0], 4, lower_bound=4, must_take=True)

                        case 15:
                            # if not(last_day_off):
                            for i in range(2):
                                add_edge(prev_intermediate_nodes[i], shift_node, 12)
                            for dep in len(e.departments):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 8)
                            add_edge(shift_node, next_intermediate_nodes[1], 4, lower_bound=4, must_take=True)

                        case 19:
                            for i in range(3):
                                add_edge(prev_intermediate_nodes[i], shift_node, 12)
                            for dep in len(e.departments):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8)
                                
                                # adds the 4 hours extra from a 12 hour shift to the evening
                                if s.calc_hours == 12:
                                    # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                    # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                    add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)

                        case 23:
                            for i in range(3):
                                add_edge(prev_intermediate_nodes[i], shift_node, 12)
                            for dep in len(e.departments):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8)
                            add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)



                                
def add_edge(frm, to, cap, back=0, w=0, low=0, must=False):
    new_edge = Edge(frm, to, cap, back, w, low, must)
    frm.add_out_going(new_edge)
    to.add_in_going(new_edge)

def what_day_is_it(day: int):
        # used to find out what day it is. 
        # first what date, and then if that date is weekend or holiday etc.
        return

def main():
    start_date = datetime.now()
    generate_graph(FlowGraph([],[]), start_date)
    v1 = Vertex(purpose=1)
    v2 = Vertex(purpose=2)
    print(v1.out_going[0])
    add_edge(v1, v2, 8)
    v1.out_going[0].add_flow(6)
    print(v1.out_going[0])

if __name__ == "__main__":
        main()