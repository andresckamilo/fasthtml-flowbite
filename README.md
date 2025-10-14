# Current state:

This project was abandoned due to time limitation.

# fasthtml-flowbite

`fasthtml-flowbite` shows how to wire [FastHTML](https://github.com/answerdev/fasthtml), Tailwind CSS, Flowbite, and HTMX together. The project introduces Python helpers for common Flowbite widgets plus runnable FastHTML demos that highlight interactive behaviours without writing JavaScript.

## Prerequisites
- Python 3.10 or newer
- Node.js 18+ (includes `npm`)
- Access to the internet to fetch Flowbite's CDN script (or replace with a local bundle)

## Setup
1. (Recommended) create and activate a virtual environment, then install the Python packages used by the examples:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use .venv\\Scripts\\activate
   pip install fasthtml uvicorn starlette
   ```
2. Install the Node dependencies needed for Tailwind and Flowbite:
   ```bash
   npm install
   ```

## Build the CSS
Generate the stylesheet that Flowbite expects under `src/static/dist/css/output.css`:
```bash
mkdir -p src/static/dist/css
npx tailwindcss -i src/styles/main.css -o src/static/dist/css/output.css --watch
```
Keep the watcher running while you develop so Tailwind picks up template changes.

## Running the example apps
Each example lives in `src/examples` and assumes you have already built the CSS.

- **Buttons catalogue** – explore `CustomButton` variations.
  ```bash
  cd src/examples
  uvicorn buttons_example:app --reload
  ```
  Visit `http://127.0.0.1:8000/`.

- **Form validation demo** – shows the navbar, floating label form, and HTMX-powered validation endpoints.
  ```bash
  cd src/examples
  uvicorn example_validation:app --reload
  ```

Stop the Tailwind watcher or the Uvicorn server with `Ctrl+C` once you are done.

## Using the components in your project
Import directly from `src/components` (exposed via `__init__.py`) and compose them inside FastHTML views:

```python
from components import CustomButton, FloatingLabelForm, FormSection, FormField

submit = CustomButton(
    "Save",
    style="green",
    htmx={"post": "/save", "target": "#result", "swap": "outerHTML"}
)

form = FloatingLabelForm(
    sections=[FormSection([FormField("email", "Email", type="email")])],
    custom_submit_button=submit,
    htmx={"post": "/submit", "target": "#result"}
)

async def view():
    return (
        Title("Profile"),
        form,
        Div(id="result"),
    )
```

## Component reference
- `src/components/buttons.py` – `CustomButton` renders Flowbite-styled buttons (regular and pill) and accepts HTMX plus arbitrary HTML attributes.
- `src/components/accordion.py` – `Accordion` and `AccordionItem` output accessible accordions with auto-generated IDs.
- `src/components/floating_form.py` – `FloatingLabelForm` builds multi-section forms with floating labels, validation placeholders, and optional custom submit buttons.
- `src/components/navbar.py` – `NavBar` and `NavMenuItem` render a responsive navigation bar with desktop and mobile menus.

## Project layout
```
.
├── README.md
├── package.json / package-lock.json
├── tailwind.config.js
└── src
    ├── components        # Flowbite-inspired Python components
    ├── examples          # FastHTML demo apps
    └── styles            # Tailwind entry point (compiled to static/dist)
```

## Development notes
- Tailwind configuration (`tailwind.config.js`) overrides the default colour palette; change it to align with your brand.
- Flowbite JavaScript is referenced from a CDN inside the FastHTML app headers. Swap to a locally bundled script if you need offline support.
- When creating new UI helpers, add them under `src/components` and export them in `src/components/__init__.py` for convenient imports.
- If your FastHTML routes use HTMX swaps, remember to include the relevant `hx_*` attributes when instantiating components.

## Contributing
Pull requests are welcome. Please keep docstrings, README sections, and examples in sync when you add or change components.

## License
Distributed under MIT license.
