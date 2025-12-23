import streamlit as st
import requests

# Configuration
API_URL = "http://127.0.0.1:8000/query"
REQUEST_TIMEOUT = 120

# Page Configuration
st.set_page_config(
    page_title="Engineering Operations RAG Assistant",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# Header
st.title(" Engineering Operations Assistant")
st.caption("RAG-powered assistant for SRE / Platform / DevOps")



# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        
        
        if msg["role"] == "assistant" and "sources" in msg:
            with st.expander(" Sources"):
                for source in msg["sources"]:
                    st.markdown(
                        f"- **{source['source_file']}** "
                        f"({source['category']} - {source['section']})"
                    )

# User input
prompt = st.chat_input("Ask any question about SRE / Platform / DevOps and Production")


if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
        
            with st.spinner("Thinking..."):
                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=REQUEST_TIMEOUT
                )
            
            
            response.raise_for_status()
            
            data = response.json()
            
            answer = data.get("answer", "No answer received")
            sources = data.get("sources", [])
            
            
            # Display answer
            response_placeholder.markdown(answer)
            
            
            # Display sources in expander
            if sources:
                with st.expander(" Sources"):
                    for source in sources:
                        st.markdown(
                            f"- **{source['source_file']}** "
                            f"({source['category']} - {source['section']})"
                        )
            
            # Save to history with sources
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })
            
            
        # Timeout error
        except requests.exceptions.Timeout:
            error_msg = " Request timed out. Please try again."
            response_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
       
            
        # Connection error
        except requests.exceptions.ConnectionError:
            error_msg = " Cannot connect to the backend. Please ensure the API is running."
            response_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
            
        # HTTP error
        except requests.exceptions.HTTPError as e:
            error_msg = f" API Error: {e.response.status_code} - {e.response.text}"
            response_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })

        
        except Exception as e:
            error_msg = f" Error: {str(e)}"
            response_placeholder.error(error_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })


# Sidebar with additional info
with st.sidebar:
    st.header("ℹ About")
    st.markdown("""
    This assistant helps you find information about:
    - Site Reliability Engineering (SRE)
    - Platform Engineering
    - DevOps practices
    - Production operations
    """)
    
    
    st.divider()
    
    if st.button(" Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.caption(f"Total messages: {len(st.session_state.messages)}")