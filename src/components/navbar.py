"""
NavBar

A class for creating a responsive navigation bar with customizable elements.

This class allows you to create a navigation bar with a logo, brand name, menu items,
and call-to-action buttons. It's designed to work with FastHTML and includes HTMX support.

Attributes:
    logo_src (str): The source URL for the logo image.
    brand_name (str): The name of the brand to display next to the logo.
    menu_items (List[NavMenuItem]): A list of NavMenuItem objects representing the menu items.
    cta_text (str): The text for the main call-to-action button. Default is "Get started".
    brand_href (str): The URL for the brand logo link. Default is "#".
    additional_buttons (List[Dict]): A list of dictionaries defining additional buttons.
    cls (str): CSS classes for the main Nav element. Default is "bg-white border-gray-200 dark:bg-gray-900".
    htmx (Dict[str, str]): HTMX attributes to apply to the Nav element.

Methods:
    __xt__(): Renders the navigation bar as an XT (XML Tree) object.

Usage:
    navbar = NavBar(
        logo_src="https://flowbite.com/docs/images/logo.svg",
        brand_name="Flowbite",
        menu_items=[
            NavMenuItem("Home", "#", active=True),
            NavMenuItem("About", "#about"),
            NavMenuItem("Services", "#services"),
            NavMenuItem("Contact", "#contact")
        ],
        cta_text="Sign Up",
        brand_href="https://flowbite.com/",
        additional_buttons=[
            {"text": "Log In", "cls": "text-gray-800 hover:bg-gray-50"}
        ],
        htmx={"boost": "true"}
    )

    # Render the navbar
    rendered_navbar = navbar.__xt__()
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from fasthtml.common import *

@dataclass
class NavMenuItem:
    """
    Represents a single item in the navigation menu.

    Attributes:
        text (str): The text to display for the menu item.
        href (str): The URL that the menu item links to.
        active (bool): Whether this item is currently active. Default is False.
        cls (str): Additional CSS classes for the menu item. Default is "".
    """
    text: str
    href: str
    active: bool = False
    cls: str = ""

@dataclass
class NavBar:
    """
    A class for creating a responsive navigation bar.

    Attributes:
        logo_src (str): The source URL for the logo image.
        brand_name (str): The name of the brand to display next to the logo.
        menu_items (List[NavMenuItem]): A list of NavMenuItem objects representing the menu items.
        cta_text (str): The text for the main call-to-action button. Default is "Get started".
        brand_href (str): The URL for the brand logo link. Default is "#".
        additional_buttons (List[Dict]): A list of dictionaries defining additional buttons.
        cls (str): CSS classes for the main Nav element. Default is "bg-white border-gray-200 dark:bg-gray-900".
        htmx (Dict[str, str]): HTMX attributes to apply to the Nav element.
    """
    logo_src: str
    brand_name: str
    menu_items: List[NavMenuItem]
    cta_text: str = "Get started"
    brand_href: str = "#"
    additional_buttons: List[Dict] = field(default_factory=list)
    cls: str = "bg-white border-gray-200 dark:bg-gray-900"
    htmx: Dict[str, str] = field(default_factory=dict)

    def __xt__(self):
        """
        Renders the navigation bar as an XT (XML Tree) object.

        Returns:
            Nav: The rendered navigation bar as a Nav element.
        """
        return Nav(
            self._render_container(),
            cls=self.cls,
            **{f"hx_{k}": v for k, v in self.htmx.items()}
        )

    def _render_container(self):
        return Div(
            self._render_brand(),
            self._render_buttons(),
            self._render_menu(),
            cls="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4"
        )

    def _render_brand(self):
        return A(
            Img(src=self.logo_src, cls='h-8', alt=f'{self.brand_name} Logo'),
            Span(self.brand_name, cls='self-center text-2xl font-semibold whitespace-nowrap dark:text-white'),
            href=self.brand_href,
            cls='flex items-center space-x-3 rtl:space-x-reverse'
        )

    def _render_buttons(self):
        buttons = [
            Button(
                self.cta_text,
                type='button',
                cls='text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'
            )
        ]
        buttons.extend([Button(**btn) for btn in self.additional_buttons])
        
        return Div(
            *buttons,
            self._render_mobile_menu_button(),
            cls='flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse'
        )

    def _render_mobile_menu_button(self):
        return Button(
            Span('Open main menu', cls='sr-only'),
            Svg(
                Path(stroke='currentColor', stroke_linecap='round', stroke_linejoin='round', stroke_width='2', d='M1 1h15M1 7h15M1 13h15'),
                cls='w-5 h-5',
                aria_hidden='true',
                xmlns='http://www.w3.org/2000/svg',
                fill='none',
                viewbox='0 0 17 14'
            ),
            data_collapse_toggle='navbar-cta',
            type='button',
            cls='inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600',
            aria_controls='navbar-cta',
            aria_expanded='false'
        )

    def _render_menu(self):
        return Div(
            Ul(
                *[self._render_menu_item(item) for item in self.menu_items],
                cls='flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700'
            ),
            cls='items-center justify-between hidden w-full md:flex md:w-auto md:order-1',
            id='navbar-cta'
        )

    def _render_menu_item(self, item: NavMenuItem):
        base_cls = "block py-2 px-3 md:p-0 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700"
        active_cls = "text-white bg-blue-700 md:bg-transparent md:text-blue-700 md:dark:text-blue-500"
        inactive_cls = "text-gray-900"
        
        cls = f"{base_cls} {active_cls if item.active else inactive_cls} {item.cls}".strip()
        
        return Li(
            A(item.text, href=item.href, cls=cls, aria_current="page" if item.active else None)
        )