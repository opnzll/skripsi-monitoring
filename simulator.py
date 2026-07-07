import random
import time
from datetime import datetime

from backend.database import insert_monitoring

# ==========================================================
# SMART ELECTRICAL IoT SIMULATOR v4
# ==========================================================

"""
Realtime Electrical Simulator

Designed for:

- Dashboard
- History
- Analytics
- Machine Learning
- K-Means

Author:
Skripsi Monitoring
"""

# ==========================================================
# CONFIGURATION
# ==========================================================

INTERVAL = 2

SMOOTHING = 0.08

BASE_VOLTAGE = 221.5

BASE_FREQUENCY = 50.00

# ==========================================================
# LOAD PROFILE
# ==========================================================

LOAD_PROFILE = [

    {
        "name": "Standby",
        "power": 120,
        "pf": 0.98,
        "duration": 180
    },

    {
        "name": "Lighting",
        "power": 220,
        "pf": 0.97,
        "duration": 180
    },

    {
        "name": "Office",
        "power": 360,
        "pf": 0.96,
        "duration": 240
    },

    {
        "name": "Television",
        "power": 500,
        "pf": 0.95,
        "duration": 180
    },

    {
        "name": "Kitchen",
        "power": 720,
        "pf": 0.94,
        "duration": 240
    },

    {
        "name": "Air Conditioner",
        "power": 980,
        "pf": 0.92,
        "duration": 300
    },

    {
        "name": "Peak Load",
        "power": 1250,
        "pf": 0.90,
        "duration": 300
    },

    {
        "name": "Night",
        "power": 250,
        "pf": 0.98,
        "duration": 180
    }

]

# ==========================================================
# EVENT PROFILE
# ==========================================================

EVENT_PROFILE = [

    {

        "name":"Normal",

        "voltage_offset":0,

        "power_multiplier":1.00,

        "pf_offset":0,

        "duration":420

    },

    {

        "name":"Voltage Drop",

        "voltage_offset":-10,

        "power_multiplier":1.00,

        "pf_offset":0,

        "duration":60

    },

    {

        "name":"Overload",

        "voltage_offset":-3,

        "power_multiplier":1.35,

        "pf_offset":-0.03,

        "duration":90

    },

    {

        "name":"Low Power Factor",

        "voltage_offset":0,

        "power_multiplier":1.00,

        "pf_offset":-0.10,

        "duration":90

    },

    {

        "name":"Recovery",

        "voltage_offset":1,

        "power_multiplier":0.95,

        "pf_offset":0.03,

        "duration":120

    }

]

# ==========================================================
# GLOBAL VARIABLE
# ==========================================================

energy = 0.0

current_power = LOAD_PROFILE[0]["power"]

load_index = 0

event_index = 0

load_counter = 0

event_counter = 0

print("="*70)

print(" SMART ELECTRICAL IoT SIMULATOR v4 ")

print("="*70)

print()

# ==========================================================
# SMART SIMULATION ENGINE
# ==========================================================

