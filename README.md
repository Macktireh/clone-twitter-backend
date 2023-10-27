# Twitter Clone Project with Django & Django Rest Framework

Welcome to my Twitter Clone project built with Django, Django Rest Framework, and Django Channels. This project includes a wide range of features, including authentication, tweet management, likes, retweets, notifications, real-time chat, and more.

## Backend Features

The backend of this project is designed to handle all the features of a Twitter clone. Here's a list of the main features implemented:

- **Authentication**: Endpoints for signup, email activation, login, password reset request, password reset, password change, JWT token refresh, JWT token verification, and logout are available.

- **Tweets**: Tweet endpoints for creating, reading, updating, and deleting tweets.

- **Likes**: Users can like tweets, and there are endpoints to manage these actions.

- **Bookmark**: Users can bookmark tweets, and there are endpoints to manage bookmarks.

- **Retweets**: You can create, read, update, and delete retweets.

- **Retweet Likes**: Users can also like retweets, and there are endpoints to manage these actions.

- **User Management**: Endpoints to get current user information, update current user information, and get information about other users are available. Additionally, you can manage following and followers.

- **Notifications**: The real-time notification system is implemented, allowing users to receive real-time notifications.

- **Real-Time Chat**: Users can communicate in real-time through the chat feature.


## Prerequisites

- Python 3.10+
- Git
- PostgreSQL (optional)
- Docker (optional)


## Installation

1. Clone this repository to your machine.

```bash
git clone https://github.com/Macktireh/clone-twitter-backend.git clone-twitter-backend
```

2. Copy the `.env.example` file to `.env` and configure the environment variables as needed.

### Using Docker

3. Run the following command to start the application with Docker Compose:

```bash
docker-compose up --build
```

### Without Docker

If you prefer not to use Docker, here's how to install the application:

3. Create a Python virtual environment and activate it.

```bash
python -m venv .venv
```

*for MacOS or Linux*
```bash
source .venv/bin/activate
```

*for Windows*
```bash
.\venv\Scripts\activate
```

4. Install Python dependencies using pip:

```bash
pip install -r requirements.txt
```
5. Apply database migrations:

```bash
python manage.py migrate
```

6. Run the Django development server:

```bash
python manage.py runserver
```

The application will be accessible at [http://localhost:8000](http://localhost:8000).


## License

his project is licensed under the MIT License - see the LICENSE file for details.