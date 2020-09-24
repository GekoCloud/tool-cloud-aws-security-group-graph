#!/usr/bin/env python

import argparse
from core.graph_manager import SGGraph

# Argparsing helper class
class keyvalue(argparse.Action):
    # Constructor calling
    def __call__(self, parser, namespace, values, option_string = None):
        setattr(namespace, self.dest, dict())
        for value in values:
            # split it into key and value
            key, value = value.split('=')
            # assign into dictionary
            getattr(namespace, self.dest)[key] = value


def _get_args():
    parser = argparse.ArgumentParser(
        description="""Displays your current AWS SecurityGroups dependencies as a Directed Graph. It's
        specially helpful when trying to have an overview of the current status, being
        able to easily recognize the dependencies between them and quickly identify any
        security issue"""
    )
    parser.add_argument(
        "--aws-profile",
        default="default",
        required=False,
        help="Name of the AWS profile you have set on your .aws/credentials file"
    )
    parser.add_argument(
        "--aws-region",
        default="eu-west-1",
        required=False,
        help="Slug-name for the AWS region you want to analyze (E.g. 'eu-west-1')"
    )
    parser.add_argument(
        "--ignore",
        default="[]",
        required=False,
        nargs='+',
        help="Space-separated list of substrings to look for in the Security Groups' names in order to ignore them"
    )
    parser.add_argument(
        "--color",
        required=False,
        metavar="PORT=COLOR",
        nargs='+',
        action = keyvalue,
        help="Set the color for a certain port"
    )

    return parser.parse_args()

def _main():
    args = _get_args()
    aws_profile = args.aws_profile
    aws_region = args.aws_region
    ignore_strs = args.ignore
    colors = args.color
    graph = SGGraph(aws_profile, aws_region, ignore_strs, colors)
    graph.sgs_2_graph()

if __name__ == "__main__":
    _main()
