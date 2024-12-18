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
   cd api_client
   ```

### Configuration (if any)
None

## License
Copyright 2024 Christopher Rauch

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Contact
For any inquiries or issues, please contact:
- **Name**: Chris Rauch
- **Email**: [rauch.christopher13@gmail.com](mailto:rauch.christopher13@gmail.com)
- **GitHub**: [Chris-Rauch](https://github.com/Chris-Rauch)