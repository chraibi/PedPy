from __future__ import annotations

import pathlib
from dataclasses import dataclass

import pandas as pd
import pygeos
from aenum import Enum, auto


class TrajectoryUnit(Enum):
    """Identifier of the unit of the trajectory coordinates"""

    _init_ = "value __doc__"
    METER = 1, "meter (m)"
    CENTIMETER = 100, "centimeter (cm)"


class TrajectoryType(Enum):
    """Identifier for the type of trajectory"""

    _init_ = "value __doc__"

    PETRACK = auto(), "PeTrack trajectory"
    JUPEDSIM = auto(), "JuPedSim trajectory"
    FALLBACK = auto(), "trajectory of unknown type"


@dataclass
class TrajectoryData:
    """Trajectory Data

    Wrapper around the trajectory data, holds the data as a data frame.

    Note:
        The coordinate data is stored in meter ('m')!

    Attributes:
        _data (pd.DataFrame): data frame containing the actual data in the form:
            "ID", "frame", "X", "Y", "Z"

        frame_rate (float): frame rate of the trajectory file

        trajectory_type (TrajectoryType): type of the trajectory used

        file (pothlib.Path): file from which is trajectories was read

    """

    data: pd.DataFrame
    frame_rate: float
    trajectory_type: TrajectoryType
    file: pathlib.Path

    def __init__(
        self,
        data: pd.DataFrame,
        frame_rate: float,
        trajectory_type: TrajectoryType,
        file: pathlib.Path,
    ):
        self.frame_rate = frame_rate
        self.trajectory_type = trajectory_type
        self.file = file

        self.data = data
        self.data["points"] = pygeos.points(self.data["X"], self.data["Y"])
