# app.py - Versión compatible con Python 3.13
import streamlit as st
import time
import random
from datetime import datetime

# Configuración
st.set_page_config(
    page_title="PronunciAId - Demo Mejorada", 
    page_icon="🎤", 
    layout="wide"
)

# CSS inline
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #1f77b4; text-align: center; margin-bottom: 1rem; }
    .score-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; color: white; text-align: center; margin: 10px 0; }
    .practice-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 15px 0; }
    .word-correct { background-color: #d4edda; color: #155724; padding: 8px 12px; border-radius: 20px; margin: 4px; display: inline-block; font-weight: bold; border: 2px solid #c3e6cb; }
    .word-incorrect { background-color: #f8d7da; color: #721c24; padding: 8px 12px; border-radius: 20px; margin: 4px; display: inline-block; font-weight: bold; border: 2px solid #f5c6cb; text-decoration: line-through; }
    .comparison-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    .comparison-table th { background-color: #667eea; color: white; padding: 10px; text-align: left; }
    .comparison-table td { padding: 10px; border-bottom: 1px solid #ddd; }
    .correct-row { background-color: #d4edda; }
    .incorrect-row { background-color: #f8d7da; }
</style>
""", unsafe_allow_html=True)

# Base de errores comunes
COMMON_ERRORS = {
    "hello": ["allo", "jello", "hellou"], "how": ["hao", "jau", "ho"], 
    "are": ["ar", "er", "r"], "you": ["yu", "iu", "iou"], "today": ["todei", "tuday", "todai"],
    "good": ["gud", "god", "goode"], "thank": ["tank", "sank", "thanku"], "please": ["plis", "plees", "pleas"],
    "water": ["wader", "vater", "wateru"], "very": ["bery", "veri", "verry"], "much": ["mach", "mush", "mouch"]
}

def analyze_pronunciation(target_text, difficulty):
    time.sleep(1.5)
    words = target_text.lower().split()
    error_chance = {"Fácil": 0.2, "Media": 0.4, "Difícil": 0.6}[difficulty]
    
    recognized_words = []
    word_status = []
    
    for word in words:
        if random.random() < error_chance and word in COMMON_ERRORS:
            error_version = random.choice(COMMON_ERRORS[word])
            recognized_words.append(error_version)
            word_status.append({"target": word, "recognized": error_version, "correct": False})
        else:
            recognized_words.append(word)
            word_status.append({"target": word, "recognized": word, "correct": True})
    
    correct_count = sum(1 for status in word_status if status["correct"])
    score = int((correct_count / len(words)) * 100)
    
    return {
        "recognized_text": " ".join(recognized_words),
        "score": score,
        "correct_words": f"{correct_count}/{len(words)}",
        "word_analysis": word_status,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

def display_word_comparison(word_analysis):
    st.subheader("🔍 Análisis palabra por palabra:")
    
    # Mostrar palabras con colores
    st.write("**Texto reconocido:**")
    html_words = ""
    for status in word_analysis:
        if status["correct"]:
            html_words += f'<span class="word-correct">{status["recognized"]}</span> '
        else:
            html_words += f'<span class="word-incorrect">{status["recognized"]}</span> '
    st.markdown(html_words, unsafe_allow_html=True)
    
    # Tabla detallada
    st.subheader("📋 Detalle de correcciones:")
    table_html = """
    <table class="comparison-table">
        <tr><th>Palabra Objetivo</th><th>Palabra Reconocida</th><th>Estado</th></tr>
    """
    
    for status in word_analysis:
        row_class = "correct-row" if status["correct"] else "incorrect-row"
        status_text = "✅ Correcto" if status["correct"] else "❌ Incorrecto"
        table_html += f"""
        <tr class="{row_class}">
            <td><strong>{status['target']}</strong></td>
            <td>{status['recognized']}</td>
            <td>{status_text}</td>
        </tr>
        """
    
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🎤 PronunciAId - Demo Compatible</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("⚙️ Configuración")
        difficulty = st.radio("Nivel de dificultad:", ["Fácil", "Media", "Difícil"], index=1)
        st.info("✅ Ahora compatible con Python 3.13")
    
    phrases = [
        "Hello how are you today",
        "Good morning how are you", 
        "Thank you very much",
        "Can I have water please"
    ]
    
    selected_phrase = st.selectbox("🎯 Selecciona una frase:", phrases)
    st.markdown(f'<div class="practice-box"><h3>📝 Frase objetivo: "{selected_phrase}"</h3></div>', unsafe_allow_html=True)
    
    if st.button("🔍 Analizar pronunciación", type="primary"):
        with st.spinner("Analizando..."):
            result = analyze_pronunciation(selected_phrase, difficulty)
            
            st.markdown(f"""
            <div class="score-card">
                <h2>Puntuación: {result['score']}%</h2>
                <p>Palabras correctas: {result['correct_words']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            display_word_comparison(result['word_analysis'])

if __name__ == "__main__":
    main()
