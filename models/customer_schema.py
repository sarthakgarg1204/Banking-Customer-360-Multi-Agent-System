"""
Customer 360 Schema Definitions

This module defines the data models for the Customer 360 view, including
customer demographics, financial profile, product holdings, and behavioral insights.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import date, datetime


class Name(BaseModel):
    """Customer name information."""
    first_name: str = Field(..., description="Customer's first name")
    middle_name: Optional[str] = Field(None, description="Customer's middle name")
    last_name: str = Field(..., description="Customer's last name")
    title: Optional[str] = Field(None, description="Customer's title (Mr., Mrs., Dr., etc.)")

    def full_name(self) -> str:
        """Return the customer's full name."""
        parts = [p for p in [self.title, self.first_name, self.middle_name, self.last_name] if p]
        return " ".join(parts)


class ContactInfo(BaseModel):
    """Customer contact information."""
    email: Optional[str] = Field(None, description="Customer's primary email address")
    phone: Optional[str] = Field(None, description="Customer's primary phone number")
    mobile: Optional[str] = Field(None, description="Customer's mobile number")
    preferred_contact: Optional[str] = Field(None, description="Customer's preferred contact method (email, phone, mobile, mail)")
    do_not_contact: bool = Field(False, description="Flag indicating if customer has opted out of communications")


class Address(BaseModel):
    """Physical address information."""
    address_line1: str = Field(..., description="First line of address")
    address_line2: Optional[str] = Field(None, description="Second line of address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State or province")
    postal_code: str = Field(..., description="Postal or ZIP code")
    country: str = Field("USA", description="Country")
    address_type: str = Field(..., description="Type of address (Home, Work, Mailing)")
    is_primary: bool = Field(False, description="Flag indicating if this is the primary address")


class Demographics(BaseModel):
    """Demographic information about the customer."""
    date_of_birth: Optional[date] = Field(None, description="Customer's date of birth")
    age: Optional[int] = Field(None, description="Customer's current age in years")
    gender: Optional[str] = Field(None, description="Customer's gender")
    marital_status: Optional[str] = Field(None, description="Customer's marital status")
    nationality: Optional[str] = Field(None, description="Customer's nationality")
    occupation: Optional[str] = Field(None, description="Customer's occupation")
    employer: Optional[str] = Field(None, description="Customer's employer")
    education_level: Optional[str] = Field(None, description="Customer's highest education level")
    household_size: Optional[int] = Field(None, description="Number of people in customer's household")


class IncomeDetails(BaseModel):
    """Income information for the customer."""
    annual_income: Optional[float] = Field(None, description="Customer's annual income")
    income_source: Optional[str] = Field(None, description="Primary source of income")
    income_verification: Optional[str] = Field(None, description="Income verification status")
    secondary_income: Optional[float] = Field(None, description="Secondary income amount")
    household_income: Optional[float] = Field(None, description="Total household income")


class WealthIndicators(BaseModel):
    """Wealth and net worth indicators."""
    total_assets: Optional[float] = Field(None, description="Total value of customer's assets")
    total_liabilities: Optional[float] = Field(None, description="Total value of customer's liabilities")
    net_worth: Optional[float] = Field(None, description="Net worth (assets - liabilities)")
    liquid_assets: Optional[float] = Field(None, description="Value of liquid assets")
    real_estate_value: Optional[float] = Field(None, description="Value of real estate holdings")


class RiskProfile(BaseModel):
    """Customer's risk profile and credit information."""
    credit_score: Optional[int] = Field(None, description="Customer's credit score")
    risk_category: Optional[str] = Field(None, description="Risk category (Low, Medium, High)")
    default_history: Optional[bool] = Field(None, description="Flag indicating history of defaults")
    bankruptcy_history: Optional[bool] = Field(None, description="Flag indicating history of bankruptcy")
    investment_risk_tolerance: Optional[str] = Field(None, description="Investment risk tolerance (Conservative, Moderate, Aggressive)")


