from redsentinel.scanners.nmap_scan import run_nmap
from redsentinel.scanners.nikto_scan import run_nikto
from redsentinel.scanners.whatweb_scan import run_whatweb


def run_all_scans(target):
    results = []

    results.append(run_nmap(target))
    results.append(run_nikto(target))
    results.append(run_whatweb(target))

    return results

