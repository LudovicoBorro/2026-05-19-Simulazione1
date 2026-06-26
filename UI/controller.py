import flet as ft

from model import artist


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDDGenre = None
        self._choiceDDArtist = None

    def fillDDGenre(self):
        genres = self._model.getAllGenres()
        for genre in genres:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(genre, data=genre, on_click=self._readDDGenre)
            )
        self._view.update_page()

    def _readDDGenre(self, e):
        if e.control.data is None:
            self._choiceDDGenre = None
            return
        self._choiceDDGenre = e.control.data

    def handleCreaGrafo(self, e):
        if self._choiceDDGenre is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un genere!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(self._choiceDDGenre)
        nodes, edges = self._model.graphDetails()
        artMaxInfluente, influence = self._model.getArtistMaxInfluence()
        top5Archi = self._model.getTop5Edges()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {edges}"))
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {artMaxInfluente}, con influenza: {influence}"))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for edge in top5Archi:
            self._view.txt_result.controls.append(ft.Text(f"{edge[0]} -> {edge[1]}: {edge[2]['weight']}"))
        self.fillDDArtist()
        self._view.update_page()

    def handleCammino(self,e):
        if not self._model.isGraphOk():
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, devi creare il grafo prima!", color="red"))
            self._view.update_page()
            return

        if self._choiceDDArtist is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un'artista!", color="red"))
            self._view.update_page()
            return

        bestPath, bestLun = self._model.bestPath(self._choiceDDArtist)

        if bestPath is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non è stato trovato alcun cammino!", color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Trovato un cammino ottimo di lunghezza {bestLun}:"))
        for node in bestPath:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def fillDDArtist(self):
        artists = self._model.getArtists()
        for artist in artists:
            self._view._ddArtist.options.append(
                ft.dropdown.Option(artist, data=artist, on_click=self._readDDArtist)
            )
        self._view.update_page()

    def _readDDArtist(self, e):
        if e.control.data is None:
            self._choiceDDArtist = None
            return
        self._choiceDDArtist = e.control.data