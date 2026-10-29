class TeachingAssistantAgent:
    @staticmethod
    def generate_feedback(recent_metrics):
        if not recent_metrics:
            return "Gathering live session data..."

        avg_score = sum(m["engagement_score"] for m in recent_metrics) / len(recent_metrics)
        avg_rms = sum(m["audio_rms"] for m in recent_metrics) / len(recent_metrics)

        if avg_score < 40.0:
            return (
                "⚠️ Attention Dip Detected: Sustained engagement dropped below 40%. "
                "Recommendation: Pause lecture and ask a polling question or prompt a 2-minute peer discussion."
            )
        elif avg_rms > 1200.0:
            return (
                "🔊 High Ambient Activity: Audio energy is elevated. "
                "Recommendation: Transition discussion back to instructor-led moderation."
            )
        else:
            return "✅ Optimal Dynamic: Classroom attention and noise balance are within standard target thresholds."