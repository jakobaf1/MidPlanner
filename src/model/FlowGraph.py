import time
from numpy import inf
from Edge import Edge
from Employee import Employee
from Shift import Shift
from Vertex import Vertex
from Preference import Preference
from datetime import datetime, timedelta
from Algorithms import Algorithms


class FlowGraph:

    period_in_weeks = 8
    days_in_period = period_in_weeks*7
    source = Vertex(purpose = 0, name = "s")
    sink = Vertex(purpose = 7, name = "t")
    shared_nodes = [] # remove as field eventually, just for debugging now

    # could add a start_date variable, so one can make the schedule from a day in the future
    def __init__(self, shifts: list[Shift], employees: list[Employee]):
        self.shifts = shifts
        self.employees = employees
        
    
def generate_graph(flow_graph, start_date):

        # initializes day, day of week and month. Used to relate to calendar
        date = start_date

        shared_nodes = [] # nodes denoting time_of_day/department/exp_lvl

        # I make the final columns of the graph for each day
        for day in range(flow_graph.days_in_period):
            daily_shared_nodes = []

            # I encode the departments as 0: labor, 1: maternity
            # the time of day is 0: day, 1: evening, 2: night
            for dep in range(2): # department loop
                for time in range(3): # time of day loop
                    # this node signifies the 2nd last layer: dep_time
                    layer_6_node = Vertex(department=1, time_of_day=0, purpose= 6, name= f"{dep}_{time}_{day}")
                    # link it to the sink
                    if time == 0:
                        add_edge(layer_6_node, flow_graph.sink, 6*8) #day needs 6 workers
                    else:
                        add_edge(layer_6_node, flow_graph.sink, 4*8) # eve/night needs 4 workers

                    for exp in range(2): # experience level loop
                        layer_5_node = Vertex(department=dep, time_of_day=time, experience=exp+1, purpose= 5, name= f"{time}_{dep}_{exp}") 
                        if time == 0:
                            add_edge(layer_5_node, layer_6_node, (6-exp)*8)
                        else:
                            add_edge(layer_5_node, layer_6_node, (4-exp)*8)

                        # add to the array for the day after all the links between the final part of the graph are connected
                        daily_shared_nodes.append(layer_5_node)

            # after making the array containing combinations i link it to the overall array
            shared_nodes.append(daily_shared_nodes[:])
        flow_graph.shared_nodes = shared_nodes[:]

        # make employee nodes + edges
        for e in flow_graph.employees:
            # reset the date for the employee
            date = start_date
            # create a boolean to keep track of which days the employee can work based on preferences
            last_day_off = True
            # create the node for the employee
            emp_node = Vertex(purpose = 1, employee = e, name= e.name)
            add_edge(flow_graph.source, emp_node, flow_graph.period_in_weeks*e.weekly_hrs)

            # I define lists of preferences based on the day and shift
            day_preferences = pref_days(e, date, flow_graph.days_in_period)
            shift_preferences  = pref_shifts(e,date, flow_graph.days_in_period)

            # define the list for intermediate nodes which the shifts are to be linked
            # next_intermediate_nodes = [Vertex(purpose=3, name="day_1_1"), Vertex(purpose=3, name="day_1_2"), Vertex(purpose=3, name="day_1_3")]

            # make the graph for each day for the employee "e"
            for day in range(flow_graph.days_in_period):
                # Weekday lets the program know what day it is
                weekday = date.weekday()
                # checking whether they should be off on this day
                shift_pref = False
                # checks whether there are any shift preferences on the current day
                if shift_preferences[day]:
                    shift_pref = True

                w = set_day_weight(day_preferences[day])
                # if the employee is required not to work this day, day is skipped
                if w == float("Inf"):
                    last_day_off = True
                    wd = weekday_to_str(weekday+1)
                    # next_intermediate_nodes =  [Vertex(purpose=3, name=f"day_{wd}_1"), Vertex(purpose=3, name=f"day_{wd}_2"), Vertex(purpose=3, name=f"day_{weekday_to_str(wd)}_3")]
                    date += timedelta(days=1)
                    # print(f"{e} took day {weekday} off")
                    continue

                day_node = Vertex(day = day, purpose= 2, name=f"{weekday_to_str(weekday)}_day_{day}")
                if not(shift_pref):
                    add_edge(emp_node, day_node, 12, w=w)
                else:
                    add_edge(emp_node, day_node, 12) # TODO have to make sure this is only 8 if the next day is a day off
                # have to define the intermediate nodes here, as they are to be used in current day and next day
                # prev_intermediate_nodes = next_intermediate_nodes[:]
                # next_intermediate_nodes =  [Vertex(purpose=3, name=f"{weekday_to_str(weekday+1)}_day_{day+1}_1"), Vertex(purpose=3, name=f"{weekday_to_str(weekday+1)}_day_{day+1}_2"), Vertex(purpose=3, name=f"{weekday_to_str(weekday+1)}_day_{day+1}_3")]

                # add edges from day to intermediate nodes
                # if not(last_day_off):
                #     for i in range(3):
                #         add_edge(day_node, prev_intermediate_nodes[i], 12)
                

                for s in flow_graph.shifts:
                    # find the weight appropriate for the shift
                    w_s = 0
                    if shift_pref:
                        w_s = set_shift_weight(shift_preferences[day], s)
                    if w_s == float("Inf"):
                        continue
                    shift_node = Vertex(day= day, shift= s, purpose=4, name=f"{s.start_time}-{s.end_time}")
                        # print(f"just set weight to: {w_s}")
                    # if last_day_off:
                        # add_edge(day_node, shift_node, s.calc_hours()+4, w=w_s, lower_bound=s.calc_hours())
                    add_edge(day_node, shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours())
                    # print(f"1: just set edge with weight: {w_s} on day: {date.weekday()}")
                    
                    exp_lvl = e.exp_lvl
                    # link to the correct node(s)
                    match s.start_time:
                        case 0:
                            # need to implement that 14 hours go from source, and somehow 24 end up at the sink :)
                            # if not(last_day_off):
                            #     add_edge(prev_intermediate_nodes[0], shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours()) # TODO this need to be 16 on the first day after a day off
                            for dep in range(len(e.departments)): # for loop in case employee is in multiple departments
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1], 8, lower_bound=8) # TODO this needs to be 12 on first day after a day off
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 8, lower_bound=8) # TODO this needs to be 12 on first day after a day off
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8, lower_bound=8) # TODO this needs to be 12 on first day after a day off
                            # add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4)
                        case 7:
                            # if not(last_day_off):
                            #     add_edge(prev_intermediate_nodes[0], shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours()) # TODO this need to be 16 on the first day after a day off
                            for dep in range(len(e.departments)): # for loop in case employee is in multiple departments
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1], 8, lower_bound=8) # TODO this needs to be 12 on first day after a day off
                                
                                # adds the 4 hours extra from a 12 hour shift to the evening
                                if s.calc_hours == 12:
                                    # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                    # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                    add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            # add_edge(shift_node, next_intermediate_nodes[0], 4, lower_bound=4)

                        case 15:
                            # if not(last_day_off):
                                # for i in range(2):
                                #     add_edge(prev_intermediate_nodes[i], shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours())
                            for dep in range(len(e.departments)):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 8, lower_bound=8)
                            # add_edge(shift_node, next_intermediate_nodes[1], 4, lower_bound=4)

                        case 19:
                            # if not(last_day_off):
                            #     for i in range(3):
                            #         add_edge(prev_intermediate_nodes[i], shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours())
                            for dep in range(len(e.departments)):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8, lower_bound=8)
                                # have to figure out how I will handle the splits from 12 hours. maybe add a minimum and maximum amount one can send through
                                # if I add a min and max of 4 hours, then there can only be sent 4 hours through here (which is what's supposed to happen)
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+2], 4, lower_bound=4)
                            # add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4)

                        case 23:
                            # if not(last_day_off):
                            #     for i in range(3):
                            #         add_edge(prev_intermediate_nodes[i], shift_node, s.calc_hours(), w=w_s, lower_bound=s.calc_hours())
                            for dep in range(len(e.departments)):
                                add_edge(shift_node, shared_nodes[day][6*dep+exp_lvl-1+4], 8, lower_bound=8)
                            # add_edge(shift_node, next_intermediate_nodes[2], 4, lower_bound=4)
                
                # print(f"finished for day {date}")
                date += timedelta(days=1)
                last_day_off = False



