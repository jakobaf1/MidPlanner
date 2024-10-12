import sys
# 1100 is also enough
sys.setrecursionlimit(1500)

class Algorithms:

    def __init__(self, fg):
        self.fg = fg


# code is heavily inspired from https://www.w3schools.com/dsa/dsa_algo_graphs_fordfulkerson.php
    # Depth-First-Search used to find an augmenting path
    def dfs(self, node, t, last_edge = None, path_min_flow = None, nodes_visited = None, path = None):
        if nodes_visited is None:
            nodes_visited = [False]*node.total_vertices
        if path is None:
            path = []

        nodes_visited[node.index] = True

        if last_edge is not None:
            path.append(last_edge)

        if path_min_flow is None:
            path_min_flow = float("Inf")

        if node == t:
            return path
        
        for e in node.out_going:
            if not nodes_visited[e.to.index] and (e.cap_forward-e.flow) > 0 and (min(path_min_flow, (e.cap_forward-e.flow)) + e.flow >= e.lower_bound):
                result_path = self.dfs(e.to, t, e, min(path_min_flow, (e.cap_forward-e.flow)), nodes_visited, path[:])
                if result_path:
                    return result_path
        return None
  
    # Ford-Fulkerson algorithm using dfs for augmenting paths
    def ford_fulkerson(self, s, t):
        max_flow = 0
        total_cost = 0
        n_each_weight = [0]*9

        path = self.dfs(s, t)
        while path:
            path_flow = float("Inf")
            for i in range(len(path)-1):
            # for e in path: Why is this causing a recursion max depth reached error?
                e = path[i]
                path_flow = min(path_flow, (e.cap_forward-e.flow))

            # what if I ditch the lower_bound requirement in the search
            # and here I start a new search if I can see that the min-flow is less than the lower bound on some edge
            # The new search will take place at the node at which the edge with the lower bound requirement comes from
            # Then flow will be added if another augmenting path with min-flow + prev_min_flow >= lower bound
            # else we skip the coming for-loop + max_flow statement
            # This would probably fix the 12 hour shift since the 12 could split into 8 and 4
            # Basically use ford-fuklerson on this ford-fulkerson call :)

            for i in range(len(path)-1):
            # for e in path: Why is this causing a recursion max depth reached error?
                e = path[i]
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
                    case float("Inf"):
                        n_each_weight[8] += 1
            max_flow += path_flow
            # Maybe add print statement here
            # new_edges = ""
            # for e in path:
            #     new_edges += str(e)
            #     new_edges += ", "
            # print(new_edges)
            path = self.dfs(s, t)

        return max_flow, total_cost, n_each_weight

    # Link to implemented bellman-ford for the purpose of max-flow, min-cost
    # this one runs the max-flow and min-cost together however, so I'll have to change the ford-fulkerson
    # Probably just gonna keep the ford-fulkerson and make a new algorithm which does both
    # https://www.geeksforgeeks.org/minimum-cost-maximum-flow-from-a-graph-using-bellman-ford-algorithm/
    def bellman_ford(self, s, n_vertices):
        edges_taken = []
        dist = []

        edges_taken.append(s)
        dist.append(0)

        # for _ in range(n_vertices): # go through each vertex in graph

        #     for e in graph: # go though every edge
        #         edges_taken.append(e)
        #         if dist[e.frm] != float("Inf") and dist[e.frm] + e.weight < dist[e.to]:
        #             dist[e.to] = dist[e.frm] + e.weight

        # for e in graph:
        #     if dist[e.frm] != float("Inf") and dist[e.frm] + e.weight < dist[e.to]:
        #         # logic which sends new flow through
        #         print("negative weight cycle found")
        #         return

    # https://www.w3schools.com/dsa/dsa_algo_graphs_edmondskarp.php
    def bfs(self, s, t, parent):
        queue = []
        nodes_visited = [False] * s.total_vertices
        
        nodes_visited[s.index] = True
        queue.append(s)

        while queue:
            node = queue.pop(0)
            for e in node.out_going:
                # if e.weight == float("Inf"):
                    # return e.weight
                if not nodes_visited[e.to.index] and (e.cap_forward - e.flow) > 0:
                    queue.append(e.to)
                    nodes_visited[e.to.index] = True
                    parent[e.to.index] = node

        return nodes_visited[t.index]

    def edmond_karp(self, s, t):
        parent = [-1]*s.total_vertices
        total_max_flow = 0
        total_cost = 0

        while self.bfs(s, t, parent):
            bottleneck_flow = float("Inf")
            node = t
            while node != s:
                edge_flow = 0
                for e in node.in_going:
                    if e.frm == parent[node.index]:
                        edge_flow = e.cap_forward - e.flow

                bottleneck_flow = min(bottleneck_flow, edge_flow)
                node = parent[node.index]
            
            total_max_flow += bottleneck_flow
            v = t
            while v != s:
                edge = None
                for e in v.in_going:
                    if e.frm == parent[v.index]:
                        edge = e
                edge.add_flow(bottleneck_flow)
                total_cost += edge.weight
                v = parent[v.index]

        return total_max_flow, total_cost