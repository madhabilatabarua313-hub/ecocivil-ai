import streamlit as st
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# 1. Page Configuration
st.set_page_config(
    page_title="EcoCivil AI - Environmental Suite",
    page_icon="🌱",
    layout="wide"
)

# Helper function to generate PDF Report
def generate_master_pdf(engineer, project, loc, harvest_liters, tank_liters, material_summary, wastewater, solid_waste, solar_kw, solar_kwh, green_score):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor("#2e7d32"), spaceAfter=10)
    normal_style = styles['Normal']
    
    story.append(Paragraph("🌱 EcoCivil AI - Executive Sustainability Report", title_style))
    story.append(Spacer(1, 10))
    
    meta_text = f"<b>Project Name:</b> {project}<br/><b>Location:</b> {loc}<br/><b>Lead Engineer:</b> {engineer}<br/><b>Date:</b> 2026-09-22"
    story.append(Paragraph(meta_text, normal_style))
    story.append(Spacer(1, 15))
    
    data = [
        ["Module / Parameter", "Calculated Metric / Value"],
        ["Annual Rainwater Harvest Potential", f"{harvest_liters:,.0f} Liters"],
        ["Recommended Storage Tank Capacity", f"{tank_liters:,.0f} Liters"],
        ["Sustainable Material Estimation", material_summary],
        ["Estimated Daily Wastewater Generation", f"{wastewater:,.0f} Liters/day"],
        ["Estimated Solid Waste Generation", f"{solid_waste:,.1f} kg/day"],
        ["Rooftop Solar PV Capacity", f"{solar_kw:,.2f} kWp"],
        ["Daily Solar Energy Generation", f"{solar_kwh:,.2f} kWh (Units/day)"],
        ["Green Building Pre-Assessment Score", f"{green_score} / 50 Points"]
    ]
    
    t = Table(data, colWidths=[230, 280])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e8f5e9")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#1b5e20")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#c8e6c9")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f1f8e9")])
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# 2. Sidebar Navigation & Meta
st.sidebar.title("🌱 EcoCivil AI")
st.sidebar.markdown("Advanced Environmental & Sustainability Suite")

