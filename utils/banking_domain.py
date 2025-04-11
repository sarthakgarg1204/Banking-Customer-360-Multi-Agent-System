# banking_domain.py - Banking domain knowledge and terminology utilities

class BankingDomainKnowledge:
    """
    Provides banking domain-specific knowledge, terminology, and validation rules
    for the Customer 360 Multi-Agent System.
    """

    @staticmethod
    def get_customer_segments():
        """Return standard customer segments used in retail banking."""
        return {
            "P": "Premium",
            "H": "High Net Worth",
            "A": "Affluent",
            "M": "Mass Affluent",
            "R": "Regular",
            "S": "Standard",
            "Y": "Youth",
            "E": "Elite",
            "B": "Business"
        }

    @staticmethod
    def get_product_categories():
        """Return standard banking product categories."""
        return [
            "Deposit Accounts",
            "Credit Cards",
            "Personal Loans",
            "Mortgages",
            "Investment Products",
            "Insurance Products",
            "Wealth Management",
            "Foreign Exchange",
            "Payment Services",
            "Digital Banking Services"
        ]

    @staticmethod
    def get_common_banking_systems():
        """Return common banking system types and their typical data domains."""
        return {
            "Core Banking System": {
                "description": "Primary system of record for customer accounts",
                "typical_data": ["customer_master", "account_master", "transaction_history", "product_catalog"],
                "update_frequency": "Real-time to daily"
            },
            "CRM System": {
                "description": "Customer relationship management system",
                "typical_data": ["customer_interactions", "sales_opportunities", "campaign_history", "service_requests"],
                "update_frequency": "Real-time"
            },
            "Digital Banking": {
                "description": "Online and mobile banking platforms",
                "typical_data": ["login_history", "feature_usage", "app_interactions", "session_data"],
                "update_frequency": "Real-time"
            },
            "Credit Risk System": {
                "description": "Credit scoring and risk assessment",
                "typical_data": ["credit_scores", "risk_assessments", "default_history", "limit_management"],
                "update_frequency": "Daily to weekly"
            },
            "Fraud Detection System": {
                "description": "Transaction monitoring and fraud analysis",
                "typical_data": ["fraud_alerts", "suspicious_activity", "behavioral_patterns"],
                "update_frequency": "Real-time"
            },
            "KYC/AML System": {
                "description": "Know Your Customer and Anti-Money Laundering",
                "typical_data": ["identity_verification", "watchlist_screening", "risk_classification"],
                "update_frequency": "Daily to weekly"
            },
            "Card Management System": {
                "description": "Credit and debit card processing",
                "typical_data": ["card_master", "authorization_history", "reward_points"],
                "update_frequency": "Real-time to daily"
            }
        }

    @staticmethod
    def get_banking_kpis():
        """Return common KPIs used in retail banking."""
        return {
            "Customer Acquisition": ["new_customer_count", "acquisition_cost", "conversion_rate"],
            "Customer Retention": ["attrition_rate", "retention_rate", "relationship_tenure"],
            "Product Performance": ["products_per_customer", "cross_sell_ratio", "product_penetration"],
            "Financial Performance": ["customer_profitability", "lifetime_value", "revenue_per_customer"],
            "Risk Management": ["default_rate", "delinquency_rate", "risk_adjusted_return"],
            "Digital Engagement": ["digital_adoption_rate", "mobile_usage_frequency", "online_transaction_ratio"]
        }

    @staticmethod
    def get_compliance_requirements():
        """Return common banking compliance domains."""
        return {
            "Data Privacy": ["GDPR", "CCPA", "Banking secrecy laws"],
            "Financial Regulation": ["Basel III", "Dodd-Frank", "PSD2"],
            "Consumer Protection": ["UDAAP", "Fair lending", "TILA", "RESPA"],
            "Anti-Money Laundering": ["BSA", "AML", "KYC", "CTF"],
            "Information Security": ["SOX", "GLBA", "PCI-DSS"]
        }

    @staticmethod
    def validate_pii_handling(attribute_name, transformation_logic):
        """
        Validates if PII data is being handled according to compliance standards.

        Args:
            attribute_name (str): Name of the data attribute
            transformation_logic (str): The transformation being applied

        Returns:
            tuple: (is_compliant, recommendation)
        """
        pii_attributes = [
            "name", "address", "email", "phone", "ssn", "tax", "dob", "birth",
            "age", "gender", "national", "passport", "license", "card_number"
        ]

        # Check if attribute might contain PII
        contains_pii = any(pii_term in attribute_name.lower() for pii_term in pii_attributes)

        if contains_pii:
            # Check if transformation includes masking or encryption
            has_protection = any(term in transformation_logic.lower()
                                for term in ["mask", "encrypt", "hash", "redact", "tokenize"])

            if not has_protection:
                return (False, "Consider masking, encrypting, or tokenizing this PII attribute")

        return (True, "Transformation appears compliant")

    @staticmethod
    def get_data_quality_rules():
        """Return common data quality rules for banking data."""
        return {
            "customer_id": {
                "nullability": False,
                "pattern": r"^[A-Z0-9]{8,12}$",
                "description": "Customer ID must be 8-12 alphanumeric characters"
            },
            "email": {
                "nullability": True,
                "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                "description": "Valid email format required when present"
            },
            "phone_number": {
                "nullability": True,
                "pattern": r"^\+?[0-9]{10,15}$",
                "description": "Phone number must be 10-15 digits with optional + prefix"
            },
            "credit_score": {
                "nullability": True,
                "range": [300, 850],
                "description": "Credit score must be between 300 and 850 when present"
            },
            "account_balance": {
                "nullability": False,
                "type": "DECIMAL",
                "description": "Account balance must be a valid decimal number"
            }
        }
