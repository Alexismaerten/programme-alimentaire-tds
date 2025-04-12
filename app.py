
import streamlit as st
import random
from fpdf import FPDF
import datetime

# --- Préférences utilisateur ---
proteines = ["Poulet grillé", "Steak haché 5%", "Escalope de dinde"]
feculents = ["Riz complet", "Pâtes complètes", "Patate douce", "Quinoa", "Lentilles"]
legumes = ["Brocolis vapeur", "Haricots verts", "Courgettes rôties", "Carottes râpées", "Poêlée de champignons"]
desserts = ["Yaourt nature + fruits rouges", "Compote sans sucre + 1 carré de chocolat noir", "Flan maison léger", "Fromage blanc + cannelle"]
collations = ["Banane + 30g amandes", "Pain complet + beurre de cacahuète", "Shaker protéiné + fruit"]

# --- Calories approximatives par aliment ---
calories = {
    "Poulet grillé": 300, "Steak haché 5%": 350, "Escalope de dinde": 280,
    "Riz complet": 220, "Pâtes complètes": 230, "Patate douce": 200, "Quinoa": 240, "Lentilles": 210,
    "Brocolis vapeur": 50, "Haricots verts": 40, "Courgettes rôties": 60, "Carottes râpées": 70, "Poêlée de champignons": 80,
    "Yaourt nature + fruits rouges": 150, "Compote sans sucre + 1 carré de chocolat noir": 130,
    "Flan maison léger": 180, "Fromage blanc + cannelle": 160,
    "Banane + 30g amandes": 450, "Pain complet + beurre de cacahuète": 400, "Shaker protéiné + fruit": 420,
    "Pomme": 80, "Orange": 90, "Kiwi": 60
}

# --- Génération du menu ---
def generer_menu():
    dejeuner = {
        "Protéine": random.choice(proteines),
        "Féculent": random.choice(feculents),
        "Légume": random.choice([l for l in legumes if l != "Tomates"]),
        "Fruit": random.choice(["Pomme", "Orange", "Kiwi"])
    }
    collation = random.choice(collations)
    diner = {
        "Protéine": random.choice(proteines),
        "Féculent": random.choice(feculents),
        "Légume": random.choice([l for l in legumes if l != "Tomates"]),
        "Dessert": random.choice(desserts)
    }
    return dejeuner, collation, diner

# --- Calcul des calories ---
def calculer_calories(repas):
    total = 0
    for item in repas.values():
        total += calories.get(item, 0)
    return total

# --- PDF export ---
def export_pdf(dejeuner, collation, diner):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Menu du jour - {datetime.date.today().strftime('%d/%m/%Y')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="Déjeuner:", ln=True)
    for k, v in dejeuner.items():
        pdf.cell(200, 8, txt=f"  - {k}: {v}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Collation: {collation}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Dîner:", ln=True)
    for k, v in diner.items():
        pdf.cell(200, 8, txt=f"  - {k}: {v}", ln=True)

    total_kcal = calculer_calories(dejeuner) + calories.get(collation, 0) + calculer_calories(diner)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Total calorique estimé : {total_kcal} kcal", ln=True)

    return pdf.output(dest='S').encode('latin-1')

# --- UI Streamlit ---
st.set_page_config(page_title="Programme alimentaire - Perte de poids", layout="centered")
st.title("🍽️ Programme alimentaire journalier")
st.subheader("Objectif : perte de poids rapide en vue de la TDS")

if st.button("🎲 Générer mon menu du jour"):
    dejeuner, collation, diner = generer_menu()
    total_kcal = calculer_calories(dejeuner) + calories.get(collation, 0) + calculer_calories(diner)

    st.markdown("### 🥗 Déjeuner")
    for k, v in dejeuner.items():
        st.write(f"- **{k}** : {v}")

    st.markdown("### 🍌 Collation après-midi")
    st.write(f"- {collation}")

    st.markdown("### 🍽️ Dîner + Dessert")
    for k, v in diner.items():
        st.write(f"- **{k}** : {v}")

    st.markdown(f"### 🔥 Total calorique estimé : **{total_kcal} kcal**")

    # Export PDF
    pdf_bytes = export_pdf(dejeuner, collation, diner)
    st.download_button(label="📄 Télécharger le menu en PDF", data=pdf_bytes, file_name="menu_journalier.pdf", mime="application/pdf")

else:
    st.info("Clique sur le bouton ci-dessus pour générer ton menu personnalisé !")
