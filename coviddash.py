import altair as alt
import pandas as pd
import requests
import streamlit as st


st.cache(persist=True)

def load_data_covid() -> pd.DataFrame:
    response = requests.get("http://localhost:8000/get_data_covid")

    if response.status_code == 200:
        try:
            json_data = response.json()
            print("Raw JSON Data:")
            print(json_data)  # Add this line to inspect the JSON

            # Check if the JSON data is a list of dictionaries
            if isinstance(json_data, list) and all(isinstance(item, dict) for item in json_data):

                covidvar = pd.DataFrame(json_data)
                print("DataFrame Info:")
                print(covidvar.info())

                return covidvar
            else:
                raise ValueError("JSON data is not in the expected format (list of dictionaries).")

        except ValueError as err:
            print(f"Error converting JSON to DataFrame: {err}")  # Add this line for debugging
            raise  # Reraise the exception to stop caching

    else:
        raise st.error(f"Error fetching data from FastAPI. Status Code: {response.status_code}")


#################################
def load_data_latest() -> pd.DataFrame:
    response = requests.get("http://localhost:8000/get_data_latest")

    if response.status_code == 200:
        try:
            json_data = response.json()
            print("Raw JSON Data:")
            print(json_data)  # Add this line to inspect the JSON

            # Check if the JSON data is a list of dictionaries
            if isinstance(json_data, list) and all(isinstance(item, dict) for item in json_data):

                latest_data = pd.DataFrame(json_data)
                print("DataFrame Info:")
                print(latest_data.info())

                return latest_data
            else:
                raise ValueError("JSON data is not in the expected format (list of dictionaries).")

        except ValueError as err:
            print(f"Error converting JSON to DataFrame: {err}")  # Add this line for debugging
            raise  # Reraise the exception to stop caching

    else:
        raise st.error(f"Error fetching data from FastAPI. Status Code: {response.status_code}")


st.title(' Covid-19 Dashboard  ')
st.sidebar.markdown(' **Covid-19 Dashboard** ')
st.header("Totals for All Countries")

covid_list = load_data_covid()
covid = pd.DataFrame(covid_list)
latest_list = load_data_latest()
latest = pd.DataFrame(latest_list)

# Afficher le total des cas confirmés, récupérations et décès pour tous les pays
total_confirmed_all = latest["Confirmed"].sum()
total_recovered_all = latest["Recovered"].sum()
total_deaths_all = latest["Deaths"].sum()

chart_data = pd.DataFrame({
    'Category': ['Confirmed', 'Recovered', 'Deaths'],
    'Value': [total_confirmed_all, total_recovered_all, total_deaths_all]
})

# Création du graphique Altair
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Category:N',
    y='Value:Q',
    color='Category:N',
    text='Value:Q'  # Ajouter des étiquettes
).properties(
    width=alt.Step(80)  # Ajuster la largeur des barres pour éviter le chevauchement
)

# Affichage du graphique Altair
st.altair_chart(chart, use_container_width=True)
cty = st.sidebar.selectbox("Select country", covid["Country"][:186] if "Country" in covid.columns else [])

st.header(f"View Daily New Cases/Recoveries/Deaths for {cty}")
daily = st.sidebar.selectbox("Select the option", ('Daily New Cases', 'Daily New Recoveries', 'Daily New Deaths'))
typ = st.sidebar.radio("Select the type of Chart", ("Line Chart", "Scatter Chart"))

ca = alt.Chart(covid[covid["Country"] == cty]).encode(
    x="Date",
    y="New cases",
    tooltip=["Date", "Country", "New cases"]
).interactive()

re = alt.Chart(covid[covid["Country"] == cty]).encode(
    x="Date",
    y="New recovered",
    tooltip=["Date", "Country", "New recovered"]
).interactive()

de = alt.Chart(covid[covid["Country"] == cty]).encode(
    x="Date",
    y="New deaths",
    tooltip=["Date", "Country", "New deaths"]
).interactive()

cas = alt.Chart(covid[covid["Country"] == cty], title="Scatter Chart", width=500, height=400).mark_circle(
    color='green').encode(
    x="Date",
    y="New cases",
    size="New deaths",
    color="New recovered",
    tooltip=["Date", "Country", "New cases", "New deaths", "New recovered"]
).interactive()

