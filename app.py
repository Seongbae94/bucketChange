from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.4whgra5.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    buckets = list(db.bucket.find({}, {'_id': False}))
    count = len(buckets) + 1;

    doc = {
        'bucket': bucket_receive,
        'num': count,
        'done': 0,
    }

    db.bucket.insert_one(doc)
    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket/undone", methods=["POST"])
def bucket_undone():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})

    return jsonify({'msg': '버킷 실패!'})

@app.route("/bucket/change", methods=["POST"])
def bucket_change():
    num_receive = request.form['num_give']
    changeVal_receive = request.form['changeVal_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'bucket': changeVal_receive}})
    return jsonify({'msg': '버킷 취소!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)