import streamlit as st
from builder.prompt_generator import generate_prompt
from builder.config_generator import generate_config
from builder.github_handler import prepare_ghl_webhook_payload, push_to_github
import base64
import json

st.set_page_config(page_title="Bot Builder Agent", layout="centered")
st.title("🤖 Bot Builder Agent")

bot_name = st.text_input("Bot Name")
bot_role = st.selectbox("Bot Type", ["Recruiting Coach", "Motivator", "Closer", "Admin Helper", "Scheduler"])
tone = st.selectbox("Tone", ["Professional", "Friendly", "Aggressive", "Empathetic", "Drill Sergeant"])
channel = st.radio("Target Platform", ["Streamlit", "ChatGPT", "Export Only"])
goal = st.text_area("Bot Goal", help="Describe what this bot should help with")

# GHL Webhook field
st.subheader("📤 Optional: Send to GoHighLevel Webhook")
ghl_webhook_url = st.text_input("GHL Webhook URL (Optional)")

# GitHub integration fields
st.subheader("📁 Optional: Push to GitHub")
github_token = st.text_input("GitHub Token", type="password")
github_repo = st.text_input("GitHub Repo (e.g., username/repo)")
github_path = st.text_input("Folder Path in Repo", value="bots")

if st.button("Build Bot"):
    prompt = generate_prompt(bot_name, bot_role, tone, goal)
    config_json = generate_config(bot_name, prompt, channel)

    st.success("✅ Bot Built Successfully!")
    st.subheader("Generated Prompt")
    st.text_area("📋 Prompt", prompt, height=300)

    st.subheader("Download Configuration")
    st.download_button(
        label="📥 Download Config (.json)",
        data=config_json,
        file_name=f"{bot_name}_config.json",
        mime="application/json"
    )

    # Send to GHL webhook if URL provided
    if ghl_webhook_url:
        payload = prepare_ghl_webhook_payload(bot_name, prompt, tone, bot_role, goal)
        try:
            import requests
            response = requests.post(ghl_webhook_url, json=payload)
            if response.status_code == 200:
                st.success("✅ Sent to GHL Webhook!")
            else:
                st.warning(f"⚠️ GHL Webhook Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error sending to webhook: {e}")

    # Push to GitHub if token and repo provided
    if github_token and github_repo:
        file_name = f"{bot_name}_config.json"
        content_encoded = base64.b64encode(config_json.encode("utf-8")).decode("utf-8")
        status, result = push_to_github(github_repo, github_path, file_name, content_encoded, github_token)
        if status in [200, 201]:
            st.success("✅ Config pushed to GitHub!")
        else:
            st.warning(f"⚠️ GitHub Push Error: {result}")
