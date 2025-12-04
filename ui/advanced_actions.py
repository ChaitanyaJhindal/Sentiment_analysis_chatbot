import streamlit as st
from services.chat_service import compute_final_sentiment, create_conversation_flow, generate_ai_summary_reply
from services.dependencies import groq

def render_advanced_actions(conversation_id, messages):
    with st.expander("🔧 Advanced Actions", expanded=False):
        st.markdown("#### Conversation Analysis")
        
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("📊 Final Sentiment", use_container_width=True):
                final = compute_final_sentiment(messages)
                if final:
                    emoji = "😊" if final['label'] == 'positive' else "😐" if final['label'] == 'neutral' else "😞"
                    st.success(f"{emoji} {final['label'].upper()} ({round(final['score'],2)}/5.0)")
                else:
                    st.warning("No user messages with sentiment yet")

        with col_b:
            if st.button("🔄 Create Flow", use_container_width=True):
                if groq is None:
                    st.error("⚠️ Groq not configured")
                else:
                    with st.spinner("Analyzing conversation..."):
                        try:
                            flow = create_conversation_flow(conversation_id, messages)
                            st.success("✅ Flow created")
                            
                            flow_text = flow if isinstance(flow, str) else flow.get("flow_text", str(flow))
                            with st.expander("📋 View Generated Flow", expanded=True):
                                st.markdown(flow_text)
                        except Exception as e:
                            st.error(f"❌ Failed: {str(e)}")

        with col_c:
            if st.button("💬 AI Summary Reply", use_container_width=True):
                if groq is None:
                    st.error("⚠️ Groq not configured")
                else:
                    with st.spinner("Generating AI summary reply..."):
                        try:
                            generate_ai_summary_reply(conversation_id, messages)
                            st.success("✅ AI summary reply added")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Failed: {str(e)}")
