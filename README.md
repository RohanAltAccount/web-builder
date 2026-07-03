# About
This is a simple web builder (just for fun) I made that retrieves the model from OpenRouter (currently using Poolside Laguna M1: Free) using an API key. Anyone can use this (open source). You can contribute to this project or use the template to configure something of your own. You can change the model by switching out the API key and model name. Feel free to look through the code. I have included some comments in there as a guide.

# How To Use
1. **Clone the repo** at https://github.com/RohanAltAccount/web-builder in IDE/code editor of your choice (I've only used VS Code and Xcode, so I don't know much about the interfaces of other ones).

2. **Create the virtual environment** by running the following in your project terminal:


```
python3 -m venv .venv 
source .venv/bin/activate
```

Here you go, Windows users (*AKA people who refuse to accept that MacOS is better*):

```
python -m venv 
.venv .venv\Scripts\activate
```

3. If you don't have them already, **install dependencies**.

` 
python -m pip install -r requirements.txt
`

If you don't have a requirements.txt, install manually:
`
python -m pip install gradio openai python-dotenv modelscope-studio dashscope
`

4. Start **setting up environment variables**. Create a .env file at the root of the project. Paste the following lines into it.

```
OPENROUTER_API_KEY=your_openrouter_api_key_here 
OPENROUTER_MODEL=poolside/laguna-m.1:free
```

Fill in the values with your model of choice and secret key.

5. Find a model and **get your key**. For more information, visit [this page]. (https://openrouter.ai/docs/quickstart#using-the-openai-sdk)

If you're gonna publish you repo publicly, keep your .env private. **DO NOT COMMIT YOUR KEY***. Instead, add .env to a .gitignore file (if you don't already have one).

6. **Run it**. Whoo. You're done.
Run this in the terminal:
`
python app.py
`

7. Open the localhost URL.

*Quick Note: If you want to share the app (while it's running) with someone else, add `share=True` to the `demo.launch(css=css)` section. There is also a comment in the code to help you there. This way, someone else can open the app on their device. Only do it if you're sharing.*
