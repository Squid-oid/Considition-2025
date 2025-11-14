import pandas as pd
import numpy as np
import networkx as nx

class g_map():
    def __init__(self, mapdat):
        '''
            Create a map object containing the information from the mapstate
        '''
        self.nodes = pd.DataFrame(mapdat['nodes']).reset_index().set_index('id')
        self.edges = pd.DataFrame(mapdat['edges']).set_index('id')
        junc_id_to_index = self.nodes.get('index')
        self.edges = self.edges.join(junc_id_to_index.rename('fromIdx'), on = 'fromNode')
        self.edges = self.edges.join(junc_id_to_index.rename('toIdx'), on = 'toNode')
        self.nodes['coord'] = self.nodes.apply(lambda row: [row['posX'],row['posY']], axis = 1)

        self.charging_nodes = pd.DataFrame([a for b,a in self.nodes.iterrows() if a.target.get('Type') != 'Null'])

        self.graph = nx.Graph()
        for id, node in self.nodes.drop(columns='customers').iterrows():
            self.graph.add_node(id, attr = node.to_dict())

        for id, edge in self.edges.rename(columns={'length':'weight'}).iterrows():
            self.graph.add_edge(u_of_edge = edge['fromNode'],
                        v_of_edge = edge['toNode'],
                        weight = edge['weight'],
                        attr = edge.to_dict()
            )

        self.fastestPathsLength = dict(nx.shortest_path_length(self.graph, weight='weight'))

        self.ticks = mapdat['ticks'] 

    def update(self, mapdat):
        '''
            Updates the map object to contain the new node states
            Note: Inefficient 
        '''
        self.nodes = pd.DataFrame(mapdat['nodes']).reset_index().set_index('id')
        self.edges = pd.DataFrame(mapdat['edges']).set_index('id')
        junc_id_to_index = self.nodes.get('index')
        self.edges = self.edges.join(junc_id_to_index.rename('fromIdx'), on = 'fromNode')
        self.edges = self.edges.join(junc_id_to_index.rename('toIdx'), on = 'toNode')
        self.nodes['coord'] = self.nodes.apply(lambda row: [row['posX'],row['posY']], axis = 1)

        self.charging_nodes = pd.DataFrame([a for b,a in self.nodes.iterrows() if a.target.get('Type') != 'Null'])

    def leastDisturbingCharger(self, origin, dest, fuel, burn, verbose = True):
        minDist = np.inf
        o = origin
        d = dest
        range = fuel/burn

        charge_node = None
        for i, node in self.charging_nodes.iterrows():
            c = node.name
            first_leg = self.distance(o,c)
            second_leg = self.distance(c,d)
            distance = first_leg + second_leg
            if distance < minDist:
                if first_leg < range or range is None:
                    charge_node = c
                    minDist = distance
                    #print(f'Got Here... For customer with origin: {o}, Range: {range}')
                else:
                    pass
                    #print(f'Got Here... For customer with origin: {o}, Range: {range}')
        if charge_node is None:
            minDist = np.inf
            for i, node in self.charging_nodes.iterrows():
                c = node.name
                first_leg = self.distance(o,c)
                if first_leg < minDist:
                    charge_node = c
                    minDist = first_leg
            #print(f'Failed to Find reachable charger for customer with origin:{o}, Range: {range}')        
        if verbose:   
            return charge_node, second_leg*burn

    def closestChargeToDest(self, origin, dest, range = None):
        minDist = np.inf
        o = origin
        d = dest
        prospects = []
        for i, node in self.charging_nodes.iterrows():
            c = node.name
            prospective = self.distance(c,d)
            if prospective <= minDist:
                prospects.append(c)
                minDist = prospective
        minDist = np.inf
        # Tie break to smallest path dist
        for node in prospects:
            prospective = self.distance(o,c)
            if prospective <= minDist:
                charge_node = c
                minDist = prospective
        return charge_node

    def distance(self, origin, destination):
        if not isinstance(origin,str):
            o = origin.get('index')
            d = destination.get('index')
        else:
            o = origin
            d = destination
        return self.fastestPathsLength[o][d]

    def getChargingNodes(self):
        return self.charging_nodes

    def getCustomers(self):
        customers = [
            dict(customer, loc=index)
            for index, node in self.nodes.iterrows()
            for customer in node.customers
        ]
        customers += [
            dict(customer, loc=edge.get('toNode'))
            for index, edge in self.edges.iterrows()
            for customer in edge.customers
        ]
        return pd.DataFrame(customers).set_index(keys='id')
        

    @staticmethod
    def getCoord(node):
        return node['coord']