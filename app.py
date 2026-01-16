import streamlit as st
import uuid
from datetime import datetime

# Custom CSS for best UI/UX
st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 8px 4px;
        cursor: pointer;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .stTextInput>div>input {
        border-radius: 8px;
        padding: 12px;
        font-size: 16px;
        border: 2px solid #ddd;
        transition: border-color 0.3s;
    }
    .stTextInput>div>input:focus {
        border-color: #4CAF50;
        outline: none;
    }
    .stCheckbox {
        margin: 10px 0;
    }
    .task-item {
        background-color: #fff;
        padding: 12px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.3s ease;
    }
    .task-item:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .task-text {
        flex-grow: 1;
        margin-left: 10px;
        font-size: 16px;
        word-break: break-word;
    }
    .task-done {
        text-decoration: line-through;
        color: #888;
    }
    .delete-btn {
        background-color: #f44336;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .delete-btn:hover {
        background-color: #d32f2f;
    }
    h1 {
        color: #fff;
        text-align: center;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .tracker-container {
        max-width: 760px;
        margin: auto;
        padding: 28px;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .add-task-section {
        margin-bottom: 18px;
        text-align: center;
    }
    .tasks-section {
        margin-top: 20px;
    }
    .no-tasks {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-top: 20px;
    }
    .meta {
        color: #444;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []  # each task: {'id','text','done','created_at'}

# Utility functions
def add_task(text: str):
    text = text.strip()
    if not text:
        st.error("Task cannot be empty!")
        return
    task = {
        "id": uuid.uuid4().hex,
        "text": text,
        "done": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    st.session_state.tasks.append(task)
    st.success("Task added successfully! ✅")

def delete_task_by_id(task_id: str):
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task_id]
    st.success("Task deleted 🗑️")
    st.experimental_rerun()

def update_task_text(task_id: str, new_text: str):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["text"] = new_text.strip()
            st.success("Task updated ✏️")
            break
    st.experimental_rerun()

def toggle_task_done(task_id: str, value: bool):
    for t in st.session_state.tasks:
        if t["id"] == task_id:
            t["done"] = value
            break

# Main app layout
st.markdown('<div class="tracker-container">', unsafe_allow_html=True)
st.title("📝 To-Do List Tracker")
st.write("Organize your tasks effortlessly. Add, check off, and delete items with style!")

# Add task form
st.markdown('<div class="add-task-section">', unsafe_allow_html=True)
st.subheader("➕ Add a New Task")
with st.form("add_task_form", clear_on_submit=True):
    new_task = st.text_input("Enter your task", placeholder="e.g., Finish homework")
    submitted = st.form_submit_button("Add Task")
    if submitted:
        add_task(new_task)
st.markdown("</div>", unsafe_allow_html=True)

# Controls: filter and counts
st.markdown('<div class="tasks-section">', unsafe_allow_html=True)
st.subheader("📋 Your Tasks")
total = len(st.session_state.tasks)
done_count = sum(1 for t in st.session_state.tasks if t["done"])
col_info, col_filter = st.columns([0.6, 0.4])
with col_info:
    st.markdown(f"<div class='meta'>Total: <b>{total}</b> • Done: <b>{done_count}</b></div>", unsafe_allow_html=True)
with col_filter:
    view = st.selectbox("View", ["All", "Active", "Done"], index=0)

# Filter tasks
if view == "Active":
    tasks_to_show = [t for t in st.session_state.tasks if not t["done"]]
elif view == "Done":
    tasks_to_show = [t for t in st.session_state.tasks if t["done"]]
else:
    tasks_to_show = list(st.session_state.tasks)

if not tasks_to_show:
    st.markdown('<div class="no-tasks">No tasks yet. Add one above to get started! 🎉</div>', unsafe_allow_html=True)
else:
    # Show tasks (stable order: newest last)
    for task in tasks_to_show:
        task_id = task["id"]
        container = st.container()
        with container:
            cols = st.columns([0.06, 0.74, 0.2])
            # Checkbox
            with cols[0]:
                done_val = st.checkbox("", value=task["done"], key=f"done_{task_id}")
                # update state immediately (without rerun)
                if done_val != task["done"]:
                    toggle_task_done(task_id, done_val)
            # Text + optional edit
            with cols[1]:
                text_display = task["text"]
                if task["done"]:
                    st.markdown(f"<div class='task-item'><span class='task-text task-done'>{st.experimental_get_query_params() and ''}{text_display}</span></div>", unsafe_allow_html=True)
                else:
                    # inline edit area
                    edit_key = f"edit_input_{task_id}"
                    # show the current text as a text_input (collapsed to save space)
                    edit_expander = st.expander(f"{text_display}", expanded=False)
                    with edit_expander:
                        new_text = st.text_input("Edit task", value=text_display, key=edit_key)
                        if st.button("Save", key=f"save_{task_id}"):
                            if new_text.strip():
                                update_task_text(task_id, new_text)
                            else:
                                st.error("Task text cannot be empty.")
            # Delete button and timestamp
            with cols[2]:
                if st.button("🗑️", key=f"delete_{task_id}"):
                    delete_task_by_id(task_id)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)