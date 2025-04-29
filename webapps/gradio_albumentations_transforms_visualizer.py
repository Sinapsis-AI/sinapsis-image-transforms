# -*- coding: utf-8 -*-
import gradio as gr
from sinapsis.webapp.agent_gradio_helper import add_logo_and_title, css_header, init_image_inference
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP

CONFIG_NAME = "visualize_transforms_with_anns_from_dir.yml"
CONFIG_DIR = "packages/sinapsis_albumentations/src/sinapsis_albumentations/configs/"
DEFAULT_CONFIG = CONFIG_DIR + CONFIG_NAME
CONFIG_FILE = AGENT_CONFIG_PATH or DEFAULT_CONFIG


def create_demo_interface() -> gr.Blocks:
    """Creates and returns the Gradio Blocks demo interface for the sinapsis albumentations webapp.

    Returns:
        gr.Blocks: The Gradio Blocks object containing the entire interface.
    """
    with gr.Blocks(css=css_header()) as demo:
        add_logo_and_title("Sinapsis Albumentations Demo")
        init_image_inference(
            CONFIG_FILE,
            "",
            False,
        )
    return demo


if __name__ == "__main__":
    demo_interface = create_demo_interface()
    demo_interface.launch(share=GRADIO_SHARE_APP)
