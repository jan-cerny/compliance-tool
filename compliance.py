#!/usr/bin/python3

import argparse
import compliance.profiles
import compliance.remediate
import compliance.scan


def parse_args():
    parser = argparse.ArgumentParser(description="Compliance Tool")
    subparsers = parser.add_subparsers(required=True)

    parser_list = subparsers.add_parser("list", help="Lists available profiles for this system")
    parser_list.set_defaults(func=compliance.profiles.list_profiles)

    parser_scan = subparsers.add_parser("scan", help="Perform a compliance scan")
    parser_scan.set_defaults(func=compliance.scan.scan)
    parser_scan.add_argument("profile", help="Profile ID. Available profiles can be listed using the 'list' sub-command.")
    parser_scan.add_argument("--report", help="Path where a HTML report should be stored")
    parser_scan.add_argument("--json", help="Path where a JSON report should be stored")

    parser_remediate = subparsers.add_parser("remediate", help="Remediate your system")
    parser_remediate.set_defaults(func=compliance.remediate.remediate)
    parser_remediate.add_argument("profile", help="Profile ID. Available profiles can be listed using the 'list' sub-command.")

    parser_info = subparsers.add_parser("info", help="Detailed information about a profile")
    parser_info.set_defaults(func=compliance.profiles.info_profile)
    parser_info.add_argument("profile", help="Profile ID. Available profiles can be listed using the 'list' sub-command.")
    parser_info.add_argument("-r", "--list-rules", action="store_true", help="List rules selected by the given profile")

    return parser.parse_args()

def main():
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()