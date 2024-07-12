from fasthtml.common import *
from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class AccordionItem:
    title: str
    content: List[str]
    id: str = field(default_factory=lambda: f"accordion-{uuid.uuid4().hex[:8]}")

    def __xt__(self):
        return (
            H2(
                Button(
                    Span(self.title),
                    Svg(
                        Path(stroke='currentColor', stroke_linecap='round', stroke_linejoin='round', stroke_width='2', d='M9 5 5 1 1 5'),
                        data_accordion_icon='',
                        cls='w-3 h-3 rotate-180 shrink-0',
                        aria_hidden='true',
                        xmlns='http://www.w3.org/2000/svg',
                        fill='none',
                        viewbox='0 0 10 6'
                    ),
                    type='button',
                    cls='flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-0 border-gray-200 rounded-t-xl focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3',
                    data_accordion_target=f'#{self.id}-body',
                    aria_expanded='false',
                    aria_controls=f'{self.id}-body'
                ),
                id=f'{self.id}-heading'
            ),
            Div(
                Div(
                    *[P(content, cls='mb-2 text-gray-500 dark:text-gray-400') for content in self.content],
                    cls='p-5 border border-b-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900'
                ),
                id=f'{self.id}-body',
                cls='hidden',
                aria_labelledby=f'{self.id}-heading'
            )
        )
    
@dataclass
class Accordion:
    items: List[AccordionItem]

    def __xt__(self):
        return Div(
            *[item.__xt__() for item in self.items],
            id='accordion-collapse',
            data_accordion='collapse'
        ) 
    
# Usage accordion_items = [
    #     AccordionItem(
    #         "What is Flowbite?",
    #         [
    #             "Flowbite is an open-source library of interactive components built on top of Tailwind CSS including buttons, dropdowns, modals, navbars, and more.",
    #             "Check out this guide to learn how to get started and start developing websites even faster with components on top of Tailwind CSS."
    #         ]
    #     ),
    #     AccordionItem(
    #         "Is there a Figma file available?",
    #         [
    #             "Flowbite is first conceptualized and designed using the Figma software so everything you see in the library has a design equivalent in our Figma file.",
    #             "Check out the Figma design system based on the utility classes from Tailwind CSS and components from Flowbite."
    #         ]
    #     ),
    #     AccordionItem(
    #         "What are the differences between Flowbite and Tailwind UI?",
    #         [
    #             "The main difference is that the core components from Flowbite are open source under the MIT license, whereas Tailwind UI is a paid product. Another difference is that Flowbite relies on smaller and standalone components, whereas Tailwind UI offers sections of pages.",
    #             "However, we actually recommend using both Flowbite, Flowbite Pro, and even Tailwind UI as there is no technical reason stopping you from using the best of two worlds.",
    #             "Learn more about these technologies:"
    #         ]
    #     )
    # ]
    