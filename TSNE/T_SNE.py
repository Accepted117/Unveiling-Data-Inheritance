import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import AllChem
import sys


# 读取文件
def pd_read_file(a_file):	
    if a_file.endswith('.xlsx'):return pd.read_excel(a_file)
    if a_file.endswith('.csv'): return pd.read_csv(a_file)   
    if a_file.endswith('.txt'): return pd.read_csv(a_file,sep=' ')
    if a_file.endswith('.can') or a_file.endswith('.smi'):
        return pd.read_csv(a_file,sep='\t')
    else:
        raise Exception('error in pd_read_file for filename : {}, must end in .xlsx, .csv or .txt'.format(a_file))
	

def cal_fingerprint(df1):
    # 将读取文件的中的分子smiles转换为rdkit的mol；df['smiles]是指数据帧中的smiles列，若含smiles的列名为其它，则改为其它
    mols = [Chem.MolFromSmiles(x) for x in df1['smiles']]
    #print(mols)
    # 计算每个分子的分子指纹，用于聚类计算，这里使用的是Morgan分子指纹，也可以用其他分子指纹，详细可参考rdkit分子指纹，另外，molmap模块含有更多种类分子指纹，但需要安装molmap环境
    fps = [AllChem.GetMorganFingerprintAsBitVect(x, 2) for x in mols]
    #print(fps)
    # 上述步骤计算完后，只能得到rdkit格式的一种表达，需要将它转换为二进制的向量，才能使用
    fps_bit = [fps[x].ToBitString() for x in range(len(fps))]
    #print(fps_bit)
    ## 然后得到的是'00010'这样的字符串，需要将其转换为数字
    fps_bit_list = [[int(n) for n in fp1] for fp1 in fps_bit]
    #print(fps_bit_list)
    # 计算fps_bit_list列表中第一个元素的长度（也是二进制向量的位长度）
    bit_length = len(fps_bit_list[0])
    #print(bit_length)
    # 创建一个新的数据框 df2，其中包含转换后的数据（fps_bit_list），每个位对应一个列
    df2 = pd.DataFrame(fps_bit_list,columns=['morgan_' + str(i) for i in range(1, bit_length + 1)])
    # 合并df1和df2
    df = pd.concat([df1,df2],axis = 1)
    # 返回新的合并后df文件
    return df


def pic_tsne(df):
    # 获取含有morgan的列
    df_use_columns = [col for col in df.columns if 'morgan' in col]
    df_use = df[df_use_columns]

    print(df_use)
    # 设置tsne参数
    # TSNE参数说明
    ## n_components，嵌入式空间的维度，即2D图or3D图；random_state 随机种子，不同值会导致不同的局部最小值，随机就好 不关键
    ## perplexity一般在5-50之间，数据集越大，值可以越大，不关键；n_iter迭代次数
    #tsne_model = TSNE(n_components=2, random_state=20, perplexity=30, n_iter=5000)
    tsne_model = TSNE(n_components=2, random_state=20, perplexity=30, n_iter=5000)

    # 拟合tsne 
    tsne_result = tsne_model.fit_transform(df_use)

    # 获取tsne拟合结果，横纵坐标
    df['x'] = tsne_result.T[0]
    df['y'] = tsne_result.T[1]

    # 设置标签映射
    df['label_name'] = df['label'].map({0: 'approved', 1: 'new'})

    # 设置图例
    plt.figure(figsize=(8, 6))
    
    # 设置颜色
    color_map = {'approved': 'Crimson', 'new': 'DeepSkyBlue'}
    unique_labels = df['label_name'].unique()
    #colors = plt.cm.get_cmap('viridis', len(unique_labels))
    for i, label in enumerate(unique_labels):
        subset = df[df['label_name'] == label]
        plt.scatter(subset['x'], subset['y'], label = label, color = color_map[label], s = 10) # 设置大小

    # 绘图，具体散点图的参数可自行检索
    plt.scatter(df.x, df.y, c=[color_map[label] for label in df['label_name']], s = 10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title("TSNE-pesticide",fontdict={'size':20})
    plt.legend()
    plt.savefig('pesticide.png')


# 写主程序将上面的函数串起来
def main(file):
    # 读取文件
    df_csv = pd_read_file(file)

    # 计算分子指纹
    df_finger = cal_fingerprint(df_csv)

    # 绘制tsne图
    pic_tsne(df_finger)


if __name__ == '__main__':
    # 从命令行参数中获取第一个参数
    file = sys.argv[1]
    main(file)