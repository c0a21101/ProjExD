# 第4回
## 迷路ゲーム:逃げろこうかとん（ex04/dodge_bomb.py）
### ゲーム概要
- ex04/dodge.pyを実行すると，1600x900のスクリーンに草原が描画され，飛び回る爆弾からこうかとんを操作して爆弾から逃げるゲーム
- こうかとんが爆弾と接触するとスコアが0になる
### 操作方法
- 矢印キーでこうかとんを上下左右に移動する 
### 追加機能
- 爆弾が1000フレームごとに追加出現するように
- スコアの概念を追加（1000フレームごとに爆弾の数ｘ100点加算）
- 被弾時にゲームが終了しないように
- こうかとんが爆弾と接触すると爆弾がすべて消えるように
- こうかとんが爆弾と接触するとスコアが0になるように
- 爆弾の出現位置によってこうかとんが即被弾するのを避けるためにy=10でのみ爆弾が生成されるように
## ToDo
- [ ] 被弾時の演出
- [ ] かすりボーナス（爆弾に接触するギリギリにいるとスコアが増える）
- [ ] 残基機能