# ProjectX: Community Empowerment Exchange (CEE)
### Created by Philip Titus © 2024

Welcome to **ProjectX: Community Empowerment Exchange (CEE)**, a dynamic platform built on React and Django that fosters a community-driven experience, where users can trade skills, offer mutual aid, and collaborate on larger community projects. Our goal is to enable neighbors and communities to help one another through time, skills, resources, or funds, while nurturing trust and engagement at a local level.

---

## Core Concept
ProjectX is a **multi-faceted platform** designed to bring people together by encouraging neighbors to assist one another. Users can:

- Trade skills through a **barter system**.
- Offer and request **neighborhood assistance**.
- **Crowdfund and collaborate** on community projects.
- Provide and receive **mutual aid** for necessities.

Our platform emphasizes localized assistance while keeping the door open for broader engagements across the network, building stronger and more supportive communities.

---

## Key Features

### 1. **Skill Exchange Barter**
- Users can **offer or request services** (e.g., graphic design, coding, tutoring, etc.) in exchange for other services.
- Each user has a profile listing **offered skills** and **desired services**. Users can **negotiate trades** directly through the app.
  
   **Example**: "I’ll design your website in exchange for help with marketing."

### 2. **Neighborhood Assistance**
- A **location-based board** where users can post small tasks they need help with, such as running errands, borrowing tools, or getting advice.
- A **proximity filter** allows users to find and offer help nearby.

   **Example**: "Need someone to walk my dog tomorrow."

### 3. **Crowdfunding & Task Completion Hybrid**
- Users can **post community projects** that need both funding and manual help. Others can contribute funds or volunteer their time.
- A **fund button** enables contributions directly within the platform.

   **Example**: "Raising funds to build a community garden. We also need volunteers for planting."

### 4. **Community Assistance Request Board**
- A simple community board for **one-time quick favors** (e.g., "Can anyone recommend a plumber?" or "Help assemble a bookshelf").

### 5. **Mutual Aid Network**
- A dedicated space where users can post **requests for financial help** or **donations of resources** (e.g., groceries, supplies).
- Optional **anonymous posting** allows for discretion when asking for assistance.

   **Example**: "I need help with groceries this week, and I have some extra books to donate."

---

## AI Integration

### 1. **AI Matching & Recommendation System**
- **AI analyzes** user profiles, skills, and tasks to recommend **matches** between those needing help and those offering it.
  
   **Example**: "Based on your profile, here are 3 people nearby looking for graphic design help in exchange for web development."

### 2. **AI Task Categorization and Priority Sorting**
- Using **Natural Language Processing (NLP)**, AI analyzes posts and automatically places them in the correct sections (e.g., barter, mutual aid).
- AI also **prioritizes urgent requests**, moving tasks that need immediate attention to the top of the feed.

### 3. **AI for Smart Task & Project Suggestions**
- AI can analyze community trends to **suggest meaningful activities** for users.

   **Example**: "Many people in your neighborhood need financial help for school supplies—would you like to start a fundraiser?"

---

## Tech Stack & Cloud Integration

### 1. **AWS Cognito**
   - **Authentication and access control**, including sign-in, sign-up, and multi-factor authentication (MFA).
   
### 2. **Amazon Rekognition**
   - **User profile verification** and analysis of images in community projects or donations.

### 3. **AWS EC2**
   - For handling **scalable computing** in the cloud environment.

### 4. **Firebase (GCP Service)**
   - **Real-time database** management (Firestore) and **push notifications** (Cloud Messaging).

### 5. **AWS S3**
   - For **storing images** or other media related to user posts and community projects.

### 6. **Google Maps Platform**
   - For the **Neighborhood Assistance** feature, allowing users to view nearby requests based on geolocation.

### 7. **Google Cloud Functions**
   - For **event-driven tasks** like sending notifications, handling requests, or automating recommendations.

---

## User Flow

1. **Create an Account**: 
   - Users fill out a profile specifying their skills for barter, the help they can offer, and the types of assistance they need.

2. **Browse the Community Hub**:
   - The feed displays categorized offers, requests, and projects:
     - **Skill Trades**
     - **Local Tasks/Errands**
     - **Community Projects**
     - **Mutual Aid**
     - **Quick Help Board**

3. **Post & Help**:
   - Users can **post requests** or **offer assistance**. They can negotiate and finalize trades or mark tasks as complete once finished.

4. **Rate and Review**:
   - After a task or trade is completed, users can **rate each other**, building a trusted and engaged community.

---

## Setup Instructions

Follow these steps to get the **backend repository** up and running on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/philiptitus/ProjectX.git
   ```
   
2. **Navigate into the Project Directory**:
   ```bash
   cd ProjectX
   ```

3. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For MacOS/Linux
   # or
   env\Scripts\activate  # For Windows
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the Database**:
   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. The **frontend** can be accessed and set up by visiting:
   ```bash
   https://github.com/philiptitus/xproj.git
   ```

### API Documentation:
- The backend includes a **Django REST Framework** API that serves the frontend.
- For more information about API endpoints, check out the **API Documentation** once the backend server is running at `/api/docs/`.

---

## Status & Development

ProjectX is currently in **steady development**, with new features being added regularly. You can check the **latest progress** by visiting our repository:

- Backend: [ProjectX Backend Repo](https://github.com/philiptitus/ProjectX.git)
- Frontend: [xproj Frontend Repo](https://github.com/philiptitus/xproj.git)

Stay tuned as we continue to expand the app's capabilities and introduce new AI-driven features.

---

## License & Copyright
© Philip Titus 2024

All rights reserved.