### Helper functions below here ###
                                
def add_edge(frm, to, cap, w=0, lower_bound=0, must_take=False):
    new_edge = Edge(0, frm, to, cap, None, w, lower_bound, must_take)
    frm.add_out_going(new_edge)
    to.add_in_going(new_edge)
    # if frm.purpose != 0 and to.purpose != 7:
    counter_edge = Edge(1, to, frm, 0, new_edge, -w, 0, must_take)
    to.add_out_going(counter_edge)
    frm.add_in_going(counter_edge)
    new_edge.counterpart = counter_edge

def pref_days(e, date, days):
    # make a list for each day in the period
    day_preferences = []
    for i in range(days):
        day_preferences.append([])

    # go through every preference for the employee
    for p in e.pref:
        if p.day is not None:
            # match the increment counter of the for loop with the current day
            # day_indices keeps track of which days the given preference are relevant to
            day_indices = []
            first_day = 0
            _,week,_ = date.isocalendar()
            weekday = date.weekday()
            if p.day == weekday:
                first_day = 0
            elif p.day < weekday:
                first_day = p.day+7-weekday
            else:
                first_day = p.day-weekday
            # after the proper day is found, add the indices
            if p.repeat is not None:
                match p.repeat:
                    case 1: # weekly
                        for j in range(first_day, days, 7):
                            day_indices.append(j)
                    case 2: # odd weeks
                        date += timedelta(days=first_day)
                        starting_week = 0 if week % 2 == 1 else 1
                        for j in range(first_day+7*starting_week, days, 14):
                            day_indices.append(j)

                        date -= timedelta(days=first_day)
                    case 3: # even weeks
                        date += timedelta(days=first_day)
                        starting_week = 0 if week % 2 == 0 else 1
                        for j in range(first_day+7*starting_week, days, 14):
                            day_indices.append(j)

                        date -= timedelta(days=first_day)
                    case 4: # tri-weekly
                        pass # TODO
                    case 5: # monthly
                        for j in range(first_day, days, 28):
                            day_indices.append(j)

            # append the preference on each relevant day
            for d in day_indices:
                day_preferences[d].append(p)

        if p.date is not None:
            day_index = 0
            for j in range(days):
                if p.date == date:
                    day_preferences[day_index].append(p)
                    date -= timedelta(days=day_index)
                    break
                date += timedelta(days= 1)
                day_index += 1

    return day_preferences[:]

def pref_shifts(e, date, days):
    shift_preferences = []
    for i in range(days):
        shift_preferences.append([])

    for p in e.pref:
        if p.shift is not None:
            if p.day is not None:
                day_indices = []
                first_day = 0
                _,week,_ = date.isocalendar()
                weekday = date.weekday()
                if p.day == weekday:
                    first_day = 0
                elif p.day < weekday:
                    first_day = p.day+7-weekday
                else:
                    first_day = p.day-weekday

                # TODO need to figure whether this will be relevant or not
                # Right now it always assumes that if one has chosen a day and time
                # then it will be repeated every week.

                # if p.repeat is not None:
                #     match p.repeat:
                #         case 0: # daily
                #             for j in range(first_day, len(shift_preferences)):
                #                 day_indices.append(j)
                #         case 1: # weekly
                for j in range(first_day, days, 7):
                    day_indices.append(j)
                        # case 2: # odd weeks
                        #     date += timedelta(days=first_day)
                        #     starting_week = 0 if week % 2 == 1 else 1
                        #     for j in range(first_day+7*starting_week, days, 14):
                        #         day_indices.append(j)

                        #     date -= timedelta(days=first_day)
                        # case 3: # even weeks
                        #     date += timedelta(days=first_day)
                        #     starting_week = 0 if week % 2 == 0 else 1
                        #     for j in range(first_day+7*starting_week, days, 14):
                        #         day_indices.append(j)

                        #     date -= timedelta(days=first_day)
                        # case 4: # tri-weekly
                        #     pass # TODO
                        # case 5: # monthly
                        #     for j in range(first_day, days, 28):
                        #         day_indices.append(j)

                # append the preference on each relevant day
                for d in day_indices:
                    shift_preferences[d].append(p)
            
            elif p.day is None:
                for j in range(len(shift_preferences)):
                    shift_preferences[j].append(p)
            
            if p.date is not None:
                day_index = 0
                for j in range(days):
                    if p.date == date:
                        shift_preferences[day_index].append(p)
                        date -= timedelta(days=day_index)
                        break
                    date += timedelta(days= 1)
                    day_index += 1

    return shift_preferences[:]
                    


