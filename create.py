from sqlalchemy.sql.functions import user
from models import *
import db
import os
 
 
if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):
 
        # テーブルを作成する
        Base.metadata.create_all(db.engine)
 
    # サンプルユーザ(admin)を作成
    admin = User(username='admin')
    db.session.add(admin)  # 追加
    db.session.commit()  # データベースにコミット
 
    # サンプルタスク
    task = Task(
        user_id=admin.id,
        user_name=admin.username,
        position='0',
        remain='24',
    )
    print(task)
    db.session.add(task)
    db.session.commit()
 
    db.session.close()