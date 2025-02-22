import time
import socket
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

async def async_test_single_dns(server, domains, num_tests, silent_mode=False):
    results = []
    progress_bar = tqdm(total=num_tests, desc=f"Testing {server}", unit="req")
    
    async def resolve_domain(session, domain):
        start_time = time.time()
        try:
            await session.get(f"http://{domain}", timeout=2)
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        except Exception:
            elapsed_time = None  # Failed resolution
        results.append(elapsed_time)
        
        if not silent_mode:
            tqdm.write(f"{domain} - {server}: {elapsed_time} ms")
        
        progress_bar.update(1)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_tests):
            domain = random.choice(domains)
            tasks.append(resolve_domain(session, domain))
        await asyncio.gather(*tasks)
    
    progress_bar.close()
    return results

def test_single_dns(server, domains, num_tests, silent_mode=False):
    results = []
    progress_bar = tqdm(total=num_tests, desc=f"Testing {server}", unit="req")
    
    for _ in range(num_tests):
        domain = random.choice(domains)
        start_time = time.time()
        try:
            socket.setdefaulttimeout(2)
            socket.getaddrinfo(domain, 80, proto=socket.IPPROTO_TCP)
            elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        except socket.gaierror:
            elapsed_time = None  # Failed resolution
        results.append(elapsed_time)
        
        if not silent_mode:
            tqdm.write(f"{domain} - {server}: {elapsed_time} ms")
        
        progress_bar.update(1)
    
    progress_bar.close()
    return results

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
            random.shuffle(dns_servers)  # Randomizza l'ordine dei server DNS
            for server in dns_servers:
                tasks.append(resolve_domain(session, server, domain))
        await asyncio.gather(*tasks)
    
    progress_bar.close()
    
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    
    summarize_results(results, "parallel")
    
    if show_graph:
        plot_results(results, "parallel")
    
    return results

def test_dns_resolution(dns_servers, domains, num_tests, output_file, show_graph=False, summary_only=False, silent_mode=False):
    results = {server: [] for server in dns_servers}
    
    if not domains:
        print("Errore: Nessun dominio disponibile per il test.")
        return results
    
    progress_bar = tqdm(total=num_tests * len(dns_servers), desc="Testing DNS resolution", unit="req")
    summary_data = {server: [] for server in dns_servers}
    
    for _ in range(num_tests):
        domain = random.choice(domains)
        random.shuffle(dns_servers)  # Randomizza l'ordine dei server DNS
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
    
    summarize_results(results, "parallel")
    
    if show_graph:
        plot_results(results, "parallel")
    
    return results

def summarize_results(results, benchmode):
    print(f"\nSummary of DNS Test Results (Benchmode: {benchmode}):")
    for server, times in results.items():
        valid_times = list(filter(None, times))
        if valid_times:
            print(f"{server}: Avg {np.mean(valid_times):.2f} ms, Min {min(valid_times):.2f} ms, Max {max(valid_times):.2f} ms, 50th Percentile {np.percentile(valid_times, 50):.2f} ms, 95th Percentile {np.percentile(valid_times, 95):.2f} ms")
        else:
            print(f"{server}: No successful resolutions")

def plot_results(results, benchmode):
    servers = list(results.keys())
    values = [list(filter(None, results[server])) for server in servers]
    means = [np.mean(val) if val else 0 for val in values]
    p50s = [np.percentile(val, 50) if val else 0 for val in values]
    p95s = [np.percentile(val, 95) if val else 0 for val in values]
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, means, color='blue', label='Average')
    plt.bar(servers, p50s, color='green', alpha=0.5, label='50th Percentile')
    plt.bar(servers, p95s, color='orange', alpha=0.5, label='95th Percentile')
    plt.xlabel("DNS Servers")
    plt.ylabel("Response Time (ms)")
    plt.title(f"DNS Resolution Performance (Benchmode: {benchmode})")
    plt.legend()
    plt.grid(axis='y')
    plt.show(block=True)

def summarize_p90_results(results, benchmode):
    print(f"\n90th Percentile DNS Test Results (Benchmode: {benchmode}):")
    for server, times in results.items():
        valid_times = list(filter(None, times))
        if valid_times:
            print(f"{server}: 90th Percentile {np.percentile(valid_times, 90):.2f} ms")
        else:
            print(f"{server}: No successful resolutions")

def plot_p90_results(results, benchmode):
    servers = list(results.keys())
    values = [list(filter(None, results[server])) for server in servers]
    p90s = [np.percentile(val, 90) if val else 0 for val in values]
    
    plt.figure(figsize=(10, 6))
    plt.bar(servers, p90s, color='red', alpha=0.5, label='90th Percentile')
    plt.xlabel("DNS Servers")
    plt.ylabel("Response Time (ms)")
    plt.title(f"90th Percentile DNS Resolution Performance (Benchmode: {benchmode})")
    plt.legend()
    plt.grid(axis='y')
    plt.show(block=True)

def load_and_plot(output_file, benchmode):
    with open(output_file, "r") as f:
        results = json.load(f)
    plot_results(results, benchmode)