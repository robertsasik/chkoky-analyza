import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import pandas as pd
import plotly.express as px
import os

# ========================== ZÁKLADNÉ NASTAVENIE STRÁNKY ==========================
st.set_page_config(
    page_title="Program starostlivosti CHKOKY",
    page_icon="data/logo_chkoky1.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================== CSS – ŠTÝLY PRE SCROLLOVATEĽNÝ ZOZNAM ==========================
st.markdown("""
<style>
/* Zoznam na šírku stránky */
div[data-testid="stSelectbox"] {
    width: 100% !important;
}

/* Scrollovateľný obsah (ak treba) */
.stSelectbox [role="listbox"] {
    max-height: 400px !important;
    overflow-y: auto !important;
}
</style>
""", unsafe_allow_html=True)

# ========================== 🟩 TIP NA OTVORENIE SIDEBARU (AUTOMATICKÉ ZMIZNUTIE) ==========================
if "show_sidebar_tip" not in st.session_state:
        st.session_state.show_sidebar_tip = True  # zobrazí sa pri prvom načítaní

if st.session_state.show_sidebar_tip:
    st.markdown("""
            <style>
            @keyframes fadeOut {
                0% {opacity: 1;}
                80% {opacity: 1;}
                100% {opacity: 0;}
            }
            .sidebar-tip {
                animation: fadeOut 10s forwards;
            }
            </style>
            <div class='sidebar-tip' style='background-color:#eef7f1; padding:8px; border-radius:8px; 
                        text-align:center; color:#1b4332; font-size:14px; font-weight:500;'>
            💡 <b>Tip:</b> Kliknite na dvojitú šípku ⏩ vľavo hore pre otvorenie bočného panela s PDF mapami.
            </div>
            """, unsafe_allow_html=True)
st.write("\n")

# ========================== HLAVIČKA STRÁNKY ==========================
row1_col1, row1_col2 = st.columns([1, 7])

with row1_col1:
    image = Image.open("data/logo_chkoky.png")
    st.image(image, use_container_width=False)

with row1_col2:
    st.write("### Chránená krajinná oblasť Kysuce")
    st.write("#### Program starostlivosti")
st.markdown("---")

# ========================== SIDEBAR – PDF MAPY PODĽA KATEGÓRIÍ ==========================

st.sidebar.subheader("🗺️ PDF mapy")
st.sidebar.button("🗺️ PDF mapy")
base_folder = "data/mapy"
subfolders = [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]

if not subfolders:
    st.sidebar.info("V priečinku `data/mapy/` sa nenašli žiadne podpriečinky s mapami.")
else:
    selected_folder = st.sidebar.selectbox("Vyber kategóriu máp:", sorted(subfolders))
    pdf_folder = os.path.join(base_folder, selected_folder)
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

    if pdf_files:
        st.sidebar.markdown(f"## 📁 Kategória máp:\n **{selected_folder}**")
        for pdf in sorted(pdf_files):
            file_path = os.path.join(pdf_folder, pdf)
            file_name = os.path.splitext(pdf)[0]
            with open(file_path, "rb") as f:
                st.sidebar.download_button(
                    label=f"📄 {file_name}",
                    data=f,
                    file_name=pdf,
                    mime="application/pdf"
                )
    else:
        st.sidebar.warning(f"V kategórii **{selected_folder}** sa nenašli žiadne PDF súbory.")

# ========================== HLAVNÝ ROLUJÚCI ZOZNAM SEKCIÍ ==========================

st.markdown("### 🧭 **Vyberte sekciu:**")

sekcia = st.selectbox(
    "",
    [
        "📊 Analýza vlastníckych vzťahov",
        "🗺️ Mapa - vlastnícke vzťahy",
        "🗺️ Mapa - ekologicko-funkčné plochy",
        "🗺️ Mapa - menežmentové opatrenia",
        "🗺️ Mapa - biotopy",
        "🦉 Mapa - výskyt živočíšnych druhov",
        "🌿 Mapa - Výskyt rastlinných druhov"
    ],
    index=0,
    key="hlavny_vyber",
    help="Vyberte sekciu, ktorú chcete zobraziť"
)
st.markdown("---")

# ========================== OBSAH PODĽA VÝBERU ==========================
# --- 1. ANALÝZA VLASTNÍCKYCH VZŤAHOV ---
if sekcia == "📊 Analýza vlastníckych vzťahov":
    df = pd.read_excel("data/analyza_vlastnictvo_drp2.xlsx", header=0)
    df = df.set_index("Druh vlastníctva")

    st.header("Výmery druhov pozemkov podľa vlastníctva (ha)")
    st.dataframe(df)

    df = df[~df.index.str.contains("Celkový", case=False, na=False)]
    df["Súčet"] = df.sum(axis=1)

    farby = {
        "súkromné a bez LV": "#626BFF",
        "obecné a mestské": "#F4E129",
        "štátne": "#00CE94",
        "cirkevné": "#88BCE1",
        "spoločenstvá": "#FEA062",
        "zmiešané": "#F1553C"
    }

    typ_grafu = st.radio(
        "Vyber typ grafu:",
        ["📈 Percentuálny podiel druhov pozemkov", "📊 Výmery pozemkov podľa vlastníctva"],
        horizontal=True
    )

    if typ_grafu == "📈 Percentuálny podiel druhov pozemkov":
        fig = px.pie(
            df, values="Súčet", names=df.index,
            title="Podiel výmery podľa druhu vlastníctva",
            color=df.index, color_discrete_map=farby, hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=True, legend_title_text="Druh vlastníctva", title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        df_sorted = df.reset_index().sort_values(by="Súčet", ascending=False)
        fig = px.bar(
            df_sorted, x="Druh vlastníctva", y="Súčet",
            color="Druh vlastníctva", color_discrete_map=farby,
            title="Výmery podľa druhu vlastníctva (ha)", text_auto=".2f"
        )
        fig.update_layout(xaxis_title="Druh vlastníctva", yaxis_title="Výmera (ha)", showlegend=False, title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)


# --- 2. VLASTNÍCKE VZŤAHY ---
elif sekcia == "🗺️ Mapa - vlastnícke vzťahy":
    st.subheader("🗺️ Vlastnícke vzťahy")
    map_url = "https://mapky.github.io/mapa_vl_vztahy/#10/49.3682/18.6386"
    components.html(f'<iframe src="{map_url}" width="100%" height="600" style="border:none;"></iframe>', height=600)
    st.markdown(f"""
    <a href="{map_url}" target="_blank">
        <button style="background-color:#2b8a3e;color:white;border:none;padding:10px 20px;
                       border-radius:8px;font-size:16px;cursor:pointer;">
        🌍 Otvoriť mapu v novom okne</button>
    </a>
    """, unsafe_allow_html=True)


# --- 3. EKOLOGICKO-FUNKČNÉ PLOCHY ---
elif sekcia == "🗺️ Mapa - ekologicko-funkčné plochy":
    st.subheader("🗺️ Ekologicko-funkčné plochy")
    map_url = "https://mapky.github.io/mapa-efp/#10/49.3682/18.6386"
    components.html(f'<iframe src="{map_url}" width="100%" height="600" style="border:none;"></iframe>', height=600)
    st.markdown(f"""
    <a href="{map_url}" target="_blank">
        <button style="background-color:#2b8a3e;color:white;border:none;padding:10px 20px;
                       border-radius:8px;font-size:16px;cursor:pointer;">
        🌍 Otvoriť mapu v novom okne</button>
    </a>
    """, unsafe_allow_html=True)


# --- 4. MENEŽMENTOVÉ OPATRENIA ---
elif sekcia == "🗺️ Mapa - menežmentové opatrenia":
    st.subheader("🗺️ Menežmentové opatrenia")
    map_url = "https://mapky.github.io/mapa-menezment/"
    components.html(f'<iframe src="{map_url}" width="100%" height="600" style="border:none;"></iframe>', height=600)
    st.markdown(f"""
    <a href="{map_url}" target="_blank">
        <button style="background-color:#2b8a3e;color:white;border:none;padding:10px 20px;
                       border-radius:8px;font-size:16px;cursor:pointer;">
        🌍 Otvoriť mapu v novom okne</button>
    </a>
    """, unsafe_allow_html=True)


# --- 5. BIOTOPY ---
elif sekcia == "🗺️ Mapa - biotopy":
    st.subheader("🗺️ Biotopy")
    map_url = "https://mapky.github.io/mapa-biotopy/#10/49.3682/18.6386"
    components.html(f'<iframe src="{map_url}" width="100%" height="600" style="border:none;"></iframe>', height=600)
    st.markdown(f"""
    <a href="{map_url}" target="_blank">
        <button style="background-color:#2b8a3e;color:white;border:none;padding:10px 20px;
                       border-radius:8px;font-size:16px;cursor:pointer;">
        🌍 Otvoriť mapu v novom okne</button>
    </a>
    """, unsafe_allow_html=True)


# --- 6. ŽIVOČÍŠNE DRUHY ---
elif sekcia == "🦉 Mapa - výskyt živočíšnych druhov":
    st.subheader("🦉 Výskyt živočíšnych druhov")
    map_url = "https://mapky.github.io/mapa-zoologia/"
    components.html(f'<iframe src="{map_url}" width="100%" height="600" style="border:none;"></iframe>', height=600)
    st.markdown(f"""
    <a href="{map_url}" target="_blank">
        <button style="background-color:#2b8a3e;color:white;border:none;padding:10px 20px;
                       border-radius:8px;font-size:16px;cursor:pointer;">
        🌍 Otvoriť mapu v novom okne</button>
    </a>
    """, unsafe_allow_html=True)


# --- 7. RASTLINNÉ DRUHY ---
elif sekcia == "🌿 Mapa - výskyt rastlinných druhov":
    st.subheader("🌿 Výskyt rastlinných druhov")
    st.info("Tu môžeš doplniť obsah pre rastlinné druhy.")


# ========================== PÄTA ==========================
st.markdown("""
<hr>
<div style='text-align: center'>
    <b>Autor:</b> 🌿Róbert Sásik<br>
    <small>© 2025 Štátna ochrana prírody SR, <br>Chránená krajinná oblasť Kysuce</small>
</div>
""", unsafe_allow_html=True)
