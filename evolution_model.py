def fitness_score(survival_rate, reproduction_rate):
    return survival_rate * reproduction_rate

def simulate_climate_shift(temp_increase):
    base_survival = 0.85
    reproduction_rate = 1.6

    adjusted_survival = base_survival - (0.04 * temp_increase)

    return {
        "temp_increase": temp_increase,
        "fitness_score": fitness_score(adjusted_survival, reproduction_rate)
    }
