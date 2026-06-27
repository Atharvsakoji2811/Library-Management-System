import streamlit as st
import requests
import pandas as pd
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIG

st.set_page_config(page_title="Nova Library", page_icon="📚", layout="wide")

# API CONFIGURATION

BASE_URL = "http://127.0.0.1:5000"

BOOK_LIST_URL = f"{BASE_URL}/books/all_books"
BOOK_ADD_URL = f"{BASE_URL}/books/add_book"

MEMBER_LIST_URL = f"{BASE_URL}/users/all_users"
ADD_MEMBER_URL = f"{BASE_URL}/users/add_user"

MEMBERSHIP_URL = f"{BASE_URL}/membership/distribution"
FINES_URL = f"{BASE_URL}/fines"


def get_data(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.json().get("data", [])

        return []

    except Exception:
        return []


def post_data(url, payload):

    try:
        response = requests.post(url, json=payload)

        if response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()

        return {"message": "Unknown Response"}

    except Exception as e:
        return {"message": str(e)}


# CUSTOM CSS

st.markdown(
    """
<style>

[data-testid="stSidebar"]{
    background:#0A0E1A;
}

.sidebar-logo{
    background: linear-gradient(135deg,#4F46E5,#06B6D4);
    padding:20px;
    border-radius:12px;
    text-align:center;
    margin-bottom:20px;
    color:white;
}

.metric-card{
    border-radius:16px;
    padding:20px;
    color:white;
    height:150px;
    box-shadow:0 6px 18px rgba(0,0,0,0.4);
}

.blue{ background: linear-gradient(135deg,#1E3A8A,#3B82F6); }
.green{ background: linear-gradient(135deg,#047857,#10B981); }
.orange{ background: linear-gradient(135deg,#B45309,#F59E0B); }
.purple{ background: linear-gradient(135deg,#6D28D9,#A855F7); }

.content-box{
    background:#0F172A;
    border-radius:12px;
    padding:20px;
    border:1px solid #1F2937;
}

</style>
""",
    unsafe_allow_html=True,
)

# SESSION STATE

if "page" not in st.session_state:
    st.session_state.page = "🏠 Overview"

# SIDEBAR

with st.sidebar:

    st.markdown(
        """<div class="sidebar-logo">
                 <h2>📚 Nova Library</h2>
                <p>LIBRARY MANAGEMENT SYSTEM</p> </div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title"><b>Main Menu<b/></div>', unsafe_allow_html=True
    )

    menu = st.sidebar.radio(
        "📌 Navigation",
        [
            "🏠 Overview",
            "📚 Books",
            "🔄 Library Activities",
            "👥 Members",
            "💳 Membership",
            "💰 Fines",
            "⚙️ Settings",
        ],
    )
    key = ("main_menu",)


# ROUTING
selected_page = menu

# OVERVIEW DASHBOARD

if selected_page == "🏠 Overview":

    st.title("🏠 Library Dashboard")

    # Fetch Data

    books = get_data(BOOK_LIST_URL)
    members = get_data(MEMBER_LIST_URL)

    total_books = 0
    available_books = 0
    circulation_books = 0
    total_members = len(members)

    categories = []
    category_values = []

    if books:

        total_books = sum(book.get("quantity", 0) for book in books)
        available_books = sum(book.get("available_quantity", 0) for book in books)
        circulation_books = total_books - available_books
        category_counter = Counter(book.get("category", "Unknown") for book in books)
        categories = list(category_counter.keys())
        category_values = list(category_counter.values())

    # # METRIC CARDS

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card blue">
                <div class="metric-title">📚 Total Books</div>
                <div class="metric-value">{total_books}</div>
                <div class="metric-sub">Books in Library</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card green">
                <div class="metric-title">👥 Members</div>
                <div class="metric-value">{total_members}</div>
                <div class="metric-sub">Registered Users</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card orange">
                <div class="metric-title">📖 Issued</div>
                <div class="metric-value">{circulation_books}</div>
                <div class="metric-sub">Currently Issued</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card purple">
                <div class="metric-title">✅ Available</div>
                <div class="metric-value">{available_books}</div>
                <div class="metric-sub">Ready to Issue</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    graph1, graph2 = st.columns(2)

# GRAPH 1 : BOOKS BY CATEGORY

    with graph1:

        if categories:

            colors = [
                "#3B82F6",  # Blue
                "#22C55E",  # Green
                "#F59E0B",  # Orange
                "#8B5CF6",  # Purple
                "#EF4444",  # Red
                "#06B6D4",  # Cyan
                "#EC4899",  # Pink
            ]

            fig = px.bar(
                x=categories,
                y=category_values,
                text=category_values,
                title="📚 Books by Category",
            )

            fig.update_traces(
                marker_color=colors[: len(categories)],
                textposition="outside",
                textfont=dict(
                    size=14,
                    color="white",
                ),
            )

            fig.update_layout(
                height=420,
                paper_bgcolor="#0F172A",
                plot_bgcolor="#0F172A",
                font_color="white",
                xaxis=dict(
                    title="",
                    showgrid=False,
                    showline=False,
                    tickfont=dict(size=12),
                ),
                yaxis=dict(
                    title="",
                    gridcolor="#1E293B",
                    zeroline=False,
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:
            st.info("No category data available.")

# GRAPH 2 : AVAILABILITY

    with graph2:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Available",
                        "Issued",
                    ],
                    values=[
                        available_books,
                        circulation_books,
                    ],
                    hole=0.60,
                )
            ]
        )

        fig.update_layout(
            title="Available vs Issued",
            height=420,
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="white",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()


# RECENT BOOKS

    st.subheader("📖 Recent Book Records")

    if books:

        df = pd.DataFrame(books)

        show_columns = []
        for col in [
            "id",
            "title",
            "author",
            "category",
            "quantity",
            "available_quantity",
            "publishes_year",
        ]:

            if col in df.columns:
                show_columns.append(col)

        st.dataframe(df[show_columns], use_container_width=True, hide_index=True)

    else:

        st.warning("No Books Found.")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.markdown("""
            <div class="content-box">
                <h3>📊 Library Summary</h3>
            </div>""",
            unsafe_allow_html=True,
        )

        st.write(f"**📚 Total Books :** {total_books}")
        st.write(f"**✅ Available Books :** {available_books}")
        st.write(f"**📖 Issued Books :** {circulation_books}")
        st.write(f"**👥 Total Members :** {total_members}")

    with right:

        st.markdown("""
            <div class="content-box">
                <h3>🏆 Top Categories</h3>
            </div>""",
            unsafe_allow_html=True,
        )

        if categories:

            top_df = pd.DataFrame({"Category": categories, "Books": category_values})
            top_df = top_df.sort_values(by="Books", ascending=False)

            st.dataframe(top_df, use_container_width=True, hide_index=True)

        else:
            st.info("No category information available.")

    st.divider()

# BOOKS MODULE

elif selected_page == "📚 Books":

    st.title("📚 Books Management")

    st.markdown(
        """
        <div class="content-box">
        <h3>Manage Library Books</h3>
         </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📋 View", "➕ Add", "🔍 Search", "✏️ Update", "🗑 Delete"]
    )

# VIEW BOOKS
    with tab1:

        st.subheader("📚 View All Books")
        col1, col2 = st.columns([3, 1])

        with col1:
            search_text = st.text_input(
                "Search by Title / Author", placeholder="Enter title or author..."
            )

        with col2:
            books_per_page = st.selectbox("Books Per Page", [5, 10, 20, 50], index=1)

        if st.button("🔄 Refresh Books"):

            st.rerun()

        books = get_data(BOOK_LIST_URL)

        if books:

            df = pd.DataFrame(books)

# Search Filter
            if search_text.strip():

                search = search_text.lower()

                if "title" in df.columns:
                    df = df[df["title"].astype(str).str.lower().str.contains(search)]

                if "author" in df.columns:
                    author_df = pd.DataFrame(books)

                    author_df = author_df[
                        author_df["author"].astype(str).str.lower().str.contains(search)]

                    df = pd.concat([df, author_df]).drop_duplicates()

            total_records = len(df)
            st.success(f"Total Books Found : {total_records}")
            df = df.head(books_per_page)
            st.dataframe(df, use_container_width=True, hide_index=True)

        else:

            st.warning("No books found in library.")

# ADD BOOK
    with tab2:

        st.subheader("➕ Add New Book")

        with st.form("add_book_form"):

            title = st.text_input("Book Title")
            author = st.text_input("Author")
            category = st.text_input("Category")
            publish_year = st.number_input(
                "Publishing Year", min_value=1900, max_value=2100, value=2026
            )

            quantity = st.number_input("Quantity", min_value=1, value=1)
            submit = st.form_submit_button("➕ Add Book")

        if submit:

            payload = {
                "title": title,
                "author": author,
                "category": category,
                "publishes_year": int(publish_year),
                "quantity": int(quantity),
            }

            result = post_data(BOOK_ADD_URL, payload)

            if "message" in result:

                if "success" in result["message"].lower():
                    st.success(result["message"])

                else:

                    st.error(result["message"])

            else:
                st.success("Book Added Successfully.")

    # Search book
    with tab3:
        st.subheader("🔍 Search Book")

        keyword = st.text_input("Enter Book Title or Author", key="search_book")
        books = get_data(BOOK_LIST_URL)

        if keyword:

            keyword = keyword.lower()

            filtered_books = []

            for book in books:

                title = str(book.get("title", "")).lower()
                author = str(book.get("author", "")).lower()

                if keyword in title or keyword in author:

                    filtered_books.append(book)

            if filtered_books:

                st.success(f"{len(filtered_books)} Book(s) Found")

                st.dataframe(
                    pd.DataFrame(filtered_books),
                    use_container_width=True,
                    hide_index=True,
                )

            else:
                st.warning("No Matching Book Found.")

        else:
            st.info("Enter a title or author to search.")

    # update book

    with tab4:

        st.subheader("✏️ Update Book")
        update_id = st.number_input("Book ID", min_value=1, step=1)
        new_title = st.text_input("New Title")
        new_author = st.text_input("New Author")
        new_category = st.text_input("New Category")
        new_year = st.number_input(
            "Publishing Year", min_value=1900, max_value=2100, value=2026
        )
        new_quantity = st.number_input("Quantity", min_value=1, value=1)

        if st.button("✅ Update Book"):

            payload = {
                "title": new_title,
                "author": new_author,
                "category": new_category,
                "publishes_year": int(new_year),
                "quantity": int(new_quantity),
            }

            try:

                response = requests.put(f"{BASE_URL}/books/{update_id}", json=payload)
                result = response.json()

                if response.status_code in [200, 201]:

                    st.success(result.get("message", "Book Updated Successfully."))

                else:

                    st.error(result.get("message", "Unable to Update Book."))

            except Exception as e:

                st.error(str(e))

    #Delete book

    with tab5:

        st.subheader("🗑 Delete Book")

        delete_id = st.number_input(
            "Book ID to Delete", min_value=1, step=1, key="delete_book"
        )

        confirm = st.checkbox("I confirm that I want to delete this book.")

        if st.button("❌ Delete Book"):

            if not confirm:

                st.warning("Please confirm before deleting.")

            else:

                try:

                    response = requests.delete(f"{BASE_URL}/books/{delete_id}")
                    result = response.json()

                    if response.status_code in [200, 201]:

                        st.success(result.get("message", "Book Deleted Successfully."))
                        st.rerun()

                    else:

                        st.error(result.get("message", "Failed to Delete Book."))

                except Exception as e:

                    st.error(str(e))


# member module

elif selected_page == "👥 Members":

    st.title("👥 Members Management")

    st.markdown("""
    <div class="content-box">
    <h3>Library Members</h3>
    </div>""",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 View Members", "➕ Add Member", "✏️ Update Member", "🗑 Delete Member"]
    )

#view members

    with tab1:

        st.subheader("📋 All Members")

        members = get_data(MEMBER_LIST_URL)

        if members:

            df = pd.DataFrame(members)

            search = st.text_input("Search Member", placeholder="Enter Name or Email")

            if search:

                search = search.lower()
                if "name" in df.columns:

                    df = df[df["name"].astype(str).str.lower().str.contains(search)]

                if "email" in df.columns:
                    email_df = pd.DataFrame(members)
                    email_df = email_df[
                    email_df["email"].astype(str).str.lower().str.contains(search)
                    ]

                    df = pd.concat([df, email_df]).drop_duplicates()

            st.dataframe(df, use_container_width=True, hide_index=True)

        else:

            st.warning("No Members Found.")
    #ADD MEMBER

    with tab2:

        st.subheader("➕ Register New Member")

        with st.form("member_form"):

            name = st.text_input("Full Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            phone = st.text_input("Phone Number")
            address = st.text_area("Address")
            role = st.selectbox("Role", ["user", "librarian", "admin"])
            submit = st.form_submit_button("Add Member")

        if submit:

            payload = {
                "name": name,
                "email": email,
                "password": password,
                "phone_no": phone,
                "address": address,
                "role": role,
            }

            result = post_data(ADD_MEMBER_URL, payload)

            if "message" in result:

                if "success" in result["message"].lower():
                    st.success(result["message"])
                    st.rerun()

                else:
                    st.error(result["message"])

            else:

                st.success("Member Added Successfully.")

# UPDATE MEMBER

    with tab3:

        st.subheader("✏️ Update Member")

        member_id = st.number_input("Member ID", min_value=1, step=1)
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_phone = st.text_input("Phone Number")
        new_address = st.text_area("Address")
        new_role = st.selectbox(
        "Role", ["user", "librarian", "admin"], key="update_role"
        )

        if st.button("✅ Update Member"):

            payload = {
                "name": new_name,
                "email": new_email,
                "phone_no": new_phone,
                "address": new_address,
                "role": new_role,
            }

            try:

                response = requests.put(f"{BASE_URL}/users/{member_id}", json=payload)
                result = response.json()

                if response.status_code in [200, 201]:

                    st.success(result.get("message", "Member Updated Successfully."))

                    st.rerun()

                else:

                    st.error(result.get("message", "Failed to Update Member."))

            except Exception as e:

                st.error(str(e))

#Delete member
    with tab4:

        st.subheader("🗑 Delete Member")

        delete_member_id = st.number_input(
            "Member ID", min_value=1, step=1, key="delete_member"
        )

        confirm_delete = st.checkbox("I confirm that I want to delete this member.")

        if st.button("❌ Delete Member"):

            if not confirm_delete:

                st.warning("Please confirm before deleting.")

            else:

                try:

                    response = requests.delete(f"{BASE_URL}/users/{delete_member_id}")
                    result = response.json()

                    if response.status_code in [200, 201]:

                        st.success(
                            result.get("message", "Member Deleted Successfully.")
                        )

                        st.rerun()

                    else:

                        st.error(result.get("message", "Unable to Delete Member."))

                except Exception as e:
                    st.error(str(e))

#membership moudel

elif selected_page == "💳 Membership":

    st.title("💳 Membership Dashboard")

    st.markdown("""
    <div class="content-box">
    <h3>Membership Statistics</h3>
    <p>View membership distribution and registered users.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    members = get_data(MEMBER_LIST_URL)

    total_members = len(members)

    admin_count = 0
    librarian_count = 0
    user_count = 0

    for member in members:

        role = str(member.get("role", "")).lower()

        if role == "admin":
            admin_count += 1

        elif role == "librarian":
            librarian_count += 1

        else:
            user_count += 1

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Members", total_members)
    with c2:
        st.metric("Users", user_count)
    with c3:
        st.metric("Librarians", librarian_count)
    with c4:
        st.metric("Admins", admin_count)
        st.divider()

# membership chart

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            names=["Users", "Librarians", "Admins"],
            values=[user_count, librarian_count, admin_count],
            hole=0.55,
            title="👥 Membership Distribution",
        )

        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font_color="white",
            height=420,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.bar(
            x=["Users", "Librarians", "Admins"],
            y=[user_count, librarian_count, admin_count],
            text=[user_count, librarian_count, admin_count],
            color=[user_count, librarian_count, admin_count],
            color_continuous_scale="Blues",
            title="📊 Members by Role",
        )

        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#180914",
            font_color="white",
            height=420,
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📋 Members List")

    if members:

        df = pd.DataFrame(members)

        columns = ["id", "name", "email", "phone_no", "role"]
        columns = [c for c in columns if c in df.columns]

        st.dataframe(df[columns], use_container_width=True, hide_index=True)

    else:

        st.info("No member records found.")

elif selected_page == "🔄 Library Activities":

    st.title("🔄 Library Activities")

    st.info(
        "Library Activities module is ready. " "Connect your Issue/Return API here."
    )

    activity_tab1, activity_tab2 = st.tabs(["📖 Issue Book", "📥 Return Book"])

# Issue book 
    with activity_tab1:

        st.subheader("📖 Issue Book")

        with st.form("issue_book_form"):

            member_id = st.number_input("Member ID", min_value=1, step=1)
            book_id = st.number_input("Book ID", min_value=1, step=1)
            issue_date = st.date_input("Issue Date")
            due_date = st.date_input("Due Date")
            submit_issue = st.form_submit_button("Issue Book")

        if submit_issue:

            payload = {
                "member_id": int(member_id),
                "book_id": int(book_id),
                "issue_date": str(issue_date),
                "due_date": str(due_date),
            }

            try:

                response = requests.post(f"{BASE_URL}/circulation/issue", json=payload)
                result = response.json()

                if response.status_code in [200, 201]:

                    st.success(result.get("message", "Book Issued Successfully."))

                else:

                    st.error(result.get("message", "Unable to Issue Book."))

            except Exception as e:

                st.error(str(e))

#Return book
    with activity_tab2:

        st.subheader("📥 Return Book")

        transaction_id = st.number_input("Transaction ID", min_value=1, step=1)

        if st.button("Return Book"):

            try:

                response = requests.post(f"{BASE_URL}/circulation/return/{id}")
                result = response.json()

                if response.status_code in [200, 201]:

                    st.success(result.get("message", "Book Returned Successfully."))

                    st.rerun()

                else:

                    st.error(result.get("message", "Unable to Return Book."))

            except Exception as e:

                st.error(str(e))

#fines module 
elif selected_page == "💰 Fines":

    st.title("💰 Fines Management")

    st.markdown("""
    <div class="content-box">
    <h3>💰 Library Fines</h3>
    <p>View and manage all fines.</p>
    </div>""",
        unsafe_allow_html=True,
    )

    fines = get_data(FINES_URL)

    if fines:

        df = pd.DataFrame(fines)

        st.metric("Total Fine Records", len(df))

        st.dataframe(df, use_container_width=True, hide_index=True)

    else:

        st.warning("No fine records found.")

# setting modules
 
elif selected_page == "⚙️ Settings":

    st.title("⚙️ Settings")

    (tab1,) = st.tabs(["🔒 Change Password"])

#change password
    with tab1:

        st.subheader("🔒 Change Password")

        member_id = st.text_input("member id", type="default")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("🔄 Change Password"):

            if new_password != confirm_password:
                st.error("New Password and Confirm Password do not match.")

            elif len(new_password) < 6:
                st.warning("Password must be at least 6 characters.")

            else:

                payload = {
                    "current_password": current_password,
                    "new_password": new_password,
                }

                try:

                    response = requests.put(
                        f"{BASE_URL}/users/change_password", json=payload
                    )

                    result = response.json()

                    if response.status_code == 200:
                        st.success(
                            result.get("message", "Password Changed Successfully.")
                        )

                    else:
                        st.error(result.get("message", "Unable to Change Password."))

                except Exception as e:
                    st.error(str(e))
