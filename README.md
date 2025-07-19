# Bravolino Educational Platform

## Overview

Bravolino is a comprehensive, interactive educational platform designed for Algerian children aged 5-12. Our mission is to provide a high-quality, engaging, and culturally relevant learning experience that aligns with the official Algerian curriculum. We focus on interactive learning through educational games, innovative activities, and a reward system that keeps children motivated.

The platform is designed to be child-friendly, with content that reflects Algerian cultural identity and values. We leverage technology to create a personalized learning path for each child, adapting to their individual pace and level.

## Features

### For Children:

*   **Interactive Lessons:** Engaging lessons in core subjects like Arabic, Math, and Science.
*   **Educational Games:** Fun and challenging games that reinforce learning concepts.
*   **Personalized Avatars:** Customizable avatars that children can personalize as they progress.
*   **Reward System:** A system of points and badges to motivate and reward children for their achievements.
*   **Progress Tracking:** Visual progress maps that show children their learning journey.

### For Parents:

*   **Dashboard:** A comprehensive dashboard to monitor a child's progress, including time spent learning and performance in different subjects.
*   **Detailed Reports:** Weekly and monthly reports with detailed analysis of a child's performance and recommendations for improvement.
*   **Parental Controls:** Tools to control usage time and content access.
*   **Safe Environment:** A secure, ad-free environment for children to learn and explore.

### For Teachers and Schools:

*   **Classroom Management:** Tools to manage classrooms, assign tasks, and track student progress.
*   **Content Library:** Access to a rich library of interactive and curriculum-aligned content.
*   **Custom Content Creation:** Tools for teachers to create and share their own educational content.
*   **Professional Development:** Training and resources to help teachers integrate technology into their teaching.

## Tech Stack

*   **Frontend:** React.js with Tailwind CSS
*   **Backend:** Flask (Python) with SQLAlchemy
*   **Database:** SQLite (for development)
*   **Deployment:** The frontend is deployed on Vercel, and the backend is deployed on Heroku.

## Project Structure

The project is organized into the following directories:

```
/
├── database/         # SQLite database file
├── docs/             # Project documentation
├── src/              # Python source code for the backend
│   ├── models/       # SQLAlchemy models
│   └── routes/       # Flask blueprints for different routes
├── static/           # React frontend application
│   └── src/
└── main.py           # Main Flask application file
```

## Getting Started

### Prerequisites

*   Python 3.7+
*   Node.js 14+
*   npm or yarn

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/bravolino.git
    cd bravolino
    ```

2.  **Set up the backend:**
    ```bash
    # Create and activate a virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    # Install Python dependencies
    pip install -r requirements.txt
    ```

3.  **Set up the frontend:**
    ```bash
    # Navigate to the frontend directory
    cd static

    # Install JavaScript dependencies
    npm install
    ```

### Running the Application

1.  **Start the backend server:**
    ```bash
    # From the root directory
    python main.py
    ```
    The backend will be running at `http://localhost:5000`.

2.  **Start the frontend development server:**
    ```bash
    # From the static directory
    npm start
    ```
    The frontend will be running at `http://localhost:3000`.

## Contributing

We welcome contributions to the Bravolino platform! Please see our `CONTRIBUTING.md` file for more information on how to get involved.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
