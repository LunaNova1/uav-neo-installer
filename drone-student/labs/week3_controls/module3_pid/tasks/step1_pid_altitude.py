"""
MIT BWSI Autonomous Drone Racing Course - UAV Neo
GNU General Public License v3.0

Week 2/3 Lab — Step 1: PID Altitude Hold
Hold a target height with a full PID controller (P + I + D).
Heights are measured above the ground sampled at launch.
"""

import drone_core
import drone_utils as uav_utils

# -- Course setup: makes the shared `neo_lab` helper importable.
#    You don't need to read or change this block. --
import os as _os, sys as _sys
_d = _os.path.dirname(_os.path.realpath(__file__))
while _os.path.basename(_d) != "labs" and _os.path.dirname(_d) != _d:
    _d = _os.path.dirname(_d)
if _d not in _sys.path:
    _sys.path.insert(0, _d)
import neo_lab

# -- Constants --------------------------------------------------------------
TARGET_HEIGHT = 0.5
KP = 0.18
KI = 0.06
KD = 0.02
INT_CLAMP = 3.0      # anti-windup limit on the integral
THROTTLE_LIMIT = 0.5
TOL = 0.15
HOLD_TIME = 3.0

# -- Module-level state -----------------------------------------------------
_err_int = 0.0
_prev_err = 0.0
_sum_err = 0.0
_hold = 0.0
_done = False

def pid_control(err, err_int, err_dot, kp, ki, kd):
    """Return the PID controller output from the three gain terms (see README, Key terms)."""
    ##################################
    #### START PUT CODE HERE #########
    P = kp* err
    I = ki* err_int
    D = kd*err_dot
    output = P + I + D
    ###### END PUT CODE HERE #########
    ##################################
    return output

def reset():
    global _err_int, _prev_err, _hold, _done
    _err_int = 0.0
    _prev_err = 0.0
    _sum_err = 0.0
    _hold = 0.0
    _done = False


def update(drone):
    global _sum_err, _prev_err, _hold, _done

    if _done:
        return True

    height = neo_lab.height(drone)
    err_curr = TARGET_HEIGHT - height

    dt = drone.get_delta_time()

    _sum_err += err_curr * dt
    _sum_err = uav_utils.clamp(_sum_err, -INT_CLAMP, INT_CLAMP)

    integral = KI * _sum_err

    if dt > 0:
        derivative = KD * (err_curr - _prev_err) / dt
    else:
        derivative = 0

    proportional = KP * err_curr

    throttle = proportional + integral + derivative

    throttle = uav_utils.clamp(
        throttle,
        -THROTTLE_LIMIT,
        THROTTLE_LIMIT
    )

    drone.flight.send_pcmd(0, 0, 0, throttle)

    _prev_err = err_curr

    # Hold condition
    if abs(err_curr) <= TOL:
        _hold += dt
        print("Holding")
        if _hold >= HOLD_TIME:
            print("Done")
            _done = True
    else:
        _hold = 0

    return _done


if __name__ == "__main__":
    _drone = drone_core.create_drone()
    _launcher = neo_lab.Launcher()

    def start():
        _launcher.reset()
        reset()
        print("Step 1: PID Altitude Hold")

    def _update():
        if not _launcher.done:        # arm + climb to a safe height first
            _launcher.update(_drone)
            return
        if update(_drone):
            _drone.flight.land()

    _drone.set_start_update(start, _update)
    _drone.go()
