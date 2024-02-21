from enum import Enum

class CANList(Enum):
    EMERGENCY=0x000
    BATTERY_ERROR=0x001
    
    ROLLER = 0x100
    
    SHOOT = 0x101
    BALL_HAND = 0x102
    
    ARM_EXPANDER = 0x103
    
    ARM_ELEVATOR = 0x104
    HAND1 = 0x105
    HAND2 = 0X106

    ARM1 = 0x108
    ARM2 = 0x109
    
    ROBOT_VEL = 0x10B
    