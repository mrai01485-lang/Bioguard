def get_advice(pest, risk, rainfall, radiation, temperature, crop="Maize"):

    advice = ""
    total_cost = 0

    # -----------------------------
    # Helper: Format pesticide info
    # -----------------------------
    def pesticide_block(name, dose, moa, toxicity, cost):
        nonlocal total_cost
        total_cost += cost
        return f"""
• {name}
  Dose: {dose}
  Mode of Action: {moa}
  WHO Toxicity Class: {toxicity}
  Estimated Cost per Acre: ₹{cost}
"""

    # =============================
    # ARMYWORM (Maize dominant)
    # =============================
    if pest == "Armyworm":

        if risk == "High Risk":

            advice += f"\nHigh Fall Armyworm Risk in {crop}.\n"

            advice += "\nRecommended Chemical Rotation (Do NOT repeat same MoA twice):\n"

            advice += pesticide_block(
                "Emamectin Benzoate 5 SG",
                "80 g/acre",
                "Group 6 (Chloride channel activator)",
                "Class II – Moderately hazardous",
                750
            )

            advice += pesticide_block(
                "Chlorantraniliprole 18.5 SC",
                "60 ml/acre",
                "Group 28 (Ryanodine receptor modulator)",
                "Class U – Unlikely acute hazard",
                1200
            )

            advice += "\nOrganic / IPM Options:\n"
            advice += """
• Neem oil (Azadirachtin 1500 ppm) – 3 ml/liter
• Install pheromone traps (5/acre)
• Release Trichogramma parasitoids
• Hand destruction of egg masses
"""

        else:
            advice += f"\nLow Armyworm Risk in {crop}.\n"
            advice += """
Monitoring Strategy:
• Install pheromone traps
• Weekly scouting of whorls
• Avoid excess nitrogen fertilizer
"""

    # =============================
    # STEM BORER (Rice / Maize)
    # =============================
    elif pest == "Stem Borer":

        if risk == "High Risk":

            advice += f"\nHigh Stem Borer Risk in {crop}.\n"

            advice += pesticide_block(
                "Cartap Hydrochloride 50 SP",
                "400 g/acre",
                "Nereistoxin analogue",
                "Class II – Moderately hazardous",
                600
            )

            advice += pesticide_block(
                "Chlorantraniliprole 0.4 GR",
                "4 kg/acre (soil)",
                "Group 28",
                "Class U",
                1400
            )

            advice += "\nIPM:\n"
            advice += """
• Remove dead hearts immediately
• Release Trichogramma japonicum
• Maintain proper irrigation drainage
"""

        else:
            advice += "\nLow Stem Borer Risk.\nField scouting recommended.\n"

    # =============================
    # APHIDS
    # =============================
    elif pest == "Aphids":

        if risk == "High Risk":

            advice += f"\nHigh Aphid Population in {crop}.\n"

            advice += pesticide_block(
                "Imidacloprid 17.8 SL",
                "40 ml/acre",
                "Group 4A (Neonicotinoid)",
                "Class II",
                500
            )

            advice += pesticide_block(
                "Thiamethoxam 25 WG",
                "40 g/acre",
                "Group 4A",
                "Class II",
                650
            )

            advice += "\nOrganic:\n"
            advice += """
• Neem oil spray
• Release ladybird beetles
• Soap-water spray (mild)
"""

        else:
            advice += "\nLow Aphid Risk.\nEncourage natural predators.\n"

    # =============================
    # WHITEFLY
    # =============================
    elif pest == "Whitefly":

        if risk == "High Risk":

            advice += f"\nHigh Whitefly Risk in {crop}.\n"

            advice += pesticide_block(
                "Buprofezin 25 SC",
                "400 ml/acre",
                "Chitin synthesis inhibitor",
                "Class U",
                900
            )

            advice += pesticide_block(
                "Spiromesifen 22.9 SC",
                "200 ml/acre",
                "Lipid synthesis inhibitor",
                "Class U",
                1500
            )

            advice += "\nIPM:\n"
            advice += """
• Yellow sticky traps (8/acre)
• Remove virus infected plants
• Crop rotation mandatory
"""

        else:
            advice += "\nLow Whitefly Risk.\nMaintain airflow and spacing.\n"

    # =============================
    # THRIPS
    # =============================
    elif pest == "Thrips":

        if risk == "High Risk":

            advice += f"\nHigh Thrips Activity in {crop}.\n"

            advice += pesticide_block(
                "Spinosad 45 SC",
                "60 ml/acre",
                "Group 5 (Nicotinic receptor modulator)",
                "Class III – Slightly hazardous",
                1100
            )

            advice += pesticide_block(
                "Fipronil 5 SC",
                "400 ml/acre",
                "Group 2B (GABA inhibitor)",
                "Class II",
                700
            )

            advice += "\nOrganic:\n"
            advice += """
• Blue sticky traps
• Neem extract spray
• Maintain adequate irrigation
"""

        else:
            advice += "\nLow Thrips Risk.\nRoutine crop inspection advised.\n"

    # =============================
    # WEATHER-SAFETY BLOCK
    # =============================

    advice += "\n\n--- Spray Safety Advisory ---\n"

    if rainfall > 10:
        advice += "• Heavy rainfall expected. Avoid spraying before rain.\n"

    if temperature > 35:
        advice += "• High temperature. Spray only early morning or late evening.\n"

    if radiation > 250:
        advice += "• High solar radiation. Avoid mid-day spraying to prevent phytotoxicity.\n"

    # =============================
    # COST SUMMARY
    # =============================

    if total_cost > 0:
        advice += f"\nEstimated Total Chemical Cost per Acre: ₹{total_cost}\n"
        advice += "Note: Prices vary by region and brand.\n"

    advice += "\nAll recommendations follow Integrated Pest Management (IPM) principles. Follow local agricultural extension guidelines."

    return advice
