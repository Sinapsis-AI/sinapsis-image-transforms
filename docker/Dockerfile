FROM sinapsis:base

COPY . /app/
WORKDIR /app
RUN uv sync --frozen && uv pip install sinapsis-image-transforms[all] --extra-index-url https://pypi.sinapsis.tech