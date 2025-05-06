#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anilist API Custom Query Runner

This script allows you to run custom GraphQL queries against the Anilist API.
"""

import json
import argparse
from anilist_client import AnilistClient


def format_json(data):
    """Format JSON data for better readability."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def run_query_from_string(query_string, variables=None):
    """Run a GraphQL query from a string."""
    client = AnilistClient()
    result = client.run_query(query_string, variables)
    return result


def run_query_from_file(query_file, variables=None):
    """Run a GraphQL query from a file."""
    with open(query_file, 'r', encoding='utf-8') as f:
        query_string = f.read()
    
    return run_query_from_string(query_string, variables)


def main():
    """Main function to run custom GraphQL queries."""
    parser = argparse.ArgumentParser(description='Run custom GraphQL queries against the Anilist API')
    
    # Query source group (mutually exclusive)
    query_source = parser.add_mutually_exclusive_group(required=True)
    query_source.add_argument('-q', '--query', help='GraphQL query string')
    query_source.add_argument('-f', '--file', help='File containing GraphQL query')
    
    # Variables
    parser.add_argument('-v', '--variables', help='JSON string of variables')
    parser.add_argument('-vf', '--variables-file', help='File containing JSON variables')
    
    # Output options
    parser.add_argument('-o', '--output', help='Output file for results')
    
    args = parser.parse_args()
    
    # Parse variables
    variables = None
    if args.variables:
        variables = json.loads(args.variables)
    elif args.variables_file:
        with open(args.variables_file, 'r', encoding='utf-8') as f:
            variables = json.loads(f.read())
    
    # Run query
    if args.query:
        result = run_query_from_string(args.query, variables)
    else:  # args.file
        result = run_query_from_file(args.file, variables)
    
    # Output results
    formatted_result = format_json(result)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(formatted_result)
        print(f"Results saved to {args.output}")
    else:
        print(formatted_result)


if __name__ == "__main__":
    # If no arguments are provided, show example usage
    import sys
    if len(sys.argv) == 1:
        print("""
Anilist API Custom Query Runner
===============================

This script allows you to run custom GraphQL queries against the Anilist API.

Example Usage:
-------------

1. Run a simple query directly:

   python custom_query.py --query '{ Media(id: 1) { id title { romaji } } }'

2. Run a query from a file:

   python custom_query.py --file query.graphql

3. Run a query with variables:

   python custom_query.py --query 'query ($id: Int) { Media(id: $id) { id title { romaji } } }' --variables '{"id": 1}'

4. Save results to a file:

   python custom_query.py --file query.graphql --variables-file vars.json --output results.json

Example Query File (query.graphql):
---------------------------------
query ($id: Int) {
  Media(id: $id) {
    id
    title {
      romaji
      english
      native
    }
    episodes
    genres
  }
}

Example Variables File (vars.json):
---------------------------------
{
  "id": 1
}
        """)
    else:
        main()
