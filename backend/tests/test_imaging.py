"""
HealthPulse AI — Medical Imaging & Segmentation Metrics Unit Tests.
"""

from backend.imaging.windowing import convert_to_hounsfield_units, apply_voi_lut_window, get_tissue_density_classification
from backend.imaging.radiology_features import calculate_cardiothoracic_ratio, estimate_nodule_volume_mm3, evaluate_pulmonary_nodule
from backend.imaging.segmentation_metrics import calculate_dice_coefficient, calculate_jaccard_index, calculate_segmentation_confusion_matrix


def test_hounsfield_unit_conversion():
    raw_pixels = [0, 1024, 2048]
    slope = 1.0
    intercept = -1024.0
    hu = convert_to_hounsfield_units(raw_pixels, slope, intercept)
    assert hu[0] == -1024.0  # Air
    assert hu[1] == 0.0      # Water
    assert hu[2] == 1024.0   # Bone


def test_voi_lut_windowing():
    hu_pixels = [-1000.0, 0.0, 40.0, 200.0, 1000.0]
    # Soft tissue window: C=40, W=400 (range -160 to +240)
    rendered = apply_voi_lut_window(hu_pixels, window_center=40.0, window_width=400.0)
    assert len(rendered) == 5
    assert rendered[0] == 0    # Below lower bound -> 0
    assert rendered[-1] == 255 # Above upper bound -> 255
    assert 120 <= rendered[2] <= 135 # Center near 128


def test_cardiothoracic_ratio():
    res = calculate_cardiothoracic_ratio(cardiac_transverse_diameter_mm=160.0, thoracic_internal_diameter_mm=300.0)
    assert res["is_cardiomegaly"] is True
    assert res["cardiothoracic_ratio"] > 0.50


def test_dice_and_jaccard():
    gt = [1, 1, 1, 0, 0, 0]
    pred = [1, 1, 0, 0, 0, 0]
    dice = calculate_dice_coefficient(gt, pred)
    jaccard = calculate_jaccard_index(gt, pred)

    assert 0.79 <= dice <= 0.81
    assert 0.65 <= jaccard <= 0.68
