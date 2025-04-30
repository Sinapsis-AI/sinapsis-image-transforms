# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import Any

from albumentations import Compose as AlbCompose
from albumentations.augmentations import transforms
from albumentations.augmentations.blur import transforms as blur_transforms
from albumentations.augmentations.crops import transforms as crops_transforms
from albumentations.augmentations.geometric import resize as resize_transforms
from albumentations.augmentations.geometric import rotate as rotate_transforms
from albumentations.augmentations.geometric import transforms as geometric_transforms
from albumentations.core.bbox_utils import BboxParams
from albumentations.core.keypoints_utils import KeypointParams
from pydantic import Field
from sinapsis_core.data_containers.annotations import (
    BoundingBox,
    ImageAnnotations,
    KeyPoint,
)
from sinapsis_core.data_containers.data_packet import DataContainer, ImagePacket
from sinapsis_core.template_base import Template
from sinapsis_core.template_base.base_models import (
    OutputTypes,
    TemplateAttributes,
    TemplateAttributeType,
    UIPropertiesMetadata,
)
from sinapsis_core.template_base.dynamic_template import (
    BaseDynamicWrapperTemplate,
    WrapperEntryConfig,
)
from sinapsis_core.template_base.dynamic_template_factory import make_dynamic_template
from sinapsis_core.utils.env_var_keys import SINAPSIS_BUILD_DOCS
from sinapsis_core.utils.logging_utils import sinapsis_logger as logging


@dataclass(frozen=True)
class AlbumentationsComposeKeys:
    bboxes: str = "bboxes"
    keypoints: str = "keypoints"
    image: str = "image"
    class_labels: str = "class_labels"
    format: str = "format"


def _make_additional_doc_str() -> str:
    return f"""
    Optionally, if apply_to_annotations is given, it applies the transforms to annotations.
    The following atts can be provided as dictionaries:
        bbox_params : {BboxParams.__doc__}
        keypoints_params: {KeypointParams.__doc__}
    """


