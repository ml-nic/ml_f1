# step 1: https://sourceforge.net/projects/vjoystick/files/latest/download
# step 2: SDK: http://vjoystick.sourceforge.net/site/index.php/component/weblinks/weblink/13-uncategorised/11-redirect-vjoy2sdk?task=weblink.go
# step 3: CONST_DLL_VJOY = "vJoyInterface.dll" ...KEEP .DLL local? 
# step 4: http://www.x360ce.com/, 64 bit download
# step 5: extract, copy to gtav directory
# step 6: run, should auto-detect vjoy, test with example make sure it works.
# step 7: CLOSE the app, run game. Test with example to see if works.

# SOURCE: https://gist.github.com/Flandan/fdadd7046afee83822fcff003ab47087#file-vjoy-py

import ctypes
import struct, time

CONST_DLL_VJOY = "vJoyInterface.dll"
MAX = 32767
MID = 16383


class vJoy(object):
    def __init__(self, reference=1):
        self.handle = None
        self.dll = ctypes.CDLL(CONST_DLL_VJOY)
        self.reference = reference
        self.acquired = False

    def open(self):
        if self.dll.AcquireVJD(self.reference):
            self.acquired = True
            return True
        return False

    def close(self):
        if self.dll.RelinquishVJD(self.reference):
            self.acquired = False
            return True
        return False

    def generateJoystickPosition(self,
                                 wThrottle=0, wRudder=0, wAileron=0,
                                 # left thb x        left thb y     left trigger
                                 wAxisX=MID, wAxisY=MAX, wAxisZ=0,
                                 # right thb x       right thb y        right trigger
                                 wAxisXRot=0, wAxisYRot=0, wAxisZRot=MAX,
                                 # ???         ???        ???
                                 wSlider=0, wDial=0, wWheel=0,
                                 # ???         ???        ???
                                 wAxisVX=0, wAxisVY=0, wAxisVZ=0,
                                 # ???         ???                ???
                                 wAxisVBRX=0, wAxisVBRY=0, wAxisVBRZ=0,
                                 # 1 = a
                                 # 2 = b  3 = a+b ??
                                 # 4 = x  5 = x+a ?? 6 = x+b
                                 # 8 = y
                                 lButtons=0, bHats=0, bHatsEx1=0, bHatsEx2=0, bHatsEx3=0):
        """
        typedef struct _JOYSTICK_POSITION
        {
            BYTE    bDevice; // Index of device. 1-based
            LONG    wThrottle;
            LONG    wRudder;
            LONG    wAileron;
            LONG    wAxisX;
            LONG    wAxisY;
            LONG    wAxisZ;
            LONG    wAxisXRot;
            LONG    wAxisYRot;
            LONG    wAxisZRot;
            LONG    wSlider;
            LONG    wDial;
            LONG    wWheel;
            LONG    wAxisVX;
            LONG    wAxisVY;
            LONG    wAxisVZ;
            LONG    wAxisVBRX;
            LONG    wAxisVBRY;
            LONG    wAxisVBRZ;
            LONG    lButtons;   // 32 buttons: 0x00000001 means button1 is pressed, 0x80000000 -> button32 is pressed
            DWORD   bHats;      // Lower 4 bits: HAT switch or 16-bit of continuous HAT switch
                        DWORD   bHatsEx1;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx2;   // 16-bit of continuous HAT switch
                        DWORD   bHatsEx3;   // 16-bit of continuous HAT switch
        } JOYSTICK_POSITION, *PJOYSTICK_POSITION;
        """
        joyPosFormat = "BlllllllllllllllllllIIII"
        pos = struct.pack(joyPosFormat, self.reference, wThrottle, wRudder,
                          wAileron, wAxisX, wAxisY, wAxisZ, wAxisXRot, wAxisYRot,
                          wAxisZRot, wSlider, wDial, wWheel, wAxisVX, wAxisVY, wAxisVZ,
                          wAxisVBRX, wAxisVBRY, wAxisVBRZ, lButtons, bHats, bHatsEx1, bHatsEx2, bHatsEx3)
        return pos

    def update(self, joystickPosition):
        if self.dll.UpdateVJD(self.reference, joystickPosition):
            return True
        return False


