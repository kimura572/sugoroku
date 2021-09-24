from fastapi import FastAPI
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import db
from models import User, Task
import re
import sugoroku

pattern = re.compile(r'\w{4,20}')  # 任意の4~20の英数字を示す正規表現

app = FastAPI(
    title='FastAPIでつくるtoDoアプリケーション',
    description='FastAPIチュートリアル：FastAPI(とstarlette)でシンプルなtoDoアプリを作りましょう．',
    version='0.9 beta'
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# new テンプレート関連の設定 (jinja2)
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
        return templates.TemplateResponse('register.html',
                                          {'request': request})
 
    if request.method == 'POST':
        # POSTデータ
        data = await request.form()
        username = data.get('username')

        # error = []
 
        # tmp_user = db.session.query(User).filter(User.username == username).first()
 
        # # 怒涛のエラー処理
        # if tmp_user is not None:
        #     error.append('同じユーザ名のユーザが存在します。')
         
        # # エラーがあれば登録ページへ戻す
        # if error:
        #     return templates.TemplateResponse('register.html',
        #                                       {'request': request,
        #                                        'username': username,
        #                                        'error': error})
        tmp_user = db.session.query(User).filter(User.username == username).first()
        # 怒涛のエラー処理
        if tmp_user is not None:
            error = '同じユーザ名のユーザが存在します。'
            return templates.TemplateResponse('register.html',
                                             {'request': request,
                                            #  'username': username,
                                             'error': error})
            
        # エラーがあれば登録ページへ戻す
        # if error:
        #     return templates.TemplateResponse('register.html',
        #                                      {'request': request,
        #                                      'username': username,
        #                                      'error': error})
    
        # 問題がなければユーザ登録
        user = User(username)
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            user_name=username,
            position=0)
        db.session.add(task)
        db.session.commit()
        db.session.close()
 
        return templates.TemplateResponse('complete.html',
                                          {'request': request,
                                           'username': username})

first = 0
async def play(request: Request):
    user = db.session.query(User).all()
    task = db.session.query(Task).all()
    if request.method == 'POST':
        db.session.close()
        return templates.TemplateResponse('play.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task})
    data = db.session.query(Task).filter(Task.user_name=='user').first()
    data.position = '10'
    db.session.close()
    db.session.commit()
    if request.method == 'GET':
        global first
        if first != 0:
            plus_number = sugoroku.sugoroku()
        else:
            first = 1
            plus_number = ''
        return templates.TemplateResponse('play.html',
                                      {'request': request,
                                       'user': user,
                                       'task': task,
                                       'data': data,
                                       'position':plus_number})

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