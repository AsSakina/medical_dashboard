# -----------------------------------------------------------------------------
# IMPORTATTIONS DES BIBLIOTHÈQUES
# -----------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import altair as alt
import os
import locale
from functools import partial

# -----------------------------------------------------------------------------
# CONFIGURATION INITIALE
# -----------------------------------------------------------------------------

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Medical Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Taux de conversion EUR vers FCFA
TAUX_EUR_FCFA = 655.957

# -----------------------------------------------------------------------------
# GESTION DES LANGUES ET TRADUCTIONS
# -----------------------------------------------------------------------------

# Dictionnaire de traduction pour le support multilingue
translations = {
    "fr": {
        # Titres principaux
        "app_title": "Tableau de Bord Médical",
        "sidebar_title": "Tableau de Bord de suivi",
        "sidebar_subtitle": "Plateforme d'Analyse Médicale Elite",
        "main_header": "TABLEAU DE BORD MÉDICAL",
        "summary_section": "Résumé des Points Importants",
        "alerts_section": "Alertes",
        "recommendations_section": "Recommandations",
        "key_metrics_section": "Métriques Clés",
        "patient_trends_section": "Tendances des Patients",
        "department_performance_section": "Performance des Départements",
        "financial_overview_section": "Aperçu Financier",
        "staff_overview_section": "Aperçu du Personnel",
        "department_quick_view_section": "Vue Rapide des Départements",
        "detailed_data_section": "Données Détaillées",
        
        # Filtres et sélecteurs
        "date_range": "Plage de Dates",
        "department": "Département",
        "all_departments": "Tous",
        "advanced_filters": "Filtres Avancés",
        "treatment_type": "Type de Traitement",
        "patient_outcome": "Résultat Patient",
        
        # Métriques
        "total_patients": "Total Patients",
        "currently_admitted": "Actuellement Hospitalisés",
        "avg_stay_duration": "Durée Moyenne d'Hospitalisation",
        "total_revenue": "Revenu Total",
        "days": "jours",
        "of_total_capacity": "% de la capacité totale",
        "from_previous_period": "% par rapport à la période précédente",
        
        # Graphiques
        "admissions_discharges": "Admissions & Sorties Quotidiennes",
        "patient_distribution": "Distribution des Patients par Département",
        "bed_utilization": "Taux d'Occupation par Département",
        "recovery_rate": "Taux de Rétablissement par Département",
        "revenue_expenses": "Revenus vs Dépenses Quotidiens",
        "department_revenue_cost": "Revenus vs Coûts de Fonctionnement par Département",
        "staff_distribution": "Distribution du Personnel par Rôle",
        "performance_score": "Score de Performance Moyen par Rôle",
        
        # Tableaux de données
        "patient_data": "Données Patients",
        "department_data": "Données Départements",
        "staff_data": "Données Personnel",
        
        # Département et rôles
        "cardiology": "Cardiologie",
        "neurology": "Neurologie",
        "oncology": "Oncologie",
        "pediatrics": "Pédiatrie",
        "emergency": "Urgences",
        "surgery": "Chirurgie",
        "administration": "Administration",
        "doctor": "Médecin",
        "nurse": "Infirmier/ère",
        "technician": "Technicien",
        "administrative": "Administratif",
        "support": "Support",
        
        # Traitements et résultats
        "medication": "Médicaments",
        "surgery_treatment": "Chirurgie",
        "therapy": "Thérapie",
        "observation": "Observation",
        "intensive_care": "Soins Intensifs",
        "recovered": "Rétabli",
        "improved": "Amélioré",
        "stable": "Stable",
        "deteriorated": "Détérioré",
        "deceased": "Décédé",
        "in_treatment": "En Traitement",
        
        # Paramètres et options
        "settings": "Paramètres",
        "language": "Langue",
        "theme": "Thème",
        "currency": "Devise",
        "compact_mode": "Mode Compact",
        "enable_compact": "Activer le mode résumé compact",
        
        # Thèmes
        "dark_gold": "Noir & Or",
        "dark_silver": "Noir & Argent",
        "dark_emerald": "Noir & Émeraude",
        "dark_ruby": "Noir & Rubis",
        "dark_sapphire": "Noir & Saphir",
        
        # Devises
        "eur": "Euro (€)",
        "fcfa": "Franc CFA (FCFA)",
        
        # Divers
        "count": "Nombre",
        "date": "Date",
        "metric": "Métrique",
        "amount": "Montant",
        "department_label": "Département",
        "role": "Rôle",
        "patients": "Patients",
        "bed_utilization_label": "Taux d'Occupation",
        "recovery_rate_label": "Taux de Rétablissement",
        "staff": "Personnel",
        "revenue": "Revenus",
        "expenses": "Dépenses",
        "profit": "Profit",
        "operating_cost": "Coût de Fonctionnement",
        "footer": "Tableau de Bord de Structure de Santé Premium | Créé avec Streamlit"
    },
    "en": {
        # Main titles
        "app_title": "Medical Dashboard",
        ##-------------------Check how to say Dashboard de suivi------------------
        "sidebar_title": "Medical Dashboard",  
        "sidebar_subtitle": "Elite Medical Analytics Platform",
        "main_header": "MEDICAL DASHBOARD",
        "summary_section": "Summary of Key Points",
        "alerts_section": "Alerts",
        "recommendations_section": "Recommendations",
        "key_metrics_section": "Key Metrics",
        "patient_trends_section": "Patient Trends",
        "department_performance_section": "Department Performance",
        "financial_overview_section": "Financial Overview",
        "staff_overview_section": "Staff Overview",
        "department_quick_view_section": "Department Quick View",
        "detailed_data_section": "Detailed Data",
        
        # Filters and selectors
        "date_range": "Date Range",
        "department": "Department",
        "all_departments": "All",
        "advanced_filters": "Advanced Filters",
        "treatment_type": "Treatment Type",
        "patient_outcome": "Patient Outcome",
        
        # Metrics
        "total_patients": "Total Patients",
        "currently_admitted": "Currently Admitted",
        "avg_stay_duration": "Average Stay Duration",
        "total_revenue": "Total Revenue",
        "days": "days",
        "of_total_capacity": "% of total capacity",
        "from_previous_period": "% from previous period",
        
        # Charts
        "admissions_discharges": "Daily Admissions & Discharges",
        "patient_distribution": "Patient Distribution by Department",
        "bed_utilization": "Bed Utilization by Department",
        "recovery_rate": "Recovery Rate by Department",
        "revenue_expenses": "Daily Revenue vs Expenses",
        "department_revenue_cost": "Department Revenue vs Operating Cost",
        "staff_distribution": "Staff Distribution by Role",
        "performance_score": "Average Performance Score by Role",
        
        # Data tables
        "patient_data": "Patient Data",
        "department_data": "Department Data",
        "staff_data": "Staff Data",
        
        # Departments and roles
        "cardiology": "Cardiology",
        "neurology": "Neurology",
        "oncology": "Oncology",
        "pediatrics": "Pediatrics",
        "emergency": "Emergency",
        "surgery": "Surgery",
        "administration": "Administration",
        "doctor": "Doctor",
        "nurse": "Nurse",
        "technician": "Technician",
        "administrative": "Administrative",
        "support": "Support",
        
        # Treatments and outcomes
        "medication": "Medication",
        "surgery_treatment": "Surgery",
        "therapy": "Therapy",
        "observation": "Observation",
        "intensive_care": "Intensive Care",
        "recovered": "Recovered",
        "improved": "Improved",
        "stable": "Stable",
        "deteriorated": "Deteriorated",
        "deceased": "Deceased",
        "in_treatment": "In Treatment",
        
        # Settings and options
        "settings": "Settings",
        "language": "Language",
        "theme": "Theme",
        "currency": "Currency",
        "compact_mode": "Compact Mode",
        "enable_compact": "Enable compact summary mode",
        
        # Themes
        "dark_gold": "Dark & Gold",
        "dark_silver": "Dark & Silver",
        "dark_emerald": "Dark & Emerald",
        "dark_ruby": "Dark & Ruby",
        "dark_sapphire": "Dark & Sapphire",
        
        # Currencies
        "eur": "Euro (€)",
        "fcfa": "CFA Franc (FCFA)",
        
        # Miscellaneous
        "count": "Count",
        "date": "Date",
        "metric": "Metric",
        "amount": "Amount",
        "department_label": "Department",
        "role": "Role",
        "patients": "Patients",
        "bed_utilization_label": "Bed Utilization",
        "recovery_rate_label": "Recovery Rate",
        "staff": "Staff",
        "revenue": "Revenue",
        "expenses": "Expenses",
        "profit": "Profit",
        "operating_cost": "Operating Cost",
        "footer": "Premium Healthcare Dashboard | Created with Streamlit"
    }
}

