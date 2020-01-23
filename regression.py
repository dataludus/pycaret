def setup(data, 
          target, 
          train_size=0.7,
          sampling=True,
          sample_estimator = None,
          categorical_features = None,
          categorical_imputation = 'constant',
          numeric_features = None,
          numeric_imputation = 'mean',
          date_features = None,
          drop_features = None,
          normalize = False,
          normalize_method = 'zscore',
          transformation = False,
          transformation_method = 'yeo-johnson',
          session_id = None,
          profile = False):
    
    """
        
    Description:
    ------------    
    This function initializes the environment in pycaret and creates the transformation
    pipeline to prepare the data for modeling and deployment. setup() must called before
    executing any other function in pycaret. It takes two mandatory parameters:
    dataframe {array-like, sparse matrix} and name of the target column. 
    
    All other parameters are optional.

        Example
        -------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        
        experiment_name = setup(data = boston,  target = 'medv')

        'boston' is a pandas DataFrame and 'medv' is the continuous target column in
         the dataframe.

    Parameters
    ----------
    data : {array-like, sparse matrix}, shape (n_samples, n_features) where n_samples 
    is the number of samples and n_features is the number of features.

    target: string
    Name of target column to be passed in as string. 
    
    train_size: float, default = 0.7
    Size of the training set. By default, 70% of the data will be used for training 
    and validation. Remaining data will be used for test / hold-out set.

    sampling: bool, default = True
    When sample size exceeds 25,000 samples, pycaret will build a base estimator at 
    various sample levels of the original dataset. This will return a performance 
    plot of R2 values at various sample levels, that will assist you in deciding the 
    preferred sample size for modeling. You are then required to enter the desired  
    sample size that will be considered for training and validation in the pycaret 
    environment. 1 - sample size will be discarded and not be used any further.
    
    sample_estimator: object, default = None
    If None, Linear Regression is used by default.
    
    categorical_features: string, default = None
    If the inferred data types are not correct, categorical_features can be used to
    overwrite the inferred type. For example upon running setup if type of column1
    is inferred as numeric instead of categorical, this parameter can be used to 
    overwrite by passing categorical_features = 'column1'
    
    categorical_imputation: string, default = 'constant'
    If missing values are found in categorical features, it will be imputed with a
    constant 'not_available' value. Other option available is 'mode' in which case
    imputation is done by most frequent value.
    
    numeric_features: string, default = None
    If the inferred data types are not correct, numeric_features can be used to
    overwrite the inferred type. For example upon running setup if type of column1
    is inferred as categorical instead of numeric, this parameter can be used to 
    overwrite by passing numeric_features = 'column1'    

    numeric_imputation: string, default = 'mean'
    If missing values are found in numeric features, it will be imputed with mean
    value of feature. Other option available is 'median' in which case imputation
    will be done by median value.
    
    date_features: string, default = None
    If data has DateTime column and is not automatically detected when running
    setup, this parameter can be used to define date_feature by passing
    data_features = 'date_column_name'. It can work with multiple date columns.
    Date columns is not used in modeling, instead feature extraction is performed
    and date column is dropped from the dataset. Incase the date column as time
    stamp, it will also extract features related to time / hours.
    
    drop_features: string, default = None
    If any feature has to be ignored for modeling, it can be passed in the param
    drop_features. Inferred ID column and DateTime column is automatically set to 
    drop from the dataset. Incase ID column is not correctly detected, it is 
    recommended to drop ID  column using drop_features. 
    
    normalize: bool, default = False
    When set to True, transform feature space using normalize_method param defined.
    Normally, linear algorithms perform better with normalized data. However, the
    results may vary and it is advised to run multiple experiments to evaluate the
    benefit of normalization.
    
    normalize_method: string, default = 'zscore'
    Defines the method to be used for normalization. By default, normalize method
    is set to 'zscore'. The other available option is 'minmax'.
    
    transformation: bool, default = False
    When set to True, apply a power transformation to make data more Gaussian-like
    This is useful for modeling issues related to heteroscedasticity or other 
    situations where normality is desired. The optimal parameter for stabilizing 
    variance and minimizing skewness is estimated through maximum likelihood.
    
    transformation_method: string, default = 'yeo-johnson'
    Defines the method for transformation. By default, transformation method is set
    to 'yeo-johnson'. The other available option is 'quantile' transformation. Both 
    the transformation transforms the feature set to follow Gaussian-like or normal
    distribution. Note that quantile transformer is non-linear and may distort linear 
    correlations between variables measured at the same scale.

    session_id: int, default = None
    If None, a random seed is generated and returned in the Information grid. The 
    unique number is then distributed as a seed in all functions used during the 
    experiment. This can be used for later reproducibility of the entire experiment.
    
    profile: bool, default = False
    If set to true, a data profile for Exploratory Data Analysis will be displayed 
    in an interactive HTML report. 
    
    Returns:
    --------

    info grid:    Information grid is printed.
    -----------      

    environment:  This function returns various outputs that are stored in variable
    -----------   as tuple. They are used by other functions in pycaret.

    Warnings:
    ---------
    None
    
    """
    
    #exception checking   
    import sys
    
    #checking train size parameter
    if type(train_size) is not float:
        sys.exit('(Type Error): train_size parameter only accepts float value.')
    
    #checking sampling parameter
    if type(sampling) is not bool:
        sys.exit('(Type Error): sampling parameter only accepts True or False.')
        
    #checking sampling parameter
    if target not in data.columns:
        sys.exit('(Value Error): Target parameter doesnt exist in the data provided.')   

    #checking session_id
    if session_id is not None:
        if type(session_id) is not int:
            sys.exit('(Type Error): session_id parameter must be an integer.')   
    
    #checking sampling parameter
    if type(profile) is not bool:
        sys.exit('(Type Error): profile parameter only accepts True or False.')
      
    
    #checking normalize parameter
    if type(normalize) is not bool:
        sys.exit('(Type Error): normalize parameter only accepts True or False.')
        
    #checking transformation parameter
    if type(transformation) is not bool:
        sys.exit('(Type Error): transformation parameter only accepts True or False.')
        
    #checking categorical imputation
    allowed_categorical_imputation = ['constant', 'mode']
    if categorical_imputation not in allowed_categorical_imputation:
        sys.exit("(Value Error): categorical_imputation param only accepts 'constant' or 'mode' ")
        
    #checking numeric imputation
    allowed_numeric_imputation = ['mean', 'median']
    if numeric_imputation not in allowed_numeric_imputation:
        sys.exit("(Value Error): numeric_imputation param only accepts 'mean' or 'median' ")
        
    #checking normalize method
    allowed_normalize_method = ['zscore', 'minmax']
    if normalize_method not in allowed_normalize_method:
        sys.exit("(Value Error): normalize_method param only accepts 'zscore' or 'minxmax' ")        
    
    #checking transformation method
    allowed_transformation_method = ['yeo-johnson', 'quantile']
    if transformation_method not in allowed_transformation_method:
        sys.exit("(Value Error): transformation_method param only accepts 'yeo-johnson' or 'quantile' ")        
        
    #cannot drop target
    if drop_features is not None:
        if target in drop_features:
            sys.exit("(Value Error): cannot drop target column. ")  
        
    #forced type check
    all_cols = list(data.columns)
    all_cols.remove(target)
    
    #categorical
    if categorical_features is not None:
        for i in categorical_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")
        
    #numeric
    if numeric_features is not None:
        for i in numeric_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")    
    
    #date features
    if date_features is not None:
        for i in date_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.")      
    
    #drop features
    if drop_features is not None:
        for i in drop_features:
            if i not in all_cols:
                sys.exit("(Value Error): Column type forced is either target column or doesn't exist in the dataset.") 
                
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import datetime, time
   
    #progress bar
    if sampling:
        max = 10 + 3
    else:
        max = 3
        
    progress = ipw.IntProgress(value=0, min=0, max=max, step=1 , description='Processing: ')
    display(progress)
    
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    #general dependencies
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn import metrics
    import random
    import seaborn as sns
    import matplotlib.pyplot as plt
    import plotly.express as px
    
    #cufflinks
    import cufflinks as cf
    cf.go_offline()
    cf.set_config_file(offline=False, world_readable=True)
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #copy original data for pandas profiler
    data_before_preprocess = data.copy()
    
    #declaring global variables to be accessed by other functions
    global X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, experiment__
    
    #generate seed to be used globally
    if session_id is None:
        seed = random.randint(150,9000)
    else:
        seed = session_id
    

    """
    preprocessing starts here
    """
    
    monitor.iloc[1,1:] = 'Preparing Data for Modeling'
    update_display(monitor, display_id = 'monitor')
            
    #define parameters for preprocessor
    
    #categorical features
    if categorical_features is None:
        cat_features_pass = []
    else:
        cat_features_pass = categorical_features
    
    #numeric features
    if numeric_features is None:
        numeric_features_pass = []
    else:
        numeric_features_pass = numeric_features
     
    #drop features
    if drop_features is None:
        drop_features_pass = []
    else:
        drop_features_pass = drop_features
     
    #date features
    if date_features is None:
        date_features_pass = []
    else:
        date_features_pass = date_features
        
    #categorical imputation strategy
    if categorical_imputation == 'constant':
        categorical_imputation_pass = 'not_available'
    elif categorical_imputation == 'mode':
        categorical_imputation_pass = 'most frequent'
    
    #transformation method strategy
    if transformation_method == 'yeo-johnson':
        trans_method_pass = 'yj'
    elif transformation_method == 'quantile':
        trans_method_pass = 'quantile'
    
    #import library
    from pycaret import preprocess
    
    data = preprocess.Preprocess_Path_One(train_data = data, 
                                          target_variable = target,
                                          categorical_features = cat_features_pass,
                                          numerical_features = numeric_features_pass,
                                          time_features = date_features_pass,
                                          features_todrop = drop_features_pass,
                                          numeric_imputation_strategy = numeric_imputation,
                                          categorical_imputation_strategy = categorical_imputation_pass,
                                          scale_data = normalize,
                                          scaling_method = normalize_method,
                                          Power_transform_data = transformation,
                                          Power_transform_method = trans_method_pass,
                                          random_state = seed)

    progress.value += 1

    if hasattr(preprocess.dtypes, 'replacement'):
            label_encoded = preprocess.dtypes.replacement
            label_encoded = str(label_encoded).replace("'", '')
            label_encoded = str(label_encoded).replace("{", '')
            label_encoded = str(label_encoded).replace("}", '')

    else:
        label_encoded = 'None'


    res_type = ['quit','Quit','exit','EXIT','q','Q','e','E','QUIT','Exit']
    res = preprocess.dtypes.response
    if res in res_type:
        sys.exit("(Process Exit): setup has been interupted with user command 'quit'. setup must rerun." )
    
    #save prep pipe
    prep_pipe = preprocess.pipe
    
    #generate values for grid show
    missing_values = data_before_preprocess.isna().sum().sum()
    if missing_values > 0:
        missing_flag = 'True'
    else:
        missing_flag = 'False'
    
    if normalize is True:
        normalize_grid = normalize_method
    else:
        normalize_grid = 'None'
        
    if transformation is True:
        transformation_grid = transformation_method
    else:
        transformation_grid = 'None'
    
    learned_types = preprocess.dtypes.learent_dtypes
    learned_types.drop(target, inplace=True)

    float_type = 0 
    cat_type = 0

    for i in preprocess.dtypes.learent_dtypes:
        if 'float' in str(i):
            float_type += 1
        elif 'object' in str(i):
            cat_type += 1
        elif 'int' in str(i):
            float_type += 1
    
    """
    preprocessing ends here
    """
    
    #reset pandas option
    pd.reset_option("display.max_rows") 
    pd.reset_option("display.max_columns")
    
    
    #create an empty list for pickling later.
    experiment__ = []
    
    #sample estimator
    if sample_estimator is None:
        model = LinearRegression()
    else:
        model = sample_estimator
        
    model_name = str(model).split("(")[0]
    
    if 'CatBoostRegressor' in model_name:
        model_name = 'CatBoostRegressor'
        
    #creating variables to be used later in the function
    X = data.drop(target,axis=1)
    y = data[target]
    
    progress.value += 1
    
    if sampling is True and data.shape[0] > 25000: #change back to 25000
    
        split_perc = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
        split_perc_text = ['10%','20%','30%','40%','50%','60%', '70%', '80%', '90%', '100%']
        split_perc_tt = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99]
        split_perc_tt_total = []
        split_percent = []

        metric_results = []
        metric_name = []
        
        counter = 0
        
        for i in split_perc:
            
            progress.value += 1
            
            t0 = time.time()
            
            '''
            MONITOR UPDATE STARTS
            '''
            
            perc_text = split_perc_text[counter]
            monitor.iloc[1,1:] = 'Fitting Model on ' + perc_text + ' sample'
            update_display(monitor, display_id = 'monitor')

            '''
            MONITOR UPDATE ENDS
            '''
    
            X_, X__, y_, y__ = train_test_split(X, y, test_size=1-i)
            X_train, X_test, y_train, y_test = train_test_split(X_, y_, test_size=0.3, random_state=seed)
            model.fit(X_train,y_train)
            pred_ = model.predict(X_test)
            
            r2 = metrics.r2_score(y_test,pred_)
            metric_results.append(r2)
            metric_name.append('R2')
            split_percent.append(i)
            
            t1 = time.time()
                       
            '''
            Time calculation begins
            '''
          
            tt = t1 - t0
            total_tt = tt / i
            split_perc_tt.pop(0)
            
            for remain in split_perc_tt:
                ss = total_tt * remain
                split_perc_tt_total.append(ss)
                
            ttt = sum(split_perc_tt_total) / 60
            ttt = np.around(ttt, 2)
        
            if ttt < 1:
                ttt = str(np.around((ttt * 60), 2))
                ETC = ttt + ' Seconds Remaining'

            else:
                ttt = str (ttt)
                ETC = ttt + ' Minutes Remaining'
                
            monitor.iloc[2,1:] = ETC
            update_display(monitor, display_id = 'monitor')
            
            
            '''
            Time calculation Ends
            '''
            
            split_perc_tt_total = []
            counter += 1

        #model_results = pd.DataFrame({'Sample %' : split_percent, 'Metric' : metric_results, 'Metric Name': metric_name})

        model_results = pd.DataFrame({'Sample %' : split_percent, 'Metric' : metric_results, 'Metric Name': metric_name})
        fig = px.line(model_results, x='Sample %', y='Metric', color='Metric Name', line_shape='linear', range_y = [0,1])
        fig.update_layout(plot_bgcolor='rgb(245,245,245)')
        title= str(model_name) + ' Metric and Sample %'
        fig.update_layout(title={'text': title, 'y':0.95,'x':0.45,'xanchor': 'center','yanchor': 'top'})
        fig.show()
        
        monitor.iloc[1,1:] = 'Waiting for input'
        update_display(monitor, display_id = 'monitor')
        
        
        print('Please Enter the sample % of data you would like to use for modeling. Example: Enter 0.3 for 30%.')
        print('Press Enter if you would like to use 100% of the data.')
        
        print(' ')
        
        sample_size = input("Sample Size: ")
        
        if sample_size == '' or sample_size == '1':
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_size, random_state=seed)
            
            '''
            Final display Starts
            '''
            clear_output()
            print(' ')

            if profile:
                print('Setup Succesfully Completed! Loading Profile Now... Please Wait!')
            else:
                print('Setup Succesfully Completed!')    
        
            functions = pd.DataFrame ( [ ['session_id', seed ],
                                         ['Original Data',X.shape ], 
                                         ['Sampled Data',X.shape ], 
                                         ['Sample %',X.shape[0] / X.shape[0]], 
                                         ['Training Set', X_train.shape ], 
                                         ['Test / Hold-out Set',X_test.shape ], 
                                         ['Categorical Features ', cat_type ],
                                         ['Numeric Features ', float_type ],
                                         ['Normalize ', normalize ],
                                         ['Normalize Method ', normalize_grid ],
                                         ['Transformation ', transformation ],
                                         ['Transformation Method ', transformation_grid ],
                                         ['Missing Values ', missing_flag],
                                         ['Numeric Imputer ', numeric_imputation],
                                         ['Categorical Imputer ', categorical_imputation],
                                       ], columns = ['Description', 'Value'] )

            functions_ = functions.style.hide_index()
            display(functions_)
            
            if profile:
                try:
                    import pandas_profiling
                    pf = pandas_profiling.ProfileReport(data_before_preprocess)
                    clear_output()
                    display(pf)
                except:
                    print('Data Profiler Failed. No output to show, please continue with Modeling.')
            
            '''
            Final display Ends
            '''   
            
            #log into experiment
            experiment__.append(('Info', functions))
            experiment__.append(('X_training Set', X_train))
            experiment__.append(('y_training Set', y_train))
            experiment__.append(('X_test Set', X_test))
            experiment__.append(('y_test Set', y_test))
            experiment__.append(('Transformation Pipeline', prep_pipe))
        
            return X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, experiment__
        
        else:
            
            sample_n = float(sample_size)
            X_selected, X_discard, y_selected, y_discard = train_test_split(X, y, test_size=1-sample_n,  
                                                                random_state=seed)
            
            X_train, X_test, y_train, y_test = train_test_split(X_selected, y_selected, test_size=1-train_size, 
                                                                random_state=seed)
            clear_output()
            
            
            '''
            Final display Starts
            '''
            
            clear_output()
            print(' ')
            
            if profile:
                print('Setup Succesfully Completed! Loading Profile Now... Please Wait!')
            else:
                print('Setup Succesfully Completed!')
            
            functions = pd.DataFrame ( [ ['session_id', seed ],
                                         ['Original Data',X.shape ], 
                                         ['Sampled Data',X_selected.shape ], 
                                         ['Sample %',X_selected.shape[0] / X.shape[0]], 
                                         ['Training Set', X_train.shape ], 
                                         ['Test / Hold-out Set',X_test.shape ], 
                                         ['Categorical Features ', cat_type ],
                                         ['Numeric Features ', float_type ],
                                         ['Normalize ', normalize ],
                                         ['Normalize Method ', normalize_grid ],
                                         ['Transformation ', transformation ],
                                         ['Transformation Method ', transformation_grid ],
                                         ['Missing Values ', missing_flag],
                                         ['Numeric Imputer ', numeric_imputation],
                                         ['Categorical Imputer ', categorical_imputation],
                                       ], columns = ['Description', 'Value'] )
            
            functions_ = functions.style.hide_index()
            display(functions_)
            
            if profile:
                try:
                    import pandas_profiling
                    pf = pandas_profiling.ProfileReport(data_before_preprocess)
                    clear_output()
                    display(pf)
                except:
                    print('Data Profiler Failed. No output to show, please continue with Modeling.')
            
            '''
            Final display Ends
            ''' 
            
            #log into experiment
            experiment__.append(('Info', functions))
            experiment__.append(('X_training Set', X_train))
            experiment__.append(('y_training Set', y_train))
            experiment__.append(('X_test Set', X_test))
            experiment__.append(('y_test Set', y_test))
            experiment__.append(('Transformation Pipeline', prep_pipe))
            
            return X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, experiment__

    else:
        
        monitor.iloc[1,1:] = 'Splitting Data'
        update_display(monitor, display_id = 'monitor')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-train_size, random_state=seed)
        progress.value += 1
        
        clear_output()
        
        '''
        Final display Starts
        '''
        clear_output()
        print(' ')
        if profile:
            print('Setup Succesfully Completed! Loading Profile Now... Please Wait!')
        else:
            print('Setup Succesfully Completed!')
        functions = pd.DataFrame ( [ ['session_id', seed ],
                                     ['Original Data',X.shape ], 
                                     ['Sampled Data',X.shape ], 
                                     ['Sample %',X.shape[0] / X.shape[0]], 
                                     ['Training Set', X_train.shape ], 
                                     ['Test / Hold-out Set',X_test.shape ], 
                                     ['Categorical Features ', cat_type ],
                                     ['Numeric Features ', float_type ],
                                     ['Normalize ', normalize ],
                                     ['Normalize Method ', normalize_grid ],
                                     ['Transformation ', transformation ],
                                     ['Transformation Method ', transformation_grid ],
                                     ['Missing Values ', missing_flag],
                                     ['Numeric Imputer ', numeric_imputation],
                                     ['Categorical Imputer ', categorical_imputation],
                                   ], columns = ['Description', 'Value'] )
        
        functions_ = functions.style.hide_index()
        display(functions_)
            
        if profile:
            try:
                import pandas_profiling
                pf = pandas_profiling.ProfileReport(data_before_preprocess)
                clear_output()
                display(pf)
            except:
                print('Data Profiler Failed. No output to show, please continue with Modeling.')
            
        '''
        Final display Ends
        '''   
        
        #log into experiment
        experiment__.append(('Regression Info', functions))
        experiment__.append(('X_training Set', X_train))
        experiment__.append(('y_training Set', y_train))
        experiment__.append(('X_test Set', X_test))
        experiment__.append(('y_test Set', y_test))
        experiment__.append(('Transformation Pipeline', prep_pipe))
        
        return X, y, X_train, X_test, y_train, y_test, seed, prep_pipe, experiment__