def set_day_weight(daily_pref):
    for p in daily_pref:
        if p.day is not None:
            match p.pref_lvl:
                case 1: 
                    if not(p.wanted):
                        return inf
                case 2:
                    return 0 if p.wanted else 2000
                case 3:
                    return 750 if p.wanted else 1250
                case 4:
                    return 950 if p.wanted else 1050
                case 5:
                    return 995 if p.wanted else 1005
            
    return 0

def set_shift_weight(daily_pref, s):
    for p in daily_pref:
        if Shift.same_shift(p.shift, s):
            match p.pref_lvl:
                case 1: 
                    if not(p.wanted):
                        return float("Inf")
                case 2:
                    return 0 if p.wanted else 2000
                case 3:
                    return 750 if p.wanted else 1250
                case 4:
                    return 950 if p.wanted else 1050
                case 5:
                    return 995 if p.wanted else 1005
            
    return 0

### PRINT STATEMENTS ###

def print_edges_with_flow(fg):
    node = fg.source
    # while node != fg.sink:
    for e in node.out_going:
        for edge in e.to.out_going:
            if edge.flow > 0:
                print(f"{edge}\n")


def print_graph_part(fg):
    s = "\t"
    start_node = fg.source
    # src to emp1
    for i in range(7):
        for e in start_node.out_going:
            if e.type == 0 and e.flow != 0:
                s += str(e)
                s += "\n\t "
                start_node = e.to
                break
    # emp1 to day_x
    # x = 0
    # s += str(start_node.out_going[x])
    # s += ", "
    # start_node = start_node.out_going[x].to
    
    print(s)

def print_graph_sink(fg):
    s = "\t"
    for e in fg.sink.in_going:
        s += str(e)
        s += "\n\t "
    print(s)

def print_graph_days(fg):
    s = ""
    start_node = fg.source
    # src to emp1
    s += str(start_node.out_going[0])
    s += "\n\t"

    start_node = start_node.out_going[0].to
    # emp1 to day_x
    for e in start_node.out_going:
        s += str(e) + ", "
        s += str(e.to.out_going[0])
        s += "\n\t"
    
    print(s)

def print_graph_shifts(fg):
    s = ""
    start_node = fg.source
    # src to emp1
    # s += str(start_node.out_going[0])
    # s += "\n\t"
    # start_node = start_node.out_going[0].to
    # for loops to loop through each day and shift
    for e in start_node.out_going:
        if e.flow == 0: continue
        print(f"{e.to}\n\t")




    # for i in range(len(start_node.out_going)):
    #     day_node = start_node.out_going[i].to # this is gonna give intermediate nodes for most
    #     if day_node.out_going[0].to.purpose == 3:
    #         for e in day_node.out_going[0].to.out_going:
    #             s += str(e)
    #             s += "\n\t"
    #     else:
    #         for e in day_node.out_going:
    #             s += str(e)
    #             s += "\n\t"
    
    # print(s)

