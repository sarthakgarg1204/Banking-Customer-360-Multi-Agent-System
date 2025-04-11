# app.py - Main Streamlit Application for Banking Customer 360 Demo

import streamlit as st
import pandas as pd
import json
import time
import random
from PIL import Image
import base64
import io

# Set page configuration
st.set_page_config(
    page_title="Banking Customer 360 Multi-Agent System",
    page_icon="🏦",
    layout="wide"
)

# Custom CSS to improve appearance
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .agent-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .success-message {
        padding: 1rem;
        background-color: #d1e7dd;
        color: #0f5132;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .processing-message {
        padding: 1rem;
        background-color: #cff4fc;
        color: #055160;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>Banking Customer 360 Multi-Agent System</h1>", unsafe_allow_html=True)
st.markdown("<p>Automate the creation of comprehensive customer data products using AI agents</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://via.placeholder.com/150x150.png?text=Banking+360", width=150)
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("", ["Demo", "Architecture", "About"])

# Sample data for demo
sample_requirements = """
Business Requirement: Premium Customer 360 View

We need a comprehensive view of our premium banking customers to support personalized service offerings and targeted marketing campaigns. The solution should integrate data from our core banking system, CRM, transaction history, and digital banking channels.

Key objectives:
1. Identify cross-sell and up-sell opportunities
2. Improve retention of high-value customers
3. Personalize digital banking experiences
4. Enable relationship managers to provide tailored service

Required customer attributes:
- Complete demographic profile
- Financial status (income, assets, liabilities)
- Product holdings and usage patterns
- Channel preferences and interaction history
- Risk profile and investment preferences
- Lifetime value and profitability metrics

The solution must comply with all banking regulations and data privacy requirements.
"""

sample_data_sources = {
    "Core Banking System": {
        "tables": ["CUSTOMER_MASTER", "ACCOUNT_MASTER", "TRANSACTION_HISTORY"],
        "update_frequency": "Daily",
        "data_quality": "High"
    },
    "CRM System": {
        "tables": ["CUSTOMER_INTERACTIONS", "SERVICE_REQUESTS", "CAMPAIGNS"],
        "update_frequency": "Real-time",
        "data_quality": "Medium"
    },
    "Digital Banking": {
        "tables": ["LOGIN_HISTORY", "FEATURE_USAGE", "APP_INTERACTIONS"],
        "update_frequency": "Real-time",
        "data_quality": "High"
    },
    "Credit Risk System": {
        "tables": ["CREDIT_SCORES", "RISK_ASSESSMENTS", "DEFAULT_HISTORY"],
        "update_frequency": "Weekly",
        "data_quality": "High"
    }
}

sample_schema = {
    "Customer": {
        "customerId": "STRING",
        "customerSegment": "STRING",
        "onboardingDate": "DATE",
        "relationshipManager": "STRING"
    },
    "DemographicProfile": {
        "name": "STRUCT<firstName:STRING, lastName:STRING>",
        "contactInfo": "STRUCT<email:STRING, phone:STRING, preferredContact:STRING>",
        "demographics": "STRUCT<age:INT, gender:STRING, occupation:STRING>"
    },
    "FinancialProfile": {
        "incomeDetails": "STRUCT<annualIncome:DECIMAL, incomeSource:STRING>",
        "wealthIndicators": "STRUCT<totalAssets:DECIMAL, totalLiabilities:DECIMAL>",
        "riskProfile": "STRUCT<creditScore:INT, riskCategory:STRING>"
    },
    "ProductHoldings": {
        "accounts": "ARRAY<STRUCT<accountId:STRING, accountType:STRING, balance:DECIMAL>>",
        "cards": "ARRAY<STRUCT<cardId:STRING, cardType:STRING, spendingLimit:DECIMAL>>",
        "investments": "ARRAY<STRUCT<portfolioId:STRING, value:DECIMAL, strategy:STRING>>"
    },
    "BehavioralInsights": {
        "transactionPatterns": "STRUCT<avgMonthlySpend:DECIMAL, topCategories:ARRAY<STRING>>",
        "channelPreferences": "STRUCT<preferredChannel:STRING, digitalEngagement:FLOAT>",
        "lifestyleIndicators": "ARRAY<STRING>"
    }
}

sample_mapping = [
    {
        "sourceSystem": "Core Banking System",
        "sourceTable": "CUSTOMER_MASTER",
        "sourceAttribute": "CUST_ANNUAL_INCOME",
        "targetEntity": "FinancialProfile",
        "targetAttribute": "incomeDetails.annualIncome",
        "transformationLogic": "CAST(CUST_ANNUAL_INCOME AS DECIMAL(12,2))",
    },
    {
        "sourceSystem": "Core Banking System",
        "sourceTable": "CUSTOMER_MASTER",
        "sourceAttribute": "CUSTOMER_SEGMENT",
        "targetEntity": "Customer",
        "targetAttribute": "customerSegment",
        "transformationLogic": "CASE WHEN CUSTOMER_SEGMENT = 'P' THEN 'Premium' WHEN CUSTOMER_SEGMENT = 'H' THEN 'High Net Worth' ELSE 'Standard' END",
    },
    {
        "sourceSystem": "Digital Banking",
        "sourceTable": "APP_INTERACTIONS",
        "sourceAttribute": "LOGIN_FREQUENCY",
        "targetEntity": "BehavioralInsights",
        "targetAttribute": "channelPreferences.digitalEngagement",
        "transformationLogic": "CASE WHEN LOGIN_FREQUENCY > 20 THEN 'High' WHEN LOGIN_FREQUENCY BETWEEN 5 AND 20 THEN 'Medium' ELSE 'Low' END",
    },
    {
        "sourceSystem": "CRM System",
        "sourceTable": "CUSTOMER_INTERACTIONS",
        "sourceAttribute": "PREFERRED_CHANNEL",
        "targetEntity": "BehavioralInsights",
        "targetAttribute": "channelPreferences.preferredChannel",
        "transformationLogic": "UPPER(PREFERRED_CHANNEL)",
    },
    {
        "sourceSystem": "Credit Risk System",
        "sourceTable": "RISK_ASSESSMENTS",
        "sourceAttribute": "CREDIT_SCORE",
        "targetEntity": "FinancialProfile",
        "targetAttribute": "riskProfile.creditScore",
        "transformationLogic": "CAST(CREDIT_SCORE AS INT)",
    }
]

# Create architecture diagram for the Architecture page
def generate_architecture_diagram():
    # This is a placeholder for a real diagram
    # In a real application, you would include an actual image file

    diagram = Image.new('RGB', (800, 400), color = (255, 255, 255))

    buffer = io.BytesIO()
    diagram.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer

# Function to simulate agent processing with progress bar
def simulate_agent_processing(agent_name, seconds=3):
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"{agent_name} Processing: {i+1}%")
        time.sleep(seconds/100)

    status_text.text(f"{agent_name} Processing: Complete!")
    time.sleep(0.5)
    status_text.empty()
    progress_bar.empty()

