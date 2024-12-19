import pyxel
import random

# 定数の設定
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 160
PLAYER_SIZE = 12  # サッカーボールの大きさ
PLAYER_SPEED = 2
OBSTACLE_SPEED = 2
WIN_CONDITION = 11  # クリア条件を11人に変更
SPEED_INCREMENT = 1.25  # スピード増加倍率（1.25倍に変更）

class DribbleChallenge:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Dribble Challenge")
        self.reset_game()
        self.round = 1  # ラウンドの初期化
        self.obstacle_speed = OBSTACLE_SPEED  # 初期の障害物のスピード
        self.start_time = pyxel.frame_count  # ゲーム開始の時間を記録
        self.game_started = False  # ゲームが開始されたかどうか
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # プレイヤーの初期位置とスコア、タイマーの初期化
        self.player_x, self.player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE * 2
        self.score = 0
        self.obstacles = []  # 障害物リストをリセット
        self.game_over = False
        self.game_clear = False
        self.white_line = None  # 白い線は初期状態では表示しない

    def update(self):
        if not self.game_started:
            # ゲーム開始前の画面表示
            if pyxel.frame_count - self.start_time < 120:  # 2秒後にゲームが始まる（120フレーム）
                return
            else:
                self.game_started = True  # ゲームが開始された
                self.start_time = pyxel.frame_count  # ゲームの開始時間を再設定
                pyxel.play(0, 0)  # ゲーム開始時に音を鳴らす（音のインデックス0）

        if not self.game_over and not self.game_clear:
            # プレイヤーの移動
            if pyxel.btn(pyxel.KEY_LEFT):
                self.player_x = max(self.player_x - PLAYER_SPEED, 0)
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.player_x = min(self.player_x + PLAYER_SPEED, SCREEN_WIDTH - PLAYER_SIZE)

            # 障害物の生成と移動
            if pyxel.frame_count % 20 == 0:  # 常に新しい障害物を生成
                obstacle_x = random.randint(0, SCREEN_WIDTH - 12)  # 横幅を考慮して範囲を調整
                self.obstacles.append([obstacle_x, 0])  # 障害物は画面上部からスタート

            # 障害物の移動と、画面外に出たかのチェック
            new_obstacles = []
            for obstacle in self.obstacles:
                obstacle[1] += self.obstacle_speed  # 下方向に移動
                if obstacle[1] < SCREEN_HEIGHT:
                    new_obstacles.append(obstacle)  # 画面内にある障害物はリストに残す
                else:
                    # 障害物が画面外に出たらスコアを加算（プレイヤーが通過したとみなす）
                    if obstacle[1] > self.player_y:
                        self.score += 1  # プレイヤーが障害物を通過
            self.obstacles = new_obstacles

            # 11番目の障害物を避けたらクリア
            if self.score == WIN_CONDITION:
                self.game_clear = True
                pyxel.play(0, 1)  # ゲームクリア時に音を鳴らす（音のインデックス1）

            # 障害物との衝突判定
            for (ox, oy) in self.obstacles:
                if abs(self.player_x - ox) < 12 and abs(self.player_y - oy) < 8:  # 横幅を12に変更
                    self.game_over = True
                    pyxel.play(0, 2)  # ゲームオーバー時に音を鳴らす（音のインデックス2）

        elif self.game_clear:
            # Nキーを押すことで次のラウンドへ進む
            if pyxel.btnp(pyxel.KEY_N):
                self.round += 1  # 現在のラウンドに1を足して次のラウンドに進む
                self.reset_game()  # 新しいラウンドを始める
                self.obstacle_speed = self.obstacle_speed * SPEED_INCREMENT  # スピードを前のラウンドの1.25倍に増加

        elif self.game_over:
            # ゲームオーバー時にラウンド1に戻る
            if pyxel.btnp(pyxel.KEY_R):
                self.round = 1  # ラウンド1に戻す
                self.reset_game()  # ゲームをリセット
                self.obstacle_speed = OBSTACLE_SPEED  # 障害物の速度を初期値に戻す

    def draw(self):
        if not self.game_started:
            # 「Dribble Challenge」の「C」を画面中央に表示
            text = "Dribble Challenge"
            # 「C」の位置が画面中央になるように調整
            c_index = text.index('C')
            c_pos_x = SCREEN_WIDTH // 2 - len(text[:c_index]) * 4  # 「C」を中央に合わせるためのX座標調整
            pyxel.text(c_pos_x, SCREEN_HEIGHT // 2, text, 7)
            return

        # 背景を緑色で塗りつぶす
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 11)  # 背景色を緑（色コード 11）

        # プレイヤー（サッカーボール）
        pyxel.circ(self.player_x + PLAYER_SIZE // 2, self.player_y + PLAYER_SIZE // 2, PLAYER_SIZE // 2, 7)  # 白色
        pyxel.circ(self.player_x + PLAYER_SIZE // 2, self.player_y + PLAYER_SIZE // 2, PLAYER_SIZE // 2 - 2, 0)  # 黒色で模様

        # 障害物（ドット絵の人キャラクター）
        for (ox, oy) in self.obstacles:
            pyxel.rect(ox, oy, 12, 8, 8)  # 横幅を12に変更
            pyxel.rect(ox, oy + 8, 12, 8, 2)  # 体（赤色のTシャツ）
            pyxel.rect(ox, oy + 14, 12, 2, 10)  # 脚（白色のパンツ）

        # ラウンド数の表示
        pyxel.text(5, 5, f"Round: {self.round}", 7)

        # スコアの表示（スコアが11/11になったら固定表示）
        if self.score >= WIN_CONDITION:
            pyxel.text(5, 20, f"Score: {WIN_CONDITION}/{WIN_CONDITION}", 7)
        else:
            pyxel.text(5, 20, f"Score: {self.score}/{WIN_CONDITION}", 7)

        # ゲームオーバーおよびクリアメッセージ
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "GAME OVER!", 7)  # 白色に変更
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 10, "Press R to Restart", 7)  # 白色に変更
        elif self.game_clear:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2, "GAME CLEAR!", 7)  # 白色に変更
            pyxel.text(SCREEN_WIDTH // 2 - 40, SCREEN_HEIGHT // 2 + 10, "Press N to Next Round", 7)  # 白色に変更

# ゲームの開始
DribbleChallenge()