def create_model(estimator = None, 
                 ensemble = False, 
                 method = None, 
                 fold = 10, 
                 round = 4,  
                 verbose = True):
    
     
    """  
     
    Description:
    ------------
    This function creates a model and scores it using Kfold Cross Validation. 
    (default = 10 Fold). The output prints a score grid that shows MAE, MSE, 
    RMSE, R2 and Max Error (ME). 

    This function returns a trained model object. 

    setup() function must be called before using create_model()

        Example
        -------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        
        lr = create_model('lr')

        This will create a trained Linear Regression model.

    Parameters
    ----------
    estimator : string, default = None

    Enter abbreviated string of the estimator class. List of estimators supported:

    Estimator                     Abbreviated String     Original Implementation 
    ---------                     ------------------     -----------------------
    Linear Regression             'lr'                   linear_model.LinearRegression
    Lasso Regression              'lasso'                linear_model.Lasso
    Ridge Regression              'ridge'                linear_model.Ridge
    Elastic Net                   'en'                   linear_model.ElasticNet
    Least Angle Regression        'lar'                  linear_model.Lars
    Lasso Least Angle Regression  'llar'                 linear_model.LassoLars
    Orthogonal Matching Pursuit   'omp'                  linear_model.OMP
    Bayesian Ridge                'br'                   linear_model.BayesianRidge
    Automatic Relevance Determ.   'ard'                  linear_model.ARDRegression
    Passive Aggressive Regressor  'par'                  linear_model.PAR
    Random Sample Consensus       'ransac'               linear_model.RANSACRegressor
    TheilSen Regressor            'tr'                   linear_model.TheilSenRegressor
    Huber Regressor               'huber'                linear_model.HuberRegressor 
    Kernel Ridge                  'kr'                   kernel_ridge.KernelRidge
    Support Vector Machine        'svm'                  svm.SVR
    K Neighbors Regressor         'knn'                  neighbors.KNeighborsRegressor 
    Decision Tree                 'dt'                   tree.DecisionTreeRegressor
    Random Forest                 'rf'                   ensemble.RandomForestRegressor
    Extra Trees Regressor         'et'                   ensemble.ExtraTreesRegressor
    AdaBoost Regressor            'ada'                  ensemble.AdaBoostRegressor
    Gradient Boosting             'gbr'                  ensemble.GradientBoostingRegressor 
    Multi Level Perceptron        'mlp'                  neural_network.MLPRegressor
    Extreme Gradient Boosting     'xgboost'              xgboost.readthedocs.io
    Light Gradient Boosting       'lightgbm'             github.com/microsoft/LightGBM
    CatBoost Regressor            'catboost'             https://catboost.ai

    ensemble: Boolean, default = False
    True would result in an ensemble of estimator using the method parameter defined. 

    method: String, 'Bagging' or 'Boosting', default = None.
    method must be defined when ensemble is set to True. Default method is set to None. 

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to. 

    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.

    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and 
                  standard deviation of the scores across the folds are also returned.

    model:        trained model object
    -----------

    Warnings:
    ---------
    None
      
    
  
    """


    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys
    
    #checking error for estimator (string)
    available_estimators = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                            'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 'gbr', 
                            'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    if estimator not in available_estimators:
        sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')
        
    #checking error for ensemble:
    if type(ensemble) is not bool:
        sys.exit('(Type Error): Ensemble parameter can only take argument as True or False.') 
    
    #checking error for method:
    
    #1 Check When method given and ensemble is not set to True.
    if ensemble is False and method is not None:
        sys.exit('(Type Error): Method parameter only accepts value when ensemble is set to True.')

    #2 Check when ensemble is set to True and method is not passed.
    if ensemble is True and method is None:
        sys.exit("(Type Error): Method parameter missing. Pass method = 'Bagging' or 'Boosting'.")
        
    #3 Check when ensemble is set to True and method is passed but not allowed.
    available_method = ['Bagging', 'Boosting']
    if ensemble is True and method not in available_method:
        sys.exit("(Value Error): Method parameter only accepts two values 'Bagging' or 'Boosting'.")
        
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import datetime, time
        
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 

    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    #general dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    
    progress.value += 1
    
    #cross validation setup starts here
    kf = KFold(fold, random_state=seed)
    
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))    
  
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Selecting Estimator'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
        
    if estimator == 'lr':
        
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        full_name = 'Linear Regression'
        
    elif estimator == 'lasso':
        
        from sklearn.linear_model import Lasso
        model = Lasso(random_state=seed)
        full_name = 'Lasso Regression'
        
    elif estimator == 'ridge':
        
        from sklearn.linear_model import Ridge
        model = Ridge(random_state=seed)
        full_name = 'Ridge Regression'
        
    elif estimator == 'en':
        
        from sklearn.linear_model import ElasticNet
        model = ElasticNet(random_state=seed)
        full_name = 'Elastic Net'
        
    elif estimator == 'lar':
        
        from sklearn.linear_model import Lars
        model = Lars()
        full_name = 'Least Angle Regression'
        
    elif estimator == 'llar':
        
        from sklearn.linear_model import LassoLars
        model = LassoLars()
        full_name = 'Lasso Least Angle Regression'
        
    elif estimator == 'omp':
        
        from sklearn.linear_model import OrthogonalMatchingPursuit
        model = OrthogonalMatchingPursuit()
        full_name = 'Orthogonal Matching Pursuit'
        
    elif estimator == 'br':
        from sklearn.linear_model import BayesianRidge
        model = BayesianRidge()
        full_name = 'Bayesian Ridge Regression' 
        
    elif estimator == 'ard':
        
        from sklearn.linear_model import ARDRegression
        model = ARDRegression()
        full_name = 'Automatic Relevance Determination'        
        
    elif estimator == 'par':
        
        from sklearn.linear_model import PassiveAggressiveRegressor
        model = PassiveAggressiveRegressor(random_state=seed)
        full_name = 'Passive Aggressive Regressor'    
        
    elif estimator == 'ransac':
        
        from sklearn.linear_model import RANSACRegressor
        model = RANSACRegressor(min_samples=0.5, random_state=seed)
        full_name = 'Random Sample Consensus'   
        
    elif estimator == 'tr':
        
        from sklearn.linear_model import TheilSenRegressor
        model = TheilSenRegressor(random_state=seed)
        full_name = 'TheilSen Regressor'     
        
    elif estimator == 'huber':
        
        from sklearn.linear_model import HuberRegressor
        model = HuberRegressor()
        full_name = 'Huber Regressor'   
        
    elif estimator == 'kr':
        
        from sklearn.kernel_ridge import KernelRidge
        model = KernelRidge()
        full_name = 'Kernel Ridge'
        
    elif estimator == 'svm':
        
        from sklearn.svm import SVR
        model = SVR()
        full_name = 'Support Vector Regression'  
        
    elif estimator == 'knn':
        
        from sklearn.neighbors import KNeighborsRegressor
        model = KNeighborsRegressor()
        full_name = 'Nearest Neighbors Regression' 
        
    elif estimator == 'dt':
        
        from sklearn.tree import DecisionTreeRegressor
        model = DecisionTreeRegressor(random_state=seed)
        full_name = 'Decision Tree Regressor'
        
    elif estimator == 'rf':
        
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(random_state=seed)
        full_name = 'Random Forest Regressor'
        
    elif estimator == 'et':
        
        from sklearn.ensemble import ExtraTreesRegressor
        model = ExtraTreesRegressor(random_state=seed)
        full_name = 'Extra Trees Regressor'    
        
    elif estimator == 'ada':
        
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(random_state=seed)
        full_name = 'AdaBoost Regressor'   
        
    elif estimator == 'gbr':
        
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(random_state=seed)
        full_name = 'Gradient Boosting Regressor'       
        
    elif estimator == 'mlp':
        
        from sklearn.neural_network import MLPRegressor
        model = MLPRegressor(random_state=seed)
        full_name = 'MLP Regressor'
        
    elif estimator == 'xgboost':
        
        from xgboost import XGBRegressor
        model = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
        full_name = 'Extreme Gradient Boosting Regressor'
        
    elif estimator == 'lightgbm':
        
        import lightgbm as lgb
        model = lgb.LGBMRegressor(random_state=seed)
        full_name = 'Light Gradient Boosting Machine'
        
    elif estimator == 'catboost':
        from catboost import CatBoostRegressor
        model = CatBoostRegressor(random_state=seed, silent = True)
        full_name = 'CatBoost Regressor'
        
    else:
        model = estimator
        full_name = str(model).split("(")[0]
    
    progress.value += 1
    
    #checking method when ensemble is set to True. 

    if method == 'Bagging':
        
        from sklearn.ensemble import BaggingRegressor
        model = BaggingRegressor(model,bootstrap=True,n_estimators=10, random_state=seed)

    elif method == 'Boosting':
        
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(model, n_estimators=10, random_state=seed)
    
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]  
        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)
       
        progress.value += 1
        
        
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_] }).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
            
        fold_num += 1
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''

    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_max_error=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_max_error=np.std(score_max_error)

    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_max_error)
    avgs_max_error = np.append(avgs_max_error, std_max_error)
    
    progress.value += 1
    
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2, 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2 , 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Compiling Final Model'
    update_display(monitor, display_id = 'monitor')
    
    model.fit(data_X, data_y)
    
    progress.value += 1
    
    #storing into experiment
    tup = (full_name,model)
    experiment__.append(tup)
    nam = str(full_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    if verbose:
        clear_output()
        display(model_results)
        return model
    else:
        clear_output()
        return model



def ensemble_model(estimator,
                   method = 'Bagging', 
                   fold = 10,
                   n_estimators = 10,
                   round = 4,  
                   verbose = True):
    """
    
    Description:
    ------------
    This function ensembles the trained base estimator using the method defined 
    in 'method' param (default = 'Bagging'). The output prints a score grid that 
    shows MAE, MSE, RMSE, R2 and Max Error (ME) by fold (default CV = 10 Folds).

    This function returns a trained model object.  

    Model must be created using create_model() or tune_model().

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        dt = create_model('dt')
        
        ensembled_dt = ensemble_model(dt)

        This will return an ensembled Decision Tree model using 'Bagging'.

    Parameters
    ----------
    estimator : object, default = None

    method: String, default = 'Bagging'
    Bagging method will create an ensemble meta-estimator that fits base 
    regressor each on random subsets of the original dataset. The other
    available method is 'Boosting' that fits a regressor on the original 
    dataset and then fits additional copies of the regressor on the same 
    dataset but where the weights of instances are adjusted according to 
    the error of the current prediction. As such, subsequent regressors 
    focus more on difficult cases.
    
    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2.
    
    n_estimators: integer, default = 10
    The number of base estimators in the ensemble.
    In case of perfect fit, the learning procedure is stopped early.

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to.

    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.


    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and
                  standard deviation of the scores across the folds are also
                  returned.

    model:        trained ensembled model object
    -----------

    Warnings:
    ---------
    None
      
        
    
    """
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys
        
    #Check for allowed method
    available_method = ['Bagging', 'Boosting']
    if method not in available_method:
        sys.exit("(Value Error): Method parameter only accepts two values 'Bagging' or 'Boosting'.")
    
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking n_estimators parameter
    if type(n_estimators) is not int:
        sys.exit('(Type Error): n_estimators parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''    
    
    #pre-load libraries
    import pandas as pd
    import datetime, time
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
        
    #dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold   
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore')    
    
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
      
    progress.value += 1
    
    #defining estimator as model
    model = estimator
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Selecting Estimator'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if method == 'Bagging':
        
        from sklearn.ensemble import BaggingRegressor
        model = BaggingRegressor(model,bootstrap=True,n_estimators=n_estimators, random_state=seed)
         
    else:
        
        from sklearn.ensemble import AdaBoostRegressor
        model = AdaBoostRegressor(model, n_estimators=n_estimators, random_state=seed)
    
    progress.value += 1
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    kf = KFold(fold, random_state=seed)
    
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))
    
    fold_num = 1 
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]
        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)
        
        progress.value += 1
        
                
        '''
        
        This section is created to update_display() as code loops through the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        
        TIME CALCULATION SUB-SECTION STARTS HERE
        
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        update_display(ETC, display_id = 'ETC')
            
        fold_num += 1
        
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        '''
        
        TIME CALCULATION ENDS HERE
        
        '''

        if verbose:
            update_display(master_display, display_id = display_id)
        
        '''
        
        Update_display() ends here
        
        '''
        
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_max_error=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_max_error=np.std(score_max_error)

    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_max_error)
    avgs_max_error = np.append(avgs_max_error, std_max_error)

    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2 , 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2 , 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)  
    
    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Compiling Final Model'
    update_display(monitor, display_id = 'monitor')
    
    model.fit(data_X, data_y)
    
    progress.value += 1
    
    #storing into experiment
    model_name = str(model).split("(")[0]
    tup = (model_name,model)
    experiment__.append(tup)
    
    nam = str(model_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    if verbose:
        clear_output()
        display(model_results)
        return model
    else:
        clear_output()
        return model



def compare_models(blacklist = None,
                   fold = 10, 
                   round = 4, 
                   sort = 'R2',
                   turbo = True):
    
    """
       
   
    Description:
    ------------
    This function uses all models in the model library and scores them using  
    Kfold Cross Validation. The output prints a score grid that shows MAE, MSE, 
    RMSE, R2 and ME by fold (default CV = 10 Folds) of all the available models
    in model library.
    
    When turbo is set to True ('kr', 'ard' and 'mlp') are excluded due to longer
    training times. By default turbo param is set to True.

    List of models in Model Library

    Estimator                     Abbreviated String     Original Implementation 
    ---------                     ------------------     -----------------------
    Linear Regression             'lr'                   linear_model.LinearRegression
    Lasso Regression              'lasso'                linear_model.Lasso
    Ridge Regression              'ridge'                linear_model.Ridge
    Elastic Net                   'en'                   linear_model.ElasticNet
    Least Angle Regression        'lar'                  linear_model.Lars
    Lasso Least Angle Regression  'llar'                 linear_model.LassoLars
    Orthogonal Matching Pursuit   'omp'                  linear_model.OMP
    Bayesian Ridge                'br'                   linear_model.BayesianRidge
    Automatic Relevance Determ.   'ard'                  linear_model.ARDRegression
    Passive Aggressive Regressor  'par'                  linear_model.PAR
    Random Sample Consensus       'ransac'               linear_model.RANSACRegressor
    TheilSen Regressor            'tr'                   linear_model.TheilSenRegressor
    Huber Regressor               'huber'                linear_model.HuberRegressor 
    Kernel Ridge                  'kr'                   kernel_ridge.KernelRidge
    Support Vector Machine        'svm'                  svm.SVR
    K Neighbors Regressor         'knn'                  neighbors.KNeighborsRegressor 
    Decision Tree                 'dt'                   tree.DecisionTreeRegressor
    Random Forest                 'rf'                   ensemble.RandomForestRegressor
    Extra Trees Regressor         'et'                   ensemble.ExtraTreesRegressor
    AdaBoost Regressor            'ada'                  ensemble.AdaBoostRegressor
    Gradient Boosting             'gbr'                  ensemble.GradientBoostingRegressor 
    Multi Level Perceptron        'mlp'                  neural_network.MLPRegressor
    Extreme Gradient Boosting     'xgboost'              xgboost.readthedocs.io
    Light Gradient Boosting       'lightgbm'             github.com/microsoft/LightGBM
    CatBoost Regressor            'catboost'             https://catboost.ai

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')

        compare_models() 

        This will return the averaged score grid of all models except 'kr', 'ard' 
        and 'mlp'. When turbo param is set to False, all models including 'kr',
        'ard' and 'mlp' are used, but this may result in longer training times.
        
        compare_models(blacklist = ['knn','gbr'], turbo = False) 

        This will return a comparison of all models except K Nearest Neighbour and
        Gradient Boosting Regressor.
        
        compare_models(blacklist = ['knn','gbr'] , turbo = True) 

        This will return a comparison of all models except K Nearest Neighbour, 
        Gradient Boosting Regressor, Kernel Ridge Regressor, Automatic Relevance
        Determinant and Multi Level Perceptron.
        
    Parameters
    ----------
    blacklist: string, default = None
    In order to omit certain models from the comparison, the abbreviation string 
    (see above list) can be passed as list in blacklist param. This is normally
    done to be more efficient with time. 

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to.
  
    sort: string, default = 'MAE'
    The scoring measure specified is used for sorting the average score grid
    Other options are 'MAE', 'MSE', 'RMSE', 'R2' and 'ME'.

    turbo: Boolean, default = True
    When turbo is set to True, it blacklists estimators that have longer
    training times.
    
    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and Max Error (ME) 
                  Mean and standard deviation of the scores across the folds is
                  also returned.

    Warnings:
    ---------
    - compare_models() though attractive, might be time consuming with large 
      datasets. By default turbo is set to True, which blacklists models that
      have longer training times. Changing turbo parameter to False may result 
      in very high training times with datasets where number of samples exceed 
      10,000.

    - This function doesn't return model object.
      
               
    
    """
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys
    
    #checking error for blacklist (string)
    available_estimators = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                            'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 'gbr', 
                            'mlp', 'xgboost', 'lightgbm', 'catboost']

    if blacklist != None:
        for i in blacklist:
            if i not in available_estimators:
                sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')
        
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking sort parameter
    allowed_sort = ['MAE', 'MSE', 'RMSE', 'R2', 'ME']
    if sort not in allowed_sort:
        sys.exit('(Value Error): Sort method not supported. See docstring for list of available parameters.')
    
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    #progress bar
    if blacklist is None:
        len_of_blacklist = 0
    else:
        len_of_blacklist = len(blacklist)
        
    if turbo:
        len_mod = 22 - len_of_blacklist
    else:
        len_mod = 25 - len_of_blacklist
        
    progress = ipw.IntProgress(value=0, min=0, max=(fold*len_mod)+25, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['Model', 'MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['Estimator' , '. . . . . . . . . . . . . . . . . .' , 'Compiling Library' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    display_ = display(master_display, display_id=True)
    display_id = display_.display_id
    
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #general dependencies
    import numpy as np
    import random
    from sklearn import metrics
    from sklearn.model_selection import KFold
    import pandas.io.formats.style
    
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    progress.value += 1
    
    #import sklearn dependencies
    from sklearn.linear_model import LinearRegression
    from sklearn.linear_model import Ridge
    from sklearn.linear_model import Lasso
    from sklearn.linear_model import ElasticNet
    from sklearn.linear_model import Lars
    from sklearn.linear_model import LassoLars
    from sklearn.linear_model import OrthogonalMatchingPursuit
    from sklearn.linear_model import BayesianRidge
    from sklearn.linear_model import ARDRegression
    from sklearn.linear_model import PassiveAggressiveRegressor
    from sklearn.linear_model import RANSACRegressor
    from sklearn.linear_model import TheilSenRegressor
    from sklearn.linear_model import HuberRegressor
    from sklearn.kernel_ridge import KernelRidge
    from sklearn.svm import SVR
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.ensemble import ExtraTreesRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.neural_network import MLPRegressor
    from xgboost import XGBRegressor
    from catboost import CatBoostRegressor
    try:
        import lightgbm as lgb
    except:
        pass
   
    progress.value += 1

    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Loading Estimator'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    #creating model object
    lr = LinearRegression()
    lasso = Lasso(random_state=seed)
    ridge = Ridge(random_state=seed)
    en = ElasticNet(random_state=seed)
    lar = Lars()
    llar = LassoLars()
    omp = OrthogonalMatchingPursuit()
    br = BayesianRidge()
    ard = ARDRegression()
    par = PassiveAggressiveRegressor(random_state=seed)
    ransac = RANSACRegressor(min_samples=0.5, random_state=seed)
    tr = TheilSenRegressor(random_state=seed)
    huber = HuberRegressor()
    kr = KernelRidge()
    svm = SVR()
    knn = KNeighborsRegressor()
    dt = DecisionTreeRegressor(random_state=seed)
    rf = RandomForestRegressor(random_state=seed)
    et = ExtraTreesRegressor(random_state=seed)
    ada = AdaBoostRegressor(random_state=seed)
    gbr = GradientBoostingRegressor(random_state=seed)
    mlp = MLPRegressor(random_state=seed)
    xgboost = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
    lightgbm = lgb.LGBMRegressor(random_state=seed)
    catboost = CatBoostRegressor(random_state=seed, silent = True)
    
    progress.value += 1
    
    model_library = [lr, lasso, ridge, en, lar, llar, omp, br, ard, par, ransac, tr, huber, kr, 
                     svm, knn, dt, rf, et, ada, gbr, mlp, xgboost, lightgbm, catboost]
    
    model_names = ['Linear Regression',
                   'Lasso Regression',
                   'Ridge Regression',
                   'Elastic Net',
                   'Least Angle Regression',
                   'Lasso Least Angle Regression',
                   'Orthogonal Matching Pursuit',
                   'Bayesian Ridge',
                   'Automatic Relevance Determination',
                   'Passive Aggressive Regressor',
                   'Random Sample Consensus',
                   'TheilSen Regressor',
                   'Huber Regressor',
                   'Kernel Ridge',
                   'Support Vector Machine',
                   'K Neighbors Regressor',
                   'Decision Tree',
                   'Random Forest',
                   'Extra Trees Regressor',
                   'AdaBoost Regressor',
                   'Gradient Boosting Regressor',
                   'Multi Level Perceptron',
                   'Extreme Gradient Boosting',
                   'Light Gradient Boosting Machine',
                   'CatBoost Regressor']
    
    
    #checking for blacklist models
    
    model_library_str = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard',
                         'par', 'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 
                         'et', 'ada', 'gbr', 'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    model_library_str_ = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard',
                         'par', 'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 
                         'et', 'ada', 'gbr', 'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    if blacklist is not None:
        
        if turbo:
            internal_blacklist = ['kr', 'ard', 'mlp']
            compiled_blacklist = blacklist + internal_blacklist
            blacklist = list(set(compiled_blacklist))
            
        else:
            blacklist = blacklist
        
        for i in blacklist:
            model_library_str_.remove(i)
        
        si = []
        
        for i in model_library_str_:
            s = model_library_str.index(i)
            si.append(s)
        
        model_library_ = []
        model_names_= []
        for i in si:
            model_library_.append(model_library[i])
            model_names_.append(model_names[i])
            
        model_library = model_library_
        model_names = model_names_
        
        
    if blacklist is None and turbo is True:
        
        model_library = [lr, lasso, ridge, en, lar, llar, omp, br, par, ransac, tr, huber, 
                         svm, knn, dt, rf, et, ada, gbr, xgboost, lightgbm, catboost]
    
        model_names = ['Linear Regression',
                       'Lasso Regression',
                       'Ridge Regression',
                       'Elastic Net',
                       'Least Angle Regression',
                       'Lasso Least Angle Regression',
                       'Orthogonal Matching Pursuit',
                       'Bayesian Ridge',
                       'Passive Aggressive Regressor',
                       'Random Sample Consensus',
                       'TheilSen Regressor',
                       'Huber Regressor',
                       'Support Vector Machine',
                       'K Neighbors Regressor',
                       'Decision Tree',
                       'Random Forest',
                       'Extra Trees Regressor',
                       'AdaBoost Regressor',
                       'Gradient Boosting Regressor',
                       'Extreme Gradient Boosting',
                       'Light Gradient Boosting Machine',
                       'CatBoost Regressor']
    
        
            
    progress.value += 1

    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    #cross validation setup starts here
    kf = KFold(fold, random_state=seed)

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))  
    
    name_counter = 0
      
    for model in model_library:
        
        progress.value += 1
        
        '''
        MONITOR UPDATE STARTS
        '''
        monitor.iloc[2,1:] = model_names[name_counter]
        monitor.iloc[3,1:] = 'Calculating ETC'
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        fold_num = 1
        
        for train_i , test_i in kf.split(data_X,data_y):
        
            progress.value += 1
            
            t0 = time.time()
            
            '''
            MONITOR UPDATE STARTS
            '''
                
            monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
            update_display(monitor, display_id = 'monitor')
            
            '''
            MONITOR UPDATE ENDS
            '''            
     
            Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
            ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]
            model.fit(Xtrain,ytrain)
            pred_ = model.predict(Xtest)
            mae = metrics.mean_absolute_error(ytest,pred_)
            mse = metrics.mean_squared_error(ytest,pred_)
            rmse = np.sqrt(mse)
            r2 = metrics.r2_score(ytest,pred_)
            max_error_ = metrics.max_error(ytest,pred_)
            score_mae = np.append(score_mae,mae)
            score_mse = np.append(score_mse,mse)
            score_rmse = np.append(score_rmse,rmse)
            score_r2 =np.append(score_r2,r2)
            score_max_error = np.append(score_max_error,max_error_)            
                
                
            '''
            TIME CALCULATION SUB-SECTION STARTS HERE
            '''
            t1 = time.time()
        
            tt = (t1 - t0) * (fold-fold_num) / 60
            tt = np.around(tt, 2)
        
            if tt < 1:
                tt = str(np.around((tt * 60), 2))
                ETC = tt + ' Seconds Remaining'
                
            else:
                tt = str (tt)
                ETC = tt + ' Minutes Remaining'
            
            fold_num += 1
            
            '''
            MONITOR UPDATE STARTS
            '''

            monitor.iloc[3,1:] = ETC
            update_display(monitor, display_id = 'monitor')

            '''
            MONITOR UPDATE ENDS
            '''
        
        avgs_mae = np.append(avgs_mae,np.mean(score_mae))
        avgs_mse = np.append(avgs_mse,np.mean(score_mse))
        avgs_rmse = np.append(avgs_rmse,np.mean(score_rmse))
        avgs_r2 = np.append(avgs_r2,np.mean(score_r2))
        avgs_max_error = np.append(avgs_max_error,np.mean(score_max_error))
        
        compare_models_ = pd.DataFrame({'Model':model_names[name_counter], 'MAE':avgs_mae, 'MSE':avgs_mse, 
                           'RMSE':avgs_rmse, 'R2':avgs_r2, 
                           'ME':avgs_max_error})
        master_display = pd.concat([master_display, compare_models_],ignore_index=True)
        master_display = master_display.round(round)
        
        if sort == 'R2':
            master_display = master_display.sort_values(by=sort,ascending=False)
        else:
            master_display = master_display.sort_values(by=sort,ascending=True)
        
        master_display.reset_index(drop=True, inplace=True)
        
        update_display(master_display, display_id = display_id)
        
        score_mae =np.empty((0,0))
        score_mse =np.empty((0,0))
        score_rmse =np.empty((0,0))
        score_r2 =np.empty((0,0))
        score_max_error =np.empty((0,0))
        
        avgs_mae = np.empty((0,0))
        avgs_mse = np.empty((0,0))
        avgs_rmse = np.empty((0,0))
        avgs_r2 = np.empty((0,0))
        avgs_max_error = np.empty((0,0))
        
        name_counter += 1
  
    progress.value += 1
    
    #storing into experiment
    model_name = 'Compare Models Score Grid'
    tup = (model_name,master_display)
    experiment__.append(tup)
    
    def highlight_min(s):
        is_min = s == s.min()
        return ['background-color: yellow' if v else '' for v in is_min]

    compare_models_ = master_display.style.apply(highlight_min,subset=['MAE','MSE','RMSE','ME'])
    compare_models_ = compare_models_.set_properties(**{'text-align': 'left'})
    compare_models_ = compare_models_.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
    
    progress.value += 1
    
    clear_output()

    return compare_models_



def blend_models(estimator_list = 'All', 
                 fold = 10, 
                 round = 4, 
                 turbo = True,
                 verbose = True):
    
    """
        
    Description:
    ------------
    This function creates an ensemble meta-estimator that fits a base regressor on 
    the whole dataset. It then averages the predictions to form a final prediction. 
    By default, this function will use all estimators in the model library (excluding 
    the few estimators when turbo is True) or a specific trained estimator passed as a
    list in estimator_list param. It scores it using Kfold Cross Validation. The output
    prints the score grid that shows MAE, MSE, RMSE, R2 and ME by fold (default = 10 Fold). 

    This function returns a trained model object.  

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        
        blend_all = blend_models() 

        This will result in VotingRegressor for all models in the library except 'ard',
        'kr' and 'mlp'.
        
        For specific models, you can use:

        lr = create_model('lr')
        rf = create_model('rf')
        knn = create_model('knn')

        blend_three = blend_models(estimator_list = [lr,rf,knn])
    
        This will create a VotingRegressor of lr, rf and knn.

    Parameters
    ----------
    estimator_list : string ('All') or list of object, default = 'All'

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to.

    turbo: Boolean, default = True
    When turbo is set to True, it blacklists estimator that uses Radial Kernel.

    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.

    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and
                  standard deviation of the scores across the folds are also 
                  returned.

    model:        trained Voting Regressor model object. 
    -----------

    Warnings:
    ---------
    None
      
       
       
  
    """
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #testing
    global model_names
    
    #exception checking   
    import sys
    
    #checking error for estimator_list (string)
    
    if estimator_list != 'All':
        for i in estimator_list:
            if 'sklearn' not in str(type(i)) and 'CatBoostRegressor' not in str(type(i)):
                sys.exit("(Value Error): estimator_list parameter only accepts 'All' as string or trained model object")
   
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
    
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
        
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    

    
    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+4, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
        
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #general dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold  
    from sklearn.ensemble import VotingRegressor
    import re
    
    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    progress.value += 1
    
    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))

    kf = KFold(fold, random_state=seed)
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Compiling Estimators'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if estimator_list == 'All':

        from sklearn.linear_model import LinearRegression
        from sklearn.linear_model import Ridge
        from sklearn.linear_model import Lasso
        from sklearn.linear_model import ElasticNet
        from sklearn.linear_model import Lars
        from sklearn.linear_model import LassoLars
        from sklearn.linear_model import OrthogonalMatchingPursuit
        from sklearn.linear_model import BayesianRidge
        from sklearn.linear_model import ARDRegression
        from sklearn.linear_model import PassiveAggressiveRegressor
        from sklearn.linear_model import RANSACRegressor
        from sklearn.linear_model import TheilSenRegressor
        from sklearn.linear_model import HuberRegressor
        from sklearn.kernel_ridge import KernelRidge
        from sklearn.svm import SVR
        from sklearn.neighbors import KNeighborsRegressor
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.ensemble import ExtraTreesRegressor
        from sklearn.ensemble import AdaBoostRegressor
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.neural_network import MLPRegressor
        from xgboost import XGBRegressor
        import lightgbm as lgb
        from catboost import CatBoostRegressor

        lr = LinearRegression()
        lasso = Lasso(random_state=seed)
        ridge = Ridge(random_state=seed)
        en = ElasticNet(random_state=seed)
        lar = Lars()
        llar = LassoLars()
        omp = OrthogonalMatchingPursuit()
        br = BayesianRidge()
        ard = ARDRegression()
        par = PassiveAggressiveRegressor(random_state=seed)
        ransac = RANSACRegressor(min_samples=0.5, random_state=seed)
        tr = TheilSenRegressor(random_state=seed)
        huber = HuberRegressor()
        kr = KernelRidge()
        svm = SVR()
        knn = KNeighborsRegressor()
        dt = DecisionTreeRegressor(random_state=seed)
        rf = RandomForestRegressor(random_state=seed)
        et = ExtraTreesRegressor(random_state=seed)
        ada = AdaBoostRegressor(random_state=seed)
        gbr = GradientBoostingRegressor(random_state=seed)
        mlp = MLPRegressor(random_state=seed)
        xgboost = XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0)
        lightgbm = lgb.LGBMRegressor(random_state=seed)
        catboost = CatBoostRegressor(random_state=seed, silent = True)

        progress.value += 1
        
        if turbo:
            
            estimator_list = [lr, lasso, ridge, en, lar, llar, omp, br, par, ransac, tr, huber, 
                             svm, knn, dt, rf, et, ada, gbr, xgboost, lightgbm, catboost]

        else:
            
            estimator_list = [lr, lasso, ridge, en, lar, llar, omp, br, ard, par, ransac, tr, huber, kr, 
                             svm, knn, dt, rf, et, ada, gbr, mlp, xgboost, lightgbm, catboost]
            

    else:

        estimator_list = estimator_list
        
    model_names = []

    for names in estimator_list:

        model_names = np.append(model_names, str(names).split("(")[0])
        
    model_names_fixed = []
    
    for i in model_names:
        if 'CatBoostRegressor' in i:
            model_names_fixed.append('CatBoost Regressor')
        else:
            model_names_fixed.append(i)
        
    model_names = model_names_fixed

    def putSpace(input):
        words = re.findall('[A-Z][a-z]*', input)
        words = ' '.join(words)
        return words  

    model_names_modified = []
    
    for i in model_names:
        
        model_names_modified.append(putSpace(i))
        model_names = model_names_modified
    
    model_names_final = []
  
    for j in model_names_modified:

        if j == 'A R D Regression':
            model_names_final.append('Automatic Relevance Determination')

        elif j == 'M L P Regressor':
            model_names_final.append('MLP Regressor')

        elif j == 'R A N S A C Regressor':
            model_names_final.append('RANSAC Regressor')

        elif j == 'S V R':
            model_names_final.append('Support Vector Regressor')
            
        elif j == 'Lars':
            model_names_final.append('Least Angle Regression')
            
        elif j == 'X G B Regressor':
            model_names_final.append('Extreme Gradient Boosting Regressor')

        elif j == 'L G B M Regressor':
            model_names_final.append('Light Gradient Boosting Machine')
            
        elif j == 'Cat Boost Regressor':
            model_names_final.append('CatBoost Regressor')        
            
        else: 
            model_names_final.append(j)
            
    model_names = model_names_final

    model_names_n = []
    counter = 0
    
    for i in model_names:
        mn = str(i) + '_' + str(counter)
        model_names_n.append(mn)
        counter += 1
        
    model_names = model_names_n

    estimator_list = estimator_list
    
    estimator_list_ = zip(model_names, estimator_list)
    #estimator_list_ = set(estimator_list_) #in order to accomodate catboost set is switched off
    estimator_list_ = list(estimator_list_)

    try:
        model = VotingRegressor(estimators=estimator_list_, n_jobs=-1)
        model.fit(Xtrain,ytrain)
    except:
        model = VotingRegressor(estimators=estimator_list_)
    
    progress.value += 1
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        progress.value += 1
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
    
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]      
        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)
    
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        fold_num += 1
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''
    
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_max_error=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_max_error=np.std(score_max_error)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_max_error)
    avgs_max_error = np.append(avgs_max_error, std_max_error)
    
    
    progress.value += 1
    
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2, 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2, 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)
    
    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Compiling Final Model'
    update_display(monitor, display_id = 'monitor')
    
    model.fit(data_X, data_y)
    
    progress.value += 1
    
    
    #storing into experiment
    model_name = 'Voting Regressor'
    tup = (model_name,model)
    experiment__.append(tup)
    nam = str(model_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    if verbose:
        clear_output()
        display(model_results)
        return model
    
    else:
        clear_output()
        return model



def tune_model(estimator = None, 
               fold = 10, 
               round = 4, 
               n_iter = 10, 
               optimize = 'r2',
               ensemble = False, 
               method = None,
               verbose = True):
    
      
    """
        
    Description:
    ------------
    This function tunes the hyperparameters of a model and scores it using Kfold 
    Cross Validation. The output prints the score grid that shows MAE, MSE, RMSE, 
    R2 and ME by fold (by default = 10 Folds).

    This function returns a trained model object.  

    tune_model() only accepts a string parameter for estimator.

        Example
        -------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        
        tuned_xgboost = tune_model('xgboost') 

        This will tune the hyperparameters of Extreme Gradient Boosting Regressor.

    Parameters
    ----------
    estimator : string, default = None

    Enter abbreviated name of the estimator class. List of estimators supported:

    Estimator                     Abbreviated String    Original Implementation 
    ---------                     ------------------    -----------------------
    Linear Regression             'lr'                  linear_model.LinearRegression
    Lasso Regression              'lasso'               linear_model.Lasso
    Ridge Regression              'ridge'               linear_model.Ridge
    Elastic Net                   'en'                  linear_model.ElasticNet
    Least Angle Regression        'lar'                 linear_model.Lars
    Lasso Least Angle Regression  'llar'                linear_model.LassoLars
    Orthogonal Matching Pursuit   'omp'                 linear_model.OMP
    Bayesian Ridge                'br'                  linear_model.BayesianRidge
    Automatic Relevance Determ.   'ard'                 linear_model.ARDRegression
    Passive Aggressive Regressor  'par'                 linear_model.PAR
    Random Sample Consensus       'ransac'              linear_model.RANSACRegressor
    TheilSen Regressor            'tr'                  linear_model.TheilSenRegressor
    Huber Regressor               'huber'               linear_model.HuberRegressor 
    Kernel Ridge                  'kr'                  kernel_ridge.KernelRidge
    Support Vector Machine        'svm'                 svm.SVR
    K Neighbors Regressor         'knn'                 neighbors.KNeighborsRegressor 
    Decision Tree                 'dt'                  tree.DecisionTreeRegressor
    Random Forest                 'rf'                  ensemble.RandomForestRegressor
    Extra Trees Regressor         'et'                  ensemble.ExtraTreesRegressor
    AdaBoost Regressor            'ada'                 ensemble.AdaBoostRegressor
    Gradient Boosting             'gbr'                 ensemble.GradientBoostingRegressor 
    Multi Level Perceptron        'mlp'                 neural_network.MLPRegressor
    Extreme Gradient Boosting     'xgboost'             xgboost.readthedocs.io
    Light Gradient Boosting       'lightgbm'            github.com/microsoft/LightGBM
    CatBoost Regressor            'catboost'            https://catboost.ai

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to. 

    n_iter: integer, default = 10
    Number of iterations within the Random Grid Search. For every iteration, 
    the model randomly selects one value from the pre-defined grid of hyperparameters.

    optimize: string, default = 'r2'
    Measure used to select the best model through hyperparameter tuning.
    The default scoring measure is 'r2'. Other measures include 'mae', 'mse' and 'me'.

    ensemble: Boolean, default = None
    True enables ensembling of the model through the method defined in 'method' param.

    method: String, 'Bagging' or 'Boosting', default = None
    method comes into effect only when ensemble = True. Default is set to None. 

    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.

    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and 
                  standard deviation of the scores across the folds are also 
                  returned.

    model:        trained model object
    -----------

    Warnings:
    ---------
    - estimator parameter takes an abbreviated string. Passing a trained model object
      returns an error. The tune_model() function internally calls create_model() 
      before tuning the hyperparameters.
        
         
  """
 


    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys
    
    #checking error for estimator (string)
    available_estimators = ['lr', 'lasso', 'ridge', 'en', 'lar', 'llar', 'omp', 'br', 'ard', 'par', 
                            'ransac', 'tr', 'huber', 'kr', 'svm', 'knn', 'dt', 'rf', 'et', 'ada', 'gbr', 
                            'mlp', 'xgboost', 'lightgbm', 'catboost']
    
    if estimator not in available_estimators:
        sys.exit('(Value Error): Estimator Not Available. Please see docstring for list of available estimators.')
        
    #checking error for ensemble:
    if type(ensemble) is not bool:
        sys.exit('(Type Error): Ensemble parameter can only take argument as True or False.') 
    
    #checking error for method:
    
    #1 Check When method given and ensemble is not set to True.
    if ensemble is False and method is not None:
        sys.exit('(Type Error): Method parameter only accepts value when ensemble is set to True.')

    #2 Check when ensemble is set to True and method is not passed.
    if ensemble is True and method is None:
        sys.exit("(Type Error): Method parameter missing. Pass method = 'Bagging' or 'Boosting'.")
        
    #3 Check when ensemble is set to True and method is passed but not allowed.
    available_method = ['Bagging', 'Boosting']
    if ensemble is True and method not in available_method:
        sys.exit("(Value Error): Method parameter only accepts two values 'Bagging' or 'Boosting'.")
        
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking n_iter parameter
    if type(n_iter) is not int:
        sys.exit('(Type Error): n_iter parameter only accepts integer value.')

    #checking optimize parameter
    allowed_optimize = ['mae', 'mse', 'r2', 'me']
    if optimize not in allowed_optimize:
        sys.exit('(Value Error): Optimization method not supported. See docstring for list of available parameters.')
    
    if type(n_iter) is not int:
        sys.exit('(Type Error): n_iter parameter only accepts integer value.')
        
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
    
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    
    #pre-load libraries
    import pandas as pd
    import time, datetime
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=fold+6, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)    
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore')    

    #Storing X_train and y_train in data_X and data_y parameter
    data_X = X_train.copy()
    data_y = y_train.copy()
    
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)

    #define optimizer
      #defining optimizer
    if optimize == 'mae':
        optimize = 'neg_mean_absolute_error'
    elif optimize == 'mse':
        optimize = 'neg_mean_squared_error'
    elif optimize == 'me':
        optimize = 'max_error'
    elif optimize == 'r2':
        optimize = 'r2'
    
    progress.value += 1
    
    
    #general dependencies
    import random
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    from sklearn.model_selection import RandomizedSearchCV
    
    progress.value += 1
    
    kf = KFold(fold, random_state=seed)

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Tuning Hyperparameters'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    #setting turbo parameters
    cv = 3
    
    if estimator == 'lr':

        from sklearn.linear_model import LinearRegression
        param_grid = {'fit_intercept': [True, False],
                     'normalize' : [True, False]
                    }        
        model_grid = RandomizedSearchCV(estimator=LinearRegression(), param_distributions=param_grid, 
                                        scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                        n_jobs=-1, iid=False)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'lasso':

        from sklearn.linear_model import Lasso

        param_grid = {'alpha': [0.0001, 0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                      'fit_intercept': [True, False],
                      'normalize' : [True, False],
                     }
        model_grid = RandomizedSearchCV(estimator=Lasso(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, cv=cv, 
                                        random_state=seed, iid=False,n_jobs=-1)
        
        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'ridge':

        from sklearn.linear_model import Ridge

        param_grid = {"alpha": [0.0001, 0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                      "fit_intercept": [True, False],
                      "normalize": [True, False],
                      }

        model_grid = RandomizedSearchCV(estimator=Ridge(random_state=seed), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       iid=False, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'en':

        from sklearn.linear_model import ElasticNet

        param_grid = {'alpha': [0.0001,0.001,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                      'l1_ratio' : [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'fit_intercept': [True, False],
                      'normalize': [True, False]
                     } 

        model_grid = RandomizedSearchCV(estimator=ElasticNet(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, cv=cv, 
                                        random_state=seed, iid=False, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

    elif estimator == 'lar':

        from sklearn.linear_model import Lars

        param_grid = {'fit_intercept':[True, False],
                     'normalize' : [True, False],
                     'eps': [0.00001, 0.0001, 0.001, 0.01, 0.05, 0.0005, 0.005, 0.00005, 0.02, 0.007]}

        model_grid = RandomizedSearchCV(estimator=Lars(), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_  

    elif estimator == 'llar':

        from sklearn.linear_model import LassoLars

        param_grid = {'alpha': [0.0001,0.001,0.1,0.15,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                     'fit_intercept':[True, False],
                     'normalize' : [True, False],
                     'eps': [0.00001, 0.0001, 0.001, 0.01, 0.05, 0.0005, 0.005, 0.00005, 0.02, 0.007]}

        model_grid = RandomizedSearchCV(estimator=LassoLars(), param_distributions=param_grid,
                                       scoring=optimize, n_iter=n_iter, cv=cv, random_state=seed,
                                       n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'omp':

        from sklearn.linear_model import OrthogonalMatchingPursuit
        import random

        param_grid = {'n_nonzero_coefs': range(1,len(X_train.columns)+1),
                      'fit_intercept' : [True, False],
                      'normalize': [True, False]}

        model_grid = RandomizedSearchCV(estimator=OrthogonalMatchingPursuit(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_        

    elif estimator == 'br':

        from sklearn.linear_model import BayesianRidge

        param_grid = {'alpha_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'alpha_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'lambda_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'lambda_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'compute_score': [True, False],
                      'fit_intercept': [True, False],
                      'normalize': [True, False]
                     }    

        model_grid = RandomizedSearchCV(estimator=BayesianRidge(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'ard':

        from sklearn.linear_model import ARDRegression

        param_grid = {'alpha_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'alpha_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'lambda_1': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'lambda_2': [0.0000001, 0.000001, 0.0001, 0.001, 0.01, 0.0005, 0.005, 0.05, 0.1, 0.15, 0.2, 0.3],
                      'threshold_lambda' : [5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000],
                      'compute_score': [True, False],
                      'fit_intercept': [True, False],
                      'normalize': [True, False]
                     }    

        model_grid = RandomizedSearchCV(estimator=ARDRegression(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'par':

        from sklearn.linear_model import PassiveAggressiveRegressor

        param_grid = {'C': [0.01, 0.005, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'fit_intercept': [True, False],
                      'early_stopping' : [True, False],
                      #'validation_fraction': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'loss' : ['epsilon_insensitive', 'squared_epsilon_insensitive'],
                      'epsilon' : [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                      'shuffle' : [True, False]
                     }    

        model_grid = RandomizedSearchCV(estimator=PassiveAggressiveRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'ransac':

        from sklearn.linear_model import RANSACRegressor

        param_grid = {'min_samples': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'max_trials': [1,2,3,4,5,6,7,8,9,10],
                      'max_skips': [1,2,3,4,5,6,7,8,9,10],
                      'stop_n_inliers': [1,2,3,4,5,6,7,8,9,10],
                      'stop_probability': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'loss' : ['absolute_loss', 'squared_loss'],
                     }    

        model_grid = RandomizedSearchCV(estimator=RANSACRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'tr':

        from sklearn.linear_model import TheilSenRegressor

        param_grid = {'fit_intercept': [True, False],
                      'max_subpopulation': [5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000]
                     }    

        model_grid = RandomizedSearchCV(estimator=TheilSenRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    

    elif estimator == 'huber':

        from sklearn.linear_model import HuberRegressor

        param_grid = {'epsilon': [1.1, 1.2, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9],
                      'alpha': [0.00001, 0.0001, 0.0003, 0.005, 0.05, 0.1, 0.0005, 0.15],
                      'fit_intercept' : [True, False]
                     }    

        model_grid = RandomizedSearchCV(estimator=HuberRegressor(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_        

    elif estimator == 'kr':

        from sklearn.kernel_ridge import KernelRidge

        param_grid = {'alpha': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1] }    

        model_grid = RandomizedSearchCV(estimator=KernelRidge(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'svm':

        from sklearn.svm import SVR

        param_grid = {#'kernel': ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed'],
                      #'float' : [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                      'C' : [0.01, 0.005, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                      'epsilon' : [1.1, 1.2, 1.3, 1.35, 1.4, 1.5, 1.55, 1.6, 1.7, 1.8, 1.9],
                      'shrinking': [True, False]
                     }    

        model_grid = RandomizedSearchCV(estimator=SVR(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_     

    elif estimator == 'knn':

        from sklearn.neighbors import KNeighborsRegressor

        param_grid = {'n_neighbors': range(1,51),
                     'weights' :  ['uniform', 'distance'],
                     'algorithm': ['ball_tree', 'kd_tree', 'brute'],
                     'leaf_size': [10,20,30,40,50,60,70,80,90]
                     } 

        model_grid = RandomizedSearchCV(estimator=KNeighborsRegressor(), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'dt':

        from sklearn.tree import DecisionTreeRegressor

        param_grid = {"max_depth": np.random.randint(3, (len(X_train.columns)*.85),4),
                      "max_features": np.random.randint(3, len(X_train.columns),4),
                      "min_samples_leaf": [0.1,0.2,0.3,0.4,0.5],
                      "min_samples_split" : [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                      "min_weight_fraction_leaf" : [0.1,0.2,0.3,0.4,0.5],
                      "min_impurity_decrease" : [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                      "criterion": ["mse", "mae", "friedman_mse"],
                      #"max_leaf_nodes" : [1,2,3,4,5,6,7,8,9,10,None]
                     } 

        model_grid = RandomizedSearchCV(estimator=DecisionTreeRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'rf':

        from sklearn.ensemble import RandomForestRegressor


        param_grid = {'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                      'criterion': ['mse', 'mae'],
                      'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                      'min_samples_split': [2, 5, 7, 9, 10],
                      'min_samples_leaf' : [1, 2, 4],
                      'max_features' : ['auto', 'sqrt', 'log2'],
                      'bootstrap': [True, False]
                      }

        model_grid = RandomizedSearchCV(estimator=RandomForestRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       


    elif estimator == 'et':

        from sklearn.ensemble import ExtraTreesRegressor

        param_grid = {'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                      'criterion': ['mse', 'mae'],
                      'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                      'min_samples_split': [2, 5, 7, 9, 10],
                      'min_samples_leaf' : [1, 2, 4],
                      'max_features' : ['auto', 'sqrt', 'log2'],
                      'bootstrap': [True, False]
                      }  

        model_grid = RandomizedSearchCV(estimator=ExtraTreesRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_       

    elif estimator == 'ada':

        from sklearn.ensemble import AdaBoostRegressor

        param_grid = {'n_estimators': [10, 40, 70, 80, 90, 100, 120, 140, 150],
                      'learning_rate': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                      'loss' : ["linear", "square", "exponential"]
                     }    

        model_grid = RandomizedSearchCV(estimator=AdaBoostRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_ 

    elif estimator == 'gbr':

        from sklearn.ensemble import GradientBoostingRegressor

        param_grid = {'loss': ['ls', 'lad', 'huber', 'quantile'],
                      'n_estimators': [10, 40, 70, 80, 90, 100, 120, 140, 150],
                      'learning_rate': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                      'subsample' : [0.1,0.3,0.5,0.7,0.9,1],
                      'criterion' : ['friedman_mse', 'mse', 'mae'],
                      'min_samples_split' : [2,4,5,7,9,10],
                      'min_samples_leaf' : [1,2,3,4,5],
                      'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                      'max_features' : ['auto', 'sqrt', 'log2']
                     }     

        model_grid = RandomizedSearchCV(estimator=GradientBoostingRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_         

    elif estimator == 'mlp':

        from sklearn.neural_network import MLPRegressor

        param_grid = {'learning_rate': ['constant', 'invscaling', 'adaptive'],
                      'solver' : ['lbfgs', 'adam'],
                      'alpha': [0.0001, 0.001, 0.01, 0.00001, 0.003, 0.0003, 0.0005, 0.005, 0.05],
                      'hidden_layer_sizes': np.random.randint(50,150,10),
                      'activation': ["tanh", "identity", "logistic","relu"]
                      }    

        model_grid = RandomizedSearchCV(estimator=MLPRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)    

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   
        
        
    elif estimator == 'xgboost':
        
        from xgboost import XGBRegressor
        
        param_grid = {'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], 
                      'n_estimators':[10, 30, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000], 
                      'subsample': [0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1],
                      'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)], 
                      'colsample_bytree': [0.5, 0.7, 0.9, 1],
                      'min_child_weight': [1, 2, 3, 4]
                     }

        model_grid = RandomizedSearchCV(estimator=XGBRegressor(random_state=seed, n_jobs=-1, verbosity=0), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   
        
        
    elif estimator == 'lightgbm':
        
        import lightgbm as lgb
        
        param_grid = {#'boosting_type' : ['gbdt', 'dart', 'goss', 'rf'],
                      'num_leaves': [10,20,30,40,50,60,70,80,90,100,150,200],
                      'max_depth': [int(x) for x in np.linspace(10, 110, num = 11)],
                      'learning_rate': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                      'n_estimators': [10, 30, 50, 70, 90, 100, 120, 150, 170, 200], 
                      'min_split_gain' : [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                      'reg_alpha': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                      'reg_lambda': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                     }
            
        model_grid = RandomizedSearchCV(estimator=lgb.LGBMRegressor(random_state=seed), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_   

    elif estimator == 'catboost':
        
        from catboost import CatBoostRegressor
        
        param_grid = {'depth':[3,1,2,6,4,5,7,8,9,10],
                      'iterations':[250,100,500,1000], 
                      'learning_rate':[0.03,0.001,0.01,0.1,0.2,0.3], 
                      'l2_leaf_reg':[3,1,5,10,100], 
                      'border_count':[32,5,10,20,50,100,200], 
                      #'ctr_border_count':[50,5,10,20,100,200]
                      }
            
        model_grid = RandomizedSearchCV(estimator=CatBoostRegressor(random_state=seed, silent=True), 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=cv, random_state=seed, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_ 
    
    progress.value += 1
    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Tuning Hyperparameters of Ensemble'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    if estimator == 'dt' and ensemble == True and method == 'Bagging':
    
    #when using normal BaggingRegressor() DT estimator raise's an exception for max_features parameter. Hence a separate 
    #call has been made for estimator='dt' and method = 'Bagging' where max_features has been removed from param_grid_dt.
    
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.ensemble import BaggingRegressor

        param_grid = {'n_estimators': [10,15,20,25,30],
                     'max_samples': [0.3,0.5,0.6,0.7,0.8,0.9],
                     'max_features':[0.3,0.5,0.6,0.7,0.8,0.9],
                     'bootstrap': [True, False],
                     'bootstrap_features': [True, False],
                     }

        param_grid_dt = {"max_depth": np.random.randint(3, (len(X_train.columns)*.85),4),
                         "min_samples_leaf": [2,3,4],
                         "min_samples_leaf": [0.1,0.2,0.3,0.4,0.5],
                         "min_samples_split" : [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                         "min_weight_fraction_leaf" : [0.1,0.2,0.3,0.4,0.5],
                         "min_impurity_decrease" : [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9],
                         "criterion": ["mse", "mae", "friedman_mse"]}


        model_grid = RandomizedSearchCV(estimator=DecisionTreeRegressor(random_state=seed), param_distributions=param_grid_dt,
                                       scoring=optimize, n_iter=n_iter, cv=fold, random_state=seed,
                                       iid=False, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_

        best_model = BaggingRegressor(best_model, random_state=seed)

        model_grid = RandomizedSearchCV(estimator=best_model, 
                                        param_distributions=param_grid, n_iter=n_iter, 
                                        cv=fold, random_state=seed, iid=False, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    
  
    elif ensemble and method == 'Bagging':
    
        from sklearn.ensemble import BaggingRegressor

        param_grid = {'n_estimators': [10,15,20,25,30],
                     'max_samples': [0.3,0.5,0.6,0.7,0.8,0.9],
                     'max_features':[0.3,0.5,0.6,0.7,0.8,0.9],
                     'bootstrap': [True, False],
                     'bootstrap_features': [True, False],
                     }

        best_model = BaggingRegressor(best_model, random_state=seed)

        model_grid = RandomizedSearchCV(estimator=best_model, 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=fold, random_state=seed, iid=False, n_jobs=-1)

        model_grid.fit(X_train,y_train)
        model = model_grid.best_estimator_
        best_model = model_grid.best_estimator_
        best_model_param = model_grid.best_params_    
  
      
    elif ensemble and method =='Boosting':
    
        from sklearn.ensemble import AdaBoostRegressor

        param_grid = {'n_estimators': [10, 40, 70, 80, 90, 100, 120, 140, 150],
                      'learning_rate': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1],
                      'loss' : ["linear", "square", "exponential"]
                     }          

        best_model = AdaBoostRegressor(best_model, random_state=seed)

        model_grid = RandomizedSearchCV(estimator=best_model, 
                                        param_distributions=param_grid, scoring=optimize, n_iter=n_iter, 
                                        cv=fold, random_state=seed, iid=False, n_jobs=-1)
    
    
   
    progress.value += 1

    
    '''
    MONITOR UPDATE STARTS
    '''
    
    monitor.iloc[1,1:] = 'Initializing CV'
    update_display(monitor, display_id = 'monitor')
    
    '''
    MONITOR UPDATE ENDS
    '''
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        t0 = time.time()
        
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]  
        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)
            
        progress.value += 1
            
            
        '''
        
        This section is created to update_display() as code loops through the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        '''
        
        TIME CALCULATION SUB-SECTION STARTS HERE
        
        '''
        
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        update_display(ETC, display_id = 'ETC')
            
        fold_num += 1
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
       
        '''
        
        TIME CALCULATION ENDS HERE
        
        '''
        
        if verbose:
            update_display(master_display, display_id = display_id)
        
        '''
        
        Update_display() ends here
        
        '''
        
    progress.value += 1
    
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_me=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_me=np.std(score_max_error)

    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_me)
    avgs_max_error = np.append(avgs_max_error, std_me)
    

    progress.value += 1
    
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2 , 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2, 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])

    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)

    progress.value += 1
    
    #refitting the model on complete X_train, y_train
    monitor.iloc[1,1:] = 'Compiling Final Model'
    update_display(monitor, display_id = 'monitor')
    
    best_model.fit(data_X, data_y)
    
    progress.value += 1
    
    
    #storing into experiment
    model_name = 'Tuned ' + str(model).split("(")[0]
    tup = (model_name,best_model)
    experiment__.append(tup)
    nam = str(model_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    
    if verbose:
        clear_output()
        display(model_results)
        return best_model
    else:
        clear_output()
        return best_model



def stack_models(estimator_list, 
                 meta_model = None, 
                 fold = 10,
                 round = 4, 
                 restack = False, 
                 plot = False,
                 finalize = False,
                 verbose = True):
    
    """
      
            
    Description:
    ------------
    This function creates a meta model and scores it using Kfold Cross Validation.
    The predictions from the base level models as passed in the estimator_list param 
    are used as input features for the meta model. The restacking parameter controls
    the ability to expose raw features to the meta model when set to True
    (default = False).

    The output prints a score grid that shows MAE, MSE, RMSE, R2 and ME by fold 
    (default = 10 Folds).
    
    This function returns a container which is the list of all models in stacking. 

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        dt = create_model('dt')
        rf = create_model('rf')
        ada = create_model('ada')
        ridge = create_model('ridge')
        knn = create_model('knn')

        stacked_models = stack_models(estimator_list=[dt,rf,ada,ridge,knn])

        This will create a meta model that will use the predictions of all the 
        models provided in estimator_list param. By default, the meta model is 
        Linear Regression but can be changed with meta_model param.

    Parameters
    ----------
    estimator_list : list of object

    meta_model : object, default = None
    if set to None, Linear Regression is used as a meta model.

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to.

    restack: Boolean, default = False
    When restack is set to True, raw data will be exposed to meta model when
    making predictions, otherwise when False, only the predicted label is passed 
    to meta model when making final predictions.

    plot: Boolean, default = False
    When plot is set to True, it will return the correlation plot of prediction
    from all base models provided in estimator_list.
    
    finalize: Boolean, default = False
    When finalize is set to True, it will fit the stacker on entire dataset
    including the hold-out sample created during the setup() stage. It is not 
    recommended to set this to True here, If you would like to fit the stacker 
    on the entire dataset including the hold-out, use finalize_model().
    
    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.

    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and
                  standard deviation of the scores across the folds are also 
                  returned.

    container:    list of all the models where last element is meta model.
    ----------

    Warnings:
    ---------
    None
      
             
          
    """
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #exception checking   
    import sys
    
    #checking error for estimator_list
    for i in estimator_list:
        if 'sklearn' not in str(type(i)) and 'CatBoostRegressor' not in str(type(i)):
            sys.exit("(Value Error): estimator_list parameter only trained model object")
            
    #checking meta model
    if meta_model is not None:
        if 'sklearn' not in str(type(meta_model)) and 'CatBoostRegressor' not in str(type(meta_model)):
            sys.exit("(Value Error): estimator_list parameter only trained model object")
    
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')

    #checking restack parameter
    if type(restack) is not bool:
        sys.exit('(Type Error): Restack parameter can only take argument as True or False.')    
    
    #checking plot parameter
    if type(restack) is not bool:
        sys.exit('(Type Error): Plot parameter can only take argument as True or False.')  
        
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
        
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    #testing
    #no active tests
    
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import time, datetime
    
    #progress bar
    max_progress = len(estimator_list) + fold + 4
    progress = ipw.IntProgress(value=0, min=0, max=max_progress, step=1 , description='Processing: ')
    master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
        
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_predict
    import seaborn as sns
    
    progress.value += 1
    
    #Defining meta model. Linear Regression hardcoded for now
    if meta_model == None:
        from sklearn.linear_model import LinearRegression
        meta_model = LinearRegression()
    else:
        meta_model = meta_model
    
    #defining data_X and data_y
    if finalize:
        data_X = X.copy()
        data_y = y.copy()
    else:       
        data_X = X_train.copy()
        data_y = y_train.copy()

    #reset index
    data_X.reset_index(drop=True,inplace=True)
    data_y.reset_index(drop=True,inplace=True)
    
    #models_ for appending
    models_ = []
    
    #defining model_library model names
    model_names = np.zeros(0)
    for item in estimator_list:
        model_names = np.append(model_names, str(item).split("(")[0])
    
    model_names_fixed = []
    
    for i in model_names:
        if 'CatBoostRegressor' in i:
            a = 'CatBoostRegressor'
            model_names_fixed.append(a)
        else:
            model_names_fixed.append(i)
            
    model_names = model_names_fixed
    
    model_names_fixed = []
    
    counter = 0
    for i in model_names:
        s = str(i) + '_' + str(counter)
        model_names_fixed.append(s)
        counter += 1
    
    base_array = np.zeros((0,0))
    base_prediction = pd.DataFrame(data_y) #changed to data_y
    base_prediction = base_prediction.reset_index(drop=True)
    
    counter = 0
    
    for model in estimator_list:
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[1,1:] = 'Evaluating ' + model_names[counter]
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        #fitting and appending
        model.fit(data_X, data_y)
        models_.append(model)
        
        progress.value += 1
        
        base_array = cross_val_predict(model,data_X,data_y,cv=fold, method='predict')
        base_array_df = pd.DataFrame(base_array)
        base_prediction = pd.concat([base_prediction,base_array_df],axis=1)
        base_array = np.empty((0,0))
        
        counter += 1
    
    #defining column names now
    target_col_name = np.array(base_prediction.columns[0])
    model_names = np.append(target_col_name, model_names_fixed) #adding fixed column names now
    base_prediction.columns = model_names #defining colum names now
    
    #defining data_X and data_y dataframe to be used in next stage.
    
    #drop column from base_prediction
    base_prediction.drop(base_prediction.columns[0],axis=1,inplace=True)
    
    if restack:
        data_X = pd.concat([data_X, base_prediction], axis=1)
        
    else:
        data_X = base_prediction
        
    #data_y = base_prediction[base_prediction.columns[0]]
    
    #Correlation matrix of base_prediction
    base_prediction_cor = base_prediction.drop(base_prediction.columns[0],axis=1)
    base_prediction_cor = base_prediction_cor.corr()
    
    #Meta Modeling Starts Here
    
    model = meta_model #this defines model to be used below as model = meta_model (as captured above)
    
    #appending in models
    model.fit(data_X, data_y)
    models_.append(model)
    
    kf = KFold(fold, random_state=seed) #capturing fold requested by user

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))  
    
    progress.value += 1
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Meta Model Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        progress.value += 1
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]

        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)
        
        
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_]}).round(round)
        master_display = pd.concat([master_display, fold_results],ignore_index=True)
        fold_results = []
        
        
        '''
        
        TIME CALCULATION SUB-SECTION STARTS HERE
        
        '''
        
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        #update_display(ETC, display_id = 'ETC')
            
        fold_num += 1
        
        
        '''
        
        TIME CALCULATION ENDS HERE
        
        '''
        
        if verbose:
            update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''
     
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_max_error=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_max_error=np.std(score_max_error)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_max_error)
    avgs_max_error = np.append(avgs_max_error, std_max_error)
      
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2 , 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2, 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])
  
    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)  
    
    progress.value += 1
    
    #appending method into models_
    models_.append(restack)
    
    #storing into experiment
    model_name = 'Stacking Regressor (Single Layer)'
    tup = (model_name,models_)
    experiment__.append(tup)
    nam = str(model_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    if plot:
        clear_output()
        ax = sns.heatmap(base_prediction_cor, vmin=1, vmax=1, center=0,cmap='magma', square=True, annot=True, 
                         linewidths=1)
    
    if verbose:
        clear_output()
        display(model_results)
        return models_
    else:
        clear_output()
        return models_



def create_stacknet(estimator_list,
                    meta_model = None,
                    fold = 10,
                    round = 4,
                    restack = False,
                    finalize = False,
                    verbose = True):
    
    """
         
    Description:
    ------------
    This function creates a sequential stack net using cross validated predictions 
    at each layer. The final score grid contains predictions from the meta model 
    using Kfold Cross Validation. Base level models can be passed as estimator_list
    param, the layers can be organized as a sub list within the estimator_list object.  
    Restacking param controls the ability to expose raw features to meta model.

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        dt = create_model('dt')
        rf = create_model('rf')
        ada = create_model('ada')
        ridge = create_model('ridge')
        knn = create_model('knn')

        stacknet = create_stacknet(estimator_list =[[dt,rf],[ada,ridge,knn]])

        This will result in the stacking of models in multiple layers. The first layer 
        contains dt and rf, the predictions of which are used by models in the second 
        layer to generate predictions which are then used by the meta model to generate
        final predictions. By default, the meta model is Linear Regression but can be 
        changed with meta_model param.

    Parameters
    ----------
    estimator_list : nested list of objects

    meta_model : object, default = None
    if set to None, Linear Regression is used as a meta model.

    fold: integer, default = 10
    Number of folds to be used in Kfold CV. Must be at least 2. 

    round: integer, default = 4
    Number of decimal places the metrics in the score grid will be rounded to.
  
    restack: Boolean, default = False
    When restack is set to True, raw data and prediction of all layers will be 
    exposed to the meta model when making predictions. When set to False, only 
    the predicted label of last layer is passed to meta model when making final 
    predictions.
    
    finalize: Boolean, default = False
    When finalize is set to True, it will fit the stacker on entire dataset
    including the hold-out sample created during the setup() stage. It is not 
    recommended to set this to True here, if you would like to fit the stacker 
    on the entire dataset including the hold-out, use finalize_model().
    
    verbose: Boolean, default = True
    Score grid is not printed when verbose is set to False.

    Returns:
    --------

    score grid:   A table containing the scores of the model across the kfolds. 
    -----------   Scoring metrics used are MAE, MSE, RMSE, R2 and ME. Mean and 
                  standard deviation of the scores across the folds are also 
                  returned.

    container:    list of all models where the last element is the meta model.
    ----------

    Warnings:
    ---------    
    None
      
      
    
    """

    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #for checking only
    #No active test
    
    #exception checking   
    import sys
    
    #checking error for estimator_list
    for i in estimator_list:
        for j in i:
            if 'sklearn' not in str(type(j)) and 'CatBoostRegressor' not in str(type(j)):
                sys.exit("(Value Error): estimator_list parameter only trained model object")
            
    #checking meta model
    if meta_model is not None:
        if 'sklearn' not in str(type(meta_model)) and 'CatBoostRegressor' not in str(type(meta_model)):
            sys.exit("(Value Error): estimator_list parameter only trained model object")
    
    #checking fold parameter
    if type(fold) is not int:
        sys.exit('(Type Error): Fold parameter only accepts integer value.')
    
    #checking round parameter
    if type(round) is not int:
        sys.exit('(Type Error): Round parameter only accepts integer value.')
 
    #checking restack parameter
    if type(restack) is not bool:
        sys.exit('(Type Error): Restack parameter can only take argument as True or False.')    
    
    #checking verbose parameter
    if type(verbose) is not bool:
        sys.exit('(Type Error): Verbose parameter can only take argument as True or False.') 
        
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    import time, datetime
    
    #progress bar
    max_progress = len(estimator_list) + fold + 4
    progress = ipw.IntProgress(value=0, min=0, max=max_progress, step=1 , description='Processing: ')
    display(progress)
    
    #display monitor
    timestampStr = datetime.datetime.now().strftime("%H:%M:%S")
    monitor = pd.DataFrame( [ ['Initiated' , '. . . . . . . . . . . . . . . . . .', timestampStr ], 
                             ['Status' , '. . . . . . . . . . . . . . . . . .' , 'Loading Dependencies' ],
                             ['ETC' , '. . . . . . . . . . . . . . . . . .',  'Calculating ETC'] ],
                              columns=['', ' ', '   ']).set_index('')
    
    display(monitor, display_id = 'monitor')
    
    if verbose:
        master_display = pd.DataFrame(columns=['MAE','MSE','RMSE', 'R2', 'ME'])
        display_ = display(master_display, display_id=True)
        display_id = display_.display_id
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #general dependencies
    import numpy as np
    from sklearn import metrics
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_predict
    
    #models_ list
    models_ = []

    progress.value += 1
    
    base_level = estimator_list[0]
    base_level_names = []
    
    #defining base_level_names
    for item in base_level:
            base_level_names = np.append(base_level_names, str(item).split("(")[0])

    base_level_fixed = []
    
    for i in base_level_names:
        if 'CatBoostRegressor' in i:
            a = 'CatBoostRegressor'
            base_level_fixed.append(a)
    else:
        base_level_fixed.append(i)
    
    base_level_names = base_level_fixed
    
    base_level_fixed_2 = []
    
    counter = 0
    for i in base_level_names:
        s = str(i) + '_' + 'BaseLevel_' + str(counter)
        base_level_fixed_2.append(s)
        counter += 1
    
    base_level_fixed = base_level_fixed_2
    
    inter_level = estimator_list[1:]
    inter_level_names = []
    
    #defining inter_level names
    for item in inter_level:
        for m in item:
            inter_level_names = np.append(inter_level_names, str(m).split("(")[0])    
            
    #defining inter_level names
    for item in inter_level:
        for m in item:
            inter_level_names = np.append(inter_level_names, str(m).split("(")[0])  
            
    #defining data_X and data_y
    if finalize:
        data_X = X.copy()
        data_y = y.copy()
    else:       
        data_X = X_train.copy()
        data_y = y_train.copy()
        
    #reset index
    data_X.reset_index(drop=True, inplace=True)
    data_y.reset_index(drop=True, inplace=True)
    
    #defining meta model
    
    if meta_model == None:
        from sklearn.linear_model import LinearRegression
        meta_model = LinearRegression()
    else:
        meta_model = meta_model
        
    base_array = np.zeros((0,0))
    base_array_df = pd.DataFrame()
    base_prediction = pd.DataFrame(data_y) #changed to data_y
    base_prediction = base_prediction.reset_index(drop=True)
    
    base_counter = 0
    
    base_models_ = []

    for model in base_level:
        
        base_models_.append(model.fit(data_X,data_y)) #changed to data_X and data_y
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[1,1:] = 'Evaluating ' + base_level_names[base_counter]
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        progress.value += 1
                     
        base_array = cross_val_predict(model,data_X,data_y,cv=fold, method='predict')
        base_array = base_array
        base_array = pd.DataFrame(base_array)
        base_array_df = pd.concat([base_array_df, base_array], axis=1)
        base_array = np.empty((0,0))
        
        base_counter += 1
        
    base_array_df.columns = base_level_fixed
    
    if restack:
        base_array_df = pd.concat([data_X,base_array_df], axis=1)
        
    early_break = base_array_df.copy()
    
    models_.append(base_models_)
    
    inter_counter = 0
    
    for level in inter_level:
        inter_inner = []
        model_counter = 0
        inter_array_df = pd.DataFrame()
        
        for model in level:
            
            '''
            MONITOR UPDATE STARTS
            '''

            monitor.iloc[1,1:] = 'Evaluating ' + inter_level_names[inter_counter]
            update_display(monitor, display_id = 'monitor')

            '''
            MONITOR UPDATE ENDS
            '''
            
            model = model.fit(X = base_array_df, y = data_y) #changed to data_y
            inter_inner.append(model)
            
            base_array = cross_val_predict(model,X = base_array_df, y = data_y,cv=fold, method='predict')
            base_array = pd.DataFrame(base_array)
            
            """
            defining columns
            """
            
            col = str(model).split("(")[0]
            if 'CatBoostRegressor' in col:
                col = 'CatBoostRegressor'
            col = col + '_InterLevel_' + str(inter_counter) + '_' + str(model_counter)
            base_array.columns = [col]
            
            """
            defining columns end here
            """
            
            inter_array_df = pd.concat([inter_array_df, base_array], axis=1)
            base_array = np.empty((0,0))
            
            model_counter += 1
    
        base_array_df = pd.concat([base_array_df,inter_array_df], axis=1)
            
        models_.append(inter_inner)
    
        if restack == False:
            i = base_array_df.shape[1] - len(level)
            base_array_df = base_array_df.iloc[:,i:]
        
        inter_counter += 1
    
    model = meta_model
    
    #redefine data_X and data_y
    data_X = base_array_df.copy()
    
    
    meta_model_ = model.fit(data_X,data_y)
    
    kf = KFold(fold, random_state=seed) #capturing fold requested by user

    score_mae =np.empty((0,0))
    score_mse =np.empty((0,0))
    score_rmse =np.empty((0,0))
    score_r2 =np.empty((0,0))
    score_max_error =np.empty((0,0))
    avgs_mae =np.empty((0,0))
    avgs_mse =np.empty((0,0))
    avgs_rmse =np.empty((0,0))
    avgs_r2 =np.empty((0,0))
    avgs_max_error =np.empty((0,0))  
    
    fold_num = 1
    
    for train_i , test_i in kf.split(data_X,data_y):
        
        t0 = time.time()
        
        '''
        MONITOR UPDATE STARTS
        '''
    
        monitor.iloc[1,1:] = 'Fitting Meta Model Fold ' + str(fold_num) + ' of ' + str(fold)
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        Xtrain,Xtest = data_X.iloc[train_i], data_X.iloc[test_i]
        ytrain,ytest = data_y.iloc[train_i], data_y.iloc[test_i]
        
        model.fit(Xtrain,ytrain)
        pred_ = model.predict(Xtest)
        mae = metrics.mean_absolute_error(ytest,pred_)
        mse = metrics.mean_squared_error(ytest,pred_)
        rmse = np.sqrt(mse)
        r2 = metrics.r2_score(ytest,pred_)
        max_error_ = metrics.max_error(ytest,pred_)
        score_mae = np.append(score_mae,mae)
        score_mse = np.append(score_mse,mse)
        score_rmse = np.append(score_rmse,rmse)
        score_r2 =np.append(score_r2,r2)
        score_max_error = np.append(score_max_error,max_error_)

        progress.value += 1
        
        '''
        
        This section handles time calculation and is created to update_display() as code loops through 
        the fold defined.
        
        '''
        
        fold_results = pd.DataFrame({'MAE':[mae], 'MSE': [mse], 'RMSE': [rmse], 
                                     'R2': [r2], 'ME': [max_error_]}).round(round)
        
        if verbose:
            master_display = pd.concat([master_display, fold_results],ignore_index=True)
        
        fold_results = []
        
        '''
        TIME CALCULATION SUB-SECTION STARTS HERE
        '''
        t1 = time.time()
        
        tt = (t1 - t0) * (fold-fold_num) / 60
        tt = np.around(tt, 2)
        
        if tt < 1:
            tt = str(np.around((tt * 60), 2))
            ETC = tt + ' Seconds Remaining'
                
        else:
            tt = str (tt)
            ETC = tt + ' Minutes Remaining'
            
        fold_num += 1
        
        '''
        MONITOR UPDATE STARTS
        '''

        monitor.iloc[2,1:] = ETC
        update_display(monitor, display_id = 'monitor')

        '''
        MONITOR UPDATE ENDS
        '''
        
        '''
        TIME CALCULATION ENDS HERE
        '''
        
        if verbose:
            update_display(master_display, display_id = display_id)
            
        
        '''
        
        Update_display() ends here
        
        '''
    
    mean_mae=np.mean(score_mae)
    mean_mse=np.mean(score_mse)
    mean_rmse=np.mean(score_rmse)
    mean_r2=np.mean(score_r2)
    mean_max_error=np.mean(score_max_error)
    std_mae=np.std(score_mae)
    std_mse=np.std(score_mse)
    std_rmse=np.std(score_rmse)
    std_r2=np.std(score_r2)
    std_max_error=np.std(score_max_error)
    
    avgs_mae = np.append(avgs_mae, mean_mae)
    avgs_mae = np.append(avgs_mae, std_mae) 
    avgs_mse = np.append(avgs_mse, mean_mse)
    avgs_mse = np.append(avgs_mse, std_mse)
    avgs_rmse = np.append(avgs_rmse, mean_rmse)
    avgs_rmse = np.append(avgs_rmse, std_rmse)
    avgs_r2 = np.append(avgs_r2, mean_r2)
    avgs_r2 = np.append(avgs_r2, std_r2)
    avgs_max_error = np.append(avgs_max_error, mean_max_error)
    avgs_max_error = np.append(avgs_max_error, std_max_error)
      
    model_results = pd.DataFrame({'MAE': score_mae, 'MSE': score_mse, 'RMSE' : score_rmse, 'R2' : score_r2 , 
                     'ME' : score_max_error})
    model_avgs = pd.DataFrame({'MAE': avgs_mae, 'MSE': avgs_mse, 'RMSE' : avgs_rmse, 'R2' : avgs_r2, 
                     'ME' : avgs_max_error},index=['Mean', 'SD'])
  
    model_results = model_results.append(model_avgs)
    model_results = model_results.round(round)      
    
    progress.value += 1
        
    #appending meta_model into models_
    models_.append(meta_model_)
    
    #appending restack param
    models_.append(restack)
    
    #storing into experiment
    model_name = 'Stacking Regressor (Multi Layer)'
    tup = (model_name,models_)
    experiment__.append(tup)
    nam = str(model_name) + ' Score Grid'
    tup = (nam, model_results)
    experiment__.append(tup)
    
    if verbose:
        clear_output()
        display(model_results)
        return models_
    
    else:
        clear_output()
        return models_ 


def plot_model(estimator, 
               plot = 'residuals'): 
    
    
    """
          
    Description:
    ------------
    This function takes a trained model object and returns a plot based on the
    test / hold-out set. The process may require the model to be re-trained in
    certain cases. See list of plots supported below. 
    
    Model must be created using create_model() or tune_model().

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        plot_model(lr)

        This will return an residuals plot of a trained Linear Regression model.

    Parameters
    ----------
    estimator : object, default = none
    A trained model object should be passed as an estimator. 
   
    plot : string, default = residual
    Enter abbreviation of type of plot. The current list of plots supported are:

    Name                        Abbreviated String     Original Implementation 
    ---------                   ------------------     -----------------------
    Residuals Plot               'residuals'           .. / residuals.html
    Prediction Error Plot        'error'               .. / peplot.html
    Cooks Distance Plot          'cooks'               .. / influence.html
    Recursive Feat. Selection    'rfe'                 .. / rfecv.html
    Learning Curve               'learning'            .. / learning_curve.html
    Validation Curve             'vc'                  .. / validation_curve.html
    Manifold Learning            'manifold'            .. / manifold.html
    Feature Importance           'feature'                   N/A 
    Model Hyperparameter         'parameter'                 N/A 

    ** https://www.scikit-yb.org/en/latest/api/regressor/<reference>

    Returns:
    --------

    Visual Plot:  Prints the visual plot. 
    ------------

    Warnings:
    ---------
    None
      
                
    """  
    
    
    '''
    
    ERROR HANDLING STARTS HERE
    
    '''
    
    #for testing
    #No active testing
    
    #exception checking   
    import sys
    
    #checking plots (string)
    available_plots = ['residuals', 'error', 'cooks', 'feature', 'parameter', 'rfe', 'learning', 'manifold', 'vc']
    
    if plot not in available_plots:
        sys.exit('(Value Error): Plot Not Available. Please see docstring for list of available Plots.')

    #exception for CatBoost
    if 'CatBoostRegressor' in str(type(estimator)):
        sys.exit('(Estimator Error): CatBoost estimator is not compatible with plot_model function, try using Catboost with interpret_model instead.')
        
    #checking for feature plot
    if not ( hasattr(estimator, 'coef_') or hasattr(estimator,'feature_importances_') ) and (plot == 'feature' or plot == 'rfe'):
        sys.exit('(Type Error): Feature Importance plot not available for estimators with coef_ attribute.')
    
    '''
    
    ERROR HANDLING ENDS HERE
    
    '''
    
    #pre-load libraries
    import pandas as pd
    import ipywidgets as ipw
    from IPython.display import display, HTML, clear_output, update_display
    
    #progress bar
    progress = ipw.IntProgress(value=0, min=0, max=5, step=1 , description='Processing: ')
    display(progress)
    
    #ignore warnings
    import warnings
    warnings.filterwarnings('ignore') 
    
    #general dependencies
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    
    progress.value += 1
    
    #defining estimator as model locally
    model = estimator
    
    progress.value += 1
    
    if plot == 'residuals':
        
        from yellowbrick.regressor import ResidualsPlot
        progress.value += 1
        visualizer = ResidualsPlot(model)
        progress.value += 1
        visualizer.score(X_test, y_test)  # Evaluate the model on the test data
        progress.value += 1
        clear_output()
        visualizer.show()
        
        
    elif plot == 'error':
        from yellowbrick.regressor import PredictionError
        progress.value += 1
        visualizer = PredictionError(model)
        progress.value += 1
        visualizer.score(X_test, y_test)
        progress.value += 1
        clear_output()
        visualizer.show()
        
    elif plot == 'cooks':
        from yellowbrick.regressor import CooksDistance
        progress.value += 1
        visualizer = CooksDistance()
        progress.value += 1
        visualizer.fit(X, y)
        progress.value += 1
        clear_output()
        visualizer.show() 
        
    elif plot == 'rfe':
        
        from yellowbrick.model_selection import RFECV 
        progress.value += 1
        visualizer = RFECV(model, cv=10)
        progress.value += 1
        visualizer.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        visualizer.poof()
        
    elif plot == 'learning':
        
        from yellowbrick.model_selection import LearningCurve
        progress.value += 1
        sizes = np.linspace(0.3, 1.0, 10)  
        visualizer = LearningCurve(model, cv=10, train_sizes=sizes, n_jobs=1, random_state=seed)
        progress.value += 1
        visualizer.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        visualizer.poof()
    
    elif plot == 'manifold':
        
        from yellowbrick.features import Manifold
        
        progress.value += 1
        X_train_transformed = X_train.select_dtypes(include='float64') 
        visualizer = Manifold(manifold='tsne', random_state = seed)
        progress.value += 1
        visualizer.fit_transform(X_train_transformed, y_train)
        progress.value += 1
        clear_output()
        visualizer.poof()

    elif plot == 'vc':
        
        model_name = str(model).split("(")[0]
        
        not_allowed = ['LinearRegression', 'PassiveAggressiveRegressor']
        
        if model_name in not_allowed:
            clear_output()
            sys.exit('(Value Error): Estimator not supported in Validation Curve Plot.')
        
        elif model_name == 'GradientBoostingRegressor':
            param_name='alpha'
            param_range = np.arange(0.1,1,0.1)
        
        #lasso/ridge/en/llar/huber/kr/mlp/br/ard
        elif hasattr(model, 'alpha'):
            param_name='alpha'
            param_range = np.arange(0,1,0.1)
            
        elif hasattr(model, 'alpha_1'):
            param_name='alpha_1'
            param_range = np.arange(0,1,0.1)
            
        #par/svm
        elif hasattr(model, 'C'):
            param_name='C'
            param_range = np.arange(1,11)
            
        #tree based models (dt/rf/et)
        elif hasattr(model, 'max_depth'):
            param_name='max_depth'
            param_range = np.arange(1,11)
        
        #knn
        elif hasattr(model, 'n_neighbors'):
            param_name='n_neighbors'
            param_range = np.arange(1,11)         
            
        #Bagging / Boosting (ada/gbr)
        elif hasattr(model, 'n_estimators'):
            param_name='n_estimators'
            param_range = np.arange(1,100,10)   

        #Bagging / Boosting (ada/gbr)
        elif hasattr(model, 'n_nonzero_coefs'):
            param_name='n_nonzero_coefs'
            if len(X_train.columns) >= 10:
                param_max = 11
            else:
                param_max = len(X_train.columns)+1
            param_range = np.arange(1,param_max,1) 
            
        elif hasattr(model, 'eps'):
            param_name='eps'
            param_range = np.arange(0,1,0.1)   
            
        elif hasattr(model, 'max_subpopulation'):
            param_name='max_subpopulation'
            param_range = np.arange(1000,20000,2000)   

        elif hasattr(model, 'min_samples'):
            param_name='min_samples'
            param_range = np.arange(0.01,1,0.1)  
            
        else: 
            clear_output()
            sys.exit('(Value Error): Estimator not supported in Validation Curve Plot.')
        
            
        progress.value += 1
            
        from yellowbrick.model_selection import ValidationCurve
        viz = ValidationCurve(model, param_name=param_name, param_range=param_range,cv=10, 
                              random_state=seed)
        viz.fit(X_train, y_train)
        progress.value += 1
        clear_output()
        viz.poof()
        
    elif plot == 'feature':
        if hasattr(estimator, 'coef_'):
            variables = abs(model.coef_)
        else:
            variables = abs(model.feature_importances_)
        col_names = np.array(X_train.columns)
        coef_df = pd.DataFrame({'Variable': X_train.columns, 'Value': variables})
        progress.value += 1
        sorted_df = coef_df.sort_values(by='Value', ascending=False)
        sorted_df = sorted_df.head(10)
        sorted_df = sorted_df.sort_values(by='Value')
        my_range=range(1,len(sorted_df.index)+1)
        plt.figure(figsize=(8,5))
        plt.hlines(y=my_range, xmin=0, xmax=sorted_df['Value'], color='skyblue')
        plt.plot(sorted_df['Value'], my_range, "o")
        plt.yticks(my_range, sorted_df['Variable'])
        progress.value += 1
        plt.title("Feature Importance Plot")
        plt.xlabel('Variable Importance')
        plt.ylabel('Features') 
        progress.value += 1
        clear_output()
   
    elif plot == 'parameter':
        
        clear_output()
        param_df = pd.DataFrame.from_dict(estimator.get_params(estimator), orient='index', columns=['Parameters'])
        display(param_df)



def interpret_model(estimator,
                   plot = 'summary',
                   feature = None, 
                   observation = None):
    
    
    """
          
    Description:
    ------------
    This function takes a trained model object and returns an interpretation plot 
    based on the test / hold-out set. It only supports tree based algorithms. 

    This function is implemented based on the SHAP (SHapley Additive exPlanations),
    which is a unified approach to explain the output of any machine learning model. 
    SHAP connects game theory with local explanations.

    For more information : https://shap.readthedocs.io/en/latest/

        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        dt = create_model('dt')
        
        interpret_model(dt)

        This will return a summary interpretation plot of Decision Tree model.

    Parameters
    ----------
    estimator : object, default = none
    A trained tree based model object should be passed as an estimator. 

    plot : string, default = 'summary'
    other available options are 'correlation' and 'reason'.

    feature: string, default = None
    This parameter is only needed when plot = 'correlation'. By default feature is 
    set to None which means the first column of the dataset will be used as a variable. 
    A feature parameter must be passed to change this.

    observation: integer, default = None
    This parameter only comes into effect when plot is set to 'reason'. If no observation
    number is provided, it will return an analysis of all observations with the option
    to select the feature on x and y axes through drop down interactivity. For analysis at
    the sample level, an observation parameter must be passed with the index value of the
    observation in test / hold-out set. 

    Returns:
    --------

    Visual Plot:  Returns the visual plot.
    -----------   Returns the interactive JS plot when plot = 'reason'.

    Warnings:
    ---------
    None
     
         
         
    """
    
    
    
    '''
    Error Checking starts here
    
    '''
    
    import sys
    
    #allowed models
    allowed_models = ['RandomForestRegressor',
                      'DecisionTreeRegressor',
                      'ExtraTreesRegressor',
                      'GradientBoostingRegressor',
                      'XGBRegressor',
                      'LGBMRegressor',
                      'CatBoostRegressor']
    
    model_name = str(estimator).split("(")[0]

    #Statement to find CatBoost and change name :
    if model_name.find("catboost.core.CatBoostRegressor") != -1:
        model_name = 'CatBoostRegressor'
    
    if model_name not in allowed_models:
        sys.exit('(Type Error): This function only supports tree based models.')
        
    #plot type
    allowed_types = ['summary', 'correlation', 'reason']
    if plot not in allowed_types:
        sys.exit("(Value Error): type parameter only accepts 'summary', 'correlation' or 'reason'.")   
           
    
    '''
    Error Checking Ends here
    
    '''
        
    
    #general dependencies
    import numpy as np
    import pandas as pd
    import shap
    
    #storing estimator in model variable
    model = estimator
    
    if plot == 'summary':
        
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test)
        shap.summary_plot(shap_values, X_test)
                              
    elif plot == 'correlation':
        
        if feature == None:
            
            dependence = X_test.columns[0]
            
        else:
            
            dependence = feature
        
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_test) 
        shap.dependence_plot(dependence, shap_values, X_test)
        
    elif plot == 'reason':
     
        if observation is None:

            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test)
            shap.initjs()
            return shap.force_plot(explainer.expected_value, shap_values, X_test)

        else:

            row_to_show = observation
            data_for_prediction = X_test.iloc[row_to_show]
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_test)
            shap.initjs()
            return shap.force_plot(explainer.expected_value, shap_values[row_to_show,:], X_test.iloc[row_to_show,:])



