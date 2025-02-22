#!/usr/bin/env python3

import random
import asyncio
import aiohttp
import json
import time
import socket
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import yaml
import argparse
from dns_stress_lib import load_config, load_domains, async_test_single_dns, test_single_dns, summarize_results, plot_results, summarize_p90_results, plot_p90_results, load_and_plot

if __name__ == "__main__":
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
    
    results = {}
    
    if args.load_graph:
        load_and_plot(output_file)
    else:
        for server in dns_servers:
            if args.async_mode:
                results[server] = asyncio.run(async_test_single_dns(server, domains, num_tests, args.silent_mode))
            else:
                results[server] = test_single_dns(server, domains, num_tests, args.silent_mode)
        
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        
        summarize_results(results)
        summarize_p90_results(results)
        
        if args.show_graph:
            plot_results(results)
            plot_p90_results(results)