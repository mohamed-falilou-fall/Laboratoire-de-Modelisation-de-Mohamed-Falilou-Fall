import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Plateforme de Scoring Pays",
    layout="wide"
)

# =========================================================
# THEME VIOLET
# =========================================================

violet_principal="#5A189A"
violet_fonce="#3C096C"
violet_clair="#9D4EDD"
violet_tres_clair="#F4ECFF"
violet_moyen="#7B2CBF"

st.markdown(f"""
<style>
.stSidebar {{
background-color:{violet_tres_clair};
}}
.stMetric {{
background-color:{violet_tres_clair};
border-radius:10px;
padding:10px;
border-left:6px solid {violet_principal};
}}
h1,h2,h3,h4 {{
color:{violet_principal};
}}
</style>
""",unsafe_allow_html=True)

# =========================================================
# TITRE & PRESENTATION
# =========================================================

st.title("Scoring du financement des pays (Data Engineering & Data Science)")
st.subheader("Première itération de la Plateforme de Scoring des Pays pour le Financement du Développement basée sur 66 indicateurs des World Development Indicators de la Banque mondiale")
st.markdown("###### Conception et développement par Mohamed Falilou Fall")

st.markdown("##")

st.markdown("""

### Objectif

La Plateforme de Scoring Financement Pays est un outil d’aide à la décision permettant d’évaluer l’attractivité des pays pour le financement du développement.

La plateforme repose sur les **World Development Indicators (Banque mondiale)** et combine plusieurs dimensions :

- Croissance économique  
- Stabilité macroéconomique  
- Investissement  
- Dette publique  
- Secteur financier  
- Energie  
- Conditions sociales  

### Méthodologie

Chaque indicateur est normalisé sur une échelle de 0 à 100 :

Score indicateur = (Valeur - Minimum) / (Maximum - Minimum)

Le score pays correspond à la moyenne des scores indicateurs.

Un ajustement stratégique est ensuite appliqué selon l’importance régionale IFC.

### Résultats produits

La plateforme fournit :

- Score pays  
- Score ajusté IFC  
- Classement mondial  
- Analyse automatique  
- Analyse régionale  
- Consultance stratégique IFC  

### Utilisation

Cet outil permet :

- La priorisation des pays  
- L’allocation des financements  
- L’analyse comparative  
- L’aide à la décision stratégique  

""")

# =========================================================
# CONFIGURATION IFC
# =========================================================

st.sidebar.header("Configuration International Finance Corporation")

importance_regions = {
"Africa":{"poids":36,"importance":"Très élevé","role":"Région prioritaire pour la finance de développement"},
"Asia":{"poids":24,"importance":"Très élevé","role":"Principaux marchés émergents"},
"South America":{"poids":19,"importance":"Élevé","role":"Marchés intermédiaires dynamiques"},
"Caribbean":{"poids":19,"importance":"Élevé","role":"Marchés intermédiaires dynamiques"},
"Eastern Europe":{"poids":15,"importance":"Moyen","role":"Transition économique"}
}

# =========================================================
# DONNEES
# =========================================================

file_path = "Filtered_World_Developement_Indicators.xlsx"
df = pd.read_excel(file_path)

# =========================================================
# PAYS PAR REGION
# =========================================================

africa = [
"Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi",
"Cabo Verde","Cameroon","Central African Republic","Comoros",
"Congo, Rep.","Congo, Dem. Rep.","Cote d'Ivoire","Djibouti",
"Egypt, Arab Rep.","Eritrea","Eswatini","Ethiopia","Gabon",
"Gambia, The","Ghana","Guinea","Guinea-Bissau","Equatorial Guinea",
"Kenya","Lesotho","Liberia","Libya","Madagascar","Malawi",
"Mali","Morocco","Mauritius","Mauritania","Mozambique",
"Namibia","Niger","Nigeria","Uganda","Rwanda",
"Sao Tome and Principe","Senegal","Seychelles","Sierra Leone",
"Somalia","Sudan","South Sudan","Tanzania","Togo",
"Tunisia","Zambia","Zimbabwe"
]

