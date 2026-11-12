from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine


class RedactManager:

    def __init__(self, config: dict):

        self.config = config

        self.language = config["pii"]["language"]

        self.entities = config["pii"]["entities"]

        self.score_threshold = config["pii"]["score_threshold"]


        # Initialize Presidio engines
        self.analyzer = AnalyzerEngine()

        self.anonymizer = AnonymizerEngine()


    def performRedacting_Of_PII(self, txt: str) -> str:

        # Analyze PII using config.yaml settings
        results = self.analyzer.analyze(

            text=txt,

            language=self.language,

            entities=self.entities,

            score_threshold=self.score_threshold

        )


        # Anonymize detected PII
        anonymized_result = self.anonymizer.anonymize(

            text=txt,

            analyzer_results=results

        )


        return anonymized_result.text