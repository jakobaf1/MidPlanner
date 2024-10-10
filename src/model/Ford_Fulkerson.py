class Ford_Fulkerson:

    def __init__(self, fg):
        self.fg = fg


# code is heavily inspired from https://www.w3schools.com/dsa/dsa_algo_graphs_fordfulkerson.php
    # Depth-First-Search used to find an augmenting path
    def dfs(self, node, t, last_edge = None, nodes_visited = None, path = None):
        if nodes_visited is None:
            nodes_visited = []
        if path is None:
            path = []

        nodes_visited.append(node)
        if last_edge is not None:
            path.append(last_edge)

        if node == t:
            return path
        
        for e in node.out_going:
            if nodes_visited.count(e.to) == 0 and (e.cap_forward-e.flow) > 0:
                result_path = self.dfs(e.to, t, e, nodes_visited, path[:])
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
            for i in range(len(path)-1):
            # for e in path: Why is this causing a recursion max depth reached error?
                e = path[i]
                path_flow = min(path_flow, e.cap_forward)

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
            max_flow += path_flow

            # Maybe add print statement here
            # new_edges = ""
            # for e in path:
            #     new_edges += str(e)
            #     new_edges += ", "
            # print(new_edges)
            path = self.dfs(s, t)

        return max_flow, total_cost, n_each_weight


    def bfs(self, s, t):
        queue = []
        edges_taken = []
        
        queue.append((s,[]))
        # node_path = None
        while queue:
            node, path = queue.pop(0)
            # print(f"node: {node} and path: {path}")
            for e in node.out_going:
                if edges_taken.count(e.to) == 0 and e.cap_forward > 0:
                    queue.append((e.to, [e]))
                    edges_taken.append(e.to)
            # if node is t:
            #     return path
        return None

    def edmond_karp(self, s, t):
        paren_nodes = []
        total_max_flow = 0


        while self.bfs(self.fg, s, t):
            bottleneck_flow = float("Inf")
            node = t

            while node != s:
                pass
                # bottleneck_flow = min(bottleneck_flow, )
