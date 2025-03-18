import random

class Domanda:
    def __init__(self, testo, difficolta, corretta, risposte):
        self.testo = testo
        self.difficolta = difficolta
        self.corretta = corretta
        self.risposte = risposte

class Giocatore:
    def __init__(self, nome, punteggio):
        self.nome = nome
        self.punteggio = int(punteggio)

def leggi_punti(nome_file):

    with open(nome_file, "r", encoding="utf-8") as file:
        righe = file.readlines()
        giocatori = []
        for riga in righe:
            nome, punteggio = riga.split(" ")
            punteggio = punteggio.strip()
            g = Giocatore(nome, punteggio)
            giocatori.append(g)
        return giocatori

def leggi_domande(nome_file):

    with open(nome_file, "r", encoding="utf-8") as file:
        contenuto = file.read().strip()

        blocchi = contenuto.split("\n\n")
        domande = []

        for blocco in blocchi:
            d = blocco.strip().split("\n")
            if len(d) == 6:
                testo = d[0]
                difficolta = int(d[1])
                corretta = d[2]
                risposte = [d[2], d[3], d[4], d[5]]
                domanda = Domanda(testo, difficolta, corretta, risposte)
                domande.append(domanda)

    return domande

def scrivi_punti(giocatori, nome_file):
    giocatori.sort(key=lambda x: x.punteggio, reverse=True)
    with open(nome_file, "w", encoding="utf-8") as file:
        for g in giocatori:
            file.write(f"{g.nome} {g.punteggio}\n")

def crea_domanda(domande, difficolta):
    domande_per_livello = [domanda for domanda in domande if domanda.difficolta == difficolta]
    if domande_per_livello:
        domanda = random.choice(domande_per_livello)
        random.shuffle(domanda.risposte)
        return domanda
    return None

def main():
    giocatori = leggi_punti("punti.txt")
    domande = leggi_domande("domande.txt")
    difficolta = 0
    punteggio = 0
    finito = False

    while not finito:
        d = crea_domanda(domande, difficolta)
        if d is None:
            print("Non ci sono più domande per questo livello.")
            break

        print(f"Livello {d.difficolta}): {d.testo}")
        for i in range(1, 5):
            print(f"{i}. {d.risposte[i - 1]}")

        indice_corretta = d.risposte.index(d.corretta) + 1

        risposta = int(input("Rispondi: "))
        if risposta == indice_corretta:
            print("Risposta corretta!")
            difficolta += 1
            punteggio += 1
        else:
            print(f"Risposta errata! La risposta corretta era: {d.corretta}")
            nome = input("Inserisci il tuo nome: ")
            giocatore = Giocatore(nome, punteggio)
            giocatori.append(giocatore)
            finito = True

    if not finito:
        nome = input("Inserisci il tuo nome: ")
        giocatore = Giocatore(nome, punteggio)
        giocatori.append(giocatore)

    scrivi_punti(giocatori, "punti.txt")

    print("\nPunteggi finali:")
    for g in giocatori:
        print(f"{g.nome}: {g.punteggio} punti")


main()