asia = [
"Afghanistan","Saudi Arabia","Armenia","Azerbaijan","Bahrain",
"Bangladesh","Bhutan","Myanmar","Brunei Darussalam","Cambodia",
"China","North Korea","South Korea","United Arab Emirates",
"Georgia","India","Indonesia","Iraq","Iran, Islamic Rep.",
"Israel","Japan","Jordan","Kazakhstan","Kyrgyz Republic",
"Kuwait","Lao PDR","Lebanon","Malaysia","Maldives",
"Mongolia","Nepal","Oman","Uzbekistan","Pakistan",
"Philippines","Qatar","Singapore","Sri Lanka",
"Syrian Arab Republic","Tajikistan","Taiwan, China",
"Thailand","Timor-Leste","Turkmenistan","Turkey",
"Yemen, Rep."
]

europe_est = [
"Belarus","Bulgaria","Czech Republic","Hungary","Poland",
"Slovak Republic","Romania","Moldova","Ukraine","Russia"
]

amerique_sud = [
"Argentina","Bolivia","Brazil","Chile","Colombia",
"Ecuador","Guyana","Paraguay","Peru","Suriname",
"Uruguay","Venezuela"
]

caraibes = [
"Antigua and Barbuda","Bahamas","Barbados","Cuba",
"Dominica","Dominican Republic","Grenada","Haiti",
"Jamaica","Saint Kitts and Nevis","Saint Lucia",
"Saint Vincent and the Grenadines","Trinidad and Tobago"
]

countries = (
[(c,"Africa") for c in africa] +
[(c,"Asia") for c in asia] +
[(c,"Eastern Europe") for c in europe_est] +
[(c,"South America") for c in amerique_sud] +
[(c,"Caribbean") for c in caraibes]
)

countries_df = pd.DataFrame(countries,columns=["Pays","Zone"])

# =========================================================
# NAVIGATION
# =========================================================

st.sidebar.header("Navigation")

selected_zone = st.sidebar.selectbox(
"Zone géographique",
countries_df["Zone"].unique()
)

selected_country = st.sidebar.selectbox(
"Pays",
countries_df[countries_df.Zone==selected_zone]["Pays"]
)

# =========================================================
# INDICATEURS (66)
# =========================================================

indicators = list(set([
"GDP growth (annual %)","GDP per capita (constant 2015 US$)",
"GDP per capita (constant LCU)","GDP per capita (current LCU)",
"GDP per capita (current US$)","GDP per capita growth (annual %)",
"GDP per capita, PPP (constant 2021 international $)",
"Government expenditure per student, primary (% of GDP per capita)",
"Government expenditure per student, secondary (% of GDP per capita)",
"Government expenditure per student, tertiary (% of GDP per capita)",
"Inflation, GDP deflator (annual %)","Inflation, GDP deflator: linked series (annual %)",
"Inflation, consumer prices (annual %)","Gross capital formation (% of GDP)",
"Gross capital formation (annual % growth)","Gross capital formation (constant 2015 US$)",
"Gross capital formation (constant LCU)","Gross capital formation (current LCU)",
"Gross capital formation (current US$)","Gross domestic income (constant LCU)",
"Gross domestic savings (% of GDP)","Gross domestic savings (current LCU)",
"Gross fixed capital formation (% of GDP)","Current account balance (% of GDP)",
"Current account balance (BoP, current US$)","Exports as a capacity to import (constant LCU)",
"Exports of goods and services (% of GDP)","Exports of goods and services (BoP, current US$)",
"Exports of goods and services (annual % growth)","Exports of goods and services (constant 2015 US$)",
"Exports of goods and services (constant LCU)","Exports of goods and services (current LCU)",
"Exports of goods and services (current US$)","Food imports (% of merchandise imports)",
"Goods imports (BoP, current US$)","Imports of goods and services (% of GDP)",
"Imports of goods and services (annual % growth)","Forest area (% of land area)",
"Forest area (sq. km)","Central government debt, total (% of GDP)",
"Central government debt, total (current LCU)","Debt service on external debt, total (TDS, current US$)",
"External debt stocks (% of GNI)","External debt stocks, total (DOD, current US$)",
"Deposit interest rate (%)","Lending interest rate (%)","Real interest rate (%)",
"Renewable energy consumption (% of total final energy consumption)",
"Energy imports, net (% of energy use)","Energy use (kg of oil equivalent per capita)",
"Mortality rate attributed to household and ambient air pollution",
"PM2.5 air pollution, mean annual exposure (micrograms per cubic meter)",
"Population ages 0-14 (% of total population)","Population ages 15-64 (% of total population)",
"Life expectancy at birth, female (years)","Life expectancy at birth, male (years)",
"Life expectancy at birth, total (years)",
"Multidimensional poverty headcount ratio (World Bank) (% of population)",
"Access to electricity (% of population)",
"Official exchange rate (LCU per US$, period average)",
"Broad money (% of GDP)","Broad money growth (annual %)",
"Tax revenue (% of GDP)",
"Taxes on income, profits and capital gains (% of revenue)",
"Taxes on goods and services (% of revenue)",
"Other taxes (% of revenue)"
]))

