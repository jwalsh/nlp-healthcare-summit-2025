# NLP Summit Healthcare 2025 Tracking Repository

This repository is designed to track sessions, contacts, and knowledge base topics for the [NLP Summit Healthcare 2025](https://www.nlpsummit.org/healthcare-2025/) event.

## Overview

This repository provides a structured approach to tracking information related to the NLP Summit Healthcare 2025 conference, including:

- Session details and notes
- Speaker contacts and networking information
- Knowledge base topics and research areas

## Repository Structure

- `sessions/` - Information about conference sessions
- `contacts/` - Details about speakers, attendees, and other contacts
- `kb/` - Knowledge base topics and notes
- `docs/` - Generated documentation and reports
- `nlp_healthcare_summit_2025/` - Python package for processing data

## Getting Started

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)
- Emacs with org-mode (optional, for org-mode functionality)

### Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd nlp-healthcare-summit-2025
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

### Usage

- Use the org-mode templates in `sessions/`, `contacts/`, and `kb/` directories to track information
- Run the update script to process the data and generate visualizations:
  ```
  ./update.sh
  ```

## Features

- **Org-mode Templates**: Structured templates for tracking sessions, contacts, and knowledge base topics
- **Python Processing**: Scripts for analyzing and visualizing the data
- **Network Visualization**: Generate visualizations of speaker connections and topic relationships
- **Poetry Integration**: Managed dependencies for reproducible environments

## Session Tracking

The `sessions/nlp_summit_sessions.org` file contains detailed information about all sessions from the NLP Summit Healthcare 2025, organized by day and track. Each session includes:

- Title, track, date, time, and format
- Speaker information
- Content details (description, key topics, technologies, applications)
- Space for notes

## Contact Management

The `contacts/speakers.org` file provides a comprehensive database of all speakers at the summit, including:

- Contact information
- Organizational affiliations
- Research interests and expertise
- Space for interaction notes

## Knowledge Base

The `kb/topics.org` file organizes key topics from the summit, including:

- Topic descriptions and categorizations
- Current state and future directions
- Healthcare applications
- Related sessions and contacts

## Customization

You can customize this repository by:

1. Adding new sessions, contacts, or topics using the templates
2. Modifying the Python scripts to perform additional analyses
3. Creating new visualization types in the docs directory

## License

[Your License Here]

## Acknowledgments

- NLP Summit Healthcare 2025 organizers and speakers
- John Snow Labs
