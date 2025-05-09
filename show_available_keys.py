#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anilist API Key Explorer

This script shows all available keys/fields in the Anilist API responses.
"""

import json
from anilist_client import AnilistClient


def print_nested_keys(data, prefix="", level=0):
    """
    Recursively print all keys in a nested dictionary or list.
    
    Args:
        data: The data to explore (dict, list, or other type)
        prefix: Prefix for the current key path
        level: Current nesting level
    """
    indent = "  " * level
    
    if isinstance(data, dict):
        print(f"{indent}{prefix} (Object):")
        for key, value in data.items():
            new_prefix = f"{key}"
            print_nested_keys(value, new_prefix, level + 1)
    
    elif isinstance(data, list) and data and isinstance(data[0], dict):
        print(f"{indent}{prefix} (Array of Objects):")
        # Just use the first item as an example
        print_nested_keys(data[0], "Item", level + 1)
    
    elif isinstance(data, list):
        if data:
            print(f"{indent}{prefix} (Array): Example value: {data[0]}")
        else:
            print(f"{indent}{prefix} (Empty Array)")
    
    else:
        value_str = str(data)
        # if len(value_str) > 50:
        #     value_str = value_str[:47] + "..."
        print(f"{indent}{prefix}: {value_str}")


def explore_anime_details():
    """Explore the structure of anime details response."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("ANIME DETAILS STRUCTURE")
    print("=" * 50)
    
    # Fetch a popular anime (Demon Slayer)
    result = client.get_anime_by_id(101922)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    # Print the structure of the Media object
    print("\nMedia Object Structure:")
    print_nested_keys(result["data"]["Media"])


def explore_search_results():
    """Explore the structure of search results response."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("SEARCH RESULTS STRUCTURE")
    print("=" * 50)
    
    # Search for a popular anime
    result = client.search_anime("Attack on Titan", per_page=1)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    # Print the structure of the Page object
    print("\nPage Object Structure:")
    print_nested_keys(result["data"]["Page"])


def explore_seasonal_anime():
    """Explore the structure of seasonal anime response."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("SEASONAL ANIME STRUCTURE")
    print("=" * 50)
    
    # Get seasonal anime
    result = client.get_seasonal_anime(2023, "WINTER", per_page=1)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    # Print the structure of the Page object
    print("\nPage Object Structure:")
    print_nested_keys(result["data"]["Page"])


def main():
    """Main function to explore Anilist API response structure."""
    print("Exploring Anilist API Response Structure")
    print("This script will show you the available keys/fields in the Anilist API responses.")
    
    explore_anime_details()
    explore_search_results()
    explore_seasonal_anime()
    
    print("\nNote: You can customize the GraphQL queries in anilist_client.py to request additional fields.")


if __name__ == "__main__":
    main()
