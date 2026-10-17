"""
Calcolatore di probabilità per il minigioco electrod nel casinò di Pokemon SoulSilver


Come funziona

• La griglia: Ti trovi davanti a una griglia 5x5 di tessere coperte.
• Indizi ai bordi: Per ogni riga e colonna, ai lati trovi due numeri:
	• (p) Il primo indica la somma dei numeri nascosti in quella riga o colonna.
	• (n) Il secondo indica il numero di Voltorb (che bloccano il livello) presenti in quella riga o colonna.
• Il valore delle tessere: Sotto le tessere si nascondono:
	• 1: Non cambiano nulla al moltiplicatore dei gettoni.
	• 2 o 3: Moltiplicano il tuo montepremi provvisorio di quel turno per 2 o per 3.
	• Voltorb (0): Se lo scopri, perdi tutti i gettoni accumulati nel round e torni indietro (o resti allo stesso livello).
• L'obiettivo: Scoprire tutte le tessere con i numeri 2 e 3 (e volendo gli 1 sicuri) evitando i Voltorb per incassare i gettoni

Voglio creare un sistema che calcoli le probabilità per ogni casella:
    P(boom) prob che sia una bomba
    P(safe) prob che non sia una bomba (1-P(boom))
    P(1) prob che sia un 1
    P(2) ... 2
    P(3) ... 3

Il sistema deve aggiornare le probabilità ogni volta che si scopre il valore effettivo di una casella.

Per ogni riga (e colonna) vengono calcolate le probabilità della generica casella. Per fare ciò devo tenere conto di alcuni dati
La struttura della riga/colonna sarà un dizionario con le seguenti chiavi:
    - P_boom    probabilità che la generica casella della riga/colonna sia una bomba
    - P1        probabilità che la generica casella della riga/colonna sia un 1
    - P2        probabilità che la generica casella della riga/colonna sia un 2
    - P3        probabilità che la generica casella della riga/colonna sia un 3
    - P_safe    probabilità che la generica casella della riga/colonna non sia una bomba
    - num_caselle_ignote    (quante caselle non sono ancora state girate in quella riga/colonna, di cui non conosciamo ancora il valore effettivo)
    - num_bombe             (quante bombe ci sono nella riga/colonna - fisso per tutta la partita)
    - somma_punteggi        (la somma dei punteggi delle caselle della riga/colonna - fisso per tutta la partita)



    QUANDO VIENE SCOPERTA UNA CASELLA

Quando viene scoperta una casella (dando per scontato che non sia una bomba, altrimenti il gioco finirebbe) devo aggiornare le probabilità delle caselle che condividono la stessa riga e colonna:

Mettiamo per esempio che venga scoperta la generica casella (x, y):

1. Ricalcolo P_boom, P1, P2, P3, P_safe e abbasso di 1 il num_caselle_ignote della riga x e della colonna y

2. Per ogni casella della riga x e della colonna y aggiorno le probabilita con update_prob.
    In update_prob concateno le probabilità di righe e colonne di quella casella aggiornata,
    Tabellone fornisce all'oggetto Casella le probabilità della sua riga e della sua colonna per permettergli internamente di ricalcolare le proprie

"""

def nuova_struttura_riga_colonna(valori):
    return {
        "P_boom" :1,
        "P1" : 0,
        "P2" : 0,
        "P3" : 0,
        "P_safe" : 0,
        "num_caselle_ignote" : 5,
        "num_bombe" : valori[0],
        "somma_punteggi" : valori[1],
    }

def studio_possibili_casi(num_caselle_ignote : int, num_bombe : int, somma_punteggi : int):
    """
    Date n caselle ignote e la somma dei punteggi prova tutte le combinazioni con i valori 1, 2 e 3 restituento le probabilità P1 P2 e P3
    """

    if num_caselle_ignote > 5 or num_caselle_ignote < 0 : raise ValueError("num_caselle_ignote può essere compreso solo tra 0 e 5")
    tmp_lista = []
    tmp_cont1 = 0
    tmp_cont2 = 0
    tmp_cont3 = 0
    tmp_cont_tot = 0
    for a in [1,2,3]:
        for b in [1,2,3]:
            for c in [1,2,3]:
                for d in [1,2,3]:
                    for e in [1,2,3]:
                        tmp_lista = [a,b,c,d,e]
                        tmp_lista = tmp_lista[0:num_caselle_ignote-num_bombe]
                        if sum(tmp_lista) == somma_punteggi:
                            tmp_cont_tot+=1
                            if 1 in tmp_lista: tmp_cont1+=1
                            if 2 in tmp_lista: tmp_cont2+=1
                            if 3 in tmp_lista: tmp_cont3+=1
                        else:
                            pass

    if tmp_cont_tot == 0:
        P1 = 0
        P2 = 0
        P3 = 0
    else:
        P1 = tmp_cont1/tmp_cont_tot
        P2 = tmp_cont2/tmp_cont_tot
        P3 = tmp_cont3/tmp_cont_tot
    return P1, P2, P3
                        



