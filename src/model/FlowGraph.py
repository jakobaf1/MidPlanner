from Edge import Edge
from Employee import Employee
from Shift import Shift
from Vertex import Vertex
from Preference import Preference
from datetime import datetime


class FlowGraph:
    
    source = Vertex(purpose = 0, name = "s")
    sink = Vertex(purpose = 7, name = "t")
    shared_nodes = [] # remove eventually, just for debugging now

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
                    layer_6_node = Vertex(department=1, time_of_day=0, purpose= 6, name= f"{dep}_{time}")
                    # link it to the sink
                    add_edge(layer_6_node, flow_graph.sink, 6*8)

                    for exp in range(2): # experience level loop
                        layer_5_node = Vertex(department=dep, time_of_day=time, experience=exp+1, purpose= 5, name= f"{time}_{dep}_{exp}") 
                        add_edge(layer_5_node, layer_6_node, (6-exp)*8)

                        # add to the array for the day after all the links between the final part of the graph are connected
                        # TODO Concern: don't think the edge made in exp=2 is visible, from the perspective of the edge where exp=1, in the final graph 
                        daily_shared_nodes.append(layer_5_node)

            # after making the array containing combinations i link it to the overall array
            shared_nodes.append(daily_shared_nodes[:])
        flow_graph.shared_nodes = shared_nodes[:]

        emp_num = 1
        # make employee nodes + edges
        for e in flow_graph.employees:
            emp_node = Vertex(purpose = 1, employee = e, name= f"E{emp_num}")
            add_edge(flow_graph.source, emp_node, 8*e.weekly_hrs)

            # for the first day there are no intermediate nodes so they are defined here
            day_node = Vertex(day = 0, purpose= 2, name= "day_1")
            add_edge(emp_node, day_node, 16)

            # define the list for intermediate nodes which the shifts are to be linked
            next_intermediate_nodes = [Vertex(purpose=3, name="day_2_1"), Vertex(purpose=3, name="day_2_2"), Vertex(purpose=3, name="day_2_3")]

            for s in flow_graph.shifts:
                shift_node = Vertex(day= 0, shift= s, purpose=4, name=f"{s.start_time}-{s.end_time}")
                add_edge(day_node, shift_node, s.calc_hours()+4)
                
                exp_lvl = e.exp_lvl
                # link to the correct node(s)
                # TODO this can be made into a function for reproducability
                # TODO should actually just be combined with the for loop
                # Since someone might have the first day of scheduling off, all days follow same pattern
                match s.start_time:
                    case 7:
                        for dep in range(len(e.departments)): # for loop in case employee is in multiple departments
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1], 8)
                            
                            # adds the 4 hours extra from a 12 hour shift to the evening
                            if s.calc_hours == 12:
                                # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 4, lower_bound=4)

                            # add the edge the the node representing the 11 hour break
                        add_edge(shift_node, next_intermediate_nodes[0], 4, lower_bound=4, must_take=True)

                    case 15:
                        for dep in range(len(e.departments)):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 8)

                        add_edge(shift_node, next_intermediate_nodes[1], 4, lower_bound=4, must_take=True)

                    case 19:
                        for dep in range(len(e.departments)):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+4], 8)

                            # adds the 4 hours extra from a 12 hour shift to the evening
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            
                        add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)

                    case 23:
                        for dep in range(len(e.departments)):
                            add_edge(shift_node, shared_nodes[0][6*dep+exp_lvl-1+4], 8)
                        add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)


            # make the graph for each day for the employee "e"
            for day in range(1, 2): # TODO temporarily set to 2 days for printing purposes
                # This should start with a works_day(day) function for checking whether they should be off on this day
                # TODO remember to also account for the intermediate nodes so they are reset
                # if not(works_day()): last_day_off = True; continue
                day_node = Vertex(day = day, purpose= 2, name=f"day_{day+1}")
                add_edge(emp_node, day_node, 12)
                prev_intermediate_nodes = next_intermediate_nodes[:] # have to define the intermediate nodes here, as they are to be used in current day and next day
                next_intermediate_nodes =  [Vertex(purpose=3, name=f"day_{day+1}_1"), Vertex(purpose=3, name=f"day_{day+1}_2"), Vertex(purpose=3, name=f"day_{day+1}_3")]

                # add edges from day to intermediate nodes
                # if not(last_day_off):
                for i in range(3):
                    add_edge(day_node, next_intermediate_nodes[i], 12)
                

                for s in flow_graph.shifts:
                    shift_node = Vertex(day= day, shift= s, purpose=4, name=f"{s.start_time}-{s.end_time}")
                    # TODO here it should lead to the solution where day is linked directly (e.g. situation above for loop with day 0)
                    # if last_day_off:
                    # add_edge(day_node, shift_node, s.calc_hours()+4)
                    
                    exp_lvl = e.exp_lvl
                    # link to the correct node(s)
                    match s.start_time:
                        case 7:
                            # if not(last_day_off):
                            add_edge(prev_intermediate_nodes[0], shift_node, 12)
                            for dep in range(len(e.departments)): # for loop in case employee is in multiple departments
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
                            for dep in range(len(e.departments)):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 8)
                            add_edge(shift_node, next_intermediate_nodes[1], 4, lower_bound=4, must_take=True)

                        case 19:
                            for i in range(3):
                                add_edge(prev_intermediate_nodes[i], shift_node, 12)
                            for dep in range(len(e.departments)):
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
                            for dep in range(len(e.departments)):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8)
                            add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4, must_take=True)

            emp_num += 1



                                
