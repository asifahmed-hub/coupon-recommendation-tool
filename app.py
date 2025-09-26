import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    data = {
        "CouponID": [1, 2, 3, 4, 5, 6],
        "Brand": ["BrandA", "BrandA", "BrandB", "BrandB", "BrandC", "BrandC"],
        "Type": ["% Off", "Cash Off", "% Off", "BOGO", "Cash Off", "BOGO"],
        "CostPerCoupon": [0.50, 0.75, 0.60, 1.00, 0.65, 0.90],
        "RedemptionRate": [0.15, 0.10, 0.20, 0.25, 0.18, 0.22],
        "RevenuePerRedemption": [5.0, 4.0, 6.0, 7.0, 5.5, 6.5]
    }
    df = pd.DataFrame(data)
    df["ROI"] = (df["RevenuePerRedemption"] * df["RedemptionRate"]) / df["CostPerCoupon"]
    df["EstimatedRevenue"] = df["RedemptionRate"] * df["RevenuePerRedemption"]
    return df

df = load_data()

st.sidebar.title("Coupon Recommendation Tool")

budget = st.sidebar.number_input("Enter your budget ($)", min_value=1.0, value=5.0, step=0.5)
brands = st.sidebar.multiselect("Select Brands", options=df["Brand"].unique(), default=df["Brand"].unique())
types = st.sidebar.multiselect("Select Coupon Types", options=df["Type"].unique(), default=df["Type"].unique())

filtered_df = df[(df["Brand"].isin(brands)) & (df["Type"].isin(types))]
filtered_df = filtered_df.sort_values(by="ROI", ascending=False).reset_index(drop=True)

recommended_coupons = []
total_cost = 0.0

for _, row in filtered_df.iterrows():
    if total_cost + row["CostPerCoupon"] <= budget:
        recommended_coupons.append(row)
        total_cost += row["CostPerCoupon"]

recommended_df = pd.DataFrame(recommended_coupons)

st.title("Recommended Coupons")
st.write(f"Total Budget: ${budget:.2f}")
st.write(f"Used Budget: ${total_cost:.2f}")

if not recommended_df.empty:
    st.dataframe(recommended_df[[
        "CouponID", "Brand", "Type", "CostPerCoupon", "RedemptionRate",
        "RevenuePerRedemption", "ROI", "EstimatedRevenue"
    ]])
else:
    st.warning("No coupons found matching your filters within the budget.")
