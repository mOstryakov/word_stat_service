import os
import uuid
import aiofiles
from concurrent.futures import ProcessPoolExecutor
import asyncio
from app.domain.text_processor import TextProcessor
from app.infrastructure.excel_exporter import ExcelExporter

executor = ProcessPoolExecutor()


async def run_in_process(file_path: str):
    loop = asyncio.get_event_loop()
    processor = TextProcessor()
    return await loop.run_in_executor(
        executor, processor.process_file, file_path
    )


class ReportService:
    @staticmethod
    async def create_report(upload_file) -> tuple:
        file_id = str(uuid.uuid4())
        temp_path = f"temp_files/{file_id}.txt"
        os.makedirs("temp_files", exist_ok=True)

        async with aiofiles.open(temp_path, "wb") as out_file:
            while content := await upload_file.read(1024 * 1024):
                await out_file.write(content)

        try:
            stats_data = await run_in_process(temp_path)

            excel_file = ExcelExporter.export_to_bytes(stats_data)
            return excel_file, upload_file.filename

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