class AlbumentationAugmentationsTransforms(BaseDynamicWrapperTemplate):
    __doc__ = f"""
    Tempĺate to perform image transforms using the albumentations library
    The template takes as an input the DataContainer with images and for
    each of the ImagePacket applies the selected transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images.

    {_make_additional_doc_str()}

    Usage example:

    agent:
      name: my_test_agent
    templates:
    - template_name: InputTemplate
      class_name: InputTemplate
    - template_name: RotateWrapper
      class_name: RotateWrapper #Note that since it is a dynamic template,
      template_input: InputTemplate ## the class name is the actual class imported
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
    """

    UIProperties = UIPropertiesMetadata(category="HuggingFace", output_type=OutputTypes.IMAGE)
    WrapperEntry = WrapperEntryConfig(wrapped_object=transforms)

    class AttributesBaseModel(TemplateAttributes):
        """Static attributes for the transformations.
        apply_to_annotations (bool): Flag to determine if transformations should also be applied to annotations
        bbox_params (dict[str, Any] | None : The values of the bboxes
        keypoints_params (dict[str, Any] | None: the values of the keypoints
        additional_targets (dict[str,Any]): Any other annotations that should be transformed.
        """

        apply_to_annotations: bool = False
        bbox_params: dict[str, Any] | None = None
        keypoints_params: dict[str, Any] | None = None
        additional_targets: dict[str, str] = Field(default={"mask": "mask"})

    def __init__(self, attributes: TemplateAttributeType) -> None:
        super().__init__(attributes)
        self.transform = AlbCompose(
            self.wrapped_callable,
            bbox_params=self.attributes.bbox_params,
            keypoint_params=self.attributes.keypoints_params,
            additional_targets=self.attributes.additional_targets,
        )

    def apply_transform_to_image(self, args: dict[str, Any]) -> dict[str, Any] | None:
        """Method that calls the apply method in the transforms class
        to transform a certain image.
        Args:
            args (dict[str, Any]): args to be passed to the Compose call method
        Returns:
            (dict[str, Any] | None): Optionally returns the transformed dictionary containing image, bboxes, etc.
        """
        try:
            transformed_img: dict[str, Any] = self.transform(**args)

            return transformed_img
        except ValueError as err:
            logging.error(f"Your transforms dictionary is not set correctly: {err}")
            return None

    def extract_anns_from_image_packet(
        self, image: ImagePacket
    ) -> tuple[list[list[float]], list[list[float]], list[str]]:
        """Prior to applying the transform,
        extract the annotations from the ImagePacket and returns as lists
        Args:
            image (ImagePacket): ImagePacket to extract the annotations from
        Returns:
            (list[list[float]]): bboxes as plain lists. the Length of the list corresponds
                to the number of annotations in the original ImagePacket
            (list[list[float]]): Keypoints as plain lists. the Length of the list corresponds
                to the number of annotations in the original ImagePacket
            list[str]: label classes as a list of strings. The length of the list
                corresponds to the number of annotations in the original ImagePacket
        """
        total_bboxes = []
        total_kpts = []
        total_labels = []

        if image.annotations is not None:
            for ann in image.annotations:
                bbox = ann.bbox
                kpts = ann.keypoints
                if (
                    self.attributes.bbox_params
                    and self.attributes.bbox_params.get(AlbumentationsComposeKeys.format) == "coco"
                ) and bbox:
                    total_bboxes.append([bbox.x, bbox.y, bbox.w, bbox.h])
                elif (
                    self.attributes.bbox_params
                    and self.attributes.bbox_params.get(AlbumentationsComposeKeys.format) == "pascal_voc"
                ) and bbox:
                    total_bboxes.append([bbox.x, bbox.y, bbox.x + bbox.w, bbox.y + bbox.h])
                if (
                    self.attributes.keypoints_params
                    and self.attributes.keypoints_params.get(AlbumentationsComposeKeys.format) == "xy"
                ) and kpts:
                    total_kpts.append([kpts.x, kpts.y, kpts.score, kpts.label])
                total_labels.append(ann.label_str)
        return total_bboxes, total_kpts, total_labels

    @staticmethod
    def parse_anns(transformed_results: dict[str, Any], annotations: list[ImageAnnotations]) -> list[ImageAnnotations]:
        """Inserts the new annotations into the ImagePacket annotations field
        Args:
            transformed_results (dict[str, Any]): the dictionary returned by Compose
                with the new annotations.
            annotations (list[ImageAnnotations]): list of original anns to be overriden
        Returns:
            (list[ImageAnnotations]): New annotations corresponding to the transformed image
        """
        for ann in annotations:
            for bbox in transformed_results[AlbumentationsComposeKeys.bboxes]:
                ann.bbox = BoundingBox(*bbox)
            for kpt in transformed_results[AlbumentationsComposeKeys.keypoints]:
                ann.keypoint = KeyPoint(*kpt)
            for label in transformed_results[AlbumentationsComposeKeys.class_labels]:
                ann.label_str = label
                ann.label = label
        return annotations

    def execute(self, container: DataContainer) -> DataContainer:
        """
        This template receives a data container, applies the transforms for
        each of the images and return the modified / updated container

        Args:
            container (DataContainer): container with images to be transformed
        Returns:
            (DataContainer): Modified DataContainer
        """
        if not container.images:
            return container

        for image in container.images:
            dict_for_args = {AlbumentationsComposeKeys.image: image.content}

            if self.attributes.apply_to_annotations:
                bbox, kpts, labels = self.extract_anns_from_image_packet(image)
                dict_for_args.update(
                    {
                        AlbumentationsComposeKeys.bboxes: bbox,
                        AlbumentationsComposeKeys.keypoints: kpts,
                        AlbumentationsComposeKeys.class_labels: labels,
                    }
                )

            transformed_results = self.apply_transform_to_image(dict_for_args)

            if transformed_results:
                image.content = transformed_results[AlbumentationsComposeKeys.image]

                if self.attributes.apply_to_annotations:
                    image.annotations = self.parse_anns(transformed_results, [ImageAnnotations()])
        return container


