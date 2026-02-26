import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Ganacsi Dashboard Premium - Interactive")

# User type
user_type = st.selectbox("Dooro type isticmaalaha:", ["Free", "Premium"])

# Number of products
if user_type == "Premium":
    num_products = st.number_input("Tirada Alaabooyinka (Premium Unlimited):", min_value=1, max_value=50, value=3)
else:
    num_products = st.number_input("Tirada Alaabooyinka (Free max 3):", min_value=1, max_value=3, value=1)

# Input product details
product_names, buys, sells, qtys = [], [], [], []

st.subheader("Geli Alaabooyinka")
for i in range(num_products):
    st.markdown(f"**Alaabta {i+1}**")
    name = st.text_input(f"Name {i+1}", value=f"Alaabta {i+1}")
    buy = st.number_input(f"Iibsiga {i+1}", min_value=1.0, max_value=1000.0, value=10.0)
    sell = st.number_input(f"Iibka {i+1}", min_value=1.0, max_value=5000.0, value=15.0)
    qty = st.number_input(f"Tirada {i+1}", min_value=1, max_value=10000, value=100)
    product_names.append(name)
    buys.append(buy)
    sells.append(sell)
    qtys.append(qty)

# Calculate profit
data = []
total_profit = 0
for i in range(num_products):
    profit = (sells[i] - buys[i]) * qtys[i]
    total_profit += profit
    data.append({
        'Alaabta': product_names[i],
        'Qiimaha Iibsiga': buys[i],
        'Qiimaha Iibka': sells[i],
        'Tirada': qtys[i],
        'Faa’iido': profit
    })

df = pd.DataFrame(data)
st.subheader("Faa’iidada Alaabooyinka")
st.dataframe(df)
st.write(f"**Faa’iidada Guud:** ${total_profit:.2f}")

# Advisory tips
if total_profit < 500:
    st.warning("Talo: Faa’iido yar, fiiri kordhinta qiimaha iibka ama dhimista kharashka iibsiga.")
elif total_profit < 2000:
    st.info("Talo: Ganacsi wanaagsan! Waxaa laga yaabaa inaad kordhiso tirada iibka.")
else:
    st.success("Talo: Ganacsi aad u fiican! Ka fikir ballaarinta suuqyada ama alaab cusub.")

# Scenario / What-if (Premium only)
if user_type == "Premium":
    st.subheader("Scenario / What-if Simulation")
    col1, col2 = st.columns(2)
    new_sell = col1.number_input("New Selling Price (Scenario)", value=max(sells))
    new_qty = col2.number_input("New Quantity (Scenario)", value=max(qtys))
    scenario_profit = sum([(new_sell - buys[i]) * new_qty for i in range(num_products)])
    st.write(f"**Faa’iidada Scenario:** ${scenario_profit:.2f}")

# Plot chart
st.subheader("Faa’iidada Alaabooyinka (Chart)")
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(df['Alaabta'], df['Faa’iido'], color=plt.cm.tab20.colors)
ax.set_ylabel("USD")
ax.set_title("Faa’iidada Alaabooyinka")
st.pyplot(fig)

# CSV Download
csv = df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='faaido_ganacsi.csv',
    mime='text/csv'
)