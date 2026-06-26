from database.DB_connect import DBConnect
from model.artist import Artist
from model.genre import Genre


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
            select * 
            from genre g 
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArtistsByGenre(genreId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
            select a2.ArtistId, a2.Name, sum(i.Quantity) as Popularity
            from track t, album a, artist a2, invoiceline i
            where t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId and t.GenreId = %s
            and i.TrackId = t.TrackId
            group by a2.ArtistId, a2.Name
        """

        cursor.execute(query, (genreId, ))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(genreId):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        query = """
                select t1.artistid as a1, t2.artistid as a2
                from 
                (
                select a2.ArtistId, a2.Name, i2.CustomerId
                from track t, album a, artist a2, invoiceline i, invoice i2 
                where t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId and t.GenreId = %s
                and i.TrackId = t.TrackId and i2.InvoiceId = i.InvoiceId 
                ) as t1,
                (
                select a2.ArtistId, a2.Name, i2.CustomerId
                from track t, album a, artist a2, invoiceline i, invoice i2 
                where t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId and t.GenreId = %s
                and i.TrackId = t.TrackId and i2.InvoiceId = i.InvoiceId 
                ) as t2
                where t1.artistid <> t2.artistid and t1.customerid = t2.customerid
        """

        cursor.execute(query, (genreId, genreId))

        for row in cursor:
            result.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return result