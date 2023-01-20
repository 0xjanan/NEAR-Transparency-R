import plotly.express as px
import streamlit as st
import pandas as pd
import requests




st.set_page_config(layout='wide', initial_sidebar_state='expanded')

new_user = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/e184d138-7cc6-4fee-8c03-af478a6855df/data/latest")
new_user_lm = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/4b012e94-bda4-4cbe-a612-5275bafbfbfe/data/latest")

active_lm = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/5c7ecdb8-a9b6-4eb6-886b-c84a9a51ad6a/data/latest")
active_lw = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/3eba0bc2-d6bf-4671-818d-4ffe6f4bf9e4/data/latest")

cont_lm = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/e4c0eb12-2c75-4d0b-9efc-94901be1903d/data/latest")
cont_lw = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/6cf40956-287f-4fa2-b9d4-b82620956c5f/data/latest")

act_cont_lw = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/3675340b-8710-42da-becc-022ed9bf65ef/data/latest")
act_cont_lm = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/cdf1e67e-f43c-43a9-af58-894a0136acde/data/latest")

gas_usd_lm = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/41c1368c-fd12-490a-840b-2eefa48739f8/data/latest")
gas_usd_lw = pd.read_json("https://api.flipsidecrypto.com/api/v2/queries/c366b50f-6be8-472f-9de4-79aab2ed0664/data/latest")

avg_gas_lm = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/452ec00c-0e2b-4139-ba19-079f59028b50/data/latest")
avg_gas_lw = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/fa7de3ed-eef3-4871-a68e-4b7d9ce03be1/data/latest")

txs_lw = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/add98081-9147-433f-82be-1cf669e85ce8/data/latest")
txs_lm = pd.read_json("https://node-api.flipsidecrypto.com/api/v2/queries/eb06b0a8-f8cc-4d84-92ad-4ab199850019/data/latest")

near_ = requests.get("https://api.coingecko.com/api/v3/coins/near").json()

near_price = near_['market_data']['current_price']['usd']
near_cirs = near_['market_data']['circulating_supply']
near_mrkcp = near_['market_data']['market_cap']['usd']


st.sidebar.header('Parameter')
st.sidebar.subheader('In this sidebar you can select the timeframe of analysis.')
timeframe = st.sidebar.selectbox('Timeframe by', ('last 7 days', 'last month')) 
st.sidebar.markdown('''
Keep in mind you can collapse this sidebar, to see wider version of charts.
''')


st.sidebar.markdown('''
---
Created with ❤️ by [Janan](https://twitter.com/0x_janan/) \n [Github](https://github.com/0xjanan/)

Powered by [Flipside](https://flipsidecrypto.xyz) & [MetricsDAO](https://metricsdao.xyz) \n


SQL credit goes to this [Dashboard](https://app.flipsidecrypto.com/dashboard/near-transparency-report-12-15-fxcrlG) Brian 👌 \n

''')




st.title('Near Transparency Report')

u1, u2, u3 = st.columns(3)
u1.metric("NEAR Price (USD)",near_price)
u2.metric("NEAR Marketcap (USD)",near_mrkcp)
u3.metric("NEAR Circulation",round(near_cirs,2))

st.markdown('''

## Introduction
---
The NEAR Protocol is a public blockchain that uses proof-of-stake and has smart contract capability. 
It serves as a community-managed cloud computing platform for building decentralized applications.
The NEAR Foundation releases data on a weekly basis to provide transparency on the health of the ecosystem as part of their Transparency Report.
One of the key factors to consider when evaluating these types of L1 blockchains is their performance, including factors such as speed and successful transactions.
One aspect of performance measurement is the number of new and active addresses on the network.

---
### New Users and Cumulation
---
New addresses in the NEAR blockchain refer to the number of new wallets or accounts that are created on the network.

''') 





c1, c2 = st.columns((5,5))
with c1:
    fig = px.bar(
        (new_user, new_user_lm) [timeframe == 'last month'],
        x='DATE',
        y='NEW_USER',
        title='New Users'
        )
    st.plotly_chart(
        fig,
        use_container_width=True)
with c2:
    fig = px.area(
        (new_user,new_user_lm) [timeframe == 'last month'],
        x='DATE',
        y='CUM_NEW_USERS',
        title='Cumulation of New Users'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )

#Row 3
st.markdown('''
### Active Users
---
Active addresses in the NEAR blockchain refer to the number of wallets or accounts that have been active on the network, 
typically measured by the number of transactions that have been made from that address.
 This metric can provide insight into the level of usage and engagement on the NEAR blockchain, 
 and can be used to assess the overall health and growth of the network.


''')


fig = px.area(
    (active_lw,active_lm)[timeframe == 'last month'],
    x='DATE',
    y='ACTIVE_USERS',
    markers=True,
    title='Active Users'
)
st.plotly_chart(
    fig,
    use_container_width=True,
    )