def all_reset(vj):
    vj.open()
    joystickPosition = vj.generateJoystickPosition(wAxisX=16383)
    joystickPosition = vj.generateJoystickPosition(wAxisXRot=0)
    joystickPosition = vj.generateJoystickPosition(wAxisY=MAX)
    joystickPosition = vj.generateJoystickPosition(wAxisYRot=0)
    joystickPosition = vj.generateJoystickPosition(wAxisZ=0)
    joystickPosition = vj.generateJoystickPosition(wAxisZRot=MAX)
    vj.update(joystickPosition)
    vj.close()


def brake_reset(vj, open=True):
    if open:
        vj.open()
    joystickPosition = vj.generateJoystickPosition(wAxisZRot=MAX)
    vj.update(joystickPosition)
    if open:
        vj.close()


def brake(vj, value=-1):
    vj.open()
    if value == -1:
        vj.open()
        for i in reversed(range(0, 33786)):
            print(i)
            joystickPosition = vj.generateJoystickPosition(wAxisZRot=i)
            vj.update(joystickPosition)
        brake_reset(open=False)
    else:
        joystickPosition = vj.generateJoystickPosition(wAxisZRot=0)
        vj.update(joystickPosition)
    vj.close()


def throttle_reset(vj, open=True):
    if open:
        vj.open()
    joystickPosition = vj.generateJoystickPosition(wAxisY=MAX)
    vj.update(joystickPosition)
    if open:
        vj.close()


def throttle(vj, value=-1):
    vj.open()
    if value == -1:
        vj.open()
        for i in reversed(range(MAX)):
            print(i)
            joystickPosition = vj.generateJoystickPosition(wAxisY=i)
            vj.update(joystickPosition)
        throttle_reset(open=False)
    else:
        joystickPosition = vj.generateJoystickPosition(wAxisY=0)
        vj.update(joystickPosition)
    vj.close()


def whole_right_and_reset(vj):
    vj.open()
    for i in range(16383, 33786):
        print(i)
        joystickPosition = vj.generateJoystickPosition(wAxisX=i)
        vj.update(joystickPosition)
    reset_wheel(open=False)
    vj.close()


def reset_wheel(vj, open=True):
    if open:
        vj.open()
    joystickPosition = vj.generateJoystickPosition(wAxisX=MID)
    vj.update(joystickPosition)
    if open:
        vj.close()


def whole_left_and_reset(vj, value=None):
    vj.open()
    for i in reversed(range(16383)):
        print(i)
        joystickPosition = vj.generateJoystickPosition(wAxisX=i)
        vj.update(joystickPosition)
    reset_wheel(open=False)
    vj.close()


def set_all(vj, wheel, acclerate, brake):
    """
    steering_angle = 0  # -1 (left) to 1 (right)
    accelerator = 1  # 1 no acceleration to -1 full acceleration
    brake = 1  # 1 no brake to -1 full brake

    wheel -1 => 0
    wheel 0 => MID
    wheel 1  => MAX

    accelerator 1 => MAX
    accelerator -1 => 0

    brake 1 => MAX
    brake -1 => 0
    """
    # scale to output format:

    def scale(old_value=None, old_min=None, old_max=None, new_max=None, new_min=None):
        return ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

    wheel = scale(old_value=wheel, old_min=-1, old_max=1, new_max=MAX, new_min=0)
    acclerate = scale(old_value=acclerate, old_min=-1, old_max=1, new_max=MAX, new_min=0)
    brake = scale(old_value=brake, old_min=-1, old_max=1, new_max=MAX, new_min=0)

    vj.open()
    joystickPosition = vj.generateJoystickPosition(wAxisX=wheel, wAxisY=acclerate, wAxisZRot=brake)
    vj.update(joystickPosition)
    vj.close()



{"left/right": "wAxisX", "throttle": "wAxisY", "brake": "wAxisZRot"}
if __name__ == '__main__':

    while (True):
        for i in reversed(range(1, 3)):
            print(i)
            time.sleep(1)

        vj.open()
        joystickPosition = vj.generateJoystickPosition(wAxisZ=32000)
        vj.update(joystickPosition)
        vj.close()
