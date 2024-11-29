import pandas as pd
import os

'''
指定ディレクトリ内の全csvファイルの各列の値の種類とその割合を調べてtxtファイルに出力する関数
引数はディレクトリパスと出力ディレクトリ名（基本デフォルトで良い）
'''
def analyze_all_csv(directory_path='data', output_dirname='analysis'):
    # 出力先ディレクトリを作成（存在しない場合）
    os.makedirs(output_dirname, exist_ok=True)
    
    # 入力ディレクトリ内のCSVファイルをすべて取得
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        input_path = os.path.join(directory_path, csv_file)  # 入力ファイルのフルパス
        output_name = os.path.splitext(csv_file)[0]  # 拡張子を除いたファイル名
        output_path = os.path.join(output_dirname, output_name)  # 出力ファイルのパス
        print(f"Processing file: {csv_file}")
        
        # CSVファイルを読み込み
        try:
            df = pd.read_csv(input_path)
            # 別ファイルの関数を呼び出して解析し、出力先を指定
            analyze_column(df, output_path)
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")


'''
指定のcsvファイルの各列の値の種類とその割合を調べる関数
引数はデータフレームと出力ファイル名（.txtより前の部分）
'''
def analyze_column(df, output_name):
    with open(f'{output_name}.txt', 'w', encoding='utf-8') as f:
        for column in df.columns:
            f.write(f"Column: {column}\n")
            
            # 欠損値（NaN）の数を取得
            total_rows = len(df)
            missing_values = df[column].isna().sum()
            missing_ratio = missing_values / total_rows
            
            f.write(f"  Missing Values: {missing_values} ({missing_ratio:.2%})\n")
            
            value_counts = df[column].value_counts(normalize=False)  # 値のカウントを取得
            value_ratios = df[column].value_counts(normalize=True)  # 値の割合を取得
            num_unique_values = len(value_counts)
            
            if num_unique_values >= 10:
                f.write(f"  （値の種類が{num_unique_values}あります。上位10個を表示します。）\n")
                value_counts = value_counts.head(10)  # 上位10個のカウントを取得
                value_ratios = value_ratios.head(10)  # 上位10個の割合を取得
            
            for (value, count), ratio in zip(value_counts.items(), value_ratios):
                f.write(f"  Value: {value}, Count: {count}, Ratio: {ratio:.2%}\n")
            
            f.write("-" * 50 + "\n")
            

'''
ある説明変数と目的変数の関係を調べる関数。カテゴリ変数に有効
引数はデータフレームと説明変数、目的変数
'''
def relation_between_target(df, explanatory_column, objective_column):
    crosstab_counts = pd.crosstab(df[f'{explanatory_column}'], df[f'{objective_column}'])
    
    # 行ごとの割合
    crosstab_row_ratios = crosstab_counts.div(crosstab_counts.sum(axis=1), axis=0) * 100
    crosstab_row_ratios = crosstab_row_ratios.map(lambda x: f"{x:.1f}%")  # フォーマット

    print("Ratios (行方向):\n", crosstab_row_ratios)
    
# df = pd.read_csv('data/train_student_info.csv')
# relation_between_target(df, 'studied_credits', 'final_result')