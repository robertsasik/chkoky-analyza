import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Mapa vlastníckych vzťahov",
    page_icon="🗺️",
    initial_sidebar_state="collapsed",
    layout="wide"
)

######################### INFO O AUTOROVI ################################################

# Skrytie pôvodného "About" footeru
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Nastavenie faviconu a názvu
st.set_page_config(page_title="Program starostlivosti", page_icon="data/logo_chkoky1.png")

# Sidebar s logom a menom autora
st.sidebar.image("data/logo_chkoky.png", use_container_width=True)
st.sidebar.markdown("### 🌿 Program starostlivosti")
st.sidebar.markdown("Autor: **Róbert Sásik**")
st.sidebar.markdown("**Správa CHKO Kysuce**")
st.sidebar.markdown("U Tomali č. 1511")
st.sidebar.markdown("022 01 Čadca")

######################### KONIEC INFO O AUTOROVI #########################################


######################### DASHBOARD – HLAVIČKA ###########################################
row1_col1, row1_col2 = st.columns([1, 7])

with row1_col1:
    image = Image.open("data/logo_chkoky.png")
    st.image(image, use_container_width=False) 
    
with row1_col2:
    st.write("## Chránená krajinná oblasť Kysuce")
    st.markdown("### Program starostlivosti")
######################### KONIEC HLAVIČKY #################################################


# 🧭 Definícia všetkých tabov
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Analýza vlastníckych vzťahov", 
    "🗺️ Vlastnícke vzťahy", 
    "🗺️ Ekologicko-funkčné plochy",
    "🗺️ Menežmentové opatrenia",
    "🗺️ Biotopy",
    "🗺️ Výskyt živočíšnych druhov",
    "📄 PDF mapy"
])


######################### TAB 1 ###########################################################
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

    # --- Výmery pozemkov podľa vlastníctva ---
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
            width=800
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.plotly_chart(fig, use_container_width=False)


######################### TAB 2 – VLASTNÍCKE VZŤAHY #######################################
with tab2:
    st.subheader("🗺️ Vlastnícke vzťahy")

    map_url = "https://mapky.github.io/mapa_vl_vztahy/#10/49.3682/18.6386"
    iframe_html = f"""<iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>"""
    components.html(iframe_html, height=500, scrolling=False)

    st.markdown("""
    <a href="https://mapky.github.io/mapa_vl_vztahy/#10/49.3682/18.6386" target="_blank">
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
    """, unsafe_allow_html=True)


######################### TAB 3 – EKOLOGICKO-FUNKČNÉ PLOCHY ##############################
with tab3:
    st.subheader("🗺️ Ekologicko-funkčné plochy")

    map_url = "https://mapky.github.io/mapa-efp/#10/49.3682/18.6386"
    iframe_html = f"""<iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>"""
    components.html(iframe_html, height=500, scrolling=False)

    st.markdown("""
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
    """, unsafe_allow_html=True)


######################### TAB 4 – MENEŽMENTOVÉ OPATRENIA ###############################
with tab4:
    st.subheader("🗺️ Menežmentové opatrenia")

    map_url = "https://mapky.github.io/mapa-menezment/#10/49.3682/18.6386"
    iframe_html = f"""<iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>"""
    components.html(iframe_html, height=500, scrolling=False)

    st.markdown("""
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
    """, unsafe_allow_html=True)


######################### TAB 5 – BIOTOPY ###############################################
with tab5:
    st.subheader("🗺️ Biotopy")

    map_url = "https://mapky.github.io/mapa-biotopy/#10/49.3682/18.6386"
    iframe_html = f"""<iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>"""
    components.html(iframe_html, height=500, scrolling=False)

    st.markdown("""
    <a href="https://mapky.github.io/mapa-biotopy/#10/49.3682/18.6386" target="_blank">
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
    """, unsafe_allow_html=True)


######################### TAB 6 – VÝSKYT ŽIVOČÍŠNYCH DRUHOV #############################
with tab6:
    st.subheader("🗺️ Výskyt živočíšnych druhov")

    map_url = "https://mapky.github.io/mapa-zoologia/"
    iframe_html = f"""<iframe src="{map_url}" width="100%" height="500" style="border:none;"></iframe>"""
    components.html(iframe_html, height=500, scrolling=False)

    st.markdown("""
    <a href="https://mapky.github.io/mapa-zoologia/" target="_blank">
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
    """, unsafe_allow_html=True)


######################### TAB 7 – PDF MAPY ##############################################
with tab7:
    st.subheader("📄 PDF mapy podľa kategórií")

    # 🔹 Cesta k hlavnému priečinku
    base_folder = "data/mapy"

    # 🔹 Získaj zoznam podpriečinkov (kategórií)
    subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

    if not subfolders:
        st.info("V priečinku `data/mapy/` sa nenašli žiadne podpriečinky s mapami.")
    else:
        # 🔹 Výber kategórie (podpriečinka)
        selected_folder = st.selectbox("Vyber kategóriu máp:", sorted(subfolders))

        # 🔹 Cesta ku konkrétnej kategórii
        pdf_folder = os.path.join(base_folder, selected_folder)

        # 🔹 Načítaj všetky PDF súbory v danej kategórii
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

        if pdf_files:
            st.markdown(f"### 📚 Mapa kategórie: **{selected_folder.capitalize()}**")
            for pdf in sorted(pdf_files):
                file_path = os.path.join(pdf_folder, pdf)
                file_name = os.path.splitext(pdf)[0]

                # 🔹 Tlačidlo na otvorenie alebo stiahnutie PDF
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"📄 {file_name}",
                        data=f,
                        file_name=pdf,
                        mime="application/pdf"
                    )
        else:
            st.warning(f"V kategórii **{selected_folder}** sa nenašli žiadne PDF súbory.")
######################### KONIEC PDF MAP #################################################



############################# INFO O AUTOROVI – PÄTA ####################################
st.markdown("""
<hr>
<div style='text-align: center'>
    <b>Autor:</b> 🌿Róbert Sásik<br>
    <small>© 2025 Štátna ochrana prírody, <br>Chránená krajinná oblasť Kysuce</small>
</div>
""", unsafe_allow_html=True)
############################# KONIEC PÄTY #################################################
