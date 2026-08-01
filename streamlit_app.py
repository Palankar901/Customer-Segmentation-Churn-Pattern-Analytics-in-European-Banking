from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='European Banking Churn Analytics', page_icon='🏦', layout='wide')
BASE = Path(__file__).parent
DATA = BASE / 'segmented_european_bank.csv' if (BASE / 'segmented_european_bank.csv').exists() else BASE / 'outputs' / 'segmented_european_bank.csv'

@st.cache_data
def load_data():
    d=pd.read_csv(DATA)
    return d

if not DATA.exists():
    st.error('Prepared data is missing. Run generate_deliverables.py first.'); st.stop()
d=load_data()
st.title('🏦 European Banking: Customer Segmentation & Churn')
st.caption('Live exploratory analytics | Churn means Exited = 1 | Source: European_Bank.csv (2025)')

with st.sidebar:
    st.header('Segment filters')
    countries=st.multiselect('Geography', sorted(d.Geography.unique()), default=sorted(d.Geography.unique()))
    ages=st.multiselect('Age group', ['<30','30-45','46-60','60+'], default=['<30','30-45','46-60','60+'])
    genders=st.multiselect('Gender', sorted(d.Gender.unique()), default=sorted(d.Gender.unique()))
    tenures=st.multiselect('Tenure group', ['New (0-2)','Mid-term (3-6)','Long-term (7+)'], default=['New (0-2)','Mid-term (3-6)','Long-term (7+)'])
    active_choice=st.multiselect('Member activity', ['Active','Inactive'], default=['Active','Inactive'])
    balance_range=st.slider('Balance range', float(d.Balance.min()), float(d.Balance.max()), (float(d.Balance.min()),float(d.Balance.max())))

f=d[(d.Geography.isin(countries))&(d.AgeGroup.isin(ages))&(d.Gender.isin(genders))&(d.TenureGroup.isin(tenures))&(d.Balance.between(*balance_range))].copy()
f=f[f.IsActiveMember.map({1:'Active',0:'Inactive'}).isin(active_choice)]
if f.empty: st.warning('No customers match these filters.'); st.stop()
churn=f.Exited.mean(); premium_threshold=d.Balance.quantile(.75); premium=f[f.Balance>=premium_threshold]
c1,c2,c3,c4=st.columns(4)
c1.metric('Customers',f'{len(f):,}')
c2.metric('Churn rate',f'{churn:.1%}',f'{f.Exited.sum():,} exited')
c3.metric('Average balance',f'{f.Balance.mean():,.0f}')
c4.metric('Premium churn rate',f'{premium.Exited.mean():.1%}' if len(premium) else '—',f'Balance ≥ {premium_threshold:,.0f}')

def rate_frame(col, order=None):
    x=f.groupby(col,observed=False).agg(Customers=('Exited','size'),Churned=('Exited','sum'),Churn_Rate=('Exited','mean')).reset_index()
    if order: x[col]=pd.Categorical(x[col],order,ordered=True);x=x.sort_values(col)
    return x

tab1,tab2,tab3,tab4=st.tabs(['Overview','Geography & demographics','Engagement & tenure','High-value explorer'])
with tab1:
    a,b=st.columns(2)
    with a:
        geo=rate_frame('Geography'); st.plotly_chart(px.bar(geo,x='Geography',y='Churn_Rate',text=geo.Churn_Rate.map(lambda x:f'{x:.1%}'),color='Churn_Rate',color_continuous_scale='Blues',title='Churn rate by geography').update_yaxes(tickformat='.0%'),use_container_width=True)
    with b:
        seg=rate_frame('BalanceSegment',['Zero balance','Low balance (>0-100k)','High balance (100k+)']); st.plotly_chart(px.bar(seg,x='BalanceSegment',y='Churn_Rate',text=seg.Churn_Rate.map(lambda x:f'{x:.1%}'),color='Churn_Rate',color_continuous_scale='Reds',title='Churn rate by balance segment').update_yaxes(tickformat='.0%'),use_container_width=True)
    st.dataframe(rate_frame('Geography').style.format({'Churn_Rate':'{:.1%}'}),use_container_width=True,hide_index=True)
with tab2:
    a,b=st.columns(2)
    with a:
        age=rate_frame('AgeGroup',['<30','30-45','46-60','60+']); st.plotly_chart(px.bar(age,x='AgeGroup',y='Churn_Rate',text=age.Churn_Rate.map(lambda x:f'{x:.1%}'),title='Churn rate by age group',color_discrete_sequence=['#2E74B5']).update_yaxes(tickformat='.0%'),use_container_width=True)
    with b:
        heat=pd.pivot_table(f,index='Geography',columns='AgeGroup',values='Exited',aggfunc='mean',observed=False).reindex(columns=['<30','30-45','46-60','60+']); st.plotly_chart(px.imshow(heat,text_auto='.1%',aspect='auto',color_continuous_scale='YlOrRd',title='Geography-age churn interaction'),use_container_width=True)
with tab3:
    a,b=st.columns(2)
    with a:
        ten=rate_frame('TenureGroup',['New (0-2)','Mid-term (3-6)','Long-term (7+)']); st.plotly_chart(px.bar(ten,x='TenureGroup',y='Churn_Rate',title='Churn by tenure group',color='Churn_Rate',color_continuous_scale='Blues').update_yaxes(tickformat='.0%'),use_container_width=True)
    with b:
        act=f.assign(Activity=np.where(f.IsActiveMember.eq(1),'Active','Inactive')); ar=rate_frame('IsActiveMember',[0,1]); ar['Activity']=ar.IsActiveMember.map({0:'Inactive',1:'Active'}); st.plotly_chart(px.bar(ar,x='Activity',y='Churn_Rate',title='Churn by activity',color='Activity',color_discrete_map={'Inactive':'#B42318','Active':'#147D8D'}).update_yaxes(tickformat='.0%'),use_container_width=True)
    pr=rate_frame('NumOfProducts',sorted(f.NumOfProducts.unique())); st.plotly_chart(px.line(pr,x='NumOfProducts',y='Churn_Rate',markers=True,title='Churn by number of products').update_yaxes(tickformat='.0%'),use_container_width=True)
with tab4:
    st.caption(f'Premium balance definition: balance at or above full-dataset 75th percentile ({premium_threshold:,.2f}).')
    hv=f[f.Balance>=premium_threshold]; a,b=st.columns(2); a.metric('Premium customers in selection',f'{len(hv):,}'); b.metric('Premium exits',f'{hv.Exited.sum():,}')
    if len(hv):
        x=hv.groupby('Geography').agg(Customers=('Exited','size'),Churned=('Exited','sum'),Churn_Rate=('Exited','mean'),Avg_Balance=('Balance','mean')).reset_index(); st.plotly_chart(px.bar(x,x='Geography',y='Churn_Rate',text=x.Churn_Rate.map(lambda v:f'{v:.1%}'),color='Churn_Rate',color_continuous_scale='Reds',title='Premium customer churn by geography').update_yaxes(tickformat='.0%'),use_container_width=True); st.dataframe(x.style.format({'Churn_Rate':'{:.1%}','Avg_Balance':'{:,.0f}'}),use_container_width=True,hide_index=True)
st.divider(); st.download_button('Download filtered data (CSV)',f.to_csv(index=False).encode('utf-8'),'filtered_churn_segments.csv','text/csv')