# -----------------------------------------------------------------------------
# DÉFINITION DES THÈMES ET PALETTES DE COULEURS
# -----------------------------------------------------------------------------

# Définition des thèmes disponibles
themes = {
    "dark_gold": {
        "name": "Noir & Or",
        "bg_color": "#121212",  # Noir profond pour le fond
        "card_bg": "#1E1E1E",  # Noir légèrement plus clair pour les cartes
        "primary_color": "#D4AF37",  # Or pour les accents principaux
        "secondary_color": "#C0C0C0",  # Argent pour les éléments secondaires
        "accent_color": "#9D8221",  # Or foncé pour certains accents
        "text_color": "#E0E0E0",  # Blanc cassé pour le texte principal
        "text_muted": "#A0A0A0",  # Gris clair pour le texte secondaire
        "success_color": "#4CAF50",  # Vert pour les indicateurs positifs
        "warning_color": "#FFC107",  # Ambre pour les avertissements
        "danger_color": "#B71C1C",  # Rouge foncé pour les alertes
        "neutral_color": "#787878",  # Gris neutre
        "border_color": "#2A2A2A",  # Bordure légèrement plus claire que le fond
        "chart_colors": ["#D4AF37", "#C0C0C0", "#9D8221", "#B8860B", "#E6BE8A", "#DAA520", "#A8A8A8"]
    },
    "dark_silver": {
        "name": "Noir & Argent",
        "bg_color": "#0A0A0A",
        "card_bg": "#1A1A1A",
        "primary_color": "#C0C0C0",
        "secondary_color": "#A8A8A8",
        "accent_color": "#D8D8D8",
        "text_color": "#F0F0F0",
        "text_muted": "#B0B0B0",
        "success_color": "#4CAF50",
        "warning_color": "#FFC107",
        "danger_color": "#B71C1C",
        "neutral_color": "#787878",
        "border_color": "#2A2A2A",
        "chart_colors": ["#C0C0C0", "#A8A8A8", "#D8D8D8", "#909090", "#E0E0E0", "#B0B0B0", "#787878"]
    },
    "dark_emerald": {
        "name": "Noir & Émeraude",
        "bg_color": "#0C1414",
        "card_bg": "#162727",
        "primary_color": "#2ECC71",
        "secondary_color": "#1ABC9C",
        "accent_color": "#16A085",
        "text_color": "#E0E0E0",
        "text_muted": "#A0A0A0",
        "success_color": "#27AE60",
        "warning_color": "#F39C12",
        "danger_color": "#C0392B",
        "neutral_color": "#7F8C8D",
        "border_color": "#1E3535",
        "chart_colors": ["#2ECC71", "#1ABC9C", "#16A085", "#27AE60", "#3498DB", "#2980B9", "#7F8C8D"]
    },
    "dark_ruby": {
        "name": "Noir & Rubis",
        "bg_color": "#0E0808",
        "card_bg": "#1A1010",
        "primary_color": "#E74C3C",
        "secondary_color": "#C0392B",
        "accent_color": "#D35400",
        "text_color": "#F0F0F0",
        "text_muted": "#B0B0B0",
        "success_color": "#27AE60",
        "warning_color": "#F39C12",
        "danger_color": "#922B21",
        "neutral_color": "#7F8C8D",
        "border_color": "#2A1515",
        "chart_colors": ["#E74C3C", "#C0392B", "#D35400", "#E67E22", "#F39C12", "#922B21", "#7F8C8D"]
    },
    "dark_sapphire": {
        "name": "Noir & Saphir",
        "bg_color": "#0A0F1A",
        "card_bg": "#141E2E",
        "primary_color": "#3498DB",
        "secondary_color": "#2980B9",
        "accent_color": "#1F618D",
        "text_color": "#E0E0E0",
        "text_muted": "#A0A0A0",
        "success_color": "#27AE60",
        "warning_color": "#F39C12",
        "danger_color": "#C0392B",
        "neutral_color": "#7F8C8D",
        "border_color": "#1E2A3A",
        "chart_colors": ["#3498DB", "#2980B9", "#1F618D", "#2C3E50", "#5DADE2", "#85C1E9", "#7F8C8D"]
    }
}

# -----------------------------------------------------------------------------
# INITIALISATION DES PARAMÈTRES DE SESSION
# -----------------------------------------------------------------------------

# Initialisation des paramètres de session s'ils n'existent pas déjà
if 'language' not in st.session_state:
    st.session_state.language = "en"  # Langue par défaut: Anglais
if 'theme' not in st.session_state:
    st.session_state.theme = "dark_emerald"  # Thème par défaut: Noir & Or
if 'currency' not in st.session_state:
    st.session_state.currency = "fcfa"  # Devise par défaut: FCFA
if 'compact_mode' not in st.session_state:
    st.session_state.compact_mode = False  # Mode compact désactivé par défaut

# Fonction de traduction pour faciliter l'accès aux textes traduits
def t(key):
    """Récupère la traduction d'une clé dans la langue actuelle"""
    return translations[st.session_state.language].get(key, key)

# Fonction pour formater les montants selon la devise choisie
def format_currency(amount, currency=None):
    """
    Formate un montant selon la devise choisie
    
    Args:
        amount: Le montant à formater
        currency: La devise à utiliser (si None, utilise la devise de session)
    
    Returns:
        Le montant formaté avec le symbole de devise approprié
    """
    if currency is None:
        currency = st.session_state.currency
    
    if currency == "fcfa":
        # Convertir de EUR à FCFA si nécessaire et formater
        amount_fcfa = amount * TAUX_EUR_FCFA
        return f"{amount_fcfa:,.0f} FCFA".replace(",", " ")
    else:
        # Format EUR
        return f"{amount:,.0f} €".replace(",", " ")

# -----------------------------------------------------------------------------
# GÉNÉRATION DES STYLES CSS BASÉS SUR LE THÈME ACTUEL
# -----------------------------------------------------------------------------

# Récupération du thème actuel
current_theme = themes[st.session_state.theme]

