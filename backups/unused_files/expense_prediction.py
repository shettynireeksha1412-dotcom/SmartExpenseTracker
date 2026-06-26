from sklearn.linear_model import LinearRegression
import numpy as np

# Sample monthly expenses
months = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
expenses = np.array([2000, 2500, 3000, 3500, 4000])

model = LinearRegression()
model.fit(months, expenses)

next_month = np.array([[6]])

prediction = model.predict(next_month)

print("\n===== EXPENSE PREDICTION =====")
print(f"Predicted Expense for Month 6: ₹{prediction[0]:.2f}")