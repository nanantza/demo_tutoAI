# app.py (usa este nombre que Streamlit reconoce automáticamente)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Configuración con opciones más compatibles
st.set_page_config(
    page_title="PronunciAId - Demo",
    page_icon="🎤",
    layout="wide"
)

# CSS inline para evitar dependencias
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; text-align: center; }
    .score-card { background: #667eea; padding: 20px; border-radius: 10px; color: white; text-align: center; }
    .practice-box { background-color: #f0f2f6; padding: 25px; border-radius: 10px; }
    .feedback-good { color: #2ecc71; font-weight: bold; }
    .feedback-average { color: #f39c12; font-weight: bold; }
    .feedback-poor { color: #e74c3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Función simplificada para mejor compatibilidad
def analyze_pronunciation_simulated(target_text, difficulty):
    time.sleep(1.5)
    words = target_text.lower().split()
    
    # Errores simulados más simples
    error_chance = {"Fácil": 0.2, "Media": 0.4, "Difícil": 0.6}[difficulty]
    recognized_words = []
    
    for word in words:
        if random.random() < error_chance:
            common_errors = {
                "hello": "allo", "how": "hao", "are": "ar", 
                "you": "yu", "today": "todei", "good": "gud",
                "morning": "moning", "thank": "tank", "please": "plis"
            }
            recognized_words.append(common_errors.get(word, word + "e"))
        else:
            recognized_words.append(word)
    
    recognized_text = " ".join(recognized_words)
    correct_words = sum(1 for w1, w2 in zip(recognized_words, words) if w1 == w2)
    score = int((correct_words / len(words)) * 100)
    
    # Feedback
    if score >= 90: feedback = "¡Excelente! Pronunciación casi perfecta."
    elif score >= 70: feedback = "Buen trabajo, pero practica más."
    else: feedback = "Sigue practicando. Tú puedes."
    
    return {
        "recognized_text": recognized_text,
        "score": score,
        "feedback": feedback,
        "correct_words": f"{correct_words}/{len(words)}"
    }

# Interfaz principal
def main():
    st.markdown('<h1 class="main-header">🎤 PronunciAId - Demo</h1>', unsafe_allow_html=True)
    
    # Sidebar simple
    with st.sidebar:
        st.title("Opciones")
        difficulty = st.radio("Dificultad:", ["Fácil", "Media", "Difícil"])
    
    # Frases para practicar
    phrase = st.selectbox("Selecciona frase:", [
        "Hello how are you today",
        "Good morning how are you", 
        "Thank you very much",
        "Can I have water please"
    ])
    
    st.markdown(f'<div class="practice-box"><h3>🎯 Frase a practicar: "{phrase}"</h3></div>', unsafe_allow_html=True)
    
    # Botones
    if st.button("⏺️ Simular grabación", type="primary"):
        with st.spinner("Analizando..."):
            result = analyze_pronunciation_simulated(phrase, difficulty)
            
            # Resultados
            st.markdown(f"""
            <div class="score-card">
                <h2>Puntuación: {result['score']}%</h2>
                <p>Palabras correctas: {result['correct_words']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**Texto reconocido:** {result['recognized_text']}")
            st.write(f"**Feedback:** {result['feedback']}")
            
            # Gráfico simple de progreso
            st.line_chart({"Día": [1,2,3,4,5], "Puntuación": [60,65,70,75,result['score']]})

if __name__ == "__main__":
    main()