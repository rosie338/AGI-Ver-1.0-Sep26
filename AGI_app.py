import numpy as np
import math
import streamlit as st
import pandas as pd

#st.set_page_config(
#    page_title="AGI Calculator",
 #   page_icon="logo.png",
  #  layout="wide"
#)

st.title("AGI Magnesium Anode Calculation")
with st.sidebar:
    st.header("Input parameters")
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

import streamlit as st
import numpy as np

# ============================================================
# PIPE INPUT FUNCTION
# ============================================================
st.header("Input Pipe Dimensions")
left, right = st.columns ([2,2])
def pipe_zone_input(zone):

    # Initialise number of pipes for this zone
    pipe_key = f"num_pipes_zone_{zone}"

    if pipe_key not in st.session_state:
        st.session_state[pipe_key] = 1

    st.write(f"### Zone {zone}")

    diameters = {}
    lengths = {}

    # -----------------------------------------
    # Input rows
    # -----------------------------------------

    for i in range(1, st.session_state[pipe_key] + 1):

        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.write(f"Pipe {i}")

        with col2:
            diameters[f"d{i}"] = st.number_input(
                "Diameter (mm)",
                value=0.0,
                key=f"zone{zone}_diameter_{i}"
            )

        with col3:
            lengths[f"l{i}"] = st.number_input(
                "Length (m)",
                value=0.0,
                key=f"zone{zone}_length_{i}"
            )

    # -----------------------------------------
    # Add pipe button
    # -----------------------------------------

    if st.session_state[pipe_key] < 8:

        if st.button(
            "➕ Add pipe",
            key=f"add_pipe_zone_{zone}"
        ):
            st.session_state[pipe_key] += 1
            st.rerun()

    # -----------------------------------------
    # Convert to 8-row dictionaries
    # -----------------------------------------

    for i in range(
        st.session_state[pipe_key] + 1,
        9
    ):
        diameters[f"d{i}"] = 0.0
        lengths[f"l{i}"] = 0.0

    return diameters, lengths

#============================================
# Display results on GUI
#============================================
with left:
    with st.expander("Zone 1", expanded=False):
        dzone1, lzone1 = pipe_zone_input(1)

    with st.expander("Zone 2"):
        dzone2, lzone2 = pipe_zone_input(2)
with right:
    with st.expander("Zone 3"):
        dzone3, lzone3 = pipe_zone_input(3)

    with st.expander("Zone 4"):
        dzone4, lzone4 = pipe_zone_input(4)

#============================================
# Current Density Values
#============================================
currentdensity = pd.DataFrame({
    "Level": ["High","Low","Average"],
    "Current Density (mAm⁻²)": [0.02, 0.001, 0.011]
                  })
currentdensitydict = {"hi":0.02,
                  "lo":0.001,
                  "avg":0.011
                  }
st.header("Current Density Values")
st.dataframe(currentdensity, hide_index = True, use_container_width=True)

#==============================================
# Extracting Values From Dictionary
#==============================================
def extract_values_from_dic(dictionary):
    value = np.array([*dictionary.values()])
    return value
dzone1_values = extract_values_from_dic(dzone1)
dzone2_values = extract_values_from_dic(dzone2)
dzone3_values = extract_values_from_dic(dzone3)
dzone4_values = extract_values_from_dic(dzone4)
lzone1_values = extract_values_from_dic(lzone1)
lzone2_values = extract_values_from_dic(lzone2)
lzone3_values = extract_values_from_dic(lzone3)
lzone4_values = extract_values_from_dic(lzone4)
currentdensity_values = extract_values_from_dic(currentdensitydict)

#===============================================
# Calculations
#===============================================
st.header("Design Results")
#-------------------------------------
#     Calculations surface area
#-------------------------------------
def finding_sa(diameter, length, zone):
    sa = sum(math.pi * diameter/1000 * length * safety_factor)
    return sa
sa1 = finding_sa(dzone1_values, lzone1_values, 1)
sa2 = finding_sa(dzone2_values, lzone2_values, 2)
sa3 = finding_sa(dzone3_values, lzone3_values, 3)
sa4 = finding_sa(dzone4_values, lzone4_values, 4)

#-------------------------------------
#  Calculations current requirement
#-------------------------------------
def current_requirements (surface_area, zone):
    current = surface_area*currentdensity_values
    return(current)
current1 = current_requirements(sa1, 1)
current2 = current_requirements(sa2, 2)
current3 = current_requirements(sa3, 3)
current4 = current_requirements(sa4, 4)
#-------------------------------------
#  Calculations mass requirement
#-------------------------------------

def calculate_mass(current, zone):
    mass = (current*design_life*8760)/(AU_efficiency*anode_capacity*1000)
    return mass #kg
mass1 = calculate_mass(current1, 1)
mass2 = calculate_mass(current2, 2)
mass3 = calculate_mass(current3, 3)
mass4 = calculate_mass(current4, 4)

