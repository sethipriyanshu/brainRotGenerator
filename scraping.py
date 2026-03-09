import requests
from typing import Any, Dict, List


def _fetch_reddit_json(reddit_url: str) -> Any:
    """
    Fetch Reddit JSON for a given URL with basic validation and error reporting.
    """
    headers = {"User-agent": "Mozilla/5.0 (compatible; BranRotBot/1.0)"}

    # Ensure we hit the JSON endpoint even if the user didn't include .json
    url = reddit_url.rstrip("/")
    if not url.endswith(".json"):
        url = url + "/.json"

    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(
            f"Reddit returned status {resp.status_code} for URL {url}. "
            "Make sure the link is a valid, public Reddit URL."
        )

    try:
        return resp.json()
    except ValueError:
        snippet = resp.text[:200].replace("\n", " ")
        raise RuntimeError(
            f"Reddit did not return JSON for URL {url}. "
            f"Response starts with: {snippet!r}"
        )


### main scripts used for scraping the text
def scrape(reddit_url: str) -> Dict[str, str]:
    """
    Scrape a single Reddit post (title + selftext).
    Intended for direct post-permalink URLs.
    """
    data = _fetch_reddit_json(reddit_url)

    # Typical post-permalink JSON is a list with at least one element
    if isinstance(data, list) and data:
        try:
            post_data = data[0]["data"]["children"][0]["data"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected Reddit JSON shape for post URL: {e}")
    # Fallback: handle listing-like structure by taking the first child
    elif isinstance(data, dict) and "data" in data and "children" in data["data"]:
        try:
            post_data = data["data"]["children"][0]["data"]
        except (KeyError, IndexError, TypeError) as e:
            raise RuntimeError(f"Unexpected Reddit JSON shape for listing URL: {e}")
    else:
        raise RuntimeError("Unsupported Reddit JSON structure for single-post scraping.")

    self_text = post_data.get("selftext", "")
    title = post_data.get("title", "")

    result: Dict[str, str] = {"title": title, "desc": self_text}
    print("Scraped! Currently saving ...")
    return result


def scrape_llm(reddit_url: str) -> List[List[str]]:
    """
    Scrape a Reddit listing (e.g., subreddit page) to build a list of
    [title, selftext] entries for LLM-based selection.

    This is NOT intended for single-post permalinks.
    """
    data = _fetch_reddit_json(reddit_url)

    # If we got a list, this looks like a single post permalink; tell the user.
    if isinstance(data, list):
        raise RuntimeError(
            "The provided URL looks like a single Reddit post. "
            "Please turn OFF the 'thread' toggle in the UI for this link."
        )

    if not (isinstance(data, dict) and "data" in data and "children" in data["data"]):
        raise RuntimeError("Unexpected Reddit JSON structure for thread/listing scraping.")

    listing = data["data"]
    children = listing.get("children", [])
    fin: List[List[str]] = []

    for child in children:
        try:
            post = child["data"]
        except (TypeError, KeyError):
            continue
        title = str(post.get("title", "")).strip()
        desc = str(post.get("selftext", "")).strip()
        if not title and not desc:
            continue
        fin.append([title, desc])

    if not fin:
        raise RuntimeError("No posts with title/description found in Reddit listing.")

    return fin

def save_map_to_txt(map, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Title: {map['title']}\n")
        file.write(f"Description: {map['desc']}\n")
    print("SCRAPING DONE! SUCCESSFULLY SAVED")
