import random

class ArtifactBank:
    def __init__(self):
        """Инициализация"""
        self.available_artifacts = []

    def get_random_artifact(self):
        """Получить случайный доступный артефакт"""
        if not self.available_artifacts:
            return None
        artifact = random.choice(self.available_artifacts)
        self.available_artifacts.remove(artifact)
        return artifact

    def return_artifacts(self, artifacts):
        """Вернуть артефакты в банк (Если человек не сохранился)"""
        for artifact in artifacts:
            self.available_artifacts.append(artifact)
        print(f"ヽ(°〇°)ﾉСИСТЕМА: Артефакты возвращены в банк: {len(artifacts)} шт.")
