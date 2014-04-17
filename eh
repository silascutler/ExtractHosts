#!/usr/bin/env python
from ExtractHosts import get_version, scan_paths, scan_file_handle, _test_extract_hosts_from_string
from sys import stdin

results = {}


def print_result(file, domain, show_files, hide_duplicates):
    if hide_duplicates:
        if show_files:
            key = file
        else:
            key = "-"
        if key in results:
            if domain in results[key]:
                return
        if key not in results:
            results[key] = []
        if domain not in results[key]:
            results[key].append(domain)
    if show_files:
        print "{0}\t{1}".format(file, domain)
    else:
        print domain


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        prog=__file__,
        description="Identifies and extracts domains and IPs from files",
        version="%(prog)s v" + get_version() + " by Brian Wallace (@botnet_hunter)",
        epilog="%(prog)s v" + get_version() + " by Brian Wallace (@botnet_hunter)"
    )
    parser.add_argument('path', metavar='path', type=str, nargs='*', default=None,
                        help="Paths to files or directories to scan (if not supplied, stdin is the file being read)")
    parser.add_argument('-r', '--recursive', default=False, required=False, action='store_true',
                        help="Scan paths recursively")
    parser.add_argument('-f', '--show-files', default=False, required=False, action='store_true',
                        help="Show file names along with results")
    parser.add_argument('-d', '--hide-duplicates', default=False, required=False, action='store_true',
                        help="Hide duplicate results (hides per file when show-files is enabled)")
    parser.add_argument('-T', '--test', default=False, required=False, action='store_true',
                        help="Run some quick self tests")

    args = parser.parse_args()

    if args.test:
        _test_extract_hosts_from_string()
        exit()

    show_files = args.show_files
    hide_duplicates = args.hide_duplicates

    if len(args.path) == 0:
        with stdin as fh:
            for domain in scan_file_handle(fh):
                print_result("stdin", domain, show_files, hide_duplicates)
    else:
        for (f, domain) in scan_paths(args.path, args.recursive):
            print_result(f, domain, show_files, hide_duplicates)