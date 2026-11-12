from presidio_analyzer import AnalyzerEngine

from presidio_anonymizer import AnonymizerEngine
 
analyzer = AnalyzerEngine()

anonymizer = AnonymizerEngine()
 
def pii_filter(txt: str) -> str:
    results = analyzer.analyze(
        text=txt,
        language="en",
        entities=["PHONE_NUMBER", "EMAIL_ADDRESS"],
        score_threshold=0.70
    )

    anonymized_result = anonymizer.anonymize(
        text=txt,
        analyzer_results=results
    )

    return anonymized_result.text
 
res = pii_filter("I am Nalla and my mail id is nalla@hexa.com and phone in 9812398123")

print(res)
