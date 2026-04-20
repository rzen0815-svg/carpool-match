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
