# app.py - Versión con visualización mejorada de palabras
import streamlit as st
import numpy as np
import time
import random
from datetime import datetime

# Configuración
st.set_page_config(
    page_title="PronunciAId - Demo Mejorada",
    page_icon="🎤",
    layout="wide"
)

# CSS inline mejorado
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
    .word-correct { 
        background-color: #d4edda; 
        color: #155724; 
        padding: 8px 12px;
        border-radius: 20px;
        margin: 4px;
        display: inline-block;
        font-weight: bold;
        border: 2px solid #c3e6cb;
    }
    .word-incorrect { 
        background-color: #f8d7da; 
        color: #721c24; 
        padding: 8px 12px;
        border-radius: 20px;
        margin: 4px;
        display: inline-block;
        font-weight: bold;
        border: 2px solid #f5c6cb;
        text-decoration: line-through;
    }
    .word-correction { 
        color: #856404; 
        background-color: #fff3cd;
        padding: 4px 8px;
        border-radius: 12px;
        margin-left: 8px;
        font-size: 0.9em;
    }
    .results-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 15px 0;
    }
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    .comparison-table th {
        background-color: #667eea;
        color: white;
        padding: 10px;
        text-align: left;
    }
    .comparison-table td {
        padding: 10px;
        border-bottom: 1px solid #ddd;
    }
    .correct-row {
        background-color: #d4edda;
    }
    .incorrect-row {
        background-color: #f8d7da;
    }
</style>
""", unsafe_allow_html=True)

# Base de datos de errores comunes más realista
COMMON_ERRORS = {
    "hello": ["allo", "jello", "hellou", "elo"],
    "how": ["hao", "jau", "ho", "howe"],
    "are": ["ar", "er", "r", "aree"],
    "you": ["yu", "iu", "iou", "youu"],
    "today": ["todei", "tuday", "todai", "tode"],
    "good": ["gud", "god", "goode", "goot"],
    "morning": ["mornin", "moning", "morningu", "mornan"],
    "thank": ["tank", "sank", "thanku", "sankyou"],
    "please": ["plis", "plees", "pleas", "plise"],
    "water": ["wader", "vater", "wateru", "wata"],
    "very": ["bery", "veri", "verry", "wery"],
    "much": ["mach", "mush", "mouch", "mutch"],
    "can": ["ken", "canne", "kan", "cann"],
    "have": ["jaf", "hav", "hef", "havee"],
    "i": ["ai", "ee", "ay", "ie"],
    "would": ["wud", "woulde", "wold", "woud"],
    "like": ["laik", "likee", "laik", "lyke"],
    "practice": ["practis", "practise", "practicee", "practize"],
    "english": ["inglish", "englis", "englishu", "anglish"]
}

def analyze_pronunciation(target_text, difficulty):
    time.sleep(1.5)
    words = target_text.lower().split()
    
    # Ajustar probabilidad de error según dificultad
    error_chance = {"Fácil": 0.2, "Media": 0.4, "Difícil": 0.6}[difficulty]
    
    recognized_words = []
    word_status = []  # Para trackear estado de cada palabra
    
    for word in words:
        if random.random() < error_chance and word in COMMON_ERRORS:
            # Seleccionar un error común para esta palabra
            error_version = random.choice(COMMON_ERRORS[word])
            recognized_words.append(error_version)
            word_status.append({
                "target": word,
                "recognized": error_version,
                "correct": False,
                "type": "common_error"
            })
        elif random.random() < error_chance * 0.5:
            # Error aleatorio (menos común)
            error_version = word + random.choice(["e", "a", "u", "i"])
            recognized_words.append(error_version)
            word_status.append({
                "target": word,
                "recognized": error_version,
                "correct": False,
                "type": "random_error"
            })
        else:
            # Palabra correcta
            recognized_words.append(word)
            word_status.append({
                "target": word,
                "recognized": word,
                "correct": True,
                "type": "correct"
            })
    
    recognized_text = " ".join(recognized_words)
    correct_count = sum(1 for status in word_status if status["correct"])
    score = int((correct_count / len(words)) * 100)
    
    return {
        "recognized_text": recognized_text,
        "score": score,
        "correct_words": f"{correct_count}/{len(words)}",
        "word_analysis": word_status,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

def display_word_comparison(word_analysis):
    """Muestra la comparación de palabras de forma visual"""
    
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
        <tr>
            <th>Palabra Objetivo</th>
            <th>Palabra Reconocida</th>
            <th>Estado</th>
            <th>Tipo de Error</th>
        </tr>
    """
    
    for i, status in enumerate(word_analysis):
        row_class = "correct-row" if status["correct"] else "incorrect-row"
        status_text = "✅ Correcto" if status["correct"] else "❌ Incorrecto"
        error_type = "-" if status["correct"] else status["type"].replace("_", " ").title()
        
        table_html += f"""
        <tr class="{row_class}">
            <td><strong>{status['target']}</strong></td>
            <td>{status['recognized']}</td>
            <td>{status_text}</td>
            <td>{error_type}</td>
        </tr>
        """
    
    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Estadísticas resumidas
    correct_count = sum(1 for status in word_analysis if status["correct"])
    total_count = len(word_analysis)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Palabras correctas", f"{correct_count}/{total_count}")
    with col2:
        st.metric("Porcentaje de acierto", f"{(correct_count/total_count)*100:.1f}%")
    with col3:
        error_count = total_count - correct_count
        st.metric("Errores", error_count)

