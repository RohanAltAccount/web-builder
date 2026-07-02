import re

import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro
from openai import OpenAI

from config import API_KEY, MODEL, SYSTEM_PROMPT, ENDPOINT


client = OpenAI(
    api_key=API_KEY,
    base_url=ENDPOINT,
)

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
    @staticmethod
    def generate_code(input_value, system_prompt_input_value, state_value):
        def get_generated_files(text):
            patterns = {
                "html": r"```html\n(.+?)\n```", "jsx": r"```jsx\n(.+?)\n```", "tsx": r"```tsx\n(.+?)\n```",
            }
            result = {}
            for key, pattern in patterns.items():
                matches = re.findall(pattern, text, re.DOTALL)
                if matches:
                    content = "\n".join(matches).strip()
                    result[f"index.{key}"] = content

            if len(result) == 0:
                result["index.html"] = text.strip()
            return result
        yield {
            output_loading: gr.update(spinning=True),
            state_tab: gr.update(active_key="loading"),
            output: gr.update(value=None),
        }
 if input_value is None:
            input_value = ""

        messages = [{"role": "system", "content": system_prompt_input_value}]
        messages += state_value["history"]
        messages.append({"role": "user", "content": input_value})
                try:
            generator = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.2,
                max_tokens=2048,
                stream=True,
            )
                    response = ""
 for chunk in generator:
                content = chunk.choices[0].delta.content
                if content:
                    response += content
                if chunk.choices[0].finish_reason == "stop":
                    break
            state_value["history"] = messages + [
                {
                    "role": "assistant",
                    "content": response,
                } ]
            generated_files = get_generated_files(response)
            react_code = generated_files.get("index.jsx") or generated_files.get("index.tsx")
            html_code = generated_files.get("index.html")

            sandbox_value = (
                {
                    "./index.tsx": """import Demo from './demo.tsx'
import "@tailwindcss/browser"

export default Demo
""",
                    "./demo.tsx": react_code,
                }
                if react_code
                else {
                    "./index.html": html_code,
                }
            )
            yield {
                output: gr.update(value=response),
                download_content: gr.update(value=react_code or html_code),
                state_tab: gr.update(active_key="render"),
                output_loading: gr.update(spinning=False),
                sandbox: gr.update(
                    template="react" if react_code else "html",
                    imports=react_imports if react_code else {},
                    value=sandbox_value,
                ),
                state: gr.update(value=state_value),
            }
        except Exception as e:
            yield {
                output_loading: gr.update(spinning=False),
                output: gr.update(value=f"Error: {e}"),
            }
    @staticmethod
    def select_example(example: dict):
        return lambda: gr.update(value=example["description"])
    @staticmethod
    def close_modal():
        return gr.update(open=False)
    @staticmethod
    def open_modal():
        return gr.update(open=True)
    @staticmethod
    def disable_btns(btns: list):
        return lambda: [gr.update(disabled=True) for _ in btns]

    @staticmethod
    def enable_btns(btns: list):
        return lambda: [gr.update(disabled=False) for _ in btns]
    @staticmethod
    def update_system_prompt(system_prompt_input_value, state_value):
        state_value["system_prompt"] = system_prompt_input_value
        return gr.update(value=state_value)
    @staticmethod
    def reset_system_prompt(state_value):
        return gr.update(value=state_value["system_prompt"])
    @staticmethod
    def render_history(state_value):
        return gr.update(value=state_value["history"])
    @staticmethod
    def clear_history(state_value):
        gr.Success("History Cleared.")
        state_value["history"] = []
        return gr.update(value=state_value)
css = """
#coder-artifacts .output-empty,
#coder-artifacts .output-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-height: 600px;
}

#coder-artifacts #output-container .ms-gr-ant-tabs-content,
#coder-artifacts .ms-gr-ant-tabs-tabpane {
    height: 100%;
}
#coder-artifacts .output-html {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 600px;
    max-height: 900px;
}

#coder-artifacts .output-html > iframe {
    flex: 1;
    width: 100%;
}
#coder-artifacts-code-drawer .output-code {
    flex: 1;
}
#coder-artifacts-code-drawer .output-code .ms-gr-ant-spin-nested-loading {
    min-height: 100%;
}
"""