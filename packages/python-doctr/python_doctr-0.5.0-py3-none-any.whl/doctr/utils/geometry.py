# Copyright (C) 2021, Mindee.

# This program is licensed under the Apache License version 2.
# See LICENSE or go to <https://www.apache.org/licenses/LICENSE-2.0.txt> for full license details.

from math import ceil
from typing import List, Tuple, Union

import cv2
import numpy as np

from .common_types import BoundingBox, Polygon4P

__all__ = ['bbox_to_polygon', 'polygon_to_bbox', 'resolve_enclosing_bbox', 'resolve_enclosing_rbbox',
           'rotate_boxes', 'rotate_abs_boxes', 'compute_expanded_shape', 'rotate_image', 'estimate_page_angle',
           'convert_to_relative_coords']


def bbox_to_polygon(bbox: BoundingBox) -> Polygon4P:
    return bbox[0], (bbox[1][0], bbox[0][1]), (bbox[0][0], bbox[1][1]), bbox[1]


def polygon_to_bbox(polygon: Polygon4P) -> BoundingBox:
    x, y = zip(*polygon)
    return (min(x), min(y)), (max(x), max(y))


def resolve_enclosing_bbox(bboxes: Union[List[BoundingBox], np.ndarray]) -> Union[BoundingBox, np.ndarray]:
    """Compute enclosing bbox either from:

    - an array of boxes: (*, 5), where boxes have this shape:
    (xmin, ymin, xmax, ymax, score)

    - a list of BoundingBox

    Return a (1, 5) array (enclosing boxarray), or a BoundingBox
    """
    if isinstance(bboxes, np.ndarray):
        xmin, ymin, xmax, ymax, score = np.split(bboxes, 5, axis=1)
        return np.array([xmin.min(), ymin.min(), xmax.max(), ymax.max(), score.mean()])
    else:
        x, y = zip(*[point for box in bboxes for point in box])
        return (min(x), min(y)), (max(x), max(y))


def resolve_enclosing_rbbox(rbboxes: List[np.ndarray], intermed_size: int = 1024) -> np.ndarray:
    cloud = np.concatenate(rbboxes, axis=0)
    # Convert to absolute for minAreaRect
    cloud *= intermed_size
    rect = cv2.minAreaRect(cloud.astype(np.int32))
    return cv2.boxPoints(rect) / intermed_size


def rotate_abs_points(points: np.ndarray, angle: float = 0.) -> np.ndarray:
    """Rotate points counter-clockwise.
    Points: array of size (N, 2)
    """

    angle_rad = angle * np.pi / 180.  # compute radian angle for np functions
    rotation_mat = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ], dtype=points.dtype)
    return np.matmul(points, rotation_mat.T)


def compute_expanded_shape(img_shape: Tuple[int, int], angle: float) -> Tuple[int, int]:
    """Compute the shape of an expanded rotated image

    Args:
        img_shape: the height and width of the image
        angle: angle between -90 and +90 degrees

    Returns:
        the height and width of the rotated image
    """

    points = np.array([
        [img_shape[1] / 2, img_shape[0] / 2],
        [-img_shape[1] / 2, img_shape[0] / 2],
    ])

    rotated_points = rotate_abs_points(points, angle)

    wh_shape = 2 * np.abs(rotated_points).max(axis=0)
    return wh_shape[1], wh_shape[0]


def rotate_abs_boxes(boxes: np.ndarray, angle: float, img_shape: Tuple[int, int], expand: bool = True) -> np.ndarray:
    """Rotate a batch of straight bounding boxes (xmin, ymin, xmax, ymax)  or polygons (N, 4, 2)
        by an angle around the image center.

    Args:
        boxes: (N, 4) or (N, 4, 2) array of ABSOLUTE coordinate boxes
        angle: angle between -90 and +90 degrees
        img_shape: the height and width of the image
        expand: whether the image should be padded to avoid information loss

    Returns:
        A batch of rotated boxes (N, 4, 2) or a batch of straight bounding boxes
    """

    # Get box corners
    if boxes.ndim == 2:
        box_corners = np.stack(
            [
                boxes[:, [0, 1]],
                boxes[:, [2, 1]],
                boxes[:, [2, 3]],
                boxes[:, [0, 3]],
            ],
            axis=1
        )
    else:
        box_corners = boxes
    img_corners = np.array([[0, 0], [0, img_shape[0]], [*img_shape[::-1]], [img_shape[1], 0]], dtype=boxes.dtype)

    stacked_points = np.concatenate((img_corners[None, ...], box_corners), axis=0)
    # Y-axis is inverted by conversion
    stacked_rel_points = np.stack(
        (stacked_points[..., 0] - img_shape[1] / 2, img_shape[0] / 2 - stacked_points[..., 1]),
        axis=-1
    )

    # Rotate them around image center, shape (N+1, 4, 2)
    rot_points = rotate_abs_points(stacked_rel_points.reshape((-1, 2)), angle).reshape(-1, 4, 2)
    img_rot_corners, box_rot_corners = rot_points[0], rot_points[1:]

    # Expand the image to fit all the original info
    if expand:
        new_corners = np.abs(img_rot_corners).max(axis=0)
        box_rot_corners[..., 0] += new_corners[0]
        box_rot_corners[..., 1] = new_corners[1] - box_rot_corners[..., 1]
    else:
        box_rot_corners[..., 0] += img_shape[1] / 2
        box_rot_corners[..., 1] = img_shape[0] / 2 - box_rot_corners[..., 1]

    return box_rot_corners


