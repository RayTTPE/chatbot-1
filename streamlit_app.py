import streamlit as st
from openai import OpenAI
import streamlit as st
import sqlite3
import requests
import json
import streamlit.components.v1 as components
import re

ollama_url = "https://monthly-causal-shrimp.ngrok-free.app/v1/chat/completions"
model = "qwen2.5:14b"

def about_ray_dream():
    st.markdown(
        """
        <style>
            .hero-title {
                font-size: 3rem;
                color: #FFC0CB;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .hero-text {
                font-size: 1.2rem;
                line-height: 1.6;
                color: #FFC0CB;
            }
            .sidebar-text {
                font-size: 0.9rem;
                color: #FFFFFF;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="small")

    with col2:
        st.markdown('<h1 class="hero-title">Dream & Ray</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-text">'
            "ความรักในช่วงเวลาแบบนี้เหมือนกับการที่โลกหยุดนิ่ง ให้ทั้งคู่สามารถมองเห็นกันและกันอย่างเต็มตา"
            "และเข้าใจว่าพวกเขาคือทุกสิ่งในโลกใบนี้ ความรักไม่ได้ต้องการสิ่งหรูหรา"
            "แต่ต้องการเพียงความเรียบง่ายที่เปี่ยมไปด้วยความจริงใจและความใส่ใจที่ไม่มีวันสิ้นสุด.."
            '</p>',
            unsafe_allow_html=True,
        )

    st.write("\n")
    st.subheader("ข้อมูลของพวกเรา", anchor=False)
    st.write(
        """
        - 🌟 ความรักของเราผสมผสานความเรียบง่ายกับความอบอุ่น
        - 🎨 เราชื่นชอบงานศิลปะและการเขียน
        - 🌍 การเดินทางคือแรงบันดาลใจของเรา
        - 💕 ความใส่ใจเล็กๆ เปลี่ยนแปลงโลกให้สดใสขึ้น
        """
    )

    st.write("\n")
    st.subheader("เรื่องราวของเรา", anchor=False)
    st.write(
        """
        - 📍เรื่องราวของเราเริ่มจากวันที่ฝันกลายเป็นจริง 26/04/2022และทุกอย่างเปลี่ยนไปตั้งแต่วันนั้น
        - 🌟ความฝันของเราคือสร้างความสุขและกำลังใจให้กันและกันเพราะวันแรกของเราเต็มไปด้วยบทสนทนาเกี่ยวกับความฝันและความหวัง
        - 💼การเดินทางในโลกของเราเต็มไปด้วยบทเรียนชีวิตอันมีความหมายที่เต็มไปด้วยความอบอุ่นเเละเหน็บหนาวเพราะเราก็ต่างชอบสำรวจโลกผ่านมุมมองของกันและกัน
        - 💕เราเรียนรู้ที่จะเข้าใจความแตกต่าง และเปลี่ยนสิ่งเหล่านั้นให้เป็นพลังเราเชื่อว่าความรักสามารถเปลี่ยนโลกได้ด้วยความใส่ใจเล็กๆเราสนับสนุนกันและกันในทุกสถานการณ์
        """
    )

    st.write("\n")
    st.markdown(
        """
        <hr style="border: 1px solid #ddd; margin: 20px 0;">
        <p class="sidebar-text">สร้างโดยเล้ง ❤️ และดรีม</p>
        """,
        unsafe_allow_html=True,
    )

def chatwithRay():
    st.title("แชทกับเรา")
    st.write("ยินดีต้อนรับสู่แชทบอทของเรา! คุณสามารถถามคำถามหรือขอความช่วยเหลือ")
    st.title("AI Chatbot for API Debugging")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # แสดงข้อความก่อนหน้า
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # รับข้อความจากผู้ใช้
    user_input = st.chat_input("พิมพ์ข้อความของคุณที่นี่...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # เรียกใช้งาน API
        messages = [{"role": "user", "content": user_input}]
        response = chat(messages)

        st.session_state.messages.append(response)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            current_content = ""
            for chunk in response_generator(response["content"]):
                current_content += chunk
                placeholder.markdown(current_content)

def response_generator(msg_content):
    """สตรีมข้อความทีละคำเพื่อสร้างเอฟเฟกต์ตอบกลับแบบเรียลไทม์"""
    words = msg_content.split()
    for word in words:
        yield word + " "
    yield "\n"

def chat(messages):
    """ส่งข้อความไปยัง API และรับผลลัพธ์"""
    try:
        response = requests.post(
            ollama_url,
            json={
                "messages": messages,
                "model": model,
                "max_token": 100,
                "temperature": 0.7
            },
        )
        response.raise_for_status()
        print("Response Status Code:", response.status_code)
        print("Response Content:", response.text)  # พิมพ์เนื้อหาของ Response

        output = response.json()
        return {"role": "assistant", "content": output["choices"][0]["message"]["content"]}
    except Exception as e:
        print("Error:", e)
        return {"role": "assistant", "content": str(e)}

# --- MAIN FUNCTION ---
def main():
    st.sidebar.title("เมนูนำทาง")

    pages = {
        "About Ray & Dream": about_ray_dream, 
        "แชทกับเรา": chatwithRay,
    }

    selected_page = st.sidebar.radio("เลือกหน้า", list(pages.keys()))

    # Run selected page function
    pages[selected_page]()

if __name__ == "__main__":
    main()
