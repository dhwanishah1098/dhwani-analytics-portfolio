"""Generate synthetic supply chain dataset inspired by North Link Melbourne Food Group internship."""
import pandas as pd, numpy as np, os
np.random.seed(7)
n = 1200

suppliers = ['FreshFarm Co','Pacific Produce','VicGreens','Aussie Meats','ColdChain Dairy',
             'BakeryDirect','SeaFresh','DrinksCo','SnackHouse','GrocerPlus']
sup_w = [0.18,0.15,0.12,0.11,0.10,0.09,0.08,0.07,0.06,0.04]
categories = ['Produce','Dairy','Meat','Bakery','Beverages','Frozen','Snacks']
cat_map = {
    'FreshFarm Co':'Produce','Pacific Produce':'Produce','VicGreens':'Produce',
    'Aussie Meats':'Meat','ColdChain Dairy':'Dairy','BakeryDirect':'Bakery',
    'SeaFresh':'Frozen','DrinksCo':'Beverages','SnackHouse':'Snacks','GrocerPlus':'Snacks'
}
warehouses = ['Tullamarine','Dandenong','Laverton']
wh_w = [0.45,0.35,0.20]

records = []
for i in range(n):
    supplier = np.random.choice(suppliers, p=sup_w)
    category = cat_map[supplier]
    warehouse = np.random.choice(warehouses, p=wh_w)
    # Lead time depends on supplier + category
    base_lt = {'Produce':2,'Dairy':1,'Meat':2,'Bakery':1,'Beverages':4,'Frozen':3,'Snacks':5}[category]
    sup_factor = {'FreshFarm Co':1.0,'Pacific Produce':1.3,'VicGreens':0.9,'Aussie Meats':1.1,
                  'ColdChain Dairy':0.8,'BakeryDirect':1.0,'SeaFresh':1.4,'DrinksCo':1.2,
                  'SnackHouse':1.1,'GrocerPlus':1.3}[supplier]
    wh_factor = {'Tullamarine':1.0,'Dandenong':1.15,'Laverton':1.25}[warehouse]
    lead_time = max(1, int(np.random.normal(base_lt * sup_factor * wh_factor, 0.8)))
    on_time = 1 if (lead_time <= base_lt + 1 and np.random.rand() > 0.15) else 0
    # Defect rate
    base_defect = {'Produce':0.08,'Dairy':0.04,'Meat':0.06,'Bakery':0.03,
                   'Beverages':0.02,'Frozen':0.05,'Snacks':0.02}[category]
    defect_qty = np.random.binomial(100, base_defect * sup_factor)
    order_qty = np.random.randint(50, 500)
    unit_cost = {'Produce':3.5,'Dairy':4.2,'Meat':12.0,'Bakery':2.8,
                 'Beverages':1.9,'Frozen':6.5,'Snacks':2.1}[category]
    order_value = round(order_qty * unit_cost * np.random.uniform(0.95,1.05), 2)
    date = pd.Timestamp('2025-06-01') + pd.Timedelta(days=np.random.randint(0, 183))
    records.append({
        'order_id':f'ORD{i:04d}','date':date.date(),'supplier':supplier,
        'category':category,'warehouse':warehouse,
        'order_qty':order_qty,'unit_cost':round(unit_cost,2),'order_value':order_value,
        'lead_time_days':lead_time,'expected_lead_days':base_lt,
        'on_time_delivery':on_time,'defect_qty':defect_qty,
        'defect_rate':round(defect_qty/100,4)
    })

df = pd.DataFrame(records)
os.makedirs(os.path.dirname(__file__), exist_ok=True)
df.to_csv(os.path.join(os.path.dirname(__file__),'supply_chain_data.csv'), index=False)
print(f"Generated {len(df)} supply chain records")
