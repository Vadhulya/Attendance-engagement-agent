import streamlit as st
import cv2
import pandas as pd
import time
from modules.vision import VisionTracker
from modules.audio import AudioMonitor
from modules.fusion import EngagementFusion
from modules.agent import TeachingAssistantAgent

st.set_page_config(page_title="Classroom Intelligence Agent", layout="wide")
st.title("Multimodal Attendance & Engagement Agent")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("Attendance & Recommendations")
    attendance_display = st.empty()
    suggestion_box = st.empty()
    chart_display = st.empty()

with col1:
    st.subheader("Live Feed Analysis")
    video_frame = st.empty()

run_session = st.toggle("Start Session Capture")

if run_session:
    tracker = VisionTracker()
    audio = AudioMonitor()
    fusion = EngagementFusion(sustained_seconds_threshold=3)
    cap = cv2.VideoCapture(0)

    try:
        while run_session:
            ret, frame = cap.read()
            if not ret:
                st.error("Camera feed unavailable.")
                break

            # 1. Vision Analysis
            vision_data = tracker.process_frame(frame)
            
            # 2. Audio Analysis
            rms = audio.get_rms()

            # 3. Fusion & Logging
            metric = fusion.update(vision_data["detected_names"], rms)

            # 4. Agent Guidance
            suggestion = TeachingAssistantAgent.generate_feedback(fusion.engagement_history[-10:])

            # UI Rendering
            for name in vision_data["detected_names"]:
                cv2.putText(frame, f"Tracked: {name}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            video_frame.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

            attendance_display.write(
                f"**Confirmed Present:** {', '.join(fusion.confirmed_attendance) if fusion.confirmed_attendance else 'None yet'}"
            )
            suggestion_box.info(suggestion)

            df_metrics = pd.DataFrame(fusion.engagement_history[-30:])
            if not df_metrics.empty:
                chart_display.line_chart(df_metrics.set_index("timestamp")["engagement_score"])

            time.sleep(0.1)

    finally:
        cap.release()
        audio.close()