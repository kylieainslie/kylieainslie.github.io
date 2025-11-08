import requests
import json
from datetime import datetime
import csv

# CHANGE THESE THREE VALUES:
ORCID_ID = "0000-0001-5419-7206"
YOUR_LAST_NAME = "Ainslie"
YOUR_EMAIL = "ainslie.kylie@gmail.com"

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
        print(f"  Warning: Could not fetch DOI metadata: {e}")
    return None

def extract_orcid_metadata(work_summary):
    """Extract metadata directly from ORCID work summary"""
    title = work_summary.get('title', {})
    if title:
        title = title.get('title', {}).get('value', 'Untitled')
    else:
        title = 'Untitled'
    
    year = None
    pub_date = work_summary.get('publication-date')
    if pub_date:
        year = pub_date.get('year', {}).get('value')
    
    journal = work_summary.get('journal-title', {})
    if journal:
        journal = journal.get('value', '')
    else:
        journal = ''
    
    work_type = work_summary.get('type', 'publication')
    
    external_ids = {}
    if work_summary.get('external-ids'):
        for ext_id in work_summary['external-ids']['external-id']:
            id_type = ext_id.get('external-id-type', '')
            id_value = ext_id.get('external-id-value', '')
            external_ids[id_type] = id_value
    
    return {
        'title': title,
        'year': year,
        'journal': journal,
        'type': work_type,
        'external_ids': external_ids,
        'source': 'orcid'
    }

def get_orcid_publications():
    """Fetch ALL publications from ORCID"""
    url = f"{ORCID_API}{ORCID_ID}/works"
    headers = {"Accept": "application/json"}
    
    print(f"Fetching publications from ORCID for {ORCID_ID}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    publications = []
    
    total_works = len(data.get("group", []))
    print(f"Found {total_works} works in ORCID profile")
    
    with_doi = 0
    without_doi = 0
    
    for idx, group in enumerate(data.get("group", []), 1):
        work_summary = group["work-summary"][0]
        
        doi = None
        if work_summary.get("external-ids"):
            for ext_id in work_summary["external-ids"]["external-id"]:
                if ext_id["external-id-type"] == "doi":
                    doi = ext_id["external-id-value"]
                    break
        
        if doi:
            print(f"  [{idx}/{total_works}] Fetching DOI: {doi}")
            doi_metadata = fetch_doi_metadata(doi)
            
            if doi_metadata:
                with_doi += 1
                publications.append({
                    'title': doi_metadata.get('title', ''),
                    'authors': doi_metadata.get('author', []),
                    'year': doi_metadata.get('issued', {}).get('date-parts', [[None]])[0][0],
                    'journal': doi_metadata.get('container-title', ''),
                    'doi': doi,
                    'type': doi_metadata.get('type', 'article'),
                    'abstract': doi_metadata.get('abstract', ''),
                    'volume': doi_metadata.get('volume', ''),
                    'issue': doi_metadata.get('issue', ''),
                    'page': doi_metadata.get('page', ''),
                    'source': 'doi'
                })
            else:
                print(f"  [{idx}/{total_works}] DOI fetch failed, using ORCID metadata")
                orcid_data = extract_orcid_metadata(work_summary)
                orcid_data['doi'] = doi
                publications.append(orcid_data)
                without_doi += 1
        else:
            title = work_summary.get('title', {}).get('title', {}).get('value', 'Unknown')
            print(f"  [{idx}/{total_works}] No DOI: {title[:60]}...")
            publications.append(extract_orcid_metadata(work_summary))
            without_doi += 1
    
    print(f"\n✓ Processed {total_works} total publications:")
    print(f"  - {with_doi} with full DOI metadata")
    print(f"  - {without_doi} using ORCID metadata only")
    
    return publications

def format_authors_list(authors, highlight_name=YOUR_LAST_NAME):
    """Format author list as string, noting which to highlight"""
    if not authors:
        return "", ""
    
    author_names = []
    for author in authors:
        family = author.get('family', '')
        given = author.get('given', '')
        name = f"{given} {family}".strip()
        author_names.append(name)
    
    # Create full author string
    if len(author_names) <= 2:
        author_str = " and ".join(author_names)
    elif len(author_names) > 10:
        author_str = f"{', '.join(author_names[:3])}, et al."
    else:
        author_str = f"{', '.join(author_names[:-1])}, and {author_names[-1]}"
    
    # Mark which author is you (for R to bold)
    is_author = any(highlight_name.lower() in name.lower() for name in author_names)
    
    return author_str, "YES" if is_author else "NO"

def clean_abstract(abstract):
    """Remove common HTML/XML tags from abstract"""
    if not abstract:
        return ""
    
    replacements = {
        '<jats:p>': '',
        '</jats:p>': '',
        '<jats:italic>': '',
        '</jats:italic>': '',
        '<jats:bold>': '',
        '</jats:bold>': '',
        '<p>': '',
        '</p>': ' ',
    }
    
    for old, new in replacements.items():
        abstract = abstract.replace(old, new)
    
    abstract = ' '.join(abstract.split())
    return abstract.strip()

def save_to_csv(publications, filename='publications_data.csv'):
    """Save publications to CSV for R to read"""
    
    rows = []
    for pub in publications:
        year = pub.get('year', '')
        
        if pub.get('source') == 'doi':
            authors, is_author = format_authors_list(pub.get('authors', []))
            title = pub.get('title', 'Untitled')
            journal = pub.get('journal', '')
            doi = pub.get('doi', '')
            abstract = clean_abstract(pub.get('abstract', ''))
            
            volume = pub.get('volume', '')
            issue = pub.get('issue', '')
            page = pub.get('page', '')
            
            rows.append({
                'year': year if year else '',
                'authors': authors,
                'is_my_paper': is_author,
                'title': title,
                'journal': journal,
                'volume': volume,
                'issue': issue,
                'page': page,
                'doi': doi,
                'abstract': abstract,
                'type': pub.get('type', ''),
                'has_doi': 'YES'
            })
        else:
            title = pub.get('title', 'Untitled')
            journal = pub.get('journal', '')
            doi = pub.get('doi', '')
            external_ids = pub.get('external_ids', {})
            
            pmid = external_ids.get('pmid', '')
            arxiv = external_ids.get('arxiv', '')
            
            rows.append({
                'year': year if year else '',
                'authors': '',
                'is_my_paper': 'UNKNOWN',
                'title': title,
                'journal': journal,
                'volume': '',
                'issue': '',
                'page': '',
                'doi': doi if doi else '',
                'abstract': '',
                'type': pub.get('type', ''),
                'has_doi': 'YES' if doi else ('PMID' if pmid else ('ARXIV' if arxiv else 'NO'))
            })
    
    # Write to CSV
    if rows:
        fieldnames = ['year', 'authors', 'is_my_paper', 'title', 'journal', 'volume', 
                     'issue', 'page', 'doi', 'abstract', 'type', 'has_doi']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"✓ Saved {len(rows)} publications to {filename}")
    else:
        print("⚠ No publications to save")

if __name__ == "__main__":
    print("=" * 60)
    print("ORCID Publications Data Fetcher")
    print("=" * 60)
    
    try:
        publications = get_orcid_publications()
        
        print(f"\nSaving publications to CSV...")
        save_to_csv(publications)
        
        print("✓ Done!")
        print("\nNext steps:")
        print("1. Check publications_data.csv")
        print("2. Use this CSV in your publications.qmd with R")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
