import sqlite3

# Sette opp kobling og peker til database
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

# Lager tabell for brukere så eiere kan logge inn
cur.execute("""CREATE TABLE IF NOT EXISTS brukere(
            id integer primary key NOT NULL,
            restaurant_id integer,
            navn text NOT NULL,
            passord text NOT NULL
            )""")
con.commit()

# Lager tabell for restauranter
cur.execute("""CREATE TABLE IF NOT EXISTS restauranter(
            id integer primary key NOT NULL,
            navn text NOT NULL
            )""")
con.commit()

# Lager tabell over ulike retter til alle restauranter med hvilke restaurant de hører til bestemt av restaurant_id
cur.execute("""CREATE TABLE IF NOT EXISTS meny_retter(
            id integer primary key NOT NULL,
            restaurant_id integer NOT NULL,
            rett text NOT NULL,
            bilde text NOT NULL,
            beskrivelse text NOT NULL,
            pris integer NOT NULL
            )""")
con.commit()

# Lager brukere og restauranter med navn og id
brukere = [{"navn":"RES1", "rid": 1}, {"navn":"RES2", "rid": 2}, {"navn":"RES3", "rid": 3}]
restauranter = [{"navn": "PASTA SPESIALISTEN", "id": 1}, {"navn": "NORSK MAT", "id": 2}, {"navn":"AMERIKANEREN", "id": 3}]

#lager unike menyer for hver av restaurantene hvor rid er id-en til restauranten
meny1 = [{"rid": 1, "rett": "Spaghetti med kjøttboller", "bilde": "spaghettiKjøttboller.jpg", "beskrivelse": "spaghetti med kjøttballer og tomatsaus", "pris": 200},
         {"rid": 1, "rett": "Tagliatelle", "bilde": "tagliatelle.jpg", "beskrivelse": "tagliatelle med pastasaus", "pris": 250},
         {"rid": 1, "rett": "Tomatsuppe", "bilde": "tomatsuppe.jpg", "beskrivelse": "Tomatsuppe med makaroni og egg, ved siden av hvitløksbrød", "pris": 170},
         {"rid": 1, "rett": "Tortellini", "bilde": "tortellini.jpg", "beskrivelse": "tortellini med pastasaus", "pris": 300},
         {"rid": 1, "rett": "spaghetti med pølser", "bilde": "spaghettiPølser.jpg", "beskrivelse": "spaghetti med pølser og tomatsaus", "pris": 200}]


# Legger til brukere og restauranter i brukere og restauranter tabellene, samt tømmer begge tabellene for å unngå kopier
cur.execute("DELETE FROM brukere")
cur.execute("DELETE FROM restauranter")
cur.execute("DELETE FROM meny_retter")
con.commit()
cur.executemany("INSERT INTO brukere(restaurant_id, navn, passord) VALUES(?, ?, 'Passord1')", [(bruker["rid"], bruker["navn"]) for bruker in brukere])
cur.executemany("INSERT INTO restauranter(id,navn) VALUES(?,?)", [(res["id"], res["navn"]) for res in restauranter])
cur.executemany("INSERT INTO meny_retter(restaurant_id,rett,bilde,beskrivelse,pris) VALUES(?,?,?,?,?)", [(rett["rid"],rett["rett"],rett["bilde"],rett["beskrivelse"],rett["pris"]) for rett in meny1])
con.commit()