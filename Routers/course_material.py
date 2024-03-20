from fastapi import APIRouter,Depends,status,HTTPException
from Schemas import schemas
from Database import mysql_database_Config
from sqlalchemy.orm import Session 
from Models import models
from Security_and_Auth import authentication

router=APIRouter(tags=["Course_Material"])

@router.post("/create_course_material",status_code=status.HTTP_201_CREATED,response_model=schemas.Course_Material_Response)
def create_teacher(new_course_material:schemas.New_Course_Material,db:Session=Depends(mysql_database_Config.get_db)
                   ,current_user:int=Depends(authentication.get_current_user)):
    coursematerial_to_be_added=models.course_material(** new_course_material.dict())
    db.add(coursematerial_to_be_added)
    db.commit()
    db.refresh(coursematerial_to_be_added)
    return coursematerial_to_be_added

@router.get("/get_all_course_materials")
def getting_all_course_materials(db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    data_to_send_back=db.query(models.course_material).all()
    return data_to_send_back

@router.get("/get_coursematerial_by_id/{id}",response_model=schemas.Course_Material_Response)
def getting_the_Course_material(id:int,db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    data_to_send_back=db.query(models.course_material).filter(models.course_material.course_material_id==id).first()
    if data_to_send_back==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    return data_to_send_back

@router.delete("/delete_course_material_by_id/{id}",status_code=status.HTTP_200_OK)
def deleting_course_material(id:int,db:Session=Depends(mysql_database_Config.get_db),current_user:int=Depends(authentication.get_current_user)):
    x=db.query(models.course_material).filter(models.course_material==id)
    if x==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    x.delete(synchronize_session=False)
    db.commit()
    return {"Message":"Successful"}

@router.put("/update_course_material/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Course_Material_Response)
def updating_course_material(id:int,update_course_material:schemas.Update_Course_Material,db:Session=Depends(mysql_database_Config.get_db)
                     ,current_user:int=Depends(authentication.get_current_user)):
    x=db.query(models.course_material).filter(models.course_material.course_material_id==id)
    if x==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id does not exist")
    x.update(update_course_material.dict())
    db.commit()
    send_back_to_user=db.query(models.course_material).filter(models.course_material.course_material_id==id).first()
    return send_back_to_user
