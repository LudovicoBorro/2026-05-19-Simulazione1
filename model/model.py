import copy

import networkx as nx
from database.DAO import DAO

class Model:

    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapArtist = {}
        self._bestPath = []
        self._bestLun = 0

    def bestPath(self, artist):
        self._bestPath = []
        self._bestLun = 0
        parziale = [artist]
        for v in self._graph.neighbors(parziale[-1]):
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        if len(self._bestPath) > 0:
            return self._bestPath, self._bestLun
        else:
            return None, None

    def _ricorsione(self, parziale):
        # Ottimalità
        if len(parziale) > self._bestLun:
            self._bestLun = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        # Ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if self._graph[parziale[-1]][v]['weight'] > self._graph[parziale[-2]][parziale[-1]]['weight'] and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()

    @staticmethod
    def getAllGenres():
        return DAO.getAllGenres()

    def getArtists(self):
        return sorted(self._idMapArtist.values(), key=lambda x: x.Name)

    def buildGraph(self, genre):
        self._graph.clear()
        self._idMapArtist.clear()
        nodes = DAO.getAllArtistsByGenre(genre.GenreId)
        for node in nodes:
            self._idMapArtist[node.ArtistId] = node
        self._graph.add_nodes_from(nodes)
        edges = DAO.getAllEdges(genre.GenreId)
        for edge in edges:
            art1 = self._idMapArtist[edge[0]]
            art2 = self._idMapArtist[edge[1]]
            peso = art1.Popularity + art2.Popularity
            if art1.Popularity == art2.Popularity:
                self._graph.add_edge(art1, art2, weight=peso)
                self._graph.add_edge(art2, art1, weight=peso)
            elif art1.Popularity > art2.Popularity:
                self._graph.add_edge(art1, art2, weight=peso)
            else:
                self._graph.add_edge(art2, art1, weight=peso)

    def graphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getArtistMaxInfluence(self):
        artistMaxInfluence = None
        bestInfluence = 0
        for artist in self._graph.nodes:
            influence = 0
            for succ in self._graph.successors(artist):
                influence += self._graph[artist][succ]['weight']
            for pred in self._graph.predecessors(artist):
                influence -= self._graph[pred][artist]['weight']
            if bestInfluence < influence:
                bestInfluence = influence
                artistMaxInfluence = artist
        return artistMaxInfluence, bestInfluence

    def getTop5Edges(self):
        archi = self._graph.edges(data=True)
        return sorted(archi, key=lambda x: x[2]['weight'], reverse=True)[:5]

    def isGraphOk(self):
        return len(self._graph.nodes) > 0 and len(self._graph.edges) > 0