import gradio as gr


def translator():
    pass


web = gr.Interface(
    fn=translator,
    inputs=gr.Audio(
        sources=["microphone"],
        type="filepath"
    ),
    outputs=[],
    title="Traductor de voz",
    description="Traductor de voz con AI a varios idiomas"
)

web.launch