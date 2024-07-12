"""
FloatingLabelForm

A class for creating forms with floating labels and HTMX-powered validation.

This class allows you to create responsive, accessible forms with real-time
validation using HTMX. It supports various input types, custom layouts, and
server-side validation.

Attributes:
    sections (List[FormSection]): A list of FormSection objects that define the
                                  structure and fields of the form.
    submit_label (str): The text to display on the submit button.
                        Default is "Submit".
    cls (str): CSS classes to apply to the form. Default is "max-w-md mx-auto".
    htmx (Dict[str, str]): HTMX attributes to apply to the form.
    custom_submit_button (Optional[CustomButton]): A CustomButton object to use
                                                   as the submit button instead
                                                   of the default.

Methods:
    __xt__(): Renders the form as an XT (XML Tree) object.
    render_section(section: FormSection): Renders a single form section.
    floating_input(field: FormField): Renders a single form field with a
                                      floating label.
    two_column_inputs(input1, input2): Renders two inputs in a two-column layout.
    render_submit_button(): Renders the form's submit button.

Usage:
    form = FloatingLabelForm(
        sections=[
            FormSection([
                FormField("username", "Username", htmx={
                    "post": "/check-username",
                    "trigger": "change",
                    "target": "#username-validation"
                }),
                FormField("password", "Password", type="password"),
                FormField("confirm_password", "Confirm Password", type="password")
            ])
        ],
        custom_submit_button=CustomButton("Register", style="primary"),
        htmx={"post": "/submit-form", "swap": "outerHTML"}
    )

    # Render the form
    rendered_form = form.__xt__()
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from fasthtml.common import *

from .buttons import CustomButton


@dataclass
class FormField:
    """
    Represents a single form field.

    Attributes:
        name (str): The name attribute of the input field.
        label (str): The label text for the input field.
        type (str): The type of input (e.g., "text", "password"). Default is "text".
        pattern (str): A regex pattern for input validation. Default is None.
        required (bool): Whether the field is required. Default is True.
        placeholder (str): Placeholder text for the input. Default is " ".
        additional_attrs (Dict[str, Any]): Additional HTML attributes for the input.
        htmx (Dict[str, str]): HTMX attributes for the input.
    """

    name: str
    label: str
    type: str = "text"
    pattern: str = None
    required: bool = True
    placeholder: str = " "
    additional_attrs: Dict[str, Any] = field(default_factory=dict)
    htmx: Dict[str, str] = field(default_factory=dict)


@dataclass
class FormSection:
    """
    Represents a section of the form, containing one or more FormFields.

    Attributes:
        fields (List[FormField]): The fields in this section.
        layout (str): The layout of the section ("single" or "double").
                      Default is "single".
    """

    fields: List[FormField]
    layout: str = "single"


@dataclass
class FloatingLabelForm:
    """
    A class for creating forms with floating labels and HTMX-powered validation.

    Attributes:
        sections (List[FormSection]): The sections of the form.
        submit_label (str): The text for the submit button. Default is "Submit".
        cls (str): CSS classes for the form. Default is "max-w-md mx-auto".
        htmx (Dict[str, str]): HTMX attributes for the form.
        custom_submit_button (Optional[CustomButton]): A custom submit button.
    """

    sections: List[FormSection]
    submit_label: str = "Submit"
    cls: str = "max-w-md mx-auto"
    htmx: Dict[str, str] = field(default_factory=dict)
    custom_submit_button: Optional[CustomButton] = None

    def __xt__(self):
        """
        Renders the form as an XT (XML Tree) object.

        Returns:
            Form: The rendered form as an XT object.
        """
        form_attrs = {"cls": self.cls}
        form_attrs.update({f"hx_{key}": value for key, value in self.htmx.items()})

        return Form(
            *[self.render_section(section) for section in self.sections],
            self.render_submit_button(),
            **form_attrs,
        )

    def render_section(self, section: FormSection):
        """
        Renders a single form section.

        Args:
            section (FormSection): The section to render.

        Returns:
            Union[Div, XT]: The rendered section.
        """
        if section.layout == "double":
            return self.two_column_inputs(
                self.floating_input(section.fields[0]),
                self.floating_input(section.fields[1]),
            )
        else:
            return Div(*[self.floating_input(field) for field in section.fields])

    def floating_input(self, field: FormField):
        """
        Renders a single form field with a floating label.

        Args:
            field (FormField): The field to render.

        Returns:
            Div: The rendered field as a Div containing the input and label.
        """
        input_attrs = {
            "type": field.type,
            "name": field.name,
            "id": f"floating_{field.name}",
            "placeholder": field.placeholder,
            "required": "" if field.required else None,
            "pattern": field.pattern,
        }

        default_cls = "block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
        additional_cls = field.additional_attrs.pop("cls", "")
        input_attrs["cls"] = f"{default_cls} {additional_cls}".strip()

        input_attrs.update({f"hx_{key}": value for key, value in field.htmx.items()})
        input_attrs.update(field.additional_attrs)

        return Div(
            Input(**input_attrs),
            Label(
                field.label,
                fr=f"floating_{field.name}",
                cls="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6",
            ),
            Div(cls="validation-message"),  
            cls="relative z-0 w-full mb-5 group",
        )

    def two_column_inputs(self, input1, input2):
        """
        Renders two inputs in a two-column layout.

        Args:
            input1: The first input to render.
            input2: The second input to render.

        Returns:
            Div: A Div containing the two inputs in a grid layout.
        """
        return Div(input1, input2, cls="grid md:grid-cols-2 md:gap-6")

    def render_submit_button(self):
        """
        Renders the form's submit button.

        Returns:
            Union[CustomButton, Button]: The rendered submit button.
        """
        if self.custom_submit_button:
            button = self.custom_submit_button
            button.type = "submit"
            button.htmx.update(self.htmx)
            return button()
        else:
            return Button(
                self.submit_label,
                type="submit",
                cls="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800",
            )


# Example usage:

# form_structure = [
#         FormSection([FormField("email", "Email address", type="email")]),
#         FormSection([FormField("password", "Password", type="password")]),
#         FormSection([FormField("repeat_password", "Confirm password", type="password")]),
#         FormSection([
#             FormField("first_name", "First name"),
#             FormField("last_name", "Last name")
#         ], layout="double"),
#         FormSection([
#             FormField("phone", "Phone number (123-456-7890)", type="tel", pattern="[0-9]{3}-[0-9]{3}-[0-9]{4}"),
#             FormField("company", "Company (Ex. Google)")
#         ], layout="double")
#     ]
#     form_structure.append(FormSection([FormField("bio", "Biography", type="textarea")]))
#     form = FloatingLabelForm(sections=form_structure)
