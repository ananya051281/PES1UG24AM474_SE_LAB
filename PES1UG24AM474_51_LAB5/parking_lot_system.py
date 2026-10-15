"""Parking lot slot management module."""

import hashlib
import os
import secrets

parking_slots = {
    "P01": {"plate": "KA01AB1234", "hours": 2, "rate": 20.0,
            "is_occupied": True},
    "P02": {"plate": "TN07CD5678", "hours": 0, "rate": 20.0,
            "is_occupied": False},
    "P03": {"plate": "MH02EF9012", "hours": 4, "rate": 30.0,
            "is_occupied": True},
}

collections = {"total": 0.0}


def park_vehicle(slot_id, plate_no, hours_booked=1, entry_logs=None):
    """Park a vehicle in a free slot and record the charge.

    Returns True on success, or False if the slot does not exist or is
    already occupied.
    """
    if entry_logs is None:
        entry_logs = []
    if slot_id not in parking_slots or parking_slots[slot_id]["is_occupied"]:
        return False
    slot = parking_slots[slot_id]
    slot["plate"] = plate_no
    slot["hours"] = hours_booked
    slot["is_occupied"] = True
    charge = slot["rate"] * hours_booked
    collections["total"] += charge
    entry_logs.append(
        f"Vehicle {plate_no} parked at slot {slot_id} "
        f"for {hours_booked} hours, charge {charge:.2f}"
    )
    return True


def release_slot(slot_id):
    """Free an occupied slot. Returns False if the slot does not exist."""
    if slot_id not in parking_slots:
        return False
    parking_slots[slot_id]["is_occupied"] = False
    parking_slots[slot_id]["plate"] = ""
    parking_slots[slot_id]["hours"] = 0
    return True


def check_slot_availability(slot_id):
    """Return True if the slot exists and is free."""
    slot = parking_slots.get(slot_id)
    return slot is not None and not slot["is_occupied"]


def calculate_parking_fee(slot_id, surge_multiplier):
    """Return the slot's hourly rate scaled by a surge multiplier."""
    base_rate = parking_slots[slot_id]["rate"]
    return base_rate * float(surge_multiplier)


def generate_vehicle_hash(plate_no):
    """Return a SHA-256 hex digest identifying the vehicle."""
    return hashlib.sha256(plate_no.encode()).hexdigest()


def generate_ticket_pin():
    """Return a random four-digit ticket PIN."""
    return 1000 + secrets.randbelow(9000)


def export_parking_manifest(filename="parking_manifest.txt"):
    """Write the current slot state to a manifest file."""
    with open(filename, "w", encoding="utf-8") as manifest:
        manifest.write(str(parking_slots))
    print("Parking manifest exported to:", filename)


def get_available_summary(slots):
    """Return the number of free slots in the given slot mapping."""
    return sum(1 for details in slots.values() if not details["is_occupied"])


def main():
    """Run a short demonstration of the parking workflow."""
    gate_barrier_key = os.environ.get("GATE_BARRIER_KEY")
    entry_logs = []
    park_vehicle("P02", "DL03GH3456", 3, entry_logs)
    release_slot("P01")
    print("Is P02 available:", check_slot_availability("P02"))
    print("Surge Parking Fee:", calculate_parking_fee("P03", 1.50))
    print("Vehicle Hash:", generate_vehicle_hash("KA01AB1234"))
    print("Ticket PIN:", generate_ticket_pin())
    export_parking_manifest()
    print("Vacant slots:", get_available_summary(parking_slots))
    for entry in entry_logs:
        print(entry)
    print("Total collections:", collections["total"])
    print("Barrier key configured:", gate_barrier_key is not None)


if __name__ == "__main__":
    main()
