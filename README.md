# TODO

## 1 __init__ class Tabella
  Sistemare __init__ della classe Tabella: quando genero un istanza specificano i valori di righe e colonne devo anche aggiornare i valori di probabilità chiamando update_riga update_colonna.

## 2 update_riga update_colonna class Tabella
  riscrivere pipeline:
  1. conto caselle ignote e aggiorno num_caselle_ignote
  2. calcolo le prob e le aggiorno (P_boom P1 P2...)
  3. chiamo update_riga() per aggiornare le prob delle caselle della riga

## 3 studio_possibili_casi()
  Da riscrivere totalmente