if daily == 'Daily New Cases':
    if typ == "Line Chart":
        st.altair_chart(ca.mark_line(color='firebrick'))
    else:
        st.altair_chart(ca.mark_circle(color='firebrick'))
elif daily == 'Daily New Recoveries':
    if typ == "Line Chart":
        st.altair_chart(re.mark_line(color='green'))
    else:
        st.altair_chart(re.mark_circle(color='green'))
elif daily == 'Daily New Deaths':
    if typ == "Line Chart":
        st.altair_chart(de.mark_line(color='purple'))
    else:
        st.altair_chart(de.mark_circle(color='purple'))

"Visualizing Daily New Cases, recoveries and deaths in a Single Chart"
"In Scatter Chart, Circle represent daily new cases, "
"size of the circle shows the daily deaths and the color variation shows the daily recoveries"
st.altair_chart(cas)

a = alt.Chart(covid[covid["Country"] == cty], width=500, height=400).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

b = alt.Chart(covid[covid["Country"] == cty], width=500, height=400).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)

c = alt.Chart(covid[covid["Country"] == cty], width=500, height=100).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

d = alt.Chart(covid[covid["Country"] == cty], width=500, height=100).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)
st.header(f"View deaths for {cty} by Month/Day/Date")

e = alt.Chart(covid[covid["Country"] == cty], width=900, height=300).mark_bar().encode(
    x="date(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

f = alt.Chart(covid[covid["Country"] == cty], width=900, height=300).mark_text(angle=270).encode(
    x="date(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)

g = alt.Chart(covid[covid["Country"] == cty], width=900, height=100).mark_bar().encode(
    x="date(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

h = alt.Chart(covid[covid["Country"] == cty], width=900, height=100).mark_text(angle=270).encode(
    x="date(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)

op = st.radio("Select the option", ('Day and Month', 'Day', 'Date and Month', 'Date'))

if op == 'Day and Month':
    st.altair_chart(a + b)
elif op == 'Day':
    st.altair_chart(c + d)
elif op == 'Date and Month':
    st.altair_chart(e + f)
elif op == 'Date':
    st.altair_chart(g + h)

st.header(f"View Total Confirmed vs Total Recovered cases for {cty}")

con = alt.Chart(covid[covid["Country"] == cty]).mark_area(color="purple").encode(
    x="Date",
    y="Confirmed",
    tooltip=["Date", "Confirmed"]

).interactive()

rec = alt.Chart(covid[covid["Country"] == cty]).mark_area(color="green").encode(
    x="Date",
    y="Recovered",
    tooltip=["Date", "Recovered"]

).interactive()

opt = st.radio(
    "Select the option",
    ('Confirmed', 'Recovered', 'Confirmed and Recovered'))

if opt == 'Confirmed':
    st.altair_chart(con)
elif opt == 'Recovered':
    st.altair_chart(rec)
else:
    st.altair_chart(con + rec)

st.header(f"Summary of Covid-19 infections in {cty}")
"From 01-02-2020 to 30-11-2020"
tot = latest[latest["Country"] == cty]['Confirmed'].sum()

# st.subhead(f"Total Confirmed cases in {cty} = {tot}")

reco = latest[latest["Country"] == cty]['Recovered'].sum()

# st.subhead(f"Total Recovered in {cty} = {reco}")

act = latest[latest["Country"] == cty]['Active'].sum()

# st.subhead(f"Total Active cases in {cty} = {act}")

dths = latest[latest["Country"] == cty]['Deaths'].sum()

# st.subheader(f"Total Deaths occured in {cty} = {dths}")
infsing = covid[covid["Country"] == cty]['New cases'].max()

deasing = covid[covid["Country"] == cty]['New deaths'].max()

recsing = covid[covid["Country"] == cty]['New recovered'].max()

tab = {"Category": ["Total Confirmed Cases", "Total Recovered", "Total Active Cases", "Total Deaths",
                    "Maximum Cases on a Single Day", "Maximum Deaths on a Single Day",
                    "Maximum Recoveries on a Single Day"],
       "Total Count": [tot, reco, act, dths, infsing, deasing, recsing]}

stat = pd.DataFrame(tab)
st.table(stat)

st.header(f"Daily New Cases and Total Cases for Selected Countries")

options = st.multiselect(
    'Select Multiple Countries',
    covid["Country"][:186])

fire = alt.Chart(covid[covid["Country"].isin(options)], width=500, height=300).mark_circle().encode(
    x="Date",
    y="Country",
    tooltip=["Date", "Country", "New cases"],
    color="Country",
    size="New cases"
).interactive()

bar1 = alt.Chart(covid[covid["Country"].isin(options)]).mark_bar().encode(
    y="sum(New cases)",
    x=alt.X("Country", sort="-y"),
    color="Country",
    tooltip="sum(New cases)"
).interactive()

st.altair_chart(fire | bar1)

texchart = alt.Chart(covid[covid["Country"].isin(options)], width=800, height=400).mark_text().encode(
    x=alt.X('sum(New cases)', axis=None),
    y=alt.Y("Country", axis=None),
    size=alt.Size("sum(New cases)", scale=alt.Scale(range=[10, 150]), legend=None),
    text="Country",
    color=alt.Color("Country", legend=None),
    tooltip=["Country", "sum(New cases)"]
).configure_view(strokeWidth=0).configure_axis(grid=False, domain=False)
st.markdown("### World Cloud representing total confirmed cases for the selected countries")
st.altair_chart(texchart)

confirm = latest.sort_values("Confirmed", ascending=False)[["Country", "Confirmed"]].head()

confirm.reset_index(inplace=True, drop=True)

bar2 = alt.Chart(confirm).mark_bar().encode(
    x="Confirmed",
    y=alt.Y("Country", sort="-x"),
    color=alt.Color("Country", legend=None),
    tooltip="Confirmed"
).interactive()

death = latest.sort_values("Deaths", ascending=False)[["Country", "Deaths"]].head()

death.reset_index(inplace=True, drop=True)

bar3 = alt.Chart(death).mark_bar().encode(
    x="Deaths",
    y=alt.Y("Country", sort="-x"),
    color=alt.Color("Country", legend=None),
    tooltip="Deaths"
).interactive()

deathper = latest["Deaths"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Death Percentage"] = deathper
deathp = lat.sort_values("Death Percentage", ascending=False)[["Country", "Death Percentage"]].head()

deathp.reset_index(inplace=True, drop=True)

bar4 = alt.Chart(deathp).mark_bar().encode(
    x="Death Percentage",
    y=alt.Y("Country", sort="-x"),
    color=alt.Color("Country", legend=None),
    tooltip="Death Percentage"
).interactive()

recover = latest.sort_values("Recovered", ascending=False)[["Country", "Recovered"]].head()

recover.reset_index(inplace=True, drop=True)

bar5 = alt.Chart(recover).mark_bar().encode(
    x="Recovered",
    y=alt.Y("Country", sort="-x"),
    color=alt.Color("Country", legend=None),
    tooltip="Recovered"
).interactive()

recper = latest["Recovered"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Recovered Percentage"] = recper
recp = lat.sort_values("Recovered Percentage", ascending=False)[["Country", "Recovered Percentage"]].head()

recp.reset_index(inplace=True, drop=True)

bar6 = alt.Chart(recp).mark_bar().encode(
    x="Recovered Percentage",
    y=alt.Y("Country", sort="-x"),
    color=alt.Color("Country", legend=None),
    tooltip="Recovered Percentage"
).interactive()

st.header(f"Do you want to know the Top 5 countries")
top = st.selectbox("Select your option",
                   ["Confirmed Cases", "Deaths", "Death Percentage", "Recovered", "Recovered Percentage"])
if top == "Confirmed Cases":
    st.altair_chart(bar2)
elif top == "Deaths":
    st.altair_chart(bar3)
elif top == "Death Percentage":
    st.altair_chart(bar4)
elif top == "Recovered":
    st.altair_chart(bar5)
else:
    st.altair_chart(bar6)
