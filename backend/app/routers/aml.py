from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.auth import verify_token
from app.models.user import User

from app.repositories.aml_repository import AMLRepository
from app.schemas.aml import (
    AMLAlertResponse,
    AMLDashboard,
    AMLStatusUpdate
)

router = APIRouter(
    prefix="/aml",
    tags=["AML"]
)


@router.get(
    "/alerts",
    response_model=list[AMLAlertResponse]
)
def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    return AMLRepository.get_all_alerts(db)


@router.get(
    "/alerts/{alert_id}",
    response_model=AMLAlertResponse
)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    alert = AMLRepository.get_alert_by_id(
        db,
        alert_id
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.patch(
    "/alerts/{alert_id}",
    response_model=AMLAlertResponse
)
def update_alert(
    alert_id: int,
    payload: AMLStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    alert = AMLRepository.get_alert_by_id(
        db,
        alert_id
    )

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return AMLRepository.update_status(
        db,
        alert,
        payload.status
    )


@router.get(
    "/dashboard",
    response_model=AMLDashboard
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
    return AMLRepository.get_dashboard_statistics(db)