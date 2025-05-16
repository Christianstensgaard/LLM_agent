import requests

# def search_papers(topic: str, year: int, year_filter: str, citation_threshold: int) -> list:
#     url = "https://api.semanticscholar.org/graph/v1/paper/search"
#     params = {
#         "query": topic,
#         "limit": 50,
#         "fields": "title,year,citationCount,url"
#     }

#     response = requests.get(url, params=params)
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}")
#         return []

#     results = response.json().get("data", [])

#     filtered = []
#     for paper in results:
#         # Filter papers based on the year filter logic
#         if year_filter == "after" and paper["year"] > year:
#             if paper["citationCount"] >= citation_threshold:
#                 filtered.append(paper)
#         elif year_filter == "before" and paper["year"] < year:
#             if paper["citationCount"] >= citation_threshold:
#                 filtered.append(paper)
#         elif year_filter == "in" and paper["year"] == year:
#             if paper["citationCount"] >= citation_threshold:
#                 filtered.append(paper)

#     # Print the filtered results to debug
#     print()
#     return filtered

def search_papers(topic: str) -> list:
  url = "https://api.semanticscholar.org/graph/v1/paper/search"
  params = {
      "query": topic,
      "limit": 50,
      "fields": "title,year,url"
  }

  response = requests.get(url, params=params)
  if response.status_code != 200:
      print(f"Error: {response.status_code}")
      return []

  results = response.json().get("data", [])

  # Print the filtered results to debug
  print(results)
  return results

