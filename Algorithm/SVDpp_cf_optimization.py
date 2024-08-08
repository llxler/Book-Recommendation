import numpy as np

# 隐式反馈的结合：
# SVD++ 算法的一个核心特点是考虑了用户对其他项目的隐式反馈信息。在代码中，这通过 self.Y 矩阵实现，它存储了项目的隐式反馈（如用户对项目的关注度、浏览次数等）。在预测中，self.Q[item, :] + np.mean(self.Y, axis=0) 部分融合了隐式反馈信息。

# 用户和项目的偏差处理：
# 在传统的矩阵分解中，用户和项目的偏差（即用户的平均评分偏差和项目的平均评分偏差）是独立处理的。在 SVD++ 中，这些偏差与用户和项目的隐性因素结合，以更精确地预测评分。代码中通过 self.b_u[user] 和 self.b_i[item] 处理了用户和项目的偏差。

# 更新规则中的隐式反馈：
# 在 fit 方法中，SVD++ 使用隐式反馈来调整用户和项目的潜在因子。具体地说，在更新 self.P[user, :]、self.Q[item, :] 和 self.Y[item, :] 时，将隐式反馈信息纳入了误差的计算中。这可以从 error * (q_i + np.mean(self.Y, axis=0)) 和 error * p_u 中看到，其中 np.mean(self.Y, axis=0) 代表了隐式反馈的平均效应。

class SVDPlusPlus:
    def __init__(self, num_users, num_items, latent_factors=10, learning_rate=0.01, reg_lambda=0.1, num_epochs=10):
        """
        初始化 SVD++ 模型的参数。
        
        :param num_users: 用户数量
        :param num_items: 项目数量
        :param latent_factors: 潜在因子的数量
        :param learning_rate: 学习率
        :param reg_lambda: 正则化参数
        :param num_epochs: 训练的轮数
        """
        self.num_users = num_users
        self.num_items = num_items
        self.latent_factors = latent_factors
        self.learning_rate = learning_rate
        self.reg_lambda = reg_lambda
        self.num_epochs = num_epochs

        # 初始化用户潜在因子矩阵 P，项目潜在因子矩阵 Q，隐式反馈矩阵 Y，以及用户和项目的偏差
        self.P = np.random.rand(num_users, latent_factors)
        self.Q = np.random.rand(num_items, latent_factors)
        self.Y = np.random.rand(num_items, latent_factors)
        self.b_u = np.zeros(num_users)
        self.b_i = np.zeros(num_items)
        self.b = np.mean(self.b_u)  # 全局偏差

    def fit(self, train_data):
        """
        训练 SVD++ 模型。
        
        :param train_data: 训练数据，格式为 (user, item, rating)
        """
        for epoch in range(self.num_epochs):
            np.random.shuffle(train_data)
            for user, item, rating in train_data:
                prediction = self.predict(user, item)
                error = rating - prediction

                # 更新用户和项目的偏差
                self.b_u[user] += self.learning_rate * (error - self.reg_lambda * self.b_u[user])
                self.b_i[item] += self.learning_rate * (error - self.reg_lambda * self.b_i[item])

                # 更新潜在因子矩阵
                p_u = self.P[user, :]
                q_i = self.Q[item, :]
                y_i = self.Y[item, :]

                # 使用隐式反馈更新用户潜在因子
                self.P[user, :] += self.learning_rate * (error * (q_i + np.mean(self.Y, axis=0)) - self.reg_lambda * p_u)
                # 使用用户潜在因子更新项目潜在因子
                self.Q[item, :] += self.learning_rate * (error * p_u - self.reg_lambda * q_i)
                # 更新隐式反馈矩阵
                self.Y[item, :] += self.learning_rate * (error * p_u - self.reg_lambda * y_i)

            # 计算并打印每轮的损失，以便调试
            loss = self.calculate_loss(train_data)
            print(f'Epoch {epoch + 1}/{self.num_epochs}, Loss: {loss}')

    def predict(self, user, item):
        """
        预测给定用户对给定项目的评分。
        
        :param user: 用户 ID
        :param item: 项目 ID
        :return: 预测评分
        """
        prediction = self.b + self.b_u[user] + self.b_i[item] + np.dot(self.P[user, :], self.Q[item, :] + np.mean(self.Y, axis=0))
        return prediction

    def calculate_loss(self, data):
        """
        计算在给定数据上的总损失。
        
        :param data: 测试数据，格式为 (user, item, rating)
        :return: 总损失
        """
        loss = 0
        for user, item, rating in data:
            prediction = self.predict(user, item)
            loss += (rating - prediction) ** 2
        # 加上正则化项以防止过拟合
        loss += self.reg_lambda * (np.linalg.norm(self.P) ** 2 + np.linalg.norm(self.Q) ** 2 + np.linalg.norm(self.Y) ** 2)
        return loss

# Example usage
if __name__ == "__main__":
    num_users = 100
    num_items = 50
    train_data = [(0, 0, 3.0), (0, 1, 4.0), (1, 0, 2.0), (1, 2, 5.0)]  # 用户、项目、评分
    model = SVDPlusPlus(num_users, num_items)
    model.fit(train_data)