# Backend Twitter Clone

<p align="center">
  <img src="https://raw.githubusercontent.com/Macktireh/Media/main/images/clone-twitter-back.png" alt="Home screen" width=400>
  <img src="https://raw.githubusercontent.com/Macktireh/Media/main/images/clone-twitter-api1.png" alt="Home screen" width=400>
  <img src="https://raw.githubusercontent.com/Macktireh/Media/main/images/clone-twitter-api2.png" alt="Home screen" width=400>
  <img src="https://raw.githubusercontent.com/Macktireh/Media/main/images/clone-twitter-api3.png" alt="Home screen" width=400>
</p>

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Installation with Docker](#installation-with-docker)
- [Installation without Docker](#installation-without-docker)


## Description

This project is a backend implementation of a Twitter clone using Django, Django REST framework, Django Channels, PostgreSQL, Redis, and Cloudinary. This project includes a wide range of features, including authentication, tweet management, likes, retweets, notifications, real-time chat, and more. This repository contains the backend code. The frontend, built with React, Redux, and other technologies, can be found [clone-twitter-frontend](https://github.com/Macktireh/clone-twitter-frontend).


## Features

- **Authentication**: Signup, email activation, login, password reset request, password reset, password change, JWT token refresh, JWT token verification, and logout.
- **Social Auth**: Login with Google.
- **Tweets**: Create, read, update, and delete tweets.
- **Likes**: Manage likes on tweets.
- **Bookmark**: Manage bookmarked tweets.
- **Retweets**: Manage retweets.
- **Retweet Likes**: Manage likes on retweets.
- **User Management**: Get and update user information, manage following and followers.
- **Notifications**: Real-time notification system.
- **Real-Time Chat**: Real-time chat feature.


## Prerequisites

- Python 3.12+
- Git
- Docker
- PostgreSQL
- Redis
- Cloudinary


## Getting Started

### Common Setup

1. Clone the repository:

```sh
git clone https://github.com/Macktireh/clone-twitter-backend.git
```
```sh
cd clone-twitter-backend
```

2. Configure environment variables: Create a `.env` file based on the `.env.example` file and set your environment variables.

### Installation with Docker

Build and start the Docker containers:

```bash
docker-compose up --build
```

### Installation without Docker

1. Create and activate a virtual environment:

```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```
5. Apply database migrations:

```bash
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```
Your Twitter clone backend should now be up and running. 🎉
The application will be accessible at [http://localhost:8000](http://localhost:8000).


## License

This project is licensed under the [MIT License](LICENSE).