def evaluate_model(estimator):
    
    
    """
          
    Description:
    ------------
    This function displays a user interface for all of the available plots for 
    a given estimator. It internally uses the plot_model() function. 
    
        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        evaluate_model(lr)
        
        This will display the User Interface for all of the plots for a given
        estimator.

    Parameters
    ----------
    estimator : object, default = none
    A trained model object should be passed as an estimator. 

    Returns:
    --------

    User Interface:  Displays the user interface for plotting.
    --------------

    Warnings:
    ---------
    None
      
         
         
    """
        
        
    from ipywidgets import widgets
    from ipywidgets.widgets import interact, fixed, interact_manual

    a = widgets.ToggleButtons(
                            options=[('Hyperparameters', 'parameter'),
                                     ('Residuals Plot', 'residuals'), 
                                     ('Prediction Error Plot', 'error'), 
                                     ('Cooks Distance Plot', 'cooks'),
                                     ('Recursive Feature Selection', 'rfe'),
                                     ('Learning Curve', 'learning'),
                                     ('Validation Curve', 'vc'),
                                     ('Manifold Learning', 'manifold'),
                                     ('Feature Importance', 'feature')
                                    ],

                            description='Plot Type:',

                            disabled=False,

                            button_style='', # 'success', 'info', 'warning', 'danger' or ''

                            icons=['']
    )
    
  
    d = interact(plot_model, estimator = fixed(estimator), plot = a)



