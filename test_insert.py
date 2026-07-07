from backend.database import insert_monitoring

insert_monitoring(
    voltage=220,
    current=1.1,
    power=240,
    energy=2.5,
    frequency=50,
    power_factor=0.98,
)

print("INSERT SUCCESS")