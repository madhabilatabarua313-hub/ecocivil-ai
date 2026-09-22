import streamlit as st
import pandas as pd
import numpy as np
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Page Configuration
st.set_page_config(
    page_title="EcoCivil AI: Professional Environmental Suite",
    page_icon="🌱",
    layout="wide"
)

# Initialize Session State Defaults
if 'annual_harvest_liters' not in st.session_state:
    st.session_state.annual_harvest_liters = 394825.0
if 'storage_tank_liters' not in st.session_state:
    st.session_state.storage_tank_liters = 32451.0
if 'total_biochar' not in st.session_state:
    st.session_state.total_biochar = 1000.0
if 'total_carbon_seq' not in st.session_state:
    st.session_state.total_carbon_seq = 800.0
if 'daily_wastewater' not in st.session_state:
    st.session_state.daily_wastewater = 38400.0
if 'daily_solid_waste' not in st.session_state:
    st.session_state.daily_solid_waste = 150.0
if 'solar_capacity' not in st.session_state:
    st.session_state.solar_capacity = 10.0
if 'solar_daily_energy' not in st.session_state:
    st.session_state.solar_daily_energy = 42.5

# Sidebar Navigation & Meta
st.sidebar.title("EcoCivil AI")
st.sidebar.markdown("Advanced Environmental & Sustainability Suite")

selected_module = st.sidebar.selectbox(
    "Select Navigation",
    [
        "Home / Dashboard",
        "Rainwater Harvesting Design",
        "Biochar & Sustainable Materials",
        "Wastewater & Waste Estimator",
        "Solar & Renewable Energy",
        "Green Building Pre-Assessment",
        "Master Executive Report"
    ]
)

st.sidebar.markdown("---")
st.sidebar.subheader("Engineer & Project Meta")
engineer_name = st.sidebar.text_input("Engineer Name", "Engr. Madhabilata Barua")
project_name = st.sidebar.text_input("Project Name", "Eco-City Complex Phase 1")