#-------------------------------------
#  Calculations anode resistance
#-------------------------------------
def calc_anode_resistance(b, l, d, r, p):
    de = d*p
    le = l*p
    ln_expression = (((4*le**2) + (4*le*math.sqrt((b**2) + (le**2))))/(de*b))
    anode_res = (((0.159* r)/le) * ((np.log(ln_expression)) + (b/le) - (math.sqrt(((b**2)+(le**2))/(le**2)))-1))
    print(f"\nAnode resistance at {p*100:.0f}%: {anode_res:.6f}")
    return(anode_res)
anode_resistance = calc_anode_resistance(TDHA_depth, 
                                         anode_length, 
                                         anode_diameter, 
                                         soil_res, 
                                         1)
anode_resistance_80 = calc_anode_resistance(TDHA_depth, 
                                            anode_length, 
                                            anode_diameter, 
                                            soil_res, 
                                            0.8)

#-------------------------------------
#Calculations individual anode current
#-------------------------------------
indv_anode_current = abs(((AOC_potential-PP_potential)*1000)/anode_resistance_80)  #mA

#-------------------------------------
#    Calculations number of anodes
#-------------------------------------
def find_number_of_anodes(current, zone):
    number = np.ceil(current/indv_anode_current)
    return(number)
number1 = (find_number_of_anodes(current1, 1))
number2 = (find_number_of_anodes(current2, 2))
number3 = (find_number_of_anodes(current3, 3))
number4 = (find_number_of_anodes(current4, 4))
total_anodes = np.ceil(number1 + number2 + number3 + number4)

#=====================================
#Printing results
#=====================================
#-------------------------------------
#  Printing surface area results
#-------------------------------------
st.subheader("Surface area (m²)")
sa = pd.DataFrame({"Zone": ["Zone 1", "Zone 2", "Zone 3", "Zone 4"],
                   "Surface Area (m²)": [sa1, sa2, sa3, sa4]})
st.dataframe(sa, hide_index = True, use_container_width=True)

#--------------------------------------------
#  Printing mass, current, and number results
#--------------------------------------------

zones = {
    "Zone 1": {
        "current": current1,
        "mass": mass1,
        "number": number1
    },

    "Zone 2": {
        "current": current2,
        "mass": mass2,
        "number": number2
    },

    "Zone 3": {
        "current": current3,
        "mass": mass3,
        "number": number3
    },

    "Zone 4": {
        "current": current4,
        "mass": mass4,
        "number": number4
    }
}

currentresults = pd.DataFrame({
    "Zone": [
        "Zone 1",
        "Zone 2",
        "Zone 3",
        "Zone 4"
    ],

    "High": [
        current1[0],
        current2[0],
        current3[0],
        current4[0]
    ],

    "Low": [
        current1[1],
        current2[1],
        current3[1],
        current4[1]
    ],

    "Average": [
        current1[2],
        current2[2],
        current3[2],
        current4[2]
    ]
})

massresults = pd.DataFrame({
    "Zone": [
        "Zone 1",
        "Zone 2",
        "Zone 3",
        "Zone 4"
    ],

    "High": [
            mass1[0],
            mass2[0],
            mass3[0],
            mass4[0]
        ],
    
        "Low": [
            mass1[1],
            mass2[1],
            mass3[1],
            mass4[1]
        ],
    
        "Average": [
            mass1[2],
            mass2[2],
            mass3[2],
            mass4[2]
        ]
    })

numberresults = pd.DataFrame({
    "Zone": [
        "Zone 1",
        "Zone 2",
        "Zone 3",
        "Zone 4"
    ],

    "High": [
        number1[0],
        number2[0],
        number3[0],
        number4[0]
    ],

    "Low": [
        number1[1],
        number2[1],
        number3[1],
        number4[1]
    ],

    "Average": [
        number1[2],
        number2[2],
        number3[2],
        number4[2]
    ]
})

#current results
st.subheader("Current Requirements (mA)")
st.dataframe(
    currentresults,
    use_container_width=True,
    hide_index=True
)

#printing amode mass requirement results
st.subheader("Anode Mass Required (kg)")
st.dataframe(
    massresults,
    use_container_width=True,
    hide_index=True
)

#printing anode design results
st.subheader("Anode Design Results")
anoderesults = pd.DataFrame({
    "Parameter": [
        "Anode Resistance at 100%",
        "Anode Resistance at 80%",
        "Individual Anode Current"
    ],
    "Value": [
        anode_resistance,
        anode_resistance_80,
        indv_anode_current
    ],
    "Units": ["Ω", "Ω", "mA"
    ]})
st.dataframe(
    anoderesults,
    use_container_width=True,
    hide_index=True)

#printing number of anodes resuts
st.subheader("Number of anodes required to meet end of life current requirement for each pipe")
st.dataframe(
    numberresults,
    use_container_width=True,
    hide_index=True
)

#printing total number of anodes results
totalnumber = pd.DataFrame({
    "High":[total_anodes[0]],
    "Low": [total_anodes[1]],
    "Average": [total_anodes[2]]
})

st.subheader("Number of Anodes Grand Total for AGI")
st.dataframe(
    totalnumber,
    use_container_width=True,
    hide_index=True
)