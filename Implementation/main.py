from surprise import Dataset, Reader, SVDpp, accuracy
from surprise.model_selection import train_test_split, cross_validate

# Define the reader with skip_lines parameter to ignore the header
reader = Reader(line_format='user item rating', sep=',', rating_scale=(1, 5), skip_lines=1)
data = Dataset.load_from_file('Implementation\\book_ratings.csv', reader=reader)

# Split the dataset
trainset, testset = train_test_split(data, test_size=0.25)

# Train the model
algorithms = [
    'AlgoBase',         # 基础算法类，所有算法的基类
    'BaselineOnly',     # 只使用基线预测的算法，基线预测是基于全局平均值、用户偏差和物品偏差的预测
    'CoClustering',     # 共聚类算法，将用户和物品共同聚类
    'KNNBaseline',      # 基于最近邻的协同过滤算法，使用基线估计作为相似性度量
    'KNNBasic',         # 基于最近邻的基础协同过滤算法
    'KNNWithMeans',     # 基于最近邻的协同过滤算法，使用平均值进行归一化
    'KNNWithZScore',    # 基于最近邻的协同过滤算法，使用Z分数进行归一化
    'NMF',              # 非负矩阵分解算法
    'NormalPredictor',  # 正常预测算法，随机预测一个评分
    'Prediction',       # 预测类，包含用户、物品、实际评分和预测评分等信息
    'PredictionImpossible', # 预测不可能类，表示无法进行预测
    'SlopeOne',         # Slope One算法，基于评分差异的简单协同过滤算法
    'SVD',              # 奇异值分解（SVD）算法
    'SVDpp'             # 改进的SVD算法，考虑了隐式反馈
]
algo = SVDpp()
algo.fit(trainset)

# Test the model
predictions = algo.test(testset)

# Calculate and print accuracy metrics
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

print('---------------------------- Test Result ----------------------------')
# Run 5-fold cross-validation and print results.
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
print('---------------------------- Test Result ----------------------------')

def get_top_n_recommendations(algo, user_id, trainset, n=10):
    # Get all item IDs
    all_item_ids = trainset.all_items()

    # Get items already rated by the user
    user_rated_items = [iid for (iid, _) in trainset.ur[trainset.to_inner_uid(user_id)]]

    # Filter out items that have been rated
    unrated_items = [iid for iid in all_item_ids if iid not in user_rated_items]

    # Predict ratings for unrated items
    predictions = [algo.predict(user_id, trainset.to_raw_iid(iid)) for iid in unrated_items]

    # Sort predictions and select top N
    top_n = sorted(predictions, key=lambda x: x.est, reverse=True)[:n]

    return [pred.iid for pred in top_n]

# Example user ID
# user_id = input("Enter User ID: ")
user_id = '1'

# Get recommended books
recommended_items = get_top_n_recommendations(algo, user_id, trainset)
print(f"Recommended books for User {user_id}: {recommended_items}")