class Account(BaseModel):
    """Individual bank account information."""
    account_id: str = Field(..., description="Account identifier")
    account_type: str = Field(..., description="Type of account (Checking, Savings, etc.)")
    account_status: str = Field(..., description="Status of the account (Active, Dormant, Closed)")
    open_date: date = Field(..., description="Date account was opened")
    close_date: Optional[date] = Field(None, description="Date account was closed, if applicable")
    balance: float = Field(..., description="Current account balance")
    average_balance_30d: Optional[float] = Field(None, description="Average balance over last 30 days")
    average_balance_90d: Optional[float] = Field(None, description="Average balance over last 90 days")
    interest_rate: Optional[float] = Field(None, description="Current interest rate, if applicable")
    currency: str = Field("USD", description="Account currency")
    is_joint: bool = Field(False, description="Flag indicating if this is a joint account")
    joint_holders: Optional[List[str]] = Field(None, description="List of joint account holders, if applicable")


class Card(BaseModel):
    """Credit, debit, or other payment card information."""
    card_id: str = Field(..., description="Card identifier")
    card_type: str = Field(..., description="Type of card (Credit, Debit, Prepaid)")
    card_status: str = Field(..., description="Status of the card (Active, Blocked, Expired)")
    issue_date: date = Field(..., description="Date card was issued")
    expiry_date: date = Field(..., description="Expiration date")
    credit_limit: Optional[float] = Field(None, description="Credit limit for credit cards")
    current_balance: Optional[float] = Field(None, description="Current balance for credit cards")
    available_credit: Optional[float] = Field(None, description="Available credit for credit cards")
    rewards_program: Optional[str] = Field(None, description="Rewards program enrollment")
    rewards_balance: Optional[float] = Field(None, description="Current rewards balance")


class Investment(BaseModel):
    """Investment portfolio or product information."""
    portfolio_id: str = Field(..., description="Portfolio identifier")
    portfolio_type: str = Field(..., description="Type of portfolio (Retirement, Brokerage, etc.)")
    current_value: float = Field(..., description="Current market value")
    initial_investment: Optional[float] = Field(None, description="Initial investment amount")
    investment_strategy: Optional[str] = Field(None, description="Investment strategy")
    risk_level: Optional[str] = Field(None, description="Risk level of the portfolio")
    performance_ytd: Optional[float] = Field(None, description="Year-to-date performance percentage")
    performance_1yr: Optional[float] = Field(None, description="One-year performance percentage")
    performance_3yr: Optional[float] = Field(None, description="Three-year performance percentage")
    asset_allocation: Optional[Dict[str, float]] = Field(None, description="Asset allocation percentages by category")


class Loan(BaseModel):
    """Loan or credit facility information."""
    loan_id: str = Field(..., description="Loan identifier")
    loan_type: str = Field(..., description="Type of loan (Mortgage, Auto, Personal, etc.)")
    loan_status: str = Field(..., description="Status of the loan (Active, Paid Off, Default)")
    origination_date: date = Field(..., description="Date loan was originated")
    maturity_date: date = Field(..., description="Loan maturity date")
    original_amount: float = Field(..., description="Original loan amount")
    current_balance: float = Field(..., description="Current loan balance")
    interest_rate: float = Field(..., description="Current interest rate")
    payment_amount: float = Field(..., description="Regular payment amount")
    payment_frequency: str = Field(..., description="Payment frequency (Monthly, Bi-weekly, etc.)")
    collateral: Optional[str] = Field(None, description="Collateral information, if applicable")
    last_payment_date: Optional[date] = Field(None, description="Date of last payment")
    next_payment_date: Optional[date] = Field(None, description="Date of next payment")
    days_past_due: Optional[int] = Field(None, description="Number of days past due, if applicable")


