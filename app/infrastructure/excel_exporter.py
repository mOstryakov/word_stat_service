import pandas as pd
from io import BytesIO
from typing import List


class ExcelExporter:
    @staticmethod
    def export_to_bytes(data: List[dict]) -> BytesIO:
        df = pd.DataFrame(data)
        df.columns = ["Словоформа", "Всего", "Распределение по строкам"]

        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Статистика")

        output.seek(0)
        return output