class AlbumentationAugmentationsTransformsBlur(AlbumentationAugmentationsTransforms):
    __doc__ = f"""
    Class for albumentations transforms, ``albumentations.transforms.blur.transforms`` module.
    The template takes as an input the DataContainer with images and for each of the
    ImagePacket applies the selected transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images

        {_make_additional_doc_str()}

    """
    WrapperEntry = WrapperEntryConfig(wrapped_object=blur_transforms)


class AlbumentationAugmentationsTransformsCrops(AlbumentationAugmentationsTransforms):
    __doc__ = f"""
    Class for albumentations transforms using ``albumentations.transforms.crops.transforms``
    module. The template takes as an input the DataContainer with images and for each of the
    ImagePacket applies the selected transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images

         {_make_additional_doc_str()}

    """

    WrapperEntry = WrapperEntryConfig(wrapped_object=crops_transforms)


class AlbumentationAugmentationsTransformsGeometric(AlbumentationAugmentationsTransforms):
    __doc__ = f"""
    Class for albumentations transforms, using ``albumentations.transforms.geometric.transforms``
    module. The template takes as an input the DataContainer with images and for each of the
    ImagePacket applies the selected transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images

        {_make_additional_doc_str()}

    """

    WrapperEntry = WrapperEntryConfig(wrapped_object=geometric_transforms)


class AlbumentationAugmentationsTransformsResize(AlbumentationAugmentationsTransforms):
    __doc__ = f"""
    Class for albumentations resize transforms, using ``albumentations.transforms.geometric.resize``.
    The template takes as an input the DataContainer with images and for each of the
    ImagePacket applies the selected resize transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images

    {_make_additional_doc_str()}
    """

    WrapperEntry = WrapperEntryConfig(wrapped_object=resize_transforms)


class AlbumentationAugmentationsTransformsRotate(AlbumentationAugmentationsTransforms):
    __doc__ = f"""
    Class for albumentations rotate transforms, using the ``albumentations.transforms.geometric.rotate``.
    The template takes as an input the DataContainer with images and for each of the
    ImagePacket applies the selected rotate transform.

    If rewrite_image_packet is set to True, then the ith ImagePacket is
    replaced with the new image, otherwise the new image is appended to
    containers.images

    {_make_additional_doc_str()}
    """

    WrapperEntry = WrapperEntryConfig(wrapped_object=rotate_transforms)


def __getattr__(name: str) -> Template:
    """
    Only create a template if it's imported, this avoids creating all the base models for all templates
    and potential import errors due to not available packages.
    """
    if name in AlbumentationAugmentationsTransforms.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransforms)
    if name in AlbumentationAugmentationsTransformsBlur.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransformsBlur)

    if name in AlbumentationAugmentationsTransformsCrops.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransformsCrops)

    if name in AlbumentationAugmentationsTransformsGeometric.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransformsGeometric)

    if name in AlbumentationAugmentationsTransformsResize.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransformsResize)

    if name in AlbumentationAugmentationsTransformsRotate.WrapperEntry.module_att_names:
        return make_dynamic_template(name, AlbumentationAugmentationsTransformsRotate)

    raise AttributeError(f"template `{name}` not found in {__name__}")


__all__ = (
    AlbumentationAugmentationsTransforms.WrapperEntry.module_att_names
    + AlbumentationAugmentationsTransformsBlur.WrapperEntry.module_att_names
    + AlbumentationAugmentationsTransformsCrops.WrapperEntry.module_att_names
    + AlbumentationAugmentationsTransformsGeometric.WrapperEntry.module_att_names
    + AlbumentationAugmentationsTransformsResize.WrapperEntry.module_att_names
    + AlbumentationAugmentationsTransformsRotate.WrapperEntry.module_att_names
)


if SINAPSIS_BUILD_DOCS:
    dynamic_templates = [__getattr__(template_name) for template_name in __all__]

    for template in dynamic_templates:
        globals()[template.__name__] = template
        del template
