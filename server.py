import json
from aiohttp import web
from models import Advertisement, Session, close_orm, init_orm
from sqlalchemy import select


#создание приложения
app = web.Application()

#контекст-менеджер для ORM
async def orm_context(app: web.Application): 
    print("STARTED")
    await init_orm()
    yield
    print("FINISHED")
    await close_orm()
    
app.cleanup_ctx.append(orm_context)

#обработка ошибок
def get_error(err_cls, message: str | dict | list):
    json_response = json.dumps({"error": message})
    return err_cls(text=json_response, content_type="application/json")


#методы
class AdvView(web.View):
    
    async def get(self):
        adv_id = int(self.request.match_info.get("adv_id"))  
        async with Session() as session:
            result = await session.execute(select(Advertisement).where(Advertisement.id == adv_id))
            adv = result.scalars().first()
            if not adv:
                raise get_error(web.HTTPNotFound, "Advertisement was not found")
            return web.json_response(adv.dict, status=200)
        
    async def post(self):
        try:
            data = await self.request.json()
        except json.JSONDecodeError:
            raise get_error(web.HTTPBadRequest, "Invalid JSON")
        
        async with Session() as session:
            try:
                
                new_adv = Advertisement(**data)
                session.add(new_adv)
                await session.commit()
                return web.json_response({"message": "New advertisement has been added"})
            except (ValueError, TypeError) as e:
                raise get_error(web.HTTPBadRequest, str(e))
            
                    
    async def delete(self):
        adv_id = int(self.request.match_info.get("adv_id"))
        async with Session() as session:
            result = await session.execute(select(Advertisement).where(Advertisement.id == adv_id))
            adv = result.scalars().first()
            if not adv:
                raise get_error(web.HTTPNotFound, "Advertisement was not found")
            await session.delete(adv)
            await session.commit()
            return web.json_response({"status":"The advertisement was deleted successfully"})
        
        
    async def patch(self):
        adv_id = int(self.request.match_info.get("adv_id"))
        try:
            data = await self.request.json()
        except json.JSONDecodeError:
            raise get_error(web.HTTPBadRequest, "Invalid JSON")

        async with Session() as session:
            result = await session.execute(select(Advertisement).where(Advertisement.id == adv_id))
            adv = result.scalars().first()
            if not adv:
                raise get_error(web.HTTPNotFound, "Advertisement was not found")
            
        for key, value in data.items():
            if hasattr(adv, key):
                setattr(adv, key, value)
                
        await session.commit()
        return web.json_response({"message": "Advertisement has been updated", "id": adv.id})
    

#маршруты
app.add_routes(
    [
    web.post("/ads", AdvView),
    web.get("/ads/{adv_id:[0-9]+}", AdvView),
    web.patch("/ads/{adv_id:[0-9]+}", AdvView),
    web.delete("/ads/{adv_id:[0-9]+}", AdvView),
    ]
)

#запуск сервера
web.run_app(app)