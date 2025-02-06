from langchain_community.llms import Ollama
import json
json_content_later = """{{
    "loan_proposed": "",
    "loan_requested": "",
    "confidence_for_loan_requested" : "",
    "analyze_on_statments" : "",
}}"""


json_content = """{{
    "customer_name" : ""
    "loan_proposed": {
        "minimum" : "",
        "maximum" : "",
    },
    "interest_proposed" : "",
    "analyze_on_statments" : "",
    "most_transacted_category" : [
        {
            "category" : "",
            "percentage" : ""
        }
    ]
}}"""

class LLamaModel:
    def llm():
        llm = Ollama(model="llama3")
        return llm
    
    def input_data(bank_statement):
        prompt = f"""
            Analyze the following bank transactions and provide insights, such as spending trends, potential savings, and any unusual activity. Fill relevant information in the JSON template
                
            Bank statements:

            {bank_statement}

            JSON template:

            {json_content}

            Instructions:
            1.Extract relevant information from the bank statement for each field in the JSON template
            2.For the customer_name attribute, extract the name of the owner of the bank statement
            3.For the loan_proposed attribute, make your prediction on what range of money (minimum to maximum in dollars) is the reasonable amount that a bank should loan this person
            4.For the interest_proposed attribute, make your approximation on what interest rate will be the most reasonable to apply to the above loan
            5.For the analyze_on_statements attribute, make an overall observation of spending trends and any unusual activity, and provide a brief reason why you would propose the amount of money above for lending
            6.For the most_transacted_category, approximate the 3 category that the user made the most transactions on (no need to be accurate). Approximate the overall percentage that these transactions account for with a single integer percentage. Fill in 3 objects of the array following the provided format.
            7.Ensure all keys from the template are present in the output JSON.
            8.Format the output as a valid JSON string.
            9.Ignore the empty field.

            Output the filled JSON template only, without any additional text or explanations.
        """
        return prompt


def call_model(text):
    llm = LLamaModel.llm()
    data = llm.invoke(LLamaModel.input_data(text))
    # print(type(data))
    # print(data)
    # temp = json.loads(data)
    return data




