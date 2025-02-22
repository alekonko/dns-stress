#!/usr/bin/env python3

import time
import socket
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import json
import random
from tqdm import tqdm
import asyncio
import aiohttp
import yaml

def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def load_domains(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

async def async_test_dns_resolution(dns_servers, domains, num_tests, output_file, show_graph=False, summary_only=False, silent_mode=False):
    results = {server: [] for server in dns_servers}
    
    if not domains:
        print("Errore: Nessun dominio disponibile per il test.")
        return
    
    progress_bar = tqdm(total=num_tests * len(dns_servers), desc="Testing DNS resolution", unit="req")
    summary_data = {server: [] for server in dns_servers}
    
    async def resolve_domain(session, server, domain):
        start_time = time.time()
        try:
            await session.get(f"http://{domain}", timeout=2)
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        except Exception:
            elapsed_time = None  # Failed resolution
        results[server].append(elapsed_time)
        summary_data[server].append(elapsed_time)
        
        if not silent_mode:
            tqdm.write(f"{domain} - {server}: {elapsed_time} ms")
        
        progress_bar.update(1)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_tests):
            domain = random.choice(domains)
            for server in dns_servers:
                tasks.append(resolve_domain(session, server, domain))
        await asyncio.gather(*tasks)
    
    progress_bar.close()
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    
    summarize_results(results)
    
    if show_graph:
        plot_results(results)

def test_dns_resolution(dns_servers, domains, num_tests, output_file, show_graph=False, summary_only=False, silent_mode=False):
    results = {server: [] for server in dns_servers}
    
    if not domains:
        print("Errore: Nessun dominio disponibile per il test.")
        return
    
    progress_bar = tqdm(total=num_tests * len(dns_servers), desc="Testing DNS resolution", unit="req")
    summary_data = {server: [] for server in dns_servers}
    
    for _ in range(num_tests):
        domain = random.choice(domains)
        for server in dns_servers:
            start_time = time.time()
            try:
                socket.setdefaulttimeout(2)
                socket.getaddrinfo(domain, 80, proto=socket.IPPROTO_TCP)
                elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
            except socket.gaierror:
                elapsed_time = None  # Failed resolution
            results[server].append(elapsed_time)
            summary_data[server].append(elapsed_time)
            
            if not silent_mode:
                tqdm.write(f"{domain} - {server}: {elapsed_time} ms")
            
            progress_bar.update(1)
    
    progress_bar.close()
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    
    summarize_results(results)
    
    if show_graph:
        plot_results(results)

def summarize_results(results):
    print("\nSummary of DNS Test Results:")
    for server, times in results.items():
        valid_times = list(filter(None, times))
        if valid_times:
            print(f"{server}: Avg {np.mean(valid_times):.2f} ms, Min {min(valid_times):.2f} ms, Max {max(valid_times):.2f} ms")
        else:
            print(f"{server}: No successful resolutions")

def plot_results(results):
    servers = list(results.keys())
    values = [list(filter(None, results[server])) for server in servers]
    means = [np.mean(val) if val else 0 for val in values]
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, means, color=['blue', 'green', 'red'])
    plt.xlabel("DNS Servers")
    plt.ylabel("Avg Response Time (ms)")
    plt.title("DNS Resolution Performance")
    plt.grid(axis='y')
    plt.show(block=True)

def load_and_plot(output_file):
    with open(output_file, "r") as f:
        results = json.load(f)
    plot_results(results)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file", type=str, default="config.yaml", help="Path to the configuration file")
    parser.add_argument("--show-graph", action="store_true", help="Show the results graph")
    parser.add_argument("--summary-only", action="store_true", help="Show only the summary results")
    parser.add_argument("--load-graph", action="store_true", help="Load and show graph from saved results")
    parser.add_argument("--silent-mode", action="store_true", help="Disable per-request output, show progress bar instead")
    parser.add_argument("--async-mode", action="store_true", help="Run tests in asynchronous mode")
    args = parser.parse_args()
    
    config = load_config(args.config_file)
    dns_servers = config["dns_servers"]
    num_tests = config["num_tests"]
    output_file = config["output_file"]
    domains_file = config["domains_file"]
    domains = load_domains(domains_file)
    
    if args.load_graph:
        load_and_plot(output_file)
    else:
        if args.async_mode:
            asyncio.run(async_test_dns_resolution(dns_servers, domains, num_tests, output_file, args.show_graph, args.summary_only, args.silent_mode))
        else:
            test_dns_resolution(dns_servers, domains, num_tests, output_file, args.show_graph, args.summary_only, args.silent_mode)

