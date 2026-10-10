#!/usr/bin/env python3
"""Read-only check of the public repository inventory and exported release bytes."""
import argparse
import sys
import zipfile

# Keep this audit read-only, including when importing the shared packaging helpers.
sys.dont_write_bytecode = True
from package_release import ROOT, check_repository_scope, load_inventory, verify_release


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope-only', action='store_true',
                        help='Check declared files before rebuilding the release archive')
    args = parser.parse_args()
    data = load_inventory()
    # The supplementary archive and a private publication/ snapshot may be
    # outside their own Git root; their exported bytes are still fully audited.
    check_repository_scope(data, require_git=False)
    if not args.scope_only:
        verify_release(data)
    print('Publication scope verified' + ('' if args.scope_only else '; archive and byte hashes verified'))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        raise SystemExit(str(error)) from error
