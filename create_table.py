from models import *
import db
import os
 
 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
 
        # テーブルを作成する
        Base.metadata.create_all(db.engine)
    username='last'
    # サンプルユーザ(admin)を作成
    admin = User(username=username)
    db.session.add(admin)  # 追加
    db.session.commit()  # データベースにコミット
 
    # サンプルタスク
    task = Task(
        user_id=admin.id,
        user_name=username,
        position=0)
    db.session.add(task)
    db.session.commit()
 
    db.session.close()  # セッションを閉じる