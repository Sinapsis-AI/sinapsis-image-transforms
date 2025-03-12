# -*- coding: utf-8 -*-
import gradio as gr
from sinapsis.webapp.agent_gradio_helper import init_image_inference, css_header, add_logo_and_title
from sinapsis_core.utils.env_var_keys import AGENT_CONFIG_PATH, GRADIO_SHARE_APP

DEFAULT_CONFIG = "src/sinapsis_image_transforms/configs/visualize_transforms_with_anns_from_dir.yml"
CONFIG_FILE = AGENT_CONFIG_PATH or DEFAULT_CONFIG



def demo()-> gr.Blocks:
    with gr.Blocks(css=css_header()) as demo:
        add_logo_and_title("Sinapsis Albumentations Demo")
        init_image_inference(CONFIG_FILE, "", False, )
    return demo


if __name__ == "__main__":

    live_interface = demo()
    live_interface.launch(share=GRADIO_SHARE_APP)

