import re

import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro
from openai import OpenAI
from config import API_KEY, MODEL, SYSTEM_PROMPT, ENDPOINT, EXAMPLES, DEFAULT_LOCALE, DEFAULT_THEME

client = OpenAI(api_key=API_KEY, base_url=ENDPOINT)



# ---------------------------------------------
# retrieve react imports frm esm.sh
# ---------------------------------------------
react_imports = {
    "lucide-react": "https://esm.sh/lucide-react@0.525.0",
    "recharts": "https://esm.sh/recharts@3.1.0",
    "framer-motion": "https://esm.sh/framer-motion@12.23.6",
    "matter-js": "https://esm.sh/matter-js@0.20.0",
    "p5": "https://esm.sh/p5@2.0.3",
    "konva": "https://esm.sh/konva@9.3.22",
    "react-konva": "https://esm.sh/react-konva@19.0.7",
    "three": "https://esm.sh/three@0.178.0",
    "@react-three/fiber": "https://esm.sh/@react-three/fiber@9.2.0",
    "@react-three/drei": "https://esm.sh/@react-three/drei@10.5.2",
    "@tailwindcss/browser": "https://esm.sh/@tailwindcss/browser@4.1.11",
    "react": "https://esm.sh/react@^19.0.0",
    "react/": "https://esm.sh/react@^19.0.0/",
    "react-dom": "https://esm.sh/react-dom@^19.0.0",
    "react-dom/": "https://esm.sh/react-dom@^19.0.0/"
}


#---------------------------------------------
# create gradio event class
#---------------------------------------------
class GradioEvent:
    @StaticMethod
    def generate_code(input_value, system_prompt_input_value, state_value):
        def get_generated_files(text):
            patterns = { 'html': r'```html\n(.+?)\n```', 'jsx': r'```jsx\n(.+?)\n```',    'tsx': r'```tsx\n(.+?)\n```', }
            result = {}
            for key, pattern in patterns.items():
                matches = re.findall(pattern, text, re.DOTALL)
                if matches:
                    content = '\n'.join(matches).strip()
                    result[f'index.{key}'] = content
if len(result) == 0:
                result['index.html'] = text.strip()
            return result
            yield {
                output_loading: gr.update(spinning =True),
                state_tab: gr.update(active_key ="loading"),
                output: gr.update(value=none),

            }

            if input_value is None:
                input_value = ""
                messages = [{role: "system", content: system_prompt_input_value}] + state_value["history"]
                
                messages.append({'role': "user", 'content': input_value})
                generator = client.chat.completions.create(
                    model=MODEL, messages=messages, temperature=0.2, max_tokens=2048, stream=True
