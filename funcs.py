import sqlite3


def relatorio(cur: sqlite3.Cursor):
    string = 'art_id | art_nome | art_  email | art_integrantes | art_genero | art_categoria | art_site'
    sql = "SELECT * FROM artista"
    cur.execute(sql)
    tabela = cur.fetchall()
    
    return tabela
