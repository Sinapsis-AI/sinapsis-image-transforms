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
<a href="#features"> 🚀 Features</a> •
<a href="#webapp"> 🌐 Webapp</a> •
<a href="#documentation">📙 Documentation</a> •
<a href="#license"> 🔍 License </a>
</p>

The `sinapsis-image-transforms` module provides templates for applying various image transformations with [**Albumentations**](https://albumentations.ai/docs/).


<h2 id="installation"> 🐍  Installation </h2>

Install using your package manager of choice. We encourage the use of <code>uv</code>

Example with <code>uv</code>:

```bash
  uv pip install sinapsis-image-transforms --extra-index-url https://pypi.sinapsis.tech
```
 or with raw <code>pip</code>:
```bash
  pip install sinapsis-image-transforms --extra-index-url https://pypi.sinapsis.tech
```

<h2 id="features">🚀 Features</h2>

<h3> Templates Supported</h3>

The **Sinapsis Image Transforms** module provides a collection of templates for applying image transformations using **Albumentations**. These templates allow users to apply a wide range of augmentations, from simple operations like flipping and resizing to more advanced transformations such as elastic distortions and geometric warping.

<h4>🌍 General Attributes</h4>

> [!NOTE]
> All templates share the following attributes:
> - **`apply_to_annotations` (bool, optional)**: Determines whether transformations should also be applied to annotations like bounding boxes, keypoints, and masks. Defaults to `False`.
> - **`bbox_params` (dict[str, Any], optional)**: Configuration for transforming bounding boxes, following Albumentations' `BboxParams` format. Defaults to `None`.
> - **`keypoints_params` (dict[str, Any], optional)**: Defines keypoint transformation settings using Albumentations' `KeypointParams`. Defaults to `None`.
> - **`additional_targets` (dict[str, Any], optional)**: Specifies extra annotation types (e.g., segmentation masks) to be transformed alongside the image. Defaults to `{"mask": "mask"}`.
>
> Additional transformation-specific attributes can be dynamically assigned through the class initialization dictionary (`*_init` attributes). These attributes correspond directly to the arguments used in Albumentations.

> [!TIP]
> Use CLI command ``` sinapsis info --all-template-names``` to show a list with all the available Template names installed with Sinapsis Image Transforms.

> [!TIP]
> Use CLI command ```sinapsis info --example-template-config TEMPLATE_NAME``` to produce an example Agent config for the Template specified in ***TEMPLATE_NAME***.

For example, for ***RotateWrapper*** use ```sinapsis info --example-template-config RotateWrapper``` to produce the following example config:

```yaml
agent:
  name: my_test_agent
templates:
- template_name: InputTemplate
  class_name: InputTemplate
- template_name: RotateWrapper
  class_name: RotateWrapper
  template_input: InputTemplate
  attributes:
    apply_to_annotations: false
    bbox_params: null
    keypoints_params: null
    additional_targets:
      mask: mask
    rotate_init:
      limit: [-45, 45]
      interpolation: 1
      border_mode: 4
      value: [0, 0, 0]
      mask_value: null
      rotate_method: "largest_box"
      crop_border: false
      fill_value: 0
      mask_fill_value: 0
      deterministic: true
      p: 1.0
```

<details>
<summary><strong><span style="font-size: 1.25em;">📚 Example Usage</span></strong></summary>

The following example demonstrates how to use **Sinapsis Image Transforms** to apply multiple image augmentations. This setup loads a dataset of images, applies **horizontal flipping** and **elastic transformation**, and saves the results. Below is the full YAML configuration, followed by a breakdown of each component.
<details>
<summary ><strong><span style="font-size: 1.4em;">Config</span></strong></summary>

```yaml
agent:
  name: transforms_agent

templates:
- template_name: InputTemplate
  class_name: InputTemplate
  attributes: {}

- template_name: FolderImageDatasetCV2
  class_name: FolderImageDatasetCV2
  template_input: InputTemplate
  attributes:
    data_dir: my_dataset

- template_name: HorizontalFlip
  class_name: HorizontalFlipWrapper
  template_input: FolderImageDatasetCV2
  attributes:
    horizontalflip_init:
      p: 1.0

- template_name: ElasticTransform
  class_name: ElasticTransformWrapper
  template_input: HorizontalFlip
  attributes:
    elastictransform_init:
      mask_value: 150
      p: 1.0
      alpha: 100
      sigma: 50

- template_name: ImageSaver
  class_name: ImageSaver
  template_input: ElasticTransform
  attributes:
    save_dir: results
    extension: jpg
```
</details>
This configuration defines an **agent** and a sequence of **templates** to apply image transformations.

> [!IMPORTANT]
>Attributes specified under the `*_init` keys (e.g., `elastictransform_init`, `horizontalflip_init`) correspond directly to the Albumentations transformation parameters. Ensure that values are assigned correctly according to the official [Albumentations documentation](https://albumentations.ai/docs/), as they affect the behavior and performance of each transformation.
>
> The FolderImageDataserCV2 and ImageSaver correspond to [sinapsis-data-readers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_readers) and [sinapsis-data-writers](https://github.com/Sinapsis-AI/sinapsis-data-tools/tree/main/packages/sinapsis_data_writers). If you want to use the example, please make sure you install the packages.
>

To run the config, use the CLI:
```bash
sinapsis run name_of_config.yml
```

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

**IMPORTANT** This docker image depends on the sinapsis-nvidia:base image. Please refer to the official [sinapsis](https://github.com/Sinapsis-ai/sinapsis?tab=readme-ov-file#docker) instructions to Build with Docker.

1. **Build the sinapsis-image-transforms image**:
```bash
docker compose -f docker/compose.yaml build
```

2. **Start the app container**:
```bash
docker compose -f docker/compose_apps.yaml up sinapsis-image-transforms-gradio -d
```
3. **Check the status**:
```bash
docker logs -f sinapsis-image-transforms-inference-gradio
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
uv pip install sinapsis-image-transforms[webapp-gradio] --extra-index-url https://pypi.sinapsis.tech
```

3. **Activate the environment**:
```bash
source .venv/bin/activate
```
4. **Run the webapp**:
```bash
python webapps/gradio_image_transform_visualizer.py
```
5. **The terminal will display the URL to access the webapp, e.g.**:

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



