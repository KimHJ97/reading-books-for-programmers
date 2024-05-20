# 01장. 벡터: 벡터와 벡터의 기본 연산

__선형대수학에서 벡터__ 는 수를 순서대로 나열한 것입니다.  
__벡터의 차원__ 은 벡터가 가진 원소의 수입니다.  
__벡터의 방향__ 은 벡터가 열 방향인지 행 방향인지를 나타냅니다.  

차원은 종종 Rⁿ 처럼 나타내는데, R은 실수, n은 차원을 나타냅니다. R²는 두 개의 원소가 있는 벡터가 됩니다. (R², R₂, R2, R^2 로 사용될 수 있다.)  

 - Numpy로 벡터 만들기
    - asArray 변수는 방향이 없는 배열로 행이나 열벡터가 아니라 NumPy의 숫자 1차원 리스트이다.
    - NumPy의 방향은 대괄호로 지정한다. 가장 바깥쪽 대괄호는 모든 숫자를 하나의 객체로 묶고, 추가적인 내부 괄호 집합은 행을 나타낸다. 행벡터는 하나의 행이 모든 숫자를 가지지만 열벡터는 하나의 숫자를 가진 행이 여러 개가 있다.
```python
asList = [1, 2, 3]
asArray = np.array([1, 2, 3]) # 1차원 배열
rowVec = np.array([ [1, 2, 3] ]) # 행
colVec = np.array([ [1], [2], [3] ]) # 열

print(f'asList: {np.shape(asList)}') # asList: (3,)
print(f'asArray: {np.shape(asArray)}') # asArray: (3,)
print(f'rowVec: {np.shape(rowVec)}') # rowVec: (1, 3)
print(f'colVec: {np.shape(colVec)}') # colVec: (3, 1)
```
