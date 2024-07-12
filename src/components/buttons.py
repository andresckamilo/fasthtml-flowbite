from fasthtml.common import *
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class CustomButton:
    label: str
    style: str = "default"
    type: str = "button"
    size: str = "base"
    pill: bool = False
    htmx: Dict[str, str] = field(default_factory=dict)
    additional_attrs: Dict[str, Any] = field(default_factory=dict)

    _style_classes = {
        "default": "text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800",
        "alternative": "text-gray-900 focus:outline-none bg-white border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700",
        "dark": "text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-4 focus:ring-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-700 dark:border-gray-700",
        "light": "text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700",
        "green": "focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800",
        "red": "focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900",
        "yellow": "focus:outline-none text-white bg-yellow-400 hover:bg-yellow-500 focus:ring-4 focus:ring-yellow-300 dark:focus:ring-yellow-900",
        "purple": "focus:outline-none text-white bg-purple-700 hover:bg-purple-800 focus:ring-4 focus:ring-purple-300 dark:bg-purple-600 dark:hover:bg-purple-700 dark:focus:ring-purple-900"
    }

    _size_classes = {
        "xs": "px-3 py-2 text-xs",
        "sm": "px-3 py-2 text-sm",
        "base": "px-5 py-2.5 text-sm",
        "lg": "px-5 py-3 text-base",
        "xl": "px-6 py-3.5 text-base"
    }

    def __call__(self):
        style_classes = self._style_classes.get(self.style, self._style_classes["default"])
        size_classes = self._size_classes.get(self.size, self._size_classes["base"])

        classes = [
            style_classes,
            size_classes,
            "font-medium",
            "rounded-full" if self.pill else "rounded-lg",
            "text-center",
            "me-2 mb-2"
        ]

        attrs = {
            "type": self.type,
            "cls": " ".join(classes),
            **self.additional_attrs
        }

        # Add HTMX attributes
        for key, value in self.htmx.items():
            attrs[f"hx_{key}"] = value

        return Button(self.label, **attrs)

# # Usage examples:
# default_button = CustomButton("Default")
# alternative_button = CustomButton("Alternative", style="alternative")
# dark_button = CustomButton("Dark", style="dark")
# light_button = CustomButton("Light", style="light")
# green_button = CustomButton("Green", style="green")
# red_button = CustomButton("Red", style="red")
# yellow_button = CustomButton("Yellow", style="yellow")
# purple_button = CustomButton("Purple", style="purple")

# # Pill style examples
# default_pill = CustomButton("Default", pill=True)
# alternative_pill = CustomButton("Alternative", style="alternative", pill=True)
# dark_pill = CustomButton("Dark", style="dark", pill=True)
# light_pill = CustomButton("Light", style="light", pill=True)
# green_pill = CustomButton("Green", style="green", pill=True)
# red_pill = CustomButton("Red", style="red", pill=True)
# yellow_pill = CustomButton("Yellow", style="yellow", pill=True)
# purple_pill = CustomButton("Purple", style="purple", pill=True)

# # HTMX example
# htmx_button = CustomButton(
#     "Load More",
#     style="default",
#     htmx={
#         "get": "/load-more",
#         "target": "#content",
#         "swap": "beforeend"
#     }
# )

# # Button with additional attributes
# custom_button = CustomButton(
#     "Custom",
#     style="default",
#     additional_attrs={
#         "data-custom": "value",
#         "aria-label": "Custom Button"
#     }
# )