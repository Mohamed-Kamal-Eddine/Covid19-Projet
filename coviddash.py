import datetime
import requests
import streamlit as st
import altair as alt
import pandas as pd


st.cache(persist=True)
def load_data_covid() -> pd.DataFrame:
    response = requests.get("http://127.0.0.1:8000/get_data_covid")
    json_data = response.json()
    covidd = pd.DataFrame(json_data)

    return covidd

#################################
st.cache(persist=True)
def load_data_latest() -> pd.DataFrame:
    response = requests.get("http://127.0.0.1:8000/get_data_latest")
    json_data = response.json()
    latestvar = pd.DataFrame(json_data)
    return latestvar

#############################################################
st.title(' Covid-19 Dashboard  ')
st.sidebar.markdown(' *Covid-19 Dashboard*  ')

covid_list = load_data_covid()
covid = pd.DataFrame(covid_list)
latest_list=load_data_latest()
latest =pd.DataFrame(latest_list)

#############metrics
cty = st.sidebar.selectbox("Select country", covid["Country"][:186] if "Country" in covid.columns else [])

st.header(" KPI Metrics")
###########
# Filtrer les données en fonction du pays sélectionné
selected_country_data = covid[covid["Country"] == cty]
selected_country_latest = latest[latest["Country"] == cty]

#######
total_confirmed = selected_country_latest['Confirmed'].sum()
total_recovered = selected_country_latest['Recovered'].sum()
total_deaths = selected_country_latest['Deaths'].sum()

col1, col2, col3 = st.columns(3)

# Définir le style CSS pour les bordures à gauche
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; padding: 10px;">
        <div style="border-left: 5px solid #007BFF; padding-left: 24px;padding-right: 5px;">
            <h3>Total Confirmed Cases</h3>
            <p>{total_confirmed}</p>
        </div>
        <div style="border-left: 5px solid #28A745;padding-left: 24px;padding-right: 5px;">
            <h3>Total Recovered</h3>
            <p>{total_recovered}</p>
        </div>
        <div style="border-left: 5px solid #DC3545; padding-left: 24px;padding-right: 5px;">
            <h3>Total Deaths</h3>
            <p>{total_deaths}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

chart_data = pd.DataFrame({
    'Category': ['Confirmed', 'Recovered', 'Deaths'],
    'Value': [total_confirmed, total_recovered, total_deaths]
})

# Altair chart
chart = alt.Chart(chart_data).mark_bar().encode(
    x='Category:N',
    y='Value:Q',
    color='Category:N',
    text='Value:N'
).properties(
    width=alt.Step(80),
    title='Total COVID-19 Cases, Recoveries, and Deaths'
)

# Display the Altair chart within Streamlit
st.altair_chart(chart)

#########side bar#####################

st.header(f"View Daily New Cases/Recoveries/Deaths for {cty}")
daily = st.sidebar.selectbox("Select the option",('Daily New Cases', 'Daily New Recoveries','Daily New Deaths'))
typ = st.sidebar.radio("Select the type of Chart",("Line Chart","Scatter Chart"))
date_format = "%Y-%m-%d"
ca = alt.Chart(covid[covid["Country"]==cty]).encode(
    x=alt.X("Date:T", title="Date"),
    y="New cases",
    tooltip=[alt.Tooltip("Date:T", title="Date", format=date_format),"Country","New cases"]
).interactive()

re = alt.Chart(covid[covid["Country"]==cty]).encode(
    x=alt.X("Date:T", title="Date"),
    y="New recovered",
    tooltip=[alt.Tooltip("Date:T", title="Date", format=date_format),"Country","New recovered"]
).interactive()

de = alt.Chart(covid[covid["Country"]==cty]).encode(
    x="Date",
    y="New deaths",
    tooltip=[alt.Tooltip("Date:T", title="Date", format=date_format),"Country","New deaths"]
).interactive()

cas= alt.Chart(covid[covid["Country"]==cty],title="Scatter Chart",width=500,height=400).mark_circle(color='green').encode(
    x="Date",
    y="New cases",
    size="New deaths",
    color="New recovered",
    tooltip=["Date","Country","New cases","New deaths","New recovered"]
).interactive()




if daily =='Daily New Cases':
    if typ == "Line Chart":
        st.altair_chart(ca.mark_line(color='firebrick'))
    else:
        st.altair_chart(ca.mark_circle(color='firebrick'))
elif daily =='Daily New Recoveries':
    if typ == "Line Chart":
        st.altair_chart(re.mark_line(color='green'))
    else:
        st.altair_chart(re.mark_circle(color='green'))
elif daily =='Daily New Deaths':
    if typ == "Line Chart":
        st.altair_chart(de.mark_line(color='purple'))
    else:
        st.altair_chart(de.mark_circle(color='purple'))

"Visualizing Daily New Cases, recoveries and deaths in a Single Chart"
"In Scatter Chart, Circle represent daily new cases, size of the circle shows the daily deaths and the color variation shows the daily recoveries"
st.altair_chart(cas)

a= alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_bar().encode(
    x="day(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

b=alt.Chart(covid[covid["Country"]==cty],width=500,height=400).mark_text().encode(
    x="day(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)

c= alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_bar().encode(
    x="day(Date):O",
   # y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

d=alt.Chart(covid[covid["Country"]==cty],width=500,height=100).mark_text().encode(
    x="day(Date):O",
    #y="month(Date):O",
    text="sum(New deaths)"
)
st.header(f"View deaths for {cty} by Month/Day/Date")

e= alt.Chart(covid[covid["Country"]==cty],width=900,height=300).mark_bar().encode(
    x="date(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

f=alt.Chart(covid[covid["Country"]==cty],width=900,height=300).mark_text(angle=270).encode(
    x="date(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)

g= alt.Chart(covid[covid["Country"]==cty],width=900,height=100).mark_bar().encode(
    x="date(Date):O",
    y="month(Date):O",
    color="sum(New deaths)",
    tooltip="sum(New deaths)"
)

h=alt.Chart(covid[covid["Country"]==cty],width=900,height=100).mark_text(angle=270).encode(
    x="date(Date):O",
    y="month(Date):O",
    text="sum(New deaths)"
)



op = st.radio("Select the option",('Day and Month', 'Day','Date and Month','Date'))

if op == 'Day and Month':
     st.altair_chart(a+b)
elif op == 'Day':
    st.altair_chart(c+d)
elif op == 'Date and Month':
    st.altair_chart(e+f)
elif op == 'Date':
    st.altair_chart(g+h)



st.header(f"View Total Confirmed vs Total Recovered cases for {cty}")

con=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="purple").encode(
    x=alt.X("Date:T", title="Date"),
    y="Confirmed",
    tooltip=[alt.Tooltip("Date:T", title="Date", format=date_format),"Confirmed"]

).interactive()

rec=alt.Chart(covid[covid["Country"]==cty]).mark_area(color="green").encode(
    x="Date",
    y="Recovered",
    tooltip=[alt.Tooltip("Date:T", title="Date", format=date_format),"Recovered"]

).interactive()

opt = st.radio(
     "Select the option",
     ('Confirmed', 'Recovered','Confirmed and Recovered'))

if opt == 'Confirmed':
     st.altair_chart(con)
elif opt == 'Recovered':
    st.altair_chart(rec)
else:
     st.altair_chart(con+rec)


st.header(f"Summary of Covid-19 infections in {cty}")
"From 01-02-2020 to 30-11-2020"
tot = latest[latest["Country"]==cty]['Confirmed'].sum()

reco = latest[latest["Country"]==cty]['Recovered'].sum()

act = latest[latest["Country"]==cty]['Active'].sum()

dths = latest[latest["Country"]==cty]['Deaths'].sum()

infsing = covid[covid["Country"]==cty]['New cases'].max()

deasing = covid[covid["Country"]==cty]['New deaths'].max()

recsing = covid[covid["Country"]==cty]['New recovered'].max()

tab = {"Category":["Total Confirmed Cases","Total Recovered","Total Active Cases","Total Deaths","Maximum Cases on a Single Day","Maximum Deaths on a Single Day","Maximum Recoveries on a Single Day"],
       "Total Count":[tot,reco,act,dths,infsing,deasing,recsing]}

stat = pd.DataFrame(tab)
st.table(stat)


confirm = latest.sort_values("Confirmed",ascending=False)[["Country","Confirmed"]].head()

confirm.reset_index(inplace = True,drop = True)

bar2 = alt.Chart(confirm).mark_bar().encode(
    x="Confirmed",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Confirmed"
).interactive()


death = latest.sort_values("Deaths",ascending=False)[["Country","Deaths"]].head()

death.reset_index(inplace = True,drop = True)

bar3 = alt.Chart(death).mark_bar().encode(
    x="Deaths",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Deaths"
).interactive()



deathper=latest["Deaths"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Death Percentage"] = deathper
deathp = lat.sort_values("Death Percentage",ascending=False)[["Country","Death Percentage"]].head()

deathp.reset_index(inplace = True,drop = True)

bar4 = alt.Chart(deathp).mark_bar().encode(
    x="Death Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Death Percentage"
).interactive()


recover = latest.sort_values("Recovered",ascending=False)[["Country","Recovered"]].head()

recover.reset_index(inplace = True,drop = True)

bar5 = alt.Chart(recover).mark_bar().encode(
    x="Recovered",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered"
).interactive()


recper=latest["Recovered"] / latest["Confirmed"] * 100
lat = latest.copy()
lat["Recovered Percentage"] = recper
recp = lat.sort_values("Recovered Percentage",ascending=False)[["Country","Recovered Percentage"]].head()

recp.reset_index(inplace = True,drop = True)

bar6 = alt.Chart(recp).mark_bar().encode(
    x="Recovered Percentage",
    y=alt.Y("Country",sort="-x"),
    color=alt.Color("Country",legend=None),
    tooltip = "Recovered Percentage"
).interactive()

st.header(f"Do you want to know the Top 5 countries")
top = st.selectbox("Select your option",["Confirmed Cases","Deaths","Death Percentage","Recovered","Recovered Percentage"])
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


st.header(f"View Covid-19 details by Date")

default_date = datetime.date(2020, 2, 1)


st.header(f"View Covid-19 Country Standings")

ques2 = st.radio("Select the option to know details",["Total Confirmed Cases","Total Recovered","Total Deaths","Total Active Cases"])

if ques2 == "Total Confirmed Cases":
    dff = latest.sort_values(by="Confirmed",ascending=False)[["Country","Confirmed"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
elif ques2 == "Total Recovered":
    dff = latest.sort_values(by="Recovered",ascending=False)[["Country","Recovered"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
elif ques2 == "Total Deaths":
    dff = latest.sort_values(by="Deaths",ascending=False)[["Country","Deaths"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
else:
    dff = latest.sort_values(by="Active",ascending=False)[["Country","Active"]].reset_index(drop=True)
    dff.index+=1
    st.dataframe(dff)