def add_edge(frm, to, cap, back=0, w=0, lower_bound=0, must_take=False):
    new_edge = Edge(frm, to, cap, back, w, lower_bound, must_take)
    frm.add_out_going(new_edge)
    to.add_in_going(new_edge)

def what_day_is_it(day: int):
        # used to find out what day it is. 
        # first what date, and then if that date is weekend or holiday etc.
        return

def print_graph_part(fg):
    s = ""
    start_node = fg.source

    for i in range(6):
        s += str(start_node.out_going[0])
        s += ", "
        start_node = start_node.out_going[0].to
    
    print(s)

def print_graph_list(fg):
    s = ""
    for i in range(len(fg.shared_nodes)):
        s += f"{i+1}: "
        for j in range(len(fg.shared_nodes[0])):
            s += f"[{fg.shared_nodes[i][j]}]"
        s += "\n"
    print(s)

def print_graph_bfs(fg):
    queue = []
    visited = []
    visited.append(fg.source)

    queue.append(fg.source)

    while queue:
        node = queue.pop(0)

        for i in range(len(node.out_going)):
            new_node = node.out_going[i].to
            if visited.count(new_node) <= 0:
                print(node.out_going[i])
                queue.append(new_node)

def print_employees(fg):
    for e in fg.source.out_going:
        print(e.to.employee)

# will be in another place later, but can serve its purpose here for now
def read_employee_file() -> list[Employee]:
    in_dir = '../../data/'
    file_name = 'employees.txt'
    file = open(in_dir+file_name, 'r')
    lines = file.readlines()
    file.close()

    emp_list = []

    for i in range(len(lines)):
        if '#' in lines[i]: continue
        if 'Employee:' in lines[i]:
            name = lines[i][10:]
            id = lines[i+1][4:]
            dep = []
            if 'labor' in lines[i+2]:
                dep.append(0)
            if 'maternity' in lines[i+2]:
                dep.append(1)
            hrs = int(lines[i+3][7:])
            exp = int(lines[i+4][12:])

            # For reading preferences
            # should maybe make a preference object outside the coming loop
            # and then set the values accordingly based on match cases
            # for j in range(i+5, len(lines)):
            #     if 'is_wanted:' in lines[j]:
            #         if 'yes' in lines[j]:
            #             pref.wanted = True
            #         else:
            #             pref.wanted = False
            #     if ',' in lines[j]:
            #       pref_list.append(pref)
            #       pref = Preference()     
            # 

            emp_list.append(Employee(name=name.strip(), id=id.strip(), departments=dep, weekly_hrs=hrs, exp_lvl=exp)) # add preferences when imlemented

    return emp_list
    



def main():
    start_date = datetime.now()
    fg = FlowGraph([Shift(7, 15, 0), Shift(15, 23, 0)], read_employee_file())
    generate_graph(fg, start_date)
    print_employees(fg)

if __name__ == "__main__":
        main()