# Génération du CSS personnalisé basé sur le thème actuel
custom_css = f"""
<style>
    /* Styles globaux */
    .stApp {{
        background-color: {current_theme["bg_color"]};
        color: {current_theme["text_color"]};
    }}
    
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {current_theme["primary_color"]};
        margin-bottom: 1.5rem;
        text-align: center;
        text-shadow: 0px 2px 3px rgba(0,0,0,0.3);
        letter-spacing: 1px;
    }}
    
    .sub-header {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {current_theme["secondary_color"]};
        margin-bottom: 1.5rem;
        border-bottom: 2px solid {current_theme["primary_color"]};
        padding-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }}
    
    /* Cartes métriques */
    .metric-card {{
        background-color: {current_theme["card_bg"]};
        border-radius: 0.5rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1.5rem;
        border-top: 3px solid {current_theme["primary_color"]};
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {current_theme["primary_color"]};
        text-shadow: 0px 1px 2px rgba(0,0,0,0.2);
    }}
    
    .metric-label {{
        font-size: 0.9rem;
        color: {current_theme["text_muted"]};
        font-weight: 500;
        letter-spacing: 0.5px;
    }}
    
    .positive-change {{
        color: {current_theme["success_color"]};
    }}
    
    .negative-change {{
        color: {current_theme["danger_color"]};
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {current_theme["bg_color"]};
        border-right: 1px solid {current_theme["border_color"]};
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdown"] {{
        color: {current_theme["text_color"]};
    }}
    
    /* Cartes département */
    .department-card {{
        background-color: {current_theme["card_bg"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        border-left: 4px solid {current_theme["primary_color"]};
        transition: transform 0.2s ease;
    }}
    
    .department-card:hover {{
        transform: translateY(-3px);
    }}
    
    .department-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {current_theme["primary_color"]};
        margin-bottom: 0.75rem;
        letter-spacing: 0.5px;
    }}
    
    .department-metric {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid {current_theme["border_color"]};
        padding-bottom: 0.25rem;
    }}
    
    .department-metric-label {{
        color: {current_theme["text_muted"]};
        font-size: 0.85rem;
    }}
    
    .department-metric-value {{
        font-weight: 600;
        color: {current_theme["secondary_color"]};
    }}
    
    /* Alertes */
    .alert-card {{
        background-color: rgba(255, 193, 7, 0.15);
        border-left: 4px solid {current_theme["warning_color"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }}
    
    .alert-card-critical {{
        background-color: rgba(183, 28, 28, 0.15);
        border-left: 4px solid {current_theme["danger_color"]};
    }}
    
    .alert-title {{
        font-weight: 600;
        color: {current_theme["warning_color"]};
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }}
    
    .alert-title-critical {{
        color: {current_theme["danger_color"]};
    }}
    
    .alert-message {{
        color: #D6C08D;
        font-size: 0.9rem;
    }}
    
    .alert-message-critical {{
        color: #E57373;
    }}
    
    /* Recommandations */
    .recommendation-card {{
        background-color: rgba(212, 175, 55, 0.1);
        border-left: 4px solid {current_theme["primary_color"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }}
    
    .recommendation-title {{
        font-weight: 600;
        color: {current_theme["primary_color"]};
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }}
    
    .recommendation-message {{
        color: {current_theme["secondary_color"]};
        font-size: 0.9rem;
    }}
    
    /* Résumé */
    .summary-card {{
        background-color: rgba(192, 192, 192, 0.1);
        border-left: 4px solid {current_theme["secondary_color"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }}
    
    .summary-title {{
        font-weight: 600;
        color: {current_theme["secondary_color"]};
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }}
    
    .summary-message {{
        color: {current_theme["text_color"]};
        font-size: 0.9rem;
    }}
    
    /* Tableaux */
    [data-testid="stTable"] {{
        background-color: {current_theme["card_bg"]};
    }}
    
    div[data-testid="stVerticalBlock"] > div:has(div.block-container) {{
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {current_theme["card_bg"]};
        color: {current_theme["text_muted"]};
        border-radius: 4px 4px 0 0;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {current_theme["primary_color"]} !important;
        color: #000 !important;
    }}
    
    /* Inputs et sélecteurs */
    [data-testid="stDateInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stMultiselect"] label {{
        color: {current_theme["secondary_color"]} !important;
    }}
    
    /* Scrollbar personnalisée */
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {current_theme["bg_color"]};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {current_theme["border_color"]};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {current_theme["primary_color"]};
    }}
    
    /* Paramètres */
    .settings-card {{
        background-color: {current_theme["card_bg"]};
        border-radius: 0.5rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-left: 4px solid {current_theme["secondary_color"]};
    }}
    
    .settings-title {{
        font-weight: 600;
        color: {current_theme["secondary_color"]};
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }}
    
    /* Mode compact */
    .compact-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
    }}
    
    .compact-card {{
        background-color: {current_theme["card_bg"]};
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        height: 100%;
    }}
    
    .compact-title {{
        font-size: 1rem;
        font-weight: 600;
        color: {current_theme["primary_color"]};
        margin-bottom: 0.5rem;
        border-bottom: 1px solid {current_theme["border_color"]};
        padding-bottom: 0.25rem;
    }}
</style>
"""

