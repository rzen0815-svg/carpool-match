# Campus Carpool Matching System
A lightweight web-based carpool matching tool designed for campus use.  
Users can submit their contact information, departure time, destination, and preferred car size, and the system will automatically match them based on simple rules.
---
## Overview
This project was built to solve a real campus problem: taking a taxi alone from school to **Fuzhou Railway Station** or **Fuzhou South Railway Station** is expensive, while sharing a ride with 2 or 3 people is much more cost-effective.
The system allows users to submit ride requests and automatically matches them according to:
- destination
- departure time
- preferred group size
It also provides:
- status checking
- cancellation
- duplicate contact detection
- basic data persistence
This is currently a **minimum viable product (MVP)** suitable for small-scale testing and future iteration.
---
## Features
- Submit a carpool request
- Choose departure time
- Choose destination
  - Fuzhou Railway Station
  - Fuzhou South Railway Station
- Choose preferred group size
  - 2 people per car
  - 3 people per car
- Automatic matching logic
  - same destination
  - close departure time
  - matching group size preference
- Check registration status
- Cancel registration
- Duplicate contact detection
  - real-time frontend check
  - backend validation on submit
- Automatic cleanup of expired requests
- Improved result and message pages
- Confirmation modal before cancellation
---
## Project Structure
```text
carpool_match/
├── app.py
├── matcher.py
├── storage.py
├── data.json
├── requirements.txt
├── Procfile
├── .gitignore
├── static/
│   └── style.css
└── templates/
    ├── index.html
    ├── manage.html
    ├── message.html
    ├── result.html
    └── status_result.html

File Description

* app.py
    Main Flask application. Handles routes, form submission, and template rendering.
* matcher.py
    Matching logic, including request creation and 2-person / 3-person matching rules.
* storage.py
    Handles loading, saving, deleting requests, and removing expired records.
* data.json
    Current lightweight storage file used by the project.
* templates/
    HTML templates for the frontend pages.
* static/style.css
    Shared stylesheet for the web pages.

⸻

Tech Stack

* Python
* Flask
* HTML
* CSS
* JavaScript
* JSON file storage

⸻

How to Run Locally

1. Clone the repository

git clone https://github.com/rzen0815-svg/carpool-match.git
cd carpool-match

2. Create and activate a virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Start the application

python app.py

Then open:

http://127.0.0.1:5000

⸻

Matching Rules

2-person carpool

Two users can be matched if:

* they have the same destination
* both selected 2 people per car
* their departure times differ by no more than 20 minutes

3-person carpool

Three users can be matched if:

* they have the same destination
* all selected 3 people per car
* the time difference between the earliest and latest request is no more than 20 minutes

Other rules

* duplicate contacts are not allowed
* users can check their status
* users can cancel their request
* expired requests are automatically removed

⸻

Highlights

* Based on a real campus transportation need
* Functional MVP with a full user flow
* Good beginner-to-intermediate Flask project
* Can be extended into a more complete campus ride-sharing tool

⸻

Possible Future Improvements

* better privacy protection
* status query code or two-step verification
* deployment for real public use
* smarter guidance / suggestion features
* better mobile responsiveness
* database instead of data.json
* admin dashboard
* richer matching strategies

⸻

Current Limitations

* uses data.json instead of a real database
* not suitable for large-scale concurrent usage yet
* no login system or SMS verification
* currently better suited for small-scale testing

⸻

Use Cases

* small-scale campus carpool testing
* Flask learning project
* Python web development practice
* real-world MVP prototype

⸻

Author Note

This project was developed step by step from a real campus need.
The goal was not to build a complex platform from the beginning, but to create a simple, usable version first, then improve it through testing, feedback, deployment, and iteration.
