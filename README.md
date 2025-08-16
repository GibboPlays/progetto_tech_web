# progetto_tech_web

Librerie principali usate:
- crispy_forms: per rendere più facile lo strutturare dei form nell'HTML;
- crispy_bootstrap4: insieme a crispy_forms per rendere la grafica più accattivante;
- gestione: per la gestione delle informazioni del progetto;
- channels: per poter usare i WebSockets per lo scambio di informazioni asincrone (insieme a daphne);
- freezegun: per aiutare nel gestire i test che avessero a che fare con l'ora dell'utente;

Il progetto si preoccupa del creare un sito web riguardante una palestra, che è in grado di gestire principalmente i corsi delle varie discipline offerte dalla palestra.
Gli utenti possibili per la palestra sono:
- Atleta: può usufruire dei servizi della palestra, prenotando o disdicendo i corsi inseriti dai personal trainers
- Personal Trainer: oltre a fare ciò che può fare un'atleta, gestisce le discipline e i corsi;
- Superuser: oltre a fare tutto ciò possono fare gli altri utenti, può iscrivere i personal trainers (tramite "Iscrivi un personal trainer"), che quindi dovranno solo accedere con le credenziali date

La palestra quindi viene popolata di discipline e da loro corsi:
- Disciplina: ha un nome e un personal trainer;
- Corso: ha una discipline e rappresenta la lezione fisica della disciplina, quindi ha una data, un'ora, un massimo di partecipanti e l'elenco degli utenti che l'hanno prenotato

Appena entrati nella home del sito da utente anonimo si può registrare (tramite "Registrati") mettendo le proprie credenziali, oppure se si ha già un account da utente (non superutente) si può accedere (tramite "Login"). Se invece si è già loggati si può fare logout (tramite "Logout"). Si possono gestire le cose riguardanti il sito (tramite "Gestione"), per il resto ci sono altre opzioni che sono presenti già in gestione. Nel contesto di gestione possiamo eseguire varie operazioni, si possono guardare i corsi giornalieri disponibili (tramite "Corsi per giorno"), dove abbiamo i corsi del giorno, con le frecce avanti e indietro scorriamo i giorni, volendo si può anche cercare un giorno specifico tramite la barra di ricerca. Sempre in gestione, possiamo anche vedere la lista generale delle discipline (tramite "Lista delle discipline"), che cliccando sopra una disciplina si vede la lista dei corsi inerenti ad essi, che possono essere prenotati (tramite "Prenota"). Ancora in gestione possiamo cercare una disciplina (tramite "Cerca una disciplina") in base a dei filtri (per nome o per personal trainer), ottentendo quindi una lista di discipline, uguale a quella che troviamo nel servizio precedente, ma che rispecchia questi requisiti. L'ultima opzione disponibile a tutti in gestione è la tua situazione (tramite "La mia situazione"), dove si può vedere l'elenco dei corsi prenotati, e si possono anche disdire (tramite "Disdici").
Le opzioni che fornisce gestione utilizzabili solo dai personal trainers e in caso dal superuser sono: puoi vedere la situazione della palestra, puoi aggiungere una disciplina e puoi aggiungere un corso.
Per quanto riguarda la situazione della palestra(tramite "Situazione Palestra"), vengono mostrati tutte le discipline della palestra, che si possono eliminare (tramite "Elimina Disciplina"), modificare (tramite "Modifica Disciplina") o visualizzare i suoi dettagli(tramite "Visualizza Dettagli Aggiuntivi"), che sarebbero i suoi corsi, a sua volta un corso si può eliminare (tramite "Elimina Corso") o modificare(tramite "Modifica Corso"). Mentre per quanto riguarda l'aggiungere una disciplina (tramite "Aggiungi una disciplina"), si specifica il nome di essa e si seleziona un personal trainer che la terrà. Similmente per un corso (tramite "Aggiungi un corso"), si specifica la disciplina di cui fa parte, la data, l'ora e il numero massimo di partecipanti.

