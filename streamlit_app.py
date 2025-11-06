import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Mapa vlastníckych vzťahov",
    page_icon="🗺️",
    initial_sidebar_state="collapsed",
    layout="wide"
    
)
######################### dashboard - prvý riadok a dva stĺpce #########################

row1_col1, row1_col2 = st.columns([1, 7])

with row1_col1:
    image = Image.open("data/logo_chkoky.png")
    st.image(image, use_container_width=False) 
    
with row1_col2:
    st.write("## Chránená krajinná oblasť Kysuce")
    st.markdown("### Program starostlivosti")

########################### koniec - prvý riadok a dva stĺpce ###########################



tab1, tab2, tab3, tab4 = st.tabs(["📊 Analýza vlastníckych vzťahov", 
                            "🗺️ Mapa vlastníckych vzťahov", 
                            "🗺️ Mapa ekologicko-funkčné plochy",
                            "🗺️ Mapa menežmentové opatrenia"])

with tab1:
    # --- Načítanie dát ---
    df = pd.read_excel(
        r"data/analyza_vlastnictvo_drp2.xlsx",
        header=0,
    )

    # Nastavenie indexu na 'Druh vlastníctva'
    df = df.set_index("Druh vlastníctva")

    st.header("Výmery druhov pozemkov podľa vlastníctva (ha)")
    st.dataframe(df)

    # Odstránenie riadku "Celkový súčet"
    df = df[~df.index.str.contains("Celkový", case=False, na=False)]

    # Výpočet celkovej výmery
    df["Súčet"] = df.sum(axis=1)

    # --- Farby podľa druhu vlastníctva ---
    farby = {
        "súkromné a bez LV": "#626BFF", 
        "obecné a mestské": "#F4E129",
        "štátne": "#00CE94",
        "cirkevné": "#88BCE1",  
        "spoločenstvá": "#FEA062",
        "zmiešané": "#F1553C"
    }

    # --- Výber typu grafu ---
    typ_grafu = st.radio(
        "Vyber typ grafu:",
        ["📈 Percentuálny podiel druhov pozemkov", "📊 Výmery pozemkov podľa vlastníctva"],
        horizontal=True
    )

    # --- Percentuálny podiel druhov pozemkov ---
    if typ_grafu == "📈 Percentuálny podiel druhov pozemkov":
        fig = px.pie(
            df,
            values="Súčet",
            names=df.index,
            title="Podiel výmery podľa druhu vlastníctva",
            color=df.index,
            color_discrete_map=farby,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            showlegend=True,
            legend_title_text="Druh vlastníctva",
            title_x=0.5,
            width=800
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Výmery pozemkov podľa vlastníctva (usporiadaný + pevná šírka + zarovnanie na stred) ---
    elif typ_grafu == "📊 Výmery pozemkov podľa vlastníctva":
        df_sorted = df.reset_index().sort_values(by="Súčet", ascending=False)

        fig = px.bar(
            df_sorted,
            x="Druh vlastníctva",
            y="Súčet",
            color="Druh vlastníctva",
            color_discrete_map=farby,
            title="Výmery podľa druhu vlastníctva (ha)",
            text_auto=".2f"
        )

        fig.update_layout(
            xaxis_title="Druh vlastníctva",
            yaxis_title="Výmera (ha)",
            showlegend=False,
            title_x=0.5,
            width=800   # pevná šírka grafu
        )

        # 🔹 Zarovnanie na stred pomocou troch stĺpcov
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.plotly_chart(fig, use_container_width=False)

with tab2:
    st.subheader("🗺️ Mapa vlastníckych vzťahov")

    # URL k tvojej GitHub Pages mape
    map_url = "https://mapky.github.io/mapa_vl_vztahy/#10/49.3599/18.6529"

    # Vlož mapu ako iframe
    iframe_html = f"""
        <iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>
        """
    components.html(iframe_html, height=500, scrolling=False)

#Tlačidlo na otvorenie mapy v novom okne       
    st.markdown(
    """
    <a href="https://mapky.github.io/mapa_vl_vztahy/#10/49.3599/18.6529" target="_blank">
        <button style="
            background-color:#2b8a3e;
            color:white;
            border:none;
            padding:10px 20px;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
        ">🌍 Otvoriť mapu v novom okne</button>
    </a>
    """,
    unsafe_allow_html=True
)

with tab3:
    st.subheader("🗺️ Mapa ekologicko-funkčné plochy")

    # URL k tvojej GitHub Pages mape
    map_url = "https://mapky.github.io/mapa-efp/#10/49.3682/18.6386"

    # Vlož mapu ako iframe
    iframe_html = f"""
        <iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>
        """
    components.html(iframe_html, height=500, scrolling=False)

    #Tlačidlo na otvorenie mapy v novom okne       
    st.markdown(
    """
    <a href="https://mapky.github.io/mapa-efp/#10/49.3682/18.6386" target="_blank">
        <button style="
            background-color:#2b8a3e;
            color:white;
            border:none;
            padding:10px 20px;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
        ">🌍 Otvoriť mapu v novom okne</button>
    </a>
    """,
    unsafe_allow_html=True
)

with tab4:
    st.subheader("🗺️ Mapa menežmentové opatrenia")

    # URL k tvojej GitHub Pages mape
    map_url = "https://mapky.github.io/mapa-menezment/#10/49.3682/18.6386"

    # Vlož mapu ako iframe
    iframe_html = f"""
        <iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>
        """
    components.html(iframe_html, height=500, scrolling=False)
        #Tlačidlo na otvorenie mapy v novom okne       
    st.markdown(
    """
    <a href="https://mapky.github.io/mapa-menezment/#10/49.3682/18.6386" target="_blank">
        <button style="
            background-color:#2b8a3e;
            color:white;
            border:none;
            padding:10px 20px;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
        ">🌍 Otvoriť mapu v novom okne</button>
    </a>
    """,
    unsafe_allow_html=True
)
    