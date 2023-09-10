// canvasElementを格納
var canv;

// canvas要素が持つ2dグラフィックのコンテキストを格納
var ctx;

// 初期位置
var ox = 0, oy = 0;

// 移動先
var x = 0, y = 0;

// draw中かどうか判断
var isdrawing = false;

// 初期化関数
function draw_init() {
    // canvas要素の取得
    canv = document.getElementById("can");

    // タッチイベントごとにイベントハンドラを登録
    // タッチ
    canv.addEventListener("touchstart", onDown, false);
    canv.addEventListener("touchmove", onMove, false);
    canv.addEventListener("touchend", onUp, false);
    // クリック
    canv.addEventListener("mousedown", onMouseDown, false);
    canv.addEventListener("mousemove", onMouseMove, false);
    canv.addEventListener("mouseup", onMouseUp, false);

    // 2dコンテキストの取得
    ctx = canv.getContext("2d");

    // 直線の色を黒に
    ctx.strokeStyle = "#000000";
    // 線の幅を15pxに
    ctx.lineWidth = 15;
    // 線の形状を丸く
    ctx.lineJoin = "round";
    ctx.lineCap = "round";

    // canvasのクリア処理
    clearCanv();
}

// タッチ開始時に実行
function onDown(event) {
    isdrawing = true;
    // タッチ位置からcanvasの左端までの座標(offset x)
    ox = event.touches[0].pageX - event.target.getBoundingClientRect().left;

    // タッチ位置からcanvasの上端までの座標(offset y)
    oy = event.touches[0].pageY - event.target.getBoundingClientRect().top;
    event.stopPropagation();
}

// 移動時に実行
function onMove(event) {
    // 描画中でない場合は何もしない
    if (!isdrawing) return;

    // x座標の取得
    x = event.touches[0].pageX - event.target.getBoundingClientRect().left;
    // y座標の取得
    y = event.touches[0].pageY - event.target.getBoundingClientRect().top;

    // 描画を行う
    drawLine();

    // 新しい座標を設定
    ox = x;
    oy = y;
    event.preventDefault();
    event.stopPropagation();
}

// タッチ終了時に実行
function onUp(event) {
    isdrawing = false;
    event.stopPropagation();
}


// マウスがクリック時に実行
function onMouseDown(event) {
    ox = event.clientX - event.target.getBoundingClientRect().left;
    oy = event.clientY - event.target.getBoundingClientRect().top;
    isdrawing = true;
}

// マウスが移動時に実行
function onMouseMove(event) {
    if (!isdrawing) return;
    x = event.clientX - event.target.getBoundingClientRect().left;
    y = event.clientY - event.target.getBoundingClientRect().top;
    drawLine();
    ox = x;
    oy = y;
}


// マウスがクリック終了時に実行
function onMouseUp(event) {
    isdrawing = false;
}


// 座標から描画処理を行う関数
function drawLine() {
    // 描画の開始
    ctx.beginPath();
    
    // 初期位置から描画を開始する
    ctx.moveTo(ox, oy);
    
    // 新しい座標まで描画を行う
    ctx.lineTo(x, y);

    // 描画を確定
    ctx.stroke();
}


// canvasをクリアする関数
function clearCanv() {
    // 白色
    ctx.fillStyle = "rgb(255,255,255)";
    // canvas全体を白色に
    ctx.fillRect(0, 0, canv.getBoundingClientRect().width, canv.getBoundingClientRect().height);
}

// 画像をサーバーへPOSTする関数
function sendImage() {
    // DataURLに変換
    var dataURL = canv.toDataURL("image/png");

    // jqueryを利用してAjaxリクエストを送信
    $.ajax({
        type: "POST", // HTTPリクエストメソッド
        url: "http://127.0.0.1:5000/classify/digitsdraw", // リクエストを送信するURL
        data: {
            img: dataURL
        } //リクエストデータ
    })
    .done((data)=>{
        //リクエストが成功した場合、処理結果を表示する
        $('#predict').html('あなたが書いた数字は<span class="predict">'+data['predict']+'</span>')
    });
}

// 初期化処理を走らせる
draw_init()
