# -*- coding: utf-8 -*-
from sklearn.base import TransformerMixin
#from category_encoders.ordinal import OrdinalEncoder
#import numpy as np
import pandas as pd
import copy
from pandas.api.types import is_numeric_dtype,is_string_dtype
from joblib import Parallel,delayed
import numpy as np
from BDMLtools.fun import raw_to_bin_sc,sp_replace

class woeTransformer(TransformerMixin):
    
    """ 
    对数据进行WOE编码
        
    Params:
    ------
        
    varbin:BDMLtools.varReport(...).fit(...).var_report_dict,dict格式,woe编码参照此编码产生       
    special_values,缺失值指代值,
            请特别注意:special_values必须与产生varbin的函数的special_values一致，否则缺失值的woe编码将出现错误结果
            + None,保证数据默认
            + list=[value1,value2,...],数据中所有列的值在[value1,value2,...]中都会被替换，字符被替换为'missing',数值被替换为np.nan
            + dict={col_name1:[value1,value2,...],...},数据中指定列替换，被指定的列的值在[value1,value2,...]中都会被替换，字符被替换为'missing',数值被替换为np.nan
    woe_missing=None,float,缺失值的woe调整值，默认None即不调整.当missing箱样本量极少时，woe值可能不具备代表性，此时可调整varbin中的woe替换值至合理水平，例如设定为0
            经过替换后的varbin=保存在self.varbin中.本模块暂不支持对不同特征的woe调整值做区别处理，所有特征的woe调整值均为woe_missing
    distr_limit=0.01,float,当woe_missing不为None时,若missing箱占比低于distr_limit时才执行替换
    check_na:bool,为True时,若经woe编码后编码数据出现了缺失值，程序将报错终止，可能的错误原因:   
            + 某箱样本量太少，且该列是字符列的可能性极高    
            + test或oot数据相应列的取值超出了train的范围，且该列是字符列的可能性极高  
            + special value设定前后不一致(varbin与本模块的speical value)
    n_jobs,int,并行数量,默认1(所有core),在数据量非常大，列非常多的情况下可提升效率但会增加内存占用，若数据量较少可设定为1
    verbose,int,并行信息输出等级 
            
    Attributes:
    -------   
    """        
    
    def __init__(self,varbin,n_jobs=1,verbose=0,special_values=None,check_na=True,woe_missing=None,distr_limit=0.01):
        
        self.varbin=varbin
        self.n_jobs=n_jobs
        self.verbose=verbose
        self.check_na=check_na
        self.special_values=special_values
        self.woe_missing=woe_missing
        self.distr_limit=distr_limit
        
    def transform(self,X,y):
        """ 
        WOE转换
        """
        X=sp_replace(X,self.special_values)

        self.varbin=copy.deepcopy(self.varbin)
        
        if isinstance(self.woe_missing,(int,float)):        
            
            
            for key in self.varbin:
            
                if 'missing' in self.varbin[key].index.tolist() and self.varbin[key].loc['missing','count_distr']<self.distr_limit:
                    
                    self.varbin[key].loc['missing','woe'] = self.woe_missing

        elif self.woe_missing is None:
            
            pass
        
        else:
            
            raise ValueError("woe_missing in (None,int,float).")
                                         
            
        p=Parallel(n_jobs=self.n_jobs,verbose=self.verbose)
        
        res=p(delayed(self.woe_map)(X[key],self.varbin[key],self.check_na) 
                              for key in self.varbin)
            
        X_woe=pd.concat({col:col_woe for col,col_woe in res},axis=1)
            
        return X_woe  
            
          
    def fit(self,X=None,y=None):
   
        return self      
    
    def woe_map(self,col,bin_df,check_na=True):
    
        if is_numeric_dtype(col):
            
            bin_df_drop= bin_df[~bin_df['breaks'].isin([-np.inf,'missing',np.inf])]
            
            woe_nan= bin_df[bin_df['breaks'].eq("missing")]['woe'][0]
            
            breaks=bin_df_drop['breaks'].astype('float64').tolist()
            
            woe=bin_df[~bin_df['breaks'].eq('missing')]['woe'].tolist()
    
            col_woe=pd.cut(col,[-np.inf]+breaks+[np.inf],labels=woe,right=False,ordered=False).astype('float32')

            col_woe=col_woe.fillna(woe_nan)
            
        elif is_string_dtype(col):
            
            breaks=bin_df.index.tolist();woe=bin_df['woe'].tolist()
            
            raw_to_breaks=raw_to_bin_sc(col.unique().tolist(),breaks)
            
            breaks_to_woe=dict(zip(breaks,woe))
            
            col_woe=col.map(raw_to_breaks).map(breaks_to_woe).astype('float32')            
            
        else:
            
            raise ValueError(col.name+"‘s dtype not in ('number' or 'str')")
            
        if check_na:
            
            if col_woe.isnull().sum()>0:
                
                raise ValueError(col.name+"_woe contains nans,bins in each variables in varbin should include all the possible values among with all the split data")
            
        return col.name,col_woe
    
    
