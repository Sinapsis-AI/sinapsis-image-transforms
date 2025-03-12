FROM sinapsis:base

COPY . /app/
WORKDIR /app
RUN uv sync --frozen
RUN uv pip install sinapsis-image-transforms[webapp-gradio] --extra-index-url https://pypi.sinapsis.tech
