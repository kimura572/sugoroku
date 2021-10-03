from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import db
from models import User, Task
import re
import sugoroku, position
# from fastapi.middleware.cors import CORSMiddleware

pattern = re.compile(r'\w{4,20}')  # 任意の4~20の英数字を示す正規表現

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
# origins = [
#     "*"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# テンプレート関連の設定 (jinja2)
templates = Jinja2Templates(directory="templates")
jinja_env = templates.env  # Jinja2.Environment : filterやglobalの設定用

def index(request: Request):
    return templates.TemplateResponse('index.html',
                                      {'request': request})

def admin(request: Request):
    # とりあえず今はadminユーザのみ取得
    user = db.session.query(User).all()
    task = db.session.query(Task).all()
    db.session.close()
 
    return templates.TemplateResponse('admin.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})

async def register(request: Request):
    if request.method == 'GET':
        task = db.session.query(Task).all()
        db.session.close()
        return templates.TemplateResponse('register.html',
                                          {'request': request,
                                            'task': task})
 
    if request.method == 'POST':
        # POSTデータ
        data = await request.form()
        username = data.get('username')

        tmp_user = db.session.query(User).filter(User.username == username).first()
        task = db.session.query(Task).all()
        # エラーがあれば登録ページへ戻す
        if tmp_user is not None:
            db.session.close()
            error = '同じユーザ名のユーザが存在します。'
            return templates.TemplateResponse('register.html',
                                             {'request': request,
                                             'task': task,
                                             'error': error})
        
        # 問題がなければユーザ登録
        user = User(username)
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            user_name=username,
            position=0,
            remain=24)
        db.session.add(task)
        db.session.commit()
        db.session.close()
 
        return templates.TemplateResponse('complete.html',
                                          {'request': request,
                                           'username': username})

first = -1
l = [0,0,0,0,0]
async def play(request: Request):
    user = db.session.query(User).all()
    task = db.session.query(Task).all()
    length = len(user)
    db.session.close()
    positions = 0
    lucky_number = ''
    if request.method == 'GET':
        global first
        if first != -1:
            plus_number = sugoroku.sugoroku()
            task = db.session.query(Task).all()
            data = task[first%length]
            user = data.user_name
            now_position = int(data.position)
            data, positions, lucky_number = position.position(now_position, plus_number, positions, data)
            l[first%length] = positions
            db.session.commit()
            db.session.close()
            first += 1
            if now_position + plus_number >= 24:
                return templates.TemplateResponse('agari.html',
                                      {'request': request,
                                       'user': data})
            '''セッションをcommit、closeした後にセッション内のインスタンスにアクセスすると以下エラーが発生した。
            sqlalchemy.orm.exc.DetachedInstanceError: Instance <Book at 0x697a4f0> is not bound to a Session; attribute refresh operation cannot proceed (Background on this error at: http://sqlalche.me/e/bhk3)
            デフォルトだとcommitするとセッション内のインスタンスが全て期限切れになるようだ。
            sessionmakerでexpire_on_commit=Falseオプションを付けると回避可能
            '''
        else:
            first += 1
            plus_number = ''
            # data = db.session.query(Task).filter(Task.user_name=='user').first()
            # db.session.close()
            user = ''

        return templates.TemplateResponse('play.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task,
                                       'position':plus_number,
                                       'positions':positions,
                                       'lucky_number':lucky_number,
                                       'user_number': first%length,
                                       'position_list': l})

def delete(request: Request, t_id):
    # 該当タスクを取得
    task = db.session.query(Task).filter(Task.id == t_id).first()
    user = db.session.query(User).filter(User.id == t_id).first()
 
    # もしユーザIDが異なれば削除せずリダイレクト
    if task.user_id != user.id:
        return RedirectResponse('/admin')
 
    # 削除してコミット
    db.session.delete(task)
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return RedirectResponse('/admin')