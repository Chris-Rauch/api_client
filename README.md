# API Clients

## Overview
Base Method APIClient creates standard functionality for making HTTP requests. 
The other sub classes in this module inherit that standard functionality but 
allows custom implementation for specific API's.

## System Design

### APIClient
Provides the following generic HTTP request methods
  1. POST
  2. GET
  3. DELETE
  4. PUT

All methods return a request.Response() object, making it easy to handle HTTP responses

### RoboClient
The RoboClient class customizes the APIClient to work specifically with the RoboTalker API. Key features include:

  1. Basic Authentication: Automatically verifies credentials.
  2. Cookie Management: Saves and uses cookies for session management.
  3. Predefined API Endpoints:
    /api/Config: Retrieve account configuration.
    /api/MultiJob (POST): Schedule a job.
    /api/JobSummary: Get a summary of a scheduled job.

## Getting Started

### Dependencies
- Python 3.8 or higher
- requests
- exceptions

### Installation
1. Clone this repository and install dependencies:
   ```bash
   git clone https://github.com/Chris-Rauch/api_client.git
   cd api_client
   pip install -r requirements.txt
   ```
   
