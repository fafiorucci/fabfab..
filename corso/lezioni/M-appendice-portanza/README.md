# Appendice M · La portanza

La portanza dall'ala alla vela (25 slide): portanza e resistenza, la mano fuori dal finestrino, Newton (flusso deviato, upwash e downwash), Bernoulli (pressioni), il mito del «percorso più lungo», angolo di incidenza, stallo, da cosa dipende (½ ρ V² S CL), la vela come ala, propulsione e scarroccio, la deriva come ala in acqua, portanza e andature, i filetti, grasso e magro, la fessura tra fiocco e randa, cosa si dice sul web. Tre verifiche con quiz ufficiali di vela (2.1.1, 2.3.1).

I disegni del flusso sono calcolati: `flow.py` risolve il flusso potenziale attorno a profili di Joukowski con la condizione di Kutta (linee di corrente, pressioni sulla superficie, tempi di percorrenza) e scrive `flow_lines.json` (serve numpy e matplotlib solo per rigenerarlo). `genera.py` (con `app_common.py`) legge il JSON e produce il mazzo in `deck/project`.

Fonti web: NASA Glenn Research Center, «Incorrect Lift Theory» e «Bernoulli and Newton»; Arvel Gentry, «A Review of Modern Sail Theory» (effetto fessura, filetti).