def rotate_boxes(
    loc_preds: np.ndarray,
    angle: float,
    orig_shape: Tuple[int, int],
    min_angle: float = 1.,
) -> np.ndarray:
    """Rotate a batch of straight bounding boxes (xmin, ymin, xmax, ymax, c) or rotated bounding boxes
    (4, 2) of an angle, if angle > min_angle, around the center of the page.
    If target_shape is specified, the boxes are remapped to the target shape after the rotation. This
    is done to remove the padding that is created by rotate_page(expand=True)

    Args:
        loc_preds: (N, 5) or (N, 4, 2) array of RELATIVE boxes
        angle: angle between -90 and +90 degrees
        orig_shape: shape of the origin image
        min_angle: minimum angle to rotate boxes

    Returns:
        A batch of rotated boxes (N, 4, 2): or a batch of straight bounding boxes
    """

    # Change format of the boxes to rotated boxes
    _boxes = loc_preds.copy()
    if _boxes.ndim == 2:
        _boxes = np.stack(
            [
                _boxes[:, [0, 1]],
                _boxes[:, [2, 1]],
                _boxes[:, [2, 3]],
                _boxes[:, [0, 3]],
            ],
            axis=1
        )
    # If small angle, return boxes (no rotation)
    if abs(angle) < min_angle or abs(angle) > 90 - min_angle:
        return _boxes
    # Compute rotation matrix
    angle_rad = angle * np.pi / 180.  # compute radian angle for np functions
    rotation_mat = np.array([
        [np.cos(angle_rad), -np.sin(angle_rad)],
        [np.sin(angle_rad), np.cos(angle_rad)]
    ], dtype=_boxes.dtype)
    # Rotate absolute points
    points = np.stack((_boxes[:, :, 0] * orig_shape[1], _boxes[:, :, 1] * orig_shape[0]), axis=-1)
    image_center = (orig_shape[1] / 2, orig_shape[0] / 2)
    rotated_points = image_center + np.matmul(points - image_center, rotation_mat)
    rotated_boxes = np.stack(
        (rotated_points[:, :, 0] / orig_shape[1], rotated_points[:, :, 1] / orig_shape[0]), axis=-1
    )
    return rotated_boxes


def rotate_image(
    image: np.ndarray,
    angle: float,
    expand: bool = False,
    preserve_origin_shape: bool = False,
) -> np.ndarray:
    """Rotate an image counterclockwise by an given angle.

    Args:
        image: numpy tensor to rotate
        angle: rotation angle in degrees, between -90 and +90
        expand: whether the image should be padded before the rotation
        preserve_origin_shape: if expand is set to True, resizes the final output to the original image size

    Returns:
        Rotated array, padded by 0 by default.
    """

    # Compute the expanded padding
    if expand:
        exp_shape = compute_expanded_shape(image.shape[:-1], angle)
        h_pad, w_pad = int(max(0, ceil(exp_shape[0] - image.shape[0]))), int(
            max(0, ceil(exp_shape[1] - image.shape[1])))
        exp_img = np.pad(image, ((h_pad // 2, h_pad - h_pad // 2), (w_pad // 2, w_pad - w_pad // 2), (0, 0)))
    else:
        exp_img = image

    height, width = exp_img.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1.0)
    rot_img = cv2.warpAffine(exp_img, rot_mat, (width, height))
    if expand:
        # Pad to get the same aspect ratio
        if (image.shape[0] / image.shape[1]) != (rot_img.shape[0] / rot_img.shape[1]):
            # Pad width
            if (rot_img.shape[0] / rot_img.shape[1]) > (image.shape[0] / image.shape[1]):
                h_pad, w_pad = 0, int(rot_img.shape[0] * image.shape[1] / image.shape[0] - rot_img.shape[1])
            # Pad height
            else:
                h_pad, w_pad = int(rot_img.shape[1] * image.shape[0] / image.shape[1] - rot_img.shape[0]), 0
            rot_img = np.pad(rot_img, ((h_pad // 2, h_pad - h_pad // 2), (w_pad // 2, w_pad - w_pad // 2), (0, 0)))
        if preserve_origin_shape:
            # rescale
            rot_img = cv2.resize(rot_img, image.shape[:-1][::-1], interpolation=cv2.INTER_LINEAR)

    return rot_img


def estimate_page_angle(polys: np.ndarray) -> float:
    """Takes a batch of rotated previously ORIENTED polys (N, 4, 2) (rectified by the classifier) and return the
    estimated angle ccw in degrees
    """
    return np.median(np.arctan(
        (polys[:, 0, 1] - polys[:, 1, 1]) /  # Y axis from top to bottom!
        (polys[:, 1, 0] - polys[:, 0, 0])
    )) * 180 / np.pi


def convert_to_relative_coords(geoms: np.ndarray, img_shape: Tuple[int, int]) -> np.ndarray:
    """Convert a geometry to relative coordinates

    Args:
        geoms: a set of polygons of shape (N, 4, 2) or of straight boxes of shape (N, 4)
        img_shape: the height and width of the image

    Returns:
        the updated geometry
    """

    # Polygon
    if geoms.ndim == 3 and geoms.shape[1:] == (4, 2):
        polygons = np.empty(geoms.shape, dtype=np.float32)
        polygons[..., 0] = geoms[..., 0] / img_shape[1]
        polygons[..., 1] = geoms[..., 1] / img_shape[0]
        return polygons.clip(0, 1)
    if geoms.ndim == 2 and geoms.shape[1] == 4:
        boxes = np.empty(geoms.shape, dtype=np.float32)
        boxes[:, ::2] = geoms[:, ::2] / img_shape[1]
        boxes[:, 1::2] = geoms[:, 1::2] / img_shape[0]
        return boxes.clip(0, 1)

    raise ValueError(f"invalid format for arg `geoms`: {geoms.shape}")
