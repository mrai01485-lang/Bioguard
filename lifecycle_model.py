from settings import EGG_GDD, LARVA_GDD, PUPA_GDD

def predict_stage(cumulative_gdd):
    if cumulative_gdd < EGG_GDD:
        return "Egg"
    elif cumulative_gdd < LARVA_GDD:
        return "Larva"
    elif cumulative_gdd < PUPA_GDD:
        return "Pupa"
    else:
        return "Adult"