class Casella:
    def __init__(self):
        self.P_boom = 1
        self.P1 = 0
        self.P2 = 0
        self.P3 = 0
        self.P_safe = 0
        self.value = "?"

    def get_dict(self):
        return {
            "P_boom" : self.P_boom,
            "P1" : self.P1,
            "P2" : self.P2,
            "P3" : self.P3,
            "P_safe" : self.P_safe,
            "value" : self.value
        }

    def update_prob(self, prob_riga : dict, prob_colonna : dict):
        """
        Ricalcolare le probabilità P_boom P_1 P_2 P_3 e P_safe basantosi sulle probabilità generiche della riga e della colonna
        Ogni probabilità è un dizionario con le seguenti chiavi:
            - P_boom    probabilità che la generica casella della riga/colonna sia una bomba
            - P1        probabilità che la generica casella della riga/colonna sia un 1
            - P2        probabilità che la generica casella della riga/colonna sia un 2
            - P3        probabilità che la generica casella della riga/colonna sia un 3
            - P_safe    probabilità che la generica casella della riga/colonna non sia una bomba
            - num_caselle_ignote        caselle ingote della riga/colonna
            - num_bombe                 numero bombe nella riga/colonna
            - somma_punteggi            somma dei punteggi nella riga/colonna

        """
        #TODO



class Tabellone:
    def __init__(self, valori_riga : list[tuple], valori_colonna : list[tuple]):
        """
        Quando dichiaro un nuovo tabellone devo immettere per ogni riga e colonna il numero di bombe e la somma dei punteggi.
        Ogni argomento è una lista che contiene i valori per ogni riga/colonna.
        I valori di ogni riga/colonna immessi dagli argomenti sono tuple contenenti:
            num_bombe : int,
            somma_punteggi : int

        STRUTTURE DELL'OGGETTO
            Questo oggetto tiene conto di un dizionario per ciascuna riga e colonna contenente probabilità e dati.
            Inoltre tiene conto di una griglia di oggetti Casella

        In questo oggetti vengono calcolate le probabilità della generica casella in una specifica riga/colonna; sarà internamente
        all'oggetto Casella che verranno calcolate le probabilità specifiche

        """
        self.caselle = [[Casella() for _ in range(5)] for _ in range(5)]
        self.valori_riga = [nuova_struttura_riga_colonna(valori_riga[i]) for i in range(5)]
        self.valori_colonna = [nuova_struttura_riga_colonna(valori_colonna[i]) for i in range(5)]

    def show(self):
        # restituisce i valori di probabilità di tutte le caselle
        for riga in range(5):
            for colonna in range(5):
                ...

    def get_casella(self, riga : int, colonna : int):
        # restituisce valori di una casella
        casella = self.caselle[riga][colonna]
        return casella.get_dict()

        
                

    def update_riga(self, n: int):
        """
        Aggiorna i valori di probabilità delle caselle di una riga
        """
        struttura = self.valori_riga[n]
        num_bombe = struttura["num_bombe"]
        num_caselle_ignote = struttura["num_caselle_ignote"]
        somma_punteggi = struttura["somma_punteggi"]


        if num_bombe == num_caselle_ignote:
            P1=0
            P2=0
            P3=0
            P_boom=1
            P_safe=0
        else:
            P_boom = num_bombe / num_caselle_ignote
            P_safe = 1-P_boom
            P1, P2, P3 = studio_possibili_casi(num_caselle_ignote, num_bombe, somma_punteggi)

        struttura["P_boom"] = P_boom
        struttura["P1"] =  P1
        struttura["P2"] =  P2
        struttura["P3"] =  P3
        struttura["P_safe"] = P_safe

        # AGGIORNAMENTO CASELLE RIGA
        for indice_colonna in range(5):
            self.caselle[n][indice_colonna].update_prob(prob_riga=self.valori_riga[n], prob_colonna=self.valori_colonna[indice_colonna])


        

    def update_colonna(self, n: int):
        """
        Aggiorna i valori di probabilità delle caselle di una colonna
        """
        struttura = self.valori_colonna[n]
        num_bombe = struttura["num_bombe"]
        num_caselle_ignote = struttura["num_caselle_ignote"]
        somma_punteggi = struttura["somma_punteggi"]


        if num_bombe == num_caselle_ignote:
            P1=0
            P2=0
            P3=0
            P_boom=1
            P_safe=0
        else:
            P_boom = num_bombe / num_caselle_ignote
            P_safe = 1-P_boom
            P1, P2, P3 = studio_possibili_casi(num_caselle_ignote, num_bombe, somma_punteggi)

        struttura["P_boom"] = P_boom
        struttura["P1"] =  P1
        struttura["P2"] =  P2
        struttura["P3"] =  P3
        struttura["P_safe"] = P_safe

        # AGGIORNAMENTO CASELLE COLONNA
        for indice_riga in range(5):
            self.caselle[indice_riga][n].update_prob(prob_riga=self.valori_riga[indice_riga], prob_colonna=self.valori_colonna[n])


    def update_tutte_le_righe(self):
        for i in range(5):
            self.update_riga(i)

    def set_casella_val(self, riga : int, colonna : int, valore):
        # setta il valore della casella e aggiorna di conseguenza la riga e la colonna 
        casella = self.caselle[riga][colonna]
        casella.value = valore
        self.valori_riga[riga]["num_caselle_ignote"]-=1
        self.valori_colonna[colonna]["num_caselle_ignote"]-=1
        self.update_riga(riga)
        self.update_colonna(colonna)