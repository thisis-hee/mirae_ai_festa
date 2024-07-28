import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# 데이터 예시 (고객 ID, 거래 빈도, 총 수익률, 총 거래 금액, 투자 경력)
np.random.seed(0)
data = {
    'customer_id': range(1, 101),  # 100명의 고객
    'daily_trades': np.random.randint(1, 20, 100),  # 1~20회 일일 매매 횟수
    'total_profit_rate': np.random.uniform(-0.3, 0.3, 100),  # -30%~30% 총 수익률
    'total_trade_amount': np.random.uniform(10000, 100000000, 100),  # 총 거래 금액
    'investment_experience': np.random.randint(0, 20, 100)  # 투자 경력 (0~20년)
}

df = pd.DataFrame(data)

X = df[['daily_trades', 'total_profit_rate', 'total_trade_amount', 'investment_experience']]

# 스케일링
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA()
pca_result = pca.fit_transform(X_scaled)

explained_variance_ratio = pca.explained_variance_ratio_

cumulative_explained_variance = np.cumsum(explained_variance_ratio)

# Scree Plot
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, marker='o', label='Individual Explained Variance')
plt.plot(range(1, len(explained_variance_ratio) + 1), cumulative_explained_variance, marker='o', label='Cumulative Explained Variance')
plt.xlabel('Number of Principal Components')
plt.ylabel('Explained Variance Ratio')
plt.title('Scree Plot')
plt.legend()
plt.show()

# 누적 설명 분산 비율이 75% 이상인 지점에서 주성분 수 결정
n_components = np.argmax(cumulative_explained_variance >= 0.75) + 1

print(f"Optimal number of principal components: {n_components}")

# PCA를 주성분 개수로 다시 수행
pca = PCA(n_components=n_components)
pca_result = pca.fit_transform(X_scaled)

# 클러스터 수 결정 elbow method
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X_scaled)
    sse.append(kmeans.inertia_)

# 엘보우 그래프 시각화
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), sse, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('SSE')
plt.title('Elbow Method for Optimal number of clusters')
plt.show()

# 최적의 클러스터 수 선택
optimal_clusters = 3

kmeans = KMeans(n_clusters=optimal_clusters, random_state=0)
clusters = kmeans.fit_predict(X_scaled)
df['cluster'] = clusters


# 주성분 로딩(각 주성분이 원래 변수들에 얼마나 기여하는지)
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

# 로딩을 데이터프레임으로 변환
loading_df = pd.DataFrame(loadings, index=X.columns, columns=['PC1', 'PC2', 'PC3'])

# 결과 출력
print("PCA Loadings:")
print(loading_df)

# 3D PCA 결과와 클러스터링 결과를 함께 시각화
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(pca_result[:, 0], pca_result[:, 1], pca_result[:, 2], c=clusters, cmap='viridis', s=100, alpha=0.7)
ax.set_title('3D PCA Result with K-means Clustering')
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
legend = ax.legend(*scatter.legend_elements(), title='Cluster')
ax.add_artist(legend)
plt.show()

# 주성분 기여도 시각화
fig, ax = plt.subplots(1, 3, figsize=(18, 6))
sns.barplot(y=loading_df.index, x=loading_df['PC1'], ax=ax[0])
ax[0].set_title('Principal Component 1 Loadings')
sns.barplot(y=loading_df.index, x=loading_df['PC2'], ax=ax[1])
ax[1].set_title('Principal Component 2 Loadings')
sns.barplot(y=loading_df.index, x=loading_df['PC3'], ax=ax[2])
ax[2].set_title('Principal Component 3 Loadings')
plt.show()