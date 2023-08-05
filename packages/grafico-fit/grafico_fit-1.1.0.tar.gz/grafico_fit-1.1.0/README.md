# Generazione grafici da dati in un foglio Excel
Il package contiene due funzioni:
- `fit()`
- `tabella()`
### fit
La funzione fit crea:
- un file pdf contenente il grafico di fit
- un file pdf contenente il grafico dei residui
- un file LaTeX contenete la tabella dei parametri ottimali della funzione usata per il fit
I dati sono presi da colonne di un foglio Excel.


### tabella
La funzione crea un file .tex contenente una tabella i cui valori vengono estratti da un foglio Excel

##### Requirement
per compilare il file LaTeX contenete una tabella generata da `tabella()` è necessario importare i package:
- `\usepackage{booktabs}`
- `\usepackage{longtable}`