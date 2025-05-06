#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anilist API Client

A simple client for testing the Anilist GraphQL API.
"""

import json
import requests
from typing import Dict, Any, Optional, List


class AnilistClient:
    """A client for the Anilist GraphQL API."""

    def __init__(self):
        self.url = "https://graphql.anilist.co"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def run_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query against the Anilist API.

        Args:
            query: The GraphQL query string
            variables: Optional variables for the query

        Returns:
            The JSON response from the API
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(self.url, json=payload, headers=self.headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def get_anime_by_id(self, anime_id: int) -> Dict[str, Any]:
        """
        Get anime information by its ID.

        Args:
            anime_id: The Anilist ID of the anime

        Returns:
            Anime information
        """
        query = """
        query ($id: Int) {
            Media (id: $id, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                episodes
                duration
                status
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                season
                seasonYear
                format
                genres
                tags {
                    name
                    rank
                }
                averageScore
                popularity
                studios {
                    nodes {
                        name
                    }
                }
                coverImage {
                    large
                }
            }
        }
        """

        variables = {"id": anime_id}
        return self.run_query(query, variables)

    def search_anime(
        self, search_term: str, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Search for anime by keyword.

        Args:
            search_term: The search keyword
            page: Page number (default: 1)
            per_page: Number of results per page (default: 10)

        Returns:
            Search results
        """
        query = """
        query ($search: String, $page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (search: $search, type: ANIME, sort: POPULARITY_DESC) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    episodes
                    format
                    status
                    seasonYear
                    averageScore
                    genres
                    coverImage {
                        medium
                    }
                }
            }
        }
        """

        variables = {"search": search_term, "page": page, "perPage": per_page}
        return self.run_query(query, variables)

    def get_seasonal_anime(
        self, year: int, season: str, page: int = 1, per_page: int = 10
    ) -> Dict[str, Any]:
        """
        Get seasonal anime.

        Args:
            year: The year
            season: The season (WINTER, SPRING, SUMMER, FALL)
            page: Page number (default: 1)
            per_page: Number of results per page (default: 10)

        Returns:
            Seasonal anime results
        """
        query = """
        query ($season: MediaSeason, $seasonYear: Int, $page: Int, $perPage: Int) {
            Page (page: $page, perPage: $perPage) {
                pageInfo {
                    total
                    currentPage
                    lastPage
                    hasNextPage
                    perPage
                }
                media (season: $season, seasonYear: $seasonYear, type: ANIME, sort: POPULARITY_DESC) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    episodes
                    format
                    status
                    averageScore
                    genres
                    coverImage {
                        medium
                    }
                }
            }
        }
        """

        variables = {
            "season": season.upper(),
            "seasonYear": year,
            "page": page,
            "perPage": per_page,
        }
        return self.run_query(query, variables)


# This space intentionally left empty after removing the print_anime_info function
# The formatting functionality has been moved to the AnimeFormatter class in main.py