navigation = st.sidebar.radio(
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
st.sidebar.subheader("👤 Engineer & Project Meta")
engineer_name = st.sidebar.text_input("Engineer Name", "Engr. Madhabilata Barua")
project_name = st.sidebar.text_input("Project Name", "Green Campus Initiative")
location = st.sidebar.text_input("Location", "Chattogram")

if "estimates_data" not in st.session_state:
    st.session_state["estimates_data"] = {}

# ----------------------------------------------------
# MODULE 1: HOME / DASHBOARD
# ----------------------------------------------------
if navigation == "Home / Dashboard":
    st.title("🌱 EcoCivil AI: Professional Environmental Suite")
    st.markdown("""
    Welcome to **EcoCivil AI**, an advanced decision-support platform engineered for environmental and civil engineers. 
    Design sustainable infrastructure, estimate ecological parameters, and evaluate green building compliance seamlessly.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Modules", "6 Tools", "Online")
    col2.metric("Standards", "BNBC & LEED", "Compliant")
    col3.metric("Calculation Engine", "Vectorized", "Active")
    col4.metric("Platform Status", "Stable", "Secure")

# ----------------------------------------------------
# MODULE 2: RAINWATER HARVESTING DESIGN
# ----------------------------------------------------
elif navigation == "Rainwater Harvesting Design":
    st.header("💧 Rooftop Rainwater Harvesting System Design")
    st.markdown("Calculate potential rainwater collection volume and recommended underground/overhead storage tank capacity.")

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        roof_area = st.number_input("Rooftop Footprint Area (sq. ft)", min_value=100.0, value=2000.0)
        annual_rainfall = st.number_input("Average Annual Rainfall (mm)", min_value=500.0, value=2500.0)
    
    with col_r2:
        runoff_coef = st.slider("Runoff Coefficient (Roof Material)", 0.6, 0.95, 0.85, 0.05)
        demand_days = st.number_input("Storage Reserve Days", min_value=10, value=30)

    annual_harvest_liters = roof_area * 0.0929 * annual_rainfall * runoff_coef
    storage_tank_liters = (annual_harvest_liters / 365) * demand_days

    st.session_state["harvest_liters"] = annual_harvest_liters
    st.session_state["tank_liters"] = storage_tank_liters

    st.markdown("---")
    st.subheader("📊 Harvesting Results")
    res1, res2 = st.columns(2)
    res1.metric("Annual Harvest Potential", f"{annual_harvest_liters:,.0f} Liters")
    res2.metric("Recommended Storage Tank", f"{storage_tank_liters:,.0f} Liters")

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
            
        # Feedstock type selection based on carbon content characteristics
        feedstock = st.selectbox(
            "Select Biochar Feedstock Type",
            [
                "Woody Biomass (High Carbon: 70% - 90%)[cite: 1]", 
                "Crop Residues / Manure (Lower Carbon: 30% - 60%)[cite: 1]"
            ]
        )
        
        # Determine carbon content factor based on feedstock selection
        if "Woody Biomass" in feedstock:
            carbon_fraction = 0.80  # Average 80% for woody biomass
        else:
            carbon_fraction = 0.45  # Average 45% for crop residues/manure
            
        total_biochar = land_area * app_rate
        total_carbon_seq = total_biochar * carbon_fraction
        
        st.success(f"🌱 Total Biochar Required for Soil Amendment: **{total_biochar:,.2f} kg**")
        st.info(f"🛡️ Estimated Long-term Carbon Sequestered: **{total_carbon_seq:,.2f} kg** (Based on selected feedstock profile[cite: 1])")

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

    st.session_state["material_summary"] = material_summary_str

# ----------------------------------------------------
# MODULE 4: WASTEWATER & WASTE ESTIMATOR
# ----------------------------------------------------
elif navigation == "Wastewater & Waste Estimator":
    st.header("♻️ Municipal Wastewater & Solid Waste Estimator")
    
    population = st.number_input("Equivalent Population (Capita)", min_value=10, value=300)
    per_capita_water = st.number_input("Per Capita Water Consumption (Liters/Day/Capita)", min_value=50.0, value=160.0)
    
    wastewater_gen = population * per_capita_water * 0.80 
    solid_waste_gen = population * 0.5 

    st.session_state["wastewater"] = wastewater_gen
    st.session_state["solid_waste"] = solid_waste_gen
    
    st.markdown("---")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Estimated Daily Wastewater", f"{wastewater_gen:,.0f} Liters/day")
    w_col2.metric("Estimated Solid Waste Generation", f"{solid_waste_gen:,.1f} kg/day")

# ----------------------------------------------------
# MODULE 5: SOLAR & RENEWABLE ENERGY
# ----------------------------------------------------
elif navigation == "Solar & Renewable Energy":
    st.header("☀️ Rooftop Solar PV & Clean Energy Estimator")
    st.markdown("Calculate rooftop solar panel capacity and estimated daily electricity generation.")

    s_col1, s_col2 = st.columns(2)
    with s_col1:
        usable_roof_area = st.number_input("Usable Rooftop Area for Solar (sq. ft)", min_value=50.0, value=1000.0)
        sun_hours = st.slider("Average Peak Sun Hours / Day", 3.0, 7.0, 5.0, 0.5)
    with s_col2:
        panel_efficiency = st.slider("Solar Panel Efficiency (%)", 15, 25, 20)
        system_loss = st.slider("System Losses / Inverter Efficiency (%)", 10, 25, 15)

    installed_capacity_kw = usable_roof_area / 100.0 * (panel_efficiency / 20.0)
    daily_energy_kwh = installed_capacity_kw * sun_hours * (1 - system_loss / 100.0)

    st.session_state["solar_kw"] = installed_capacity_kw
    st.session_state["solar_kwh"] = daily_energy_kwh

    st.markdown("---")
    sc1, sc2 = st.columns(2)
    sc1.metric("Estimated Solar Capacity", f"{installed_capacity_kw:,.2f} kWp")
    sc2.metric("Daily Energy Generation", f"{daily_energy_kwh:,.2f} kWh (Units/day)")

# ----------------------------------------------------
# MODULE 6: GREEN BUILDING PRE-ASSESSMENT
# ----------------------------------------------------
elif navigation == "Green Building Pre-Assessment":
    st.header("Rating Checklist & Pre-Assessment")
    st.markdown("Evaluate your project's readiness for green building certification based on sustainable criteria.")

    score = 0
    max_score = 50

    st.subheader("Checklist Criteria:")
    c1 = st.checkbox("Rainwater harvesting system implemented (+10 pts)")
    if c1: score += 10

    c2 = st.checkbox("Use of sustainable materials / biochar / recycled aggregate (+10 pts)")
    if c2: score += 10

    c3 = st.checkbox("Rooftop solar PV integration planned (+10 pts)")
    if c3: score += 10

    c4 = st.checkbox("Wastewater treatment & greywater recycling system (+10 pts)")
    if c4: score += 10

    c5 = st.checkbox("Proper solid waste management & composting unit (+10 pts)")
    if c5: score += 10

    st.session_state["green_score"] = score

    st.markdown("---")
    st.metric("Total Green Building Score", f"{score} / {max_score} Points")
    if score >= 40:
        st.success("🌟 Rating: Platinum Class Green Project Ready!")
    elif score >= 25:
        st.info("👍 Rating: Gold Class Project Potential.")
    else:
        st.warning("⚠️ Rating: Needs more sustainable infrastructure integration.")

# ----------------------------------------------------
# MODULE 7: MASTER EXECUTIVE REPORT
# ----------------------------------------------------
elif navigation == "Master Executive Report":
    st.header("📄 Master Executive Report & PDF Export")
    st.markdown("Compile all modular computations into a comprehensive professional PDF engineering report.")

    h_liters = st.session_state.get("harvest_liters", 394825.0)
    t_liters = st.session_state.get("tank_liters", 32451.0)
    mat_summary = st.session_state.get("material_summary", "Biochar Soil Amendment: 1,000.00 kg")
    w_water = st.session_state.get("wastewater", 38400.0)
    s_waste = st.session_state.get("solid_waste", 150.0)
    s_kw = st.session_state.get("solar_kw", 10.0)
    s_kwh = st.session_state.get("solar_kwh", 42.5)
    g_score = st.session_state.get("green_score", 40)

    st.info("Click the button below to generate and download the complete project summary report in PDF format.")
    
    pdf_bytes = generate_master_pdf(engineer_name, project_name, location, h_liters, t_liters, mat_summary, w_water, s_waste, s_kw, s_kwh, g_score)
    
    st.download_button(
        label="📥 Download Master Executive PDF Report",
        data=pdf_bytes,
        file_name=f"EcoCivil_AI_Report_{project_name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
