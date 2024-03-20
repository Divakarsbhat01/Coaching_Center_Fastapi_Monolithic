from fastapi import APIRouter,Depends,status,HTTPException
from Schemas import schemas
from Database import mysql_database_Config
from sqlalchemy.orm import Session 
from Models import models
from Security_and_Auth import authentication

router=APIRouter(tags=["mentor(Parent)"])

@router.post("/create_mentor",status_code=status.HTTP_201_CREATED,response_model=schemas.Parent_Response)
def create_student(new_parent:schemas.New_Parent,db:Session=Depends(mysql_database_Config.get_db)
                   ,current_user:int=Depends(authentication.get_current_user)):
    parent_to_be_added=models.Mentor(** new_parent.dict())
    db.add(parent_to_be_added)
    db.commit()
    db.refresh(parent_to_be_added)
    return parent_to_be_added

@router.get("/get_all_mentors")
def getting_all_mentors(db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    data_to_send_back=db.query(models.Mentor).all()
    return data_to_send_back

@router.get("/get_Mentor_by_id/{id}",response_model=schemas.Parent_Response)
def getting_the_mentor(id:int,db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    data_to_send_back=db.query(models.Mentor).filter(models.Mentor.parent_id==id).first()
    if data_to_send_back==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    return data_to_send_back

@router.delete("/delete_mentor_by_id/{id}",status_code=status.HTTP_200_OK)
def deleting_mentor(id:int,db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    x=db.query(models.Mentor).filter(models.Mentor.parent_id==id)
    if x==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    x.delete(synchronize_session=False)
    db.commit()
    return {"Message":"Successful"}

@router.put("/update_mentor/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Parent_Response)
def updating_mentor(id:int,update_mentor:schemas.Update_Parent,db:Session=Depends(mysql_database_Config.get_db)
                     ,current_user:int=Depends(authentication.get_current_user)):
    x=db.query(models.Mentor).filter(models.Mentor.parent_id==id)
    if x==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    x.update(update_mentor.dict())
    db.commit()
    send_back_to_user=db.query(models.Mentor).filter(models.Mentor.parent_id==id).first()
    return send_back_to_user