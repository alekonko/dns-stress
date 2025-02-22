# DNS Stress Test

Questo progetto esegue test di risoluzione DNS utilizzando server DNS specificati e domini di test.

## Requisiti

- Python 3.x
- Moduli Python: `aiohttp`, `tqdm`, `matplotlib`, `numpy`, `pyyaml`

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

3. Installa i moduli richiesti utilizzando `pip`:
    ```sh
    pip install aiohttp tqdm matplotlib numpy pyyaml
    ```

4. (Opzionale) Installa `tkinter` per il backend di Matplotlib:
    ```sh
    sudo apt-get install python3-tk
    ```

## Scripts

### dns-stress.py

This script performs DNS resolution tests using both synchronous and asynchronous methods. It supports calculating and displaying various statistics, including average, minimum, maximum, 50th percentile, 90th percentile, and 95th percentile response times.

#### Usage

```bash
./dns-stress.py --config-file <path_to_config> [options]
```

#### Options

- `--config-file`: Path to the configuration file (default: `config.yaml`).
- `--show-graph`: Show the results graph.
- `--summary-only`: Show only the summary results.
- `--load-graph`: Load and show graph from saved results.
- `--silent-mode`: Disable per-request output, show progress bar instead.
- `--async-mode`: Run tests in asynchronous mode.

### dns-stress-v2.py

This script is similar to `dns-stress.py` but includes additional features for calculating and displaying percentile values (50th, 90th, and 95th percentiles) in the summary and graphs.

#### Usage

```bash
./dns-stress-v2.py --config-file <path_to_config> [options]
```

#### Options

- `--config-file`: Path to the configuration file (default: `config.yaml`).
- `--show-graph`: Show the results graph.
- `--summary-only`: Show only the summary results.
- `--load-graph`: Load and show graph from saved results.
- `--silent-mode`: Disable per-request output, show progress bar instead.
- `--async-mode`: Run tests in asynchronous mode.

## Configuration

Both scripts use a configuration file (`config.yaml` by default) to specify the DNS servers, number of tests, output file, and domains file.

Example `config.yaml`:

```yaml
dns_servers:
  - 8.8.8.8
  - 8.8.4.4
num_tests: 100
output_file: results.json
domains_file: domains.txt
```

## Domains File

The domains file should contain a list of domains to test, one per line.

Example `domains.txt`:

```
example.com
google.com
yahoo.com
```

## Output

The results are saved in a JSON file specified in the configuration file. The summary and graphs can be displayed based on the provided options.

## Summary

- `dns-stress.py`: Basic DNS resolution testing with average, min, max, and 50th percentile statistics.
- `dns-stress-v2.py`: Enhanced DNS resolution testing with additional 90th and 95th percentile statistics.