def weekday_to_str(day) -> str:
    match day:
        case 0:
            return 'monday'
        case 1:
            return 'tuesday'
        case 2:
            return 'wednesday'
        case 3:
            return 'thursday'
        case 4:
            return 'friday'
        case 5:
            return 'saturday'
        case 6:
            return 'sunday'
        case 7:
            return 'monday'

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
                # print(node.out_going[i])
                queue.append(new_node)
                visited.append(new_node)
    
    print(f"Amount of nodes in graph: {len(visited)}")
    

def print_employees(fg):
    sum_lab = 0
    sum_mat = 0
    sum_both = 0
    for e in fg.source.out_going:
        print(e.to.employee)
        if e.to.employee.departments == [0]:
            sum_lab += e.to.employee.weekly_hrs
        elif e.to.employee.departments == [1]:
            sum_mat += e.to.employee.weekly_hrs
        elif e.to.employee.departments == [0,1]:
            sum_both += e.to.employee.weekly_hrs
    print(f"sum working in lab: {sum_lab} ")
    print(f"sum working in mat: {sum_mat} ")
    print(f"sum working in both: {sum_both} ")

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
            preferences = []
            j = i+5
            pref = Preference()
            if 'Preferences:' not in lines[j]:
                continue

            while ']' not in lines[j]:
                if 'is_wanted:' in lines[j]:
                    if 'yes' in lines[j]:
                        pref.wanted = True
                    else:
                        pref.wanted = False
                elif 'preference level:' in lines[j]:
                    pref.pref_lvl = int(lines[j][18])
                elif 'date:' in lines[j]:
                    pref.date = datetime(2000+int(lines[j][12:14]), int(lines[j][9:11]), int(lines[j][6:8]))
                elif 'day' in lines[j]:
                    match lines[j][5:].strip().lower():
                        case 'monday':
                            pref.day = 0
                        case 'tuesday':
                            pref.day = 1
                        case 'wednesday':
                            pref.day = 2
                        case 'thursday':
                            pref.day = 3
                        case 'friday':
                            pref.day = 4
                        case 'saturday':
                            pref.day = 5
                        case 'sunday':
                            pref.day = 6
                elif 'shifts:' in lines[j]:
                    k = 7
                    start = int(lines[j][k:k+3])
                    end = int(lines[j][k+4:k+6])
                    
                    shift = Shift(start, end)
                    k += 5
                    # if more shifts are listed
                    # while lines[j][k] == '.':
                    #     start = int(lines[j][k+1:k+2])
                    #     end = int(lines[j][k+4:k+5])
                    #     Shift(start, end)
                    #     k += 6
                    pref.shift = shift
                elif 'repeat' in lines[j]:
                    if 'daily' in lines[j][7:]:
                        pref.repeat = 0
                    elif 'weekly' in lines[j][7:]:
                        pref.repeat = 1
                    elif 'odd' in lines[j][7:]:
                        pref.repeat = 2
                    elif 'even' in lines[j][7:]:
                        pref.repeat = 3
                    elif 'tri' in lines[j][7:]:
                        pref.repeat = 4
                    elif 'monthly' in lines[j][7:]:
                        pref.repeat = 5
                elif ',' in lines[j]:
                  preferences.append(pref)
                  pref = Preference()

                j += 1

            new_emp = Employee(name=name.strip(), id=id.strip(), departments=dep, weekly_hrs=hrs, exp_lvl=exp, pref= preferences)
            emp_list.append(new_emp) 
    return emp_list