# =========================================================
# CALCUL SCORE PAYS
# =========================================================

years = [c for c in df.columns if str(c).isdigit()]
latest_year = max(years)

country_data = df[df["Country Name"]==selected_country]
country_data = country_data[country_data["Indicator Name"].isin(indicators)]
country_data["Value"] = country_data[latest_year]

country_data["Score"] = (
country_data["Value"] - country_data["Value"].min()
)/(
country_data["Value"].max()-country_data["Value"].min()+0.0001
)*100

score_global = round(country_data["Score"].mean(),2)
poids_region = importance_regions[selected_zone]["poids"]
score_ifc = round(score_global*(1+poids_region/100),2)

col1,col2=st.columns(2)
col1.metric("Score Pays",score_global)
col2.metric("Score Ajusté IFC",score_ifc)

# =========================================================
# ANALYSE AVANCEE PAR ZONE
# =========================================================

st.markdown("---")
st.header(f"Analyse Avancée - {selected_zone}")

zone_countries = countries_df[countries_df["Zone"]==selected_zone]["Pays"]

zone_results = []

for country in zone_countries:
    d=df[df["Country Name"]==country]
    d=d[d["Indicator Name"].isin(indicators)]
    d["Value"]=d[latest_year]
    d["Score"]=(d["Value"]-d["Value"].min())/(d["Value"].max()-d["Value"].min()+0.0001)*100
    zone_results.append([country,d["Score"].mean()])

zone_df = pd.DataFrame(zone_results,columns=["Pays","Score"]).sort_values("Score",ascending=False)

st.subheader("Classement des pays de la zone")
st.dataframe(zone_df,use_container_width=True)

fig,ax=plt.subplots(figsize=(8,5))
ax.barh(zone_df["Pays"],zone_df["Score"],color=violet_moyen)
ax.invert_yaxis()
st.pyplot(fig)

score_zone = round(zone_df["Score"].mean(),2)
st.metric("Score moyen régional",score_zone)

st.subheader("Comparaison Pays vs Moyenne Zone")

fig,ax=plt.subplots(figsize=(6,4))
ax.bar(["Pays sélectionné","Moyenne Zone"],
       [score_global,score_zone],
       color=[violet_principal,violet_clair])
st.pyplot(fig)

# =========================================================
# CONSULTANCE IFC
# =========================================================

st.markdown("---")
st.header("Consultance IFC - Zone sélectionnée")

consult_df = zone_df.sort_values("Score").head(5)

st.dataframe(consult_df,use_container_width=True)

fig,ax=plt.subplots(figsize=(6,4))
ax.barh(consult_df["Pays"],consult_df["Score"],color=violet_fonce)
ax.invert_yaxis()
st.pyplot(fig)
