# Senior Python Software Engineer Assignment

## About the solution

This project implements the following functionality:

1. An AI agent that answers user questions. In particular, it only answers questions related to 
either math or history. It doesn't answer any other questions.
2. An API that allows the user to submit questions and receive answers.



## Practical considerations

Gemini is used as the underlying AI model to answer the questions. The only reason for this choice 
is that Gemini offers a free tier, which simplifies things a lot for this case. In a real 
application, it should be fairly straightforward to replace it with any other model.



## Setting up the project

### Prerequisites

You will need to have the following things installed in your system:

- `python`: I used Python `3.13.5` during development and testing, but earlier versions would most 
likely work as well. However, I cannot make any promises in that regard.
- `docker`: I used Docker `4.40.0`, but any recent version should work just fine.
- `uv` for Python project and dependencies management. You can find the official install 
instructions [here](https://docs.astral.sh/uv/getting-started/installation/)


### Environment variables

The AI agent is built using Gemini. In order to access Gemini you will need an API key 
(get it [here](https://aistudio.google.com/app/apikey)).

The application expects environment variables to be defined in a `.env` file. You can find an 
example of what this file should look like in `.env.example`. In order to get things to work:

1. Create a `.env` file with the same keys as `.env.example`
2. Replace the dummy value of `GOOGLE_API_KEY` with your API key


### Running locally

This is optional. You can also run everything with Docker with a single command (see [Running with Docker](#running-with-docker))

#### Installing dependencies

From the project root, you can install all required dependencies with `uv`:

```shell
uv sync
```

This will generate a virtual environment in the `.venv` directory.

You can then run the API in development mode by running (from the project root):

```shell
fastapi dev ./assignment/api/app.py
```

The API will then be reachable at `http://localhost:8000`

To run the tests:

```shell
pytest
```


### Running with Docker

Everything should work just fine by running `docker compose up`. Once everything is up and running, 
you should be able to reach the API at `http://localhost:8000`.


### API documentation

You can find the API documentation at `http://localhost:8000/docs`