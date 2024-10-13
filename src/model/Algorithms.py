import sys
# 1100 is also enough
sys.setrecursionlimit(1500)

class Algorithms:

    def __init__(self, fg):
        self.fg = fg
        self.employee_shifts = [[None for i in range(fg.days_in_period)] for j in range(len(fg.employees))]        


# code is heavily inspired from https://www.w3schools.com/dsa/dsa_algo_graphs_fordfulkerson.php
    # Depth-First-Search used to find an augmenting path
    def dfs(self, node, t, last_edge = None, path_min_flow = None, nodes_visited = None, path = None):
        if nodes_visited is None:
            nodes_visited = [False]*node.total_vertices
        if path is None:
            path = []

        nodes_visited[node.vertex_index] = True

        if last_edge is not None:
            path.append(last_edge)

        if path_min_flow is None:
            path_min_flow = float("Inf")

        if node == t:
            for edge in path:
                if edge.to.purpose == 1:
                    emp = edge.to.employee
                elif edge.to.purpose == 2:
                    day = edge.to.day
                elif edge.to.purpose == 4:
                    shift = edge.to.shift
            self.employee_shifts[emp.emp_index][day] = shift
            return path
        
        for e in node.out_going:
            if not nodes_visited[e.to.vertex_index] and (e.cap_forward-e.flow) > 0 and (min(path_min_flow, (e.cap_forward-e.flow)) + e.flow >= e.lower_bound) :
                if node.purpose >= 4:
                    for edge in path:
                        if edge.to.purpose == 1:
                            emp = edge.to.employee
                        elif edge.to.purpose == 2:
                            day = edge.to.day
                        elif edge.to.purpose == 4:
                            shift = edge.to.shift
                if node.purpose < 4 or self.eleven_hour_rule(emp, day, shift):
                    result_path = self.dfs(e.to, t, e, min(path_min_flow, (e.cap_forward-e.flow)), nodes_visited, path[:])
                    if result_path:
                        return result_path
        return None
  
    # Ford-Fulkerson algorithm using dfs for augmenting paths
    def ford_fulkerson(self, s, t):
        max_flow = 0
        total_cost = 0
        n_each_weight = [0]*8

        path = self.dfs(s, t)
        while path:
            path_flow = float("Inf")
            # for i in range(len(path)):
            for e in path:
                # e = path[i]
                if e.to.purpose == 1:
                    emp = e.to.employee
                elif e.to.purpose == 2:
                    day = e.to.day
                elif e.to.purpose == 4:
                    shift = e.to.shift
                path_flow = min(path_flow, (e.cap_forward-e.flow))

            # what if I ditch the lower_bound requirement in the search
            # and here I start a new search if I can see that the min-flow is less than the lower bound on some edge
            # The new search will take place at the node at which the edge with the lower bound requirement comes from
            # Then flow will be added if another augmenting path with min-flow + prev_min_flow >= lower bound
            # else we skip the coming for-loop + max_flow statement
            # This would probably fix the 12 hour shift since the 12 could split into 8 and 4
            # Basically use ford-fuklerson on this ford-fulkerson call :)
            
            # for i in range(len(path)):
            for e in path:
                # e = path[i]
                e.add_flow(path_flow)
                total_cost += e.weight
                match e.weight:
                    case 1000:
                        n_each_weight[0] += 1
                    case 250:
                        n_each_weight[1] += 1
                    case 50:
                        n_each_weight[2] += 1
                    case 5:
                        n_each_weight[3] += 1
                    case -1000:
                        n_each_weight[4] += 1
                    case -250:
                        n_each_weight[5] += 1
                    case -50:
                        n_each_weight[6] += 1
                    case -5:
                        n_each_weight[7] += 1
            max_flow += path_flow
            # self.employee_shifts[emp.emp_index][day] = shift
            # Maybe add print statement here
            # new_edges = ""
            # for e in path:
            #     new_edges += str(e)
            #     new_edges += ", "
            # print(new_edges)
            path = self.dfs(s, t)

        return max_flow, total_cost, n_each_weight, self.employee_shifts

    # https://www.w3schools.com/dsa/dsa_algo_graphs_edmondskarp.php
    def bfs(self, s, t, parent, nodes_visited):
        queue = []
        
        nodes_visited[s.vertex_index] = True
        queue.append(s)

        while queue:
            node = queue.pop(0)
            for e in node.out_going:
                if (not nodes_visited[e.to.vertex_index] or self.twelve_hr_shift(e)) and (e.cap_forward - e.flow) > 0:
                    queue.append(e.to)
                    nodes_visited[e.to.vertex_index] = True
                    parent[e.to.vertex_index] = node
                if nodes_visited[t.vertex_index]:
                    return True
        # return nodes_visited[t.vertex_index]

    def twelve_hr_shift(self, e) -> bool:
        shift = e.to.shift
        return (shift is not None and shift.calc_hours() == 12 and e.flow == 8)
    
    def edmond_karp(self, s, t):
        parent = [-1]*s.total_vertices
        total_max_flow = 0
        total_cost = 0
        nodes_visited = [False] * s.total_vertices

        while self.bfs(s, t, parent, nodes_visited[:]):
            shift_node = None
            bottleneck_flow = float("Inf")
            node = t
            while node != s:
                edge_flow = 0
                for e in node.in_going:
                    if e.frm == parent[node.vertex_index]:
                        if e.to.purpose == 1:
                            emp = e.to.employee
                        elif e.to.purpose == 2:
                            day = e.to.day
                        elif e.to.purpose == 4:
                            shift = e.to.shift
                            shift_node = e.to
                        edge_flow = e.cap_forward - e.flow

                bottleneck_flow = min(bottleneck_flow, edge_flow)
                node = parent[node.vertex_index]

            if self.employee_shifts[emp.emp_index][day] is None:
                self.employee_shifts[emp.emp_index][day] = shift
            elif self.employee_shifts[emp.emp_index][day] != shift:
                nodes_visited[shift_node.vertex_index] = True
                continue
            total_max_flow += bottleneck_flow
            per = total_max_flow/9224.0*100
            print("currently at {:.2f}%".format(per))
            v = t
            while v != s:
                edge = None
                for e in v.in_going:
                    if e.frm == parent[v.vertex_index]:
                        edge = e
                edge.add_flow(bottleneck_flow)
                total_cost += edge.weight
                v = parent[v.vertex_index]
            self.employee_shifts[emp.emp_index][day] = shift
            
        return total_max_flow, total_cost, self.employee_shifts

        
    def eleven_hour_rule(self, employee, day, shift) -> bool:
        if employee is None or shift is None or day is None:
            # print("All are None")
            return True
        
        if day == 0:
            # print("day is 0")
            return True
        if self.employee_shifts[employee.emp_index][day-1] is None:
            # print("prev day is None")
            return True
        
        end_time = self.employee_shifts[employee.emp_index][day-1].end_time
        start_time = shift.start_time
        if end_time == 7:
            # print(f"end_time  == 7: {(start_time-end_time) >= 11}")
            return (start_time-end_time) >= 11
        else:
            # print(f"other: {(24-end_time + start_time) >= 11}")
            return (24-end_time + start_time) >= 11


    # link to site used https://cp-algorithms.com/graph/min_cost_flow.html
    def shortest_paths(self, n, s, dist, parent, can_visit):
        inf = float("Inf")
        dist[:] = [inf]*n
        dist[s.vertex_index] = 0
        in_queue = [False]*n
        q = [s]
        parent[:] = [-1]*n

        while q:
            node = q.pop(0)
            in_queue[node.vertex_index] = False
            for e in node.out_going:
                to_node = e.to
                if e.cap_forward-e.flow > 0 and dist[to_node.vertex_index] > dist[node.vertex_index] + e.weight and can_visit[node.vertex_index]:
                    dist[to_node.vertex_index] = dist[node.vertex_index] + e.weight
                    parent[to_node.vertex_index] = node
                    if not in_queue[to_node.vertex_index]:
                        in_queue[to_node.vertex_index] = True
                        q.append(to_node)
            
          
    def min_cost_flow(self, n, k, s, t):
        total_flow = 0
        total_cost = 0
        dist = []
        parent = []
        can_visit = [False]*s.total_vertices

        while total_flow < k:
            self.shortest_paths(n,s, dist, parent, can_visit)
            if dist[t.vertex_index] == float("Inf"):
                break

            bottle_flow = k - total_flow
            node = t
            while node != s:
                for e in node.in_going: # can greatly improve algorithm by introducing a "path" array
                    if e.frm == parent[node.vertex_index]:
                        edge = e
                        break
                bottle_flow = min(bottle_flow, edge.cap_forward-edge.flow)
                node = parent[node.vertex_index]

            total_flow += bottle_flow
            total_cost += dist[t.vertex_index]
            node = t
            while node != s:
                for e in node.in_going: # can greatly improve algorithm by introducing a "path" array
                    if e.frm == parent[node.vertex_index]:
                        edge = e
                        break
                edge.add_flow(bottle_flow)
                node = parent[node.vertex_index]

            per = total_flow/9224.0*100
            print("currently at {:.2f}%".format(per))
        return total_flow, total_cost