def finalize_model(estimator):
    
    """
          
    Description:
    ------------
    This function fits the estimator onto the complete dataset passed during the
    setup() stage. The purpose of this function is to prepare for final model
    deployment after experimentation. 
    
        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        final_lr = finalize_model(lr)
        
        This will return the final model object fitted to complete dataset. 

    Parameters
    ----------
    estimator : object, default = none
    A trained model object should be passed as an estimator. 

    Returns:
    --------

    Model:  Trained model object fitted on complete dataset.
    ------   

    Warnings:
    ---------
    - If the model returned by finalize_model(), is used on predict_model() without 
      passing a new unseen dataset, then the information grid printed is misleading 
      as the model is trained on the complete dataset including test / hold-out sample. 
      Once finalize_model() is used, the model is considered ready for deployment and
      should be used on new unseens dataset only.
       
         
    """
    
    #import depedencies
    from copy import deepcopy
    
    if type(estimator) is list:
        
        if type(estimator[0]) is not list:
            
            """
            Single Layer Stacker
            """
            
            stacker_final = deepcopy(estimator)
            stack_restack = stacker_final.pop()
            stack_meta_final = stacker_final.pop()
            
            model_final = stack_models(estimator_list = stacker_final, 
                                       meta_model = stack_meta_final, 
                                       restack = stack_restack,
                                       finalize=True, 
                                       verbose=False)
            
        else:
            
            """
            multiple layer stacknet
            """
            
            stacker_final = deepcopy(estimator)
            stack_restack = stacker_final.pop()
            stack_meta_final = stacker_final.pop()
            
            model_final = create_stacknet(estimator_list = stacker_final,
                                          meta_model = stack_meta_final,
                                          restack = stack_restack,
                                          finalize = True,
                                          verbose = False)

    else:
        model_final = deepcopy(estimator)
        model_final.fit(X,y)
    
    #storing into experiment
    model_name = str(estimator).split("(")[0]
    model_name = 'Final ' + model_name
    tup = (model_name,model_final)
    experiment__.append(tup)
    
    return model_final