def generate_sample():

    global energy
    global current_power

    global load_index
    global load_counter

    global event_index
    global event_counter

    # ------------------------------------------------------
    # ACTIVE PROFILE
    # ------------------------------------------------------

    load = LOAD_PROFILE[load_index]
    event = EVENT_PROFILE[event_index]

    # ------------------------------------------------------
    # TIMER
    # ------------------------------------------------------

    load_counter += INTERVAL
    event_counter += INTERVAL

    # ------------------------------------------------------
    # CHANGE LOAD PROFILE
    # ------------------------------------------------------

    if load_counter >= load["duration"]:

        load_counter = 0

        load_index += 1

        if load_index >= len(LOAD_PROFILE):
            load_index = 0

        load = LOAD_PROFILE[load_index]

        print()
        print("=" * 70)
        print(f"LOAD PROFILE : {load['name']}")
        print("=" * 70)

    # ------------------------------------------------------
    # CHANGE EVENT
    # ------------------------------------------------------

    if event_counter >= event["duration"]:

        event_counter = 0

        event_index += 1

        if event_index >= len(EVENT_PROFILE):
            event_index = 0

        event = EVENT_PROFILE[event_index]

        print()
        print("-" * 70)
        print(f"EVENT : {event['name']}")
        print("-" * 70)

    # ------------------------------------------------------
    # TARGET POWER
    # ------------------------------------------------------

    target_power = (
        load["power"] *
        event["power_multiplier"]
    )

    current_power += (
        target_power - current_power
    ) * SMOOTHING

    power = current_power

    power += random.uniform(-3, 3)

    power = max(power, 30)

    # ------------------------------------------------------
    # POWER FACTOR
    # ------------------------------------------------------

    pf = (
        load["pf"] +
        event["pf_offset"]
    )

    pf += random.uniform(-0.003, 0.003)

    pf = max(min(pf, 0.99), 0.80)

    # ------------------------------------------------------
    # VOLTAGE MODEL
    # ------------------------------------------------------

    voltage = BASE_VOLTAGE

    voltage += event["voltage_offset"]

    voltage -= power * 0.0018

    voltage += random.uniform(-0.25, 0.25)

    voltage = max(voltage, 180)
    voltage = min(voltage, 240)

    # ------------------------------------------------------
    # FREQUENCY MODEL
    # ------------------------------------------------------

    frequency = BASE_FREQUENCY

    frequency -= power * 0.00003

    frequency += random.uniform(-0.01, 0.01)

    frequency = max(frequency, 49.80)
    frequency = min(frequency, 50.20)

    # ------------------------------------------------------
    # CURRENT MODEL
    # ------------------------------------------------------

    current = power / (voltage * pf)

    current += random.uniform(-0.005, 0.005)

    current = max(current, 0)

    # ------------------------------------------------------
    # ENERGY
    # ------------------------------------------------------

    energy += (

        power *

        INTERVAL

    ) / 3600000

    # ------------------------------------------------------
    # SMALL SENSOR NOISE
    # ------------------------------------------------------

    voltage = round(voltage, 2)

    current = round(current, 3)

    power = round(power, 2)

    frequency = round(frequency, 2)

    pf = round(pf, 2)

    energy = round(energy, 5)

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return {

        "voltage": voltage,

        "current": current,

        "power": power,

        "energy": energy,

        "frequency": frequency,

        "power_factor": pf,

        "load": load["name"],

        "event": event["name"]

    }

# ==========================================================
# DATABASE WRITER
# ==========================================================

def save_to_database(sample):

    insert_monitoring(

        voltage=sample["voltage"],

        current=sample["current"],

        power=sample["power"],

        energy=sample["energy"],

        frequency=sample["frequency"],

        power_factor=sample["power_factor"]

    )


# ==========================================================
# LOGGER
# ==========================================================

def print_log(sample):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(

        f"[{timestamp}] "

        f"{sample['load']:<18}"

        f"| {sample['event']:<18}"

        f"| V={sample['voltage']:>6.2f}V "

        f"| I={sample['current']:>6.3f}A "

        f"| P={sample['power']:>7.2f}W "

        f"| PF={sample['power_factor']:.2f} "

        f"| F={sample['frequency']:.2f}Hz "

        f"| E={sample['energy']:.5f}kWh"

    )


# ==========================================================
# SIMULATOR LOOP
# ==========================================================

def run_simulator():

    print()
    print("=" * 70)
    print("Realtime Electrical Monitoring Started")
    print("=" * 70)
    print()

    while True:

        try:

            sample = generate_sample()

            save_to_database(sample)

            print_log(sample)

            time.sleep(INTERVAL)

        except KeyboardInterrupt:

            print()

            print("=" * 70)
            print("Simulator stopped by user.")
            print("=" * 70)

            break

        except Exception as e:

            print()

            print("=" * 70)
            print("DATABASE CONNECTION ERROR")
            print("=" * 70)

            print(e)

            print()

            print("Retrying in 5 seconds...")

            print()

            time.sleep(5)


# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":

    run_simulator()