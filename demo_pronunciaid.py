# demo_pronunciaid.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Configuración de la página
st.set_page_config(
    page_title="PronunciAId - Demo",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .practice-box {
        background-color: #f0f2f6;
        padding: 25px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    .feedback-good { color: #2ecc71; font-weight: bold; }
    .feedback-average { color: #f39c12; font-weight: bold; }
    .feedback-poor { color: #e74c3c; font-weight: bold; }
    .word-correct { color: #2ecc71; }
    .word-incorrect { color: #e74c3c; text-decoration: line-through; }
</style>
""", unsafe_allow_html=True)

# Función para simular análisis de audio
def analyze_pronunciation_simulated(target_text, difficulty):
    time.sleep(2)  # Simular procesamiento
    
    words = target_text.lower().split()
    total_words = len(words)
    
    # Base de errores comunes por palabra
    common_errors = {
        "hello": ["allo", "jello", "hellou"],
        "how": ["jao", "hao", "ho"],
        "are": ["ar", "er", "r"],
        "you": ["yu", "iu", "iou"],
        "today": ["todei", "tuday", "todai"],
        "good": ["gud", "god", "goode"],
        "morning": ["mornin", "moning", "morningu"],
        "thank": ["tank", "sank", "thanku"],
        "please": ["plis", "plees", "pleas"],
        "water": ["wader", "vater", "wateru"]
    }
    
    # Ajustar dificultad
    error_chance = {"Fácil": 0.2, "Media": 0.4, "Difícil": 0.6}[difficulty]
    
    # Generar texto reconocido con posibles errores
    recognized_words = []
    for word in words:
        if word in common_errors and random.random() < error_chance:
            recognized_words.append(random.choice(common_errors[word]))
        else:
            recognized_words.append(word)
    
    recognized_text = " ".join(recognized_words)
    
    # Calcular puntuación
    correct_words = sum(1 for w1, w2 in zip(recognized_words, words) if w1 == w2)
    score = int((correct_words / total_words) * 100)
    
    # Generar feedback
    if score >= 90:
        feedback = "¡Excelente! Tu pronunciación es casi perfecta."
        feedback_class = "feedback-good"
    elif score >= 70:
        feedback = "Buen trabajo, pero hay algunos detalles por mejorar."
        feedback_class = "feedback-average"
    else:
        feedback = "Sigue practicando. Presta atención a los sonidos difíciles."
        feedback_class = "feedback-poor"
    
    return {
        "recognized_text": recognized_text,
        "score": score,
        "feedback": feedback,
        "feedback_class": feedback_class,
        "correct_words": f"{correct_words}/{total_words}",
        "word_analysis": list(zip(words, recognized_words))
    }

# Función para generar visualización de audio
def generate_audio_waveform(duration=3):
    x = np.linspace(0, duration * np.pi, 1000)
    y = np.sin(x) + 0.3 * np.sin(3*x) + 0.1 * np.sin(5*x)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(x, y, color='#1f77b4', linewidth=2)
    ax.fill_between(x, y, color='#1f77b4', alpha=0.3)
    ax.set_ylim(-1.5, 1.5)
    ax.axis('off')
    return fig

# Interfaz principal
def main():
    st.markdown('<h1 class="main-header">🎤 PronunciAId - Demo Interactiva</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
        st.title("Opciones")
        difficulty = st.select_slider("Nivel de dificultad:", options=["Fácil", "Media", "Difícil"])
        st.divider()
        st.info("Esta es una demostración simulada. La versión final incluirá análisis real de audio.")
    
    # Selección de frase
    phrases = {
        "Saludo básico": "Hello how are you today",
        "Buenos días": "Good morning how are you",
        "Por favor": "Can I have water please",
        "Agradecimiento": "Thank you very much"
    }
    
    selected_phrase = st.selectbox("Selecciona una frase para practicar:", list(phrases.keys()))
    target_text = phrases[selected_phrase]
    
    st.markdown(f'<div class="practice-box"><h3>🎯 Frase para practicar:</h3><h4 style="color: #1f77b4; text-align: center;">"{target_text}"</h4></div>', unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎧 Escuchar pronunciación modelo", use_container_width=True):
            st.success("🔊 Reproduciendo audio de ejemplo...")
    with col2:
        record = st.button("⏺️ Simular grabación de mi voz", use_container_width=True, type="primary")
    
    # Procesamiento
    if record:
        st.session_state.recorded = True
    
    if 'recorded' in st.session_state and st.session_state.recorded:
        with st.spinner("Procesando tu audio..."):
            # Visualización de audio
            st.subheader("🎵 Tu grabación (simulada):")
            audio_viz = generate_audio_waveform()
            st.pyplot(audio_viz)
            
            # Análisis
            result = analyze_pronunciation_simulated(target_text, difficulty)
            st.session_state.result = result
        
        # Mostrar resultados
        if 'result' in st.session_state:
            result = st.session_state.result
            
            st.subheader("📊 Resultados del análisis:")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="score-card">
                    <h2>Puntuación: {result['score']}%</h2>
                    <p>Palabras correctas: {result['correct_words']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Nivel de dificultad", difficulty)
            
            with col3:
                st.metric("Tiempo de análisis", "2.3 segundos")
            
            # Feedback
            st.markdown(f'<p class="{result["feedback_class"]}">{result["feedback"]}</p>', unsafe_allow_html=True)
            
            # Análisis detallado por palabra
            st.subheader("🔍 Análisis detallado por palabra:")
            
            for target_word, recognized_word in result['word_analysis']:
                if target_word == recognized_word:
                    st.markdown(f'<p class="word-correct">✅ {target_word} - Correcto</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="word-incorrect">❌ {target_word} -> {recognized_word} - Needs practice</p>', unsafe_allow_html=True)
            
            # Gráfico de progreso simulado
            st.subheader("📈 Tu progreso simulado:")
            progress_data = {
                "Día": ["Lun", "Mar", "Mié", "Jue", "Vie"],
                "Puntuación": [65, 72, 68, 85, 88]
            }
            st.line_chart(progress_data, x="Día", y="Puntuación")
    
    # Información adicional
    with st.expander("💡 Acerca de esta demostración"):
        st.write("""
        Esta es una **demostración simulada** de PronunciAId, tu futuro tutor de inglés con IA.
        
        **En la versión final encontrarás:**
        - ✅ Análisis real de tu voz con Whisper AI
        - ✅ Grabación de audio real con tu micrófono
        - ✅ Feedback preciso por sonidos y fonemas
        - ✅ Seguimiento de progreso personalizado
        - ✅ Lecciones adaptativas según tu nivel
        
        **Tecnologías utilizadas:** Python, Streamlit, Whisper AI, Librosa
        """)

if __name__ == "__main__":
    main()