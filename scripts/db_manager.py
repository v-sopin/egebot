import aiomysql
from pymysql import connect
from scripts.config import DB_NAME, DB_USER, DB_HOST, DB_PASSWORD
from scripts.models import User


async def create_con(loop):
    con = await aiomysql.connect(host=DB_HOST, user=DB_USER, db=DB_NAME, password=DB_PASSWORD, loop=loop)
    cur = await con.cursor()
    return con, cur


def create_sync_con():
    con = connect(host=DB_HOST, user=DB_USER, db=DB_NAME,
                  password=DB_PASSWORD)
    cur = con.cursor()

    return con, cur


class UsersDbManager:
    @staticmethod
    def clear():
        con, cur = create_sync_con()
        cur.execute('delete from users')
        con.commit()
        con.close()

    @staticmethod
    async def user_exist(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from users where tel_id = %s', tel_id)
        r = await cur.fetchone()
        count = r[0]
        return count > 0

    @staticmethod
    async def add_user(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into users values(%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 , 0, 1)', (tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_all_users(loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from users')
        users = await cur.fetchall()
        con.close()

        result = []
        for u in users:
            result.append(User(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[11], u[12]))
        return result

    @staticmethod
    async def get_user(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from users where tel_id = {0}'.format(tel_id))
        u = await cur.fetchone()
        con.close()

        if u is None:
            return None
        else:
            return User(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7], u[8], u[9], u[10], u[11], u[12])

    @staticmethod
    async def upd_ege_math_base(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set ege_math_base = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_ege_math_pro(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set ege_math_pro = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_ege_physics(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set ege_physics = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_ege_history(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set ege_history = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_ege_social(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set ege_social = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_oge_math(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set oge_math = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_oge_physics(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set oge_physics = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_oge_history(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set oge_history = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_oge_lit(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set oge_lit = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def upd_oge_social(tel_id, new_val, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set oge_social = {new_val} where tel_id = {tel_id}')
        await con.commit()
        con.close()

    @staticmethod
    async def update_context(tel_id, new_context, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set context = %s where tel_id = %s', (new_context, tel_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_context(tel_id, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'select context from users where tel_id = {tel_id}')
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    def sync_get_context(tel_id):
        con, cur = create_sync_con()
        cur.execute(f'select context from users where tel_id = {tel_id}')
        context = cur.fetchone()
        con.close()

        if context is None:
            return None

        return context[0]

    @staticmethod
    async def update_is_using(tel_id, new_status, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set is_using = {new_status} where tel_id = {tel_id}')
        await con.commit()
        con.close()