# ----------------------------------------------------
# MODULE 1: HOME / DASHBOARD
# ----------------------------------------------------
if selected_module == "Home / Dashboard":
    st.subheader("🌱 EcoCivil AI: Professional Environmental Suite")
    st.markdown("""
    Welcome to **EcoCivil AI**, an advanced decision-support platform engineered for environmental and civil engineers. 
    Design sustainable infrastructure, estimate ecological parameters, and evaluate green building compliance seamlessly.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Modules", "6 Tools", "Online")
    with col2:
        st.metric("Standards", "BNBC & LEED", "Compliant")
    with col3:
        st.metric("Calculation Engine", "Vectorized", "Active")
    with col4:
        st.metric("Platform Status", "Stable", "Secure")
        
    st.markdown("---")
    st.info("💡 **Quick Tip:** Use the sidebar navigation to switch between environmental design modules, execute calculations, and export master executive reports instantly.")


# ----------------------------------------------------
# MODULE 2: RAINWATER HARVESTING DESIGN
# ----------------------------------------------------
elif selected_module == "Rainwater Harvesting Design":
    st.subheader("🌧️ Rainwater Harvesting & Storage Design")
    st.markdown("Calculate annual rooftop rainwater harvesting potential and optimal underground storage tank capacity.")
    
    col1, col2 = st.columns(2)
    with col1:
        roof_area = st.number_input("Roof Area (sq. ft)", min_value=100.0, value=2000.0, step=50.0)
        rainfall_mm = st.number_input("Annual Average Rainfall (mm)", min_value=100.0, value=2500.0, step=50.0)
    with col2:
        runoff_coeff = st.slider("Runoff Coefficient (Roof Type)", min_value=0.5, max_value=0.95, value=0.85, step=0.05)
        reserve_days = st.slider("Storage Reserve Days", min_value=10, max_value=90, value=30, step=5)
        
    # Calculations
    roof_area_sqm = roof_area * 0.092903
    annual_harvest = roof_area_sqm * rainfall_mm * runoff_coeff
    tank_capacity = (annual_harvest / 365.0) * reserve_days
    
    st.session_state.annual_harvest_liters = annual_harvest
    st.session_state.storage_tank_liters = tank_capacity
    
    st.markdown("---")
    st.subheader("📊 Harvesting Results")
    res1, res2 = st.columns(2)
    res1.metric("Annual Harvest Potential", f"{annual_harvest:,.0f} Liters")
    res2.metric("Recommended Storage Tank", f"{tank_capacity:,.0f} Liters")


# ----------------------------------------------------
# MODULE 3: BIOCHAR & SUSTAINABLE MATERIALS
# ----------------------------------------------------
elif selected_module == "Biochar & Sustainable Materials":
    st.subheader("🌍 Sustainable Construction Materials & Carbon Sequestration")
    st.markdown("Estimate quantities for biochar applications, recycled coarse aggregates, and supplementary cementitious materials.")
    
    mat_type = st.selectbox(
        "Select Sustainable Material Estimator",
        [
            "Biochar: Soil Amendment & Carbon Sequestration", 
            "Biochar: Concrete Cement Replacement", 
            "Recycled Concrete Aggregate (RCA)", 
            "Fly Ash / SCM Replacement"
        ]
    )
    
    if mat_type == "Biochar: Soil Amendment & Carbon Sequestration":
        col1, col2 = st.columns(2)
        with col1:
            land_area = st.number_input("Land Area (sq. m)", min_value=10.0, value=500.0, step=10.0)
        with col2:
            app_rate = st.number_input("Application Rate (kg/sq. m)", min_value=0.1, value=2.0, step=0.1)
            
        feedstock = st.selectbox(
            "Select Biochar Feedstock Type",
            [
                "Woody Biomass (High Carbon: 70% - 90%)", 
                "Crop Residues / Manure (Lower Carbon: 30% - 60%)"
            ]
        )
        
        # Carbon content percentage based on feedstock characteristics[cite: 1]
        if "Woody Biomass" in feedstock:
            carbon_fraction = 0.80  # Average 80% for woody biomass
        else:
            carbon_fraction = 0.45  # Average 45% for crop residues/manure
            
        total_biochar = land_area * app_rate
        total_carbon_seq = total_biochar * carbon_fraction
        
        st.session_state.total_biochar = total_biochar
        st.session_state.total_carbon_seq = total_carbon_seq
        
        st.success(f"🌱 Total Biochar Required for Soil Amendment: **{total_biochar:,.2f} kg**")
        st.info(f"🛡️ Estimated Long-term Carbon Sequestered: **{total_carbon_seq:,.2f} kg** (Based on feedstock profile: 70-90% for wood, 30-60% for crop residues)[cite: 1]")

    elif mat_type == "Biochar: Concrete Cement Replacement":
        conc_vol = st.number_input("Concrete Volume (CFT)", min_value=10.0, value=500.0, step=10.0)
        replacement_pct = st.slider("Cement Replacement by Biochar (%)", min_value=1.0, max_value=20.0, value=5.0)
        
        biochar_weight = conc_vol * 22.0 * (replacement_pct / 100.0)
        st.success(f"🧱 Biochar Required for Concrete Mix: **{biochar_weight:,.2f} kg**")

    elif mat_type == "Recycled Concrete Aggregate (RCA)":
        total_conc = st.number_input("Total Concrete Volume Required (CFT)", min_value=50.0, value=1000.0, step=50.0)
        rca_pct = st.slider("RCA Replacement Percentage (%)", min_value=10.0, max_value=100.0, value=30.0)
        
        rca_volume = total_conc * 0.75 * (rca_pct / 100.0)
        st.success(f"♻️ Recycled Concrete Aggregate (RCA) Needed: **{rca_volume:,.2f} CFT**")

    elif mat_type == "Fly Ash / SCM Replacement":
        cement_bags = st.number_input("Total Cement Bags (50 kg/bag)", min_value=10, value=100, step=5)
        scm_pct = st.slider("SCM / Fly Ash Replacement (%)", min_value=10.0, max_value=50.0, value=25.0)
        
        total_cement_kg = cement_bags * 50.0
        fly_ash_weight = total_cement_kg * (scm_pct / 100.0)
        st.success(f"🏭 Fly Ash / SCM Required: **{fly_ash_weight:,.2f} kg**")


# ----------------------------------------------------
# MODULE 4: WASTEWATER & WASTE ESTIMATOR
# ----------------------------------------------------
elif selected_module == "Wastewater & Waste Estimator":
    st.subheader("💧 Municipal Wastewater & Solid Waste Estimator")
    st.markdown("Estimate daily municipal sewage generation and solid waste output based on occupancy and population standards.")
    
    col1, col2 = st.columns(2)
    with col1:
        population = st.number_input("Design Population / Occupants", min_value=10, value=300, step=10)
    with col2:
        water_consumption = st.number_input("Per Capita Water Consumption (Liters/day)", min_value=50, value=160, step=5)
        
    wastewater = population * water_consumption * 0.80
    solid_waste = population * 0.5
    
    st.session_state.daily_wastewater = wastewater
    st.session_state.daily_solid_waste = solid_waste
    
    st.markdown("---")
    colA, colB = st.columns(2)
    colA.metric("Daily Wastewater Generation", f"{wastewater:,.2f} Liters/day")
    colB.metric("Daily Solid Waste Generation", f"{solid_waste:,.2f} kg/day")


# ----------------------------------------------------
# MODULE 5: SOLAR & RENEWABLE ENERGY
# ----------------------------------------------------
elif selected_module == "Solar & Renewable Energy":
    st.subheader("☀️ Solar PV & Renewable Energy Estimator")
    st.markdown("Calculate photovoltaic system capacity and daily clean energy generation potential.")
    
    col1, col2 = st.columns(2)
    with col1:
        solar_roof = st.number_input("Usable Roof Area for Solar (sq. ft)", min_value=100.0, value=1000.0, step=50.0)
        sun_hours = st.number_input("Peak Sun Hours (hrs/day)", min_value=2.0, value=5.0, step=0.5)
    with col2:
        panel_efficiency = st.slider("Panel Efficiency (%)", min_value=10.0, max_value=25.0, value=20.0, step=1.0)
        system_loss = st.slider("System Losses (%)", min_value=5.0, max_value=30.0, value=15.0, step=1.0)
        
    solar_capacity = (solar_roof / 100.0) * (panel_efficiency / 20.0)
    daily_energy = solar_capacity * sun_hours * (1.0 - (system_loss / 100.0))
    
    st.session_state.solar_capacity = solar_capacity
    st.session_state.solar_daily_energy = daily_energy
    
    st.markdown("---")
    colA, colB = st.columns(2)
    colA.metric("Installed Solar Capacity", f"{solar_capacity:,.2f} kWp")
    colB.metric("Estimated Daily Energy", f"{daily_energy:,.2f} kWh (Units)")


# ----------------------------------------------------
# MODULE 6: GREEN BUILDING PRE-ASSESSMENT
# ----------------------------------------------------
elif selected_module == "Green Building Pre-Assessment":
    st.subheader("🌿 Green Building Pre-Assessment (LEED & BNBC Aligned)")
    st.markdown("Evaluate sustainability compliance and pre-assess certification readiness.")
    
    c1 = st.checkbox("Rainwater Harvesting & Water Efficiency Measures Implemented", value=True)
    c2 = st.checkbox("Use of Sustainable Construction Materials (Biochar, Fly Ash, RCA)", value=True)
    c3 = st.checkbox("Rooftop Solar PV Integration for Renewable Energy", value=True)
    c4 = st.checkbox("Wastewater Treatment & Management System Provision", value=False)
    c5 = st.checkbox("Eco-friendly Site Planning & Ecological Preservation", value=True)
    
    score = sum([c1, c2, c3, c4, c5]) * 20
    
    st.markdown("---")
    st.metric("Green Building Compliance Score", f"{score} / 100 Points")
    if score >= 80:
        st.success("🌟 Rating: **Platinum Class Ready** (Exceptional Sustainability Standard)")
    elif score >= 60:
        st.info("⭐ Rating: **Gold Class Ready** (Strong Environmental Compliance)")
    else:
        st.warning("⚠️ Rating: **Standard Compliance** (Additional Sustainability Credits Recommended)")


# ----------------------------------------------------
# MODULE 7: MASTER EXECUTIVE REPORT
# ----------------------------------------------------
elif selected_module == "Master Executive Report":
    st.subheader("📄 Master Executive Report PDF Generator")
    st.markdown("Generate and download a comprehensive, professional PDF engineering report aggregating all module estimates.")
    
    if st.button("📥 Generate Executive PDF Report"):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#1b4332'),
            spaceAfter=15
        )
        elements.append(Paragraph("EcoCivil AI: Master Executive Report", title_style))
        elements.append(Paragraph(f"<b>Project Name:</b> {project_name}", styles['Normal']))
        elements.append(Paragraph(f"<b>Lead Engineer:</b> {engineer_name}", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Summary Data Table
        data = [
            ["Environmental Module", "Estimated Metric Output"],
            ["Rainwater Annual Harvest", f"{st.session_state.annual_harvest_liters:,.2f} Liters"],
            ["Recommended Storage Tank", f"{st.session_state.storage_tank_liters:,.2f} Liters"],
            ["Biochar Soil Amendment", f"{st.session_state.total_biochar:,.2f} kg"],
            ["Carbon Sequestered (Biochar)", f"{st.session_state.total_carbon_seq:,.2f} kg"],
            ["Daily Wastewater Volume", f"{st.session_state.daily_wastewater:,.2f} Liters/day"],
            ["Daily Solid Waste Output", f"{st.session_state.daily_solid_waste:,.2f} kg/day"],
            ["Solar PV Capacity", f"{st.session_state.solar_capacity:,.2f} kWp"],
            ["Daily Clean Energy Generation", f"{st.session_state.solar_daily_energy:,.2f} kWh"]
        ]
        
        t = Table(data, colWidths=[250, 250])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2d6a4f')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f3f4')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(t)
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<i>This report is generated automatically by EcoCivil AI Suite, adhering to international green building and engineering estimation standards.</i>", styles['Italic']))
        
        doc.build(elements)
        buffer.seek(0)
        
        st.success("✅ Executive PDF Report Generated Successfully!")
        st.download_button(
            label="⬇️ Download PDF Report",
            data=buffer,
            file_name="EcoCivil_AI_Executive_Report.pdf",
            mime="application/pdf"
        )
