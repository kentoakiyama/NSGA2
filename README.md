# NSGA2

遺伝的アルゴリズムの一種である[NSGA2](https://ieeexplore.ieee.org/document/996017)のコードになります。

## 特徴
### 高速優越ソート

### 混雑度ソートによる個体選択

## 使い方
### 問題設定
問題の設定はクラスを用いて定義してください。
インスタンス変数として


- n_var:    決定変数の数
- n_obj:    目的関数の数
- n_constr: 制約関数の数
- xl:       決定変数の下限値
- xu:       決定変数の上限値


が必要です。


また、目的関数・制約関数の評価のためにevaluateメソッドを記述してください。


evaluateメソッドは引数として、


- x:   決定変数
- gen: 世代数
- id:  個体ID


を受け取ります。（gen, idはメソッド内でのフォルダ作成で使用する可能性があったため追加しています。）


返り値として、目的関数と制約関数をそれぞれリスト形式で返してください。


例としてZDT2の定義を示します。
```python
class ZDT2:
    def __init__(self):
        self.n_var = 2              # number of variables
        self.n_obj = 2              # number of objective functions
        self.n_constr = 0           # number of constraint functions
        self.xl = np.array([0, 0])  # lower bound for variables
        self.xu = np.array([1, 1])  # upper bound for variables
    
    def evaluate(self, x, gen, id):
        x1, x2 = x
        # objective fucntions
        f1 = x1
        g = 1 + 9 * x2 / (self.n_var - 1)
        f2 = g * (1 - (f1 / g)**2)
        return [f1, f2], []
```

## 環境
- numpy
- matplotlib


