# app.py - Versión optimizada sin matplotlib
import streamlit as st
import numpy as np
import time
import random
from datetime import datetime

# Configuración
st.set_page_config(
    page_title="PronunciAId - Demo Funcional",
    page_icon="🎤",
    layout="wide"
)

# CSS inline minimalista
st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        color: #1f77b4; 
        text-align: center;
        margin-bottom: 1rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .practice-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
    }
    .word-correct { color: #2ecc71; font-weight: bold; }
    .word-incorrect { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Función de análisis simplificada
def analyze_pronunciation(target_text, difficulty):
    time.sleep(1.5)  # Simular procesamiento
    
    words = target_text.lower().split()
    error_level = {"Fácil": 0.1, "Media": 0.3, "Difícil": 0.5}[difficulty]
    
    # Generar resultado con posibles errores
    recognized_words = []
    for word in words:
        if random.random() < error_level:
            # Simular error común
            error_version = word + random.choice(["", "e", "a", "u"])
            recognized_words.append(error_version)
        else:
            recognized_words.append(word)
    
    recognized_text = " ".join(recognized_words)
    correct_count = sum(1 for i, word in enumerate(words) if word == recognized_words[i])
    score = int((correct_count / len(words)) * 100)
    
    return {
        "recognized_text": recognized_text,
        "score": score,
        "correct_words": f"{correct_count}/{len(words)}",
        "word_analysis": list(zip(words, recognized_words)),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

# Interfaz principal
def main():
    st.markdown('<h1 class="main-header">🎤 PronunciAId - Demo Funcional</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuración")
        difficulty = st.radio("Nivel de dificultad:", ["Fácil", "Media", "Difícil"], index=1)
        st.divider()
        st.success("✅ Entorno funcionando correctamente")
        st.info("Esta demo simula el análisis de pronunciación que hará la IA")
    
    # Selección de frase
    phrases = [
        "Hello how are you today",
        "Good morning how are you",
        "Thank you very much",
        "Can I have water please",
        "I would like to practice english"
    ]
    
    selected_phrase = st.selectbox("🎯 Selecciona una frase para practicar:", phrases)
    
    st.markdown(f'''
    <div class="practice-box">
        <h3>📝 Frase seleccionada:</h3>
        <h4 style="color: #1f77b4;">"{selected_phrase}"</h4>
    </div>
    ''', unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎧 Escuchar pronunciación", use_container_width=True):
            st.toast("Reproduciendo audio de ejemplo...")
    with col2:
        analyze = st.button("🔍 Analizar mi pronunciación", type="primary", use_container_width=True)
    
    # Procesamiento
    if analyze:
        with st.spinner(f"Analizando pronunciación con nivel {difficulty}..."):
            result = analyze_pronunciation(selected_phrase, difficulty)
            
            # Mostrar resultados
            st.markdown(f"""
            <div class="score-card">
                <h2>Puntuación: {result['score']}%</h2>
                <p>Palabras correctas: {result['correct_words']}</p>
                <small>Análisis a las {result['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Análisis detallado
            st.subheader("📊 Análisis detallado:")
            for target_word, recognized_word in result['word_analysis']:
                if target_word == recognized_word:
                    st.markdown(f'<p class="word-correct">✅ {target_word}</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p class="word-incorrect">❌ {target_word} → {recognized_word}</p>', unsafe_allow_html=True)
            
            # Progreso simulado
            st.subheader("📈 Tu progreso:")
            days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
            scores = [60, 65, 70, 68, 75, result['score'], 80]
            chart_data = {"Día": days, "Puntuación": scores}
            st.line_chart(chart_data, x="Día", y="Puntuación", height=300)
    
    # Información de la demo
    with st.expander("ℹ️ Acerca de esta demo"):
        st.write("""
        **Características de esta versión:**
        - ✅ 100% compatible con GitHub Codespaces
        - ✅ Sin dependencias problemáticas
        - ✅ Interfaz responsive y profesional
        - ✅ Simulación realista del análisis de pronunciación
        
        **En la versión final con IA:**
        - Análisis real con Whisper AI
        - Grabación de audio real
        - Feedback por fonemas
        - Seguimiento de progreso avanzado
        """)

if __name__ == "__main__":
    main()