# Appliquer le CSS personnalisé
st.markdown(custom_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GÉNÉRATION DES DONNÉES D'EXEMPLE
# -----------------------------------------------------------------------------

def generer_donnees_exemple():
    """
    Génère des données d'exemple pour le tableau de bord
    
    Returns:
        tuple: (patients_df, personnel_df, departements_df, quotidien_df)
    """
    # Traduire les noms de départements selon la langue actuelle
    departements = [
        t("cardiology"), t("neurology"), t("oncology"), 
        t("pediatrics"), t("emergency"), t("surgery")
    ]
    
    traitements = [
        t("medication"), t("surgery_treatment"), t("therapy"), 
        t("observation"), t("intensive_care")
    ]
    
    resultats = [
        t,  t("therapy"), 
        t("observation"), t("intensive_care") ]
    
    
    resultats = [
        t("recovered"), t("improved"), t("stable"), 
        t("deteriorated"), t("deceased"), t("in_treatment")
    ]
    
    # Données des patients
    patients = pd.DataFrame({
        'idPatient': [f'P{1000+i}' for i in range(1000)],
        'age': np.random.randint(1, 95, 1000),
        'sexe': np.random.choice(['Homme', 'Femme'], 1000),
        'departement': np.random.choice(departements, 1000),
        'dateAdmission': [datetime.now() - timedelta(days=np.random.randint(1, 90)) for _ in range(1000)],
        'dureeHospitalisation': np.random.randint(1, 30, 1000),
        'traitement': np.random.choice(traitements, 1000),
        'resultat': np.random.choice(resultats, 1000),
        'coutTraitement': np.random.randint(1000, 20000, 1000),
        'couvertureAssurance': np.random.randint(500, 15000, 1000),
        'estHospitalise': np.random.choice([True, False], 1000, p=[0.3, 0.7])
    })
    
    # Calculer la date de sortie en fonction de la date d'admission et de la durée d'hospitalisation
    patients['dateSortie'] = patients.apply(
        lambda x: None if x['estHospitalise'] else x['dateAdmission'] + timedelta(days=x['dureeHospitalisation']), 
        axis=1
    )
    
    # Données du personnel
    roles = [t("doctor"), t("nurse"), t("technician"), t("administrative"), t("support")]
    personnel = pd.DataFrame({
        'idPersonnel': [f'S{1000+i}' for i in range(200)],
        'departement': np.random.choice(departements + [t("administration")], 200),
        'role': np.random.choice(roles, 200),
        'anneeService': np.random.randint(0, 30, 200),
        'salaire': np.random.randint(40000, 200000, 200),
        'patientsTraites': np.random.randint(0, 100, 200),
        'scorePerformance': np.random.uniform(0.7, 1.0, 200)
    })
    
    # Données des départements
    departements_df = pd.DataFrame({
        'departement': departements,
        'totalPatients': np.random.randint(100, 300, 6),
        'dureeHospitalisationMoyenne': np.random.uniform(3, 15, 6),
        'revenusTotal': np.random.randint(500000, 2000000, 6),
        'totalSalaires': np.random.randint(300000, 1000000, 6),
        'coutFonctionnement': np.random.randint(400000, 1500000, 6),
        'tauxRetablissement': np.random.uniform(0.6, 0.95, 6),
        'litsDisponibles': [50, 40, 60, 45, 30, 35],
        'patientsActuels': np.random.randint(10, 50, 6),
        'nombrePersonnel': np.random.randint(20, 60, 6),
        'nombreMedecins': np.random.randint(5, 20, 6),
        'nombreInfirmiers': np.random.randint(10, 30, 6)
    })
    
    departements_df['tauxOccupation'] = departements_df['patientsActuels'] / departements_df['litsDisponibles']
    
    # Métriques quotidiennes
    dates = [datetime.now() - timedelta(days=i) for i in range(90)]
    quotidien = pd.DataFrame({
        'date': dates,
        'nouvellesAdmissions': np.random.randint(5, 25, 90),
        'sorties': np.random.randint(5, 20, 90),
        'visiteUrgences': np.random.randint(20, 60, 90),
        'operations': np.random.randint(3, 15, 90),
        'revenus': np.random.randint(50000, 150000, 90),
        'depenses': np.random.randint(40000, 120000, 90)
    })
    
    return patients, personnel, departements_df, quotidien

# -----------------------------------------------------------------------------
# CHARGEMENT DES DONNÉES
# -----------------------------------------------------------------------------

@st.cache_data
def charger_donnees():
    """
    Charge les données depuis des fichiers JSON ou génère des données d'exemple
    
    Returns:
        tuple: (patients_df, personnel_df, departements_df, quotidien_df)
    """
    try:
        # Essayer de charger à partir des fichiers JSON s'ils existent
        if os.path.exists('./data/patients.json'):
            # Code pour charger les données depuis les fichiers JSON
            # Omis pour la brièveté - utiliser le code de génération de données à la place
            return generer_donnees_exemple()
        else:
            # Si les fichiers n'existent pas, générer des données d'exemple
            st.info("Fichiers de données non trouvés. Utilisation de données d'exemple générées.")
            return generer_donnees_exemple()
    except Exception as e:
        st.warning(f"Erreur lors du chargement des données: {e}. Utilisation de données d'exemple générées.")
        return generer_donnees_exemple()

# Charger les données
patients_df, personnel_df, departements_df, quotidien_df = charger_donnees()

# -----------------------------------------------------------------------------
# BARRE LATÉRALE ET PARAMÈTRES
# -----------------------------------------------------------------------------

# Barre latérale
# st.sidebar.image("https://img.icons8.com/color/96/000000/hospital-3.png", width=80)
st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown(f"<div style='color: {current_theme['primary_color']}; margin-bottom: 20px; font-weight: 500;'>{t('sidebar_subtitle')}</div>", unsafe_allow_html=True)

# Section des paramètres
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='color: {current_theme['secondary_color']}; font-weight: 500;'>{t('settings')}</div>", unsafe_allow_html=True)

# Sélection de la langue
language_options = {"fr": "Français", "en": "English"}
selected_language = st.sidebar.selectbox(
    t("language"),
    options=list(language_options.keys()),
    format_func=lambda x: language_options[x],
    index=list(language_options.keys()).index(st.session_state.language)
)

if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()

# Sélection du thème
theme_options = {k: v["name"] for k, v in themes.items()}
selected_theme = st.sidebar.selectbox(
    t("theme"),
    options=list(theme_options.keys()),
    format_func=lambda x: theme_options[x],
    index=list(theme_options.keys()).index(st.session_state.theme)
)

if selected_theme != st.session_state.theme:
    st.session_state.theme = selected_theme
    st.rerun()

# Sélection de la devise
currency_options = {"eur": t("eur"), "fcfa": t("fcfa")}
selected_currency = st.sidebar.selectbox(
    t("currency"),
    options=list(currency_options.keys()),
    format_func=lambda x: currency_options[x],
    index=list(currency_options.keys()).index(st.session_state.currency)
)

if selected_currency != st.session_state.currency:
    st.session_state.currency = selected_currency
    st.rerun()

# Option de mode compact
compact_mode = st.sidebar.checkbox(
    t("enable_compact"),
    value=st.session_state.compact_mode
)

if compact_mode != st.session_state.compact_mode:
    st.session_state.compact_mode = compact_mode
    st.rerun()

# Séparateur
st.sidebar.markdown("---")

# Filtres
# Filtre de date
min_date = quotidien_df['date'].min().date()
max_date = quotidien_df['date'].max().date()
plage_date = st.sidebar.date_input(
    t("date_range"),
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filtre de département
tous_departements = [t("all_departments")] + list(departements_df['departement'].unique())
departement_selectionne = st.sidebar.selectbox(t("department"), tous_departements)

# Filtres supplémentaires
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='color: {current_theme['secondary_color']}; font-weight: 500;'>{t('advanced_filters')}</div>", unsafe_allow_html=True)
filtre_traitement = st.sidebar.multiselect(
    t("treatment_type"),
    options=patients_df['traitement'].unique(),
    default=[]
)

filtre_resultat = st.sidebar.multiselect(
    t("patient_outcome"),
    options=patients_df['resultat'].unique(),
    default=[]
)

# -----------------------------------------------------------------------------
# APPLICATION DES FILTRES
# -----------------------------------------------------------------------------

# Appliquer les filtres
if len(plage_date) == 2: 
    date_debut, date_fin = plage_date
    # Convertir en datetime pour une comparaison correcte
    date_debut_dt = pd.Timestamp(date_debut)
    date_fin_dt = pd.Timestamp(date_fin)
    quotidien_filtre = quotidien_df[(quotidien_df['date'] >= date_debut_dt) & (quotidien_df['date'] <= date_fin_dt)]
else:
    quotidien_filtre = quotidien_df
    # Par défaut à la plage complète si plage_date n'est pas correctement définie
    date_debut = min_date
    date_fin = max_date

# Appliquer le filtre de département
if departement_selectionne != t("all_departments"):
    patients_filtre = patients_df[patients_df['departement'] == departement_selectionne]
    personnel_filtre = personnel_df[personnel_df['departement'] == departement_selectionne]
    departements_filtre = departements_df[departements_df['departement'] == departement_selectionne]
else:
    patients_filtre = patients_df
    personnel_filtre = personnel_df
    departements_filtre = departements_df

# Appliquer le filtre de traitement
if filtre_traitement:
    patients_filtre = patients_filtre[patients_filtre['traitement'].isin(filtre_traitement)]

# Appliquer le filtre de résultat
if filtre_resultat:
    patients_filtre = patients_filtre[patients_filtre['resultat'].isin(filtre_resultat)]

# -----------------------------------------------------------------------------
# FONCTIONS D'ANALYSE ET DE GÉNÉRATION D'INSIGHTS
# -----------------------------------------------------------------------------

def generer_alertes(departements, patients, quotidien):
    """
    Génère des alertes basées sur les données
    
    Args:
        departements: DataFrame des départements
        patients: DataFrame des patients
        quotidien: DataFrame des métriques quotidiennes
    
    Returns:
        list: Liste d'alertes avec titre, message, département et type
    """
    alertes = []
    
    # Alertes critiques
    for _, dept in departements.iterrows():
        # Alerte de taux d'occupation élevé
        if dept['tauxOccupation'] > 0.9:
            alertes.append({
                'titre': f"Taux d'occupation critique en {dept['departement']}",
                'message': f"Le taux d'occupation des lits est de {dept['tauxOccupation']*100:.1f}% ({dept['patientsActuels']} patients pour {dept['litsDisponibles']} lits).",
                'departement': dept['departement'],
                'type': 'critique'
            })
        
        # Alerte de taux de rétablissement faible
        if dept['tauxRetablissement'] < 0.7:
            alertes.append({
                'titre': f"Taux de rétablissement faible en {dept['departement']}",
                'message': f"Le taux de rétablissement est de seulement {dept['tauxRetablissement']*100:.1f}%, ce qui est inférieur à l'objectif de 70%.",
                'departement': dept['departement'],
                'type': 'critique'
            })
        
        # Alerte de ratio personnel/patients
        ratio_medecins = dept['nombreMedecins'] / max(1, dept['patientsActuels'])
        if ratio_medecins < 0.1:  # Moins de 1 médecin pour 10 patients
            alertes.append({
                'titre': f"Manque de médecins en {dept['departement']}",
                'message': f"Ratio médecin/patients de 1:{int(1/ratio_medecins)}, ce qui est inférieur aux recommandations.",
                'departement': dept['departement'],
                'type': 'critique'
            })
    
    # Alertes générales
    # Tendance d'admissions vs sorties
    if len(quotidien) >= 7:  # Au moins une semaine de données
        derniere_semaine = quotidien.sort_values('date').tail(7)
        admissions = derniere_semaine['nouvellesAdmissions'].sum()
        sorties = derniere_semaine['sorties'].sum()
        if admissions > sorties * 1.3:  # 30% plus d'admissions que de sorties
            alertes.append({
                'titre': "Déséquilibre admissions/sorties",
                'message': f"Sur les 7 derniers jours, il y a eu {admissions} admissions pour seulement {sorties} sorties, ce qui indique une pression croissante sur les capacités.",
                'departement': 'Tous',
                'type': 'avertissement'
            })
    
    # Alerte financière
    if len(quotidien) >= 30:  # Au moins un mois de données
        dernier_mois = quotidien.sort_values('date').tail(30)
        revenus = dernier_mois['revenus'].sum()
        depenses = dernier_mois['depenses'].sum()
        if depenses > revenus:
            alertes.append({
                'titre': "Déficit financier",
                'message': f"Sur les 30 derniers jours, les dépenses ({format_currency(depenses)}) ont dépassé les revenus ({format_currency(revenus)}), créant un déficit de {format_currency(depenses-revenus)}.",
                'departement': 'Tous',
                'type': 'avertissement'
            })
    
    return alertes

def generer_recommandations(departements, patients, personnel, alertes):
    """
    Génère des recommandations basées sur les données et les alertes
    
    Args:
        departements: DataFrame des départements
        patients: DataFrame des patients
        personnel: DataFrame du personnel
        alertes: Liste des alertes générées
    
    Returns:
        list: Liste de recommandations avec titre et message
    """
    recommandations = []
    
    # Recommandations basées sur les alertes
    alertes_occupation = [a for a in alertes if "occupation" in a['titre'].lower()]
    if alertes_occupation:
        depts_concernes = [a['departement'] for a in alertes_occupation]
        recommandations.append({
            'titre': "Optimisation de la capacité d'accueil",
            'message': f"Envisager d'augmenter la capacité en lits dans les départements suivants : {', '.join(depts_concernes)}. Alternativement, mettre en place un système de transfert vers d'autres établissements pour les cas non urgents."
        })
    
    # Recommandations pour l'amélioration des taux de rétablissement
    alertes_retablissement = [a for a in alertes if "rétablissement" in a['titre'].lower()]
    if alertes_retablissement:
        depts_concernes = [a['departement'] for a in alertes_retablissement]
        recommandations.append({
            'titre': "Amélioration des taux de rétablissement",
            'message': f"Analyser les protocoles de traitement dans les départements suivants : {', '.join(depts_concernes)}. Envisager une révision des protocoles de soins et une formation supplémentaire du personnel."
        })
    
    # Recommandations pour l'optimisation du personnel
    alertes_personnel = [a for a in alertes if "médecins" in a['titre'].lower() or "personnel" in a['titre'].lower()]
    if alertes_personnel:
        depts_concernes = [a['departement'] for a in alertes_personnel]
        recommandations.append({
            'titre': "Optimisation des ressources humaines",
            'message': f"Recruter du personnel supplémentaire ou réaffecter temporairement du personnel vers les départements suivants : {', '.join(depts_concernes)}. Envisager également des heures supplémentaires pour le personnel existant."
        })
    
    # Recommandations financières
    alertes_financieres = [a for a in alertes if "financier" in a['titre'].lower() or "déficit" in a['titre'].lower()]
    if alertes_financieres:
        recommandations.append({
            'titre': "Optimisation financière",
            'message': "Revoir la structure des coûts et identifier les postes de dépenses à optimiser. Envisager une révision des tarifs pour certains services spécialisés."
        })
    
    # Recommandations générales basées sur les données
    # Recommandation sur la durée d'hospitalisation
    duree_moyenne = patients['dureeHospitalisation'].mean()
    if duree_moyenne > 10:  # Si la durée moyenne est supérieure à 10 jours
        recommandations.append({
            'titre': "Réduction de la durée d'hospitalisation",
            'message': f"La durée moyenne d'hospitalisation est de {duree_moyenne:.1f} jours. Mettre en place des protocoles de sortie anticipée pour les patients stables et développer les soins ambulatoires."
        })
    
    # Recommandation sur l'équilibre des départements
    dept_counts = patients['departement'].value_counts()
    if len(dept_counts) > 1:  # S'assurer qu'il y a au moins deux départements
        max_dept = dept_counts.idxmax()
        min_dept = dept_counts.idxmin()
        if dept_counts.max() > 3 * dept_counts.min():  # Si un département a 3 fois plus de patients qu'un autre
            recommandations.append({
                'titre': "Rééquilibrage des ressources entre départements",
                'message': f"Le département {max_dept} traite significativement plus de patients que le département {min_dept}. Envisager une redistribution des ressources et du personnel."
            })
    
    return recommandations

def generer_resume(departements, patients, quotidien, alertes):
    """
    Génère un résumé des points importants basé sur les données
    
    Args:
        departements: DataFrame des départements
        patients: DataFrame des patients
        quotidien: DataFrame des métriques quotidiennes
        alertes: Liste des alertes générées
    
    Returns:
        list: Liste de résumés avec titre et message
    """
    resume = []
    
    # Statistiques générales
    total_patients = len(patients)
    patients_hospitalises = len(patients[patients['estHospitalise']])
    taux_occupation_moyen = departements['tauxOccupation'].mean()
    taux_retablissement_moyen = departements['tauxRetablissement'].mean()
    
    resume.append({
        'titre': "Vue d'ensemble",
        'message': f"L'établissement a traité {total_patients} patients, dont {patients_hospitalises} sont actuellement hospitalisés. Le taux d'occupation moyen est de {taux_occupation_moyen*100:.1f}% et le taux de rétablissement moyen est de {taux_retablissement_moyen*100:.1f}%."
    })
    
    # Département le plus performant
    if not departements.empty:
        dept_performance = departements.copy()
        dept_performance['score'] = dept_performance['tauxRetablissement'] * 0.6 + (1 - dept_performance['tauxOccupation']) * 0.4
        meilleur_dept = dept_performance.loc[dept_performance['score'].idxmax()]
        
        resume.append({
            'titre': "Département le plus performant",
            'message': f"Le département de {meilleur_dept['departement']} présente les meilleurs indicateurs avec un taux de rétablissement de {meilleur_dept['tauxRetablissement']*100:.1f}% et un taux d'occupation équilibré de {meilleur_dept['tauxOccupation']*100:.1f}%."
        })
    
    # Tendances financières
    if len(quotidien) >= 30:
        dernier_mois = quotidien.sort_values('date').tail(30)
        revenus_total = dernier_mois['revenus'].sum()
        depenses_total = dernier_mois['depenses'].sum()
        profit = revenus_total - depenses_total
        
        resume.append({
            'titre': "Situation financière",
            'message': f"Sur les 30 derniers jours, l'établissement a généré {format_currency(revenus_total)} de revenus pour {format_currency(depenses_total)} de dépenses, résultant en {'un profit' if profit >= 0 else 'une perte'} de {format_currency(abs(profit))}."
        })
    
    # Résumé des alertes
    if alertes:
        alertes_critiques = len([a for a in alertes if a['type'] == 'critique'])
        alertes_avertissement = len([a for a in alertes if a['type'] == 'avertissement'])
        
        resume.append({
            'titre': "Points d'attention",
            'message': f"Le système a identifié {alertes_critiques} alertes critiques et {alertes_avertissement} avertissements qui nécessitent une attention particulière."
        })
    
    return resume

# -----------------------------------------------------------------------------
# GÉNÉRATION DES INSIGHTS
# -----------------------------------------------------------------------------

# Générer alertes, recommandations et résumé
alertes = generer_alertes(departements_filtre, patients_filtre, quotidien_filtre)
recommandations = generer_recommandations(departements_filtre, patients_filtre, personnel_filtre, alertes)
resume = generer_resume(departements_filtre, patients_filtre, quotidien_filtre, alertes)

# -----------------------------------------------------------------------------
# AFFICHAGE DU TABLEAU DE BORD
# -----------------------------------------------------------------------------

# Titre principal
st.markdown(f'<div class="main-header">{t("main_header")}</div>', unsafe_allow_html=True)

# Mode compact (résumé sans défilement)
if st.session_state.compact_mode:
    # Affichage du mode compact
    st.markdown(f'<div class="sub-header">{t("summary_section")}</div>', unsafe_allow_html=True)
    
    # Grille de résumé compact
    st.markdown('<div class="compact-grid">', unsafe_allow_html=True)
    
    # Métriques clés
    total_patients = len(patients_filtre)
    patients_actuels = len(patients_filtre[patients_filtre['estHospitalise']])
    duree_moyenne = patients_filtre['dureeHospitalisation'].mean()
    revenu_total = patients_filtre['coutTraitement'].sum()
    
    # Colonne 1: Métriques clés
    st.markdown(f"""
    <div class="compact-card">
        <div class="compact-title">{t("key_metrics_section")}</div>
        <div class="metric-value">{total_patients:,}</div>
        <div class="metric-label">{t("total_patients")}</div>
        <hr style="border-color: {current_theme['border_color']}; margin: 0.5rem 0;">
        <div class="metric-value">{patients_actuels:,}</div>
        <div class="metric-label">{t("currently_admitted")}</div>
        <hr style="border-color: {current_theme['border_color']}; margin: 0.5rem 0;">
        <div class="metric-value">{duree_moyenne:.1f}</div>
        <div class="metric-label">{t("avg_stay_duration")} ({t("days")})</div>
        <hr style="border-color: {current_theme['border_color']}; margin: 0.5rem 0;">
        <div class="metric-value">{format_currency(revenu_total)}</div>
        <div class="metric-label">{t("total_revenue")}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Colonne 2: Alertes critiques
    alertes_critiques = [a for a in alertes if a['type'] == 'critique']
    st.markdown(f"""
    <div class="compact-card">
        <div class="compact-title">{t("alerts_section")}</div>
        {"".join([f'<div style="color: {current_theme["danger_color"]}; margin-bottom: 0.5rem; font-weight: 600;">{a["titre"]}</div>' for a in alertes_critiques[:3]])}
        {f'<div style="color: {current_theme["text_muted"]}; font-size: 0.8rem;">+ {len(alertes_critiques) - 3} autres alertes critiques</div>' if len(alertes_critiques) > 3 else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Colonne 3: Recommandations principales
    st.markdown(f"""
    <div class="compact-card">
        <div class="compact-title">{t("recommendations_section")}</div>
        {"".join([f'<div style="color: {current_theme["primary_color"]}; margin-bottom: 0.5rem; font-weight: 600;">{r["titre"]}</div>' for r in recommandations[:3]])}
        {f'<div style="color: {current_theme["text_muted"]}; font-size: 0.8rem;">+ {len(recommandations) - 3} autres recommandations</div>' if len(recommandations) > 3 else ''}
    </div>
    """, unsafe_allow_html=True)
    
    # Colonne 4: Résumé financier
    if len(quotidien_filtre) > 0:
        revenus_total = quotidien_filtre['revenus'].sum()
        depenses_total = quotidien_filtre['depenses'].sum()
        profit = revenus_total - depenses_total
        profit_color = current_theme["success_color"] if profit >= 0 else current_theme["danger_color"]
        
        st.markdown(f"""
        <div class="compact-card">
            <div class="compact-title">{t("financial_overview_section")}</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: {current_theme["text_muted"]};">{t("revenue")}:</span>
                <span style="color: {current_theme["success_color"]}; font-weight: 600;">{format_currency(revenus_total)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: {current_theme["text_muted"]};">{t("expenses")}:</span>
                <span style="color: {current_theme["danger_color"]}; font-weight: 600;">{format_currency(depenses_total)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: {current_theme["text_muted"]};">{t("profit")}:</span>
                <span style="color: {profit_color}; font-weight: 600;">{format_currency(profit)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Fermer la grille
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques compacts
    st.markdown('<div class="compact-grid" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # Graphique 1: Admissions et sorties
    if len(quotidien_filtre) > 0:
        fig = px.line(quotidien_filtre, x='date', y=['nouvellesAdmissions', 'sorties'], 
                     title=t("admissions_discharges"),
                     labels={'value': t("count"), 'date': t("date"), 'variable': t("metric")},
                     color_discrete_map={'nouvellesAdmissions': current_theme["primary_color"], 'sorties': current_theme["accent_color"]})
        fig.update_layout(
            height=250,
            legend_title_text='', 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor=current_theme["card_bg"],
            paper_bgcolor=current_theme["card_bg"],
            font=dict(color=current_theme["text_color"]),
            xaxis=dict(gridcolor=current_theme["border_color"]),
            yaxis=dict(gridcolor=current_theme["border_color"]),
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Graphique 2: Taux d'occupation par département
    if not departements_filtre.empty:
        fig = px.bar(departements_filtre, x='departement', y='tauxOccupation', 
                    title=t("bed_utilization"),
                    labels={'tauxOccupation': t("bed_utilization_label"), 'departement': t("department_label")},
                    #color='departement  'departement': t("department_label")},
                    color='departement',
                    color_discrete_map={dept: color for dept, color in zip(departements_filtre['departement'], current_theme["chart_colors"])})
        fig.update_layout(
            height=250,
            coloraxis_showscale=False,
            plot_bgcolor=current_theme["card_bg"],
            paper_bgcolor=current_theme["card_bg"],
            font=dict(color=current_theme["text_color"]),
            xaxis=dict(gridcolor=current_theme["border_color"]),
            yaxis=dict(gridcolor=current_theme["border_color"]),
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig.update_yaxes(range=[0, 1], tickformat='.0%')
        st.plotly_chart(fig, use_container_width=True)
    
    # Fermer la grille
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tableau des départements
    st.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
    st.markdown(f'<div class="compact-title">{t("department_quick_view_section")}</div>', unsafe_allow_html=True)
    
    # Créer une grille pour les départements
    if not departements_filtre.empty:
        dept_data = departements_filtre.copy()
        dept_data = dept_data.sort_values('totalPatients', ascending=False)
        
        cols = st.columns(min(3, len(dept_data)))
        for i, dept in enumerate(dept_data.iterrows()):
            dept = dept[1]  # Accéder aux données
            with cols[i % 3]:
                st.markdown(f"""
                <div class="department-card" style="border-left: 4px solid {current_theme["chart_colors"][i % len(current_theme["chart_colors"])]}">
                    <div class="department-title">{dept['departement']}</div>
                    <div class="department-metric">
                        <span class="department-metric-label">{t("patients")}:</span>
                        <span class="department-metric-value">{dept['totalPatients']}</span>
                    </div>
                    <div class="department-metric">
                        <span class="department-metric-label">{t("bed_utilization_label")}:</span>
                        <span class="department-metric-value">{dept['tauxOccupation']*100:.1f}%</span>
                    </div>
                    <div class="department-metric">
                        <span class="department-metric-label">{t("recovery_rate_label")}:</span>
                        <span class="department-metric-value">{dept['tauxRetablissement']*100:.1f}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Affichage du mode standard avec défilement
    
    # Afficher le résumé en haut
    st.markdown(f'<div class="sub-header">{t("summary_section")}</div>', unsafe_allow_html=True)
    
    for item in resume:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-title">{item['titre']}</div>
            <div class="summary-message">{item['message']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Afficher les alertes
    if alertes:
        st.markdown(f'<div class="sub-header">{t("alerts_section")}</div>', unsafe_allow_html=True)
        
        # Trier les alertes par type (critiques d'abord)
        alertes_triees = sorted(alertes, key=lambda x: 0 if x['type'] == 'critique' else 1)
        
        for alerte in alertes_triees:
            est_critique = alerte['type'] == 'critique'
            st.markdown(f"""
            <div class="alert-card {'alert-card-critical' if est_critique else ''}">
                <div class="alert-title {'alert-title-critical' if est_critique else ''}">{alerte['titre']}</div>
                <div class="alert-message {'alert-message-critical' if est_critique else ''}">{alerte['message']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Afficher les recommandations
    if recommandations:
        st.markdown(f'<div class="sub-header">{t("recommendations_section")}</div>', unsafe_allow_html=True)
        
        for recommandation in recommandations:
            st.markdown(f"""
            <div class="recommendation-card">
                <div class="recommendation-title">{recommandation['titre']}</div>
                <div class="recommendation-message">{recommandation['message']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Métriques principales
    st.markdown(f'<div class="sub-header">{t("key_metrics_section")}</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculer les métriques
    total_patients = len(patients_filtre)
    patients_actuels = len(patients_filtre[patients_filtre['estHospitalise']])
    duree_moyenne = patients_filtre['dureeHospitalisation'].mean()
    revenu_total = patients_filtre['coutTraitement'].sum()
    
    # Calculer les changements par rapport à la période précédente
    jours_periode_prec = (date_fin - date_debut).days
    debut_prec = date_debut - timedelta(days=jours_periode_prec)
    fin_prec = date_debut - timedelta(days=1)
    
    # Convertir en datetime pour une comparaison correcte
    debut_prec_dt = pd.Timestamp(debut_prec)
    fin_prec_dt = pd.Timestamp(fin_prec)
    
    # Filtrer les patients pour la période précédente
    patients_prec = len(patients_df[(patients_df['dateAdmission'] >= debut_prec_dt) & 
                                   (patients_df['dateAdmission'] <= fin_prec_dt)])
    changement_patients = ((total_patients - patients_prec) / patients_prec * 100) if patients_prec > 0 else 0
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("total_patients")}</div>
            <div class="metric-value">{total_patients:,}</div>
            <div class="metric-label {'positive-change' if changement_patients >= 0 else 'negative-change'}">
                {f"+{changement_patients:.1f}" if changement_patients >= 0 else f"{changement_patients:.1f}"}% {t("from_previous_period")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("currently_admitted")}</div>
            <div class="metric-value">{patients_actuels:,}</div>
            <div class="metric-label">{round(patients_actuels / departements_df['litsDisponibles'].sum() * 100, 1)}% {t("of_total_capacity")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("avg_stay_duration")}</div>
            <div class="metric-value">{duree_moyenne:.1f} {t("days")}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{t("total_revenue")}</div>
            <div class="metric-value">{format_currency(revenu_total)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques ligne 1
    st.markdown(f'<div class="sub-header">{t("patient_trends_section")}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Admissions et sorties quotidiennes
        fig = px.line(quotidien_filtre, x='date', y=['nouvellesAdmissions', 'sorties'], 
                     title=t("admissions_discharges"),
                     labels={'value': t("count"), 'date': t("date"), 'variable': t("metric")},
                     color_discrete_map={'nouvellesAdmissions': current_theme["primary_color"], 'sorties': current_theme["accent_color"]})
        fig.update_layout(
            legend_title_text='', 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor=current_theme["card_bg"],
            paper_bgcolor=current_theme["card_bg"],
            font=dict(color=current_theme["text_color"]),
            xaxis=dict(gridcolor=current_theme["border_color"]),
            yaxis=dict(gridcolor=current_theme["border_color"])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution par département
        if not patients_filtre.empty:
            dept_counts = patients_filtre['departement'].value_counts().reset_index()
            dept_counts.columns = [t("department_label"), t("count")]
            
            # Créer une carte de couleurs pour les départements
            dept_color_map = {dept: color for dept, color in zip(dept_counts[t("department_label")], current_theme["chart_colors"])}
            
            fig = px.pie(dept_counts, values=t("count"), names=t("department_label"), 
                        title=t("patient_distribution"),
                        color=t("department_label"),
                        color_discrete_map=dept_color_map)
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='#000000'))
            fig.update_layout(
                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                font=dict(color=current_theme["text_color"]),
                paper_bgcolor=current_theme["card_bg"],
                plot_bgcolor=current_theme["card_bg"]
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Graphiques ligne 2
    st.markdown(f'<div class="sub-header">{t("department_performance_section")}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Taux d'occupation par département
        if not departements_filtre.empty:
            fig = px.bar(departements_filtre, x='departement', y='tauxOccupation', 
                        title=t("bed_utilization"),
                        labels={'tauxOccupation': t("bed_utilization_label"), 'departement': t("department_label")},
                        color='departement',
                        color_discrete_map={dept: color for dept, color in zip(departements_filtre['departement'], current_theme["chart_colors"])})
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor=current_theme["card_bg"],
                paper_bgcolor=current_theme["card_bg"],
                font=dict(color=current_theme["text_color"]),
                xaxis=dict(gridcolor=current_theme["border_color"]),
                yaxis=dict(gridcolor=current_theme["border_color"]),
                showlegend=False
            )
            fig.update_yaxes(range=[0, 1], tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Taux de rétablissement par département
        if not departements_filtre.empty:
            fig = px.bar(departements_filtre, x='departement', y='tauxRetablissement', 
                        title=t("recovery_rate"),
                        labels={'tauxRetablissement': t("recovery_rate_label"), 'departement': t("department_label")},
                        color='departement',
                        color_discrete_map={dept: color for dept, color in zip(departements_filtre['departement'], current_theme["chart_colors"])})
            fig.update_layout(
                coloraxis_showscale=False,
                plot_bgcolor=current_theme["card_bg"],
                paper_bgcolor=current_theme["card_bg"],
                font=dict(color=current_theme["text_color"]),
                xaxis=dict(gridcolor=current_theme["border_color"]),
                yaxis=dict(gridcolor=current_theme["border_color"]),
                showlegend=False
            )
            fig.update_yaxes(range=[0, 1], tickformat='.0%')
            st.plotly_chart(fig, use_container_width=True)
    
    # Graphiques ligne 3
    st.markdown(f'<div class="sub-header">{t("financial_overview_section")}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenus vs Dépenses
        fig = px.line(quotidien_filtre, x='date', y=['revenus', 'depenses'], 
                     title=t("revenue_expenses"),
                     labels={'value': t("amount"), 'date': t("date"), 'variable': t("metric")},
                     color_discrete_map={'revenus': current_theme["success_color"], 'depenses': current_theme["danger_color"]})
        
        # Ajouter la zone de profit
        quotidien_filtre['profit'] = quotidien_filtre['revenus'] - quotidien_filtre['depenses']
        fig.add_trace(go.Scatter(
            x=quotidien_filtre['date'],
            y=quotidien_filtre['profit'],
            fill='tozeroy',
            mode='none',
            name=t("profit"),
            fillcolor=f'rgba({int(current_theme["success_color"][1:3], 16)}, {int(current_theme["success_color"][3:5], 16)}, {int(current_theme["success_color"][5:7], 16)}, 0.2)'
        ))
        
        fig.update_layout(
            legend_title_text='', 
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor=current_theme["card_bg"],
            paper_bgcolor=current_theme["card_bg"],
            font=dict(color=current_theme["text_color"]),
            xaxis=dict(gridcolor=current_theme["border_color"]),
            yaxis=dict(gridcolor=current_theme["border_color"])
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Revenus et coûts par département
        if not departements_filtre.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=departements_filtre['departement'],
                y=departements_filtre['revenusTotal'],
                name=t("revenue"),
                marker_color=current_theme["success_color"]
            ))
            
            fig.add_trace(go.Bar(
                x=departements_filtre['departement'],
                y=departements_filtre['coutFonctionnement'],
                name=t("operating_cost"),
                marker_color=current_theme["danger_color"]
            ))
            
            fig.update_layout(
                title=t("department_revenue_cost"),
                barmode='group',
                xaxis_title=t("department_label"),
                yaxis_title=t("amount"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                plot_bgcolor=current_theme["card_bg"],
                paper_bgcolor=current_theme["card_bg"],
                font=dict(color=current_theme["text_color"]),
                xaxis=dict(gridcolor=current_theme["border_color"]),
                yaxis=dict(gridcolor=current_theme["border_color"])
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Section du personnel
    st.markdown(f'<div class="sub-header">{t("staff_overview_section")}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution du personnel par rôle
        if not personnel_filtre.empty:
            role_counts = personnel_filtre['role'].value_counts().reset_index()
            role_counts.columns = [t("role"), t("count")]
            
            # Créer une carte de couleurs pour les rôles
            role_colors = {
                t("doctor"): current_theme["primary_color"],
                t("nurse"): current_theme["secondary_color"],
                t("technician"): current_theme["accent_color"],
                t("administrative"): current_theme["chart_colors"][3],
                t("support"): current_theme["chart_colors"][4]
            }
            
            fig = px.bar(role_counts, x=t("role"), y=t("count"), 
                        title=t("staff_distribution"),
                        color=t("role"),
                        color_discrete_map=role_colors)
            fig.update_layout(
                showlegend=False,
                plot_bgcolor=current_theme["card_bg"],
                paper_bgcolor=current_theme["card_bg"],
                font=dict(color=current_theme["text_color"]),
                xaxis=dict(gridcolor=current_theme["border_color"]),
                yaxis=dict(gridcolor=current_theme["border_color"])
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Performance du personnel
        if not personnel_filtre.empty:
            performance_data = personnel_filtre.groupby('role')['scorePerformance'].mean().reset_index()
            
            fig = px.bar(performance_data, x='role', y='scorePerformance', 
                        title=t("performance_score"),
                        labels={'scorePerformance': t("performance_score"), 'role': t("role")},
                        color='role',
                        color_discrete_map=role_colors)
            fig.update_layout(
                showlegend=False,
                plot_bgcolor=current_theme["card_bg"],
                paper_bgcolor=current_theme["card_bg"],
                font=dict(color=current_theme["text_color"]),
                xaxis=dict(gridcolor=current_theme["border_color"]),
                yaxis=dict(gridcolor=current_theme["border_color"])
            )
            fig.update_yaxes(range=[0, 1])
            st.plotly_chart(fig, use_container_width=True)
    
    # Cartes des départements
    st.markdown(f'<div class="sub-header">{t("department_quick_view_section")}</div>', unsafe_allow_html=True)
    
    # Créer des cartes de département en rangées de 3
    if not departements_filtre.empty:
        dept_data = departements_filtre.copy()
        dept_data = dept_data.sort_values('totalPatients', ascending=False)
        
        # Créer des rangées de 3 cartes
        for i in range(0, len(dept_data), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(dept_data):
                    dept = dept_data.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="department-card" style="border-left: 4px solid {current_theme["chart_colors"][j % len(current_theme["chart_colors"])]}">
                            <div class="department-title">{dept['departement']}</div>
                            <div class="department-metric">
                                <span class="department-metric-label">{t("patients")}:</span>
                                <span class="department-metric-value">{dept['totalPatients']}</span>
                            </div>
                            <div class="department-metric">
                                <span class="department-metric-label">{t("bed_utilization_label")}:</span>
                                <span class="department-metric-value">{dept['tauxOccupation']*100:.1f}%</span>
                            </div>
                            <div class="department-metric">
                                <span class="department-metric-label">{t("recovery_rate_label")}:</span>
                                <span class="department-metric-value">{dept['tauxRetablissement']*100:.1f}%</span>
                            </div>
                            <div class="department-metric">
                                <span class="department-metric-label">{t("staff")}:</span>
                                <span class="department-metric-value">{dept['nombrePersonnel']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Tableaux détaillés
    st.markdown(f'<div class="sub-header">{t("detailed_data_section")}</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([t("patient_data"), t("department_data"), t("staff_data")])
    
    with tab1:
        st.dataframe(patients_filtre.drop(['estHospitalise'], axis=1), use_container_width=True)
    
    with tab2:
        st.dataframe(departements_filtre, use_container_width=True)
    
    with tab3:
        st.dataframe(personnel_filtre, use_container_width=True)

# Pied de page
st.markdown("---")
st.markdown(f'<div style="text-align: center; color: {current_theme["primary_color"]};">{t("footer")}</div>', unsafe_allow_html=True)
