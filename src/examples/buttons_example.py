from typing import List
from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from components import CustomButton

# Usage examples:
default_button = CustomButton("Default")
alternative_button = CustomButton("Alternative", style="alternative")
dark_button = CustomButton("Dark", style="dark")
light_button = CustomButton("Light", style="light")
green_button = CustomButton("Green", style="green")
red_button = CustomButton("Red", style="red")
yellow_button = CustomButton("Yellow", style="yellow")
purple_button = CustomButton("Purple", style="purple")

# Pill style examples
default_pill = CustomButton("Default", pill=True)
alternative_pill = CustomButton("Alternative", style="alternative", pill=True)
dark_pill = CustomButton("Dark", style="dark", pill=True)
light_pill = CustomButton("Light", style="light", pill=True)
green_pill = CustomButton("Green", style="green", pill=True)
red_pill = CustomButton("Red", style="red", pill=True)
yellow_pill = CustomButton("Yellow", style="yellow", pill=True)
purple_pill = CustomButton("Purple", style="purple", pill=True)

# HTMX example
htmx_button = CustomButton(
    "Load More",
    style="default",
    htmx={
        "get": "/load-more",
        "target": "#content",
        "swap": "beforeend"
    }
)

# Button with additional attributes
custom_button = CustomButton(
    "Custom",
    style="default",
    additional_attrs={
        "data-custom": "value",
        "aria-label": "Custom Button"
    }
)

app = FastHTMLWithLiveReload(
    hdrs=(
        Link(rel="stylesheet", href="/static/dist/css/output.css"),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.8.0/flowbite.min.js", defer=True)
    )
)
app.mount("/static", StaticFiles(directory="../static"), name="static")

rt: app.route = app.route

@rt("/", methods=["GET"])
async def index():
        
    return Div(
        H1("Button Styles Demo"),
        H2("Regular Buttons"),
        default_button(),
        alternative_button(),
        dark_button(),
        light_button(),
        green_button(),
        red_button(),
        yellow_button(),
        purple_button(),
        H2("Pill Buttons"),
        default_pill(),
        alternative_pill(),
        dark_pill(),
        light_pill(),
        green_pill(),
        red_pill(),
        yellow_pill(),
        purple_pill(),
        H2("Custom Buttons"),
        htmx_button(),
        custom_button()
    )
        

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)