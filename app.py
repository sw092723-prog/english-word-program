from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    word = ""
    result = None
    error = None

    if request.method == "POST":
        word = request.form["word"].strip().lower()

        if word:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    result = response.json()[0]

                    # 검색 기록 저장
                    with open("history.txt", "a", encoding="utf-8") as f:
                        f.write(result["word"] + "\n")
                else:
                    error = "단어를 찾을 수 없습니다."

            except requests.exceptions.RequestException:
                error = "인터넷 연결 또는 서버 오류가 발생했습니다."

    return render_template(
        "index.html",
        word=word,
        result=result,
        error=error
    )


@app.route("/history")
def history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r", encoding="utf-8") as f:
            history_list = f.read().splitlines()
    else:
        history_list = []

    return render_template(
        "history.html",
        history=history_list
    )


@app.route("/delete-history")
def delete_history():
    if os.path.exists("history.txt"):
        os.remove("history.txt")

    return render_template(
        "history.html",
        history=[]
    )


if __name__ == "__main__":
    app.run(debug=True)