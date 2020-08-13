# %%
from durable.lang import *


with ruleset("diagnosing_automotive"):

    @when_all(
        (m.engine_gets_gas == True) & (m.engine_turns_over == True)
    )
    def problem_is_spark_plugs(c):
        print(c.m)
        print("The problem is spark plugs.")

    @when_all(
        (m.engine_turns_over == False) & (m.lights_come_on == False)
    )
    def problem_is_battery_or_cables(c):
        print(c.m)
        print("The problem is battery or cables.")

    @when_all(
        (m.engine_turns_over == False) & (m.lights_come_on == True)
    )
    def problem_is_starter_motor(c):
        print(c.m)
        print("The problem is starter motor.")

    @when_all(
        (m.gas_in_fuel_tank == True) & (m.gas_in_carburator == True)
    )
    def engine_gets_gas_confirmed(c):
        post(
            "diagnosing_automotive",
            {
                "engine_gets_gas": True,
                "engine_turns_over": c.m.engine_turns_over,
                "lights_come_on": c.m.lights_come_on,
            },
        )

    @when_all(
        (m.gas_in_fuel_tank == False) | (m.gas_in_carburator == False)
    )
    def engine_gets_gas_unknown(c):
        post(
            "diagnosing_automotive",
            {
                "engine_gets_gas": c.m.engine_gets_gas,
                "engine_turns_over": c.m.engine_turns_over,
                "lights_come_on": c.m.lights_come_on,
            },
        )

    @when_all(
        (m.engine_gets_gas == None) | (m.engine_gets_gas == False)
    )
    def problem_is_unknown(c):
        print(c.m)
        print("The problem is unknown.")


# %%
from itertools import product

for (
    engine_turns_over,
    lights_come_on,
    gas_in_fuel_tank,
    gas_in_carburator,
) in product(
    [True, False], [True, False], [True, False], [True, False]
):
    fact = {
        "engine_turns_over": engine_turns_over,
        "lights_come_on": lights_come_on,
        "gas_in_fuel_tank": gas_in_fuel_tank,
        "gas_in_carburator": gas_in_carburator,
    }
    post("diagnosing_automotive", fact)