class TransactionPatterns(BaseModel):
    """Analysis of customer transaction patterns."""
    avg_monthly_deposit: Optional[float] = Field(None, description="Average monthly deposit amount")
    avg_monthly_withdrawal: Optional[float] = Field(None, description="Average monthly withdrawal amount")
    avg_monthly_spend: Optional[float] = Field(None, description="Average monthly spending amount")
    top_deposit_sources: Optional[List[str]] = Field(None, description="Top sources of deposits")
    top_merchants: Optional[List[str]] = Field(None, description="Top merchants by spending")
    top_categories: Optional[List[str]] = Field(None, description="Top spending categories")
    recurring_payments: Optional[List[Dict[str, Any]]] = Field(None, description="Identified recurring payments")
    cash_usage: Optional[float] = Field(None, description="Percentage of transactions in cash")
    international_activity: Optional[bool] = Field(None, description="Flag indicating international transaction activity")


class ChannelPreferences(BaseModel):
    """Customer's preferred banking channels and usage patterns."""
    preferred_channel: Optional[str] = Field(None, description="Primary banking channel (Branch, Online, Mobile, etc.)")
    channel_usage: Optional[Dict[str, float]] = Field(None, description="Percentage usage by channel")
    digital_engagement: Optional[float] = Field(None, description="Digital engagement score (0-100)")
    last_branch_visit: Optional[date] = Field(None, description="Date of last branch visit")
    branch_visit_frequency: Optional[str] = Field(None, description="Branch visit frequency (Weekly, Monthly, etc.)")
    mobile_app_usage: Optional[str] = Field(None, description="Mobile app usage frequency")
    online_banking_usage: Optional[str] = Field(None, description="Online banking usage frequency")
    atm_usage: Optional[str] = Field(None, description="ATM usage frequency")


class LifestyleIndicators(BaseModel):
    """Lifestyle indicators derived from transaction patterns."""
    travel_frequency: Optional[str] = Field(None, description="Travel frequency inference")
    luxury_preference: Optional[str] = Field(None, description="Luxury spending preference")
    dining_preference: Optional[str] = Field(None, description="Dining out frequency")
    entertainment_spending: Optional[float] = Field(None, description="Entertainment spending as percentage of total")
    healthcare_spending: Optional[float] = Field(None, description="Healthcare spending as percentage of total")
    lifestyle_categories: Optional[List[str]] = Field(None, description="Identified lifestyle categories")


class ProductRecommendations(BaseModel):
    """Product recommendations for the customer."""
    next_best_product: Optional[str] = Field(None, description="Next best product recommendation")
    recommendation_score: Optional[float] = Field(None, description="Confidence score for recommendation (0-100)")
    recommendation_reason: Optional[str] = Field(None, description="Reasoning behind recommendation")
    additional_recommendations: Optional[List[Dict[str, Any]]] = Field(None, description="Additional product recommendations")
    upsell_opportunities: Optional[List[Dict[str, Any]]] = Field(None, description="Potential upsell opportunities")
    cross_sell_opportunities: Optional[List[Dict[str, Any]]] = Field(None, description="Potential cross-sell opportunities")


class RetentionMetrics(BaseModel):
    """Customer retention metrics and churn risk indicators."""
    customer_lifetime_value: Optional[float] = Field(None, description="Calculated customer lifetime value")
    relationship_tenure: Optional[int] = Field(None, description="Relationship tenure in months")
    churn_risk_score: Optional[float] = Field(None, description="Churn risk score (0-100)")
    churn_risk_factors: Optional[List[str]] = Field(None, description="Identified churn risk factors")
    satisfaction_score: Optional[float] = Field(None, description="Customer satisfaction score, if available")
    complaint_history: Optional[List[Dict[str, Any]]] = Field(None, description="History of complaints")
    loyalty_program_status: Optional[str] = Field(None, description="Status in loyalty program, if applicable")
    loyalty_points: Optional[int] = Field(None, description="Current loyalty points balance")


class DemographicProfile(BaseModel):
    """Comprehensive demographic profile."""
    name: Name
    contact_info: ContactInfo
    addresses: List[Address] = Field(default_factory=list)
    demographics: Demographics = Field(default_factory=Demographics)


