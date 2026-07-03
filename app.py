import re
import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import modelscope_studio.components.pro as pro
from openai import OpenAI
# OpenaAI sdk ^__^
from config import API_KEY, MODEL, SYSTEM_PROMPT, ENDPOINT, EXAMPLES

print("Gradio app is running at: http://localhost:7860")
print("Press Ctrl+C to stop the server.")
print("API key loaded:", API_KEY is not None)
print("Model:", MODEL)

client = OpenAI(
    api_key=API_KEY,
    base_url=ENDPOINT,
)
# ---------------------------------------------
# React imports frm esm.sh
# ---------------------------------------------
react_imports = {
    "lucide-react": "https://esm.sh/lucide-react@0.525.0",
    "recharts": "https://esm.sh/recharts@3.1.0",
    "framer-motion": "https://esm.sh/framer-motion@12.23.6",
    "@tailwindcss/browser": "https://esm.sh/@tailwindcss/browser@4.1.11",
    "react": "https://esm.sh/react@^19.0.0",
    "react/": "https://esm.sh/react@^19.0.0/",
    "react-dom": "https://esm.sh/react-dom@^19.0.0",
    "react-dom/": "https://esm.sh/react-dom@^19.0.0/",
}


class GradioEvent:
    @staticmethod
    def generate_code(input_value, system_prompt_input_value, state_value):
        def get_generated_files(text):
            patterns = {
                "html": r"```html\n(.+?)\n```",
                "jsx": r"```jsx\n(.+?)\n```",
                "tsx": r"```tsx\n(.+?)\n```",
            }

            result = {}

            for key, pattern in patterns.items():
                matches = re.findall(pattern, text, re.DOTALL)
                if matches:
                    result[f"index.{key}"] = "\n".join(matches).strip()

            if not result:
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
                }
            ]

            generated_files = get_generated_files(response)

            react_code = generated_files.get("index.jsx") or generated_files.get("index.tsx")
            html_code = generated_files.get("index.html")

            if react_code:
                sandbox_value = {
                    "./index.tsx": """import Demo from './demo.tsx'
import "@tailwindcss/browser"

export default Demo
""",
                    "./demo.tsx": react_code,
                }
            else:
                sandbox_value = {
                    "./index.html": html_code,
                }

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
    def select_example(example):
        return lambda: gr.update(value=example["description"])

    @staticmethod
    def update_system_prompt(system_prompt_input_value, state_value):
        state_value["system_prompt"] = system_prompt_input_value
        return gr.update(value=state_value)

    @staticmethod
    def clear_history(state_value):
        gr.Success("History Cleared.")
        state_value["history"] = []
        return gr.update(value=state_value)


css = """
body,
.gradio-container,
#coder-artifacts {
    background: #000 !important;
    color: #ffd500 !important;
}
.ant-input,
.ant-input-textarea textarea {
    background: #000 !important;
    color: #ffd500 !important;
    border-color: #444 !important;
}
.ant-input::placeholder,
.ant-input-textarea textarea::placeholder {
    color: #888 !important;
}
.ant-typography,
.ant-card,
.ant-card-meta-title,
.ant-card-meta-description,
.ant-divider,
.ant-tabs-tab,
span,
p,
label,
div {
    color: #ffd500 !important;
}
.ant-card {
    background: #111 !important;
}
.ant-tabs-content,
.ant-tabs-tabpane {
    background: #000 !important;
}


"""


with gr.Blocks(css=css) as demo:
    state = gr.State({"system_prompt": SYSTEM_PROMPT, "history": []})

    with ms.Application(elem_id="coder-artifacts"):
        with ms.AutoLoading():
            with antd.Row(gutter=[32, 12], elem_style=dict(marginTop=20), align="stretch"):
                with antd.Col(span=24, md=8):
                    with antd.Flex(vertical=True, gap="middle", wrap=True):
                        input_box = antd.Input.Textarea(
                            size="large",
                            allow_clear=True,
                            auto_size=dict(min_rows=2, max_rows=6),
                            placeholder=(
                                "Enter your website request here. These are the main instructions for the AI to generate the site. Any context or specifications can be added below, in the System Prompt. "
                            ),
                            elem_id="input-area",
                        )

                        system_prompt_input = antd.Input.Textarea(
                            value=SYSTEM_PROMPT,
                            auto_size=dict(minRows=4, maxRows=10),
                            placeholder="Write your system prompt here. This will be used to guide the AI in generating the website code.",
                        )

                        generate_btn = antd.Button(
                            "Generate Site",
                            variant="filled",
                            color="default",
                        )

                        antd.Divider("Examples")

                        with antd.Flex(gap="small", wrap=True):
                            for example in EXAMPLES:
                                with antd.Card(
                                    elem_style=dict(flex="1 1 fit-content"),
                                    hoverable=True,
                                ) as example_card:
                                    antd.Card.Meta(
                                        title=example["title"],
                                        description=example["description"],
                                    )

                                example_card.click(
                                    fn=GradioEvent.select_example(example),
                                    outputs=[input_box],
                                )

                with antd.Col(span=24, md=16):
                    output_loading = antd.Spin(spinning=False)

                    with antd.Tabs(active_key="render") as state_tab:
                        with antd.Tabs.Item(label="Render", key="render"):
                            sandbox = pro.WebSandbox()

                        with antd.Tabs.Item(label="Code", key="code"):
                            output = antd.Input.Textarea(
                                auto_size=dict(minRows=20, maxRows=30),
                                read_only=True,
                            )

                        with antd.Tabs.Item(label="Loading", key="loading"):
                            ms.Markdown("Generating...")

                    download_content = gr.State("")

        generate_btn.click(
            fn=GradioEvent.generate_code,
            inputs=[input_box, system_prompt_input, state],
            outputs=[
                output_loading,
                state_tab,
                output,
                download_content,
                sandbox,
                state,
            ],
        )


if __name__ == "__main__":
    demo.launch()
   # if you want to share the demo publicly, set share=True in the launch method