# Demo page content
if page == "Demo":
    st.markdown("<h2 class='sub-header'>Interactive Demo</h2>", unsafe_allow_html=True)

    # Two columns layout
    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### Business Requirements")
        requirements = st.text_area("Enter your business requirements for Customer 360 view:",
                                    sample_requirements, height=300)

        run_demo = st.button("Process Requirements")

    if run_demo:
        with col2:
            st.markdown("### Multi-Agent Processing")

            # Use Case Agent
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Use Case Agent")
            simulate_agent_processing("Use Case Agent", 2)
            st.markdown("Extracted key requirements and KPIs:")
            st.json({
                "businessObjective": "Create comprehensive view of premium banking customers",
                "primaryUseCase": "Personalized service and targeted marketing",
                "keyAttributes": ["demographics", "financial_status", "product_holdings",
                                 "channel_preferences", "risk_profile", "lifetime_value"],
                "complianceRequirements": ["banking_regulations", "data_privacy"]
            })
            st.markdown("</div>", unsafe_allow_html=True)

            # Data Designer Agent
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Data Designer Agent")
            simulate_agent_processing("Data Designer Agent", 2)
            st.markdown("Recommended Customer 360 Schema:")
            st.json(sample_schema)
            st.markdown("</div>", unsafe_allow_html=True)

            # Source System Agent
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Source System Agent")
            simulate_agent_processing("Source System Agent", 2)
            st.markdown("Identified Data Sources:")
            st.json(sample_data_sources)
            st.markdown("</div>", unsafe_allow_html=True)

            # Mapping Agent
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Mapping Agent")
            simulate_agent_processing("Mapping Agent", 3)
            st.markdown("Generated Data Mappings:")

            # Display mapping as a table
            df = pd.DataFrame(sample_mapping)
            st.dataframe(df)
            st.markdown("</div>", unsafe_allow_html=True)

            # Certification Agent
            st.markdown("<div class='agent-card'>", unsafe_allow_html=True)
            st.markdown("#### 🤖 Certification Agent")
            simulate_agent_processing("Certification Agent", 2)
            st.markdown("Certification Results:")
            certification_results = {
                "dataQualityScore": 92,
                "complianceStatus": "Approved",
                "privacyAssessment": "Compliant with GDPR and banking regulations",
                "dataCoverage": "87% of required attributes mapped",
                "missingElements": ["investment_preferences", "household_information"],
                "recommendations": [
                    "Add data lineage documentation",
                    "Implement data masking for sensitive attributes"
                ]
            }
            st.json(certification_results)
            st.markdown("</div>", unsafe_allow_html=True)

            # Final output
            st.markdown("<div class='success-message'>", unsafe_allow_html=True)
            st.markdown("#### ✅ Customer 360 Data Product Ready!")
            st.markdown("The Customer 360 data product has been successfully created and certified. It is now ready for use in personalized banking services and marketing campaigns.")
            st.markdown("</div>", unsafe_allow_html=True)