def save_model(model, model_name, verbose=True):
    
    """
          
    Description:
    ------------
    This function saves the transformation pipeline and trained model object 
    into the current active directory as a pickle file for later use. 
    
        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        save_model(lr, 'lr_model_23122019')
        
        This will save the transformation pipeline and model as a binary pickle
        file in the current directory. 

    Parameters
    ----------
    model : object, default = none
    A trained model object should be passed as an estimator. 
    
    model_name : string, default = none
    Name of pickle file to be passed as a string.
    
    verbose: Boolean, default = True
    Success message is not printed when verbose is set to False.

    Returns:
    --------    
    Success Message
    
    Warnings:
    ---------
    None
      
            
    """
    
    import joblib
    model_name = model_name + '.pkl'
    joblib.dump(model, model_name)
    if verbose:
        print('Transformation Pipeline and Model Succesfully Saved')


def load_model(model_name, verbose=True):
    
    """
          
    Description:
    ------------
    This function loads a previously saved transformation pipeline and model 
    from the current active directory into the current python environment. 
    Load object must be a pickle file.
    
        Example:
        --------
        saved_lr = load_model('lr_model_23122019')
        
        This will load the previously saved model in saved_lr variable. The file 
        must be in the current directory.

    Parameters
    ----------
    model_name : string, default = none
    Name of pickle file to be passed as a string.
    
    verbose: Boolean, default = True
    Success message is not printed when verbose is set to False.

    Returns:
    --------    
    Success Message
    
    Warnings:
    ---------
    None
      
         
         
    """
        
        
    import joblib
    model_name = model_name + '.pkl'
    if verbose:
        print('Transformation Pipeline and Model Sucessfully Loaded')
    return joblib.load(model_name)


