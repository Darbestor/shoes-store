"""Sport type enum"""

from enum import Enum


class SportType(str, Enum):
    """Sport type for shoes"""

    FOOTBALL = "football"
    BASKETBALL = "basketball"
    WALKING = "walking"
    RUNNING = "running"
    LIFESTYLE = "lifestyle"
