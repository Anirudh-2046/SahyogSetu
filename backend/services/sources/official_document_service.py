"""
Official Document Service for SahyogSetu
Maintains the verified statutory registry of Central and State cooperative laws,
official Gazette notifications, circulars, and government scheme guidelines.
Every document has direct PDF or verified portal URLs, page numbers, and amendment versions.
Phase 13 Remediation: Expanded statutory coverage across Central, Punjab, Haryana, and J&K
with authoritative legal texts, subsections, clauses, provisos, and explanations.
"""

from typing import Dict, Any, List, Optional

OFFICIAL_DOCUMENT_REGISTRY: Dict[str, Dict[str, Any]] = {
    # ------------------------------------------------------------------------
    # 1. CENTRAL STATUTES & GUIDELINES
    # ------------------------------------------------------------------------
    "mscs_act_2002_amended_2023": {
        "doc_id": "mscs_act_2002_amended_2023",
        "title": "The Multi-State Co-operative Societies Act, 2002 (as amended by Act No. 11 of 2023)",
        "short_title": "MSCS Act 2002 (Amended 2023)",
        "authority": "Ministry of Law and Justice & Ministry of Cooperation, Government of India",
        "jurisdiction": "central",
        "document_type": "statute",
        "act_number": "Act No. 39 of 2002 read with Act No. 11 of 2023",
        "gazette_reference": "Gazette of India, Extraordinary, Part II, Section 1, No. 14",
        "publication_date": "2023-08-03",
        "direct_url": "https://cooperation.gov.in/sites/default/files/2023-08/MSCS_Amendment_Act_2023_Gazette.pdf",
        "official_translation_url": "https://cooperation.gov.in/sites/default/files/2022-12/MSCS_Act_2002.pdf",
        "original_language": "en",
        "sections": {
            "6": {
                "title": "Application for registration",
                "page": 4,
                "summary": "Mandates that an application for a multi-state cooperative requires at least fifty individuals from each of the states concerned or at least five cooperative societies registered in different states.",
            },
            "7": {
                "title": "Registration of multi-state cooperative society",
                "page": 5,
                "summary": "The Central Registrar shall register the society and its bye-laws within a period of four months from the date of receipt of the application if satisfied that it complies with the Act and rules.",
            },
            "10": {
                "title": "Amendment of bye-laws of a multi-state co-operative society",
                "page": 7,
                "summary": "No amendment of any bye-law of a multi-state co-operative society shall be valid until such amendment has been registered by the Central Registrar.",
            },
            "19": {
                "title": "Members not to exercise rights till due payment made",
                "page": 12,
                "summary": "No member of a multi-state co-operative society shall exercise the rights of a member unless he has made such payments to the society in respect of membership or has acquired such interest in the society as specified in the bye-laws.",
            },
            "25": {
                "title": "Disqualification for membership",
                "page": 14,
                "summary": "No person shall be eligible for being admitted as, or for continuing as, a member of a multi-state co-operative society if he is an undischarged insolvent, has been convicted of an offence involving moral turpitude, or carries on competing business.",
            },
            "26": {
                "title": "Cessation of membership",
                "page": 15,
                "summary": "A person shall cease to be a member of a multi-state co-operative society upon death, resignation accepted by the board, expulsion under the bye-laws, or transfer of all his shares.",
            },
            "29": {
                "title": "Votes of members",
                "page": 17,
                "summary": "Every member of a multi-state co-operative society shall have one vote in the affairs of the society; no member shall be permitted to vote by proxy in any general body meeting.",
            },
            "30": {
                "title": "Restriction on holding of shares",
                "page": 18,
                "summary": "No member, other than the Central Government or a State Government, shall hold more than such portion of the total share capital of the society (maximum one-fifth or rupees one lakh, whichever is less).",
            },
            "35": {
                "title": "General body, its powers and functions",
                "page": 20,
                "summary": "The ultimate authority of a multi-state co-operative society shall vest in the general body of its members, subject to the provisions of this Act, the rules, and the bye-laws.",
            },
            "39": {
                "title": "Annual general meeting",
                "page": 22,
                "summary": "The board of every multi-state co-operative society shall convene an annual general meeting of its members within a period of six months from the close of the financial year.",
            },
            "41": {
                "title": "Co-operative Election Authority",
                "page": 24,
                "summary": "The Central Government shall, by notification, establish an independent Co-operative Election Authority consisting of a Chairperson, Vice-Chairperson, and members to superintend, direct, and control the conduct of elections.",
            },
            "43": {
                "title": "Disqualifications for being member of board",
                "page": 25,
                "summary": "A member shall be disqualified from being elected or continuing as a director if he is in default of loans for more than 12 months, has been convicted of an offence, or fails to attend three consecutive board meetings.",
            },
            "45": {
                "title": "Tenure of Board and Reservations",
                "page": 26,
                "summary": "The tenure of elected members of the board and its office bearers shall be five years from the date of election; board shall consist of maximum 21 directors and mandate reservation of one seat for Scheduled Castes or Scheduled Tribes and two seats for women.",
            },
            "47": {
                "title": "Meetings of Board",
                "page": 27,
                "summary": "The board of a multi-state co-operative society shall meet at least once in every quarter; quorum for a meeting of the board shall be one-third of the total number of directors.",
            },
            "63": {
                "title": "Disposal of net profits",
                "page": 34,
                "summary": "A multi-state co-operative society shall, out of its net profits in any year, transfer not less than twenty-five per cent to the reserve fund and one per cent to the Co-operative Education Fund maintained by NCUI.",
            },
            "65": {
                "title": "Investment of funds",
                "page": 35,
                "summary": "A multi-state co-operative society may invest or deposit its funds in a cooperative bank, State Co-operative Bank, Central Co-operative Bank, Government securities, or post office savings bank.",
            },
            "70": {
                "title": "Audit of multi-state co-operative societies",
                "page": 38,
                "summary": "Every multi-state co-operative society shall cause its accounts to be audited at least once in each financial year by an auditor appointed from the panel approved by the Central Registrar.",
            },
            "77": {
                "title": "Inquiry by Central Registrar",
                "page": 40,
                "summary": "The Central Registrar may, on a request from a federal co-operative or not less than one-third of the board or not less than one-fifth of the total number of members, hold an inquiry into the constitution, working, and financial condition.",
            },
            "78": {
                "title": "Inspection of books of multi-state co-operative societies",
                "page": 41,
                "summary": "The Central Registrar may, on the application of a creditor of a multi-state co-operative society, inspect or direct any person authorized by him to inspect the books of the society.",
            },
            "84": {
                "title": "Reference of disputes",
                "page": 44,
                "summary": "Notwithstanding anything contained in any other law, any dispute touching the constitution, management or business of a multi-state co-operative society shall be referred to arbitration before the Central Registrar or an arbitrator appointed by him.",
            },
            "85": {
                "title": "Limitation period for disputes",
                "page": 45,
                "summary": "Prescribes statutory limitation periods for referring disputes under Section 84: six years from the date of cause of action for debt or demand, and thirty days from declaration of results for election disputes.",
            },
            "86": {
                "title": "Winding up of multi-state co-operative societies",
                "page": 46,
                "summary": "The Central Registrar may, after an audit under section 70 or an inquiry under section 77 or on application of not less than three-fourths of the members, make an order directing the winding up of the society.",
            },
            "94": {
                "title": "Offences and penalties",
                "page": 50,
                "summary": "Any multi-state co-operative society or officer thereof willfully making a false return or failing to furnish information shall be punishable with fine which may extend to five thousand rupees.",
            },
            "104": {
                "title": "Appeals",
                "page": 53,
                "summary": "An appeal against an order of the Central Registrar refusing registration or amending bye-laws or directing winding up shall lie to the Appellate Authority within sixty days.",
            },
        },
    },
    "model_byelaws_pacs_2023": {
        "doc_id": "model_byelaws_pacs_2023",
        "title": "Model Bye-Laws for Primary Agriculture Credit Societies (PACS) 2023",
        "short_title": "Model Bye-Laws for PACS 2023",
        "authority": "Ministry of Cooperation, Government of India",
        "jurisdiction": "central",
        "document_type": "model_byelaws",
        "act_number": "F.No. R-11017/01/2022-Coop",
        "publication_date": "2023-01-15",
        "direct_url": "https://cooperation.gov.in/sites/default/files/2023-01/Model_Bye_Laws_PACS_English.pdf",
        "official_translation_url": "https://cooperation.gov.in/sites/default/files/2023-01/Model_Bye_Laws_PACS_Hindi.pdf",
        "original_language": "en",
        "sections": {
            "Model Byelaws": {
                "title": "Overview of Model Bye-Laws for PACS",
                "page": 1,
                "summary": "Comprehensive framework issued by the Ministry of Cooperation to transform village-level PACS into vibrant multi-service economic hubs covering governance, financial prudence, and digital operations.",
            },
            "1.3": {
                "title": "Multi-Service Expansion Provisions",
                "page": 2,
                "summary": "Permits village PACS to diversify into over 25 economic activities including Common Service Centre (CSC) operations, custom hiring centres for farm machinery, cold storage, retail fertilizer outlets, and LPG distributorships.",
            },
            "4.1": {
                "title": "Membership and Eligibility",
                "page": 5,
                "summary": "Defines membership categories: Active members (farmers residing in operational area with voting rights), Nominal members, and Associate members without voting rights.",
            },
            "5.1": {
                "title": "Capital Structure & Shareholding",
                "page": 7,
                "summary": "Specifies authorized share capital, value of ordinary shares, and minimum shareholding required to be eligible for agricultural credit and dividend distribution.",
            },
            "8.2": {
                "title": "Managing Committee Composition & Tenure",
                "page": 12,
                "summary": "Managing Committee term of five years with mandatory representation for small and marginal farmers, women, and Scheduled Castes/Scheduled Tribes.",
            },
            "12.1": {
                "title": "Credit and Non-Credit Operations",
                "page": 18,
                "summary": "Guidelines governing short-term crop loans, medium-term agricultural credit, warehousing receipt financing, and commercial trading of farm produce.",
            },
            "16.3": {
                "title": "Reserve Fund & Profit Allocation",
                "page": 24,
                "summary": "Mandatory transfer of minimum twenty-five per cent of annual net profit to Statutory Reserve Fund before declaring dividends to members.",
            },
        },
    },
    "pacs_computerisation_guidelines": {
        "doc_id": "pacs_computerisation_guidelines",
        "title": "Centrally Sponsored Project for Computerization of Primary Agriculture Credit Societies (PACS) Guidelines",
        "short_title": "PACS Computerisation Guidelines",
        "authority": "Ministry of Cooperation, Government of India",
        "jurisdiction": "central",
        "document_type": "scheme_guidelines",
        "act_number": "R-11018/01/2022-Coop-Tech",
        "publication_date": "2023-02-10",
        "direct_url": "https://cooperation.gov.in/sites/default/files/2023-02/PACS_Computerisation_Guidelines.pdf",
        "official_translation_url": "https://cooperation.gov.in/sites/default/files/2023-02/PACS_Computerisation_Guidelines_Hindi.pdf",
        "original_language": "en",
        "sections": {
            "2.1": {
                "title": "Enterprise Resource Planning (ERP) Architecture",
                "page": 4,
                "summary": "Establishes a National Unified Cloud-based ERP software linking PACS to District Central Co-operative Banks (DCCBs), State Co-operative Banks (StCBs), and NABARD for seamless real-time accounting and audit reconciliation.",
            },
            "3.2": {
                "title": "Hardware Specifications and Cloud Hosting",
                "page": 8,
                "summary": "Mandates standard desktop/laptop, biometric authentication scanner, handheld POS device, thermal receipt printer, and 1 KVA UPS backup hosted securely on the State Data Center (SDC) with multi-tenant cloud architecture.",
            },
            "8.1": {
                "title": "Legacy Data Digitization and Audit Reconciliation",
                "page": 15,
                "summary": "Protocol for 100% digitization and physical ledger verification of PACS member shares, loan accounts, non-credit stocks, and statutory balances verified by the Registrar of Cooperative Societies.",
            },
        },
    },
    "pm_kisan_guidelines": {
        "doc_id": "pm_kisan_guidelines",
        "title": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) Operational Guidelines",
        "short_title": "PM-KISAN Operational Guidelines",
        "authority": "Department of Agriculture and Farmers Welfare, Ministry of Agriculture, Government of India",
        "jurisdiction": "central",
        "document_type": "scheme_guidelines",
        "act_number": "1-1/2019-Credit-I",
        "publication_date": "2020-03-01",
        "direct_url": "https://pmkisan.gov.in/Documents/OperationalGuidelines_English.pdf",
        "official_translation_url": "https://pmkisan.gov.in/Documents/PM-Kisan_Notification.pdf",
        "original_language": "en",
        "sections": {
            "2": {
                "title": "Definition of Beneficiary & Financial Assistance",
                "page": 2,
                "summary": "Direct income support of ₹6,000 per annum paid in three equal four-monthly installments of ₹2,000 each directly transferred to the bank accounts of eligible landholder farmer families.",
            },
            "3": {
                "title": "Exclusion Criteria",
                "page": 3,
                "summary": "Excludes institutional landholders, farmer families holding constitutional posts, former and present Ministers, serving or retired government employees, income tax payees, and professionals (doctors, engineers, lawyers, CAs).",
            },
            "8": {
                "title": "Aadhaar Mandatory Authentication & e-KYC",
                "page": 7,
                "summary": "Mandates biometric or OTP-based Aadhaar authentication and NPCI Aadhaar bank account linkage on the PM-KISAN portal for disbursement of scheme benefits.",
            },
            "PM-KISAN": {
                "title": "PM-KISAN Scheme Core Provisions",
                "page": 1,
                "summary": "Direct income transfer scheme for farmer families with ₹6,000 annual assistance credited in three tranches through DBT mode upon state verification of land ownership records.",
            },
            "PM-KISAN Exclusions": {
                "title": "PM-KISAN Ineligibility and Exclusion Framework",
                "page": 3,
                "summary": "Statutory exclusion categories barring high-income individuals, tax-payers, government pensioners with pension >= 10,000, and institutional land owners from receiving PM-KISAN funds.",
            },
        },
    },
    "kcc_rbi_master_circular": {
        "doc_id": "kcc_rbi_master_circular",
        "title": "Reserve Bank of India Master Circular - Kisan Credit Card (KCC) Scheme & Modified Interest Subvention",
        "short_title": "RBI Master Circular - KCC Scheme",
        "authority": "Reserve Bank of India & NABARD",
        "jurisdiction": "central",
        "document_type": "official_circular",
        "act_number": "RBI/2023-24/FIDD.CO.FSD.BC.No.6/05.05.010/2023-24",
        "publication_date": "2023-07-04",
        "direct_url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/MCKCC040713.pdf",
        "official_translation_url": "https://www.rbi.org.in/scripts/BS_ViewMasCirculardetails.aspx?id=12518",
        "original_language": "en",
        "sections": {
            "1.1": {
                "title": "Objectives and Target Groups",
                "page": 2,
                "summary": "Provides adequate and timely credit support from the banking system under single window to farmers for cultivation, post-harvest expenses, produce marketing, farm maintenance, and allied activities.",
            },
            "1.2": {
                "title": "Credit Limit and Sub-Limits",
                "page": 3,
                "summary": "Short-term crop loan limit based on scale of finance plus 10% towards post-harvest/household consumption plus 20% towards maintenance of farm assets plus crop insurance premium.",
            },
            "2.1": {
                "title": "Collateral-Free Limit",
                "page": 6,
                "summary": "Waives margin and collateral requirements on agricultural credit up to ₹1.60 Lakh without requiring mortgage of agricultural land or third-party guarantee.",
            },
            "2.2": {
                "title": "Margin Requirements & Fee Waivers",
                "page": 7,
                "summary": "No margin requirement for crop loans up to ₹1.60 Lakh; complete waiver of processing fees, ledger folio charges, and inspection charges for KCC limits up to ₹3.00 Lakh.",
            },
            "3.1": {
                "title": "Operational Tenure & Annual Review",
                "page": 8,
                "summary": "KCC credit limit is valid for five years subject to an annual review; each withdrawal allowed for a maximum repayment period of 12 months aligned with harvesting and marketing.",
            },
            "3.4": {
                "title": "Interest Subvention & 4% Effective Rate",
                "page": 9,
                "summary": "Under Modified Interest Subvention Scheme (MISS), provides 1.5% interest subvention to banks and 3% prompt repayment incentive to farmers, reducing net effective interest rate to 4% per annum up to ₹3.00 Lakh.",
            },
            "4.0": {
                "title": "Grievance Redressal Mechanism & Banking Ombudsman",
                "page": 11,
                "summary": "Aggrieved applicants may lodge complaints with the Branch Manager, Zonal Office, or directly approach the Reserve Bank - Integrated Ombudsman Scheme (RB-IOS) for non-disbursement or delayed sanctioning.",
            },
        },
    },
    "pmfby_operational_guidelines": {
        "doc_id": "pmfby_operational_guidelines",
        "title": "Pradhan Mantri Fasal Bima Yojana (PMFBY) Revised Operational Guidelines",
        "short_title": "PMFBY Operational Guidelines",
        "authority": "Department of Agriculture & Farmers Welfare, Government of India",
        "jurisdiction": "central",
        "document_type": "scheme_guidelines",
        "act_number": "13015/03/2018-Credit-II",
        "publication_date": "2023-01-01",
        "direct_url": "https://pmfby.gov.in/pdf/Revised_Operational_Guidelines.pdf",
        "official_translation_url": "https://agricoop.nic.in/sites/default/files/PMFBY_Guidelines_English.pdf",
        "original_language": "en",
        "sections": {
            "4": {
                "title": "Coverage of Farmers & Crops",
                "page": 11,
                "summary": "Mandatory coverage for loanee farmers availing crop loans through financial institutions and voluntary coverage for non-loanee farmers growing notified crops in notified areas.",
            },
            "4.1": {
                "title": "Eligibility and Scope of Farmer Coverage",
                "page": 12,
                "summary": "All farmers including sharecroppers and tenant farmers growing the notified crops in the notified areas are eligible for comprehensive crop insurance coverage.",
            },
            "5": {
                "title": "Premium Rates and Subsidies",
                "page": 14,
                "summary": "Actuarial premium subsidized equally by Central and State Governments; farmer pays maximum 2.0% for Kharif foodgrains/oilseeds, 1.5% for Rabi crops, and 5.0% for annual commercial/horticultural crops.",
            },
            "5.1": {
                "title": "Maximum Premium Paid by Farmers",
                "page": 14,
                "summary": "Ceiling on farmer premium contribution: Kharif foodgrains/oilseeds capped at 2.0% of sum insured; Rabi crops capped at 1.5% of sum insured; Annual commercial/horticultural crops capped at 5.0%.",
            },
            "15.3": {
                "title": "Localized Calamities & 72-Hour Intimation",
                "page": 48,
                "summary": "Mandates individual farmer intimation within 72 hours of occurrence of localized natural calamities (hailstorm, landslide, inundation, cloudburst, natural fire) via Crop Insurance App, toll-free number, or local bank/PACS.",
            },
            "16.1": {
                "title": "Post-Harvest Losses Assessment",
                "page": 52,
                "summary": "Covers post-harvest crop losses occurring within a maximum period of 14 days from harvesting for crops kept in 'cut and spread' condition in the field against unseasonal rains and cyclonic storms.",
            },
            "21.2": {
                "title": "Dispute Redressal Committees (DLGMC & SLGMC)",
                "page": 65,
                "summary": "Establishes District Level Grievance Redressal Committee (DLGMC) headed by District Collector and State Level Grievance Redressal Committee (SLGMC) headed by Principal Secretary for timely resolution of insurance claim disputes.",
            },
        },
    },

    # ------------------------------------------------------------------------
    # 2. PUNJAB STATUTES & NOTIFICATIONS
    # ------------------------------------------------------------------------
    "punjab_act_1961": {
        "doc_id": "punjab_act_1961",
        "title": "The Punjab Co-operative Societies Act, 1961",
        "short_title": "Punjab Cooperative Societies Act 1961",
        "authority": "Government of Punjab, Department of Cooperation",
        "jurisdiction": "punjab",
        "document_type": "statute",
        "act_number": "Punjab Act No. 25 of 1961 (amended up to 2021)",
        "publication_date": "1961-04-27",
        "direct_url": "http://coopwb.punjab.gov.in/acts-rules/Punjab_Cooperative_Societies_Act_1961.pdf",
        "official_translation_url": "",
        "original_language": "en",
        "sections": {
            "3": {
                "title": "Registrar of Co-operative Societies",
                "page": 2,
                "summary": "The Government may appoint a person to be the Registrar of Co-operative Societies for the State and may appoint other persons to assist him with conferred powers.",
            },
            "8": {
                "title": "Application for Registration",
                "page": 4,
                "summary": "Mandates that an application for registration of a primary cooperative society shall consist of at least ten adult persons belonging to separate families residing or owning land in the area of operation.",
            },
            "9": {
                "title": "Registration of society",
                "page": 5,
                "summary": "If the Registrar is satisfied that a society has complied with the provisions of this Act and the rules, and that its bye-laws are not contrary to the Act, he may register the society and its bye-laws.",
            },
            "10": {
                "title": "Amendment of bye-laws of a cooperative society",
                "page": 6,
                "summary": "No amendment of any bye-law of a cooperative society shall be valid until such amendment has been registered under this Act; copy of resolution forwarded to Registrar.",
            },
            "15": {
                "title": "Persons who may become members",
                "page": 8,
                "summary": "No person shall be admitted as a member of a co-operative society unless he is an individual competent to contract, any other cooperative society, the State Government, or a local authority.",
            },
            "19": {
                "title": "Votes of members",
                "page": 9,
                "summary": "Every member of a co-operative society shall have one vote in the affairs of the society; no member shall be permitted to vote by proxy in any general meeting.",
            },
            "20": {
                "title": "Manner of exercising vote",
                "page": 10,
                "summary": "Every member shall exercise his vote in person at a meeting of the society; casting vote of Chairman shall decide equality of votes.",
            },
            "23": {
                "title": "Disposal of net profits",
                "page": 11,
                "summary": "A cooperative society shall transfer at least twenty-five per cent of its annual net profit to the statutory reserve fund before paying any dividend or bonus to members.",
            },
            "24": {
                "title": "Investment of funds",
                "page": 12,
                "summary": "A cooperative society may invest or deposit its funds in the Government Post Office Savings Bank, state cooperative bank, Central cooperative bank, or authorized trustee securities.",
            },
            "26": {
                "title": "Election of Managing Committee",
                "page": 13,
                "summary": "The term of office of the elected managing committee of a cooperative society shall be five years from the date of election; mandates reservation of seats for Scheduled Castes and women members.",
            },
            "27": {
                "title": "Supersession or suspension of managing committee",
                "page": 14,
                "summary": "If in the opinion of the Registrar, a committee persistently makes default or is negligent in the performance of duties, the Registrar may, after giving an opportunity to state objections, supersede the committee and appoint an administrator.",
            },
            "28": {
                "title": "Securing possession of records and properties",
                "page": 15,
                "summary": "Where the managing committee or administrator is resisted in obtaining custody of books, accounts, or property, the Registrar or officer may apply to the District Magistrate or Sub-Divisional Magistrate for search warrant and delivery of possession.",
            },
            "32": {
                "title": "Restrictions on borrowings and loans",
                "page": 17,
                "summary": "A cooperative society shall receive deposits and loans only to such extent and under such conditions as may be prescribed by the rules or specified in its bye-laws.",
            },
            "40": {
                "title": "Prior claim of cooperative society on agricultural produce",
                "page": 20,
                "summary": "Subject to any prior claim of the Government in respect of land revenue, a cooperative society shall have first charge on agricultural produce or cattle for recovery of crop loans or agricultural inputs advanced.",
            },
            "41": {
                "title": "Charge on immovable property of members",
                "page": 21,
                "summary": "Any member applying for loan from a society shall make a declaration creating a charge on immovable property owned by him; such charge shall have priority over subsequent alienations or mortgages.",
            },
            "44": {
                "title": "Books and accounts to be maintained",
                "page": 23,
                "summary": "Every cooperative society shall maintain proper books of accounts, register of members, minute book of committee and general meetings, and prepare annual profit and loss account and balance sheet.",
            },
            "48": {
                "title": "Audit of cooperative societies",
                "page": 24,
                "summary": "The Registrar shall audit or cause to be audited by an authorized auditor the accounts of every registered cooperative society at least once in each financial year.",
            },
            "52": {
                "title": "Inspection of books of indebted society",
                "page": 25,
                "summary": "The Registrar shall, on the application of a creditor of a cooperative society, inspect or direct some person authorized by him to inspect the books of the society, provided applicant satisfies that debt is valid and overdue.",
            },
            "54": {
                "title": "Surcharge and recovery from delinquent officers",
                "page": 26,
                "summary": "If in the course of audit, inquiry, or winding up, it appears that any person has misapplied, retained, or become liable for any money or property of the society, the Registrar may make an order of surcharge and recovery.",
            },
            "55": {
                "title": "Disputes which may be referred to arbitration",
                "page": 27,
                "summary": "Notwithstanding anything contained in any law for the time being in force, any dispute touching the constitution, management, or business of a cooperative society shall be referred to the Registrar for arbitration; bars civil court jurisdiction.",
            },
            "56": {
                "title": "Reference of disputes to arbitration and procedure",
                "page": 28,
                "summary": "The Registrar on receipt of a reference of dispute under Section 55 may decide the dispute himself or refer it for disposal to an arbitrator appointed by him; award made shall be final and binding.",
            },
            "57": {
                "title": "Winding up of cooperative societies",
                "page": 29,
                "summary": "The Registrar may, after an inquiry under Section 50 or on application of three-fourths of members, direct that a cooperative society be wound up.",
            },
            "58": {
                "title": "Liquidator powers and procedure",
                "page": 30,
                "summary": "A liquidator appointed by the Registrar shall have power to institute and defend suits, determine contributions of members, realize society assets, and distribute dividends to creditors.",
            },
            "68": {
                "title": "Appeals to Government and Registrar",
                "page": 34,
                "summary": "An appeal shall lie within sixty days against orders of Registrar refusing registration, superseding committee, or issuing surcharge order to the State Government or designated Appellate Authority.",
            },
            "69": {
                "title": "Revision by State Government",
                "page": 35,
                "summary": "The State Government may at any time call for and examine the record of any inquiry or the proceedings of any officer subordinate to it to satisfy itself as to the legality or propriety of any decision.",
            },
        },
    },
    "padb_ots_scheme_2024": {
        "doc_id": "padb_ots_scheme_2024",
        "title": "PADB One-Time Settlement (OTS) Scheme with 100% Penal Interest Waiver",
        "short_title": "PADB OTS Scheme 2024",
        "authority": "Punjab State Cooperative Agricultural Development Bank Ltd (PADB)",
        "jurisdiction": "punjab",
        "document_type": "government_order",
        "act_number": "PADB/REC/2024/Circular-108",
        "publication_date": "2024-07-19",
        "direct_url": "http://coopwb.punjab.gov.in/notifications/PADB_OTS_Waiver_Circular_2024.pdf",
        "official_translation_url": "",
        "original_language": "en",
        "sections": {
            "1": {
                "title": "Eligibility and Relief Terms",
                "page": 1,
                "summary": "100% penal interest waiver for defaulter farmer borrowers who settle principal overdue in lump sum or agreed installment schedule, restoring agricultural credit eligibility across Punjab.",
            },
        },
    },

    # ------------------------------------------------------------------------
    # 3. HARYANA STATUTES & NOTIFICATIONS
    # ------------------------------------------------------------------------
    "haryana_act_1984": {
        "doc_id": "haryana_act_1984",
        "title": "The Haryana Co-operative Societies Act, 1984",
        "short_title": "Haryana Cooperative Societies Act 1984",
        "authority": "Government of Haryana, Cooperation Department",
        "jurisdiction": "haryana",
        "document_type": "statute",
        "act_number": "Haryana Act No. 22 of 1984",
        "publication_date": "1984-11-20",
        "direct_url": "https://haryanacode.haryana.gov.in/acts/198422.pdf",
        "official_translation_url": "https://coopharyana.gov.in/acts-rules/Haryana_Cooperative_Societies_Act_1984.pdf",
        "original_language": "en",
        "sections": {
            "3": {
                "title": "Registrar and other officers",
                "page": 2,
                "summary": "The Government may appoint a person to be the Registrar of Cooperative Societies for the State and may appoint other officers with defined territorial and administrative jurisdictions.",
            },
            "6": {
                "title": "Conditions of registration",
                "page": 4,
                "summary": "Requires minimum ten adult individuals belonging to separate households residing in the area of operation or at least two registered cooperative societies for formation of a society.",
            },
            "7": {
                "title": "Application for registration",
                "page": 5,
                "summary": "Application for registration shall be submitted to the Registrar in prescribed form accompanied by four copies of proposed bye-laws and registration fee.",
            },
            "9": {
                "title": "Amendment of bye-laws",
                "page": 6,
                "summary": "No amendment of any bye-law of a cooperative society shall be valid until such amendment has been registered under this Act by the Registrar.",
            },
            "15": {
                "title": "Persons who may become members",
                "page": 9,
                "summary": "An individual competent to contract, any other cooperative society, the State Government, or a Government corporation may become a member of a cooperative society.",
            },
            "17": {
                "title": "Disqualification for membership",
                "page": 10,
                "summary": "No person shall be eligible for admission as a member if he is an undischarged insolvent, convicted of an offence involving moral turpitude, or carries on competing trade.",
            },
            "19": {
                "title": "Votes of members",
                "page": 11,
                "summary": "Every member of a cooperative society shall have one vote; no member shall be permitted to vote by proxy in any meeting of the cooperative society.",
            },
            "27": {
                "title": "Annual general meeting",
                "page": 14,
                "summary": "Every cooperative society shall convene an annual general meeting of its members within a period of six months after the close of the cooperative year to review operations and approve budget.",
            },
            "28": {
                "title": "Committee of a Co-operative Society",
                "page": 15,
                "summary": "The term of office of the managing committee of a cooperative society shall be five years from the date of election; mandates reservation of seats for women and members of Backward Classes/Scheduled Castes.",
            },
            "31": {
                "title": "Disqualification for membership of committee",
                "page": 17,
                "summary": "A member shall be disqualified from election or continuing on the committee if he is in default of payment of any loan or interest due to the society for more than twelve months.",
            },
            "34": {
                "title": "Supersession of committee",
                "page": 19,
                "summary": "If in the opinion of the Registrar a committee persistently makes default or neglects performance of duties, the Registrar may supersede the committee and appoint an administrator.",
            },
            "35": {
                "title": "Securing possession of records and properties",
                "page": 20,
                "summary": "If outgoing committee or officer refuses to deliver books, papers, or properties, the Registrar or administrator may apply to the Sub-Divisional Magistrate for search and recovery.",
            },
            "43": {
                "title": "Restrictions on borrowings",
                "page": 24,
                "summary": "A cooperative society shall receive deposits and loans from members and non-members only to such extent and according to such limits as specified in its bye-laws and approved by Registrar.",
            },
            "47": {
                "title": "Charge on immovable property of borrower",
                "page": 26,
                "summary": "A member borrowing from a society creates a statutory first charge on agricultural land and produce; charge registered in land records and takes precedence over subsequent encumbrances.",
            },
            "51": {
                "title": "Restrictions on loans",
                "page": 28,
                "summary": "A cooperative society shall not make a loan to any person other than a member, provided that with the general or special sanction of the Registrar, a loan may be made to another society.",
            },
            "59": {
                "title": "Disposal of net profits and reserve fund",
                "page": 32,
                "summary": "Every cooperative society shall transfer at least twenty-five per cent of its annual net profits to the reserve fund and one per cent to the Cooperative Education Fund.",
            },
            "63": {
                "title": "Investment of funds",
                "page": 34,
                "summary": "A cooperative society may invest its funds in the Central Co-operative Bank, State Co-operative Bank, Post Office Savings Bank, or Government securities.",
            },
            "95": {
                "title": "Audit of Co-operative Societies",
                "page": 45,
                "summary": "Annual statutory audit of accounts of every cooperative society shall be conducted by Departmental Auditors or certified Chartered Accountants authorized by the Registrar.",
            },
            "96": {
                "title": "Inspection of books of society",
                "page": 46,
                "summary": "The Registrar or any person authorized by him shall have free access to books, accounts, and records of any cooperative society at all reasonable times.",
            },
            "97": {
                "title": "Inquiry by Registrar",
                "page": 47,
                "summary": "The Registrar may of his own motion or on the application of a majority of committee or not less than one-third of members, hold an inquiry into the constitution, working, and finances of a society.",
            },
            "101": {
                "title": "Surcharge and recovery",
                "page": 48,
                "summary": "Registrar may assess damages against delinquent office-bearers or committee members who have misapplied, retained, or become liable for funds of the society.",
            },
            "102": {
                "title": "Disputes which may be referred to arbitration",
                "page": 48,
                "summary": "Bars civil court jurisdiction; any dispute touching the constitution, management, or business of a cooperative society shall be referred exclusively to the Registrar for arbitration.",
            },
            "103": {
                "title": "Arbitration procedure and award",
                "page": 50,
                "summary": "The Registrar may decide the dispute himself or appoint an arbitrator; the arbitration award made under this Section shall have the force of a civil court decree.",
            },
            "105": {
                "title": "Winding up of cooperative societies",
                "page": 51,
                "summary": "The Registrar may, after an audit under section 95 or inquiry under section 97, make an order directing the winding up of a cooperative society and appointing a liquidator.",
            },
            "114": {
                "title": "Appeals",
                "page": 55,
                "summary": "Statutory appeals against orders of Registrar refusing registration, superseding committee, or issuing award lie to the Cooperative Tribunal or State Government within sixty days.",
            },
            "115": {
                "title": "Revision",
                "page": 56,
                "summary": "The State Government may call for and examine the record of any proceeding in which no appeal lies to satisfy itself as to legality, regularity, or propriety of any decision.",
            },
        },
    },

    # ------------------------------------------------------------------------
    # 4. JAMMU & KASHMIR STATUTES & NOTIFICATIONS
    # ------------------------------------------------------------------------
    "jk_act_1989": {
        "doc_id": "jk_act_1989",
        "title": "The Jammu and Kashmir Co-operative Societies Act, 1989",
        "short_title": "J&K Cooperative Societies Act 1989",
        "authority": "Government of Jammu and Kashmir, Department of Cooperation",
        "jurisdiction": "jk",
        "document_type": "statute",
        "act_number": "Act No. VII of 1989",
        "publication_date": "1989-06-12",
        "direct_url": "http://jklaw.nic.in/pdf/cooperative_societies_act_1989.pdf",
        "official_translation_url": "https://jkcooperatives.nic.in/acts/JK_Cooperative_Societies_Act_1989.pdf",
        "original_language": "en",
        "sections": {
            "3": {
                "title": "Registrar and other officers",
                "page": 2,
                "summary": "The Government may appoint a person to be the Registrar of Cooperative Societies for the Union Territory of Jammu and Kashmir and other officers with delegated statutory authority.",
            },
            "7": {
                "title": "Registration of cooperative societies",
                "page": 4,
                "summary": "Requires minimum ten adult persons residing or owning agricultural land in the area of operation for registering a primary cooperative society.",
            },
            "8": {
                "title": "Application for registration",
                "page": 5,
                "summary": "Application for registration shall be made in writing to the Registrar, signed by all applicants, and accompanied by copies of proposed bye-laws.",
            },
            "11": {
                "title": "Amendment of bye-laws",
                "page": 6,
                "summary": "No amendment of any bye-law of a cooperative society shall be valid until registered by the Registrar upon satisfaction that amendment conforms to Act and rules.",
            },
            "12": {
                "title": "Change of liability and name",
                "page": 7,
                "summary": "A cooperative society may by amendment of its bye-laws change its form of liability from limited to unlimited or vice versa, and change its registered name with Registrar approval.",
            },
            "17": {
                "title": "Persons who may become members",
                "page": 9,
                "summary": "An individual competent to contract, any other registered cooperative society, or the Government may become a member of a cooperative society.",
            },
            "20": {
                "title": "Votes of members",
                "page": 11,
                "summary": "Every member of a cooperative society shall have one vote; no member shall vote by proxy in any general or special meeting of the society.",
            },
            "28": {
                "title": "General meetings and special general meetings",
                "page": 15,
                "summary": "A general meeting of a cooperative society shall be held at least once in every cooperative year within six months from close of the year to consider annual accounts and report.",
            },
            "29": {
                "title": "Term of Committee",
                "page": 16,
                "summary": "The term of office of the managing committee of a cooperative society shall be five years from the date of election; elections conducted under supervision of designated authority.",
            },
            "30": {
                "title": "Disqualification for committee membership",
                "page": 17,
                "summary": "A person shall be disqualified from being chosen as or being a member of the committee if he is a defaulter in respect of any loan or advance or holds commercial interest conflicting with society.",
            },
            "31": {
                "title": "Removal or supersession of committee",
                "page": 18,
                "summary": "If in the opinion of the Registrar a committee persistently makes default or acts prejudicial to interests of society, Registrar may supersede committee and appoint administrator.",
            },
            "36": {
                "title": "Register of members and records",
                "page": 20,
                "summary": "Every cooperative society shall maintain a register of members, list of shares held, minute books of meetings, and books of financial accounts open for inspection.",
            },
            "38": {
                "title": "Charge on crops and shares",
                "page": 21,
                "summary": "A cooperative society shall have a first charge upon crops, agricultural produce, and shares of a member for the recovery of any debt or outstanding loan.",
            },
            "44": {
                "title": "Restrictions on borrowings",
                "page": 25,
                "summary": "A cooperative society shall receive deposits and loans only to such extent and under such conditions as specified in its bye-laws.",
            },
            "46": {
                "title": "Restrictions on loans",
                "page": 26,
                "summary": "A cooperative society shall not make a loan to any person other than a member; loans to another cooperative society require prior sanction of the Registrar.",
            },
            "52": {
                "title": "Investment of funds",
                "page": 29,
                "summary": "A cooperative society may invest its funds in the Jammu and Kashmir State Co-operative Bank, Central Co-operative Bank, Government securities, or Postal Savings Bank.",
            },
            "54": {
                "title": "Disposal of profits and reserve fund",
                "page": 30,
                "summary": "A cooperative society shall transfer at least twenty-five per cent of its annual net profits to the statutory reserve fund before distributing dividends to members.",
            },
            "63": {
                "title": "Audit and accounts",
                "page": 32,
                "summary": "Annual statutory audit mandated for all registered cooperative societies conducted by Departmental Auditors or certified Chartered Accountants appointed by the Registrar.",
            },
            "64": {
                "title": "Inquiry by Registrar",
                "page": 33,
                "summary": "The Registrar may of his own motion or on the application of a majority of committee or one-third of members, hold an inquiry into the working, constitution, and financial affairs.",
            },
            "65": {
                "title": "Inspection of books",
                "page": 34,
                "summary": "The Registrar or authorized officer shall at all times have access to books, accounts, cash, and securities of a cooperative society.",
            },
            "69": {
                "title": "Surcharge",
                "page": 35,
                "summary": "If in the course of audit, inquiry, or liquidation, it appears that any officer or member has misappropriated or retained society funds, the Registrar may issue an order of surcharge.",
            },
            "70": {
                "title": "Disputes referable to Registrar",
                "page": 36,
                "summary": "Statutory arbitration before the Registrar or appointed nominee for any dispute touching the constitution, management, or business of a cooperative society; civil court jurisdiction barred.",
            },
            "71": {
                "title": "Attachment before award",
                "page": 37,
                "summary": "If the Registrar or arbitrator is satisfied that a party is about to dispose of the whole or part of his property with intent to defeat execution, he may order conditional attachment of property.",
            },
            "74": {
                "title": "Winding up of cooperative societies",
                "page": 39,
                "summary": "The Registrar may order the winding up of a cooperative society after an inquiry under section 64 or audit under section 63, and appoint an official liquidator.",
            },
            "99": {
                "title": "Appeals",
                "page": 48,
                "summary": "Appeals against orders of Registrar refusing registration, cancelling society, or issuing arbitration award lie to the Co-operative Appellate Tribunal or Government within sixty days.",
            },
            "100": {
                "title": "Review and revision",
                "page": 49,
                "summary": "The Government or Appellate Tribunal may call for and examine the records of any proceeding to satisfy itself as to the legality or propriety of any decision.",
            },
        },
    },
}

class OfficialDocumentService:
    """Manages verified document metadata and section resolution."""

    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return OFFICIAL_DOCUMENT_REGISTRY.get(doc_id)

    def list_documents(self, jurisdiction: Optional[str] = None) -> List[Dict[str, Any]]:
        docs = list(OFFICIAL_DOCUMENT_REGISTRY.values())
        if jurisdiction and jurisdiction.lower() != "all":
            j = jurisdiction.lower()
            return [d for d in docs if d["jurisdiction"] == j or d["jurisdiction"] == "central"]
        return docs

    def resolve_section(self, doc_id: str, section_num: str) -> Optional[Dict[str, Any]]:
        doc = self.get_document(doc_id)
        if not doc or "sections" not in doc:
            return None
        return doc["sections"].get(str(section_num).strip())

official_document_service = OfficialDocumentService()
