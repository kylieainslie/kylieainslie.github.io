# Kylie Ainslie, PhD - Personal Academic Website

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fkylieainslie.github.io)](https://kylieainslie.github.io)
[![GitHub Pages](https://img.shields.io/badge/Deployed%20with-GitHub%20Pages-blue)](https://pages.github.com/)
[![Quarto](https://img.shields.io/badge/Made%20with-Quarto-blue)](https://quarto.org)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub last commit](https://img.shields.io/github/last-commit/kylieainslie/kylieainslie.github.io)](https://github.com/kylieainslie/kylieainslie.github.io/commits/main)
[![GitHub repo size](https://img.shields.io/github/repo-size/kylieainslie/kylieainslie.github.io)](https://github.com/kylieainslie/kylieainslie.github.io)
[![GitHub issues](https://img.shields.io/github/issues/kylieainslie/kylieainslie.github.io)](https://github.com/kylieainslie/kylieainslie.github.io/issues)

Source code for Kylie Ainslie's personal academic website: [kylieainslie.github.io](https://kylieainslie.github.io)

## Technology Stack

- **Generator**: Quarto
- **Hosting**: GitHub Pages
- **Language**: R + Quarto Markdown (.qmd)

## Website Organization

The site is organized into main sections:

- **`index.qmd`** - Homepage with introduction
- **`about.qmd`** - Professional background and research interests  
- **`research.qmd`** - Current and past research projects
- **`publications.qmd`** - Academic papers and outputs
- **`software.qmd`** - R packages and computational tools
- **`presentations.qmd`** - Conference talks and presentations
- **`tutorials.qmd`** - Educational resources and guides
- **`cv.qmd`** - Academic curriculum vitae

Supporting content is organized in directories (`pdfs/`, `presentations/`, `tutorials/`, etc.)

## Repository Structure

```
├── _site/                    # Generated site (Quarto output)
├── docs/                     # Documentation
├── images/                   # Site images
├── pdfs/                     # PDF downloads
├── photos/                   # Profile photos
├── presentations/            # Presentation files
├── pubs/                     # Publications directory
├── tutorials/                # Tutorial content
├── _quarto.yml              # Site configuration
├── *.qmd                    # Page content (Quarto Markdown)
├── styles.css               # Custom CSS
└── kylieainslie.github.io.Rproj  # R Project file
```

## Local Development

### Prerequisites
- [R](https://www.r-project.org/) (4.0+)
- [Quarto CLI](https://quarto.org/docs/get-started/)
- [RStudio](https://rstudio.com/) (recommended)

### Setup
```bash
git clone https://github.com/kylieainslie/kylieainslie.github.io.git
cd kylieainslie.github.io
```

Open `kylieainslie.github.io.Rproj` in RStudio or run:

```bash
quarto preview    # Development server
quarto render     # Build site
```

Site will be available at `http://localhost:4200`

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the main branch. 

- `.nojekyll` file prevents Jekyll processing
- `_site/` contains the rendered output
- GitHub Pages serves directly from the repository

## Content Management

- **Pages**: Edit `.qmd` files in root directory
- **Configuration**: Modify `_quarto.yml`
- **Styling**: Update `styles.css`
- **Assets**: Add files to appropriate directories (`images/`, `pdfs/`, etc.)

### Common Tasks

**Adding a new publication:**
1. Update `publications.qmd` with new entry
2. Add PDF to `pdfs/` directory if available
3. Run `quarto render` to rebuild

**Adding a presentation:**
1. Create folder in `presentations/YEAR/event-name/`
2. Add presentation files (slides, materials)
3. Update `presentations.qmd` with new entry

**Optimizing images:**
- Use web-optimized formats (WebP, optimized PNG/JPEG)
- Compress images before uploading
- Consider using `images/` for site assets, `photos/` for personal photos

## Troubleshooting

**Site not updating after push:**
- Check GitHub Pages settings in repository
- Verify `_site/` directory was committed
- Check for build errors in Actions tab

**Quarto render fails:**
- Ensure R packages are installed
- Check for syntax errors in `.qmd` files
- Verify `_quarto.yml` is valid YAML

**Images not displaying:**
- Check file paths are relative to site root
- Ensure image files are committed to repository
- Verify file extensions match actual file types

## Contributing

Feel free to open issues for bugs or suggestions. For major changes, please open an issue first.

## License

Website content: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)  
Code: [MIT License](LICENSE)
