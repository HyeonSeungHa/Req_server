import sqlite3
import time
import traceback
import logging
from fastapi import FastAPI, Request 

reqApp = FastAPI(root_path='/')

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.DEBUG,
    datefmt='%m/%d/%Y %I:%M:%S %p',
)

# 결과 값 받기
@reqApp.post("/req/")
async def req_msg(request: Request):
    json_data = await request.json()
    logging.info(f'Get Request :: {json_data}')
    # 결과 값 insert
    status = insert_req(json_data)
    
    return status

# DB에서 결과값 찾기
@reqApp.get("/getData/{task_id}")
def get_data(task_id: str):
    logging.info(f'Get task_id :: {task_id}')
    result = data_from_db(task_id=task_id)
    # 결과값 삭제
    delete_data = delete_req()
    if delete_data == False:
        logging.error('Delete Data err')
    else:
        logging.info(f'Delete Data :: {delete_data}')
        
    return result


# 결과값 조회
def data_from_db(task_id: str):
        try:
            count = 0
            while True:
                conn = sqlite3.connect('req_db.db')
                cur = conn.cursor()
                
                cur.execute(f'SELECT * FROM REQ_DATA WHERE task_id = "{task_id}"')
                
                row = cur.fetchall()
                conn.close()
                if not row:
                    time.sleep(1)
                    count += 1
                    logging.info(f'Wait ::: {count}')
                    pass
                else:
                    logging.info('Get Data From DB')
                    return {'task_id' : row[0][0], 'gid' : row[0][1], 'end_point' : row[0][2]}
        except IndexError:
            pass
        except:
            logging.error(traceback.format_exc())

# 결과값 INSERT
def insert_req(data):
    try:
        logging.info('Insert Data Start')
        conn = sqlite3.connect('req_db.db')
        cur = conn.cursor()
        
        cur.execute('INSERT INTO REQ_DATA Values(:Task_id, :Gid, :End_point);', {'Task_id' : data['task_id'], 'Gid': data['upload_gid'], 'End_point' : data['req_info']['end_point']})
        
        conn.commit()
        conn.close()
        logging.info('Insert Data Done')
        return True
    
    except:
        logging.error(traceback.format_exc())
        
        return False

# 결과값 삭제
def delete_req():
    try:
        logging.info('Delete Data Start')
        conn = sqlite3.connect('req_db.db')
        cur = conn.cursor()
        
        cur.execute('SELECT COUNT(*) FROM REQ_DATA')
        row = cur.fetchone()
        if row[0] >= 5:
            cur.execute('DELETE FROM REQ_DATA WHERE 1=1')
            conn.commit()
            conn.close()
        else:
            conn.close()
            
        return row[0]
    
    except:
        logging.error(traceback.format_exc())
        
        return False