# syzygy 🪐

> In astronomy, a syzygy (/ˈsɪzədʒi/ SIZ-ə-jee; from Ancient Greek συζυγία (suzugía) 'union, yoking', expressing the sense of σύν (syn- "together") and ζυγ- (zug- "a yoke")) is a roughly straight-line configuration of three or more celestial bodies in a gravitational system.
>
> ([source](https://en.wikipedia.org/wiki/Syzygy_(astronomy)))

## Installation

Set up and activate virtual environment in `.venv/`

```bash
python -m venv .venv
source .venv/bin/activate
```

Install required Python libraries:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend && npm install
```

## Usage

### Command-Line Tool (`syzygy.py`)

See `--help` for usage instructions.

### Web application

`Makefile` rules:

| rule | description |
| -- | -- |
| `dev-backend` | run backend in dev mode |
| `dev-frontend` | run frontend in dev mode |


## Configuration

### Backend (Flask `app.py`)

The backend uses the following shell environment variables:

| name | description | required |
| -- | -- | -- |
| `PORT` | server port | N: default = `defaults.PORT` |
| `DEBUG` | enable/disable debug logging | N: default = `defaults.DEBUG` |


### Frontend (SvelteKit `./frontend`)

The `syzygy` frontend uses the following environment variables (stored in `frontend/.env`):

| name | description | required |
| -- | -- | -- |
| `PUBLIC_FLASK_HOST` | Flask server host | Y |
| `PUBLIC_FLASK_PORT` | Flask server port | Y |


where the Flask server is the machine running `app.py`.

Example configuration (Flask server on port `8000` of the same host as the frontend):

```bash
# Flask server on port 8000 of the same host as the frontend
PUBLIC_FLASK_HOST="http://localhost"
PUBLIC_FLASK_PORT=8000
```

## To do
- [x] document environment variables
- [ ] Makefile for running web app
    - [x] dev
    - [ ] prod
- [ ] improve rendered SVGs
    - [x] scale to boxes
    - [ ] add scrollbar if too long
    - [x] randomise member colours
    - [x] member info on hover: [DaisyUI tooltip](https://daisyui.com/components/tooltip)
- [ ] improve test cases (currently in `test_struct.c`)
- [x] favicon and title
- [ ] other pages
    - [ ] how to use
    - [ ] examples
        - [ ] base
        - [x] tidy up
    - [ ] about
