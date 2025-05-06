#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Anilist API Test Script

This script demonstrates how to use the Anilist API client to fetch anime data.
"""

import sys
import json
import textwrap
from anilist_client import AnilistClient


class AnimeFormatter:
    """Formats anime data for display."""
    
    @staticmethod
    def format_anime_details(anime):
        """Format detailed anime information into a readable string."""
        title = anime["title"]
        
        # Format basic info
        info = [
            f"📺 {title['romaji']} ({anime['id']})",
            f"   {title.get('native', '')}"
        ]
        
        if title.get("english"):
            info.append(f"   English: {title['english']}")
        
        # Format description
        if anime.get("description"):
            description = anime["description"].replace("<br>", " ").replace("<i>", "").replace("</i>", "")
            wrapped_desc = textwrap.fill(description, width=80)[:300]
            if len(description) > 300:
                wrapped_desc += "..."
            info.append(f"\n📝 {wrapped_desc}")
        
        # Format key details
        details = []
        if anime.get("episodes"):
            details.append(f"Episodes: {anime['episodes']}")
        if anime.get("duration"):
            details.append(f"Duration: {anime['duration']}min")
        if anime.get("status"):
            details.append(f"Status: {anime['status']}")
        
        if details:
            info.append("\n🔍 " + " | ".join(details))
        
        # Format dates
        dates = []
        if anime.get("startDate") and anime["startDate"].get("year"):
            start = anime["startDate"]
            dates.append(f"Start: {start.get('year')}-{start.get('month', '??')}-{start.get('day', '??')}")
        
        if anime.get("endDate") and anime["endDate"].get("year"):
            end = anime["endDate"]
            dates.append(f"End: {end.get('year')}-{end.get('month', '??')}-{end.get('day', '??')}")
        
        if dates:
            info.append("📅 " + " | ".join(dates))
        
        # Format season and format
        if anime.get("season") or anime.get("format"):
            season_format = []
            if anime.get("season") and anime.get("seasonYear"):
                season_format.append(f"{anime['season']} {anime['seasonYear']}")
            if anime.get("format"):
                season_format.append(anime["format"])
            
            info.append("🗓️ " + " | ".join(season_format))
        
        # Format genres and tags
        if anime.get("genres"):
            info.append(f"🏷️ {', '.join(anime['genres'][:5])}")
        
        if anime.get("tags"):
            top_tags = sorted(anime["tags"], key=lambda x: x["rank"], reverse=True)[:3]
            info.append(f"🔖 {', '.join(tag['name'] for tag in top_tags)}")
        
        # Format ratings
        ratings = []
        if anime.get("averageScore"):
            ratings.append(f"Score: {anime['averageScore']}/100")
        if anime.get("popularity"):
            ratings.append(f"Popularity: {anime['popularity']}")
        
        if ratings:
            info.append("⭐ " + " | ".join(ratings))
        
        # Format studios
        if anime.get("studios") and anime["studios"].get("nodes"):
            studios = [studio["name"] for studio in anime["studios"]["nodes"]]
            info.append(f"🏢 {', '.join(studios)}")
        
        return "\n".join(info)
    
    @staticmethod
    def format_anime_card(anime):
        """Format basic anime information into a card-like string."""
        title = anime["title"]
        
        info = [
            f"📺 {title['romaji']} ({anime['id']})",
            f"   {title.get('native', '')}"
        ]
        
        details = []
        if anime.get("episodes"):
            details.append(f"Ep: {anime['episodes']}")
        if anime.get("format"):
            details.append(anime["format"])
        if anime.get("seasonYear"):
            details.append(str(anime["seasonYear"]))
        if anime.get("averageScore"):
            details.append(f"⭐ {anime['averageScore']}/100")
        
        if details:
            info.append("🔍 " + " | ".join(details))
        
        if anime.get("genres"):
            info.append(f"🏷️ {', '.join(anime['genres'][:3])}")
        
        return "\n".join(info)


def display_anime_details(client, anime_id):
    """Display detailed information about an anime by ID."""
    print(f"\n{'=' * 50}")
    print(f"ANIME DETAILS (ID: {anime_id})")
    print(f"{'=' * 50}")
    
    try:
        result = client.get_anime_by_id(anime_id)
        
        if "errors" in result:
            print(f"Error: {result['errors'][0]['message']}")
            return
        
        anime = result["data"]["Media"]
        formatted_info = AnimeFormatter.format_anime_details(anime)
        print(formatted_info)
        
    except Exception as e:
        print(f"Error fetching anime details: {e}")


def search_anime_by_keyword(client, keyword, page=1, per_page=5):
    """Search for anime by keyword and display results."""
    print(f"\n{'=' * 50}")
    print(f"SEARCH RESULTS: '{keyword}' (Page {page})")
    print(f"{'=' * 50}")
    
    try:
        result = client.search_anime(keyword, page, per_page)
        
        if "errors" in result:
            print(f"Error: {result['errors'][0]['message']}")
            return
        
        page_info = result["data"]["Page"]["pageInfo"]
        media_list = result["data"]["Page"]["media"]
        
        print(f"Found {page_info['total']} results. Page {page_info['currentPage']}/{page_info['lastPage']}.")
        
        if not media_list:
            print("No results found.")
            return
        
        for i, anime in enumerate(media_list, 1):
            print(f"\n--- Result {i} ---")
            formatted_info = AnimeFormatter.format_anime_card(anime)
            print(formatted_info)
        
    except Exception as e:
        print(f"Error searching anime: {e}")


def get_seasonal_anime(client, year, season, page=1, per_page=5):
    """Get seasonal anime and display results."""
    print(f"\n{'=' * 50}")
    print(f"{season.upper()} {year} ANIME (Page {page})")
    print(f"{'=' * 50}")
    
    try:
        result = client.get_seasonal_anime(year, season, page, per_page)
        
        if "errors" in result:
            print(f"Error: {result['errors'][0]['message']}")
            return
        
        page_info = result["data"]["Page"]["pageInfo"]
        media_list = result["data"]["Page"]["media"]
        
        print(f"Found {page_info['total']} results. Page {page_info['currentPage']}/{page_info['lastPage']}.")
        
        if not media_list:
            print("No results found.")
            return
        
        for i, anime in enumerate(media_list, 1):
            print(f"\n--- Anime {i} ---")
            formatted_info = AnimeFormatter.format_anime_card(anime)
            print(formatted_info)
        
    except Exception as e:
        print(f"Error fetching seasonal anime: {e}")


def main():
    """Main function to demonstrate the Anilist API client."""
    client = AnilistClient()
    
    # Example 1: Get anime by ID (Demon Slayer: Kimetsu no Yaiba)
    display_anime_details(client, 101922)
    
    # Example 2: Search for anime by keyword
    search_anime_by_keyword(client, "Attack on Titan")
    
    # Example 3: Get seasonal anime
    get_seasonal_anime(client, 2023, "WINTER")


if __name__ == "__main__":
    main()
