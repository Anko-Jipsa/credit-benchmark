import streamlit as st
import streamlit_func as sf
from scripts import data_proc as dp
from pages import *

country = sf.country_select()
df = dp.read_file(country)
item = sf.item_selector()

if item == "Front":
    front.main()

elif (item == "ECL") | (item == "EAD"):
    ecl_ead_page.main(df, item)

elif item == "Coverage Ratio":
    coverage_page.main(df)

elif item == "Staging balances (%)":
    stage_prop_page.main(df)