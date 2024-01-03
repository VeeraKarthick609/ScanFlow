# app.py

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os, cassio
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from flask import jsonify

app = Flask(__name__)

uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

ASTRA_DB_APPLICATION_TOKEN = "AstraCS:ILZypOGjFwoIJhZRiNLBRQrL:313ee209ea64ff5189789c1e2150c2c91cd0fd077b21c89981e317153a9cf2f3"
ASTRA_DB_ID = "a8f85ee4-aea7-4c60-8be2-5a1531d14788"
OPENAI_API_KEY = "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"

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None
)

astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            file_path = os.path.join(uploads_dir, secure_filename(file.filename))
            file.save(file_path)

            raw_text = extract_text_from_pdf(file_path)
            texts = text_splitter.split_text(raw_text)
            astra_vector_store.add_texts(texts=texts[:50])
            print("Inserted %i headlines." % len(texts[:50]))

            return redirect(url_for('result', file_path=file_path, texts=texts[:50]))

    return render_template('upload.html')

@app.route('/result')
def result():
    file_path = request.args.get('file_path')
    texts = request.args.get('texts')

    return render_template('result.html', file_path=file_path, texts=texts)

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    query_text = data.get('queryText', '')

    answer = astra_vector_index.query(query_text, llm=llm).strip()

    return jsonify({'answer': answer})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def extract_text_from_pdf(file_path):
    raw_text = ""
    pdf_reader = PdfReader(file_path)

    for i, page in enumerate(pdf_reader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    return raw_text

@app.route('/delete_file', methods=['GET'])
def delete_file():
    try:
        print("Deleting123")
        # Get the file_path from the query parameters
        file_path = request.args.get('file_path', '')

        # Construct the full path to the file
        file_path = os.path.join(uploads_dir, secure_filename(file_path))

        # Delete the file
        os.remove(file_path)

        # Redirect to the root page
        return redirect(url_for('upload_file'))

    except Exception as e:
        print(f"Error deleting file: {str(e)}")
       


if __name__ == '__main__':
    app.run(debug=True)
