# DNS Stress Test

Questo progetto esegue test di risoluzione DNS su una lista di domini utilizzando diversi server DNS. Può eseguire i test in modalità sincrona o asincrona e visualizzare i risultati in un grafico.

## Requisiti

Assicurati di avere Python 3.6 o superiore installato sul tuo sistema.

## Installazione

1. Clona il repository:
    ```sh
    git clone https://github.com/aleconco/dns-stress.git
    cd dns-stress
    ```

2. Crea un ambiente virtuale e attivalo:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Installa le dipendenze:
    ```sh
    pip install -r requirements.txt
    ```

4. (Opzionale) Installa `tkinter` per il backend di Matplotlib:
    ```sh
    sudo apt-get install python3-tk
    ```

## Utilizzo

### Esecuzione dei test

Per eseguire i test di risoluzione DNS, utilizza il seguente comando:

```sh
python dns-stress.py
```

### Parametri

Puoi specificare i seguenti parametri durante l'esecuzione del comando:

- `-d`, `--domains`: Specifica il file contenente la lista di domini (default: `domains.txt`).
- `-s`, `--servers`: Specifica il file contenente la lista di server DNS (default: `servers.txt`).
- `-m`, `--mode`: Specifica la modalità di esecuzione (`sync` per sincrono, `async` per asincrono; default: `sync`).
- `-o`, `--output`: Specifica il file di output per i risultati (default: `results.csv`).

Esempio di utilizzo con parametri:

```sh
python dns-stress.py -d mydomains.txt -s myservers.txt -m async -o myresults.csv
```