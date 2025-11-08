import requests
import json
from datetime import datetime

# CHANGE THESE TWO VALUES:
ORCID_ID = "0000-0001-5419-7206"  # Your ORCID ID here
YOUR_LAST_NAME = "Ainslie"  # Your last name to highlight in author lists
YOUR_EMAIL = "ainslie.kylie@gmail.com"  # Your email for API requests

ORCID_API = "https://pub.orcid.org/v3.0/"

def fetch_doi_metadata(doi):
    """Fetch full citation metadata from DOI"""
    url = f"https://dx.doi.org/{doi}"
    headers = {
        "accept": "application/citeproc+json",
        "User-Agent": f"mailto:{YOUR_EMAIL}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching DOI {doi}: {e}")
    return None

def get_orcid_publications():
    """Fetch publications from ORCID"""
    url = f"{ORCID_API}{ORCID_ID}/works"
    headers = {"Accept": "application/json"}
    
    print(f"Fetching publications from ORCID for {ORCID_ID}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    publications = []
    
    total_works = len(data.get("group", []))
    print(f"Found {total_works} works in ORCID profile")
    
    for idx, group in enumerate(data.get("group", []), 1):
        work_summary = group["work-summary"][0]
        
        # Extract DOI
        doi = None
        if work_summary.get("external-ids"):
            for ext_id in work_summary["external-ids"]["external-id"]:
                if ext_id["external-id-type"] == "doi":
                    doi = ext_id["external-id-value"]
                    break
        
        if doi:
            print(f"  [{idx}/{total_works}] Fetching: {doi}")
            metadata = fetch_doi_metadata(doi)
            if metadata:
                # Extract abstract if available
                abstract = metadata.get('abstract', '')
                
                publications.append({
                    'title': metadata.get('title', ''),
                    'authors': metadata.get('author', []),
                    'year': metadata.get('issued', {}).get('date-parts', [[None]])[0][0],
                    'journal': metadata.get('container-title', ''),
                    'doi': doi,
                    'type': metadata.get('type', 'article'),
                    'abstract': abstract,
                    'volume': metadata.get('volume', ''),
                    'issue': metadata.get('issue', ''),
                    'page': metadata.get('page', '')
                })
            else:
                print(f"  [{idx}/{total_works}] Warning: Could not fetch metadata for {doi}")
        else:
            title = work_summary.get('title', {}).get('title', {}).get('value', 'Unknown')
            print(f"  [{idx}/{total_works}] Skipping (no DOI): {title}")
    
    return publications

def format_authors(authors, highlight_name=YOUR_LAST_NAME):
    """Format author list, highlighting your name"""
    author_list = []
    for author in authors:
        family = author.get('family', '')
        given = author.get('given', '')
        name = f"{given} {family}".strip()
        
        # Bold your name
        if highlight_name.lower() in family.lower():
            name = f"**{name}**"
        
        author_list.append(name)
    
    if len(author_list) == 0:
        return ""
    elif len(author_list) == 1:
        return author_list[0]
    elif len(author_list) == 2:
        return f"{author_list[0]} and {author_list[1]}"
    else:
        # All authors if 10 or fewer, otherwise first 3 + et al.
        if len(author_list) > 10:
            return f"{', '.join(author_list[:3])}, et al."
        else:
            return f"{', '.join(author_list[:-1])}, and {author_list[-1]}"

def clean_abstract(abstract):
    """Remove common HTML/XML tags from abstract"""
    if not abstract:
        return ""
    
    # Remove common tags
    replacements = {
        '<jats:p>': '',
        '</jats:p>': '',
        '<jats:italic>': '*',
        '</jats:italic>': '*',
        '<jats:bold>': '**',
        '</jats:bold>': '**',
        '<p>': '',
        '</p>': '\n\n',
    }
    
    for old, new in replacements.items():
        abstract = abstract.replace(old, new)
    
    return abstract.strip()

def generate_publications_qmd(publications):
    """Generate Quarto markdown with collapsible abstracts"""
    
    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get('year', 0) or 0, reverse=True)
    
    # Group by year
    by_year = {}
    for pub in publications:
        year = pub.get('year', 'Unknown')
        if year not in by_year:
            by_year[year] = []
        by_year[year].append(pub)
    
    # Generate markdown
    content = """---
title: "Publications"
---

*Last updated: {date}*

::: {{.callout-note}}
## About
All publications are automatically updated from my [ORCID profile](https://orcid.org/{orcid}).  
Click on any publication title to view the abstract.
:::

""".format(date=datetime.now().strftime("%B %d, %Y"), orcid=ORCID_ID)
    
    for year in sorted(by_year.keys(), reverse=True):
        if year == 'Unknown':
            continue
            
        content += f"\n## {year}\n\n"
        
        for i, pub in enumerate(by_year[year], 1):
            authors = format_authors(pub.get('authors', []))
            title = pub.get('title', 'Untitled')
            journal = pub.get('journal', '')
            doi = pub.get('doi', '')
            abstract = pub.get('abstract', '')
            
            # Build citation
            content += f"{i}. {authors}. "
            content += f"*{title}*. "
            if journal:
                content += f"{journal}"
                volume = pub.get('volume', '')
                issue = pub.get('issue', '')
                page = pub.get('page', '')
                
                if volume:
                    content += f" {volume}"
                if issue:
                    content += f"({issue})"
                if page:
                    content += f":{page}"
                content += ". "
            
            if doi:
                content += f"[https://doi.org/{doi}](https://doi.org/{doi})"
            
            content += "\n\n"
            
            # Collapsible abstract
            if abstract:
                clean_abs = clean_abstract(abstract)
                if clean_abs:
                    # Make title clickable to expand abstract
                    content += f"""<details>
<summary>Show abstract</summary>

{clean_abs}

</details>

"""
            
            content += "\n"
    
    # Add publications with unknown year at the end
    if 'Unknown' in by_year:
        content += "\n## Other Publications\n\n"
        for i, pub in enumerate(by_year['Unknown'], 1):
            authors = format_authors(pub.get('authors', []))
            title = pub.get('title', 'Untitled')
            doi = pub.get('doi', '')
            
            content += f"{i}. {authors}. *{title}*. "
            if doi:
                content += f"[https://doi.org/{doi}](https://doi.org/{doi})"
            content += "\n\n"
    
    return content

if __name__ == "__main__":
    print("=" * 60)
    print("ORCID Publications Updater")
    print("=" * 60)
    
    try:
        publications = get_orcid_publications()
        
        print(f"\n✓ Successfully fetched {len(publications)} publications with DOIs")
        
        print("\nGenerating publications.qmd...")
        content = generate_publications_qmd(publications)
        
        with open("publications.qmd", "w", encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Done! publications.qmd has been updated.")
        print("\nNext steps:")
        print("1. Review publications.qmd")
        print("2. Run 'quarto preview' to see how it looks")
        print("3. Commit and push to GitHub")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