class FinancialProfile(BaseModel):
    """Comprehensive financial profile."""
    income_details: IncomeDetails = Field(default_factory=IncomeDetails)
    wealth_indicators: WealthIndicators = Field(default_factory=WealthIndicators)
    risk_profile: RiskProfile = Field(default_factory=RiskProfile)


class ProductHoldings(BaseModel):
    """All financial products held by the customer."""
    accounts: List[Account] = Field(default_factory=list)
    cards: List[Card] = Field(default_factory=list)
    investments: List[Investment] = Field(default_factory=list)
    loans: List[Loan] = Field(default_factory=list)
    total_products: int = Field(0, description="Total number of products held")
    total_balance: float = Field(0.0, description="Total balance across all accounts")
    total_debt: float = Field(0.0, description="Total debt across all loans and credit cards")
    product_history: Optional[List[Dict[str, Any]]] = Field(None, description="History of product holdings")


class BehavioralInsights(BaseModel):
    """Behavioral insights derived from transaction and interaction data."""
    transaction_patterns: TransactionPatterns = Field(default_factory=TransactionPatterns)
    channel_preferences: ChannelPreferences = Field(default_factory=ChannelPreferences)
    lifestyle_indicators: LifestyleIndicators = Field(default_factory=LifestyleIndicators)
    last_interaction: Optional[datetime] = Field(None, description="Date and time of last interaction")
    interaction_frequency: Optional[str] = Field(None, description="Frequency of interactions")


class Customer360(BaseModel):
    """Complete Customer 360 view."""
    # Core customer information
    customer_id: str = Field(..., description="Unique customer identifier")
    customer_segment: str = Field(..., description="Customer segment (Mass, Affluent, Premium, etc.)")
    onboarding_date: date = Field(..., description="Date customer was onboarded")
    relationship_manager: Optional[str] = Field(None, description="Assigned relationship manager")

    # Detailed profiles
    demographic_profile: DemographicProfile
    financial_profile: FinancialProfile
    product_holdings: ProductHoldings
    behavioral_insights: BehavioralInsights

    # Business intelligence
    product_recommendations: ProductRecommendations = Field(default_factory=ProductRecommendations)
    retention_metrics: RetentionMetrics = Field(default_factory=RetentionMetrics)

    # Metadata
    last_updated: datetime = Field(..., description="Timestamp of last update")
    data_quality_score: Optional[float] = Field(None, description="Data quality score (0-100)")
    compliance_status: Optional[str] = Field(None, description="Compliance status (Compliant, Non-compliant)")

    class Config:
        schema_extra = {
            "example": {
                "customer_id": "C123456789",
                "customer_segment": "Premium",
                "onboarding_date": "2018-05-15",
                "relationship_manager": "Jane Smith",
                "demographic_profile": {
                    "name": {
                        "first_name": "John",
                        "last_name": "Doe",
                        "title": "Mr."
                    },
                    "contact_info": {
                        "email": "john.doe@example.com",
                        "phone": "555-123-4567",
                        "preferred_contact": "email"
                    },
                    "addresses": [
                        {
                            "address_line1": "123 Main St",
                            "city": "Anytown",
                            "state": "CA",
                            "postal_code": "12345",
                            "address_type": "Home",
                            "is_primary": True
                        }
                    ],
                    "demographics": {
                        "date_of_birth": "1975-08-21",
                        "age": 49,
                        "gender": "Male",
                        "occupation": "Software Engineer"
                    }
                },
                "financial_profile": {
                    "income_details": {
                        "annual_income": 150000.00,
                        "income_source": "Employment"
                    },
                    "wealth_indicators": {
                        "total_assets": 750000.00,
                        "total_liabilities": 250000.00,
                        "net_worth": 500000.00
                    },
                    "risk_profile": {
                        "credit_score": 780,
                        "risk_category": "Low",
                        "investment_risk_tolerance": "Moderate"
                    }
                },
                "last_updated": "2025-04-10T14:30:00Z",
                "data_quality_score": 92.5
            }
        }
