<h1 align="center">
<br>
<a href="https://sinapsis.tech/">
  <img
    src="https://github.com/Sinapsis-AI/brand-resources/blob/main/sinapsis_logo/4x/logo.png?raw=true"
    alt="" width="300">
</a><br>
Sinapsis Image Transforms
<br>
</h1>

<h4 align="center">Templates for applying image transformations using Albumentations.</h4>

<p align="center">
<a href="#installation">🐍  Installation</a> •
<a href="#packages">📦 Packages</a> •
<a href="#webapp"> 🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license"> 🔍 License </a>
</p>

This mono repo contains the `sinapsis-albumentations` package, featuring an extensive collection of templates for image transformation supported by the [**Albumentations**](https://albumentations.ai/docs/) library.

<h2 id="installation"> 🐍  Installation </h2>

   

Install using your package manager of choice. We encourage the use of <code>uv</code>

Example with <code>uv</code>:

```bash
  uv pip install sinapsis-albumentations --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-albumentations --extra-index-url https://pypi.sinapsis.tech
```



<h2 id="packages">📦 Packages</h2>

<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">Sinapsis albumentations</span></strong></summary>

The **Sinapsis Albumentations** package provides a collection of templates for applying image transformations using **Albumentations**. 

For specific instructions and further details, see the [sinapsis-albumentations README](https://github.com/sinapsis-ai/sinapsis-image-transforms/blob/main/packages/sinapsis_albumentations/README.md).



</details>




<h2 id="webapp">🌐 Webapp</h2>

The webapp provides an interactive interface to visualize and experiment with image transformations in real time.

> [!IMPORTANT]
> To run the app you first need to clone this repository:

```bash
git clone git@github.com:Sinapsis-ai/sinapsis-image-transforms.git
cd sinapsis-image-transforms
```
> [!NOTE]
> If you'd like to enable external app sharing in Gradio, `export GRADIO_SHARE_APP=True`
<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">🐳 Docker</span></strong></summary>



1. **Build the sinapsis-image-transforms image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up sinapsis-albumentations-gradio -d
```
3. **Check the status**:
```bash
docker logs -f sinapsis-albumentations-inference-gradio
```
3. The logs will display the URL to access the webapp, e.g.:

NOTE: The url can be different, check the output of logs
```bash
Running on local URL:  http://127.0.0.1:7860
```
4. To stop the app:
```bash
docker compose -f docker/compose_apps.yaml down
```

</details>


<details>
<summary id="uv"><strong><span style="font-size: 1.4em;">💻 UV</span></strong></summary>

To run the webapp using the <code>uv</code> package manager, please:

1. **Create the virtual environment and sync the dependencies**:
```bash
uv sync --frozen
```
2. **Install the wheel**:
```bash
uv pip install sinapsis-image-transforms[all] --extra-index-url https://pypi.sinapsis.tech
```

3. **Run the webapp**:
```bash
uv run webapps/gradio_albumentations_transforms_visualizer.py
```
4. **The terminal will display the URL to access the webapp, e.g.**:

NOTE: The url can be different, check the output of the terminal
```bash
Running on local URL:  http://127.0.0.1:7860
```

</details>

<h2 id="documentation">📙 Documentation</h2>

Documentation for this and other sinapsis packages is available on the [sinapsis website](https://docs.sinapsis.tech/docs)

Tutorials for different projects within sinapsis are available at [sinapsis tutorials page](https://docs.sinapsis.tech/tutorials)


<h2 id="license">🔍 License</h2>

This project is licensed under the AGPLv3 license, which encourages open collaboration and sharing. For more details, please refer to the [LICENSE](LICENSE) file.

For commercial use, please refer to our [official Sinapsis website](https://sinapsis.tech) for information on obtaining a commercial license.



