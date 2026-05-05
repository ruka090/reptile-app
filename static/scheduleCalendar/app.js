<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <h1>飼育個体の一覧</h1>
    {% load static %}
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Hachi+Maru+Pop&display=swap');
        /* 全体のフォントと背景画像を設定 */
        body {
            font-family: Arial, sans-serif; /* フォントファミリーの設定 */
            background-image: url('https://cdn.pixabay.com/photo/2020/06/05/19/42/lizard-5264263_1280.jpg'); /* 背景画像の設定 */
            background-position: center; /* 背景画像を中央に配置 */
            margin: 0; /* デフォルトのマージンを削除 */
            color: rgb(27, 2, 2); /* テキストカラーの設定 */
            padding-bottom: 160px; /* ナビゲーションバーの高さ分の余白 */
        }

        /* コンテナーの最大幅と中央揃え */
        .container {
            max-width: 1200px; /* 最大幅の設定 */
            margin: auto; /* 自動で中央揃え */
        }

        /* タイトルのスタイル */
        h1 {
            font-size: 2.5em;
            text-align: center;
            font-family: 'Hachi Maru Pop', sans-serif;  /* 中央揃え */
        }

        /* 検索バーのスタイル */
        .search-bar {
            margin-bottom: 20px; /* 下に余白を追加 */
            text-align: center; /* 中央揃え */
        }

        /* 検索入力フィールドのスタイル */
        .search-input {
            padding: 10px; /* 内側の余白 */
            width: 300px; /* 幅の設定 */
            border-radius: 5px; /* 角を丸める */
            border: 1px solid #ccc; /* 枠線の設定 */
        }

        /* カードコンテナのスタイル */
        .card-container {
            animation: fadeInUp 1s ease-out;
            display: flex; /* フレックスボックスレイアウト */
            flex-wrap: wrap;
            border-radius: 5px; /* 子要素が折り返すようにする */
            justify-content: center; /* 中央揃え */
        }

        /* カードのスタイル */
        .card {
            background-image: url('https://th.bing.com/th/id/OIP.CocjFA2pfGGHwoc5QnE_hAHaKb?rs=1&pid=ImgDetMain'); /* 背景画像の設定 */
            background-color: rgba(0, 0, 0, 0.8); /* 背景色と透明度 */
            border-radius: 40px; /* 角を丸める */
            padding: 20px; /* 内側の余白 */
            margin: 10px; /* 外側の余白 */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.8); /* 影の追加 */
            flex: 0 0 30%; /* 幅を30%に設定して三つ横並び */
            box-sizing: border-box; /* パディングを幅に含める */
            text-align: center; /* カード内のテキストを中央揃え */
        }

        /* 画像のスタイル */
        img {
            max-width: 100px; /* 最大幅を100pxに設定 */
            height: auto; /* 高さを自動設定 */
            border-radius: 5px; /* 角を丸める */
            margin-bottom: 10px; /* 下にマージンを追加 */
        }

        /* ボタンのスタイル */
        .button {
            transition: transform 0.3s ease, background-color 0.3s ease;
            background-color: #28a745; /* 背景色 */
            color: white; /* 文字色 */
            border: none; /* 枠線なし */
            border-radius: 5px; /* 角を丸める */
            padding: 10px 20px; /* 内側の余白 */
            cursor: pointer; /* カーソルをポインターに変更 */
            font-size: 16px; /* フォントサイズの設定 */
             /* 背景色のトランジション */
            text-decoration: none; /* テキスト装飾を削除 */
            display: inline-block; /* インラインブロックに設定 */
            margin-top: 10px; /* 上にマージンを追加 */
        }

        /* ボタンのホバー時のスタイル */
        .button:hover {
            background-color: #218838; /* ホバー時の背景色 */
        }

        /* アクションエリアのスタイル */
        .actions {
            display: flex; /* フレックスボックスレイアウト */
            justify-content: center; /* 中央揃え */
            gap: 10px; /* 子要素間の間隔 */
            margin-top: 20px; /* 上にマージンを追加 */
        }
        @keyframes fadeInUp {
    0% {
        opacity: 0;
        transform: translateY(20px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}
        /* ナビゲーションバーのスタイル */
        .navbar {
            font-family: 'Hachi Mar', sans-serif;
            background-image: url('https://i.pinimg.com/originals/e5/e8/c0/e5e8c030d4a67fd11d55b57a613517bd.jpg');
            position: fixed; /* 固定位置に配置 */
            bottom: 0; /* 画面下部に配置 */
            left: 0;
            right: 0;
            background-color: rgba(40, 167, 69, 0.9); /* 背景色と透明度 */
            display: flex; /* フレックスボックスレイアウト */
            justify-content: space-around; /* 要素を均等に配置 */
            align-items: center; /* 中央揃え */
            padding: 10px 0; /* 上下の内側余白 */
            box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.2); /* 上に影を追加 */
        }

        /* ナビゲーションリンクのスタイル */
        .navbar a {
            font-family: 'Hachi Maru Pop', sans-serif;
            color: rgb(15, 15, 15); /* 文字色 */
            font-weight: bold; /* 太字 */
            padding: 10px 15px; /* 内側の余白 */
            border-radius: 5px; /* 角を丸める */
            transition: background-color 0.3s; /* 背景色のトランジション */
            align-items: center; /* アイコンとテキストを中央に揃える */
        }

        /* ナビゲーションリンクのホバー時のスタイル */
        .navbar a:hover {
            background-color: #818181; /* ホバー時の背景色 */
        }

        /* ナビゲーションアイコンのスタイル */
        .navbar a img.navbar-icon {
            width: 60px; /* アイコンの幅を設定 */
            height: 60px; /* アイコンの高さを設定 */
            margin-right: 1px; /* アイコンとテキストの間にスペースを追加 */
        }
        .reptile.thumbnail{
            object-fit: cover;
            border-radius: px;
        }
    </style>
</head>
<body>
    <div class="container">

        <div class="search-bar">
            <input type="text" id="search" class="search-input" placeholder="飼育個体を検索..." oninput="filterReptiles()">
        </div>

        <div class="card-container" id="cardContainer">
            {% for reptile in reptiles %}
                <div class="card">
                    <div>
                        {% if reptile.thumbnail %}
                            <img src="{{ reptile.thumbnail.url }}" alt="{{ reptile.name }}のサムネイル画像">
                        {% else %}
                            <span>画像なし</span>
                        {% endif %}
                    </div>
                    <div class="info">
                        <h2><a href="{% url 'reptile_profile' reptile.id %}">{{ reptile.name }}</a></h2>
                        <p>種類: {{ reptile.species }}</p>
                        <p>モルフ: {{ reptile.morph }}</p>
                        <p>お迎え日:{{ reptile.acquisition_date|date:"Y年n月j日" }}</p>
                        <p>体重: {{ reptile.weight }} g</p>
                        <p>健康メモ: {{ reptile.health_notes }}</p>
                    </div>
                    <a href="{% url 'create_feeding_record' %}?reptile_id={{ reptile.id }}" class="button">餌をやる</a>
                </div>
            {% empty %}
                <p>飼育個体が登録されていません。</p>
            {% endfor %}
        </div>

        <div class="actions">
            <a href="{% url 'add_reptile' %}" class="button">飼育個体を追加</a>
            <a href="{% url 'logout' %}" class="button">ログアウト</a>
        </div>
    </div>

    <div class="navbar">
        <a href="{% url 'weight_history' 1 %}" class="navbar-item">
                <img src="{% static 'img\ダウンロード (2).jpg' %}" alt="分析" class="navbar-icon"> analysis 
            </a>
        <a href="{% url 'calender' %}">
            <img src="{% static 'img\ダウンロード (3).jpg' %}" alt="カレンダー" class="navbar-icon"> carendar
        </a>
        <a href="{% url 'reptile_list' %}">
            <img src="{% static 'img\bc0ff855c693f627b88ea6291dd8e261_t.jpeg' %}" alt="ペット" class="navbar-icon"> pet
        </a>
        <a href="{% url 'home' %}" class="home-link">
            <img src="{% static 'img\ダウンロード (4).jpg' %}" alt="ホーム" class="navbar-icon"> home
        </a>
    </div>

    <script>
        function filterReptiles() {
            const searchInput = document.getElementById('search').value.toLowerCase();
            const cards = document.querySelectorAll('.card');

            cards.forEach(card => {
                const name = card.querySelector('h2 a').textContent.toLowerCase();
                if (name.includes(searchInput)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    </script>
</body>
</html>
