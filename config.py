import os

API_KEY = os.environ.get("OPENROUTER_API_KEY", "sk-or-v1-...")
ENDPOINT = "https://openrouter.ai/api/v1"

MODEL = os.environ.get(
    "OPENROUTER_MODEL",
    "poolside/laguna-m.1:free"
)
SYSTEM_PROMPT = """ Act as a helpful, structured assistant generating modern, simple, and highly efficient web applications without hallucinating. Use React (functional components/hooks), Next.js, TypeScript, and Tailwind CSS, ensuring all code uses the latest, widely supported, and fully compatible versions with no deprecated features. Carefully include every feature requested by the user, working step-by-step and asking for clarification if unsure, while strictly adhering to the specified tech stack unless directed otherwise.
The app should be responsive and work well on different screen sizes and devices, including desktops, tablets, and mobile phones. Use CSS media queries to adjust the layout and styling based on the screen size. Ensure that all interactive elements are easily tappable on touch devices, with appropriate spacing and sizing. Test the app on different devices and browsers to ensure compatibility and a consistent user experience."""



# ---------------------------------------------
# Example prompts for the user to select from
# ---------------------------------------------


EXAMPLES = [
    {
        "title": "Photography Portfolio Website",
        "description": "Make a page that showcases a photography portfolio. The page should have a gallery of images, a contact form, and a section for the photographer's bio."
    },
    {
        "title": "E-commerce Website",
        "description": "Make a page that showcases an e-commerce website. The page should have a product catalog, a shopping cart, and a checkout process."
    },
    {
        "title": "Blog Website",
        "description": "Make a page that showcases a blog website. The page should have a list of blog posts, a search functionality, and a comment section."
    },
]