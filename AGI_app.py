import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


st.title("AGI Magnesium Anode Calculation")

safety_factor = 1.5
design_life = 15 #yr
anode_capacity = 1230 #A.hr/kg
anode_diameter = 0.146 #m
anode_length = 0.508 #m
AU_efficiency = 0.8 #80% (anode utilisation efficiency)
TDHA_depth = 3 #m (twice depth of horizontal anode burial)
AOC_potential = -1.7 #V (anode oped circuit potential)
PP_potential = -0.95 #V (pipeline polarised potential)
anode_mass = 7.7 #kg
soil_res = 1000 #Ωm

import streamlit as st

safety_factor = st.number_input("Safety factor", value=1.5)

design_life = st.number_input("Design life (yr)", value=15)

anode_capacity = st.number_input("Anode capacity (A.hr/kg)", value=1230)

anode_diameter = st.number_input("Anode diameter (m)", value=0.146)

anode_length = st.number_input("Anode length (m)", value=0.508)

AU_efficiency = st.number_input("Anode utilisation efficiency", value=0.8)

TDHA_depth = st.number_input("TDHA depth (m)", value=3.0)

AOC_potential = st.number_input("Anode open circuit potential (V)", value=-1.7)

PP_potential = st.number_input("Pipeline polarised potential (V)", value=-0.95)

anode_mass = st.number_input("Anode mass (kg)", value=7.7)

soil_res = st.number_input("Soil resistivity (Ωm)", value=1000)

parameters = {

    "Safety factor": safety_factor,
    "Design life": design_life,
    "Anode capacity": anode_capacity,
    "Anode diameter": anode_diameter,
    "Anode length": anode_length,
    "Anode utilisation efficiency": AU_efficiency,
    "TDHA depth": TDHA_depth,
    "Anode open circuit potential": AOC_potential,
    "Pipeline polarised potential": PP_potential,
    "Anode mass": anode_mass,
    "Soil resistivity": soil_res
}