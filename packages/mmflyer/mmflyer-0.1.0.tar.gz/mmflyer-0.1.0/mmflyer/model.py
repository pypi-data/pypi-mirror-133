import pint
u = pint.UnitRegistry()

C_l = [0.06, 0.135, 0.2, 0.25, 0.3, 0.35, 0.395, 0.44]
C_d = [0.008, 0.009, 0.01, 0.012, 0.014, 0.019, 0.024, 0.0335]
alpha = [-2.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0]

aw = 150.0 * u.inches**2
test_model = {
    "SW": 150.0 * u.inches**2,
    "WC": 5.5* u.inches,
    "WH": 3.0*u.inches,
    "WT": 0.070 * u.ounces,
    "PCW":  0.40, # percent
    "TA": 17.0 * u.inches
}
