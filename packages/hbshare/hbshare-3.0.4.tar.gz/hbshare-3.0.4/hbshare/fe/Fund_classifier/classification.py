import datetime
import pandas as pd
from ..XZ import db_engine
from hbshare.fe.nav_attr import nav_attribution
from ..Machine_learning import classifier
import joblib



class Classifier:

    def __init__(self):

        self.localengine=db_engine.PrvFunDB().engine
        self.hbdb=db_engine.HBDB()
        self.theme_map={'大金融' : ['银行','券商','房地产','保险',],
                   '消费' : ['家用电器','酒类','制药','医疗保健','生物科技','商业服务','零售','纺织服装','食品','农业','家居用品','餐饮旅游','软饮料'],
                   'TMT' : ['半导体','电子元器件','精细化工','电脑硬件','软件','互联网','文化传媒'],
                   '周期': ['化工原料','基本金属','贵金属','钢铁','化纤','建筑','煤炭','化肥农药','石油天然气','日用化工','建材','石油化工'],
                   '制造' : ['工业机械','电工电网','电力','发电设备','汽车零部件','航天军工','能源设备','航空','环保','汽车','通信设备','海运','工程机械'],
                   }

    def wind_theme_data2localdb(self):

        fund_theme=pd.read_csv(r"E:\基金分类\wind主题分类.csv",encoding='gbk')
        fund_theme['证券代码'] = [x.split('.')[0] for x in fund_theme['证券代码']]
        fund_theme['所属主题基金类别(Wind行业)'] = [x.split('行业')[0] for x in fund_theme['所属主题基金类别(Wind行业)']]
        fund_theme['record_date']=str(datetime.datetime.today().date())
        fund_theme.to_sql('mutual_fund_theme',con=self.localengine,index=False,if_exists='append')

    def wind_risk_data2localdb(self):

        fund_theme=pd.read_csv(r"E:\基金分类\windrisk.csv",encoding='gbk')
        fund_theme['证券代码'] = [x.split('.')[0] for x in fund_theme['证券代码']]
        fund_theme['基金风险等级'] = [x.split('-')[0] for x in fund_theme['基金风险等级']]
        fund_theme['record_date']=str(datetime.datetime.today().date())
        fund_theme.to_sql('wind_fund_risk_level',con=self.localengine,index=False,if_exists='append')

    def lable_trans(self,inputdf):

        fg_dict={
                '1':'成长',
                '2': '均衡',
                '3': '价值'
        }
        sz_dict={
            '1': '小盘',
            '2': '中盘',
            '3': '大盘'
        }
        for key in fg_dict.keys():
            inputdf.loc[inputdf['wdfgsx']==key,'wdfgsx']=fg_dict[key]
        for key in sz_dict.keys():
            inputdf.loc[inputdf['wdszsx']==key,'wdszsx']=sz_dict[key]

        return  inputdf

    def get_fund_basicinfo(self):

        sql="""
        select jjdm,wdfgsx,wdszsx,clrq,zzrq from st_fund.t_st_gm_jjxx 
        where wdfgsx is not null and  wdszsx is not null and cpfl='2'
        """
        fund_df=self.hbdb.db2df(sql=sql,db='funduser')

        sql= "select distinct(jjdm) from funddb.jjxx1"
        left_df=self.hbdb.db2df(sql=sql,db='readonly')
        fund_df=pd.merge(left_df,fund_df,how='inner',left_on='JJDM',right_on='jjdm').drop(['JJDM','ROW_ID'],axis=1)

        today=str(datetime.datetime.today().date())
        today=''.join(today.split('-'))

        return fund_df.fillna(today)

    def save_exp_df2db(self):
        funddf = self.get_fund_basicinfo()
        fg_exp_df = pd.DataFrame()

        record=[]

        for i in range(len(funddf)):
            jjdm = funddf.iloc[i]['jjdm']
            start_date = str(funddf.iloc[i]['clrq'])
            end_date = str(funddf.iloc[i]['zzrq'])
            sql="select jzrq from st_fund.t_st_gm_jjjz where jjdm='{0}' and jzrq>='{1}' and jzrq<={2}"\
                .format(jjdm,str(int(end_date[0:4])-1)+"0101",end_date)
            jzrq=self.hbdb.db2df(sql=sql, db='funduser')['jzrq'].values
            gap=pd.Series(jzrq[1:]-jzrq[0:-1]).mode()[0]
            if(gap==1):
                fre='day'
            elif(gap==7):
                fre='week'
            try:
                nav_attr = nav_attribution.StyleAttribution(fund_id=jjdm, fund_type='mutual', start_date=start_date,
                                                            end_date=end_date, factor_type='style_allo',
                                                            benchmark_id='000300',
                                                            nav_frequency=fre).get_all(processed=False)['attribution_df']
            except Exception:
                record.append(i)
                continue


            fg_exp_df = pd.concat([fg_exp_df, nav_attr['factor_exposure'].to_frame().T], axis=0)
            print('the {1}th data {0} done..'.format(jjdm,str(i)))


        fg_exp_df.columns=nav_attr['style_factor']
        fg_exp_df['jjdm']=funddf['jjdm']
        fg_exp_df['wdfgsx']=funddf['wdfgsx']
        fg_exp_df['wdszsx'] = funddf['wdszsx']
        today=str(datetime.datetime.today().date())
        today=''.join(today.split('-'))
        fg_exp_df['end_date']=today
        fg_exp_df.to_sql('style_exp', con=self.localengine)
        record_df=pd.DataFrame(data=record,columns=['wrong_i'])
        record_df.to_csv('record_i.csv')


        print('data saved in table style_exp')

    def read_style_lable_fromhbdb(self):

        sql="""
        select jjdm,wdfgsx,wdszsx from st_fund.t_st_gm_jjxx 
        where wdfgsx is not null and  wdszsx is not null and cpfl='2'
        """
        fund_df=self.hbdb.db2df(sql=sql,db='funduser')

        return fund_df

    def read_exp_fromhbdb(self,asofdate,attr_type,fund_type):

        if(fund_type.lower()=='mutual'):

            sql="""
            select jjdm,style_factor,data_value from st_fund.r_st_nav_attr_df where attr_type='{1}' 
            and tjrq='{0}' and data_type='exposure'
            """.format(asofdate,attr_type)
            exp_df=self.hbdb.db2df(sql=sql,db='funduser')


        elif(fund_type.lower()=='priviate'):

            sql="select jjdm from st_hedge.t_st_jjxx where clbz in ('1','2','3','4') and jjfl='1'"
            prv_list=self.hbdb.db2df(sql=sql,db='highuser')['jjdm'].tolist()
            list_con="'"+"','".join(prv_list)+"'"

            sql="""
            select jjdm,style_factor,data_value from st_hedge.r_st_nav_attr_df where attr_type='{1}' 
            and tjrq='{0}' and data_type='exposure' and jjdm in ({2})
            """.format(asofdate,attr_type,list_con)
            exp_df=self.hbdb.db2df(sql=sql,db='highuser')

        else:
            raise Exception
            print("the input fund type could either be mutual or priviate")

        exp_df.sort_values(by='jjdm', inplace=True)
        exp_df.reset_index(drop=True, inplace=True)

        return exp_df

    def read_vol_fromhbdb(self,asofdate,fund_type):

        term_list=['2101','2103','2106','2201','2999']
        term_con="'"+"','".join(term_list)+"'"

        if(fund_type=='mutual'):
            sql="select jjdm,zblb,zbnp from st_fund.t_st_gm_zqjbdl where tjrq={0} and zblb in ({1}) "\
                .format(asofdate,term_con)
            fund_vol=self.hbdb.db2df(sql,db='funduser')

        elif(fund_type=='priviate'):

            sql="select jjdm from st_hedge.t_st_jjxx where clbz in ('1','2','3','4') and jjfl='1'"
            prv_list=self.hbdb.db2df(sql=sql,db='highuser')['jjdm'].tolist()
            list_con="'"+"','".join(prv_list)+"'"

            sql="select jjdm,zblb,zbnp from st_hedge.t_st_sm_zqjbdl where tjrq='{0}' and zblb in ({1}) and jjdm in ({2}) "\
                .format(asofdate,term_con,list_con)
            fund_vol=self.hbdb.db2df(sql,db='highuser')

        else:
            raise Exception
            print("the input fund type could either be mutual or priviate")

        fund_vol.sort_values(by='jjdm', inplace=True)
        fund_vol.reset_index(drop=True, inplace=True)

        return fund_vol

    def read_theme_lable_fromloacldb(self):

        sql="select * from mutual_fund_theme"
        fund_theme=pd.read_sql(sql,con=self.localengine)

        return fund_theme[['证券代码','所属主题基金类别(Wind行业)']]

    def read_risk_level_fromloacldb(self,asofdate):

        sql="select * from wind_fund_risk_level where record_date='{}'".format(asofdate)
        fund_theme=pd.read_sql(sql,con=self.localengine)

        return fund_theme[['证券代码','基金风险等级']]

    def model_selection(self,inputdf,features_col,label_col,dir):

        max_f1_score=0
        for modelname in ['xgboost','randomforest','svm']:
            model,f1_score=classifier.model_built_up(inputdf,label_col,modelname,features_col,0.2)
            if(f1_score>max_f1_score):
                max_f1_score=f1_score
                best_model=modelname

        print('The winning model is {0}'.format(best_model))
        model, f1_score = classifier.model_built_up(inputdf, label_col, best_model, features_col, 0)

        joblib.dump(model, dir)
        print("the best fited model is saved at E:\GitFolder\hbshare\fe\Fund_classifier ")

    def model_generation_style(self):

        print('Training the style label model...')

        #read the fund data with style lable
        fund_style=self.read_style_lable_fromhbdb()

        #read the style exposure of mutual fund from the hb data base
        style_exp=self.read_exp_fromhbdb('20201231','style_allo','mutual')

        inputdf=pd.DataFrame()
        inputdf['jjdm']=style_exp['jjdm'].unique()
        #reshape the exposure dataframe
        for style in ['小盘价值','小盘成长','中盘成长','中盘价值','大盘价值','大盘成长']:
            inputdf[style]=style_exp[style_exp['style_factor']==style]['data_value'].values

        #join the two df
        inputdf=pd.merge(fund_style,inputdf,how='inner',left_on='jjdm',right_on='jjdm')
        del fund_style,style_exp

        #transfrom the style name from int to strings
        inputdf=self.lable_trans(inputdf)
        inputdf['Label']=inputdf['wdszsx']+inputdf['wdfgsx']
        inputdf.drop(['wdfgsx','wdszsx','jjdm'],axis=1,inplace=True)

        features_col=inputdf.columns.tolist()
        features_col.remove('Label')

        dir=r"E:\GitFolder\hbshare\fe\Fund_classifier\model_style_{0}.pkl".format(str(datetime.datetime.today().date()))
        self.model_selection(inputdf=inputdf, features_col=features_col, label_col='Label', dir=dir)

    def model_generation_theme(self):

        print('Training the theme label model...')

        #read the fund data with theme lable
        fund_theme=self.read_theme_lable_fromloacldb()

        #read the style exposure of mutual fund from the hb data base
        theme_exp=self.read_exp_fromhbdb('20201231','sector','mutual')

        for key in self.theme_map.keys():
            map_list=self.theme_map[key]
            for industry in map_list:
                fund_theme.loc[fund_theme['所属主题基金类别(Wind行业)']==industry,'所属主题基金类别(Wind行业)']=key

        inputdf=pd.DataFrame()
        inputdf['jjdm']=theme_exp['jjdm'].unique()

        #reshape the exposure dataframe
        for style in self.theme_map.keys():
            inputdf[style]=theme_exp[theme_exp['style_factor']==style]['data_value'].values

        #join the two df
        inputdf=pd.merge(fund_theme,inputdf,how='inner',left_on='证券代码',right_on='jjdm').drop(['证券代码','jjdm'],axis=1)
        del fund_theme,theme_exp

        inputdf.rename(columns={'所属主题基金类别(Wind行业)':'Label'},inplace=True)

        features_col=inputdf.columns.tolist()
        features_col.remove('Label')

        dir=r"E:\GitFolder\hbshare\fe\Fund_classifier\model_theme_{0}.pkl".format(str(datetime.datetime.today().date()))

        self.model_selection(inputdf=inputdf, features_col=features_col, label_col='Label', dir=dir)

    def model_generation_risk_level(self):

        print('Training the risk label model...')

        # read the vol data of mutual fund from the hb data base
        fund_vol=self.read_vol_fromhbdb(asofdate='20211220',fund_type='mutual')

        # read the fund data with theme lable from local db
        fund_risk=self.read_risk_level_fromloacldb(asofdate='2021-12-29')

        inputdf=pd.DataFrame()
        inputdf['jjdm']=fund_vol['jjdm'].unique()

        #reshape the exposure dataframe
        for risk in ['2101','2103','2106','2201','2999']:
            inputdf[risk]=fund_vol[fund_vol['zblb']==risk]['zbnp'].values

        #join the two df
        inputdf=pd.merge(fund_risk,inputdf,how='inner',left_on='证券代码',right_on='jjdm').drop(['证券代码','jjdm'],axis=1)
        del fund_risk,fund_vol
        inputdf.rename(columns={'基金风险等级':'Label'},inplace=True)

        #deal with the outliers by assuming that the vol for certain term equals to its vol since established
        for col in ['2101','2103','2106','2201']:
            inputdf.loc[inputdf[col]==99999,col]=inputdf[inputdf[col]==99999]['2999']

        features_col=inputdf.columns.tolist()
        features_col.remove('Label')

        dir=r"E:\GitFolder\hbshare\fe\Fund_classifier\model_risk_{0}.pkl".format(str(datetime.datetime.today().date()))

        self.model_selection(inputdf=inputdf,features_col=features_col,label_col='Label',dir=dir)

    def label_style(self,asofdate,filename):

        #load the trained style lable model
        dir=r"E:\GitFolder\hbshare\fe\Fund_classifier\{}".format(filename)
        trained_model= joblib.load(dir)

        #read the style exposure of target priviate fund from the hb data base
        style_exp=self.read_exp_fromhbdb(asofdate,'style_allo','priviate')

        inputdf=pd.DataFrame()
        inputdf['jjdm']=style_exp['jjdm'].unique()
        #reshape the exposure dataframe
        for style in ['小盘价值','小盘成长','中盘成长','中盘价值','大盘价值','大盘成长']:
            inputdf[style]=style_exp[style_exp['style_factor']==style]['data_value'].values
        del style_exp

        #make the prediction of the lables
        label=trained_model.predict(inputdf[['小盘价值','小盘成长','中盘成长','中盘价值','大盘价值','大盘成长']])
        inputdf['style']=label
        print('style label marked')
        return inputdf[['jjdm','style']]

    def label_theme(self,asofdate,filename):

        # load the trained style lable model
        dir = r"E:\GitFolder\hbshare\fe\Fund_classifier\{}".format(filename)
        trained_model = joblib.load(dir)

        # read the style exposure of target priviate fund from the hb data base
        theme_exp = self.read_exp_fromhbdb(asofdate, 'sector', 'priviate')

        inputdf = pd.DataFrame()
        inputdf['jjdm'] = theme_exp['jjdm'].unique()

        # reshape the exposure dataframe
        for style in self.theme_map.keys():
            inputdf[style] = theme_exp[theme_exp['style_factor'] == style]['data_value'].values

        # make the prediction of the lables
        label = trained_model.predict(inputdf[self.theme_map.keys()])
        inputdf['theme'] = label
        print('theme label marked')
        return inputdf[['jjdm','theme']]

    def label_risk(self, asofdate, filename):

        # load the trained style lable model
        dir = r"E:\GitFolder\hbshare\fe\Fund_classifier\{}".format(filename)
        trained_model = joblib.load(dir)

        # read the vol data of priviate fund from the hb data base
        fund_vol=self.read_vol_fromhbdb(asofdate=asofdate,fund_type='priviate')

        inputdf = pd.DataFrame()
        inputdf['jjdm'] = fund_vol['jjdm'].unique()

        #reshape the vol dataframe
        for risk in ['2101','2103','2106','2201','2999']:
            inputdf[risk]=fund_vol[fund_vol['zblb']==risk]['zbnp'].values

        #deal with the outliers by assuming that the vol for certain term equals to its vol since established
        for col in ['2101','2103','2106','2201']:
            inputdf.loc[inputdf[col]==99999,col]=inputdf[inputdf[col]==99999]['2999']

        # make the prediction of the lables
        label = trained_model.predict(inputdf[['2101','2103','2106','2201','2999']])
        inputdf['risk_level'] = label
        print('risk label marked')
        return inputdf[['jjdm','risk_level']]

    def classify(self):

        style_label=self.label_style(asofdate='20210930',filename='model_style_2021-12-29.pkl')
        theme_label=self.label_theme(asofdate='20210930',filename='model_theme_2021-12-29.pkl')
        risk_label=self.label_risk(asofdate='20211220', filename='model_risk_2021-12-29.pkl')

        final_df=pd.merge(style_label,theme_label,how='inner',left_on='jjdm',right_on='jjdm')
        final_df=pd.merge(final_df,risk_label,how='inner',left_on='jjdm',right_on='jjdm')
        today=str(datetime.datetime.today().date())
        final_df['saved_date']=today

        #check if the same data exists already, if yes, updates them with latest data
        sql="select distinct (saved_date) from prv_fund_lable"
        date_list=pd.read_sql(sql,con=self.localengine)['saved_date'].tolist()
        if(today in date_list):
            sql="delete from prv_fund_lable where saved_date='{}'".format(today)

        final_df.to_sql('prv_fund_lable',con=self.localengine,index=False,if_exists='append')

        print('')


