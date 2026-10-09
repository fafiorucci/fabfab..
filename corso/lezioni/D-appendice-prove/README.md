# Appendice D · Prove d'esame simulate

Venti esami completi (197 slide) in due parti, costruiti come le prove del DM 323/2021, art. 6.

## Parte 1 · Prove entro 12 miglia (10 prove)

- **quiz di elementi di carteggio**: un esercizio ufficiale entro 12 miglia (elenco DD 131/2022, sigla 4.1.1, 50 esercizi sulla carta 5/D), con i suoi 5 quesiti: distanza, ora di arrivo o velocità, carburante, coordinate di partenza e di arrivo; 20 minuti, almeno 4 su 5; esercizi presi a rotazione dai tre settori della carta;
- **quiz base**: 20 domande ripartite per tema come nell'All. C;
- **quiz vela**: 5 domande;
- **correzione**: intervalli ufficiali dei 5 quesiti e griglia delle lettere per i quiz.

## Parte 2 · Prove oltre 12 miglia (10 prove)

- **carteggio**: 4 esercizi ufficiali (DD 131/2022), uno per argomento; prove 5 e 10 sulla carta 42/D, le altre sulla 5/D; 60 minuti, almeno 3 su 4;
- **quiz base**: 20 domande ripartite per tema come nell'All. C (navigazione 4, COLREG 2, sicurezza 3, normativa 3, manovra 4, scafo 1, meteo 2, motori 1);
- **quiz vela**: 5 domande;
- **correzione**: risposte ufficiali del carteggio con la lezione dove l'esercizio è risolto, griglia delle lettere per i quiz.

Nessun quiz o esercizio si ripete, né dentro una parte né tra le due parti; si preferiscono domande non usate nelle verifiche delle lezioni. Le prove oltre 12 miglia sono identiche a quelle della versione precedente: `genera.py` le legge da `prove_oltre.json` (id degli esercizi e numeri dei quiz), così non cambiano se cambiano le verifiche delle lezioni. Le prove entro 12 miglia usano un seme fisso ed escludono le domande già usate nelle prove oltre. `prove.json` (copia di `prove_oltre.json`) e `prove_entro.json` elencano il contenuto delle due parti.