def main():
    st.markdown('<h1 class="main-header">🎤 PronunciAId - Análisis Detallado</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("⚙️ Configuración")
        difficulty = st.radio("Nivel de dificultad:", ["Fácil", "Media", "Difícil"], index=1)
        
        st.divider()
        st.info("**Modo de demostración:** Los errores se generan automáticamente según el nivel de dificultad")
        st.success("✅ Análisis visual mejorado activado")
    
    # Selección de frase
    phrases = [
        "Hello how are you today",
        "Good morning how are you",
        "Thank you very much",
        "Can I have water please",
        "I would like to practice english",
        "How is the weather today",
        "Where is the nearest restaurant",
        "What time does the train leave"
    ]
    
    selected_phrase = st.selectbox("🎯 Selecciona una frase para practicar:", phrases)
    
    st.markdown(f'''
    <div class="practice-box">
        <h3>📝 Frase objetivo:</h3>
        <h4 style="color: #1f77b4;">"{selected_phrase}"</h4>
    </div>
    ''', unsafe_allow_html=True)
    
    # Botones de acción
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎧 Escuchar pronunciación modelo", use_container_width=True):
            st.toast("Audio de ejemplo reproducido")
    with col2:
        analyze = st.button("🔍 Analizar pronunciación", type="primary", use_container_width=True)
    
    # Procesamiento y resultados
    if analyze:
        with st.spinner(f"Analizando con nivel {difficulty}..."):
            result = analyze_pronunciation(selected_phrase, difficulty)
            
            # Tarjeta de puntuación principal
            st.markdown(f"""
            <div class="score-card">
                <h2>Puntuación General: {result['score']}%</h2>
                <p>Palabras correctas: {result['correct_words']}</p>
                <small>Análisis realizado a las {result['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar comparación visual mejorada
            display_word_comparison(result['word_analysis'])
            
            # Feedback adicional
            st.subheader("💡 Recomendaciones:")
            incorrect_words = [status for status in result['word_analysis'] if not status['correct']]
            
            if not incorrect_words:
                st.success("¡Perfecto! Todas las palabras fueron pronunciadas correctamente.")
            else:
                st.warning("**Palabras para practicar:**")
                for status in incorrect_words:
                    st.write(f"- **{status['target']}** → Se escuchó como: '{status['recognized']}'")
                
                st.info("**Sugerencia:** Intenta grabar de nuevo prestando atención a las palabras marcadas.")

if __name__ == "__main__":
    main()