def print_full_schedule(fg):
    s = ""
    for e in fg.source.out_going:
        if e.flow > 0:
            s += f"{e.to.name}\n\t"
            for edge in e.to.out_going:
                s += f"{e.to.name}\n\t"
                if edge.flow > 0:
                    s += f"{edge}\n\t"
                for n in edge.to.out_going:
                    if n.to.purpose == 3:
                        if n.flow > 0:
                            for n2 in n.to.out_going:
                                if n2.flow > 0:
                                    s += f"{n2}\n\t"
                    else:
                        if n.flow > 0:
                            for n2 in n.to.out_going:
                                if n2.flow > 0:
                                    s += f"{n2}\n\t"
                                

    print(s)

def find_paths_with_flow(vertex, sink, visited, path, flows, flow, capacities, cap):
    visited[vertex.vertex_index] = True
    path.append(vertex)
    if flow != 0:
        flows.append(flow)
    if cap > 0:
        capacities.append(cap)
    

    # If we reach the sink, print the path
    if vertex.purpose == 7:
        s = ""
        for i, node in enumerate(path):
            if i == len(path)-1:
                s += f"{node}\n"
            else:
                s += f"{node} - {flows[i]}/{capacities[i]} -> "
        print(s)
    else:
        # Traverse all out-going edges from this vertex
        for edge in vertex.out_going:
            # Check if there is positive flow on the edge and if the destination has not been visited
            if edge.flow > 0 and not(visited[edge.to.vertex_index]):
            # if edge.cap_forward > 0 and not(visited[edge.to.vertex_index]):
                find_paths_with_flow(edge.to, sink, visited, path, flows, edge.flow, capacities, edge.cap_forward)

    # Backtrack
    path.pop()
    if len(flows) > 0:
        flows.pop()
        capacities.pop()
    visited[vertex.vertex_index] = False

def print_flow_paths(source, sink):
    visited = [False]*source.total_vertices  # To keep track of visited vertices
    path = []        # To store the current path
    flows = []
    capacities = []
    find_paths_with_flow(source, sink, visited, path, flows, 0, capacities, 0)

def print_shift_assignments(fg, shift_assignments):
    sum = 0
    for i in range(len(shift_assignments)):
        print(f"Employee: {fg.employees[i].name}")    
        for j in range(len(shift_assignments[0])):
            if shift_assignments[i][j] is not None:
                print(f"\tDay: {j}, Shift: {shift_assignments[i][j]}")
                sum += shift_assignments[i][j].calc_hours()
    print(f"Sum using array of shifts: {sum}")

def main():
    start_date = datetime.now()
    fg = FlowGraph([Shift(7, 19), Shift(19,7), Shift(7, 15), Shift(15, 23), Shift(23, 7), Shift(0, 24)], read_employee_file())
    generate_graph(fg, start_date)
    start_time = time.time()
    algo = Algorithms(fg)

    # flow, cost, n_each_weight, shift_assignments = algo.ford_fulkerson(fg.source, fg.sink)
    # flow, cost, shift_assignments = algo.edmond_karp(fg.source, fg.sink)
    flow, cost = algo.min_cost_flow(fg.source.total_vertices, 9224, fg.source, fg.sink)
    print(f"max flow in graph: {flow}\nTotal cost: {cost}")
    # print(f"amount of each weight [1000, 250, 50, 5, -1000, -250, -50, -5]: {n_each_weight}\nThere are {Edge.total_edges} edges")
    # flow = algo.ford_fulkerson(fg.source, fg.sink)
    # print(f"max flow: {flow}")
    # for i in range(len(path)):
    #     print(f"{path[i]}\n")
    end_time = time.time()
    print(f"Runtime: {(end_time - start_time)} s")
    print_flow_paths(fg.source, fg.sink)
    # print_shift_assignments(fg, shift_assignments)
    # print_graph_sink(fg)


    # flow_sum = 0
    # for e in fg.sink.in_going:
    #     flow_sum += e.flow
    # print(f"sum of flows going into sink: {flow_sum}")


if __name__ == "__main__":
        main()