# Modul Graph Backend

## Development

### Using Devcontainer

This project has a working devcontainer setup. This is the preferred method for development.

### Manual Setup

#### 1. Install dependencies

This project requires the following applications/tools to work: 

- Python 3 (>= 3.12)
- Poetry
- Neo4J
- gettext

#### 2. Setup project

Before you start with the next steps be sure that a Neo4J database is running!

```bash 
# 1. Setup your venv using poetry: 
POETRY_VIRTUALENVS_IN_PROJECT=1 poetry install

# 1.5 make sure you use that virtualenv

# 2. Create .env file in project root (see: .env.example)
cp .env.example .env

# 3. Generate translations
./gen_translations.sh

# 4. Create initial graph
python -m modul_graph --recreate-graph
```

### Running the Project

Run the backend by typing: `python -m modul_graph`


## Production

For production it is recommended to use the docker containers. 

Take a look at the docker-compose.yml and make changes as you see fit


