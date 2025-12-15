import streamlit as st
import pandas as pd
from PIL import Image
from datetime import date

# -----------------------------------------------------------------------------
# KONFIGURASI HALAMAN & TEMA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sistem Profil SPA",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Tema Dark & Purple/White
st.markdown("""
    <style>
    /* Mengubah warna latar belakang utama */
    .stApp {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    /* Mengubah warna sidebar */
    section[data-testid="stSidebar"] {
        background-color: #16213e;
    }
    /* Warna butang utama (Purple) */
    div.stButton > button:first-child {
        background-color: #6a0dad; 
        color: white;
        border-radius: 10px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #8a2be2;
        color: white;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #16213e;
        color: white;
        border-radius: 5px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #6a0dad;
        color: white;
    }
    h1, h2, h3 {
        color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PENGURUSAN DATA (SESSION STATE)
# Nota: Untuk kekal selamanya (permanent database), anda perlu sambungkan ke Google Sheets/SQL.
# Di sini kita guna Session State untuk simulasi.
# -----------------------------------------------------------------------------
if 'profile_data' not in st.session_state:
    st.session_state['profile_data'] = {}
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.title("🧬 Program Sains Perubatan Asas (SPA)")
st.markdown("---")

# -----------------------------------------------------------------------------
# TABS UTAMA
# -----------------------------------------------------------------------------
tab_dashboard, tab_form, tab_aktiviti, tab_subjek = st.tabs([
    "📊 Dashboard Profil", 
    "📝 Kemaskini Maklumat", 
    "📅 Aktiviti Program", 
    "📚 Subjek Diajar"
])

# =============================================================================
# TAB 1: DASHBOARD PROFIL (PAPARAN)
# =============================================================================
with tab_dashboard:
    if not st.session_state['submitted']:
        st.info("Tiada data profil dijumpai. Sila pergi ke tab 'Kemaskini Maklumat' untuk mengisi data.")
    else:
        data = st.session_state['profile_data']
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown("### Profil Pengajar")
            if data['image'] is not None:
                st.image(data['image'], caption="Gambar Profil", use_container_width=True)
            else:
                st.markdown("🚫 *Tiada Gambar*")
            
            st.markdown(f"**{data['nama']}**")
            st.caption(f"📧 {data['email']}")
            st.caption(f"📞 {data['phone']}")
            st.markdown(f"**Lantikan:** {data['tarikh_mula']}")
            
        with col2:
            st.header(f"Dr. {data['nama']}" if "PhD" in data['pendidikan'] else f"En/Pn {data['nama']}")
            st.subheader(f"Kepakaran: {data['kepakaran']}")
            
            with st.container():
                st.markdown("#### 🎓 Latar Belakang Akademik")
                st.success(f"{data['pendidikan']}")
                
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown("#### 📚 Penerbitan (Publications)")
                pubs = data['publication'].split('\n')
                for p in pubs:
                    if p.strip():
                        st.markdown(f"- {p}")
                        
            with col_b:
                st.markdown("#### 🏆 Kepimpinan (Leadership)")
                leads = data['leadership'].split('\n')
                for l in leads:
                    if l.strip():
                        st.markdown(f"- {l}")

# =============================================================================
# TAB 2: INPUT BORANG (LOGIK)
# =============================================================================
with tab_form:
    st.header("Maklumat Pengajar")
    
    with st.form("profiling_form"):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            nama = st.text_input("Nama Penuh", value=st.session_state['profile_data'].get('nama', ''))
            email = st.text_input("Emel Rasmi", value=st.session_state['profile_data'].get('email', ''))
            phone = st.text_input("No. Telefon", value=st.session_state['profile_data'].get('phone', ''))
            tarikh_mula = st.date_input("Tarikh Mula Lantikan", value=date.today())
            
        with col_f2:
            st.markdown("**Muat Naik Gambar Profil**")
            uploaded_file = st.file_uploader("Format JPG/PNG", type=['jpg', 'png', 'jpeg'])
            kepakaran = st.text_input("Bidang Kepakaran (cth: Anatomi, Fisiologi)", value=st.session_state['profile_data'].get('kepakaran', ''))
            
        st.markdown("---")
        st.subheader("Maklumat Akademik")
        # Multiselect untuk kelayakan
        options_edu = ["Diploma", "Post Basik", "Ijazah Sarjana Muda", "Master", "PhD"]
        pendidikan = st.multiselect("Pilih Kelayakan Akademik", options_edu, default=st.session_state['profile_data'].get('pendidikan_list', []))
        
        st.markdown("---")
        col_text1, col_text2 = st.columns(2)
        
        with col_text1:
            st.subheader("Senarai Publication")
            st.caption("Masukkan satu penerbitan per baris.")
            publication = st.text_area("Publication", height=150, value=st.session_state['profile_data'].get('publication', ''))
            
        with col_text2:
            st.subheader("Senarai Kepimpinan")
            st.caption("Masukkan satu jawatan/peranan per baris.")
            leadership = st.text_area("Kepimpinan", height=150, value=st.session_state['profile_data'].get('leadership', ''))
            
        # Butang Tindakan
        st.markdown("---")
        col_b1, col_b2, col_b3 = st.columns([1,1,4])
        
        submitted = st.form_submit_button("💾 Simpan & Hantar")
        
        if submitted:
            if not nama or not email:
                st.error("Sila isi Nama dan Emel sekurang-kurangnya.")
            else:
                # Simpan data ke session state
                st.session_state['profile_data'] = {
                    'nama': nama,
                    'email': email,
                    'phone': phone,
                    'tarikh_mula': tarikh_mula,
                    'image': uploaded_file if uploaded_file else st.session_state['profile_data'].get('image'),
                    'kepakaran': kepakaran,
                    'pendidikan': ", ".join(pendidikan),
                    'pendidikan_list': pendidikan,
                    'publication': publication,
                    'leadership': leadership
                }
                st.session_state['submitted'] = True
                st.success("Data berjaya disimpan dan dihantar! Sila semak tab Dashboard.")

# =============================================================================
# TAB 3: AKTIVITI PROGRAM SPA
# =============================================================================
with tab_aktiviti:
    st.header("📅 Aktiviti Program Sains Perubatan Asas")
    
    # Contoh data statik (boleh dijadikan dinamik nanti)
    activities = [
        {"Tarikh": "15 Dis 2025", "Aktiviti": "Bengkel Penyediaan Soalan SPA", "Tempat": "Bilik Mesyuarat Utama"},
        {"Tarikh": "20 Jan 2026", "Aktiviti": "Seminar Penyelidikan Kesihatan", "Tempat": "Auditorium"},
        {"Tarikh": "05 Feb 2026", "Aktiviti": "Lawatan Akademik Pelajar Tahun 1", "Tempat": "Hospital Besar"},
    ]
    df_act = pd.DataFrame(activities)
    
    # Papar dalam table yang kemas dengan background gelap
    st.table(df_act)
    
    st.markdown("### Galeri Aktiviti")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("Gambar Aktiviti 1")
    with c2: st.info("Gambar Aktiviti 2")
    with c3: st.info("Gambar Aktiviti 3")

# =============================================================================
# TAB 4: SUBJEK DIAJAR
# =============================================================================
with tab_subjek:
    st.header("📚 Subjek Diajar")
    
    col_sub1, col_sub2 = st.columns(2)
    
    with col_sub1:
        st.markdown("""
        ### Semester 1
        * **SPA101**: Anatomi Manusia & Fisiologi I
        * **SPA102**: Biokimia Asas
        * **SPA103**: Mikrobiologi & Parasitologi
        """)
        
    with col_sub2:
        st.markdown("""
        ### Semester 2
        * **SPA201**: Anatomi Manusia & Fisiologi II
        * **SPA202**: Patologi Asas
        * **SPA203**: Farmakologi
        """)

    st.warning("Senarai subjek dikemaskini mengikut sesi akademik 2025/2026.")