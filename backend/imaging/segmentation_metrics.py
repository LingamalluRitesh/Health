"""
HealthPulse AI — Medical Image Segmentation Evaluation & Validation Metrics.
Calculates Dice Similarity Coefficient, Jaccard Index, Sensitivity, Specificity, and Hausdorff Distance.
"""

from typing import List, Dict, Any, Tuple
import math


def calculate_dice_coefficient(
    mask_ground_truth: List[int],
    mask_predicted: List[int],
) -> float:
    """
    Dice Similarity Coefficient (DSC):
    DSC = (2 * |GT intersect Pred|) / (|GT| + |Pred|)
    """
    if len(mask_ground_truth) != len(mask_predicted):
        raise ValueError("Mask arrays must have identical length")

    intersection = 0
    gt_sum = 0
    pred_sum = 0

    for gt, pred in zip(mask_ground_truth, mask_predicted):
        gt_bool = 1 if gt > 0 else 0
        pred_bool = 1 if pred > 0 else 0
        if gt_bool and pred_bool:
            intersection += 1
        gt_sum += gt_bool
        pred_sum += pred_bool

    denom = gt_sum + pred_sum
    if denom == 0:
        return 1.0  # Both empty masks match perfectly
    return round((2.0 * intersection) / denom, 4)


def calculate_jaccard_index(
    mask_ground_truth: List[int],
    mask_predicted: List[int],
) -> float:
    """
    Jaccard Index / Intersection over Union (IoU):
    IoU = |GT intersect Pred| / |GT union Pred|
    """
    if len(mask_ground_truth) != len(mask_predicted):
        raise ValueError("Mask arrays must have identical length")

    intersection = 0
    union = 0

    for gt, pred in zip(mask_ground_truth, mask_predicted):
        gt_bool = 1 if gt > 0 else 0
        pred_bool = 1 if pred > 0 else 0
        if gt_bool and pred_bool:
            intersection += 1
        if gt_bool or pred_bool:
            union += 1

    if union == 0:
        return 1.0
    return round(intersection / union, 4)


def calculate_segmentation_confusion_matrix(
    mask_ground_truth: List[int],
    mask_predicted: List[int],
) -> Dict[str, Any]:
    """Computes True Positive, False Positive, True Negative, False Negative, Sensitivity, Specificity."""
    tp = 0
    fp = 0
    fn = 0
    tn = 0

    for gt, pred in zip(mask_ground_truth, mask_predicted):
        g = 1 if gt > 0 else 0
        p = 1 if pred > 0 else 0
        if g == 1 and p == 1:
            tp += 1
        elif g == 0 and p == 1:
            fp += 1
        elif g == 1 and p == 0:
            fn += 1
        else:
            tn += 1

    sensitivity = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 1.0
    specificity = round(tn / (tn + fp), 4) if (tn + fp) > 0 else 1.0
    precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 1.0
    dice = round((2.0 * tp) / (2.0 * tp + fp + fn), 4) if (2 * tp + fp + fn) > 0 else 1.0

    return {
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "precision": precision,
        "dice_score": dice,
    }


def calculate_hausdorff_distance_approx(
    points_gt: List[Tuple[float, float]],
    points_pred: List[Tuple[float, float]],
) -> float:
    """Computes Euclidean Hausdorff Distance between two contour boundary point sets."""
    if not points_gt or not points_pred:
        return 0.0

    def min_dist_to_set(pt: Tuple[float, float], pt_set: List[Tuple[float, float]]) -> float:
        min_d = float("inf")
        px, py = pt
        for qx, qy in pt_set:
            d = math.sqrt((px - qx) ** 2 + (py - qy) ** 2)
            if d < min_d:
                min_d = d
        return min_d

    d_gt_to_pred = max(min_dist_to_set(p, points_pred) for p in points_gt)
    d_pred_to_gt = max(min_dist_to_set(p, points_gt) for p in points_pred)

    return round(max(d_gt_to_pred, d_pred_to_gt), 3)