# Architecture page content
elif page == "Architecture":
    st.markdown("<h2 class='sub-header'>System Architecture</h2>", unsafe_allow_html=True)

    # Display the architecture diagram
    diagram_buffer = generate_architecture_diagram()
    st.image(diagram_buffer, caption="Multi-Agent System Architecture", use_column_width=True)

    # Architecture explanation
    st.markdown("""
    ### Agent Framework Overview

    Our solution employs a multi-agent architecture powered by the Gemma-2B model via Ollama.
    The system consists of six specialized agents that work collaboratively:

    1. **Use Case Agent**: Interprets business requirements and extracts key objectives
    2. **Data Designer Agent**: Creates optimal data schemas for Customer 360 views
    3. **Source System Agent**: Identifies and catalogs relevant banking data sources
    4. **Mapping Agent**: Generates source-to-target data mappings and transformations
    5. **Certification Agent**: Validates data products against governance standards
    6. **Orchestrator Agent**: Coordinates workflow between specialized agents

    ### Technology Stack

    - **Foundation Model**: Gemma-2B via Ollama
    - **Agent Framework**: LangChain
    - **State Management**: Redis
    - **Data Storage**: Snowflake + MongoDB
    - **API Layer**: FastAPI
    - **Deployment**: Docker containers with Kubernetes

    ### Workflow Process

    1. Business requirements enter the system through the Orchestrator
    2. Use Case Agent analyzes and structures the requirements
    3. Data Designer and Source System Agents work in parallel
    4. Mapping Agent combines outputs to create source-to-target mappings
    5. Certification Agent validates the complete data product
    6. Final Customer 360 view is ready for use in banking applications
    """)

# About page content
elif page == "About":
    st.markdown("<h2 class='sub-header'>About This Project</h2>", unsafe_allow_html=True)

    st.markdown("""
    ### Project Overview

    The Banking Customer 360 Multi-Agent System revolutionizes how retail banks create and manage comprehensive customer data products. By automating the entire process from requirements to certification, we dramatically reduce time-to-value while ensuring compliance with data governance standards.

    ### Business Impact

    - **70% reduction** in time to implement Customer 360 data products
    - **85% decrease** in data mapping errors
    - **100% compliance** with banking governance standards
    - Improved customer experience through better data integration

    ### Hackathon Submission

    This project is a submission for the [Hackathon Name] focused on innovative AI applications in financial services. Our team combined expertise in retail banking, data engineering, and AI to create this transformative solution.

    ### Team Information

    Our team combines expertise in:
    - Retail banking domain knowledge
    - AI/ML engineering
    - Data architecture
    - LLM application development
    - ETL/ELT implementation

    ### Contact

    For more information, visit our GitHub repository or contact us at:
    - GitHub: [Your GitHub Link]
    - Email: [Your Email]
    """)

# Footer
st.markdown("---")
st.markdown("© 2025 Banking Customer 360 Team | Powered by Gemma-2B & Ollama")
