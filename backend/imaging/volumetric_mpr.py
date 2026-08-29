"""
HealthPulse AI — 3D Volumetric Reconstruction & Multi-Planar Reformation (MPR).
Constructs 3D voxel volume from 2D DICOM series and slices along Axial, Coronal, and Sagittal planes.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
from backend.imaging.dicom_parser import DICOMDataset


class PlaneType(str, Enum):
    AXIAL = "axial"
    CORONAL = "coronal"
    SAGITTAL = "sagittal"


@dataclass
class MPRSlice:
    plane: PlaneType
    slice_index: int
    rows: int
    columns: int
    pixel_spacing: Tuple[float, float]
    pixels_hu: List[float]


class VolumetricSeries:
    """Represents a full 3D CT/MRI volumetric array (Z, Y, X)."""

    def __init__(self, slices: List[DICOMDataset]):
        if not slices:
            raise ValueError("VolumetricSeries requires at least one DICOM slice")

        # Sort slices along Z-axis by SliceLocation or InstanceNumber
        self.slices = sorted(slices, key=lambda s: s.slice_location)
        self.num_slices = len(self.slices)
        self.rows = self.slices[0].rows
        self.cols = self.slices[0].columns
        self.row_spacing, self.col_spacing = self.slices[0].pixel_spacing
        self.slice_thickness = self.slices[0].slice_thickness

        # Build 3D array of HU values: [Z, Y, X]
        self._volume: List[List[List[float]]] = []
        for s in self.slices:
            raw = s.pixel_data or [0] * (s.rows * s.columns)
            slope = s.rescale_slope
            intercept = s.rescale_intercept
            
            slice_2d: List[List[float]] = []
            for r in range(s.rows):
                row_vals: List[float] = []
                start_idx = r * s.columns
                for c in range(s.columns):
                    val = (raw[start_idx + c] * slope) + intercept
                    row_vals.append(val)
                slice_2d.append(row_vals)
            self._volume.append(slice_2d)

    def get_voxel(self, z: int, y: int, x: int) -> float:
        if 0 <= z < self.num_slices and 0 <= y < self.rows and 0 <= x < self.cols:
            return self._volume[z][y][x]
        return -1000.0  # Air default


class MultiPlanarReconstructor:
    """Generates orthogonal 2D slices from 3D volumetric array."""

    def __init__(self, series: VolumetricSeries):
        self.series = series

    def extract_axial(self, z_index: int) -> MPRSlice:
        """Extracts standard transaxial slice (Y x X)."""
        z = max(0, min(self.series.num_slices - 1, z_index))
        flat_hu: List[float] = []
        for r in range(self.series.rows):
            for c in range(self.series.cols):
                flat_hu.append(self.series.get_voxel(z, r, c))

        return MPRSlice(
            plane=PlaneType.AXIAL,
            slice_index=z,
            rows=self.series.rows,
            columns=self.series.cols,
            pixel_spacing=(self.series.row_spacing, self.series.col_spacing),
            pixels_hu=flat_hu,
        )

    def extract_coronal(self, y_index: int) -> MPRSlice:
        """Extracts coronal plane slice (Z x X) (Frontal view)."""
        y = max(0, min(self.series.rows - 1, y_index))
        out_rows = self.series.num_slices
        out_cols = self.series.cols
        flat_hu: List[float] = []

        # From top to bottom (Z descending or ascending)
        for z in range(self.series.num_slices - 1, -1, -1):
            for x in range(self.series.cols):
                flat_hu.append(self.series.get_voxel(z, y, x))

        return MPRSlice(
            plane=PlaneType.CORONAL,
            slice_index=y,
            rows=out_rows,
            columns=out_cols,
            pixel_spacing=(self.series.slice_thickness, self.series.col_spacing),
            pixels_hu=flat_hu,
        )

    def extract_sagittal(self, x_index: int) -> MPRSlice:
        """Extracts sagittal plane slice (Z x Y) (Lateral view)."""
        x = max(0, min(self.series.cols - 1, x_index))
        out_rows = self.series.num_slices
        out_cols = self.series.rows
        flat_hu: List[float] = []

        for z in range(self.series.num_slices - 1, -1, -1):
            for y in range(self.series.rows):
                flat_hu.append(self.series.get_voxel(z, y, x))

        return MPRSlice(
            plane=PlaneType.SAGITTAL,
            slice_index=x,
            rows=out_rows,
            columns=out_cols,
            pixel_spacing=(self.series.slice_thickness, self.series.row_spacing),
            pixels_hu=flat_hu,
        )

    def compute_maximum_intensity_projection(
        self,
        plane: PlaneType = PlaneType.AXIAL,
        slab_thickness_slices: int = 10,
        start_slice: int = 0,
    ) -> List[float]:
        """Calculates Maximum Intensity Projection (MIP) across a slab for CT angiography."""
        end_slice = min(self.series.num_slices, start_slice + slab_thickness_slices)
        num_pixels = self.series.rows * self.series.cols
        mip_pixels = [-10000.0] * num_pixels

        for z in range(start_slice, end_slice):
            for r in range(self.series.rows):
                for c in range(self.series.cols):
                    idx = r * self.series.cols + c
                    val = self.series.get_voxel(z, r, c)
                    if val > mip_pixels[idx]:
                        mip_pixels[idx] = val

        return mip_pixels
