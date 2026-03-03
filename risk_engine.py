import pandas as pd


# -------------------------------------------------------
# CONTROL METHODS DATABASE
# -------------------------------------------------------
def get_control_methods():
    methods = [
        {
            "name": "Chemical Pesticide",
            "cost": 2500,
            "risk": 0.7,
            "effectiveness": 0.9,
            "environmental_impact": "High",
            "type": "Synthetic"
        },
        {
            "name": "Biological Control",
            "cost": 1800,
            "risk": 0.3,
            "effectiveness": 0.75,
            "environmental_impact": "Low",
            "type": "Biological"
        },
        {
            "name": "Neem-based Organic Spray",
            "cost": 900,
            "risk": 0.2,
            "effectiveness": 0.6,
            "environmental_impact": "Very Low",
            "type": "Organic"
        },
        {
            "name": "Integrated Pest Management (IPM)",
            "cost": 2200,
            "risk": 0.4,
            "effectiveness": 0.85,
            "environmental_impact": "Medium",
            "type": "Integrated"
        }
    ]

    df = pd.DataFrame(methods)
    df["estimated_yield_gain"] = df["effectiveness"] * 100
    return df


# -------------------------------------------------------
# ADVANCED DECISION ENGINE
# -------------------------------------------------------
def recommend_method(risk_score, budget, life_stage=None):

    df = get_control_methods()
    df = df[df["cost"] <= budget]

    if df.empty:
        return None

    df = df.copy()

    # ----------------------------
    # Dynamic Weights by Risk Level
    # ----------------------------
    if risk_score > 0.7:  # High outbreak
        w_eff = 0.6
        w_risk = 0.2
        w_cost = 0.2

    elif risk_score > 0.4:  # Moderate outbreak
        w_eff = 0.4
        w_risk = 0.3
        w_cost = 0.3

    else:  # Low outbreak
        w_eff = 0.3
        w_risk = 0.4
        w_cost = 0.3

    # ----------------------------
    # Lifecycle Adjustment
    # ----------------------------
    stage_bonus = 0

    if life_stage == "Larva":
        stage_bonus = 0.1  # prioritize stronger control
    elif life_stage == "Egg":
        stage_bonus = -0.05  # eco-friendly bias

    # ----------------------------
    # Decision Score Formula
    # ----------------------------
    df["decision_score"] = (
        w_eff * df["effectiveness"]
        - w_risk * df["risk"]
        - w_cost * (df["cost"] / budget)
        + stage_bonus
    )

    best = df.sort_values("decision_score", ascending=False).iloc[0]
    return best


# -------------------------------------------------------
# EXTENDED FARMER ADVISORY ENGINE
# -------------------------------------------------------
def generate_extended_advisory(
    pest,
    risk_level,
    rainfall,
    radiation,
    temperature,
    life_stage
):

    advisory = []

    # ----------------------------
    # Risk-based Advisory
    # ----------------------------
    if risk_level == "High":
        advisory.append(
            f"High {pest} outbreak probability detected. Immediate intervention recommended."
        )
        advisory.append(
            "Conduct detailed field inspection within 48 hours and identify hotspot zones."
        )

    elif risk_level == "Moderate":
        advisory.append(
            f"Moderate {pest} activity observed. Preventive measures should be initiated."
        )
        advisory.append(
            "Increase scouting frequency to twice per week."
        )

    else:
        advisory.append(
            f"Low {pest} risk currently. Monitoring is sufficient."
        )

    # ----------------------------
    # Weather-based Advisory
    # ----------------------------
    if rainfall > 50:
        advisory.append(
            "Recent high rainfall may enhance pest breeding and secondary infections."
        )

    if temperature > 30:
        advisory.append(
            "High temperature accelerates pest development cycle."
        )

    if radiation < 100:
        advisory.append(
            "Low solar radiation may increase leaf moisture and vulnerability."
        )

    # ----------------------------
    # Lifecycle Guidance
    # ----------------------------
    advisory.append(f"Current predicted life stage: {life_stage}")

    if life_stage == "Egg":
        advisory.append(
            "Destroy visible egg clusters manually if infestation is localized."
        )

    elif life_stage == "Larva":
        advisory.append(
            "Larval stage is most destructive. Apply control during early instars for maximum effectiveness."
        )

    elif life_stage == "Pupa":
        advisory.append(
            "Pupal stage less responsive to sprays. Consider soil or residue management."
        )

    else:
        advisory.append(
            "Adult stage active. Install pheromone traps for monitoring and mass trapping."
        )

    # ----------------------------
    # Integrated Pest Management Section
    # ----------------------------
    advisory.append("--- Integrated Pest Management Guidelines ---")
    advisory.append("• Avoid excessive nitrogen fertilizer.")
    advisory.append("• Maintain field sanitation.")
    advisory.append("• Rotate crops to break pest cycles.")
    advisory.append("• Use economic threshold-based spraying.")
    advisory.append("• Wear protective equipment during pesticide application.")
    advisory.append("• Follow local agricultural extension recommendations.")

    return "\n".join(advisory)
