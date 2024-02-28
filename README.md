
# Scholarly Paper Scraper

## Introduction
🔍 _A simple, quick tool to search for keywords in various scholar search engines and retrieve relevant academic information, including titles, authors, and abstracts. The tool then ranks each source using the predefined scoring function which could be optimized by the user._

## Features
### Current Features
- 🌐 Keyword search on Google Scholar.
- 📑 Extraction of titles, authors, and abstracts.

### Upcoming Milestones
- [x] 🛡️ Implement proxies to prevent blocking.
- [x] 💬 Implementing API for easier handling
- [x] 💬 Develop a custom ChatGPT interface for the scraper.
- [x] 📄 Implement a scoring function to rank the papers. 

## Getting Started
### Prerequisites
  - Python 3.x
  - BeautifulSoup

### Installation
```bash
# Instructions to install your tool
git clone https://github.com/amirbabaei97/paper_scrapper
cd paper_scrapper
pip install -r requirements.txt
```

## Usage
🚀 _How to use the tool:_
```python
# Example command or script
python scraper.py --keyword "machine learning"
```
_Output format: Results are presented in a structured JSON format._

## Roadmap
🚧 _Future enhancements:_
- [ ] Integration with additional scientific paper search engines:
  - [x] Google Scholar 
  - [ ] Arxiv
  - [x] Semantic Scholar
  - [ ] Open Review
  - [ ] Science.gov
  - [ ] core.ac.uk
  - [ ] Science Direct
  - [ ] PubMed
  - [ ] Scopus

## Contributing
🤝 _We welcome contributions!_
- Please do a fork and then send a PR with the explanations of the changes. 
- For major changes, please open an issue first to discuss what you would like to change.

## License
📄 _This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html)._

## Acknowledgments
- Hat tip to ChatGPT for helping in the development process
- Thank you to arXiv for use of its open access interoperability.
- Thank you Semantic Scholar for providing a free API key for this project.
