import streamlit as st
import pandas as pd
from datetime import date

st.title("🎓 Class Attendance App")

# Load student list (HallTicket + Name)
students = pd.read_csv("students.csv")

# Load attendance file (create if not exists)
try:
    df = pd.read_csv("attendance.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "HallTicket", "StudentName", "Status"])

# Sidebar menu
menu = ["Mark Attendance", "View Records", "Reports"]
choice = st.sidebar.selectbox("Menu", menu)

today = date.today()

# ------------------- MARK ATTENDANCE -------------------
if choice == "Mark Attendance":
    st.subheader(f"Mark Attendance for {today}")

    attendance_data = []
    for _, row in students.iterrows():
        status = st.radio(
            f"{row['HallTicket']} - {row['StudentName']}",
            ["Present", "Absent"],
            key=row['HallTicket']
        )
        attendance_data.append({
            "Date": today,
            "HallTicket": row['HallTicket'],
            "StudentName": row['StudentName'],
            "Status": status
        })

    if st.button("Save Today's Attendance"):
        df = pd.concat([df, pd.DataFrame(attendance_data)], ignore_index=True)
        df.to_csv("attendance.csv", index=False)
        st.success("✅ Attendance saved successfully!")

# ------------------- VIEW RECORDS -------------------
elif choice == "View Records":
    st.subheader("📋 Attendance Records")
    st.write(df)

# ------------------- REPORTS -------------------
elif choice == "Reports":
    st.subheader("📊 Attendance Report")
    if not df.empty:
        report = df.groupby(["HallTicket", "StudentName", "Status"]).size().unstack(fill_value=0)
        report["Attendance %"] = report["Present"] / (report["Present"] + report["Absent"]) * 100
        st.write(report)
    else:
        st.info("No attendance records yet.")
