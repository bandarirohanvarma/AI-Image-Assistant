import streamlit as st
from vision import analyze_image, ask_question
from PIL import Image

st.set_page_config(page_title="AI Image Assistant")

st.title("🧠 AI Image Assistant")

# session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "image_uploaded" not in st.session_state:
    st.session_state.image_uploaded = None


uploaded_file = st.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"]
)

# show image
if uploaded_file:

    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")

    st.session_state.image_uploaded = uploaded_file

    if st.button("Analyze Image"):

        summary = analyze_image(uploaded_file)

        st.session_state.messages.append(
            {"role": "assistant", "content": summary}
        )


# chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# chat input
if prompt := st.chat_input("Ask something about the image..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        if st.session_state.image_uploaded:

            answer = ask_question(
                st.session_state.image_uploaded,
                prompt
            )

            st.write(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )