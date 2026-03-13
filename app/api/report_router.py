from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.application.report_service import ReportService

router = APIRouter(prefix="/public/report")


@router.post("/export")
async def export_report(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(
            status_code=400, detail="Only .txt files are allowed"
        )

    excel_stream, original_name = await ReportService.create_report(file)

    filename = f"report_{original_name.split('.')[0]}.xlsx"
    return StreamingResponse(
        excel_stream,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
