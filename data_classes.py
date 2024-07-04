from dataclasses import dataclass
from typing import Optional


@dataclass
class RobotCommand:
    id: int
    kickspeedx: Optional[float] = 0
    kickspeedz: Optional[float] = 0
    veltangent: Optional[float] = 0
    velnormal: Optional[float] = 0
    velangular: Optional[float] = 0
    spinner: Optional[bool] = False
    wheelsspeed: Optional[bool] = False
    wheel1: Optional[float] = 0
    wheel2: Optional[float] = 0
    wheel3: Optional[float] = 0
    wheel4: Optional[float] = 0