def save_experiment(experiment_name=None):
    
        
    """
          
    Description:
    ------------
    This function saves the entire experiment into the current active directory. 
    All outputs using pycaret are internally saved into a binary list which is
    pickilized when save_experiment() is used. 
    
        Example:
        --------
        save_experiment()
        
        This will save the entire experiment into the current active directory. By 
        default, the name of the experiment will use the session_id generated during 
        setup(). To use a custom name, a string must be passed to the experiment_name 
        param. For example:
        
        save_experiment('experiment_23122019')

    Parameters
    ----------
    experiment_name : string, default = none
    Name of pickle file to be passed as a string.

    Returns:
    --------    
    Success Message
    
    Warnings:
    ---------
    None
      
         
         
    """
    
    #general dependencies
    import joblib
    global experiment__
    
    #defining experiment name
    if experiment_name is None:
        experiment_name = 'experiment_' + str(seed)
        
    else:
        experiment_name = experiment_name  
        
    experiment_name = experiment_name + '.pkl'
    joblib.dump(experiment__, experiment_name)
    
    print('Experiment Succesfully Saved')


def load_experiment(experiment_name):
    
    """
          
    Description:
    ------------
    This function loads a previously saved experiment from the current active 
    directory into current python environment. Load object must be a pickle file.
    
        Example:
        --------
        saved_experiment = load_experiment('experiment_23122019')
        
        This will load the entire experiment pipeline into the object saved_experiment.
        The experiment file must be in current directory.
        
    Parameters
    ----------
    experiment_name : string, default = none
    Name of pickle file to be passed as a string.

    Returns:
    --------    
    Information Grid containing details of saved objects in experiment pipeline.
    
    Warnings:
    ---------
    None
      
          
    """
    
    #general dependencies
    import joblib
    import pandas as pd
    
    experiment_name = experiment_name + '.pkl'
    temp = joblib.load(experiment_name)
    
    name = []
    exp = []

    for i in temp:
        name.append(i[0])
        exp.append(i[-1])

    ind = pd.DataFrame(name, columns=['Object'])
    display(ind)

    return exp




