#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anilist API Examples

This script demonstrates various examples of fetching specific information from the Anilist API.
"""

import json
from anilist_client import AnilistClient


def example_get_anime_basic_info():
    """Example: Get basic information about an anime."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("EXAMPLE: BASIC ANIME INFORMATION")
    print("=" * 50)
    
    # Define a custom query to get basic information
    query = """
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
                native
            }
            episodes
            duration
            status
            season
            seasonYear
            format
            genres
            averageScore
        }
    }
    """
    
    # Fetch data for Demon Slayer
    variables = {"id": 101922}
    result = client.run_query(query, variables)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    anime = result["data"]["Media"]
    
    print("Basic Anime Information:")
    print(f"Title: {anime['title']['romaji']} / {anime['title']['native']}")
    print(f"Episodes: {anime['episodes']}")
    print(f"Duration: {anime['duration']} minutes per episode")
    print(f"Status: {anime['status']}")
    print(f"Season: {anime['season']} {anime['seasonYear']}")
    print(f"Format: {anime['format']}")
    print(f"Genres: {', '.join(anime['genres'])}")
    print(f"Average Score: {anime['averageScore']}/100")


def example_get_anime_characters():
    """Example: Get characters for an anime."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("EXAMPLE: ANIME CHARACTERS")
    print("=" * 50)
    
    # Define a custom query to get character information
    query = """
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            title {
                romaji
            }
            characters(sort: ROLE, perPage: 5) {
                edges {
                    node {
                        id
                        name {
                            full
                            native
                        }
                        gender
                        age
                    }
                    role
                    voiceActors(language: JAPANESE) {
                        id
                        name {
                            full
                            native
                        }
                    }
                }
            }
        }
    }
    """
    
    # Fetch data for Attack on Titan
    variables = {"id": 16498}  # Attack on Titan ID
    result = client.run_query(query, variables)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    anime = result["data"]["Media"]
    
    print(f"Characters in {anime['title']['romaji']}:")
    
    for i, edge in enumerate(anime["characters"]["edges"], 1):
        character = edge["node"]
        print(f"\n{i}. {character['name']['full']} ({character['name']['native']})")
        print(f"   Role: {edge['role']}")
        
        if character.get("gender"):
            print(f"   Gender: {character['gender']}")
        
        if character.get("age"):
            print(f"   Age: {character['age']}")
        
        if edge["voiceActors"]:
            va = edge["voiceActors"][0]
            print(f"   Voice Actor: {va['name']['full']} ({va['name']['native']})")


def example_get_studio_works():
    """Example: Get works by a specific studio."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("EXAMPLE: STUDIO WORKS")
    print("=" * 50)
    
    # Define a custom query to get studio information
    query = """
    query ($id: Int) {
        Studio (id: $id) {
            id
            name
            isAnimationStudio
            media(sort: POPULARITY_DESC, perPage: 5) {
                nodes {
                    id
                    title {
                        romaji
                    }
                    format
                    seasonYear
                    averageScore
                }
            }
        }
    }
    """
    
    # Fetch data for ufotable (studio that made Demon Slayer)
    variables = {"id": 43}  # ufotable ID
    result = client.run_query(query, variables)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    studio = result["data"]["Studio"]
    
    print(f"Studio: {studio['name']}")
    print(f"Animation Studio: {'Yes' if studio['isAnimationStudio'] else 'No'}")
    print("\nPopular Works:")
    
    for i, anime in enumerate(studio["media"]["nodes"], 1):
        print(f"{i}. {anime['title']['romaji']} ({anime['format']}, {anime['seasonYear']})")
        print(f"   Score: {anime['averageScore']}/100")


def example_get_seasonal_rankings():
    """Example: Get top anime for a specific season."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("EXAMPLE: SEASONAL RANKINGS")
    print("=" * 50)
    
    # Define a custom query to get seasonal rankings
    query = """
    query ($season: MediaSeason, $seasonYear: Int) {
        Page(page: 1, perPage: 10) {
            media(season: $season, seasonYear: $seasonYear, type: ANIME, sort: SCORE_DESC) {
                id
                title {
                    romaji
                }
                format
                episodes
                averageScore
                popularity
                studios(isMain: true) {
                    nodes {
                        name
                    }
                }
            }
        }
    }
    """
    
    # Fetch data for Winter 2023
    variables = {"season": "WINTER", "seasonYear": 2023}
    result = client.run_query(query, variables)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    anime_list = result["data"]["Page"]["media"]
    
    print(f"Top Anime of Winter 2023 (by Score):")
    
    for i, anime in enumerate(anime_list, 1):
        studio_name = "Unknown"
        if anime["studios"]["nodes"]:
            studio_name = anime["studios"]["nodes"][0]["name"]
        
        print(f"{i}. {anime['title']['romaji']} ({anime['format']})")
        print(f"   Episodes: {anime['episodes']}")
        print(f"   Score: {anime['averageScore']}/100")
        print(f"   Popularity: {anime['popularity']}")
        print(f"   Studio: {studio_name}")
        print()


def example_get_genres_and_tags():
    """Example: Get anime by genre and tag."""
    client = AnilistClient()
    
    print("\n" + "=" * 50)
    print("EXAMPLE: GENRES AND TAGS")
    print("=" * 50)
    
    # Define a custom query to get anime by genre and tag
    query = """
    query ($genre: String, $tag: String) {
        Page(page: 1, perPage: 5) {
            media(genre: $genre, tag: $tag, type: ANIME, sort: POPULARITY_DESC) {
                id
                title {
                    romaji
                }
                format
                seasonYear
                averageScore
                genres
                tags {
                    name
                    rank
                }
            }
        }
    }
    """
    
    # Fetch data for Action genre and "Time Travel" tag
    variables = {"genre": "Action", "tag": "Time Travel"}
    result = client.run_query(query, variables)
    
    if "errors" in result:
        print(f"Error: {result['errors'][0]['message']}")
        return
    
    anime_list = result["data"]["Page"]["media"]
    
    print(f"Popular Action Anime with Time Travel:")
    
    for i, anime in enumerate(anime_list, 1):
        print(f"{i}. {anime['title']['romaji']} ({anime['format']}, {anime.get('seasonYear', 'Unknown')})")
        print(f"   Score: {anime['averageScore']}/100")
        print(f"   Genres: {', '.join(anime['genres'])}")
        
        # Get top 3 tags by rank
        top_tags = sorted(anime["tags"], key=lambda x: x["rank"], reverse=True)[:3]
        print(f"   Top Tags: {', '.join(tag['name'] for tag in top_tags)}")
        print()


def main():
    """Main function to run examples."""
    print("Anilist API Examples")
    print("This script demonstrates various examples of fetching specific information.")
    
    # Run examples
    example_get_anime_basic_info()
    example_get_anime_characters()
    example_get_studio_works()
    example_get_seasonal_rankings()
    example_get_genres_and_tags()
    
    print("\nThese examples demonstrate how to fetch specific information from the Anilist API.")
    print("You can modify the queries to get different information based on your needs.")


if __name__ == "__main__":
    main()
