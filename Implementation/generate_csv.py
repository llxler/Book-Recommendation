import pandas as pd
import numpy as np

# 设置随机种子以确保可重复性
np.random.seed(42)

# 配置用户数、图书数和评分数
num_users = 18 # 用户数量
num_books = 31 # 图书馆真实书籍数量
num_ratings = 1000  # 总评分数

# 生成随机用户ID、图书ID和评分数据
user_ids = np.random.randint(1, num_users + 1, size=num_ratings)
book_ids = np.random.randint(1, num_books + 1, size=num_ratings)
ratings = np.random.randint(1, 6, size=num_ratings)

# 转换为DataFrame
data = {
    'user_id': user_ids,
    'book_id': book_ids,
    'rating': ratings
}
df = pd.DataFrame(data)

# 保存为CSV文件
file_path = 'Implementation\\book_ratings.csv'
df.to_csv(file_path, index=False)

print(f"Data saved to {file_path}")