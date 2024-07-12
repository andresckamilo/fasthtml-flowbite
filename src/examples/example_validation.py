from typing import Callable

import uvicorn
from fasthtml.common import *
from starlette.staticfiles import StaticFiles
from components import CustomButton, FloatingLabelForm, FormSection, FormField, NavBar, NavMenuItem

app = FastHTMLWithLiveReload(
    hdrs=(
        Link(rel="stylesheet", href="/static/dist/css/output.css"),
        Script(
            src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.8.0/flowbite.min.js",
            defer=True,
        ),
    )
)
app.mount("/static", StaticFiles(directory="../static"), name="static")

rt: Callable = app.route

form_structure = [
    FormSection([
        FormField(
            name="username",
            label="Username",
            type="text",
            htmx={
                "post": "/check-username",
                "trigger": "change",
                "target": "next .validation-message",
                "swap": "innerHTML"
            },
            additional_attrs={"autocomplete": "off"}
        )
    ]),
    FormSection([
        FormField(
            name="password",
            label="Password",
            type="password",
            htmx={
                "post": "/check-password-match",
                "trigger": "change",
                "target": "#password-match-validation",
                "include": "#confirm_password",
            },
        )
    ]),
    FormSection([
        FormField(
            name="confirm_password",
            label="Confirm Password",
            type="password",
            htmx={
                "post": "/check-password-match",
                "trigger": "change",
                "target": "#password-match-validation",
                "include": "#password",
            },
        )
    ]),
    FormSection(
        [
            FormField("first_name", "First name"),
            FormField("last_name", "Last name"),
        ],
        layout="double",
    ),
    FormSection(
        [
            FormField(
                "phone",
                "Phone number (123-456-7890)",
                type="tel",
                pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}",
            ),
            FormField("company", "Company (Ex. Google)"),
        ],
        layout="double",
    ),
    FormSection([FormField("bio", "Biography", type="textarea")])
]

def create_navbar(current_path):
    return NavBar(
        logo_src="/static/logo.svg",
        brand_name="TechCorp",
        menu_items=[
            NavMenuItem("Home", "/", active=current_path == "/"),
            NavMenuItem("About", "/about", active=current_path == "/about"),
            NavMenuItem("Register", "/register", active=current_path == "/register"),
            NavMenuItem("Contact", "/contact", active=current_path == "/contact"),
        ],
        cta_text="Login",
        brand_href="/",
        htmx={"boost": "true"}
    )

@rt("/", methods=["GET"])
async def home():
    return (
        Title("TechCorp - Home"),
        create_navbar("/"),
        Main(
            H1("Welcome to TechCorp", cls="text-3xl font-bold mb-4"),
            P("Innovating for a better tomorrow.", cls="text-xl"),
            cls="container mx-auto mt-8 px-4"
        )
    )

@rt("/about", methods=["GET"])
async def about():
    return (
        Title("TechCorp - About Us"),
        create_navbar("/about"),
        Main(
            H1("About TechCorp", cls="text-3xl font-bold mb-4"),
            P("We are a cutting-edge technology company focused on innovation.", cls="text-xl"),
            cls="container mx-auto mt-8 px-4"
        )
    )

@rt("/register", methods=["GET"])
async def register():
    form = FloatingLabelForm(
        sections=form_structure,
        custom_submit_button=CustomButton(
            "Register",
            style="default",
            additional_attrs={"type": "submit", "aria-label": "Register"}
        ),
        htmx={"post": "/submit-form", "target": "#form-response"}
    )
    return (
        Title("TechCorp - Register"),
        create_navbar("/register"),
        Main(
            H1("Register for TechCorp", cls="text-3xl font-bold mb-4"),
            form,
            Div(id="form-response"),
            cls="container mx-auto mt-8 px-4"
        )
    )

@rt("/check-username", methods=["POST"])
async def check_username(request):
    form_data = await request.form()
    username = form_data.get('username', '')
    print(username)
    
    if username.lower() == "admin":
        return P(
            Span("Oops!", cls="font-medium"),
            " Username already taken!",
            cls="mt-2 text-sm text-red-600 dark:text-red-500"
        )
    else:
        return P(
            Span("Alright!", cls="font-medium"),
            " Username available!",
            cls="mt-2 text-sm text-green-600 dark:text-green-500"
        )

@rt("/contact", methods=["GET"])
async def contact():
    return (
        Title("TechCorp - Contact Us"),
        create_navbar("/contact"),
        Main(
            H1("Contact Us", cls="text-3xl font-bold mb-4"),
            P("Get in touch with us for any inquiries.", cls="text-xl"),
            cls="container mx-auto mt-8 px-4"
        )
    )


@rt("/check-password-match", methods=["POST"])
async def check_password_match(request):
    form_data = await request.form()
    password = form_data.get('password', '')
    confirm_password = form_data.get('confirm_password', '')
    
    if password == confirm_password:
        return Div(
            P(
                Span("Great!", cls="font-medium"),
                " Passwords match.",
                cls="mt-2 text-sm text-green-600 dark:text-green-500"
            ),
            id="password-match-validation",
            cls="mt-2"
        )
    else:
        return Div(
            P(
                Span("Oops!", cls="font-medium"),
                " Passwords do not match.",
                cls="mt-2 text-sm text-red-600 dark:text-red-500"
            ),
            id="password-match-validation",
            cls="mt-2"
        )

@rt("/submit-form", methods=["POST"])
async def submit_form(request):
    form_data = await request.form()
    password = form_data.get('password')
    confirm_password = form_data.get('confirm_password')
    
    if password != confirm_password:
        return Div(
            H2("Form Submission Failed", cls="text-red-600"),
            P("Passwords do not match. Please try again."),
            cls="text-center"
        )
    
    # Process the form data (e.g., save to database)
    # For this example, we'll just return a success message
    return Div(
        H2("Registration Successful!", cls="text-green-600"),
        P(f"Welcome, {form_data.get('username')}!"),
        cls="text-center"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)