st.markdown('''
### New Contracts on NEAR
---
New contracts on the NEAR blockchain refer to the number of new smart contracts that are deployed on the network.
 A smart contract is a self-executing digital contract with the terms of the agreement directly written into code.
  They are deployed on the blockchain, meaning that they are stored on the network and can be executed automatically when certain conditions are met.
  New contracts on the NEAR blockchain can indicate the level of developer activity and the growth of decentralized applications (dapps) being built on the network.

''')


h1, h2 = st.columns((5,5))
with h1: 
    fig = px.line(
        (cont_lw,cont_lm)[timeframe == 'last month'],
        x='DATE',
        y='NEW_CONTRACTS',
        markers=True,
        title='New Contracts'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )
with h2:
    fig = px.line(
        (cont_lw,cont_lm)[timeframe == 'last month'],
        x='DATE',
        y='CUM_NEW_CONTRACTS',
        markers=True,
        title='Cumulation of New Contracts'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.markdown('''
### Active Contracts on NEAR
---
Active contracts on the NEAR blockchain refer to the number of smart contracts that have been executed or used on the network. 
This metric can provide insight into the level of usage and engagement of smart contracts on the NEAR blockchain,
 and can be used to assess the overall health and growth of the decentralized applications (dapps) being built on the network. 
 It's the number of smart contracts that have been recently interacted with, showing their usage and relevance.




''')


#Active Contracts Data
j1, j2 = st.columns((5,5))
with j1:
    fig = px.area(
        (act_cont_lw,act_cont_lm)[timeframe == 'last month'],
        x='DATE',
        y='SMART_CONTRACTS',
        title='Active Contracts',
        color='TYPE',
        markers=True
    )
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))
    st.plotly_chart(
        fig,
        use_container_width=True
    )
with j2:
    fig = px.area(
        (act_cont_lw,act_cont_lm)[timeframe == 'last month'],
        x='DATE',
        y='CUM_SMART_CONTRACTS',
        title='Cumulation of Active Contracts',
        color='TYPE',
        markers=True
    )
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))
    st.plotly_chart(
        fig,
        use_container_width=True
    )


#Gas
st.markdown('''
### Gas Usage and Average of Gas Usage
---
The NEAR blockchain utilizes a transaction fee system to secure and process transactions on the network. 
These fees are paid by users to the validators (the nodes that process and validate transactions) 
for the resources and computational power required to process and include the transaction in a block. 
The fees are typically measured in the native cryptocurrency of the blockchain, in the case of NEAR it is NEAR token. 
The fees can vary depending on the complexity and size of the transaction, and can also change over time based on network conditions such as congestion.
 The fees are used as an incentive for validators to process transactions, and also to limit spam and malicious activity on the network.

''')


j1, j2 = st.columns((5,5))
with j1:
    fig = px.bar(
        (gas_usd_lw,gas_usd_lm)[timeframe == 'last month'],
        x='DAYS',
        y='GAS_USED_PETA',
        title='Gas Used in PetaNear'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )
with j2:
    fig = px.bar(
        (gas_usd_lw,gas_usd_lm)[timeframe == 'last month'],
        x='DAYS',
        y='AVG_GAS_PRICE_PETA',
        title='Average of Gas Used'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.markdown('''
### Fees and Average Transactions Fees
---

''')
f1, f2 = st.columns((5,5))
with f1:
    fig1 = px.area(
        (gas_usd_lw,gas_usd_lm)[timeframe == 'last month'],
        x='DAYS',
        y='FEES',
        title='NEAR Fees'
    )
    st.plotly_chart(
        fig1,
        use_container_width=True
    )
with f2:
    fig = px.area(
        (gas_usd_lw,gas_usd_lm)[timeframe == 'last month'],
        x='DAYS',
        y='AVG_TX_FEE',
        title='NEAR Average TX Fee'
    )
    st.plotly_chart(
        fig,
        use_container_width=True
    )



#TXs
st.markdown('''
### Transactions
---
A useful metric to assess the health of a network is the number of transactions being conducted by users.
 The next metric we will analyze is the daily number of transactions.


''')
fig = px.line(
    (txs_lw,txs_lm)[timeframe == 'last month'],
    x='DATE',
    y='NUMBER_TRANSACTIONS',
    markers=True,
    title='Transactions'
)
st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown('''
### Findings
In conclusion, the NEAR Transparency report shows that the network has seen significant growth in recent weeks and month. 
The number of active addresses on the network has spiked, indicating a high level of usage and engagement. 
Additionally, the number of new contracts, transactions, and new addresses have all increased,
 indicating a growing developer activity and a rise in decentralized applications being built on the network. Overall, 
 these metrics suggest that the NEAR blockchain is healthy and growing, with a strong and active community using and contributing to the network.

''')
