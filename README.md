![coffee_shop](https://user-images.githubusercontent.com/73973314/199586107-6db2b82d-0b92-486c-a9e7-8b32bb9dbae4.PNG)

# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

Udacity has decided to open a new digitally enabled cafe for students to order drinks, socialize, and study hard.

I demonstrated my newly learned skills to create a full stack drink menu application. The application does the following:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.


I recommend checking the sections in order. Start by reading the READMEs in:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## About the Stack

This is a full stack application. It is designed with key functional areas:

### Backend

The `./backend` directory contains a completed Flask server with a written SQLAlchemy module to simplify data needs. I completed the required endpoints, configure, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. I updated the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.

[View the README.md within ./frontend for more details.](./frontend/README.md)
