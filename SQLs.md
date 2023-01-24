--- CREDIT GOES TO BRIAN  
[link](https://next.flipsidecrypto.xyz/edit/queries/1f862ca0-6bd8-4d5d-b892-325d965256eb) \n
### TRANSACTIONS SQL
WITH
  swaps AS (
    -- Credit to 0xHaM☰d for the swaps
    SELECT
      block_timestamp,
      logs[0] AS log,
      substring(log, 1, CHARINDEX(' wrap.near for', log)) AS first_part,
      regexp_replace(first_part, '[^0-9]', '') / pow(10, 24) AS near_amount,
      substring(log, CHARINDEX('for', log), 100) AS second_part,
      substring(second_part, 1, CHARINDEX('dac', second_part) -2) AS second_part_amount,
      regexp_replace(second_part_amount, '[^0-9]', '') / pow(10, 6) AS usdt_amount
    FROM
      near.core.fact_receipts
    WHERE
      logs[0] like 'Swapped % wrap.near for % dac17f958d2ee523a2206206994597c13d831ec7.factory.bridge.near'
      and block_timestamp::date >= CURRENT_DATE - INTERVAL '1 MONTH'
  )
SELECT
  DATE,
  NUMBER_TRANSACTIONS
FROM
  (
    SELECT
      *,
      LAG(active_users, 1) OVER (
        ORDER BY
          date
      ) active_users_prev,
      LAG(number_transactions, 1) OVER (
        ORDER BY
          date
      ) number_transactions_prev,
      LAG(txn_fees_usd) OVER (
        ORDER BY
          date
      ) txn_fees_prev
    FROM
      (
        SELECT
          tr.*,
          txn_fees * np.price AS txn_fees_usd
        FROM
          (
            SELECT
              DATE_TRUNC('day', block_timestamp::date) AS date,
              DATE_TRUNC('day', block_timestamp::date - 1) AS date_prev,
              COUNT(DISTINCT TX_SIGNER) AS active_users,
              COUNT(DISTINCT TX_HASH) AS number_transactions,
              SUM(TRANSACTION_FEE / POW(10, 24)) AS txn_fees
            FROM
              near.core.fact_transactions AS tr
            WHERE
              date < CURRENT_DATE
            GROUP BY
              date,
              date_prev
          ) AS tr
          INNER JOIN (
            SELECT
              DATE_TRUNC('day', block_timestamp) AS date,
              avg(usdt_amount) / avg(near_amount) AS price
            FROM
              swaps
            GROUP BY
              date
          ) AS np ON tr.date = np.date
      )
  )
ORDER BY
  date DESC
  
  
  ### GAS USED SQL
  
  select
  trunc(block_timestamp, 'day') as days,
  sum(gas_used / 1e18) as gas_used_peta,
  avg(gas_used / 1e18) as avg_gas_price_peta,
  sum(TRANSACTION_FEE / 1e24) as fees,
  avg(TRANSACTION_FEE / 1e24) as avg_tx_fee,
  'Near' as chain
from
  near.core.fact_transactions x
  join near.core.fact_prices y on trunc(x.block_timestamp, 'hour') = trunc(y.timestamp, 'hour')
where
  x.block_timestamp > getdate () - interval '1 MONTH'
  and symbol = 'wNEAR'
group by
  1
  
  
  ### ACTIVE CONTRACTS SQL
  
  SELECT
	date_trunc('day', call.block_timestamp) as date,
  case when split(split(rc.status_value,':')[0],'{')[1] ilike '%Failure%' then 'Fail execution'
  else 'Successful execution' end as type,
    COUNT(DISTINCT tr.TX_RECEIVER) as smart_contracts,
  sum(smart_contracts) over (partition by type order by date) as cum_smart_contracts
FROM near.core.fact_actions_events_function_call call
INNER JOIN near.core.fact_transactions tr
ON call.TX_HASH = tr.TX_HASH
INNER JOIN near.core.fact_receipts as rc
ON tr.TX_HASH=rc.TX_HASH
	WHERE ACTION_NAME = 'FunctionCall'
    AND METHOD_NAME <> 'new'
  	AND date >=CURRENT_DATE-INTERVAL '1 MONTH'
group by 1,2 order by 1 asc,2 desc

### CONTRACTS SQL

SELECT
  trunc(first_date, 'day') as date,
  count(distinct receiver_id) as new_contracts,
  sum(new_contracts) over (
    order by
      date
  ) as cum_new_contracts
from
  (
    select
      receiver_id,
      min(x.block_timestamp) as first_date
    from
      near.core.fact_actions_events x
      join near.core.fact_receipts y on x.tx_hash = y.tx_hash
    where
      action_name = 'DeployContract'
    group by
      1
  )
where
  first_date >= CURRENT_DATE - INTERVAL '1 MONTH'
group by
  1
order by
  1 asc
  
  
  ### ACTIVE USERS SQL
  
  WITH
  swaps AS (
    -- Credit to 0xHaM☰d for the swaps
    SELECT
      block_timestamp,
      logs[0] AS log,
      substring(log, 1, CHARINDEX(' wrap.near for', log)) AS first_part,
      regexp_replace(first_part, '[^0-9]', '') / pow(10, 24) AS near_amount,
      substring(log, CHARINDEX('for', log), 100) AS second_part,
      substring(second_part, 1, CHARINDEX('dac', second_part) -2) AS second_part_amount,
      regexp_replace(second_part_amount, '[^0-9]', '') / pow(10, 6) AS usdt_amount
    FROM
      near.core.fact_receipts
    WHERE
      logs[0] like 'Swapped % wrap.near for % dac17f958d2ee523a2206206994597c13d831ec7.factory.bridge.near'
      and block_timestamp::date >= CURRENT_DATE - INTERVAL '1 MONTH'
  )
SELECT
  *,
  ROUND(
    (active_users - active_users_prev) / active_users_prev * 100,
    2
  ) AS pct_diff_active,
  ROUND(
    (number_transactions - number_transactions_prev) / number_transactions_prev * 100,
    2
  ) AS pct_diff_transactions,
  ROUND(
    (txn_fees_usd - txn_fees_prev) / txn_fees_prev * 100,
    2
  ) AS pct_diff_txn_fees
FROM
  (
    SELECT
      *,
      LAG(active_users, 1) OVER (
        ORDER BY
          date
      ) active_users_prev,
      LAG(number_transactions, 1) OVER (
        ORDER BY
          date
      ) number_transactions_prev,
      LAG(txn_fees_usd) OVER (
        ORDER BY
          date
      ) txn_fees_prev
    FROM
      (
        SELECT
          tr.*,
          txn_fees * np.price AS txn_fees_usd
        FROM
          (
            SELECT
              DATE_TRUNC('day', block_timestamp::date) AS date,
              DATE_TRUNC('day', block_timestamp::date - 1) AS date_prev,
              COUNT(DISTINCT TX_SIGNER) AS active_users,
              COUNT(DISTINCT TX_HASH) AS number_transactions,
              SUM(TRANSACTION_FEE / POW(10, 24)) AS txn_fees
            FROM
              near.core.fact_transactions AS tr
            WHERE
              date < CURRENT_DATE
            GROUP BY
              date,
              date_prev
          ) AS tr
          INNER JOIN (
            SELECT
              DATE_TRUNC('day', block_timestamp) AS date,
              avg(usdt_amount) / avg(near_amount) AS price
            FROM
              swaps
            GROUP BY
              date
          ) AS np ON tr.date = np.date
      )
  )
ORDER BY
  date DESC
  
  ### NEW USERS SQL
  
  with
  t1 as (
    select distinct
      tx_signer,
      min(block_timestamp) as debut
    from
      near.core.fact_transactions
    where
      tx_status = 'Success'
    group by
      1
  ),
  t2 as (
    SELECT distinct
      tx_signer,
      debut
    from
      t1
    where
      debut >= CURRENT_DATE - INTERVAL '1 MONTH'
  )
select
  trunc(debut, 'day') as date,
  count(distinct tx_signer) as new_user,
  sum(new_user) over (
    order by
      date
  ) as cum_new_users
from
  t2
group by
  1
order by
  1 asc
