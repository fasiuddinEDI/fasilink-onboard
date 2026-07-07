"""
FasiLink Client Onboarding Portal
Simple form for pharmacies and wholesalers to submit their info for EDI setup
"""
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="FasiLink EDI Onboarding",
    page_icon="⚕️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a5f;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background: #dcfce7;
        color: #166534;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bbf7d0;
        text-align: center;
    }
    .info-box {
        background: #eff6ff;
        color: #1e40af;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bfdbfe;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">⚕️ FasiLink EDI Onboarding</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Submit your information for AI-powered EDI setup</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <b>What happens next?</b><br>
    1. You fill out this form (takes 5 minutes)<br>
    2. FasiLink AI validates your credentials automatically<br>
    3. Our team reviews and approves your application<br>
    4. You receive EDI connection details within 24 hours<br>
    5. Start exchanging documents with your trading partners
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA STORAGE
# ============================================================
DATA_DIR = Path("fasilink_data")
DATA_DIR.mkdir(exist_ok=True)
SUBMISSIONS_FILE = DATA_DIR / "client_submissions.json"

if not SUBMISSIONS_FILE.exists():
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump([], f)

def load_submissions():
    try:
        with open(SUBMISSIONS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_submission(data):
    submissions = load_submissions()
    submissions.append(data)
    with open(SUBMISSIONS_FILE, 'w') as f:
        json.dump(submissions, f, indent=2, default=str)

# ============================================================
# ONBOARDING FORM
# ============================================================
with st.form("client_onboarding"):
    st.markdown("### 📋 Company Information")

    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Company Legal Name *", placeholder="e.g., Rx Care Specialty Pharmacy, LLC")
        company_type = st.selectbox("Company Type *", ["Pharmacy", "Wholesaler/Distributor", "Hospital/Health System", "Manufacturer", "3PL/Logistics", "Other"])
        email = st.text_input("Primary Email *", placeholder="edi@yourcompany.com")
        phone = st.text_input("Phone *", placeholder="(800) 555-0100")
    with col2:
        website = st.text_input("Website", placeholder="https://yourcompany.com")
        address = st.text_input("Address *", placeholder="123 Main St")
        city = st.text_input("City *", placeholder="Houston")
        state = st.selectbox("State *", ["TX", "CA", "NY", "FL", "IL", "PA", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI", "CO", "MN", "SC", "AL", "LA", "KY", "OR", "OK", "CT", "UT", "NV", "AR", "MS", "KS", "NM", "NE", "WV", "ID", "HI", "NH", "ME", "MT", "RI", "DE", "SD", "ND", "AK", "VT", "WY", "DC"])
        zip_code = st.text_input("ZIP Code *", placeholder="77001")

    st.markdown("### 📄 Regulatory Information")
    col3, col4 = st.columns(2)
    with col3:
        npi = st.text_input("NPI (10-digit) *", placeholder="1234567890", max_chars=10)
        dea = st.text_input("DEA Registration (9-char) *", placeholder="BR1234567", max_chars=9)
    with col4:
        state_license = st.text_input("State License Number *", placeholder="PHA-12345-TX")
        nabp = st.text_input("NABP Accreditation (if applicable)", placeholder="Optional")

    st.markdown("### 💻 Software & Systems")
    col5, col6 = st.columns(2)
    with col5:
        if company_type == "Pharmacy":
            pms_software = st.selectbox(
                "Pharmacy Management System (PMS) *",
                ["PioneerRx", "PrimeRx (MMS)", "QS/1 (NRx)", "Rx30", "ComputerRx", "Epic", "Liberty Software", "MicroHelix (McKesson)", "SRS Pharma", "VendRx", "Other", "Unknown"]
            )
            erp_system = "Not Applicable"
        else:
            pms_software = "Not Applicable"
            erp_system = st.selectbox(
                "ERP / Business System *",
                ["BlueLink ERP", "SAP", "Oracle NetSuite", "Microsoft Dynamics", "Epicor", "Infor", "McKesson Connect", "Cardinal Health Connect", "AmerisourceBergen (AB)", "Custom/Proprietary", "Other", "Unknown"]
            )
    with col6:
        software_version = st.text_input("Software Version (if known)", placeholder="e.g., 2024.1")

    st.markdown("### 🔌 EDI Preferences")
    col7, col8 = st.columns(2)
    with col7:
        preferred_docs = st.multiselect(
            "Which EDI documents do you need?",
            ["850 - Purchase Order", "855 - PO Acknowledgment", "856 - Advance Ship Notice", "810 - Invoice", "846 - Inventory Inquiry", "844 - Chargeback", "845 - Contract Notification"],
            default=["850 - Purchase Order", "855 - PO Acknowledgment", "856 - Advance Ship Notice", "810 - Invoice"]
        )
    with col8:
        test_first = st.toggle("Start with Test Mode (recommended)", value=True)
        dscsa_verify = st.toggle("Enable DSCSA Compliance Checks", value=True)

    st.markdown("### 👤 Primary Contact")
    col9, col10 = st.columns(2)
    with col9:
        contact_name = st.text_input("Contact Name *", placeholder="John Smith")
        contact_title = st.text_input("Job Title *", placeholder="Pharmacy Manager")
    with col10:
        contact_email = st.text_input("Contact Email *", placeholder="john.smith@yourcompany.com")
        contact_phone = st.text_input("Contact Phone *", placeholder="(713) 555-0100")

    st.markdown("### 📝 Additional Information")
    notes = st.text_area("Notes / Special Requirements", placeholder="Any specific requirements, existing EDI setup, preferred go-live date, etc.")

    st.markdown("---")
    agree_terms = st.checkbox("I agree to FasiLink's Terms of Service and Privacy Policy *")

    submitted = st.form_submit_button("🚀 Submit for AI Review")

    if submitted:
        if not all([company_name, company_type, email, phone, address, city, state, zip_code, npi, dea, state_license, contact_name, contact_email, contact_phone, agree_terms]):
            st.error("Please fill in all required fields (marked with *) and agree to the terms.")
        else:
            submission = {
                "id": f"SUB_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "company_name": company_name,
                "company_type": company_type,
                "email": email,
                "phone": phone,
                "website": website,
                "address": address,
                "city": city,
                "state": state,
                "zip": zip_code,
                "npi": npi,
                "dea": dea,
                "state_license": state_license,
                "nabp": nabp,
                "pms_software": pms_software,
                "erp_system": erp_system,
                "software_version": software_version,
                "preferred_docs": preferred_docs,
                "test_first": test_first,
                "dscsa_verify": dscsa_verify,
                "contact_name": contact_name,
                "contact_title": contact_title,
                "contact_email": contact_email,
                "contact_phone": contact_phone,
                "notes": notes,
                "status": "Pending Review",
                "submitted_at": datetime.now().isoformat(),
                "ai_reviewed": False
            }

            save_submission(submission)

            st.markdown(f"""
            <div class="success-box">
                <h3 style="margin:0;">✅ Submission Received!</h3>
                <p style="margin:0.5rem 0 0 0;">
                    Thank you, <b>{company_name}</b>. Your application has been submitted for AI review.<br>
                    <b>Submission ID:</b> {submission['id']}<br>
                    <b>Next Steps:</b> Our team will review your credentials and send EDI connection details within 24 hours.<br>
                    <b>Contact:</b> {contact_email} | {contact_phone}
                </p>
            </div>
            """)
            st.balloons()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <p><b>FasiLink EDI Solutions</b> — AI-Powered Pharmaceutical EDI</p>
    <p>Questions? Contact us at support@fasilink.com | (800) 555-FASI</p>
    <p style="font-size:0.75rem;">© 2026 FasiLink EDI Solutions. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