def predict_model(estimator, 
                  data=None,
                  round=4):
    
    """
       
    Description:
    ------------
    This function is used to predict new data using a trained estimator. It accepts
    an estimator created using one of the function in pycaret that returns a trained 
    model object or a list of trained model objects created using stack_models() or 
    create_stacknet(). New unseen data can be passed to data param as pandas Dataframe. 
    If data is not passed, the test / hold-out set separated at the time of setup() is
    used to generate predictions. 
    
        Example:
        --------
        from pycaret.datasets import get_data
        boston = get_data('boston')
        experiment_name = setup(data = boston,  target = 'medv')
        lr = create_model('lr')
        
        lr_predictions_holdout = predict_model(lr)
        
    Parameters
    ----------
    estimator : object or list of objects, default = None
    
    data : {array-like, sparse matrix}, shape (n_samples, n_features) where n_samples 
    is the number of samples and n_features is the number of features. All features 
    used during training must be present in the new dataset.
    
    round: integer, default = 4
    Number of decimal places the predicted labels will be rounded to.
    
    Returns:
    --------

    info grid:    Information grid is printed when data is None.
    ----------      
    
    Warnings:
    ---------
    - if the estimator passed is created using finalize_model() then the metrics 
      printed in the information grid maybe misleading as the model is trained on
      the complete dataset including the test / hold-out set. Once finalize_model() 
      is used, the model is considered ready for deployment and should be used on new 
      unseen datasets only.
      
    
    
    """
    
    #testing
    #no active tests
    
    #general dependencies
    import numpy as np
    import pandas as pd
    import re
    from sklearn import metrics
    from copy import deepcopy
    
    #check if estimator is string, then load model
    if type(estimator) is str:
        estimator = load_model(estimator, verbose=False)
        
    #dataset
    if data is None:
        
        Xtest = X_test.copy()
        ytest = y_test.copy()
        X_test_ = X_test.copy()
        y_test_ = y_test.copy()
        
        Xtest.reset_index(drop=True, inplace=True)
        ytest.reset_index(drop=True, inplace=True)
        X_test_.reset_index(drop=True, inplace=True)
        y_test_.reset_index(drop=True, inplace=True)
        
        model = estimator
        
    else:
        
        estimator_ = deepcopy(estimator)
        
        if type(estimator_) is list:
            
            if 'sklearn.pipeline.Pipeline' in str(type(estimator_[0])):
            
                prep_pipe_transformer = estimator_.pop(0)
                model = estimator_[0]
                estimator = estimator_[0]
                
            else:
                
                prep_pipe_transformer = prep_pipe
                model = estimator
                estimator = estimator
            
        else:
            
            prep_pipe_transformer = prep_pipe
            model = estimator
            estimator = estimator
        
        try:
            model = finalize_model(estimator)
        except:
            model = estimator
            
        Xtest = prep_pipe_transformer.transform(data)                     
        X_test_ = data.copy() #original concater
        
        Xtest.reset_index(drop=True, inplace=True)
        X_test_.reset_index(drop=True, inplace=True)
        
    
    if type(estimator) is list:
        
        if type(estimator[0]) is list:
        
            """
            Multiple Layer Stacking
            """
            
            #utility
            stacker = model.copy()
            restack = stacker.pop()
            #stacker_method = stacker.pop()
            #stacker_method = stacker_method[0]
            stacker_meta = stacker.pop()
            stacker_base = stacker.pop(0)

            #base model names
            base_model_names = []

            #defining base_level_names
            for i in stacker_base:
                b = str(i).split("(")[0]
                base_model_names.append(b)

            base_level_fixed = []

            for i in base_model_names:
                if 'CatBoostRegressor' in i:
                    a = 'CatBoostRegressor'
                    base_level_fixed.append(a)
                else:
                    base_level_fixed.append(i)

            base_level_fixed_2 = []

            counter = 0
            for i in base_level_fixed:
                s = str(i) + '_' + 'BaseLevel_' + str(counter)
                base_level_fixed_2.append(s)
                counter += 1

            base_level_fixed = base_level_fixed_2

            """
            base level predictions
            """
            base_pred = []
            for i in stacker_base:
                a = i.predict(Xtest) #change
                base_pred.append(a)

            base_pred_df = pd.DataFrame()
            for i in base_pred:
                a = pd.DataFrame(i)
                base_pred_df = pd.concat([base_pred_df, a], axis=1)

            base_pred_df.columns = base_level_fixed
            
            base_pred_df_no_restack = base_pred_df.copy()
            base_pred_df = pd.concat([Xtest,base_pred_df], axis=1)
            

            """
            inter level predictions
            """

            inter_pred = []
            combined_df = pd.DataFrame(base_pred_df)

            inter_counter = 0

            for level in stacker:

                inter_pred_df = pd.DataFrame()

                model_counter = 0 

                for model in level:
                    try:
                        if inter_counter == 0:
                            try:
                                p = model.predict(base_pred_df)
                            except:
                                p = model.predict(base_pred_df_no_restack)
                            
                        else:
                            p = model.predict(last_level_df)
            
                    except:
                        p = model.predict(combined_df)

                    p = pd.DataFrame(p)

                    col = str(model).split("(")[0]
                    if 'CatBoostRegressor' in col:
                        col = 'CatBoostRegressor'
                    col = col + '_InterLevel_' + str(inter_counter) + '_' + str(model_counter)
                    p.columns = [col]

                    inter_pred_df = pd.concat([inter_pred_df, p], axis=1)

                    model_counter += 1

                last_level_df = inter_pred_df.copy()

                inter_counter += 1

                combined_df = pd.concat([combined_df,inter_pred_df], axis=1)

            """
            meta final predictions
            """

            #final meta predictions
            try:
                pred_ = stacker_meta.predict(combined_df)
            except:
                pred_ = stacker_meta.predict(inter_pred_df)

            if data is None:
                mae = metrics.mean_absolute_error(ytest,pred_)
                mse = metrics.mean_squared_error(ytest,pred_)
                rmse = np.sqrt(mse)
                r2 = metrics.r2_score(ytest,pred_)
                max_error_ = metrics.max_error(ytest,pred_)


                df_score = pd.DataFrame( {'Model' : 'Stacking Regressor', 'MAE' : [mae], 'MSE' : [mse], 'RMSE' : [rmse], 
                                          'R2' : [r2], 'ME' : [max_error_]})
                df_score = df_score.round(round)
                display(df_score)
        
            label = pd.DataFrame(pred_)
            label = label.round(round)
            label.columns = ['Label']
            label['Label']=label['Label']

            if data is None:
                X_test_ = pd.concat([Xtest,ytest,label], axis=1)
            else:
                X_test_ = pd.concat([X_test_,label], axis=1)

        else:
            
            """
            Single Layer Stacking
            """
            
            #copy
            stacker = model.copy()
            
            #restack
            restack = stacker.pop()

            #separate metamodel
            meta_model = stacker.pop()

            model_names = []
            for i in stacker:
                model_names = np.append(model_names, str(i).split("(")[0])

            model_names_fixed = []

            for i in model_names:
                if 'CatBoostRegressor' in i:
                    a = 'CatBoostRegressor'
                    model_names_fixed.append(a)
                else:
                    model_names_fixed.append(i)

            model_names = model_names_fixed

            model_names_fixed = []
            counter = 0

            for i in model_names:
                s = str(i) + '_' + str(counter)
                model_names_fixed.append(s)
                counter += 1

            model_names = model_names_fixed

            base_pred = []

            for i in stacker:
                p = i.predict(Xtest) #change
                base_pred.append(p)

            df = pd.DataFrame()
            for i in base_pred:
                i = pd.DataFrame(i)
                df = pd.concat([df,i], axis=1)

            df.columns = model_names
            
            df_restack = pd.concat([Xtest,df], axis=1) #change

            #ytest = y_test

            #meta predictions starts here

            #restacking check
            try:
                pred_ = meta_model.predict(df)
            except:
                pred_ = meta_model.predict(df_restack) 
                

            if data is None:
                mae = metrics.mean_absolute_error(ytest,pred_)
                mse = metrics.mean_squared_error(ytest,pred_)
                rmse = np.sqrt(mse)
                r2 = metrics.r2_score(ytest,pred_)
                max_error_ = metrics.max_error(ytest,pred_)


                df_score = pd.DataFrame( {'Model' : 'Stacking Regressor', 'MAE' : [mae], 'MSE' : [mse], 'RMSE' : [rmse], 
                                          'R2' : [r2], 'ME' : [max_error_]})
                df_score = df_score.round(round)
                display(df_score)
                
            label = pd.DataFrame(pred_)
            label = label.round(round)
            label.columns = ['Label']
            label['Label']=label['Label']

            if data is None:
                X_test_ = pd.concat([Xtest,ytest,label], axis=1)
            else:
                X_test_ = pd.concat([X_test_,label], axis=1)


    else:
        
        #model name
        full_name = str(model).split("(")[0]
        def putSpace(input):
            words = re.findall('[A-Z][a-z]*', input)
            words = ' '.join(words)
            return words  
        full_name = putSpace(full_name)

        if full_name == 'A R D Regression':
            full_name = 'Automatic Relevance Determination'

        elif full_name == 'M L P Regressor':
            full_name = 'MLP Regressor'

        elif full_name == 'R A N S A C Regressor':
            full_name = 'RANSAC Regressor'

        elif full_name == 'S V R':
            full_name = 'Support Vector Regressor'
            
        elif full_name == 'Lars':
            full_name = 'Least Angle Regression'
            
        elif full_name == 'X G B Regressor':
            full_name = 'Extreme Gradient Boosting Regressor'

        elif full_name == 'L G B M Regressor':
            full_name = 'Light Gradient Boosting Machine'

        elif 'Cat Boost Regressor' in full_name:
            full_name = 'CatBoost Regressor'

        #prediction starts here
        pred_ = model.predict(Xtest)
        
        if data is None:
            mae = metrics.mean_absolute_error(ytest,pred_)
            mse = metrics.mean_squared_error(ytest,pred_)
            rmse = np.sqrt(mse)
            r2 = metrics.r2_score(ytest,pred_)
            max_error_ = metrics.max_error(ytest,pred_)

            
            df_score = pd.DataFrame( {'Model' : [full_name], 'MAE' : [mae], 'MSE' : [mse], 'RMSE' : [rmse], 
                                      'R2' : [r2], 'ME' : [max_error_]})
            df_score = df_score.round(4)
            display(df_score)
        
            label = pd.DataFrame(pred_)
            label = label.round(round)
            label.columns = ['Label']
            label['Label']=label['Label']

        label = pd.DataFrame(pred_)
        label = label.round(round)
        label.columns = ['Label']
        label['Label']=label['Label']
        
        if data is None:
            X_test_ = pd.concat([Xtest,ytest,label], axis=1)
        else:
            X_test_ = pd.concat([X_test_,label], axis=1)

    return X_test_