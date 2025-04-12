import streamlit as st
import random
from fpdf import FPDF
import datetime

# --- Préférences utilisateur ---
proteines = {
    "Poulet grillé": "150g",
    "Steak haché 5%": "150g",
    "Escalope de dinde": "150g"
}

feculents = {
    "Riz complet": "100g cuit",
    "Pâtes complètes": "100g cuit",
    "Patate douce": "150g",
    "Quinoa": "100g cuit",
    "Lentilles": "100g cuites"
}

legumes = {
    "Brocolis vapeur": "200g",
    "Haricots verts": "200g",
    "Courgettes rôties": "200g",
    "Carottes râpées": "150g",
    "Poêlée de champignons": "150g"
}

desserts = {
    "Yaourt nature + fruits rouges": "1 pot (125g)",
    "Compote sans sucre + 1 carré de chocolat noir": "1 compote (100g) + 1 carré",
    "Flan maison léger": "1 portion (150g)",
    "Fromage blanc + cannelle": "1 pot (150g)"
}

collations = {
    "Banane + 30g amandes": "1 banane + 30g amandes",
    "Pain complet + beurre de cacahuète": "2 tranches de pain complet + 20g beurre de cacahuète",
    "Shaker protéiné + fruit": "1 shaker + 1 fruit"
}

fruits = {
    "Pomme": "1 fruit",
    "Orange": "1 fruit",
    "Kiwi": "1 fruit"
}

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
        "Protéine": random.choice(list(proteines.keys())),
        "Féculent": random.choice(list(feculents.keys())),
        "Légume": random.choice([l for l in legumes.keys() if l != "Tomates"]),
        "Fruit": random.choice(list(fruits.keys()))
    }
    collation = random.choice(list(collations.keys()))
    diner = {
        "Protéine": random.choice(list(proteines.keys())),
        "Féculent": random.choice(list(feculents.keys())),
        "Légume": random.choice([l for l in legumes.keys() if l != "Tomates"]),
        "Dessert": random.choice(list(desserts.keys()))
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
        pdf.cell(200, 8, txt=f"  - {k}: {v} ({globals()[k][v]})", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Collation: {collation} ({collations[collation]})", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt="Dîner:", ln=True)
    for k, v in diner.items():
        pdf.cell(200, 8, txt=f"  - {k}: {v} ({globals()[k][v]})", ln=True)

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
        st.write(f"- **{k}** : {v} ({globals()[k][v]})")

    st.markdown("### 🍌 Collation après-midi")
    st.write(f"- {collation} ({collations[collation]})")

    st.markdown("### 🍽️ Dîner + Dessert")
    for k, v in diner.items():
        st.write(f"- **{k}** : {v} ({globals()[k][v]})")

    st.markdown(f"### 🔥 Total calorique estimé : **{total_kcal} kcal**")

    # Export PDF
    pdf_bytes = export_pdf(dejeuner, collation, diner)
    st.download_button(label="📄 Télécharger le menu en PDF", data=pdf_bytes, file_name="menu_journalier.pdf", mime="application/pdf")

else:
    st.info("Clique sur le bouton ci-dessus pour générer ton menu personnalisé !")