if __name__ == "__main__":
    # prompt = f'''Use this fact to answer the question: Title of each class Trading Symbol(s) Name of each exchange on which registered
    # # Common Stock, Par Value $.01 Per Share MMM New York Stock Exchange
    # # MMM Chicago Stock Exchange, Inc.
    # # 1.500% Notes due 2026 MMM26 New York Stock Exchange
    # # 1.750% Notes due 2030 MMM30 New York Stock Exchange
    # # 1.500% Notes due 2031 MMM31 New York Stock Exchange

    # # Which debt securities are registered to trade on a national securities exchange under 3M's name as of Q2 of 2023?'''


    bank_statement = """
Money Out                                    £3801.48  Balance on 30 November 2019 £2062.05                    
     Date                        Description                                  Type   In (£) Out (£) Balance (£)
 04 Sep19 LNK COOPERATIVE SW CD 4821 08DEC19                                   CPT           300.00      873.56
 09 Sep19               P ADAMCZUK KASA 7420                                   TFR    50.00                    
                                                                                                         923.56
 11 Sep19                BARCLAYCARD CD 7420                                   DEB             2.50      921.06
 15 Sep19              WESTERN VILLA CD 7420                                   DEB                       681.06
                                                                                             240.00            
 16 Sep19                   WINELEAF CD 7420                                   DEB            26.69      654.37
 17 Sep19 LNK COOPERATIVE SW CD 7420 06DEC19                                   CPT           200.00      454.37
 18 Sep19               LV LIFE 03592291015W                                    DD            33.03      421.34
 22 Sep19         PARK FOOD AND WINE CD 7420                                   DEB            30.46      390.88
 22 Sep19 LNK COOPERATIVE SW CD 7420 05DEC19                                   CPT            20.00      370.88
 25 Sep19 LNK COOPERATIVE SW CD 7420 03DEC19                                   CPT           200.00      170.88
 26 Sep19                  UBER  *TRIP LJSAM                                   DEB                       153.45
                                                                                              17.43            
                                 D ROBERTSON                                         960.00             1113.45
 29 Sep19                                                                      DEB                             
                            WINELEAF CD 7420                                   DEB            17.00            
03 Oct 19                                                                                               1096.45
05 Oct 19              KATE EYR G D LTD KEGD                                   FPI   790.00             1886.45
                          RP4679969826950500                                                                   
 08 Oct19 LNK COOPERATIVE SW CD 7420 01DEC19                                   CPT           100.00     1786.45
 12 Oct19 LNK PO MITCHAM LAN CD 7420 30NOV19                                   CPT            10.00     1776.45
                     MIS BAR MLECZNY CD 7420                                   DEB            28.90     1747.55
12 Oct 19                                                                                                      
16 Oct 19           SPORTSDIRECT 252 CD 7420                                   DEB            27.99     1719.56
19 Oct 19              KATE EYR G D LTD KEGD                                   FPI   860.00             1849.56
                          RP4679969433992900                                                                   
                          LOYD STREATHAM HIG                                   CSH   730.00             2579.56
22 Oct 19                                                                                                      
                                A FARAFOSZYN                                   TFR           100.00     2479.56
 23 Oct19                                                                                                      
                                                   30 November 2019                                                                              Page 1 of 2            
               Classic statement                                                                           01 September 2019 to 30 November 2019                        
                                                                                                                                                                        
                    Oleh Beshleu                                                       Sort code: 11-10-51                                                              
                 293 STRONE ROAD                                                          BIC: LOYDGB21033                                                              
MANOR PARK(BARKING AND DAGENHAM)                                                                                                                                        
                                                                                  Account number: 45201526                                                              
                          LONDON                                                                                                                                        
                                                                              IBAN: GB17LOYD30135525281061                                                              
                         E12 6TR                                                                                                                                        
                        Money In                                    £5420.12  Balance on 01 September 2019                              £1173.56                        
                                                                                                                                                                        
                       Money Out                                     £3801.48  Balance on 30 November 2019                              £2062.05                        
                            Date                        Description                                   Type                                In (£)     Out (£) Balance (£)
                        04 Sep19 LNK COOPERATIVE SW CD 4821 08DEC19                                    CPT                                            300.00      873.56
                        09 Sep19               P ADAMCZUK KASA 7420                                    TFR                                 50.00                        
                                                                                                                                                                  923.56
                        11 Sep19                BARCLAYCARD CD 7420                                    DEB                                              2.50      921.06
                        15 Sep19              WESTERN VILLA CD 7420                                    DEB                                                        681.06
                                                                                                                                                      240.00            
                        16 Sep19                   WINELEAF CD 7420                                    DEB                                             26.69      654.37
                        17 Sep19 LNK COOPERATIVE SW CD 7420 06DEC19                                    CPT                                            200.00      454.37
                        18 Sep19               LV LIFE 03592291015W                                     DD                                             33.03      421.34
                        22 Sep19         PARK FOOD AND WINE CD 7420                                    DEB                                             30.46      390.88
                        22 Sep19 LNK COOPERATIVE SW CD 7420 05DEC19                                    CPT                                             20.00      370.88
                        25 Sep19 LNK COOPERATIVE SW CD 7420 03DEC19                                    CPT                                            200.00      170.88
                        26 Sep19                  UBER  *TRIP LJSAM                                    DEB                                                        153.45
                                                                                                                                                       17.43            
                                                        D ROBERTSON                                                                       960.00                 1113.45
                        29 Sep19                                                                       DEB                                                              
                                                   WINELEAF CD 7420                                    DEB                                             17.00            
                       03 Oct 19                                                                                                                                 1096.45
                       05 Oct 19              KATE EYR G D LTD KEGD                                    FPI                                790.00                 1886.45
                                                 RP4679969826950500                                                                                                     
                        08 Oct19 LNK COOPERATIVE SW CD 7420 01DEC19                                    CPT                                            100.00     1786.45
                        12 Oct19 LNK PO MITCHAM LAN CD 7420 30NOV19                                    CPT                                             10.00     1776.45
                                            MIS BAR MLECZNY CD 7420                                    DEB                                             28.90     1747.55
                       12 Oct 19                                                                                                                                        
                       16 Oct 19           SPORTSDIRECT 252 CD 7420                                    DEB                                             27.99     1719.56
                       19 Oct 19              KATE EYR G D LTD KEGD                                    FPI                                860.00                 1849.56
                                                 RP4679969433992900                                                                                                     
                                                 LOYD STREATHAM HIG                                    CSH                                730.00                 2579.56
                       22 Oct 19                                                                                                                                        
                                                       A FARAFOSZYN                                    TFR                                            100.00     2479.56
                        23 Oct19                                                                                                                                        
                                             Lloyds Bank - Print Friendly Statement                       
                            WINELEAF CD 7420                                    DEB         10.50 2469.06.
23 Oct 19                                                                                                 
24 Oct 19 LNK PO MITCHAM LAN CD 7420 11SEP15                                    CPT        150.00  2319.06
27 Oct 19                   MCDONALDS CD7420                                    DEB                2293.67
                                                                                            25.79         
30 Oct 19               SUPER CHOICE CD 7420                                    DEB         76.60  2216.67
05 Nov 19          TESCO STORES 6765 CD 7420                                    DEB                2174.07
                                                                                            42.60         
06 Nov 19                   CROY CTRL 773001                                        200.12         2374.07
                                                                                DEB                       
07 Nov 19       VODAFONE LTD 7014378191-1001                                     DD         50.00  2324.07
11 Nov 19          LOYD ROYDON CENTR CD 7420                                    CPT        200.00  2124.07
13 Nov 19         NIKE FACTORY STORE CD 7420                                               250.00  1874.07
                                                                                DEB                       
13 Nov 19                 LOYD STREATHAM HIG                                    CSH        340.00  1534.04
                       .$7( (<5 * ' /7' .(*'                                    )3, 870.00         2404.04
14 Nov 19                                                                                                 
                                          53                                                              
                                                                                            56.60  2347.44
17 Nov 19                 KINGS TUN  CD 7420                                    DEB                       
          LNK COOPERATIVE SW CD 7420 17NOV19                                    CPT        170.00  2177.44
18 Nov 19                                                                                                 
17 Nov 19                 KINGS TUN  CD 7420 DEB         56.60        
          LNK COOPERATIVE SW CD 7420 17NOV19 CPT        170.00 2177.44
18 Nov 19                                                             
                                                        185.60 1991.84
19 Nov 19               WESTERN VILLA CD7420 DEB                      
                             P ADAMCZUK KASA TFR        210.00 1781.84
19 Nov 19                                                             
22 Nov 19             BEDFORD TAVERN CD 7420 DEB        198.00 1583.84
                           MCDONALDS DC 7420             16.34 1567.05
 23 Nov19                                    DEB                      
26 Nov 19              KATE EYR G D LTD KEGD FPI 960.00               
                                                               2527.05
                          RP4679966305820600                          
        28 Nov 19                                                                                                        DELIGHT CD 7420 DEB 133.45        
        29 Nov 19                                                                                             Amazon UK Marketpl CD 7420 DEB 262.00 2062.05
                        Lloyds Bank plc Registered Office: 25 Gresham Street, London EC2V 7HN. Registered in England and Wales No: 2065.                   
                   Authorised by the Prudential Regulation Authority and regulated by the Financial Conduct Authority and the Prudential                   
                                                                                 Regulation Authority, under registration number 119278.                   
                     Eligible deposits with us are protected by the Financial Services Compensation Scheme (FSCS). We are covered by the                   
                  Financial Ombudsman Service(FOS). Please note that due to FSCS and FOS eligibiliti criteria not all business customers                   
                            will be covered. For further information about the compensation provided by the FSCS,refer to the website at                   
www.FSCS.org.uk/.                                                                                                                                          
    """        


    call_model(bank_statement)